#!/usr/bin/env python3
"""
Re-verifies every entry in index.html against its official source (using
Claude's web search) and rewrites the file in place if anything needs to
change. Designed to run inside the GitHub Action at
.github/workflows/refresh.yml — do not run this against a file you haven't
backed up / committed, since it overwrites index.html directly.

Requires: ANTHROPIC_API_KEY environment variable (set as a repo secret).

NOTE: this script was written without the ability to execute it end-to-end
(no network access to api.anthropic.com from the environment that authored
it). Test it via the workflow's manual "Run workflow" button before relying
on the schedule, and check the Action's logs on first run.
"""

import os
import re
import sys
import datetime

import anthropic

HTML_PATH = "index.html"
MIN_EXPECTED_CARDS = 20  # sanity check — the site has 20 entries as of writing
START_MARKER = "<<<HTML_START>>>"
END_MARKER = "<<<HTML_END>>>"

SYSTEM_PROMPT = """\
You maintain the source code of KnowHow, a static HTML directory that helps \
Indian immigrants abroad find official government services — passport \
renewal, OCI, voting rights, emergencies, tax/banking, and more. Every entry \
links to an official government or mission source and includes step-by-step \
"how to apply" guidance (steps, required documents, conditions).

Your job each time you're run: verify the content is still accurate by \
checking the official sources with web search, and output a corrected \
version of the ENTIRE file.

Rules — follow these exactly:
1. Preserve the HTML structure, CSS, and JavaScript exactly as given unless \
something is actually wrong. Do not redesign, reformat, reorder, or rewrite \
anything that doesn't need a factual correction.
2. Only change: dead or moved links, outdated steps/eligibility/documents, \
factually wrong statements, or a service that has been renamed/replaced. If \
you can't confirm something changed, leave it alone.
3. Do not remove or reorder any of the 20 cards or their sections. Do not \
change the site's name, design, or copy tone.
4. Always update the text inside the element with id="verifiedDate" to \
today's real date, in the same "27 Aug 2026"-style format already used — \
even if nothing else changed.
5. If you find something that needs a human's judgment call rather than a \
factual fix, leave the content as-is (don't guess) — flag it in your final \
reply after the closing marker instead.
6. Output ONLY the complete corrected HTML file, and nothing else, wrapped \
exactly like this with no text before the start marker:

<<<HTML_START>>>
...the complete file, starting with <title> and ending with </script>...
<<<HTML_END>>>

Anything you want to flag for human review goes AFTER the end marker.
"""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        current_html = f.read()

    client = anthropic.Anthropic(api_key=api_key)

    today = datetime.datetime.utcnow().strftime("%d %b %Y")

    response = client.messages.create(
        # Pin to a specific dated model in your Anthropic console if you want
        # reproducibility; "latest" aliases can change underneath you.
        model="claude-sonnet-4-5",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 40,
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today's date is {today}. Here is the current "
                    f"index.html:\n\n{current_html}\n\n"
                    "Verify it against official sources and output the "
                    "corrected file per your instructions."
                ),
            }
        ],
    )

    # Concatenate all text blocks in the final response (server-side tool
    # calls/results are handled by the API within this single call; we just
    # need the text Claude produced at the end).
    full_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    if START_MARKER not in full_text or END_MARKER not in full_text:
        print("ERROR: response did not contain the expected markers — aborting without writing.", file=sys.stderr)
        print("---- raw response (truncated) ----", file=sys.stderr)
        print(full_text[:2000], file=sys.stderr)
        sys.exit(1)

    new_html = full_text.split(START_MARKER, 1)[1].split(END_MARKER, 1)[0].strip()
    notes = full_text.split(END_MARKER, 1)[1].strip() if END_MARKER in full_text else ""

    # --- Sanity checks before overwriting the live file ---
    problems = []
    if len(new_html) < len(current_html) * 0.6:
        problems.append(f"new file is suspiciously short ({len(new_html)} vs {len(current_html)} chars)")
    if new_html.count('<article class="card') < MIN_EXPECTED_CARDS:
        problems.append(f"fewer than {MIN_EXPECTED_CARDS} cards found in output")
    if "<title>" not in new_html or "</script>" not in new_html:
        problems.append("missing <title> or closing </script> — looks truncated")

    if problems:
        print("ERROR: refusing to write output — failed sanity checks:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)

    print("index.html refreshed successfully.")
    if notes:
        print("\nNotes from this run (for human review):\n" + notes)


if __name__ == "__main__":
    main()
