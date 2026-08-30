# -*- coding: utf-8 -*-
"""
Generates index.html for Uthavi from structured, multi-language data.
Run: python3 build_site.py   ->  writes ../index.html (repo root)
"""
import html as _html
import os

LANGS = ["en", "hi", "ta", "te", "ml"]
LANG_LABEL = {"en": "English", "hi": "हिन्दी", "ta": "தமிழ்", "te": "తెలుగు", "ml": "മലയാളം"}
LANG_SHORT = {"en": "EN", "hi": "हि", "ta": "த", "te": "తె", "ml": "മ"}
LANG_RAIL_ORDER = ["en", "ta", "ml", "te", "hi"]  # display order of the language chips only; data keys above are unaffected

PASS_CODES = ["EP", "SPass", "WP", "DP"]  # Singapore-only: Employment Pass, S Pass, Work Permit, Dependant's Pass
PASS_UI_KEY = {"EP": "pass_ep", "SPass": "pass_spass", "WP": "pass_wp", "DP": "pass_dp"}

# ---------------------------------------------------------------------------
# UI strings (chrome: labels, buttons, section notes, footer, notice)
# ---------------------------------------------------------------------------
UI = {
    "brand_tag": {
        "en": "Overseas Indian Services Directory",
        "hi": "प्रवासी भारतीय सेवा निर्देशिका",
        "ta": "வெளிநாட்டு இந்திய சேவைகள் அடைவு",
        "te": "విదేశీ భారతీయ సేవల డైరెక్టరీ",
        "ml": "വിദേശ ഇന്ത്യൻ സേവന ഡയറക്ടറി",
    },
    "entries_curated": {
        "en": "Entries curated", "hi": "प्रविष्टियाँ", "ta": "பதிவுகள்", "te": "నమోదులు", "ml": "എൻട്രികൾ",
    },
    "snapshot_verified": {
        "en": "Snapshot verified", "hi": "जानकारी सत्यापित",
        "ta": "தகவல் சரிபார்க்கப்பட்டது", "te": "సమాచారం ధృవీకరించబడింది", "ml": "വിവരം സ്ഥിരീകരിച്ചു",
    },
    "lede": {
        "en": "A link to a government portal isn't enough on its own — so every entry here also walks through the actual steps, documents, and conditions to get it done: not just where to go, but the know-how to get it done once you're there. A single map for the paperwork of living abroad while staying an Indian citizen — passports, OCI, voting rights, emergencies, taxes.",
        "hi": "सिर्फ़ किसी सरकारी पोर्टल का लिंक काफ़ी नहीं है — इसलिए यहाँ हर प्रविष्टि में असली चरण, ज़रूरी दस्तावेज़ और शर्तें भी बताई गई हैं: सिर्फ़ यह नहीं कि कहाँ जाना है, बल्कि वहाँ पहुँचकर काम कैसे पूरा करना है। विदेश में रहते हुए भारतीय नागरिकता से जुड़े हर काग़ज़ी काम के लिए एक ही जगह — पासपोर्ट, OCI, मतदान अधिकार, आपातकाल, कर।",
        "ta": "அரசு போர்ட்டலுக்கான இணைப்பு மட்டும் போதாது — அதனால் இங்குள்ள ஒவ்வொரு பதிவும் உண்மையான படிகள், ஆவணங்கள், நிபந்தனைகள் ஆகியவற்றையும் விளக்குகிறது: எங்கு செல்ல வேண்டும் என்பது மட்டுமல்ல, அங்கு சென்றபின் எப்படி முடிக்க வேண்டும் என்பதும். வெளிநாட்டில் வாழ்ந்தாலும் இந்தியக் குடியுரிமையுடன் தொடர்புடைய அனைத்து ஆவணப் பணிகளுக்கும் ஒரே இடம் — பாஸ்போர்ட், OCI, வாக்குரிமை, அவசரநிலை, வரி.",
        "te": "ప్రభుత్వ పోర్టల్ లింక్ మాత్రమే సరిపోదు — అందుకే ఇక్కడ ప్రతి నమోదులో అసలైన దశలు, అవసరమైన పత్రాలు, షరతులు కూడా వివరించబడ్డాయి: ఎక్కడికి వెళ్లాలో మాత్రమే కాదు, అక్కడికి వెళ్లాక పని ఎలా పూర్తి చేయాలో కూడా. విదేశాల్లో ఉంటూ భారత పౌరసత్వాన్ని కొనసాగించే ప్రతి కాగితం పనికి ఒకే వేదిక — పాస్‌పోర్ట్, OCI, ఓటు హక్కు, అత్యవసర సాయం, పన్ను.",
        "ml": "ഒരു സർക്കാർ പോർട്ടലിന്റെ ലിങ്ക് മാത്രം പോരാ — അതിനാൽ ഇവിടെ ഓരോ എൻട്രിയും യഥാർത്ഥ ഘട്ടങ്ങൾ, ആവശ്യമായ രേഖകൾ, നിബന്ധനകൾ എന്നിവയും വിശദീകരിക്കുന്നു: എവിടെ പോകണം എന്നത് മാത്രമല്ല, അവിടെ എത്തിയാൽ എങ്ങനെ പൂർത്തിയാക്കാം എന്നതും. വിദേശത്ത് ജീവിക്കുമ്പോഴും ഇന്ത്യൻ പൗരത്വം നിലനിർത്തുന്നതിനുള്ള എല്ലാ രേഖാ ജോലികൾക്കുമുള്ള ഒറ്റ ഇടം — പാസ്‌പോർട്ട്, OCI, വോട്ടവകാശം, അടിയന്തരാവസ്ഥ, നികുതി.",
    },
    "country_india": {"en": "India — general", "hi": "भारत — सामान्य", "ta": "இந்தியா — பொது", "te": "భారత్ — సాధారణ", "ml": "ഇന്ത്യ — പൊതു"},
    "country_singapore": {"en": "Singapore — live", "hi": "सिंगापुर — उपलब्ध", "ta": "சிங்கப்பூர் — செயலில்", "te": "సింగపూర్ — అందుబాటులో", "ml": "സിംഗപ്പൂർ — ലഭ്യം"},
    "country_suggest": {"en": "+ suggest one", "hi": "+ सुझाव दें", "ta": "+ ஒன்றை பரிந்துரைக்க", "te": "+ ఒకటి సూచించండి", "ml": "+ ഒന്ന് നിർദ്ദേശിക്കുക"},
    "search_placeholder": {
        "en": "Search “lost passport”, “PCC”, “vote from abroad”…",
        "hi": "खोजें “खोया पासपोर्ट”, “PCC”, “विदेश से मतदान”…",
        "ta": "தேடுங்கள் “பாஸ்போர்ட் தொலைந்தது”, “PCC”, “வெளிநாட்டிலிருந்து வாக்களித்தல்”…",
        "te": "“పాస్‌పోర్ట్ పోయింది”, “PCC”, “విదేశం నుండి ఓటు” అని వెతకండి…",
        "ml": "“പാസ്‌പോർട്ട് നഷ്ടപ്പെട്ടു”, “PCC”, “വിദേശത്ത് നിന്ന് വോട്ട്” എന്ന് തിരയുക…",
    },
    "results_shown": {
        "en": "{shown} of {total} shown", "hi": "{total} में से {shown} दिख रहे हैं",
        "ta": "{total} இல் {shown} காட்டப்படுகிறது", "te": "{total} లో {shown} చూపబడ్డాయి",
        "ml": "{total} ൽ {shown} കാണിക്കുന്നു",
    },
    "how_to_apply": {"en": "How to apply", "hi": "कैसे आवेदन करें", "ta": "எப்படி விண்ணப்பிக்க வேண்டும்", "te": "ఎలా దరఖాస్తు చేయాలి", "ml": "എങ്ങനെ അപേക്ഷിക്കാം"},
    "how_to_use": {"en": "How to use it", "hi": "इसका उपयोग कैसे करें", "ta": "இதை எப்படி பயன்படுத்துவது", "te": "దీన్ని ఎలా ఉపయోగించాలి", "ml": "ഇത് എങ്ങനെ ഉപയോഗിക്കാം"},
    "what_to_know": {"en": "What to know", "hi": "क्या जानना ज़रूरी है", "ta": "என்ன தெரிந்திருக்க வேண்டும்", "te": "ఏమి తెలుసుకోవాలి", "ml": "എന്ത് അറിഞ്ഞിരിക്കണം"},
    "steps": {"en": "Steps", "hi": "चरण", "ta": "படிகள்", "te": "దశలు", "ml": "ഘട്ടങ്ങൾ"},
    "key_facts": {"en": "Key facts", "hi": "मुख्य तथ्य", "ta": "முக்கிய தகவல்கள்", "te": "ముఖ్య వాస్తవాలు", "ml": "പ്രധാന വസ്തുതകൾ"},
    "usually_need": {"en": "Usually need", "hi": "आमतौर पर ज़रूरी", "ta": "பொதுவாக தேவை", "te": "సాధారణంగా అవసరం", "ml": "സാധാരണയായി ആവശ്യം"},
    "penalties": {"en": "Penalties", "hi": "दंड", "ta": "தண்டனைகள்", "te": "శిక్షలు", "ml": "ശിക്ഷകൾ"},
    "good_to_know": {"en": "Good to know", "hi": "जानना ज़रूरी", "ta": "தெரிந்து கொள்ள வேண்டியவை", "te": "తెలుసుకోవలసినవి", "ml": "അറിഞ്ഞിരിക്കേണ്ടത്"},
    "contact_location": {"en": "Contact & location", "hi": "संपर्क और पता", "ta": "தொடர்பு மற்றும் முகவரி", "te": "సంప్రదింపు & చిరునామా", "ml": "ബന്ധപ്പെടാനുള്ള വിവരവും സ്ഥലവും"},
    "where": {"en": "Where", "hi": "कहाँ", "ta": "எங்கே", "te": "ఎక్కడ", "ml": "എവിടെ"},
    "phone": {"en": "Phone", "hi": "फ़ोन", "ta": "தொலைபேசி", "te": "ఫోన్", "ml": "ഫോൺ"},
    "email": {"en": "Email", "hi": "ईमेल", "ta": "மின்னஞ்சல்", "te": "ఇమెయిల్", "ml": "ഇമെയിൽ"},
    "handles": {"en": "Handles", "hi": "किसके लिए", "ta": "கையாள்வது", "te": "నిర్వహించేవి", "ml": "കൈകാര്യം ചെയ്യുന്നത്"},
    "official_badge": {"en": "Official", "hi": "आधिकारिक", "ta": "அதிகாரப்பூர்வம்", "te": "అధికారికం", "ml": "ഔദ്യോഗികം"},
    "report_link": {"en": "⚑ Report outdated info", "hi": "⚑ पुरानी जानकारी की सूचना दें", "ta": "⚑ காலாவதியான தகவலைப் புகாரளிக்க", "te": "⚑ పాత సమాచారాన్ని నివేదించండి", "ml": "⚑ കാലഹരണപ്പെട്ട വിവരം റിപ്പോർട്ട് ചെയ്യുക"},
    "contact_link": {"en": "✉ Contact / ask a question", "hi": "✉ संपर्क करें / सवाल पूछें", "ta": "✉ தொடர்பு கொள்ள / கேள்வி கேட்க", "te": "✉ సంప్రదించండి / ప్రశ్న అడగండి", "ml": "✉ ബന്ധപ്പെടുക / ചോദ്യം ചോദിക്കുക"},
    "pass_filter_label": {"en": "Your pass:", "hi": "आपका पास:", "ta": "உங்கள் பாஸ்:", "te": "మీ పాస్:", "ml": "നിങ്ങളുടെ പാസ്:"},
    "pass_all": {"en": "All passes", "hi": "सभी पास", "ta": "அனைத்து பாஸ்களும்", "te": "అన్ని పాస్‌లు", "ml": "എല്ലാ പാസുകളും"},
    "pass_ep": {"en": "EP", "hi": "EP", "ta": "EP", "te": "EP", "ml": "EP"},
    "pass_spass": {"en": "S Pass", "hi": "S Pass", "ta": "S Pass", "te": "S Pass", "ml": "S Pass"},
    "pass_wp": {"en": "Work Permit", "hi": "Work Permit", "ta": "Work Permit", "te": "Work Permit", "ml": "Work Permit"},
    "pass_dp": {"en": "Dependant's Pass", "hi": "Dependant's Pass", "ta": "Dependant's Pass", "te": "Dependant's Pass", "ml": "Dependant's Pass"},
    "no_results": {
        "en": "No entries match that search. Try a shorter word, or clear the filter above.",
        "hi": "इस खोज से कोई प्रविष्टि नहीं मिली। छोटा शब्द आज़माएँ, या ऊपर दिया गया फ़िल्टर हटाएँ।",
        "ta": "இந்தத் தேடலுக்குப் பொருந்தும் பதிவுகள் இல்லை. குறுகிய சொல்லை முயற்சிக்கவும், அல்லது மேலே உள்ள வடிகட்டியை அழிக்கவும்.",
        "te": "ఈ శోధనకు సరిపోలే నమోదులు లేవు. చిన్న పదాన్ని ప్రయత్నించండి, లేదా పైన ఉన్న ఫిల్టర్‌ను తీసివేయండి.",
        "ml": "ഈ തിരയലുമായി പൊരുത്തപ്പെടുന്ന എൻട്രികൾ ഇല്ല. ചെറിയ വാക്ക് ശ്രമിക്കുക, അല്ലെങ്കിൽ മുകളിലുള്ള ഫിൽട്ടർ നീക്കം ചെയ്യുക.",
    },
    "notice_h": {
        "en": "Independent directory, not a government site",
        "hi": "स्वतंत्र निर्देशिका, कोई सरकारी वेबसाइट नहीं",
        "ta": "சுயாதீன அடைவு, அரசு தளம் அல்ல",
        "te": "స్వతంత్ర డైరెక్టరీ, ఇది ప్రభుత్వ సైట్ కాదు",
        "ml": "സ്വതന്ത്ര ഡയറക്ടറി, ഇത് ഒരു സർക്കാർ സൈറ്റ് അല്ല",
    },
    "notice_p": {
        "en": "Uthavi is a community-curated index of links to official Indian government and mission sources, plus Singapore's official government sources for the Singapore section — it is not run by, or affiliated with, the Ministry of External Affairs, any Indian mission, or the Government of Singapore. Procedures, fees and eligibility rules change; always complete the actual transaction on the official portal linked from each card. Contact numbers and addresses are checked at each refresh but can change without notice — verify before an urgent trip. Translations beyond English are AI-assisted; if one reads oddly or seems wrong, please report it. Spot something outdated? Use the “Report outdated info” link on that card — it's checked against the official source before anything changes.",
        "hi": "Uthavi आधिकारिक भारतीय सरकारी और मिशन स्रोतों के साथ-साथ सिंगापुर खंड के लिए सिंगापुर के आधिकारिक सरकारी स्रोतों के लिंक की एक सामुदायिक-संकलित सूची है — यह विदेश मंत्रालय, किसी भी भारतीय मिशन, या सिंगापुर सरकार द्वारा संचालित या संबद्ध नहीं है। प्रक्रियाएँ, शुल्क और पात्रता नियम बदलते रहते हैं; हमेशा हर कार्ड में दिए गए आधिकारिक पोर्टल पर ही असली लेन-देन पूरा करें। संपर्क नंबर और पते हर बार अपडेट पर जाँचे जाते हैं पर बिना सूचना बदल सकते हैं — ज़रूरी यात्रा से पहले पुष्टि कर लें। अंग्रेज़ी के अलावा अनुवाद AI की मदद से किए गए हैं; अगर कोई अनुवाद अजीब या ग़लत लगे, तो कृपया सूचित करें। कुछ पुराना लगे? उस कार्ड पर “पुरानी जानकारी की सूचना दें” लिंक का उपयोग करें — कुछ भी बदलने से पहले आधिकारिक स्रोत से जाँचा जाता है।",
        "ta": "Uthavi என்பது அதிகாரப்பூர்வ இந்திய அரசு மற்றும் தூதரக மூலங்களுக்கான இணைப்புகளின் சமூகம்-தொகுத்த அட்டவணை ஆகும், சிங்கப்பூர் பிரிவிற்கு சிங்கப்பூரின் அதிகாரப்பூர்வ அரசு மூலங்களும் சேர்க்கப்பட்டுள்ளன — இது வெளியுறவு அமைச்சகம், எந்த இந்திய தூதரகம், அல்லது சிங்கப்பூர் அரசால் நடத்தப்படுவது அல்ல, அவற்றுடன் தொடர்புடையதும் அல்ல. நடைமுறைகள், கட்டணங்கள் மற்றும் தகுதி விதிகள் மாறும்; ஒவ்வொரு அட்டையிலும் இணைக்கப்பட்ட அதிகாரப்பூர்வ போர்ட்டலில் மட்டுமே உண்மையான பரிவர்த்தனையை முடிக்கவும். தொடர்பு எண்கள் மற்றும் முகவரிகள் ஒவ்வொரு புதுப்பிப்பிலும் சரிபார்க்கப்படுகின்றன, ஆனால் அறிவிப்பின்றி மாறலாம் — அவசர பயணத்திற்கு முன் உறுதிப்படுத்தவும். ஆங்கிலம் தவிர்த்த மொழிபெயர்ப்புகள் AI உதவியுடன் செய்யப்பட்டவை; ஏதேனும் விசித்திரமாகவோ தவறாகவோ தோன்றினால், தயவுசெய்து புகாரளிக்கவும். ஏதேனும் காலாவதியாகத் தெரிகிறதா? அந்த அட்டையில் உள்ள “காலாவதியான தகவலைப் புகாரளிக்க” இணைப்பைப் பயன்படுத்தவும் — எதுவும் மாறுவதற்கு முன் அதிகாரப்பூர்வ மூலத்துடன் சரிபார்க்கப்படும்.",
        "te": "Uthavi అనేది అధికారిక భారత ప్రభుత్వ మరియు మిషన్ మూలాల లింక్‌ల సంఘం-సంకలిత సూచిక, సింగపూర్ విభాగం కోసం సింగపూర్ అధికారిక ప్రభుత్వ మూలాలు కూడా చేర్చబడ్డాయి — ఇది విదేశీ వ్యవహారాల మంత్రిత్వ శాఖ, ఏ భారత మిషన్, లేదా సింగపూర్ ప్రభుత్వంచే నడపబడదు, వాటితో సంబంధం కూడా లేదు. విధానాలు, రుసుములు మరియు అర్హత నియమాలు మారుతూ ఉంటాయి; ప్రతి కార్డులో లింక్ చేసిన అధికారిక పోర్టల్‌లోనే అసలు లావాదేవీని పూర్తి చేయండి. సంప్రదింపు నంబర్లు మరియు చిరునామాలు ప్రతి రిఫ్రెష్‌లో తనిఖీ చేయబడతాయి కానీ ముందస్తు సూచన లేకుండా మారవచ్చు — అత్యవసర ప్రయాణానికి ముందు ధృవీకరించుకోండి. ఆంగ్లం కాకుండా ఇతర అనువాదాలు AI సహాయంతో చేయబడ్డాయి; ఏదైనా విచిత్రంగా అనిపిస్తే లేదా తప్పుగా అనిపిస్తే, దయచేసి నివేదించండి. ఏదైనా పాతదిగా అనిపిస్తుందా? ఆ కార్డులో ఉన్న “పాత సమాచారాన్ని నివేదించండి” లింక్‌ను ఉపయోగించండి — ఏదైనా మారడానికి ముందు అధికారిక మూలంతో సరిచూడబడుతుంది.",
        "ml": "Uthavi എന്നത് ഔദ്യോഗിക ഇന്ത്യൻ സർക്കാർ, മിഷൻ സ്രോതസ്സുകളിലേക്കുള്ള ലിങ്കുകളുടെ ഒരു കമ്മ്യൂണിറ്റി-ക്യൂറേറ്റഡ് സൂചികയാണ്, സിംഗപ്പൂർ വിഭാഗത്തിനായി സിംഗപ്പൂരിന്റെ ഔദ്യോഗിക സർക്കാർ സ്രോതസ്സുകളും ഉൾപ്പെടുത്തിയിട്ടുണ്ട് — ഇത് വിദേശകാര്യ മന്ത്രാലയമോ, ഏതെങ്കിലും ഇന്ത്യൻ മിഷനോ, സിംഗപ്പൂർ സർക്കാരോ നടത്തുന്നതോ അവയുമായി ബന്ധപ്പെട്ടതോ അല്ല. നടപടിക്രമങ്ങൾ, ഫീസ്, യോഗ്യതാ നിയമങ്ങൾ എന്നിവ മാറിക്കൊണ്ടിരിക്കും; എല്ലായ്‌പ്പോഴും ഓരോ കാർഡിലും ലിങ്ക് ചെയ്ത ഔദ്യോഗിക പോർട്ടലിൽ തന്നെ യഥാർത്ഥ ഇടപാട് പൂർത്തിയാക്കുക. ബന്ധപ്പെടാനുള്ള നമ്പറുകളും വിലാസങ്ങളും ഓരോ പുതുക്കലിലും പരിശോധിക്കുന്നുണ്ടെങ്കിലും അറിയിപ്പില്ലാതെ മാറാം — അടിയന്തിര യാത്രയ്ക്ക് മുമ്പ് ഉറപ്പാക്കുക. ഇംഗ്ലീഷ് ഒഴികെയുള്ള പരിഭാഷകൾ AI സഹായത്തോടെയാണ്; എന്തെങ്കിലും വിചിത്രമായി തോന്നിയാലോ തെറ്റാണെന്ന് തോന്നിയാലോ ദയവായി റിപ്പോർട്ട് ചെയ്യുക. എന്തെങ്കിലും കാലഹരണപ്പെട്ടതായി തോന്നുന്നുവോ? ആ കാർഡിലെ “കാലഹരണപ്പെട്ട വിവരം റിപ്പോർട്ട് ചെയ്യുക” ലിങ്ക് ഉപയോഗിക്കുക — എന്തെങ്കിലും മാറ്റുന്നതിന് മുമ്പ് ഔദ്യോഗിക സ്രോതസ്സുമായി പരിശോധിക്കും.",
    },
    "free_banner": {
        "en": "Uthavi is 100% free to use — always will be. No login, no fees, no ads.",
        "hi": "Uthavi का उपयोग पूरी तरह मुफ़्त है — हमेशा रहेगा। कोई लॉगिन नहीं, कोई शुल्क नहीं, कोई विज्ञापन नहीं।",
        "ta": "Uthavi முழுவதும் இலவசமாக பயன்படுத்தலாம் — எப்போதும் இருக்கும். உள்நுழைவு தேவையில்லை, கட்டணம் இல்லை, விளம்பரங்கள் இல்லை.",
        "te": "Uthavi ఉపయోగించడం పూర్తిగా ఉచితం — ఎప్పటికీ ఉచితంగానే ఉంటుంది. లాగిన్ అవసరం లేదు, రుసుము లేదు, ప్రకటనలు లేవు.",
        "ml": "Uthavi ഉപയോഗിക്കുന്നത് പൂർണ്ണമായും സൗജന്യമാണ് — എന്നും അങ്ങനെ തന്നെയായിരിക്കും. ലോഗിൻ വേണ്ട, ഫീസ് ഇല്ല, പരസ്യങ്ങളില്ല.",
    },
    "footer_left": {
        "en": "Uthavi — India + Singapore edition, prototype build. Next: Philippines, Bangladesh, Nigeria.",
        "hi": "Uthavi — भारत + सिंगापुर संस्करण, प्रोटोटाइप। आगे: फिलीपींस, बांग्लादेश, नाइजीरिया।",
        "ta": "Uthavi — இந்தியா + சிங்கப்பூர் பதிப்பு, முன்மாதிரி. அடுத்து: பிலிப்பீன்ஸ், பங்களாதேஷ், நைஜீரியா.",
        "te": "Uthavi — భారత్ + సింగపూర్ ఎడిషన్, ప్రోటోటైప్. తర్వాత: ఫిలిప్పీన్స్, బంగ్లాదేశ్, నైజీరియా.",
        "ml": "Uthavi — ഇന്ത്യ + സിംഗപ്പൂർ പതിപ്പ്, പ്രോട്ടോടൈപ്പ്. അടുത്തത്: ഫിലിപ്പീൻസ്, ബംഗ്ലാദേശ്, നൈജീരിയ.",
    },
    "footer_right": {
        "en": "Sources cross-checked against mea.gov.in, passportindia.gov.in, ociservices.gov.in, ica.gov.sg, mom.gov.sg and individual mission/agency sites.",
        "hi": "स्रोत mea.gov.in, passportindia.gov.in, ociservices.gov.in, ica.gov.sg, mom.gov.sg और अन्य मिशन/एजेंसी साइटों से जाँचे गए।",
        "ta": "mea.gov.in, passportindia.gov.in, ociservices.gov.in, ica.gov.sg, mom.gov.sg மற்றும் தனிப்பட்ட தூதரக/அமைப்பு தளங்களுடன் மூலங்கள் ஒப்பிடப்பட்டுள்ளன.",
        "te": "mea.gov.in, passportindia.gov.in, ociservices.gov.in, ica.gov.sg, mom.gov.sg మరియు వ్యక్తిగత మిషన్/ఏజెన్సీ సైట్‌లతో మూలాలు సరిచూడబడ్డాయి.",
        "ml": "mea.gov.in, passportindia.gov.in, ociservices.gov.in, ica.gov.sg, mom.gov.sg കൂടാതെ വ്യക്തിഗത മിഷൻ/ഏജൻസി സൈറ്റുകളുമായി സ്രോതസ്സുകൾ ഒത്തുനോക്കിയിട്ടുണ്ട്.",
    },
}

# ---------------------------------------------------------------------------
# Category metadata: key -> (country 'all'|'singapore', label{}, note{})
# ---------------------------------------------------------------------------
CATEGORIES = []  # filled below as list of dicts, preserves order

def cat(key, country, label, note):
    CATEGORIES.append({"key": key, "country": country, "label": label, "note": note})

cat("emergency", "all",
    {"en": "Emergency", "hi": "आपातकाल", "ta": "அவசரநிலை", "te": "అత్యవసరం", "ml": "അടിയന്തരാവസ്ഥ"},
    {"en": "For the situations you hope you'll never need — an arrest, a death abroad, a country turning unsafe overnight, or just needing a human on the phone right now.",
     "hi": "उन हालात के लिए जिनकी उम्मीद कोई नहीं करता — गिरफ़्तारी, विदेश में मृत्यु, रातों-रात किसी देश का असुरक्षित हो जाना, या बस अभी फ़ोन पर किसी इंसान की ज़रूरत।",
     "ta": "நீங்கள் ஒருபோதும் தேவைப்படாது என்று நம்பும் சூழல்களுக்கு — கைது, வெளிநாட்டில் மரணம், ஒரு நாடு திடீரென பாதுகாப்பற்றதாக மாறுவது, அல்லது இப்போதே தொலைபேசியில் ஒரு மனிதர் தேவைப்படுவது.",
     "te": "మీకు ఎప్పుడూ అవసరం రాకూడదని ఆశించే పరిస్థితుల కోసం — అరెస్టు, విదేశంలో మరణం, ఒక దేశం రాత్రికి రాత్రి అసురక్షితంగా మారడం, లేదా ఇప్పుడే ఫోన్‌లో ఒక మనిషి కావాలి అనిపించడం.",
     "ml": "നിങ്ങൾക്ക് ഒരിക്കലും ആവശ്യം വരരുതെന്ന് ആഗ്രഹിക്കുന്ന സാഹചര്യങ്ങൾക്ക് — അറസ്റ്റ്, വിദേശത്ത് മരണം, ഒരു രാജ്യം പെട്ടെന്ന് അപകടകരമാകുന്നത്, അല്ലെങ്കിൽ ഇപ്പോൾ തന്നെ ഫോണിൽ ഒരു മനുഷ്യനെ വേണമെന്നത്."})

cat("passport", "all",
    {"en": "Passport", "hi": "पासपोर्ट", "ta": "பாஸ்போர்ட்", "te": "పాస్‌పోర్ట్", "ml": "പാസ്‌പോർട്ട്"},
    {"en": "Everything about the little navy booklet itself: getting a new one, replacing a lost one, or getting cleared for a police check abroad.",
     "hi": "उस छोटी नीली किताब से जुड़ी हर बात: नई बनवाना, खोई हुई बदलवाना, या विदेश में पुलिस जाँच के लिए मंज़ूरी लेना।",
     "ta": "அந்த சிறிய நேவி நிற புத்தகத்தைப் பற்றிய அனைத்தும்: புதிதாகப் பெறுவது, தொலைந்ததை மாற்றுவது, அல்லது வெளிநாட்டில் காவல் சரிபார்ப்புக்கு அனுமதி பெறுவது.",
     "te": "ఆ చిన్న నేవీ రంగు పుస్తకానికి సంబంధించిన ప్రతిదీ: కొత్తది తీసుకోవడం, పోయినదాన్ని మార్చుకోవడం, లేదా విదేశంలో పోలీసు తనిఖీకి అనుమతి పొందడం.",
     "ml": "ആ ചെറിയ നേവി നിറമുള്ള പുസ്തകത്തെക്കുറിച്ചുള്ള എല്ലാം: പുതിയത് നേടുക, നഷ്ടപ്പെട്ടത് മാറ്റുക, അല്ലെങ്കിൽ വിദേശത്ത് പോലീസ് പരിശോധനയ്ക്ക് അനുമതി നേടുക."})

cat("citizenship", "all",
    {"en": "OCI & citizenship", "hi": "OCI और नागरिकता", "ta": "OCI மற்றும் குடியுரிமை", "te": "OCI & పౌరసత్వం", "ml": "OCI, പൗരത്വം"},
    {"en": "For anyone who has taken, or is considering, another country's citizenship while wanting to keep ties to India.",
     "hi": "उन सभी के लिए जिन्होंने किसी दूसरे देश की नागरिकता ले ली है, या लेने पर विचार कर रहे हैं, पर भारत से नाता बनाए रखना चाहते हैं।",
     "ta": "வேறொரு நாட்டின் குடியுரிமையை எடுத்த, அல்லது எடுக்க யோசிக்கும், ஆனால் இந்தியாவுடன் தொடர்பை தக்க வைக்க விரும்பும் அனைவருக்கும்.",
     "te": "మరొక దేశ పౌరసత్వం తీసుకున్న, లేదా తీసుకోవాలని ఆలోచిస్తున్న, కానీ భారత్‌తో సంబంధాన్ని కొనసాగించాలనుకునే వారి కోసం.",
     "ml": "മറ്റൊരു രാജ്യത്തിന്റെ പൗരത്വം സ്വീകരിച്ചവർക്ക്, അല്ലെങ്കിൽ സ്വീകരിക്കാൻ ആലോചിക്കുന്നവർക്ക്, ഇന്ത്യയുമായുള്ള ബന്ധം നിലനിർത്താൻ ആഗ്രഹിക്കുന്നവർക്കായി."})

cat("consular", "all",
    {"en": "Embassy & consular help", "hi": "दूतावास और वाणिज्य सहायता", "ta": "தூதரகம் & துணைத்தூதரக உதவி", "te": "రాయబార & కాన్సులర్ సహాయం", "ml": "എംബസി, കോൺസുലാർ സഹായം"},
    {"en": "The standing channels for ongoing problems and formal support — as distinct from the acute, right-now situations above.",
     "hi": "जारी समस्याओं और औपचारिक सहायता के लिए स्थायी माध्यम — ऊपर दी गई तुरंत वाली आपात स्थितियों से अलग।",
     "ta": "தொடர்ச்சியான பிரச்சினைகள் மற்றும் முறையான உதவிக்கான நிலையான வழிகள் — மேலே உள்ள உடனடி நிலைமைகளிலிருந்து வேறுபட்டவை.",
     "te": "కొనసాగుతున్న సమస్యలు మరియు అధికారిక సహాయం కోసం స్థిరమైన మార్గాలు — పైన ఉన్న తక్షణ పరిస్థితుల నుండి వేరుగా.",
     "ml": "തുടരുന്ന പ്രശ്നങ്ങൾക്കും ഔപചാരിക പിന്തുണയ്ക്കുമുള്ള സ്ഥിരം മാർഗങ്ങൾ — മുകളിൽ പറഞ്ഞ അടിയന്തിര സാഹചര്യങ്ങളിൽ നിന്ന് വ്യത്യസ്തമായി."})

cat("documents", "all",
    {"en": "Documents & certification", "hi": "दस्तावेज़ और प्रमाणीकरण", "ta": "ஆவணங்கள் & சான்றளிப்பு", "te": "పత్రాలు & ధృవీకరణ", "ml": "രേഖകൾ, സാക്ഷ്യപ്പെടുത്തൽ"},
    {"en": "Getting Indian paperwork recognised abroad, and staying registered for the certificates that keep pensions and family records current.",
     "hi": "भारतीय काग़ज़ात को विदेश में मान्यता दिलाना, और पेंशन व पारिवारिक रिकॉर्ड को अद्यतन रखने वाले प्रमाणपत्रों के लिए पंजीकृत रहना।",
     "ta": "இந்திய ஆவணங்களை வெளிநாட்டில் அங்கீகரிக்கச் செய்வது, மற்றும் ஓய்வூதியம் மற்றும் குடும்ப பதிவுகளை புதுப்பித்த நிலையில் வைத்திருக்கும் சான்றிதழ்களுக்கு பதிவு செய்திருப்பது.",
     "te": "భారతీయ పత్రాలను విదేశాలలో గుర్తింపు పొందేలా చేయడం, పింఛన్లు మరియు కుటుంబ రికార్డులను తాజాగా ఉంచే ధృవపత్రాలకు నమోదు కొనసాగించడం.",
     "ml": "ഇന്ത്യൻ രേഖകൾ വിദേശത്ത് അംഗീകാരം നേടുന്നതും, പെൻഷനും കുടുംബ രേഖകളും കാലികമായി നിലനിർത്തുന്ന സർട്ടിഫിക്കറ്റുകൾക്കായി രജിസ്റ്റർ ചെയ്തിരിക്കുന്നതും."})

cat("voting", "all",
    {"en": "Voting rights", "hi": "मतदान अधिकार", "ta": "வாக்குரிமை", "te": "ఓటు హక్కు", "ml": "വോട്ടവകാശം"},
    {"en": "Indian citizens abroad keep their vote — it just has to be registered from outside the country.",
     "hi": "विदेश में रहने वाले भारतीय नागरिकों का मत अधिकार बना रहता है — बस उसे देश के बाहर से पंजीकृत करना होता है।",
     "ta": "வெளிநாட்டில் உள்ள இந்திய குடிமக்கள் தங்கள் வாக்குரிமையை தக்க வைத்திருக்கிறார்கள் — அதை நாட்டிற்கு வெளியே இருந்தே பதிவு செய்ய வேண்டும்.",
     "te": "విదేశాల్లో ఉన్న భారత పౌరులు తమ ఓటు హక్కును కొనసాగిస్తారు — దాన్ని దేశం బయటి నుండి నమోదు చేసుకోవాలి అంతే.",
     "ml": "വിദേശത്തുള്ള ഇന്ത്യൻ പൗരന്മാർ വോട്ടവകാശം നിലനിർത്തുന്നു — അത് രാജ്യത്തിന് പുറത്ത് നിന്ന് രജിസ്റ്റർ ചെയ്യേണ്ടതുണ്ട് എന്ന് മാത്രം."})

cat("work", "all",
    {"en": "Work & emigration", "hi": "कार्य और उत्प्रवास", "ta": "வேலை & குடிபெயர்வு", "te": "పని & వలస", "ml": "ജോലി, കുടിയേറ്റം"},
    {"en": "A step that surprises a lot of first-time workers heading to certain countries.",
     "hi": "एक ऐसा चरण जो कुछ देशों की ओर जा रहे कई पहली बार के कामगारों को चौंका देता है।",
     "ta": "சில நாடுகளுக்குச் செல்லும் முதல்முறை தொழிலாளர்கள் பலரை ஆச்சரியப்படுத்தும் ஒரு படி.",
     "te": "కొన్ని దేశాలకు వెళ్తున్న మొదటిసారి కార్మికులు చాలామందిని ఆశ్చర్యపరిచే ఒక దశ.",
     "ml": "ചില രാജ്യങ്ങളിലേക്ക് പോകുന്ന ആദ്യമായി ജോലിക്ക് പോകുന്ന പലരെയും അമ്പരപ്പിക്കുന്ന ഒരു ഘട്ടം."})

cat("finance", "all",
    {"en": "Tax & banking", "hi": "कर और बैंकिंग", "ta": "வரி & வங்கி", "te": "పన్ను & బ్యాంకింగ్", "ml": "നികുതി, ബാങ്കിംഗ്"},
    {"en": "The paperwork that keeps Indian bank accounts and tax filings compliant once you're a non-resident.",
     "hi": "वह काग़ज़ी काम जो अनिवासी बनने के बाद भारतीय बैंक खातों और कर रिटर्न को नियमों के अनुरूप बनाए रखता है।",
     "ta": "நீங்கள் அசாதாரண குடியுரிமையாளராக ஆனதும் இந்திய வங்கிக் கணக்குகள் மற்றும் வரி தாக்கல்களை விதிமுறைக்கு உட்பட்டதாக வைத்திருக்கும் ஆவணப் பணி.",
     "te": "మీరు నివాసేతరులుగా మారిన తర్వాత భారతీయ బ్యాంకు ఖాతాలు మరియు పన్ను ఫైలింగ్‌లను నిబంధనలకు అనుగుణంగా ఉంచే కాగితం పని.",
     "ml": "നിങ്ങൾ ഒരു അപ്രവാസി ആയതിന് ശേഷം ഇന്ത്യൻ ബാങ്ക് അക്കൗണ്ടുകളും നികുതി ഫയലിംഗും നിയമാനുസൃതമായി നിലനിർത്തുന്ന രേഖാ ജോലി."})

cat("sg_immigration", "singapore",
    {"en": "Singapore — Immigration & ID", "hi": "सिंगापुर — आव्रजन और पहचान", "ta": "சிங்கப்பூர் — குடிவரவு & அடையாளம்", "te": "సింగపూర్ — ఇమిగ్రేషన్ & గుర్తింపు", "ml": "സിംഗപ്പൂർ — ഇമിഗ്രേഷൻ, തിരിച്ചറിയൽ"},
    {"en": "The first two things you sort out after landing — your work pass/FIN, and the digital identity almost everything else in Singapore runs on.",
     "hi": "पहुँचने के बाद सबसे पहले सुलझाई जाने वाली दो चीज़ें — आपका वर्क पास/FIN, और वह डिजिटल पहचान जिस पर सिंगापुर में लगभग बाक़ी सब कुछ चलता है।",
     "ta": "வந்திறங்கியதும் முதலில் சரிசெய்யும் இரண்டு விஷயங்கள் — உங்கள் வேலை பாஸ்/FIN, மற்றும் சிங்கப்பூரில் மற்ற அனைத்தும் இயங்கும் டிஜிட்டல் அடையாளம்.",
     "te": "దిగిన తర్వాత మొదట సర్దుకునే రెండు విషయాలు — మీ వర్క్ పాస్/FIN, మరియు సింగపూర్‌లో మిగతా అన్నీ నడిచే డిజిటల్ గుర్తింపు.",
     "ml": "ഇറങ്ങിയ ഉടനെ ആദ്യം ശരിയാക്കുന്ന രണ്ട് കാര്യങ്ങൾ — നിങ്ങളുടെ വർക്ക് പാസ്/FIN, സിംഗപ്പൂരിൽ മറ്റെല്ലാം പ്രവർത്തിക്കുന്ന ഡിജിറ്റൽ ഐഡന്റിറ്റി."})

cat("sg_money", "singapore",
    {"en": "Singapore — Money, CPF & tax", "hi": "सिंगापुर — पैसा, CPF और कर", "ta": "சிங்கப்பூர் — பணம், CPF & வரி", "te": "సింగపూర్ — డబ్బు, CPF & పన్ను", "ml": "സിംഗപ്പൂർ — പണം, CPF, നികുതി"},
    {"en": "Getting paid, banked and taxed correctly as a new resident employee.",
     "hi": "एक नए निवासी कर्मचारी के रूप में सही तरीक़े से वेतन, बैंकिंग और कर व्यवस्था करना।",
     "ta": "ஒரு புதிய குடியிருப்பாளர் ஊழியராக சரியாக ஊதியம் பெறுவது, வங்கியிடல் மற்றும் வரி செலுத்துவது.",
     "te": "కొత్త నివాస ఉద్యోగిగా సరిగ్గా జీతం పొందడం, బ్యాంకింగ్ చేయడం, పన్ను చెల్లించడం.",
     "ml": "ഒരു പുതിയ താമസക്കാരൻ ജീവനക്കാരൻ എന്ന നിലയിൽ ശരിയായി ശമ്പളം വാങ്ങുന്നതും, ബാങ്കിംഗ് ചെയ്യുന്നതും, നികുതി അടയ്ക്കുന്നതും."})

cat("sg_settling", "singapore",
    {"en": "Singapore — Settling in", "hi": "सिंगापुर — बस जाना", "ta": "சிங்கப்பூர் — குடியேறுதல்", "te": "సింగపూర్ — స్థిరపడటం", "ml": "സിംഗപ്പൂർ — സ്ഥിരതാമസമാക്കൽ"},
    {"en": "Housing, driving, schooling and healthcare — the everyday admin of actually living here.",
     "hi": "आवास, ड्राइविंग, स्कूली शिक्षा और स्वास्थ्य सेवा — यहाँ वास्तव में रहने का रोज़मर्रा का काग़ज़ी काम।",
     "ta": "வீட்டுவசதி, வாகனம் ஓட்டுதல், பள்ளிக்கல்வி மற்றும் சுகாதாரம் — இங்கு உண்மையில் வாழ்வதற்கான தினசரி நிர்வாகம்.",
     "te": "గృహవసతి, డ్రైవింగ్, పాఠశాల విద్య మరియు ఆరోగ్య సంరక్షణ — ఇక్కడ నిజంగా జీవించడానికి రోజువారీ నిర్వహణ.",
     "ml": "പാർപ്പിടം, ഡ്രൈവിംഗ്, സ്കൂൾ വിദ്യാഭ്യാസം, ആരോഗ്യ പരിരക്ഷ — ഇവിടെ യഥാർത്ഥത്തിൽ ജീവിക്കുന്നതിനുള്ള ദൈനംദിന കാര്യങ്ങൾ."})

cat("sg_consular", "singapore",
    {"en": "Singapore — Indian consular services", "hi": "सिंगापुर — भारतीय वाणिज्य सेवाएँ", "ta": "சிங்கப்பூர் — இந்திய துணைத்தூதரக சேவைகள்", "te": "సింగపూర్ — భారత కాన్సులర్ సేవలు", "ml": "സിംഗപ്പൂർ — ഇന്ത്യൻ കോൺസുലാർ സേവനങ്ങൾ"},
    {"en": "How the Passport/OCI cards above actually work if you're filing from Singapore specifically — the local centre that handles it.",
     "hi": "ऊपर दिए गए पासपोर्ट/OCI कार्ड सिंगापुर से आवेदन करने पर असल में कैसे काम करते हैं — इसे संभालने वाला स्थानीय केंद्र।",
     "ta": "நீங்கள் குறிப்பாக சிங்கப்பூரிலிருந்து விண்ணப்பிக்கும்போது மேலே உள்ள பாஸ்போர்ட்/OCI அட்டைகள் உண்மையில் எப்படி செயல்படுகின்றன — அதை கையாளும் உள்ளூர் மையம்.",
     "te": "మీరు ప్రత్యేకంగా సింగపూర్ నుండి దరఖాస్తు చేసుకున్నప్పుడు పైన ఉన్న పాస్‌పోర్ట్/OCI కార్డులు నిజంగా ఎలా పనిచేస్తాయి — దీన్ని నిర్వహించే స్థానిక కేంద్రం.",
     "ml": "നിങ്ങൾ പ്രത്യേകമായി സിംഗപ്പൂരിൽ നിന്ന് അപേക്ഷിക്കുമ്പോൾ മുകളിലുള്ള പാസ്‌പോർട്ട്/OCI കാർഡുകൾ യഥാർത്ഥത്തിൽ എങ്ങനെ പ്രവർത്തിക്കുന്നു — ഇത് കൈകാര്യം ചെയ്യുന്ന പ്രാദേശിക കേന്ദ്രം."})

cat("sg_workpermit", "singapore",
    {"en": "Singapore — Work Permit holders", "hi": "सिंगापुर — Work Permit धारक", "ta": "சிங்கப்பூர் — Work Permit வைத்திருப்பவர்கள்", "te": "సింగపూర్ — Work Permit హోల్డర్లు", "ml": "സിംഗപ്പൂർ — Work Permit ഉടമകൾ"},
    {"en": "What's structurally different if you're on a Work Permit rather than an EP or S Pass — housing, changing employers, pay rights, and where to get help.",
     "hi": "अगर आप EP या S Pass के बजाय Work Permit पर हैं तो संरचनात्मक रूप से क्या अलग है — आवास, नियोक्ता बदलना, वेतन अधिकार, और मदद कहाँ से लें।",
     "ta": "EP அல்லது S Pass க்குப் பதிலாக நீங்கள் Work Permit இல் இருந்தால் கட்டமைப்பு ரீதியாக என்ன வேறுபடுகிறது — வீட்டுவசதி, முதலாளியை மாற்றுவது, ஊதிய உரிமைகள், மற்றும் உதவி எங்கே பெறுவது.",
     "te": "మీరు EP లేదా S Pass కు బదులుగా Work Permit పై ఉంటే నిర్మాణాత్మకంగా ఏమి భిన్నంగా ఉంటుంది — గృహవసతి, యజమానిని మార్చడం, జీతం హక్కులు, మరియు సహాయం ఎక్కడ పొందాలో.",
     "ml": "EP അല്ലെങ്കിൽ S Pass ന് പകരം നിങ്ങൾ Work Permit ൽ ആണെങ്കിൽ ഘടനാപരമായി എന്താണ് വ്യത്യസ്തം — പാർപ്പിടം, തൊഴിലുടമയെ മാറ്റുന്നത്, ശമ്പള അവകാശങ്ങൾ, സഹായം എവിടെ നിന്ന് ലഭിക്കും."})

cat("sg_laws", "singapore",
    {"en": "Singapore — Laws & what not to do", "hi": "सिंगापुर — क़ानून और क्या न करें", "ta": "சிங்கப்பூர் — சட்டங்கள் & என்ன செய்யக்கூடாது", "te": "సింగపూర్ — చట్టాలు & ఏమి చేయకూడదు", "ml": "സിംഗപ്പൂർ — നിയമങ്ങളും ചെയ്യരുതാത്തതും"},
    {"en": "The rules that carry real consequences here — from zero-tolerance drug laws to fines for everyday things that aren't offences back home.",
     "hi": "यहाँ जिन नियमों के असली परिणाम होते हैं — ज़ीरो-टॉलरेंस ड्रग क़ानूनों से लेकर रोज़मर्रा की उन चीज़ों के जुर्माने तक जो घर पर अपराध नहीं हैं।",
     "ta": "இங்கு உண்மையான விளைவுகளைக் கொண்ட விதிகள் — பூஜ்ஜிய-சகிப்புத்தன்மை போதைப்பொருள் சட்டங்கள் முதல் சொந்த நாட்டில் குற்றமல்லாத அன்றாட விஷயங்களுக்கான அபராதங்கள் வரை.",
     "te": "ఇక్కడ నిజమైన పరిణామాలున్న నియమాలు — జీరో-టాలరెన్స్ డ్రగ్ చట్టాల నుండి స్వదేశంలో నేరాలు కాని రోజువారీ విషయాలకు జరిమానాల వరకు.",
     "ml": "ഇവിടെ യഥാർത്ഥ പരിണതഫലങ്ങളുള്ള നിയമങ്ങൾ — പൂജ്യം-സഹിഷ്ണുത മയക്കുമരുന്ന് നിയമങ്ങൾ മുതൽ സ്വദേശത്ത് കുറ്റമല്ലാത്ത ദൈനംദിന കാര്യങ്ങൾക്കുള്ള പിഴകൾ വരെ."})

ENTRIES = []

STYLE_EXTRA = r"""
<style>
  :root {
    --paper: #f3f4f8;
    --paper-raised: #ffffff;
    --ink: #1b2340;
    --ink-soft: #4b5170;
    --accent: #c97a1d;
    --accent-deep: #8f5410;
    --accent-tint: #f6e6cd;
    --verified: #2f7b64;
    --verified-tint: #dcefe7;
    --line: rgba(27, 35, 64, 0.14);
    --line-strong: rgba(27, 35, 64, 0.28);
    --shadow: rgba(27, 35, 64, 0.08);
    --focus: #2f5fd0;
    --critical: #a3372f;
    --critical-tint: #f5ddd9;
  }

  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --paper: #12162a; --paper-raised: #1a2038; --ink: #eceef7; --ink-soft: #b3b8d4;
      --accent: #e8a04a; --accent-deep: #f4c07d; --accent-tint: #3a2c15;
      --verified: #6bbfa2; --verified-tint: #163229;
      --line: rgba(236, 238, 247, 0.16); --line-strong: rgba(236, 238, 247, 0.32);
      --shadow: rgba(0, 0, 0, 0.35); --focus: #7ea1ff;
      --critical: #e8837a; --critical-tint: #3a1e1b;
    }
  }

  :root[data-theme="dark"] {
    --paper: #12162a; --paper-raised: #1a2038; --ink: #eceef7; --ink-soft: #b3b8d4;
    --accent: #e8a04a; --accent-deep: #f4c07d; --accent-tint: #3a2c15;
    --verified: #6bbfa2; --verified-tint: #163229;
    --line: rgba(236, 238, 247, 0.16); --line-strong: rgba(236, 238, 247, 0.32);
    --shadow: rgba(0, 0, 0, 0.35); --focus: #7ea1ff;
    --critical: #e8837a; --critical-tint: #3a1e1b;
  }

  * { box-sizing: border-box; }
  html { color-scheme: light dark; }
  body { margin: 0; background: var(--paper); color: var(--ink); font-family: "IBM Plex Sans", -apple-system, "Segoe UI", sans-serif; font-size: 16px; line-height: 1.5; -webkit-font-smoothing: antialiased; }
  a { color: inherit; }
  h1, h2, h3 { font-family: "Source Serif 4", Georgia, "Times New Roman", serif; text-wrap: balance; margin: 0; }
  .mono { font-family: "IBM Plex Mono", "SFMono-Regular", Menlo, monospace; }
  :focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }

  /* Indic script fonts: applied to the whole page once that language becomes active.
     The corresponding @font-face CSS is only fetched from Google Fonts when needed (see ensureFont in JS),
     so a reader who only ever uses English never downloads Devanagari/Tamil/Telugu/Malayalam font files. */
  body[data-lang="hi"] { font-family: "Noto Sans Devanagari", "IBM Plex Sans", sans-serif; }
  body[data-lang="hi"] h3 { font-family: "Noto Sans Devanagari", serif; }
  body[data-lang="ta"] { font-family: "Noto Sans Tamil", "IBM Plex Sans", sans-serif; }
  body[data-lang="ta"] h3 { font-family: "Noto Sans Tamil", serif; }
  body[data-lang="te"] { font-family: "Noto Sans Telugu", "IBM Plex Sans", sans-serif; }
  body[data-lang="te"] h3 { font-family: "Noto Sans Telugu", serif; }
  body[data-lang="ml"] { font-family: "Noto Sans Malayalam", "IBM Plex Sans", sans-serif; }
  body[data-lang="ml"] h3 { font-family: "Noto Sans Malayalam", serif; }

  /* Small "loading a language" affordance while its JSON file is being fetched */
  .lang-chip.is-loading { opacity: 0.6; cursor: wait; }
  .lang-status { font-size: 0.78rem; color: var(--ink-soft); margin-left: 6px; }
  .lang-status[hidden] { display: none; }

  /* ---------- Masthead ---------- */
  .masthead { border-bottom: 1px solid var(--line); background: var(--paper-raised); }
  .masthead-inner { max-width: 1180px; margin: 0 auto; padding: 28px 28px 22px; }
  .masthead-top { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .brand { display: flex; align-items: baseline; gap: 10px; }
  .brand-logo { flex: none; align-self: center; }
  .brand-mark { font-family: "Source Serif 4", serif; font-size: 1.7rem; font-weight: 600; letter-spacing: -0.01em; }
  .brand-mark span { color: var(--accent-deep); font-style: italic; }
  .brand-tag { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.11em; color: var(--ink-soft); border-left: 1px solid var(--line-strong); padding-left: 12px; }
  .masthead-meta { display: flex; gap: 18px; font-size: 0.78rem; color: var(--ink-soft); flex-wrap: wrap; }
  .masthead-meta strong { color: var(--verified); font-weight: 600; }
  .masthead-lede { max-width: 62ch; margin-top: 18px; font-size: 1.05rem; color: var(--ink-soft); }

  .country-rail { display: flex; gap: 8px; margin-top: 20px; flex-wrap: wrap; }
  .country-chip { display: inline-flex; align-items: center; gap: 7px; padding: 7px 14px; border-radius: 999px; border: 1px solid var(--line-strong); font-size: 0.82rem; font-weight: 500; background: var(--paper); color: var(--ink-soft); font-family: inherit; cursor: pointer; }
  .country-chip.active { background: var(--ink); color: var(--paper); border-color: var(--ink); }
  .country-chip.soon { opacity: 0.55; cursor: default; }

  /* Pass-type filter row: only shown while the Singapore country chip is active */
  .pass-rail { display: none; align-items: center; gap: 8px; margin-top: 10px; flex-wrap: wrap; font-size: 0.82rem; }
  .pass-rail.show { display: flex; }
  .pass-rail-label { color: var(--ink-soft); font-weight: 500; }
  .pass-chip { display: inline-flex; align-items: center; padding: 5px 12px; border-radius: 999px; border: 1px solid var(--line-strong); font-size: 0.78rem; font-weight: 600; background: var(--paper); color: var(--ink-soft); font-family: "IBM Plex Mono", monospace; cursor: pointer; }
  .pass-chip.active { background: var(--accent-deep); border-color: var(--accent-deep); color: #201400; }
  /* Small badges on a card itself, showing which pass(es) that card is specific to */
  .pass-badges { display: flex; gap: 5px; flex-wrap: wrap; margin-top: -4px; }
  .pass-badge { font-family: "IBM Plex Mono", monospace; font-size: 0.62rem; font-weight: 600; letter-spacing: 0.02em; padding: 2px 6px; border-radius: 4px; background: var(--accent-tint); color: var(--accent-deep); white-space: nowrap; }

  .lang-rail { display: flex; gap: 6px; margin-top: 12px; flex-wrap: wrap; }
  .lang-chip { display: inline-flex; align-items: center; padding: 5px 12px; border-radius: 999px; border: 1px solid var(--line-strong); font-size: 0.78rem; font-weight: 500; background: var(--paper); color: var(--ink-soft); font-family: "IBM Plex Sans", "Noto Sans Devanagari", "Noto Sans Tamil", "Noto Sans Telugu", "Noto Sans Malayalam", sans-serif; cursor: pointer; }
  .lang-chip.active { background: var(--accent); border-color: var(--accent); color: #201400; }

  /* ---------- Controls ---------- */
  .controls { position: sticky; top: 0; z-index: 5; background: var(--paper); border-bottom: 1px solid var(--line); backdrop-filter: blur(6px); }
  .controls-inner { max-width: 1180px; margin: 0 auto; padding: 14px 28px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  .search-box { flex: 1 1 240px; display: flex; align-items: center; gap: 8px; background: var(--paper-raised); border: 1px solid var(--line-strong); border-radius: 8px; padding: 9px 12px; }
  .search-box svg { flex: none; opacity: 0.55; }
  .search-box input { border: none; background: none; outline: none; color: var(--ink); font-family: inherit; font-size: 0.92rem; width: 100%; }
  .search-box input::placeholder { color: var(--ink-soft); }
  .filter-chips { display: flex; gap: 6px; flex-wrap: wrap; }
  .chip { font-family: "IBM Plex Mono", monospace; font-size: 0.72rem; letter-spacing: 0.03em; padding: 7px 11px; border-radius: 6px; border: 1px solid var(--line-strong); background: var(--paper-raised); color: var(--ink-soft); cursor: pointer; transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease; }
  .chip:hover { border-color: var(--accent); color: var(--ink); }
  .chip.active { background: var(--accent); border-color: var(--accent); color: #201400; }
  .chip[hidden] { display: none !important; }
  .result-count { font-size: 0.76rem; color: var(--ink-soft); white-space: nowrap; }

  /* ---------- Layout ---------- */
  main { max-width: 1180px; margin: 0 auto; padding: 30px 28px 60px; }
  .section { margin-top: 44px; }
  .section:first-child { margin-top: 8px; }
  .section-head { display: flex; align-items: baseline; gap: 14px; margin-bottom: 16px; border-bottom: 1px solid var(--line); padding-bottom: 10px; }
  .section-head h2 { font-size: 1.3rem; font-weight: 600; }
  .section-count { font-family: "IBM Plex Mono", monospace; font-size: 0.72rem; color: var(--ink-soft); }
  .section-note { font-size: 0.88rem; color: var(--ink-soft); margin: -6px 0 16px; max-width: 68ch; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 16px; align-items: start; }

  /* ---------- Card ---------- */
  .card { position: relative; background: var(--paper-raised); border: 1px solid var(--line); border-radius: 3px; padding: 18px 18px 16px; box-shadow: 0 1px 2px var(--shadow); display: flex; flex-direction: column; gap: 10px; }
  .card::before { content: ""; position: absolute; top: 0; left: 18px; width: 34px; height: 5px; background: var(--accent); border-radius: 0 0 2px 2px; }
  .card-emergency::before { background: var(--critical); }
  .card-emergency .badge { background: var(--critical-tint); color: var(--critical); }
  .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-top: 6px; }
  .card h3 { font-size: 1.06rem; font-weight: 600; line-height: 1.3; }
  .badge { flex: none; font-family: "IBM Plex Mono", monospace; font-size: 0.64rem; letter-spacing: 0.04em; text-transform: uppercase; padding: 3px 7px; border-radius: 4px; background: var(--verified-tint); color: var(--verified); white-space: nowrap; }
  .card p.i18n-p { margin: 0; font-size: 0.9rem; color: var(--ink-soft); }
  .card-meta { display: flex; flex-wrap: wrap; gap: 6px 14px; font-family: "IBM Plex Mono", monospace; font-size: 0.68rem; color: var(--ink-soft); margin-top: 2px; }
  .card-meta b { color: var(--ink); font-weight: 500; }
  .card-links { margin-top: auto; padding-top: 12px; border-top: 1px dashed var(--line); display: flex; flex-direction: column; gap: 6px; }
  .card-links a { display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 500; text-decoration: none; color: var(--accent-deep); }
  .card-links a:hover { text-decoration: underline; }
  .card-links a.report-link { color: var(--ink-soft); font-size: 0.78rem; font-weight: 500; margin-top: 4px; padding-top: 8px; border-top: 1px dotted var(--line); }
  .card-links a.report-link:hover { color: var(--critical); }
  .card[data-cat] { scroll-margin-top: 90px; }
  .card[data-country-hidden] { display: none !important; }

  /* ---------- How-to detail ---------- */
  .card-detail { border-top: 1px dashed var(--line); margin-top: 2px; }
  .detail-toggle { display: flex; align-items: center; justify-content: space-between; width: 100%; background: none; border: none; padding: 10px 0 2px; margin: 0; font-family: inherit; font-size: 0.82rem; font-weight: 600; color: var(--accent-deep); cursor: pointer; text-align: left; }
  .detail-toggle svg { transition: transform 0.15s ease; flex: none; }
  .detail-toggle[aria-expanded="true"] svg { transform: rotate(180deg); }
  .detail-panel { padding: 10px 0 2px; display: flex; flex-direction: column; gap: 12px; }
  .detail-panel[hidden] { display: none; }
  .detail-block h4 { font-family: "IBM Plex Mono", monospace; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--ink-soft); margin: 0 0 6px; font-weight: 600; }
  .detail-block ol { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: 5px; font-size: 0.85rem; color: var(--ink); }
  .detail-block ol li::marker { color: var(--accent-deep); font-family: "IBM Plex Mono", monospace; font-weight: 600; font-size: 0.8em; }
  .doc-list { margin: 0; padding-left: 0; list-style: none; display: flex; flex-direction: column; gap: 4px; font-size: 0.85rem; color: var(--ink); }
  .doc-list li { padding-left: 1.1em; position: relative; }
  .doc-list li::before { content: ""; position: absolute; left: 0; top: 0.55em; width: 5px; height: 5px; border-radius: 999px; background: var(--verified); }
  .condition-note { margin: 0; font-size: 0.83rem; color: var(--ink-soft); }

  /* ---------- Notice ---------- */
  .notice { margin-top: 46px; border: 1px solid var(--line-strong); background: var(--paper-raised); border-radius: 4px; padding: 18px 20px; display: flex; gap: 14px; align-items: flex-start; }
  .notice svg { flex: none; margin-top: 2px; opacity: 0.7; }
  .notice h4 { font-family: "IBM Plex Sans", sans-serif; font-size: 0.9rem; font-weight: 600; margin: 0 0 4px; }
  .notice p { margin: 0; font-size: 0.85rem; color: var(--ink-soft); max-width: 72ch; }

  /* ---------- Footer ---------- */
  footer { border-top: 1px solid var(--line); background: var(--paper-raised); }
  .footer-inner { max-width: 1180px; margin: 0 auto; padding: 26px 28px 34px; display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; font-size: 0.78rem; color: var(--ink-soft); }
  .footer-inner a { color: var(--ink-soft); text-decoration: underline; text-underline-offset: 2px; }
  .no-results { display: none; padding: 40px 0; text-align: center; color: var(--ink-soft); font-size: 0.92rem; }
  .no-results.show { display: block; }

  /* ---------- Free-service banner ---------- */
  .free-banner { background: var(--accent-tint); border-bottom: 1px solid var(--line); }
  .free-banner-inner { max-width: 1180px; margin: 0 auto; padding: 8px 28px; display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--accent-deep); font-weight: 500; }
  .free-banner-inner svg { flex: none; opacity: 0.85; }

  @media (max-width: 560px) {
    .masthead-inner, .controls-inner, main, .footer-inner { padding-left: 18px; padding-right: 18px; }
    .brand-tag { display: none; }

    /* Compact sticky controls bar: search on its own row, chips as one
       horizontally-scrollable row instead of wrapping to many lines. */
    .controls-inner { flex-direction: column; align-items: stretch; flex-wrap: nowrap; gap: 8px; padding-top: 10px; padding-bottom: 10px; }
    .search-box { flex: 0 0 auto; width: 100%; padding: 7px 10px; }
    .filter-chips { flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none; padding-bottom: 1px; }
    .filter-chips::-webkit-scrollbar { display: none; }
    .chip { flex: none; padding: 6px 10px; font-size: 0.68rem; }
    .result-count { display: none; }

    .free-banner-inner { padding: 6px 18px; font-size: 0.74rem; }
  }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
"""

SCRIPT_TEMPLATE = r"""
<script>
  (function () {
    var I18N = __I18N_JSON__;
    var LANG_LABELS = __LANG_LABELS_JSON__;
    var currentLang = 'en';
    var activeCountry = 'all';
    var activeFilter = 'all';
    var activePass = 'all';

    var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.section'));
    var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
    var passChips = Array.prototype.slice.call(document.querySelectorAll('.pass-chip'));
    var passRail = document.getElementById('passRail');
    var searchInput = document.getElementById('searchInput');
    var resultCount = document.getElementById('resultCount');
    var noResults = document.getElementById('noResults');
    var langStatus = document.getElementById('langStatus');
    var resultsTemplate = __RESULTS_TEMPLATE_JSON__;

    // ---- Lazy-loaded languages -------------------------------------------------
    // The page ships in English only. Hindi/Tamil/Telugu/Malayalam each live in their
    // own lang-<code>.json file (built alongside index.html) and are fetched at most
    // once, the first time a reader actually picks that language, then cached in memory.
    var LANG_FILES = { hi: 'lang-hi.json', ta: 'lang-ta.json', te: 'lang-te.json', ml: 'lang-ml.json' };
    var LANG_FONT_HREF = {
      hi: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap',
      ta: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap',
      te: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700&display=swap',
      ml: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Malayalam:wght@400;500;600;700&display=swap'
    };
    var enCache = {};       // captured once at load: id -> original English innerHTML, so switching back to EN needs no network
    var langCache = {};     // id -> parsed JSON, filled in as each non-English language is first requested
    var loadedFonts = {};   // lang -> true once its @font-face stylesheet has been injected

    function captureEnCache() {
      document.querySelectorAll('[data-i18n-id]').forEach(function (elNode) {
        enCache[elNode.getAttribute('data-i18n-id')] = elNode.innerHTML;
      });
    }

    function applyLangData(data) {
      document.querySelectorAll('[data-i18n-id]').forEach(function (elNode) {
        var id = elNode.getAttribute('data-i18n-id');
        if (Object.prototype.hasOwnProperty.call(data, id)) elNode.innerHTML = data[id];
      });
    }

    function ensureFont(lang) {
      if (loadedFonts[lang] || !LANG_FONT_HREF[lang]) return;
      loadedFonts[lang] = true;
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = LANG_FONT_HREF[lang];
      document.head.appendChild(link);
    }

    function setLangStatus(text) {
      if (!langStatus) return;
      if (text) { langStatus.textContent = text; langStatus.removeAttribute('hidden'); }
      else { langStatus.setAttribute('hidden', ''); langStatus.textContent = ''; }
    }

    function applyI18nChrome() {
      document.querySelectorAll('[data-i18n]').forEach(function (elNode) {
        var key = elNode.getAttribute('data-i18n');
        var dict = I18N[key];
        if (!dict) return;
        var text = dict[currentLang] || dict.en;
        if (elNode.hasAttribute('data-i18n-upper')) text = text.toUpperCase();
        elNode.textContent = text;
      });
      searchInput.placeholder = (I18N.search_placeholder[currentLang] || I18N.search_placeholder.en);
    }

    function finishLangSwitch(lang, data) {
      currentLang = lang;
      document.body.setAttribute('data-lang', lang);
      applyLangData(data);
      applyI18nChrome();
      applyFilters();
      setLangStatus(null);
    }

    function setLang(lang) {
      document.querySelectorAll('.lang-chip').forEach(function (btn) {
        btn.classList.toggle('active', btn.getAttribute('data-lang-btn') === lang);
      });

      if (lang === 'en') { finishLangSwitch('en', enCache); return; }

      ensureFont(lang);

      if (langCache[lang]) { finishLangSwitch(lang, langCache[lang]); return; }

      var btn = document.querySelector('.lang-chip[data-lang-btn="' + lang + '"]');
      if (btn) btn.classList.add('is-loading');
      setLangStatus((LANG_LABELS[lang] || lang) + '…');

      fetch(LANG_FILES[lang]).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      }).then(function (data) {
        langCache[lang] = data;
        if (btn) btn.classList.remove('is-loading');
        finishLangSwitch(lang, data);
      }).catch(function () {
        if (btn) btn.classList.remove('is-loading');
        setLangStatus('Could not load this language — check your connection and try again.');
        // stay on whatever language was active before; re-mark its chip active
        document.querySelectorAll('.lang-chip').forEach(function (b) {
          b.classList.toggle('active', b.getAttribute('data-lang-btn') === currentLang);
        });
      });
    }

    function applyFilters() {
      var q = searchInput.value.trim().toLowerCase();
      var shown = 0;

      cards.forEach(function (card) {
        var cat = card.getAttribute('data-cat');
        var cardCountry = card.getAttribute('data-country');
        var cardPasses = card.getAttribute('data-passes') || '';
        var haystack = (card.getAttribute('data-title') + ' ' + card.textContent).toLowerCase();
        var matchesCat = activeFilter === 'all' || cat === activeFilter;
        var matchesQuery = q === '' || haystack.indexOf(q) !== -1;
        var matchesCountry = cardCountry === 'all' || cardCountry === activeCountry;
        // A card with no passes listed applies regardless of pass (e.g. emergency, OCI, driving licence).
        var matchesPass = activePass === 'all' || cardPasses === '' || cardPasses.split(',').indexOf(activePass) !== -1;
        var visible = matchesCat && matchesQuery && matchesCountry && matchesPass;
        card.style.display = visible ? '' : 'none';
        if (visible) shown++;
      });

      // The pass filter only makes sense within the Singapore section.
      if (passRail) passRail.classList.toggle('show', activeCountry === 'singapore');

      sections.forEach(function (section) {
        var secCountry = section.getAttribute('data-country');
        var countryOk = secCountry === 'all' || secCountry === activeCountry;
        var visibleCards = section.querySelectorAll('.card:not([style*="display: none"])');
        section.style.display = (countryOk && visibleCards.length) ? '' : 'none';
      });

      chips.forEach(function (chip) {
        var chipCountry = chip.getAttribute('data-country');
        if (!chipCountry) return; // the ALL chip has no data-country, always visible
        var ok = chipCountry === 'all' || chipCountry === activeCountry;
        if (!ok && chip.classList.contains('active')) {
          chip.classList.remove('active');
          document.querySelector('.chip[data-filter="all"]').classList.add('active');
          activeFilter = 'all';
        }
        if (ok) chip.removeAttribute('hidden'); else chip.setAttribute('hidden', '');
      });

      var template = resultsTemplate[currentLang] || resultsTemplate.en;
      resultCount.textContent = template.replace('{shown}', shown).replace('{total}', cards.length);
      noResults.classList.toggle('show', shown === 0);
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('active'); });
        chip.classList.add('active');
        activeFilter = chip.getAttribute('data-filter');
        applyFilters();
      });
    });

    document.querySelectorAll('[data-country-filter]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeCountry = btn.getAttribute('data-country-filter');
        document.querySelectorAll('[data-country-filter]').forEach(function (b) {
          b.classList.toggle('active', b === btn);
        });
        applyFilters();
      });
    });

    passChips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        passChips.forEach(function (c) { c.classList.remove('active'); });
        chip.classList.add('active');
        activePass = chip.getAttribute('data-pass-filter');
        applyFilters();
      });
    });

    document.querySelectorAll('[data-lang-btn]').forEach(function (btn) {
      btn.addEventListener('click', function () { setLang(btn.getAttribute('data-lang-btn')); });
    });

    searchInput.addEventListener('input', applyFilters);

    var CONTACT_EMAIL = 'msaratkumar3@gmail.com';
    cards.forEach(function (card) {
      // Canonical English title (baked in as a data attribute, independent of whatever
      // language is currently displayed) keeps email subjects consistent no matter which
      // language the reporter was viewing when they clicked the link.
      var title = card.getAttribute('data-title-en') || card.getAttribute('data-title') || '';
      var linksBlock = card.querySelector('.card-links');
      if (!linksBlock) return;

      // "Report outdated info" — opens a pre-filled email to the site owner. Keeps the same
      // structured template (what's wrong + a source) that used to go into a GitHub issue.
      var body = 'Entry: ' + title + '\n\n' +
        'What looks outdated or wrong?\n\n\n' +
        'Source that confirms the correction (link, if you have one):\n\n\n' +
        '— sent from the "Report outdated info" link on Uthavi';
      var report = document.createElement('a');
      report.className = 'report-link';
      report.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent('Outdated info: ' + title) +
        '&body=' + encodeURIComponent(body);
      report.setAttribute('data-i18n', 'report_link');
      report.textContent = I18N.report_link.en;
      linksBlock.appendChild(report);

      // "Contact / ask a question" — a direct email for anything that isn't a specific
      // correction (a question, feedback, or something the report template doesn't fit).
      var contact = document.createElement('a');
      contact.className = 'report-link';
      contact.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent('Uthavi — ' + title);
      contact.setAttribute('data-i18n', 'contact_link');
      contact.textContent = I18N.contact_link.en;
      linksBlock.appendChild(contact);
    });

    document.querySelectorAll('.detail-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var panel = btn.nextElementSibling;
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        if (open) { panel.setAttribute('hidden', ''); }
        else { panel.removeAttribute('hidden'); }
      });
    });

    captureEnCache();
    document.body.setAttribute('data-lang', 'en');
    applyFilters();
  })();
</script>
"""

def entry(category, badge_official, search_en, title, desc, handles, steps, docs, note, links,
          country="all", emergency=False, toggle_key="how_to_apply", location=None, phone=None, email=None,
          passes=None, steps_label_key="steps", docs_label_key="usually_need"):
    """
    title/desc/handles/note: {lang: str}
    steps/docs: {lang: [str, ...]}   (same order/count across langs)
    links: [{"href": url, "label": {lang: str}}, ...]
    location/phone/email: {lang: str} or None (omitted from the contact block if None)
    passes: list of pass codes this entry is specific to, e.g. ["EP", "SPass"], drawn from
            {"EP", "SPass", "WP", "DP"}. None (the default) means "not pass-specific" — the card
            is shown regardless of the pass filter and gets no pass badge. Singapore-only concept;
            ignored for country="all" (India-generic) entries.
    steps_label_key/docs_label_key: which UI dict key labels the steps/docs block headers — lets a
            card repurpose those two blocks (e.g. "key_facts"/"penalties" for a laws card) while
            reusing the same rendering and data-i18n-id machinery as a normal how-to card.
    """
    ENTRIES.append({
        "category": category, "country": country, "emergency": emergency,
        "badge_official": badge_official, "search_en": search_en, "toggle_key": toggle_key,
        "title": title, "desc": desc, "handles": handles, "steps": steps, "docs": docs, "note": note,
        "links": links, "location": location, "phone": phone, "email": email,
        "passes": passes, "steps_label_key": steps_label_key, "docs_label_key": docs_label_key,
    })

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def e(s):
    return _html.escape(s, quote=False)

def _steps_html(items):
    return "".join('<li>%s</li>' % e(s) for s in items)

def _docs_html(items):
    return "".join('<li>%s</li>' % e(d) for d in items)

def render_card(entry_id, ent):
    """Renders ONE copy of the card, in English, with data-i18n-id markers on every
    translatable node. Other languages are not baked into this HTML at all — they live in
    lang-<code>.json and get fetched + swapped in by JS only when a reader picks that language.
    This keeps the shipped page roughly a fifth of the size it'd be with all 5 languages inline,
    and keeps card count/DOM size constant regardless of how many languages the site supports."""
    cat_key = ent["category"]
    cls = "card card-emergency" if ent["emergency"] else "card"
    passes = ent.get("passes") or []
    parts = []
    parts.append('<article class="%s" data-cat="%s" data-country="%s" data-title="%s" data-title-en="%s" data-passes="%s" id="%s">' % (
        cls, cat_key, ent["country"], e(ent["search_en"]), e(ent["title"]["en"]), ",".join(passes), entry_id))

    # title + badge (badge text is shared chrome copy, not per-card, so it uses the small always-loaded I18N dict)
    parts.append('<div class="card-top"><h3 data-i18n-id="%s-title">%s</h3><span class="badge" data-i18n="official_badge">%s</span></div>' % (
        entry_id, e(ent["title"]["en"]), e(UI["official_badge"]["en"])))

    # pass-type badges (Singapore-only concept): which work pass(es) this card is specific to.
    # No badges at all means "applies regardless of pass" — nothing to flag.
    if passes:
        pass_bits = "".join('<span class="pass-badge" data-i18n="%s">%s</span>' % (PASS_UI_KEY[p], e(UI[PASS_UI_KEY[p]]["en"])) for p in passes)
        parts.append('<div class="pass-badges">%s</div>' % pass_bits)

    # description
    parts.append('<p class="i18n-p" data-i18n-id="%s-desc">%s</p>' % (entry_id, e(ent["desc"]["en"])))

    # meta / handles ("Handles:" label is shared chrome copy; the value is per-card)
    parts.append('<div class="card-meta"><span data-i18n="handles">%s</span>: <b data-i18n-id="%s-handles">%s</b></div>' % (
        e(UI["handles"]["en"]), entry_id, e(ent["handles"]["en"])))

    # detail toggle + panel
    toggle_label_key = ent["toggle_key"]
    chev = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>'
    btn = ('<button class="detail-toggle" aria-expanded="false" type="button">'
           '<span data-i18n="%s">%s</span>%s</button>') % (toggle_label_key, e(UI[toggle_label_key]["en"]), chev)

    steps_label_key = ent.get("steps_label_key", "steps")
    docs_label_key = ent.get("docs_label_key", "usually_need")

    blocks = []
    if ent["steps"].get("en"):
        blocks.append('<div class="detail-block"><h4 data-i18n="%s">%s</h4><ol data-i18n-id="%s-steps">%s</ol></div>' % (
            steps_label_key, e(UI[steps_label_key]["en"]), entry_id, _steps_html(ent["steps"]["en"])))
    if ent["docs"].get("en"):
        blocks.append('<div class="detail-block"><h4 data-i18n="%s">%s</h4><ul class="doc-list" data-i18n-id="%s-docs">%s</ul></div>' % (
            docs_label_key, e(UI[docs_label_key]["en"]), entry_id, _docs_html(ent["docs"]["en"])))
    if ent["note"].get("en"):
        blocks.append('<div class="detail-block"><h4 data-i18n="good_to_know">%s</h4><p class="condition-note" data-i18n-id="%s-note">%s</p></div>' % (
            e(UI["good_to_know"]["en"]), entry_id, e(ent["note"]["en"])))

    contact_lines = []
    if ent["location"]:
        contact_lines.append('<li><b data-i18n="where">%s</b>: <span data-i18n-id="%s-location">%s</span></li>' % (
            e(UI["where"]["en"]), entry_id, e(ent["location"]["en"])))
    if ent["phone"]:
        contact_lines.append('<li><b data-i18n="phone">%s</b>: <span data-i18n-id="%s-phone">%s</span></li>' % (
            e(UI["phone"]["en"]), entry_id, e(ent["phone"]["en"])))
    if ent["email"]:
        contact_lines.append('<li><b data-i18n="email">%s</b>: <span data-i18n-id="%s-email">%s</span></li>' % (
            e(UI["email"]["en"]), entry_id, e(ent["email"]["en"])))
    if contact_lines:
        blocks.append('<div class="detail-block"><h4 data-i18n="contact_location">%s</h4><ul class="doc-list">%s</ul></div>' % (
            e(UI["contact_location"]["en"]), "".join(contact_lines)))

    panel = '<div class="detail-panel" hidden>%s</div>' % "".join(blocks)
    parts.append('<div class="card-detail">%s%s</div>' % (btn, panel))

    # links (href never changes; only the visible label text is per-language)
    link_html = "".join(
        '<a href="%s" target="_blank" rel="noopener" data-i18n-id="%s-link-%d">%s</a>' % (e(l["href"]), entry_id, i, e(l["label"]["en"]))
        for i, l in enumerate(ent["links"]))
    parts.append('<div class="card-links">%s</div>' % link_html)

    parts.append('</article>')
    return "\n".join(parts)


def render_i18n_text(key, tag="span", cls=None, attrs=""):
    """Chrome text driven by JS data-i18n dictionary (single element, JS swaps textContent)."""
    cls_attr = ' class="%s"' % cls if cls else ""
    return '<%s%s data-i18n="%s"%s>%s</%s>' % (tag, cls_attr, key, attrs, e(UI[key]["en"]), tag)


def build_i18n_dict():
    d = {}
    for k, v in UI.items():
        d[k] = v
    for c in CATEGORIES:
        d["cat_%s_label" % c["key"]] = c["label"]
        d["cat_%s_note" % c["key"]] = c["note"]
    return d


def build_lang_payload(lang):
    """All per-card translated content for one non-English language, keyed by the same
    data-i18n-id values used in the HTML. Written to lang-<code>.json and fetched by the
    browser only the first time a reader switches to that language."""
    data = {}
    for i, ent in enumerate(ENTRIES):
        entry_id = "card-%d" % i
        data["%s-title" % entry_id] = e(ent["title"][lang])
        data["%s-desc" % entry_id] = e(ent["desc"][lang])
        data["%s-handles" % entry_id] = e(ent["handles"][lang])
        if ent["steps"].get(lang):
            data["%s-steps" % entry_id] = _steps_html(ent["steps"][lang])
        if ent["docs"].get(lang):
            data["%s-docs" % entry_id] = _docs_html(ent["docs"][lang])
        if ent["note"].get(lang):
            data["%s-note" % entry_id] = e(ent["note"][lang])
        if ent["location"]:
            data["%s-location" % entry_id] = e(ent["location"][lang])
        if ent["phone"]:
            data["%s-phone" % entry_id] = e(ent["phone"][lang])
        if ent["email"]:
            data["%s-email" % entry_id] = e(ent["email"][lang])
        for li, l in enumerate(ent["links"]):
            data["%s-link-%d" % (entry_id, li)] = e(l["label"][lang])
    return data


def render_shell():
    import json
    i18n_json = json.dumps(build_i18n_dict(), ensure_ascii=False)
    lang_labels_json = json.dumps(LANG_LABEL, ensure_ascii=False)
    lang_short_json = json.dumps(LANG_SHORT, ensure_ascii=False)

    # ---- category chips ----
    chip_html = ['<button class="chip active" data-filter="all">ALL</button>']
    for c in CATEGORIES:
        label_en = c["label"]["en"].upper()
        chip_html.append('<button class="chip" data-filter="%s" data-country="%s" data-i18n="cat_%s_label" data-i18n-upper="1">%s</button>' % (
            c["key"], c["country"], c["key"], e(label_en)))

    # ---- sections ----
    section_html = []
    for c in CATEGORIES:
        cat_entries = [(i, ent) for i, ent in enumerate(ENTRIES) if ent["category"] == c["key"]]
        if not cat_entries:
            continue
        cards = "\n".join(render_card("card-%d" % i, ent) for i, ent in cat_entries)
        head = ('<div class="section-head"><h2 data-i18n="cat_%s_label">%s</h2>'
                '<span class="section-count">%d</span></div>') % (c["key"], e(c["label"]["en"]), len(cat_entries))
        note = '<p class="section-note" data-i18n="cat_%s_note">%s</p>' % (c["key"], e(c["note"]["en"]))
        section_html.append(
            '<section class="section" data-section="%s" data-country="%s">%s%s<div class="grid">\n%s\n</div></section>' % (
                c["key"], c["country"], head, note, cards))

    total_entries = len(ENTRIES)

    doc = []
    doc.append('<meta charset="utf-8">')
    doc.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    doc.append('<title>Uthavi</title>')
    doc.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    doc.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    # Only the Latin fonts load up front. The four Indic-script families (Devanagari/Tamil/Telugu/Malayalam)
    # are ~fetched on demand by ensureFont() in JS, the first time a reader actually switches to that language.
    doc.append('<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">')

    doc.append(STYLE_EXTRA)

    doc.append('<div class="free-banner"><div class="free-banner-inner">'
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>'
                '<span data-i18n="free_banner">%s</span></div></div>' % e(UI["free_banner"]["en"]))

    doc.append('<header class="masthead"><div class="masthead-inner"><div class="masthead-top">')
    doc.append('<div class="brand">')
    doc.append('<svg class="brand-logo" width="30" height="30" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
                # Two arms meeting in a clasp — helping hands — for Uthavi.
                '<path d="M4 28 L14 15" style="stroke:var(--accent-deep);stroke-width:6.5;stroke-linecap:round"/>'
                '<path d="M28 28 L18 15" style="stroke:var(--accent);stroke-width:6.5;stroke-linecap:round"/>'
                '<circle cx="16" cy="14" r="4.2" style="fill:var(--verified)"/></svg>')
    doc.append('<div class="brand-mark">Utha<span>vi</span></div>')
    doc.append('<div class="brand-tag" data-i18n="brand_tag">%s</div>' % e(UI["brand_tag"]["en"]))
    doc.append('</div>')  # .brand
    doc.append('<div class="masthead-meta">'
                '<span data-i18n="entries_curated">%s</span>: <strong class="mono">%d</strong>'
                '<span data-i18n="snapshot_verified">%s</span>: <strong class="mono" id="verifiedDate">30 Aug 2026</strong>'
                '</div>' % (e(UI["entries_curated"]["en"]), total_entries, e(UI["snapshot_verified"]["en"])))
    doc.append('</div>')  # .masthead-top

    doc.append('<p class="masthead-lede" data-i18n="lede">%s</p>' % e(UI["lede"]["en"]))

    doc.append('<div class="country-rail">')
    doc.append('<button class="country-chip active" data-country-filter="all">🇮🇳 <span data-i18n="country_india">%s</span></button>' % e(UI["country_india"]["en"]))
    doc.append('<button class="country-chip" data-country-filter="singapore">🇸🇬 <span data-i18n="country_singapore">%s</span></button>' % e(UI["country_singapore"]["en"]))
    doc.append('</div>')  # .country-rail

    # Pass-type filter: hidden by default (JS shows it only while Singapore is the active country)
    doc.append('<div class="pass-rail" id="passRail">')
    doc.append('<span class="pass-rail-label" data-i18n="pass_filter_label">%s</span>' % e(UI["pass_filter_label"]["en"]))
    doc.append('<button class="pass-chip active" data-pass-filter="all" data-i18n="pass_all">%s</button>' % e(UI["pass_all"]["en"]))
    for code in PASS_CODES:
        key = PASS_UI_KEY[code]
        doc.append('<button class="pass-chip" data-pass-filter="%s" data-i18n="%s">%s</button>' % (code, key, e(UI[key]["en"])))
    doc.append('</div>')  # .pass-rail

    doc.append('<div class="lang-rail" id="langRail">')
    for lang in LANG_RAIL_ORDER:
        active = " active" if lang == "en" else ""
        doc.append('<button class="lang-chip%s" data-lang-btn="%s">%s</button>' % (active, lang, e(LANG_LABEL[lang])))
    doc.append('<span class="lang-status" id="langStatus" hidden></span>')
    doc.append('</div>')

    doc.append('</div></header>')  # .masthead-inner .masthead

    doc.append('<div class="controls"><div class="controls-inner">')
    doc.append('<label class="search-box"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
                '<input id="searchInput" type="text" placeholder="%s" autocomplete="off"></label>' % e(UI["search_placeholder"]["en"]))
    doc.append('<div class="filter-chips" id="filterChips">%s</div>' % "".join(chip_html))
    doc.append('<span class="result-count" id="resultCount"></span>')
    doc.append('</div></div>')  # .controls-inner .controls

    doc.append('<main>')
    doc.append("\n".join(section_html))
    doc.append('<p class="no-results" id="noResults" data-i18n="no_results">%s</p>' % e(UI["no_results"]["en"]))
    doc.append('<div class="notice"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
                '<div><h4 data-i18n="notice_h">%s</h4><p data-i18n="notice_p">%s</p></div></div>' % (e(UI["notice_h"]["en"]), e(UI["notice_p"]["en"])))
    doc.append('</main>')

    doc.append('<footer><div class="footer-inner">'
                '<span data-i18n="footer_left">%s</span>'
                '<span data-i18n="footer_right">%s</span>'
                '</div></footer>' % (e(UI["footer_left"]["en"]), e(UI["footer_right"]["en"])))

    doc.append(SCRIPT_TEMPLATE.replace("__I18N_JSON__", i18n_json)
                .replace("__LANG_LABELS_JSON__", lang_labels_json)
                .replace("__RESULTS_TEMPLATE_JSON__", json.dumps(UI["results_shown"], ensure_ascii=False)))

    return "\n".join(doc)

# ===========================================================================
# ENTRIES DATA
# ===========================================================================

# ---- Emergency ----

entry(
    category="emergency", emergency=True, badge_official=True,
    search_en="24/7 distress helpline owrc emergency contact phone unpaid wages passport withheld",
    title={"en": "24/7 distress helpline (OWRC)", "hi": "24/7 संकट हेल्पलाइन (OWRC)",
           "ta": "24/7 நெருக்கடி உதவி எண் (OWRC)", "te": "24/7 సంక్షోభ హెల్ప్‌లైన్ (OWRC)",
           "ml": "24/7 പ്രതിസന്ധി ഹെൽപ്‌ലൈൻ (OWRC)"},
    desc={"en": "The Overseas Workers Resource Centre is the first call for anything urgent — a passport held by an employer, unpaid wages, unsafe working conditions, or needing a legal or medical referral right now. It covers the pre-departure and reintegration stages too, not only people already abroad.",
          "hi": "Overseas Workers Resource Centre किसी भी तुरंत मामले के लिए पहला संपर्क है — नियोक्ता द्वारा रोका गया पासपोर्ट, बकाया वेतन, असुरक्षित काम की स्थिति, या अभी क़ानूनी या चिकित्सा सहायता की ज़रूरत। यह केवल विदेश में रह रहे लोगों के लिए नहीं, बल्कि जाने से पहले और स्वदेश लौटने के बाद के चरण के लिए भी है।",
          "ta": "Overseas Workers Resource Centre என்பது அவசரமான எதற்கும் முதல் தொடர்பு — முதலாளியிடம் பாஸ்போர்ட் வைத்திருப்பது, ஊதியம் கிடைக்காதது, பாதுகாப்பற்ற வேலை நிலைமைகள், அல்லது இப்போதே சட்ட அல்லது மருத்துவ உதவி தேவைப்படுவது. இது ஏற்கனவே வெளிநாட்டில் உள்ளவர்களுக்கு மட்டுமல்ல, புறப்படுவதற்கு முன்னும் திரும்பி வந்த பின்னும் உள்ள கட்டங்களையும் உள்ளடக்கியது.",
          "te": "Overseas Workers Resource Centre అత్యవసరమైన దేనికైనా మొదటి కాల్ — యజమాని పాస్‌పోర్ట్ ఆపడం, జీతం రాకపోవడం, అసురక్షిత పని పరిస్థితులు, లేదా ఇప్పుడే న్యాయ లేదా వైద్య సహాయం అవసరం కావడం. ఇది ఇప్పటికే విదేశాల్లో ఉన్నవారికే కాదు, బయలుదేరే ముందు మరియు తిరిగి వచ్చిన తర్వాత దశలకు కూడా వర్తిస్తుంది.",
          "ml": "Overseas Workers Resource Centre അടിയന്തിരമായ ഏത് കാര്യത്തിനും ആദ്യം വിളിക്കേണ്ട ഇടമാണ് — തൊഴിലുടമ പാസ്‌പോർട്ട് പിടിച്ചുവയ്ക്കുന്നത്, ശമ്പളം കിട്ടാത്തത്, സുരക്ഷിതമല്ലാത്ത ജോലി സാഹചര്യങ്ങൾ, അല്ലെങ്കിൽ ഇപ്പോൾ തന്നെ നിയമ അല്ലെങ്കിൽ മെഡിക്കൽ സഹായം വേണ്ടിവരുന്നത്. ഇത് നിലവിൽ വിദേശത്തുള്ളവർക്ക് മാത്രമല്ല, പോകുന്നതിന് മുൻപും തിരിച്ചെത്തിയ ശേഷവുമുള്ള ഘട്ടങ്ങൾക്കും ബാധകമാണ്."},
    handles={"en": "round-the-clock contact · legal/medical referral", "hi": "चौबीसों घंटे संपर्क · क़ानूनी/चिकित्सा सहायता",
             "ta": "இருபத்தி நான்கு மணி நேர தொடர்பு · சட்ட/மருத்துவ உதவி", "te": "రౌండ్-ది-క్లాక్ సంప్రదింపు · న్యాయ/వైద్య సహాయం",
             "ml": "24 മണിക്കൂർ ബന്ധപ്പെടൽ · നിയമ/മെഡിക്കൽ സഹായം"},
    steps={"en": ["Call, email or message OWRC or your nearest mission's emergency line as soon as the problem starts — don't wait to see if it resolves itself.",
                  "Describe the situation clearly: employer, location, and what's happened (wages withheld, passport taken, unsafe housing).",
                  "OWRC or the mission logs the case and connects you to the right help — legal, medical, shelter, or a labour dispute officer.",
                  "Keep any evidence (contract, messages, payslips) — you'll likely be asked for it later."],
           "hi": ["समस्या शुरू होते ही OWRC या अपने नज़दीकी मिशन की आपातकालीन लाइन पर कॉल, ईमेल या मैसेज करें — यह देखने का इंतज़ार न करें कि यह अपने आप सुलझ जाएगी।",
                  "स्थिति स्पष्ट रूप से बताएँ: नियोक्ता, जगह, और क्या हुआ (वेतन रोका गया, पासपोर्ट लिया गया, असुरक्षित आवास)।",
                  "OWRC या मिशन मामला दर्ज करता है और आपको सही मदद से जोड़ता है — क़ानूनी, चिकित्सा, आश्रय, या श्रम विवाद अधिकारी।",
                  "कोई भी सबूत (अनुबंध, संदेश, वेतन पर्ची) रखें — बाद में इनकी माँग हो सकती है।"],
           "ta": ["பிரச்சினை தொடங்கியவுடன் OWRC அல்லது உங்கள் அருகிலுள்ள தூதரகத்தின் அவசர எண்ணை அழைக்கவும், மின்னஞ்சல் அல்லது செய்தி அனுப்பவும் — அது தானாகவே தீரும் என்று காத்திருக்க வேண்டாம்.",
                  "நிலைமையை தெளிவாக விவரிக்கவும்: முதலாளி, இடம், என்ன நடந்தது (ஊதியம் தடுக்கப்பட்டது, பாஸ்போர்ட் எடுக்கப்பட்டது, பாதுகாப்பற்ற வீடு).",
                  "OWRC அல்லது தூதரகம் வழக்கைப் பதிவு செய்து சரியான உதவியுடன் உங்களை இணைக்கும் — சட்டம், மருத்துவம், தங்குமிடம், அல்லது தொழிலாளர் தகராறு அதிகாரி.",
                  "ஏதேனும் ஆதாரங்களை (ஒப்பந்தம், செய்திகள், ஊதியப் பட்டியல்) வைத்திருங்கள் — பின்னர் அவை கேட்கப்படலாம்."],
           "te": ["సమస్య మొదలైన వెంటనే OWRC కి లేదా మీ సమీప మిషన్ యొక్క అత్యవసర లైన్‌కు కాల్ చేయండి, ఇమెయిల్ లేదా మెసేజ్ చేయండి — అది దానంతట అదే పరిష్కారం అవుతుందా అని వేచి ఉండకండి.",
                  "పరిస్థితిని స్పష్టంగా వివరించండి: యజమాని, ప్రదేశం, ఏమి జరిగింది (జీతం ఆపడం, పాస్‌పోర్ట్ తీసుకోవడం, అసురక్షిత గృహవసతి).",
                  "OWRC లేదా మిషన్ కేసును నమోదు చేసి సరైన సహాయంతో మిమ్మల్ని కలుపుతుంది — న్యాయ, వైద్య, ఆశ్రయం, లేదా కార్మిక వివాద అధికారి.",
                  "ఏదైనా ఆధారాలు (ఒప్పందం, సందేశాలు, జీతం స్లిప్‌లు) ఉంచుకోండి — తర్వాత అవి అడగబడవచ్చు."],
           "ml": ["പ്രശ്നം തുടങ്ങിയ ഉടനെ OWRC യെയോ നിങ്ങളുടെ അടുത്തുള്ള മിഷന്റെ അടിയന്തിര ലൈനിലേക്കോ വിളിക്കുക, ഇമെയിൽ അല്ലെങ്കിൽ സന്ദേശം അയക്കുക — അത് സ്വയം പരിഹരിക്കുമോ എന്ന് കാത്തിരിക്കരുത്.",
                  "സാഹചര്യം വ്യക്തമായി വിവരിക്കുക: തൊഴിലുടമ, സ്ഥലം, എന്താണ് സംഭവിച്ചത് (ശമ്പളം തടഞ്ഞുവച്ചത്, പാസ്‌പോർട്ട് എടുത്തത്, സുരക്ഷിതമല്ലാത്ത താമസം).",
                  "OWRC അല്ലെങ്കിൽ മിഷൻ കേസ് രേഖപ്പെടുത്തി ശരിയായ സഹായവുമായി നിങ്ങളെ ബന്ധിപ്പിക്കും — നിയമം, മെഡിക്കൽ, അഭയം, അല്ലെങ്കിൽ തൊഴിൽ തർക്ക ഉദ്യോഗസ്ഥൻ.",
                  "എന്തെങ്കിലും തെളിവുകൾ (കരാർ, സന്ദേശങ്ങൾ, ശമ്പള സ്ലിപ്പുകൾ) സൂക്ഷിക്കുക — പിന്നീട് ഇവ ചോദിക്കപ്പെടാം."]},
    docs={"en": ["Passport/ID details", "Current location and a working contact number", "Employer or agent's name, if relevant", "Any written proof of the issue (contract, messages, payslips)"],
          "hi": ["पासपोर्ट/पहचान विवरण", "वर्तमान स्थान और सक्रिय संपर्क नंबर", "नियोक्ता या एजेंट का नाम, अगर लागू हो", "समस्या का कोई लिखित प्रमाण (अनुबंध, संदेश, वेतन पर्ची)"],
          "ta": ["பாஸ்போர்ட்/அடையாள விவரங்கள்", "தற்போதைய இருப்பிடம் மற்றும் இயங்கும் தொடர்பு எண்", "முதலாளி அல்லது முகவரின் பெயர், தேவைப்பட்டால்", "பிரச்சினைக்கான ஏதேனும் எழுத்துப்பூர்வ ஆதாரம் (ஒப்பந்தம், செய்திகள், ஊதியப் பட்டியல்)"],
          "te": ["పాస్‌పోర్ట్/గుర్తింపు వివరాలు", "ప్రస్తుత ప్రదేశం మరియు పనిచేసే సంప్రదింపు నంబర్", "యజమాని లేదా ఏజెంట్ పేరు, వర్తిస్తే", "సమస్యకు సంబంధించిన ఏదైనా లిఖితపూర్వక ఆధారం (ఒప్పందం, సందేశాలు, జీతం స్లిప్‌లు)"],
          "ml": ["പാസ്‌പോർട്ട്/ഐഡി വിവരങ്ങൾ", "നിലവിലെ സ്ഥലവും പ്രവർത്തിക്കുന്ന ബന്ധപ്പെടാനുള്ള നമ്പറും", "തൊഴിലുടമയുടെയോ ഏജന്റിന്റെയോ പേര്, ബാധകമെങ്കിൽ", "പ്രശ്നത്തിന്റെ രേഖാമൂലമുള്ള തെളിവ് (കരാർ, സന്ദേശങ്ങൾ, ശമ്പള സ്ലിപ്പുകൾ)"]},
    note={"en": "This is a support line, not a police line — for immediate physical danger, contact local emergency services first, then OWRC.",
          "hi": "यह एक सहायता लाइन है, पुलिस लाइन नहीं — तुरंत शारीरिक ख़तरे की स्थिति में पहले स्थानीय आपातकालीन सेवाओं से संपर्क करें, फिर OWRC से।",
          "ta": "இது ஒரு உதவி எண், காவல் எண் அல்ல — உடனடி உடல் ஆபத்து இருந்தால் முதலில் உள்ளூர் அவசர சேவைகளைத் தொடர்பு கொள்ளவும், பின்னர் OWRC ஐ.",
          "te": "ఇది ఒక సహాయ లైన్, పోలీసు లైన్ కాదు — తక్షణ శారీరక ప్రమాదం ఉంటే మొదట స్థానిక అత్యవసర సేవలను సంప్రదించండి, తర్వాత OWRC ని.",
          "ml": "ഇത് ഒരു സപ്പോർട്ട് ലൈൻ ആണ്, പോലീസ് ലൈൻ അല്ല — ഉടനടി ശാരീരിക അപകടം ഉണ്ടെങ്കിൽ ആദ്യം പ്രാദേശിക അടിയന്തിര സേവനങ്ങളെ ബന്ധപ്പെടുക, പിന്നീട് OWRC യെ."},
    location={"en": "Online/phone service — works from anywhere; covers Gulf and other major worker-destination countries",
               "hi": "ऑनलाइन/फ़ोन सेवा — कहीं से भी उपयोग करें; ख़ाड़ी और अन्य प्रमुख कामगार-गंतव्य देशों को कवर करता है",
               "ta": "ஆன்லைன்/தொலைபேசி சேவை — எங்கிருந்தும் பயன்படுத்தலாம்; வளைகுடா மற்றும் பிற முக்கிய தொழிலாளர் இலக்கு நாடுகளை உள்ளடக்கியது",
               "te": "ఆన్‌లైన్/ఫోన్ సేవ — ఎక్కడి నుండైనా పనిచేస్తుంది; గల్ఫ్ మరియు ఇతర ప్రధాన కార్మిక-గమ్యస్థాన దేశాలను కవర్ చేస్తుంది",
               "ml": "ഓൺലൈൻ/ഫോൺ സേവനം — എവിടെ നിന്നും ഉപയോഗിക്കാം; ഗൾഫും മറ്റ് പ്രധാന തൊഴിലാളി-ലക്ഷ്യ രാജ്യങ്ങളും ഉൾക്കൊള്ളുന്നു"},
    phone={"en": "1800-11-3090 (toll-free, India) · +91-124-2341002 (from abroad) · 0124-4420215",
            "hi": "1800-11-3090 (टोल-फ़्री, भारत) · +91-124-2341002 (विदेश से) · 0124-4420215",
            "ta": "1800-11-3090 (கட்டணமில்லா, இந்தியா) · +91-124-2341002 (வெளிநாட்டிலிருந்து) · 0124-4420215",
            "te": "1800-11-3090 (టోల్-ఫ్రీ, భారత్) · +91-124-2341002 (విదేశం నుండి) · 0124-4420215",
            "ml": "1800-11-3090 (ടോൾ-ഫ്രീ, ഇന്ത്യ) · +91-124-2341002 (വിദേശത്ത് നിന്ന്) · 0124-4420215"},
    email={"en": "helpline@owrc.in", "hi": "helpline@owrc.in", "ta": "helpline@owrc.in", "te": "helpline@owrc.in", "ml": "helpline@owrc.in"},
    links=[
        {"href": "https://www.owrc.in", "label": {"en": "↗ OWRC — current helpline & contact details", "hi": "↗ OWRC — मौजूदा हेल्पलाइन और संपर्क विवरण",
                                                    "ta": "↗ OWRC — தற்போதைய உதவி எண் & தொடர்பு விவரங்கள்", "te": "↗ OWRC — ప్రస్తుత హెల్ప్‌లైన్ & సంప్రదింపు వివరాలు",
                                                    "ml": "↗ OWRC — നിലവിലെ ഹെൽപ്‌ലൈൻ & ബന്ധപ്പെടാനുള്ള വിവരങ്ങൾ"}},
        {"href": "https://www.mea.gov.in/owrc-and-pbsk", "label": {"en": "↗ Background — mea.gov.in", "hi": "↗ पृष्ठभूमि — mea.gov.in",
                                                                    "ta": "↗ பின்னணி — mea.gov.in", "te": "↗ నేపథ్యం — mea.gov.in", "ml": "↗ പശ്ചാത്തലം — mea.gov.in"}},
    ],
)

entry(
    category="emergency", emergency=True, badge_official=True,
    search_en="arrested detained abroad consular access lawyer jail prison",
    title={"en": "Arrested or detained abroad", "hi": "विदेश में गिरफ़्तारी या हिरासत",
           "ta": "வெளிநாட்டில் கைது அல்லது தடுப்புக்காவல்", "te": "విదేశంలో అరెస్టు లేదా నిర్బంధం",
           "ml": "വിദേശത്ത് അറസ്റ്റ് അല്ലെങ്കിൽ തടങ്കൽ"},
    desc={"en": "You can ask local authorities to inform the nearest Indian mission and to arrange a consular visit. The mission can't secure a release, but it will visit, share a list of local lawyers, and keep your family back home informed.",
          "hi": "आप स्थानीय अधिकारियों से नज़दीकी भारतीय मिशन को सूचित करने और वाणिज्य दूत मुलाक़ात कराने को कह सकते हैं। मिशन रिहाई नहीं करा सकता, लेकिन मुलाक़ात करेगा, स्थानीय वकीलों की सूची देगा, और घर पर परिवार को सूचित रखेगा।",
          "ta": "உள்ளூர் அதிகாரிகளிடம் அருகிலுள்ள இந்திய தூதரகத்திற்கு தெரிவிக்கவும், துணைத்தூதரக வருகையை ஏற்பாடு செய்யவும் கேட்கலாம். தூதரகம் விடுதலையை உறுதி செய்ய முடியாது, ஆனால் வருகை தரும், உள்ளூர் வழக்கறிஞர்களின் பட்டியலை பகிரும், வீட்டில் உள்ள குடும்பத்தினருக்கு தகவல் தெரிவிக்கும்.",
          "te": "సమీప భారత మిషన్‌కు తెలియజేయమని, కాన్సులర్ సందర్శన ఏర్పాటు చేయమని స్థానిక అధికారులను మీరు అడగవచ్చు. మిషన్ విడుదల చేయించలేదు, కానీ సందర్శిస్తుంది, స్థానిక న్యాయవాదుల జాబితా ఇస్తుంది, ఇంట్లో కుటుంబానికి సమాచారం అందిస్తుంది.",
          "ml": "അടുത്തുള്ള ഇന്ത്യൻ മിഷനെ അറിയിക്കാനും കോൺസുലാർ സന്ദർശനം ഏർപ്പാടാക്കാനും പ്രാദേശിക അധികാരികളോട് ആവശ്യപ്പെടാം. മോചനം ഉറപ്പാക്കാൻ മിഷന് കഴിയില്ല, പക്ഷേ സന്ദർശിക്കും, പ്രാദേശിക അഭിഭാഷകരുടെ പട്ടിക നൽകും, നാട്ടിലെ കുടുംബത്തെ വിവരം അറിയിക്കും."},
    handles={"en": "consular access · lawyer referrals · family liaison", "hi": "वाणिज्य दूत पहुँच · वकील सिफ़ारिश · परिवार संपर्क",
             "ta": "துணைத்தூதரக அணுகல் · வழக்கறிஞர் பரிந்துரை · குடும்ப தொடர்பு", "te": "కాన్సులర్ యాక్సెస్ · న్యాయవాది సిఫార్సు · కుటుంబ సంప్రదింపు",
             "ml": "കോൺസുലാർ ആക്സസ് · അഭിഭാഷക ശുപാർശ · കുടുംബ ബന്ധം"},
    steps={"en": ["Ask the arresting authority, clearly and immediately, to notify the Indian mission — this is a right under the Vienna Convention on Consular Relations.",
                  "Avoid signing anything you don't fully understand until a lawyer or consular officer has seen it.",
                  "Once notified, the mission normally arranges a consular visit and shares a list of local lawyers.",
                  "Ask a family member or friend to also inform the mission directly, in case the official notification is delayed."],
           "hi": ["गिरफ़्तार करने वाले अधिकारी से स्पष्ट रूप से और तुरंत भारतीय मिशन को सूचित करने को कहें — यह वियना कन्वेंशन के तहत आपका अधिकार है।",
                  "जब तक कोई वकील या वाणिज्य दूत अधिकारी न देख ले, ऐसी किसी चीज़ पर हस्ताक्षर न करें जिसे आप पूरी तरह न समझें।",
                  "सूचना मिलने पर, मिशन आमतौर पर वाणिज्य दूत मुलाक़ात की व्यवस्था करता है और स्थानीय वकीलों की सूची देता है।",
                  "परिवार के किसी सदस्य या मित्र से भी मिशन को सीधे सूचित करने को कहें, अगर आधिकारिक सूचना में देरी हो।"],
           "ta": ["இந்திய தூதரகத்திற்குத் தெரிவிக்குமாறு கைது செய்யும் அதிகாரியிடம் தெளிவாகவும் உடனடியாகவும் கேளுங்கள் — இது வியன்னா ஒப்பந்தத்தின் கீழ் உங்கள் உரிமை.",
                  "வழக்கறிஞர் அல்லது துணைத்தூதரக அதிகாரி பார்க்கும் வரை நீங்கள் முழுமையாக புரிந்துகொள்ளாத எதிலும் கையெழுத்திட வேண்டாம்.",
                  "தெரிவிக்கப்பட்டதும், தூதரகம் பொதுவாக ஒரு துணைத்தூதரக வருகையை ஏற்பாடு செய்து உள்ளூர் வழக்கறிஞர்களின் பட்டியலை பகிரும்.",
                  "அதிகாரப்பூர்வ அறிவிப்பு தாமதமானால், குடும்ப உறுப்பினர் அல்லது நண்பரையும் தூதரகத்திற்கு நேரடியாக தெரிவிக்கச் சொல்லுங்கள்."],
           "te": ["భారత మిషన్‌కు తెలియజేయమని అరెస్టు చేసిన అధికారిని స్పష్టంగా, వెంటనే అడగండి — ఇది వియన్నా ఒప్పందం ప్రకారం మీ హక్కు.",
                  "న్యాయవాది లేదా కాన్సులర్ అధికారి చూసే వరకు మీకు పూర్తిగా అర్థం కాని దేనిపైనా సంతకం చేయవద్దు.",
                  "తెలియజేసిన తర్వాత, మిషన్ సాధారణంగా కాన్సులర్ సందర్శనను ఏర్పాటు చేసి స్థానిక న్యాయవాదుల జాబితాను ఇస్తుంది.",
                  "అధికారిక సమాచారం ఆలస్యమైతే, కుటుంబ సభ్యుడు లేదా స్నేహితుడు కూడా నేరుగా మిషన్‌కు తెలియజేయమని అడగండి."],
           "ml": ["ഇന്ത്യൻ മിഷനെ അറിയിക്കാൻ അറസ്റ്റ് ചെയ്യുന്ന അധികാരിയോട് വ്യക്തമായും ഉടനടിയും ആവശ്യപ്പെടുക — ഇത് വിയന്ന കൺവെൻഷൻ പ്രകാരമുള്ള നിങ്ങളുടെ അവകാശമാണ്.",
                  "ഒരു അഭിഭാഷകനോ കോൺസുലാർ ഉദ്യോഗസ്ഥനോ കണ്ടതിനു ശേഷം മാത്രമേ പൂർണ്ണമായി മനസ്സിലാകാത്ത എന്തിലും ഒപ്പിടാവൂ.",
                  "അറിയിച്ചു കഴിഞ്ഞാൽ, മിഷൻ സാധാരണയായി ഒരു കോൺസുലാർ സന്ദർശനം ഏർപ്പാടാക്കുകയും പ്രാദേശിക അഭിഭാഷകരുടെ പട്ടിക നൽകുകയും ചെയ്യും.",
                  "ഔദ്യോഗിക അറിയിപ്പ് വൈകുകയാണെങ്കിൽ, ഒരു കുടുംബാംഗത്തോടോ സുഹൃത്തിനോടോ കൂടി മിഷനെ നേരിട്ട് അറിയിക്കാൻ ആവശ്യപ്പെടുക."]},
    docs={"en": ["Passport number and full name", "Name/location of the detaining authority", "A contact for next of kin"],
          "hi": ["पासपोर्ट नंबर और पूरा नाम", "हिरासत में रखने वाले अधिकारी का नाम/स्थान", "नज़दीकी परिजन के लिए संपर्क"],
          "ta": ["பாஸ்போர்ட் எண் மற்றும் முழுப் பெயர்", "தடுப்புக்காவல் அதிகாரியின் பெயர்/இடம்", "நெருங்கிய உறவினரின் தொடர்பு"],
          "te": ["పాస్‌పోర్ట్ నంబర్ మరియు పూర్తి పేరు", "నిర్బంధించిన అధికారి పేరు/ప్రదేశం", "సన్నిహిత బంధువుల సంప్రదింపు"],
          "ml": ["പാസ്‌പോർട്ട് നമ്പറും മുഴുവൻ പേരും", "തടങ്കലിൽ വച്ച അധികാരിയുടെ പേര്/സ്ഥലം", "അടുത്ത ബന്ധുവിന്റെ ബന്ധപ്പെടാനുള്ള വിവരം"]},
    note={"en": "The mission can't get someone released or intervene in a country's legal process — it monitors welfare, ensures fair treatment, and keeps family informed.",
          "hi": "मिशन किसी को रिहा नहीं करा सकता या किसी देश की क़ानूनी प्रक्रिया में हस्तक्षेप नहीं कर सकता — यह कल्याण की निगरानी करता है, उचित व्यवहार सुनिश्चित करता है, और परिवार को सूचित रखता है।",
          "ta": "தூதரகம் யாரையும் விடுவிக்கவோ ஒரு நாட்டின் சட்ட செயல்முறையில் தலையிடவோ முடியாது — இது நலனை கண்காணிக்கிறது, நியாயமான நடத்தையை உறுதி செய்கிறது, குடும்பத்திற்கு தகவல் தெரிவிக்கிறது.",
          "te": "మిషన్ ఎవరినీ విడుదల చేయించలేదు లేదా ఒక దేశ న్యాయ ప్రక్రియలో జోక్యం చేసుకోలేదు — ఇది సంక్షేమాన్ని పర్యవేక్షిస్తుంది, న్యాయమైన చికిత్సను నిర్ధారిస్తుంది, కుటుంబానికి సమాచారం అందిస్తుంది.",
          "ml": "മിഷന് ആരെയും മോചിപ്പിക്കാനോ ഒരു രാജ്യത്തിന്റെ നിയമ പ്രക്രിയയിൽ ഇടപെടാനോ കഴിയില്ല — ഇത് ക്ഷേമം നിരീക്ഷിക്കുന്നു, ന്യായമായ പെരുമാറ്റം ഉറപ്പാക്കുന്നു, കുടുംബത്തെ വിവരം അറിയിക്കുന്നു."},
    location={"en": "Your nearest Indian Mission — see the \"Find your High Commission/Consulate\" card below",
               "hi": "आपका नज़दीकी भारतीय मिशन — नीचे \"अपना उच्चायोग/वाणिज्य दूतावास खोजें\" कार्ड देखें",
               "ta": "உங்கள் அருகிலுள்ள இந்திய தூதரகம் — கீழே \"உங்கள் உயர் ஸ்தானிகராலயம்/தூதரகத்தைக் கண்டறியவும்\" அட்டையைப் பார்க்கவும்",
               "te": "మీ సమీప భారత మిషన్ — దిగువ \"మీ హై కమిషన్/కాన్సులేట్ కనుగొనండి\" కార్డు చూడండి",
               "ml": "നിങ്ങളുടെ ഏറ്റവും അടുത്ത ഇന്ത്യൻ മിഷൻ — താഴെയുള്ള \"നിങ്ങളുടെ ഹൈക്കമ്മീഷൻ/കോൺസുലേറ്റ് കണ്ടെത്തുക\" കാർഡ് കാണുക"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/indians-imprisoned-abroad", "label": {"en": "↗ Indians imprisoned abroad — mea.gov.in", "hi": "↗ विदेश में क़ैद भारतीय — mea.gov.in",
                                                                                    "ta": "↗ வெளிநாட்டில் சிறையில் உள்ள இந்தியர்கள் — mea.gov.in", "te": "↗ విదేశాల్లో జైలులో ఉన్న భారతీయులు — mea.gov.in",
                                                                                    "ml": "↗ വിദേശത്ത് ജയിലിലുള്ള ഇന്ത്യക്കാർ — mea.gov.in"}}],
)

entry(
    category="emergency", emergency=True, badge_official=True,
    search_en="death abroad mortal remains death certificate repatriation body",
    title={"en": "Death abroad: certificates & mortal remains", "hi": "विदेश में मृत्यु: प्रमाणपत्र और पार्थिव शरीर",
           "ta": "வெளிநாட்டில் மரணம்: சான்றிதழ்கள் & உடல் அனுப்புதல்", "te": "విదేశంలో మరణం: ధృవపత్రాలు & మృతదేహం తరలింపు",
           "ml": "വിദേശത്ത് മരണം: സർട്ടിഫിക്കറ്റുകളും മൃതദേഹവും"},
    desc={"en": "Missions can help register a death with local authorities, put together the paperwork India will accept, and coordinate sending mortal remains home. Where a family can't cover the cost, the Community Welfare Fund below can help fund the repatriation.",
          "hi": "मिशन स्थानीय अधिकारियों के साथ मृत्यु दर्ज कराने, भारत द्वारा स्वीकार्य काग़ज़ी काम तैयार करने, और पार्थिव शरीर को घर भेजने में समन्वय कर सकते हैं। अगर परिवार ख़र्च नहीं उठा सकता, तो नीचे दिया Community Welfare Fund प्रत्यावर्तन में मदद कर सकता है।",
          "ta": "உள்ளூர் அதிகாரிகளுடன் மரணத்தை பதிவு செய்ய, இந்தியா ஏற்றுக்கொள்ளும் ஆவணங்களை தயார் செய்ய, உடலை வீட்டிற்கு அனுப்ப ஒருங்கிணைக்க தூதரகங்கள் உதவலாம். செலவை குடும்பத்தால் ஈடுசெய்ய முடியாவிட்டால், கீழே உள்ள Community Welfare Fund திரும்ப அனுப்புவதற்கு உதவலாம்.",
          "te": "స్థానిక అధికారులతో మరణాన్ని నమోదు చేయడంలో, భారత్ అంగీకరించే కాగితాలను సిద్ధం చేయడంలో, మృతదేహాన్ని ఇంటికి పంపడాన్ని సమన్వయం చేయడంలో మిషన్లు సహాయపడగలవు. కుటుంబం ఖర్చు భరించలేకపోతే, దిగువ Community Welfare Fund తరలింపుకు నిధులు సమకూర్చడంలో సహాయపడగలదు.",
          "ml": "പ്രാദേശിക അധികാരികളുമായി മരണം രജിസ്റ്റർ ചെയ്യാനും, ഇന്ത്യ അംഗീകരിക്കുന്ന രേഖകൾ തയ്യാറാക്കാനും, മൃതദേഹം നാട്ടിലേക്ക് അയക്കാൻ ഏകോപിപ്പിക്കാനും മിഷനുകൾക്ക് സഹായിക്കാം. ചെലവ് വഹിക്കാൻ കുടുംബത്തിന് കഴിയുന്നില്ലെങ്കിൽ, താഴെയുള്ള Community Welfare Fund തിരിച്ചയക്കലിന് ധനസഹായം നൽകാം."},
    handles={"en": "death certificate · repatriation · ICWF funding", "hi": "मृत्यु प्रमाणपत्र · प्रत्यावर्तन · ICWF फंडिंग",
             "ta": "மரண சான்றிதழ் · திருப்பி அனுப்புதல் · ICWF நிதி", "te": "మరణ ధృవపత్రం · తరలింపు · ICWF నిధులు",
             "ml": "മരണ സർട്ടിഫിക്കറ്റ് · തിരിച്ചയക്കൽ · ICWF ധനസഹായം"},
    steps={"en": ["The local authority or hospital issues a local death certificate first — nothing else can proceed without it.",
                  "Register the death with the nearest Indian mission, in person or via India's consular services portal where available.",
                  "The mission attests the death certificate; once a funeral home issues embalming/health clearance, it issues a No-Objection Certificate for the remains to travel.",
                  "If cost is the barrier, ask the mission about ICWF support for repatriation (see Embassy & consular help below)."],
           "hi": ["स्थानीय अधिकारी या अस्पताल पहले स्थानीय मृत्यु प्रमाणपत्र जारी करता है — इसके बिना कुछ भी आगे नहीं बढ़ सकता।",
                  "नज़दीकी भारतीय मिशन के पास व्यक्तिगत रूप से या जहाँ उपलब्ध हो वहाँ भारत के वाणिज्य दूत सेवा पोर्टल के ज़रिए मृत्यु दर्ज कराएँ।",
                  "मिशन मृत्यु प्रमाणपत्र सत्यापित करता है; अंत्येष्टि गृह द्वारा एम्बामिंग/स्वास्थ्य मंज़ूरी जारी होने के बाद, यह पार्थिव शरीर की यात्रा के लिए अनापत्ति प्रमाणपत्र जारी करता है।",
                  "अगर ख़र्च बाधा है, तो मिशन से प्रत्यावर्तन के लिए ICWF सहायता के बारे में पूछें (नीचे दूतावास और वाणिज्य सहायता देखें)।"],
           "ta": ["உள்ளூர் அதிகாரி அல்லது மருத்துவமனை முதலில் உள்ளூர் மரண சான்றிதழை வழங்குகிறது — இது இல்லாமல் வேறு எதுவும் தொடர முடியாது.",
                  "நேரில் அல்லது கிடைக்கும் இடங்களில் இந்தியாவின் துணைத்தூதரக சேவைகள் போர்ட்டல் மூலம் அருகிலுள்ள இந்திய தூதரகத்தில் மரணத்தை பதிவு செய்யவும்.",
                  "தூதரகம் மரண சான்றிதழை சான்றளிக்கிறது; இறுதிச் சடங்கு இல்லம் எம்பாமிங்/சுகாதார அனுமதி வழங்கியதும், உடல் பயணிக்க தடையில்லா சான்றிதழை வழங்குகிறது.",
                  "செலவு தடையாக இருந்தால், திருப்பி அனுப்புவதற்கான ICWF உதவி பற்றி தூதரகத்திடம் கேளுங்கள் (கீழே தூதரகம் & துணைத்தூதரக உதவி பார்க்கவும்)."],
           "te": ["స్థానిక అధికారి లేదా ఆసుపత్రి ముందుగా స్థానిక మరణ ధృవపత్రాన్ని జారీ చేస్తుంది — ఇది లేకుండా మరేదీ ముందుకు సాగదు.",
                  "వ్యక్తిగతంగా లేదా అందుబాటులో ఉన్న చోట భారత కాన్సులర్ సేవల పోర్టల్ ద్వారా సమీప భారత మిషన్‌లో మరణాన్ని నమోదు చేయండి.",
                  "మిషన్ మరణ ధృవపత్రాన్ని ధృవీకరిస్తుంది; ఫ్యూనరల్ హోమ్ ఎంబామింగ్/ఆరోగ్య అనుమతి జారీ చేసిన తర్వాత, మృతదేహం ప్రయాణానికి నో-అబ్జెక్షన్ సర్టిఫికేట్ జారీ చేస్తుంది.",
                  "ఖర్చు అడ్డంకిగా ఉంటే, తరలింపు కోసం ICWF సహాయం గురించి మిషన్‌ను అడగండి (దిగువ రాయబార & కాన్సులర్ సహాయం చూడండి)."],
           "ml": ["പ്രാദേശിക അധികാരി അല്ലെങ്കിൽ ആശുപത്രി ആദ്യം പ്രാദേശിക മരണ സർട്ടിഫിക്കറ്റ് നൽകുന്നു — ഇത് കൂടാതെ മറ്റൊന്നും മുന്നോട്ട് പോകില്ല.",
                  "നേരിട്ട് അല്ലെങ്കിൽ ലഭ്യമായ ഇടത്ത് ഇന്ത്യയുടെ കോൺസുലാർ സേവന പോർട്ടൽ വഴി അടുത്തുള്ള ഇന്ത്യൻ മിഷനിൽ മരണം രജിസ്റ്റർ ചെയ്യുക.",
                  "മിഷൻ മരണ സർട്ടിഫിക്കറ്റ് സാക്ഷ്യപ്പെടുത്തുന്നു; ഫ്യൂണറൽ ഹോം എംബാമിംഗ്/ആരോഗ്യ ക്ലിയറൻസ് നൽകിക്കഴിഞ്ഞാൽ, മൃതദേഹം യാത്ര ചെയ്യാൻ നോ-ഒബ്ജക്ഷൻ സർട്ടിഫിക്കറ്റ് നൽകുന്നു.",
                  "ചെലവാണ് തടസ്സമെങ്കിൽ, തിരിച്ചയക്കലിനുള്ള ICWF സഹായത്തെക്കുറിച്ച് മിഷനോട് ചോദിക്കുക (താഴെ എംബസി & കോൺസുലാർ സഹായം കാണുക)."]},
    docs={"en": ["Deceased's passport and local death certificate", "Informant's ID and proof of relationship", "Embalming/health certificate, for repatriation of remains"],
          "hi": ["मृतक का पासपोर्ट और स्थानीय मृत्यु प्रमाणपत्र", "सूचना देने वाले का पहचान पत्र और रिश्ते का प्रमाण", "पार्थिव शरीर के प्रत्यावर्तन हेतु एम्बामिंग/स्वास्थ्य प्रमाणपत्र"],
          "ta": ["இறந்தவரின் பாஸ்போர்ட் மற்றும் உள்ளூர் மரண சான்றிதழ்", "தகவல் தெரிவிப்பவரின் அடையாள அட்டை மற்றும் உறவு சான்று", "உடலை திருப்பி அனுப்ப எம்பாமிங்/சுகாதார சான்றிதழ்"],
          "te": ["మృతుడి పాస్‌పోర్ట్ మరియు స్థానిక మరణ ధృవపత్రం", "సమాచారం ఇచ్చినవారి గుర్తింపు మరియు సంబంధ రుజువు", "మృతదేహం తరలింపు కోసం ఎంబామింగ్/ఆరోగ్య ధృవపత్రం"],
          "ml": ["മരിച്ചയാളുടെ പാസ്‌പോർട്ടും പ്രാദേശിക മരണ സർട്ടിഫിക്കറ്റും", "വിവരം നൽകുന്നയാളുടെ ഐഡിയും ബന്ധത്തിന്റെ തെളിവും", "മൃതദേഹം തിരിച്ചയക്കാൻ എംബാമിംഗ്/ആരോഗ്യ സർട്ടിഫിക്കറ്റ്"]},
    note={"en": "Repatriating a body is paperwork- and time-heavy — expect days, not hours. The mission's consular section coordinates it, not the funeral home.",
          "hi": "पार्थिव शरीर को स्वदेश भेजना काग़ज़ी काम और समय की दृष्टि से भारी है — घंटों नहीं, दिनों की उम्मीद रखें। इसे मिशन का वाणिज्य दूत अनुभाग समन्वित करता है, अंत्येष्टि गृह नहीं।",
          "ta": "உடலைத் திருப்பி அனுப்புவது ஆவணப்பணி மற்றும் நேரம் அதிகம் தேவைப்படும் — மணிநேரங்கள் அல்ல, நாட்களை எதிர்பாருங்கள். இதை தூதரகத்தின் துணைத்தூதரக பிரிவு ஒருங்கிணைக்கிறது, இறுதிச் சடங்கு இல்லம் அல்ல.",
          "te": "మృతదేహాన్ని తరలించడం కాగితం పని మరియు సమయం అధికంగా తీసుకుంటుంది — గంటలు కాదు, రోజులు ఆశించండి. దీన్ని మిషన్ యొక్క కాన్సులర్ విభాగం సమన్వయం చేస్తుంది, ఫ్యూనరల్ హోమ్ కాదు.",
          "ml": "മൃതദേഹം തിരിച്ചയക്കുന്നത് കടലാസ്-സമയ അധികമായ പ്രക്രിയയാണ് — മണിക്കൂറുകളല്ല, ദിവസങ്ങൾ പ്രതീക്ഷിക്കുക. ഇത് ഏകോപിപ്പിക്കുന്നത് മിഷന്റെ കോൺസുലാർ വിഭാഗമാണ്, ഫ്യൂണറൽ ഹോം അല്ല."},
    location={"en": "Your nearest Indian Mission's consular section", "hi": "आपके नज़दीकी भारतीय मिशन का वाणिज्य दूत अनुभाग",
               "ta": "உங்கள் அருகிலுள்ள இந்திய தூதரகத்தின் துணைத்தூதரக பிரிவு", "te": "మీ సమీప భారత మిషన్ యొక్క కాన్సులర్ విభాగం",
               "ml": "നിങ്ങളുടെ ഏറ്റവും അടുത്ത ഇന്ത്യൻ മിഷന്റെ കോൺസുലാർ വിഭാഗം"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/transfer-of-mortal-remains", "label": {"en": "↗ Transfer of mortal remains — mea.gov.in", "hi": "↗ पार्थिव शरीर का स्थानांतरण — mea.gov.in",
                                                                                     "ta": "↗ உடல் மாற்றுதல் — mea.gov.in", "te": "↗ మృతదేహం తరలింపు — mea.gov.in", "ml": "↗ മൃതദേഹം കൈമാറ്റം — mea.gov.in"}}],
)

entry(
    category="emergency", emergency=True, badge_official=True,
    search_en="crisis evacuation travel advisory war conflict natural disaster operation ganga sindhu",
    title={"en": "Crisis advisories & evacuation", "hi": "संकट परामर्श और निकासी", "ta": "நெருக்கடி ஆலோசனைகள் & வெளியேற்றம்",
           "te": "సంక్షోభ సలహాలు & తరలింపు", "ml": "പ്രതിസന്ധി മുന്നറിയിപ്പുകളും ഒഴിപ്പിക്കലും"},
    desc={"en": "When a country turns unsafe — conflict, unrest, a natural disaster — the mission posts a travel advisory and, in a full evacuation, registers and moves Indian nationals out first, as in Operation Ganga or Operation Sindhu. Checking this page and following your mission's channels is the fastest way to know what's happening.",
          "hi": "जब कोई देश असुरक्षित हो जाता है — संघर्ष, अशांति, प्राकृतिक आपदा — मिशन यात्रा परामर्श जारी करता है और पूर्ण निकासी में, ऑपरेशन गंगा या ऑपरेशन सिंधु की तरह, पहले भारतीय नागरिकों को पंजीकृत कर बाहर निकालता है। यह पृष्ठ देखना और अपने मिशन के माध्यमों का पालन करना सबसे तेज़ तरीक़ा है।",
          "ta": "ஒரு நாடு பாதுகாப்பற்றதாக மாறும்போது — மோதல், அமைதியின்மை, இயற்கை பேரிடர் — தூதரகம் பயண ஆலோசனையை வெளியிடுகிறது, முழு வெளியேற்றத்தில், ஆபரேஷன் கங்கா அல்லது ஆபரேஷன் சிந்து போல, முதலில் இந்திய குடிமக்களை பதிவு செய்து வெளியேற்றுகிறது. இந்தப் பக்கத்தை சரிபார்ப்பதும் உங்கள் தூதரக வழிகளைப் பின்பற்றுவதும் என்ன நடக்கிறது என்பதை அறியும் வேகமான வழி.",
          "te": "ఒక దేశం అసురక్షితంగా మారినప్పుడు — సంఘర్షణ, అశాంతి, ప్రకృతి విపత్తు — మిషన్ ప్రయాణ సలహాను పోస్ట్ చేస్తుంది, పూర్తి తరలింపులో, ఆపరేషన్ గంగా లేదా ఆపరేషన్ సింధు వలె, మొదట భారతీయ పౌరులను నమోదు చేసి బయటకు తరలిస్తుంది. ఈ పేజీని తనిఖీ చేయడం మరియు మీ మిషన్ ఛానెల్‌లను అనుసరించడం ఏమి జరుగుతుందో తెలుసుకోవడానికి వేగవంతమైన మార్గం.",
          "ml": "ഒരു രാജ്യം അപകടകരമാകുമ്പോൾ — സംഘർഷം, അസ്വസ്ഥത, പ്രകൃതി ദുരന്തം — മിഷൻ യാത്രാ മുന്നറിയിപ്പ് പോസ്റ്റ് ചെയ്യുന്നു, പൂർണ്ണ ഒഴിപ്പിക്കലിൽ, ഓപ്പറേഷൻ ഗംഗ അല്ലെങ്കിൽ ഓപ്പറേഷൻ സിന്ധു പോലെ, ആദ്യം ഇന്ത്യൻ പൗരന്മാരെ രജിസ്റ്റർ ചെയ്ത് പുറത്തെത്തിക്കുന്നു. ഈ പേജ് പരിശോധിക്കുന്നതും നിങ്ങളുടെ മിഷന്റെ ചാനലുകൾ പിന്തുടരുന്നതുമാണ് എന്താണ് സംഭവിക്കുന്നതെന്ന് അറിയാനുള്ള വേഗതയേറിയ വഴി."},
    handles={"en": "live advisories · evacuation registration", "hi": "लाइव परामर्श · निकासी पंजीकरण", "ta": "நேரடி ஆலோசனைகள் · வெளியேற்றப் பதிவு",
             "te": "లైవ్ సలహాలు · తరలింపు నమోదు", "ml": "തത്സമയ മുന്നറിയിപ്പുകൾ · ഒഴിപ്പിക്കൽ രജിസ്ട്രേഷൻ"},
    steps={"en": ["Check the MEA travel advisories page for your country as soon as tensions or a disaster start making news.",
                  "Register your presence with the nearest mission if it asks — often a simple online form during a crisis — this is how you get found for evacuation flights.",
                  "Follow the mission's social media/website for real-time instructions rather than general news.",
                  "Keep your passport, some cash, and essential documents together and reachable."],
           "hi": ["जैसे ही तनाव या आपदा की ख़बरें आने लगें, अपने देश के लिए MEA यात्रा परामर्श पृष्ठ जाँचें।",
                  "अगर मिशन माँगे तो नज़दीकी मिशन के पास अपनी उपस्थिति पंजीकृत कराएँ — अक्सर संकट के दौरान एक सरल ऑनलाइन फ़ॉर्म — इसी से आप निकासी उड़ानों के लिए खोजे जाते हैं।",
                  "सामान्य समाचार के बजाय वास्तविक समय के निर्देशों के लिए मिशन के सोशल मीडिया/वेबसाइट का अनुसरण करें।",
                  "अपना पासपोर्ट, कुछ नक़दी, और ज़रूरी दस्तावेज़ साथ और पहुँच में रखें।"],
           "ta": ["பதற்றங்கள் அல்லது பேரிடர் செய்திகளில் வர ஆரம்பித்தவுடன், உங்கள் நாட்டிற்கான MEA பயண ஆலோசனை பக்கத்தை சரிபார்க்கவும்.",
                  "தூதரகம் கேட்டால் அருகிலுள்ள தூதரகத்தில் உங்கள் இருப்பை பதிவு செய்யவும் — நெருக்கடியின் போது பெரும்பாலும் ஒரு எளிய ஆன்லைன் படிவம் — வெளியேற்ற விமானங்களுக்கு நீங்கள் இதன் மூலமே கண்டறியப்படுவீர்கள்.",
                  "பொதுவான செய்திகளை விட நிகழ்நேர வழிமுறைகளுக்கு தூதரகத்தின் சமூக ஊடகம்/இணையதளத்தைப் பின்பற்றவும்.",
                  "உங்கள் பாஸ்போர்ட், சில பணம், மற்றும் அத்தியாவசிய ஆவணங்களை ஒன்றாக, எளிதில் எடுக்கும் வகையில் வைத்திருங்கள்."],
           "te": ["ఉద్రిక్తతలు లేదా విపత్తు వార్తలు రావడం మొదలుపెట్టిన వెంటనే, మీ దేశం కోసం MEA ప్రయాణ సలహా పేజీని తనిఖీ చేయండి.",
                  "మిషన్ అడిగితే సమీప మిషన్‌లో మీ ఉనికిని నమోదు చేసుకోండి — సంక్షోభ సమయంలో తరచుగా సాధారణ ఆన్‌లైన్ ఫారం — తరలింపు విమానాల కోసం మిమ్మల్ని కనుగొనేది ఇలానే.",
                  "సాధారణ వార్తల కంటే మిషన్ యొక్క సోషల్ మీడియా/వెబ్‌సైట్‌ను రియల్-టైమ్ సూచనల కోసం అనుసరించండి.",
                  "మీ పాస్‌పోర్ట్, కొంత నగదు, మరియు అవసరమైన పత్రాలను కలిపి, అందుబాటులో ఉంచుకోండి."],
           "ml": ["സംഘർഷമോ ദുരന്തമോ വാർത്തയാകാൻ തുടങ്ങിയ ഉടനെ നിങ്ങളുടെ രാജ്യത്തിനുള്ള MEA യാത്രാ മുന്നറിയിപ്പ് പേജ് പരിശോധിക്കുക.",
                  "മിഷൻ ആവശ്യപ്പെട്ടാൽ അടുത്തുള്ള മിഷനിൽ നിങ്ങളുടെ സാന്നിധ്യം രജിസ്റ്റർ ചെയ്യുക — പ്രതിസന്ധി സമയത്ത് പലപ്പോഴും ലളിതമായ ഓൺലൈൻ ഫോം — ഒഴിപ്പിക്കൽ വിമാനങ്ങൾക്കായി നിങ്ങളെ കണ്ടെത്തുന്നത് ഇങ്ങനെയാണ്.",
                  "സാധാരണ വാർത്തകൾക്ക് പകരം തത്സമയ നിർദ്ദേശങ്ങൾക്കായി മിഷന്റെ സോഷ്യൽ മീഡിയ/വെബ്സൈറ്റ് പിന്തുടരുക.",
                  "നിങ്ങളുടെ പാസ്‌പോർട്ട്, കുറച്ച് പണം, ആവശ്യമായ രേഖകൾ എന്നിവ ഒരുമിച്ചും എടുക്കാൻ പാകത്തിലും സൂക്ഷിക്കുക."]},
    docs={"en": ["Passport details", "Current address/location", "A working phone number"],
          "hi": ["पासपोर्ट विवरण", "वर्तमान पता/स्थान", "सक्रिय फ़ोन नंबर"],
          "ta": ["பாஸ்போர்ட் விவரங்கள்", "தற்போதைய முகவரி/இடம்", "இயங்கும் தொலைபேசி எண்"],
          "te": ["పాస్‌పోర్ట్ వివరాలు", "ప్రస్తుత చిరునామా/ప్రదేశం", "పనిచేసే ఫోన్ నంబర్"],
          "ml": ["പാസ്‌പോർട്ട് വിവരങ്ങൾ", "നിലവിലെ വിലാസം/സ്ഥലം", "പ്രവർത്തിക്കുന്ന ഫോൺ നമ്പർ"]},
    note={"en": "Evacuation operations (like Operation Ganga or Operation Sindhu) are announced during the crisis itself — there's no pre-registration list to join in advance.",
          "hi": "निकासी अभियान (जैसे ऑपरेशन गंगा या ऑपरेशन सिंधु) संकट के दौरान ही घोषित किए जाते हैं — पहले से जुड़ने के लिए कोई पूर्व-पंजीकरण सूची नहीं होती।",
          "ta": "வெளியேற்ற நடவடிக்கைகள் (ஆபரேஷன் கங்கா அல்லது ஆபரேஷன் சிந்து போன்றவை) நெருக்கடியின் போதே அறிவிக்கப்படும் — முன்கூட்டியே சேர பதிவு பட்டியல் எதுவும் இல்லை.",
          "te": "తరలింపు కార్యకలాపాలు (ఆపరేషన్ గంగా లేదా ఆపరేషన్ సింధు వంటివి) సంక్షోభ సమయంలోనే ప్రకటించబడతాయి — ముందుగానే చేరడానికి ప్రీ-రిజిస్ట్రేషన్ జాబితా ఏదీ లేదు.",
          "ml": "ഒഴിപ്പിക്കൽ പ്രവർത്തനങ്ങൾ (ഓപ്പറേഷൻ ഗംഗ അല്ലെങ്കിൽ ഓപ്പറേഷൻ സിന്ധു പോലുള്ളവ) പ്രതിസന്ധി സമയത്ത് തന്നെ പ്രഖ്യാപിക്കുന്നു — മുൻകൂട്ടി ചേരാൻ ഒരു രജിസ്ട്രേഷൻ പട്ടികയും ഇല്ല."},
    location={"en": "Online (MEA advisories page) + your mission's own channels",
               "hi": "ऑनलाइन (MEA परामर्श पृष्ठ) + आपके मिशन के अपने माध्यम",
               "ta": "ஆன்லைன் (MEA ஆலோசனை பக்கம்) + உங்கள் தூதரகத்தின் சொந்த வழிகள்",
               "te": "ఆన్‌లైన్ (MEA సలహాల పేజీ) + మీ మిషన్ యొక్క సొంత ఛానెల్‌లు",
               "ml": "ഓൺലൈൻ (MEA മുന്നറിയിപ്പ് പേജ്) + നിങ്ങളുടെ മിഷന്റെ സ്വന്തം ചാനലുകൾ"},
    phone={"en": "MEA 24x7 Control Room (stood up during major crises — number reissued each time, e.g. 1800-11-8797 toll-free / +91-11-2301-2113): check mea.gov.in for the live number",
            "hi": "MEA 24x7 कंट्रोल रूम (बड़े संकट के दौरान सक्रिय — हर बार नया नंबर, जैसे 1800-11-8797 टोल-फ़्री / +91-11-2301-2113): चालू नंबर के लिए mea.gov.in देखें",
            "ta": "MEA 24x7 கட்டுப்பாட்டு அறை (பெரிய நெருக்கடிகளின் போது இயக்கப்படும் — ஒவ்வொரு முறையும் புதிய எண், எ.கா. 1800-11-8797 கட்டணமில்லா / +91-11-2301-2113): நடப்பு எண்ணுக்கு mea.gov.in பார்க்கவும்",
            "te": "MEA 24x7 కంట్రోల్ రూమ్ (పెద్ద సంక్షోభాల సమయంలో ఏర్పాటు చేయబడుతుంది — ప్రతిసారీ కొత్త నంబర్, ఉదా. 1800-11-8797 టోల్-ఫ్రీ / +91-11-2301-2113): ప్రస్తుత నంబర్ కోసం mea.gov.in చూడండి",
            "ml": "MEA 24x7 കൺട്രോൾ റൂം (വലിയ പ്രതിസന്ധികളിൽ സജ്ജമാക്കുന്നു — ഓരോ തവണയും പുതിയ നമ്പർ, ഉദാ. 1800-11-8797 ടോൾ-ഫ്രീ / +91-11-2301-2113): നിലവിലെ നമ്പറിന് mea.gov.in കാണുക"},
    email=None,
    links=[{"href": "https://www.mea.gov.in/travel-advisories", "label": {"en": "↗ Travel advisories — mea.gov.in", "hi": "↗ यात्रा परामर्श — mea.gov.in",
                                                                            "ta": "↗ பயண ஆலோசனைகள் — mea.gov.in", "te": "↗ ప్రయాణ సలహాలు — mea.gov.in", "ml": "↗ യാത്രാ മുന്നറിയിപ്പുകൾ — mea.gov.in"}}],
)

entry(
    category="emergency", emergency=True, badge_official=True,
    search_en="find helpline number tele inquiry directory mission emergency contact",
    title={"en": "Find the right helpline number", "hi": "सही हेल्पलाइन नंबर खोजें", "ta": "சரியான உதவி எண்ணைக் கண்டறியவும்",
           "te": "సరైన హెల్ప్‌లైన్ నంబర్ కనుగొనండి", "ml": "ശരിയായ ഹെൽപ്‌ലൈൻ നമ്പർ കണ്ടെത്തുക"},
    desc={"en": "Every mission publishes its own emergency line, and MEA keeps a directory of tele-inquiry numbers by subject in Delhi. If a card on this page doesn't have the exact number you need, start here rather than guessing at one.",
          "hi": "हर मिशन अपनी आपातकालीन लाइन प्रकाशित करता है, और MEA दिल्ली में विषयवार टेली-इंक्वायरी नंबरों की सूची रखता है। अगर इस पृष्ठ के किसी कार्ड में ज़रूरी सटीक नंबर नहीं है, तो अंदाज़ा लगाने के बजाय यहाँ से शुरू करें।",
          "ta": "ஒவ்வொரு தூதரகமும் அதன் சொந்த அவசர எண்ணை வெளியிடுகிறது, MEA டெல்லியில் பொருள் வாரியாக டெலி-விசாரணை எண்களின் அடைவை வைத்திருக்கிறது. இந்தப் பக்கத்தில் உள்ள ஒரு அட்டையில் தேவையான சரியான எண் இல்லையென்றால், யூகிப்பதற்குப் பதிலாக இங்கிருந்து தொடங்குங்கள்.",
          "te": "ప్రతి మిషన్ దాని స్వంత అత్యవసర లైన్‌ను ప్రచురిస్తుంది, MEA ఢిల్లీలో అంశం వారీగా టెలి-ఎంక్వైరీ నంబర్ల డైరెక్టరీని ఉంచుతుంది. ఈ పేజీలోని ఒక కార్డులో మీకు కావలసిన ఖచ్చితమైన నంబర్ లేకపోతే, ఊహించే బదులు ఇక్కడ నుండి ప్రారంభించండి.",
          "ml": "ഓരോ മിഷനും അതിന്റേതായ അടിയന്തിര ലൈൻ പ്രസിദ്ധീകരിക്കുന്നു, MEA ഡൽഹിയിൽ വിഷയം അനുസരിച്ച് ടെലി-അന്വേഷണ നമ്പറുകളുടെ ഡയറക്ടറി സൂക്ഷിക്കുന്നു. ഈ പേജിലെ ഒരു കാർഡിൽ നിങ്ങൾക്ക് വേണ്ട കൃത്യമായ നമ്പർ ഇല്ലെങ്കിൽ, ഊഹിക്കുന്നതിന് പകരം ഇവിടെ നിന്ന് തുടങ്ങുക."},
    handles={"en": "helpline directory · by-subject inquiry", "hi": "हेल्पलाइन निर्देशिका · विषयवार पूछताछ", "ta": "உதவி எண் அடைவு · பொருள் வாரியான விசாரணை",
             "te": "హెల్ప్‌లైన్ డైరెక్టరీ · అంశం వారీగా విచారణ", "ml": "ഹെൽപ്‌ലൈൻ ഡയറക്ടറി · വിഷയം അനുസരിച്ചുള്ള അന്വേഷണം"},
    steps={"en": ["Start at MEA's tele-inquiry directory to find the right desk for your subject (passport, OCI, grievance, etc).",
                  "If it's mission-specific, check that mission's own \"Contact/Consular\" page for a direct local number.",
                  "If nothing fits, MADAD (see Embassy & consular help below) is the fallback for anything without an obvious number."],
           "hi": ["अपने विषय (पासपोर्ट, OCI, शिकायत, आदि) के लिए सही डेस्क खोजने हेतु MEA की टेली-इंक्वायरी निर्देशिका से शुरू करें।",
                  "अगर यह मिशन-विशिष्ट है, तो सीधे स्थानीय नंबर के लिए उस मिशन के अपने \"संपर्क/वाणिज्य दूत\" पृष्ठ की जाँच करें।",
                  "अगर कुछ भी फ़िट न बैठे, तो बिना स्पष्ट नंबर वाली किसी भी चीज़ के लिए MADAD (नीचे दूतावास और वाणिज्य सहायता देखें) विकल्प है।"],
           "ta": ["உங்கள் பொருளுக்கான (பாஸ்போர்ட், OCI, குறை, முதலியன) சரியான மேசையைக் கண்டறிய MEA இன் டெலி-விசாரணை அடைவில் தொடங்குங்கள்.",
                  "இது தூதரக-குறிப்பிட்டதாக இருந்தால், நேரடி உள்ளூர் எண்ணுக்கு அந்த தூதரகத்தின் சொந்த \"தொடர்பு/துணைத்தூதரகம்\" பக்கத்தை சரிபார்க்கவும்.",
                  "எதுவும் பொருந்தவில்லை என்றால், தெளிவான எண் இல்லாத எதற்கும் MADAD (கீழே தூதரகம் & துணைத்தூதரக உதவி பார்க்கவும்) மாற்று வழி."],
           "te": ["మీ అంశానికి (పాస్‌పోర్ట్, OCI, ఫిర్యాదు, మొదలైనవి) సరైన డెస్క్‌ను కనుగొనడానికి MEA యొక్క టెలి-ఎంక్వైరీ డైరెక్టరీలో ప్రారంభించండి.",
                  "ఇది మిషన్-నిర్దిష్టమైతే, ప్రత్యక్ష స్థానిక నంబర్ కోసం ఆ మిషన్ యొక్క సొంత \"సంప్రదింపు/కాన్సులర్\" పేజీని తనిఖీ చేయండి.",
                  "ఏదీ సరిపోకపోతే, స్పష్టమైన నంబర్ లేని దేనికైనా MADAD (దిగువ రాయబార & కాన్సులర్ సహాయం చూడండి) ప్రత్యామ్నాయం."],
           "ml": ["നിങ്ങളുടെ വിഷയത്തിന് (പാസ്‌പോർട്ട്, OCI, പരാതി, മുതലായവ) ശരിയായ ഡെസ്ക് കണ്ടെത്താൻ MEA യുടെ ടെലി-അന്വേഷണ ഡയറക്ടറിയിൽ തുടങ്ങുക.",
                  "ഇത് മിഷൻ-നിർദ്ദിഷ്ടമാണെങ്കിൽ, നേരിട്ടുള്ള പ്രാദേശിക നമ്പറിനായി ആ മിഷന്റെ സ്വന്തം \"ബന്ധപ്പെടൽ/കോൺസുലാർ\" പേജ് പരിശോധിക്കുക.",
                  "ഒന്നും യോജിക്കുന്നില്ലെങ്കിൽ, വ്യക്തമായ നമ്പർ ഇല്ലാത്ത എന്തിനും MADAD (താഴെ എംബസി & കോൺസുലാർ സഹായം കാണുക) ആണ് ബദൽ."]},
    docs={"en": [], "hi": [], "ta": [], "te": [], "ml": []},
    note={"en": "Save the number for your specific mission once you find it — during a crisis, mission-specific lines get through faster than the general Delhi ones.",
          "hi": "अपने विशिष्ट मिशन का नंबर मिलते ही सहेज लें — संकट के दौरान, मिशन-विशिष्ट लाइनें सामान्य दिल्ली लाइनों से तेज़ी से लगती हैं।",
          "ta": "உங்கள் குறிப்பிட்ட தூதரகத்தின் எண்ணைக் கண்டதும் சேமிக்கவும் — நெருக்கடியின் போது, தூதரக-குறிப்பிட்ட எண்கள் பொதுவான டெல்லி எண்களை விட வேகமாக இணைக்கும்.",
          "te": "మీ నిర్దిష్ట మిషన్ నంబర్‌ను కనుగొన్న వెంటనే సేవ్ చేసుకోండి — సంక్షోభ సమయంలో, మిషన్-నిర్దిష్ట లైన్లు సాధారణ ఢిల్లీ లైన్ల కంటే వేగంగా అందుతాయి.",
          "ml": "നിങ്ങളുടെ പ്രത്യേക മിഷന്റെ നമ്പർ കണ്ടെത്തിക്കഴിഞ്ഞാൽ സേവ് ചെയ്യുക — പ്രതിസന്ധി സമയത്ത്, മിഷൻ-നിർദ്ദിഷ്ട ലൈനുകൾ പൊതുവായ ഡൽഹി ലൈനുകളേക്കാൾ വേഗത്തിൽ ബന്ധപ്പെടാം."},
    location={"en": "Online directory (MEA) + your mission's contact page", "hi": "ऑनलाइन निर्देशिका (MEA) + आपके मिशन का संपर्क पृष्ठ",
               "ta": "ஆன்லைன் அடைவு (MEA) + உங்கள் தூதரகத்தின் தொடர்பு பக்கம்", "te": "ఆన్‌లైన్ డైరెక్టరీ (MEA) + మీ మిషన్ సంప్రదింపు పేజీ",
               "ml": "ഓൺലൈൻ ഡയറക്ടറി (MEA) + നിങ്ങളുടെ മിഷന്റെ ബന്ധപ്പെടൽ പേജ്"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/contact-tele-inquiry", "label": {"en": "↗ Tele-inquiry directory — mea.gov.in", "hi": "↗ टेली-इंक्वायरी निर्देशिका — mea.gov.in",
                                                                               "ta": "↗ டெலி-விசாரணை அடைவு — mea.gov.in", "te": "↗ టెలి-ఎంక్వైరీ డైరెక్టరీ — mea.gov.in", "ml": "↗ ടെലി-അന്വേഷണ ഡയറക്ടറി — mea.gov.in"}}],
)

# ---- Passport ----

entry(
    category="passport", badge_official=True,
    search_en="passport renewal reissue fresh apply",
    title={"en": "Passport renewal & reissue", "hi": "पासपोर्ट नवीनीकरण और पुनः जारी", "ta": "பாஸ்போர்ட் புதுப்பித்தல் & மறு வழங்கல்",
           "te": "పాస్‌పోర్ట్ రెన్యువల్ & రీఇష్యూ", "ml": "പാസ്‌പോർട്ട് പുതുക്കൽ, വീണ്ടും നൽകൽ"},
    desc={"en": "Renew an expiring passport, replace a full booklet, or update details (address, name, appearance) while living outside India. Applications for those abroad are filed through the Passport Seva system at your nearest Indian Mission, or an outsourced centre (VFS/BLS) where the mission uses one.",
          "hi": "विदेश में रहते हुए समाप्त होते पासपोर्ट का नवीनीकरण करें, पूरी हो चुकी बुकलेट बदलें, या विवरण (पता, नाम, रूप) अपडेट करें। विदेश में रहने वालों के आवेदन नज़दीकी भारतीय मिशन पर Passport Seva प्रणाली के ज़रिए, या जहाँ मिशन इस्तेमाल करता हो वहाँ आउटसोर्स केंद्र (VFS/BLS) के ज़रिए दाख़िल होते हैं।",
          "ta": "இந்தியாவிற்கு வெளியே வாழும்போது காலாவதியாகும் பாஸ்போர்ட்டைப் புதுப்பிக்கவும், முழுமையாக நிரப்பப்பட்ட புத்தகத்தை மாற்றவும், அல்லது விவரங்களை (முகவரி, பெயர், தோற்றம்) புதுப்பிக்கவும். வெளிநாட்டில் உள்ளவர்களுக்கான விண்ணப்பங்கள் அருகிலுள்ள இந்திய தூதரகத்தில் Passport Seva முறை மூலம், அல்லது தூதரகம் பயன்படுத்தும் இடத்தில் அவுட்சோர்ஸ் மையம் (VFS/BLS) மூலம் தாக்கல் செய்யப்படுகின்றன.",
          "te": "భారత్ వెలుపల నివసిస్తూ గడువు ముగుస్తున్న పాస్‌పోర్ట్‌ను రెన్యూ చేసుకోండి, పూర్తయిన బుక్‌లెట్‌ను మార్చుకోండి, లేదా వివరాలను (చిరునామా, పేరు, రూపం) అప్‌డేట్ చేయండి. విదేశాల్లో ఉన్నవారి దరఖాస్తులు సమీప భారత మిషన్‌లో Passport Seva వ్యవస్థ ద్వారా, లేదా మిషన్ ఉపయోగించే చోట అవుట్‌సోర్స్ కేంద్రం (VFS/BLS) ద్వారా దాఖలు చేయబడతాయి.",
          "ml": "ഇന്ത്യക്ക് പുറത്ത് താമസിക്കുമ്പോൾ കാലഹരണപ്പെടുന്ന പാസ്‌പോർട്ട് പുതുക്കുകയോ, പൂർണ്ണമായ ബുക്ക്‌ലെറ്റ് മാറ്റുകയോ, വിവരങ്ങൾ (വിലാസം, പേര്, രൂപം) പുതുക്കുകയോ ചെയ്യുക. വിദേശത്തുള്ളവരുടെ അപേക്ഷകൾ അടുത്തുള്ള ഇന്ത്യൻ മിഷനിൽ Passport Seva സംവിധാനത്തിലൂടെയോ, മിഷൻ ഉപയോഗിക്കുന്നിടത്ത് ഔട്ട്‌സോഴ്‌സ് കേന്ദ്രത്തിലൂടെയോ (VFS/BLS) സമർപ്പിക്കുന്നു."},
    handles={"en": "renewal · reissue · minors", "hi": "नवीनीकरण · पुनः जारी · नाबालिग", "ta": "புதுப்பித்தல் · மறு வழங்கல் · சிறார்கள்",
             "te": "రెన్యువల్ · రీఇష్యూ · మైనర్లు", "ml": "പുതുക്കൽ · വീണ്ടും നൽകൽ · കുട്ടികൾ"},
    steps={"en": ["Register a new account on the Passport Seva portal for your mission — use a fresh email even if you've used the portal in India before.",
                  "Fill the reissue application online, upload your documents, and pay the fee.",
                  "Book an appointment — directly if your mission runs its own Passport Seva Kendra, or through the outsourced VFS/BLS centre it uses.",
                  "Attend in person with the printed application and original documents; photo and biometrics are captured there.",
                  "Track your Application Reference Number (ARN) online until the new passport is ready for collection or courier."],
           "hi": ["अपने मिशन के लिए Passport Seva पोर्टल पर नया खाता बनाएँ — भारत में पहले पोर्टल इस्तेमाल किया हो तब भी नया ईमेल इस्तेमाल करें।",
                  "ऑनलाइन पुनः जारी आवेदन भरें, दस्तावेज़ अपलोड करें, और शुल्क चुकाएँ।",
                  "अपॉइंटमेंट बुक करें — अगर मिशन अपना Passport Seva Kendra चलाता है तो सीधे, या इस्तेमाल किए जाने वाले आउटसोर्स VFS/BLS केंद्र के ज़रिए।",
                  "प्रिंट किए गए आवेदन और मूल दस्तावेज़ों के साथ व्यक्तिगत रूप से जाएँ; फ़ोटो और बायोमेट्रिक वहीं लिए जाते हैं।",
                  "जब तक नया पासपोर्ट संग्रह या कूरियर के लिए तैयार न हो, अपना Application Reference Number (ARN) ऑनलाइन ट्रैक करें।"],
           "ta": ["உங்கள் தூதரகத்திற்கான Passport Seva போர்ட்டலில் புதிய கணக்கைப் பதிவு செய்யவும் — இந்தியாவில் முன்பு போர்ட்டலைப் பயன்படுத்தியிருந்தாலும் புதிய மின்னஞ்சலைப் பயன்படுத்தவும்.",
                  "மறு வழங்கல் விண்ணப்பத்தை ஆன்லைனில் நிரப்பி, ஆவணங்களை பதிவேற்றி, கட்டணம் செலுத்தவும்.",
                  "அப்பாயிண்ட்மென்ட் பதிவு செய்யவும் — உங்கள் தூதரகம் அதன் சொந்த Passport Seva Kendra ஐ இயக்கினால் நேரடியாக, அல்லது அது பயன்படுத்தும் அவுட்சோர்ஸ் VFS/BLS மையம் மூலம்.",
                  "அச்சிடப்பட்ட விண்ணப்பம் மற்றும் அசல் ஆவணங்களுடன் நேரில் கலந்துகொள்ளுங்கள்; புகைப்படம் மற்றும் பயோமெட்ரிக் அங்கு எடுக்கப்படும்.",
                  "புதிய பாஸ்போர்ட் சேகரிப்பு அல்லது கூரியருக்கு தயாராகும் வரை உங்கள் Application Reference Number (ARN) ஐ ஆன்லைனில் கண்காணிக்கவும்."],
           "te": ["మీ మిషన్ కోసం Passport Seva పోర్టల్‌లో కొత్త ఖాతాను నమోదు చేసుకోండి — భారత్‌లో ఇంతకుముందు పోర్టల్ ఉపయోగించినా కొత్త ఇమెయిల్ వాడండి.",
                  "రీఇష్యూ దరఖాస్తును ఆన్‌లైన్‌లో పూరించి, పత్రాలను అప్‌లోడ్ చేసి, రుసుము చెల్లించండి.",
                  "అపాయింట్‌మెంట్ బుక్ చేసుకోండి — మీ మిషన్ దాని సొంత Passport Seva Kendra నడిపితే నేరుగా, లేదా అది ఉపయోగించే అవుట్‌సోర్స్ VFS/BLS కేంద్రం ద్వారా.",
                  "ప్రింట్ చేసిన దరఖాస్తు మరియు అసలు పత్రాలతో వ్యక్తిగతంగా హాజరు కండి; ఫోటో మరియు బయోమెట్రిక్ అక్కడే తీసుకుంటారు.",
                  "కొత్త పాస్‌పోర్ట్ సేకరణ లేదా కొరియర్‌కు సిద్ధమయ్యే వరకు మీ Application Reference Number (ARN) ను ఆన్‌లైన్‌లో ట్రాక్ చేయండి."],
           "ml": ["നിങ്ങളുടെ മിഷനുള്ള Passport Seva പോർട്ടലിൽ പുതിയ അക്കൗണ്ട് രജിസ്റ്റർ ചെയ്യുക — ഇന്ത്യയിൽ മുമ്പ് പോർട്ടൽ ഉപയോഗിച്ചിട്ടുണ്ടെങ്കിലും പുതിയ ഇമെയിൽ ഉപയോഗിക്കുക.",
                  "വീണ്ടും നൽകൽ അപേക്ഷ ഓൺലൈനിൽ പൂരിപ്പിച്ച്, രേഖകൾ അപ്‌ലോഡ് ചെയ്ത്, ഫീസ് അടയ്ക്കുക.",
                  "അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്യുക — നിങ്ങളുടെ മിഷൻ സ്വന്തം Passport Seva Kendra നടത്തുന്നുവെങ്കിൽ നേരിട്ട്, അല്ലെങ്കിൽ അത് ഉപയോഗിക്കുന്ന ഔട്ട്‌സോഴ്‌സ് VFS/BLS കേന്ദ്രം വഴി.",
                  "പ്രിന്റ് ചെയ്ത അപേക്ഷയും യഥാർത്ഥ രേഖകളുമായി നേരിട്ട് ഹാജരാകുക; ഫോട്ടോയും ബയോമെട്രിക്കും അവിടെ എടുക്കും.",
                  "പുതിയ പാസ്‌പോർട്ട് ശേഖരണത്തിനോ കൊറിയറിനോ തയ്യാറാകുന്നത് വരെ നിങ്ങളുടെ Application Reference Number (ARN) ഓൺലൈനിൽ ട്രാക്ക് ചെയ്യുക."]},
    docs={"en": ["Current or expired passport", "Passport-size photo to spec", "Proof of current overseas address (residence permit, utility bill, or visa)", "Self-attested copies of the old passport", "For minors: birth certificate and parental ID/consent"],
          "hi": ["वर्तमान या समाप्त पासपोर्ट", "निर्धारित माप का पासपोर्ट साइज़ फ़ोटो", "वर्तमान विदेशी पते का प्रमाण (निवास परमिट, यूटिलिटी बिल, या वीज़ा)", "पुराने पासपोर्ट की स्व-सत्यापित प्रतियाँ", "नाबालिगों के लिए: जन्म प्रमाणपत्र और माता-पिता का पहचान पत्र/सहमति"],
          "ta": ["தற்போதைய அல்லது காலாவதியான பாஸ்போர்ட்", "குறிப்பிட்ட அளவு பாஸ்போர்ட் அளவு புகைப்படம்", "தற்போதைய வெளிநாட்டு முகவரிக்கான ஆதாரம் (குடியிருப்பு அனுமதி, பயன்பாட்டு பில், அல்லது விசா)", "பழைய பாஸ்போர்ட்டின் சுய-சான்றளிக்கப்பட்ட நகல்கள்", "சிறார்களுக்கு: பிறப்புச் சான்றிதழ் மற்றும் பெற்றோர் அடையாள அட்டை/ஒப்புதல்"],
          "te": ["ప్రస్తుత లేదా గడువు ముగిసిన పాస్‌పోర్ట్", "నిర్దేశిత కొలతలలో పాస్‌పోర్ట్ సైజు ఫోటో", "ప్రస్తుత విదేశీ చిరునామాకు రుజువు (నివాస అనుమతి, యుటిలిటీ బిల్లు, లేదా వీసా)", "పాత పాస్‌పోర్ట్ యొక్క స్వీయ-ధృవీకరించిన కాపీలు", "మైనర్ల కోసం: జనన ధృవపత్రం మరియు తల్లిదండ్రుల గుర్తింపు/సమ్మతి"],
          "ml": ["നിലവിലെ അല്ലെങ്കിൽ കാലഹരണപ്പെട്ട പാസ്‌പോർട്ട്", "നിർദ്ദിഷ്ട അളവിലുള്ള പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ", "നിലവിലെ വിദേശ വിലാസത്തിന്റെ തെളിവ് (റെസിഡൻസ് പെർമിറ്റ്, യൂട്ടിലിറ്റി ബിൽ, അല്ലെങ്കിൽ വിസ)", "പഴയ പാസ്‌പോർട്ടിന്റെ സ്വയം സാക്ഷ്യപ്പെടുത്തിയ പകർപ്പുകൾ", "കുട്ടികൾക്ക്: ജനന സർട്ടിഫിക്കറ്റും മാതാപിതാക്കളുടെ ഐഡി/സമ്മതവും"]},
    note={"en": "Apply for reissue as soon as your passport has under a year of validity left — many countries refuse entry or visas on a passport nearing expiry.",
          "hi": "जैसे ही आपके पासपोर्ट की वैधता एक साल से कम रह जाए, पुनः जारी के लिए आवेदन करें — कई देश समाप्ति के क़रीब पासपोर्ट पर प्रवेश या वीज़ा देने से इनकार करते हैं।",
          "ta": "உங்கள் பாஸ்போர்ட்டின் செல்லுபடியாகும் காலம் ஒரு வருடத்திற்கும் குறைவாக இருக்கும்போதே மறு வழங்கலுக்கு விண்ணப்பிக்கவும் — காலாவதியாகும் தருவாயில் உள்ள பாஸ்போர்ட்டில் பல நாடுகள் நுழைவு அல்லது விசாவை மறுக்கின்றன.",
          "te": "మీ పాస్‌పోర్ట్ చెల్లుబాటు ఒక సంవత్సరం కంటే తక్కువ మిగిలి ఉన్నప్పుడే రీఇష్యూ కోసం దరఖాస్తు చేసుకోండి — గడువు ముగియబోతున్న పాస్‌పోర్ట్‌పై చాలా దేశాలు ప్రవేశం లేదా వీసాను తిరస్కరిస్తాయి.",
          "ml": "നിങ്ങളുടെ പാസ്‌പോർട്ടിന് ഒരു വർഷത്തിൽ താഴെ കാലാവധി ബാക്കിയുള്ളപ്പോൾ തന്നെ വീണ്ടും നൽകലിന് അപേക്ഷിക്കുക — കാലഹരണപ്പെടാറായ പാസ്‌പോർട്ടിൽ പല രാജ്യങ്ങളും പ്രവേശനമോ വിസയോ നിരസിക്കുന്നു."},
    location={"en": "Your nearest mission's Passport Seva Kendra, or its outsourced VFS/BLS centre",
               "hi": "आपके नज़दीकी मिशन का Passport Seva Kendra, या इसका आउटसोर्स VFS/BLS केंद्र",
               "ta": "உங்கள் அருகிலுள்ள தூதரகத்தின் Passport Seva Kendra, அல்லது அதன் அவுட்சோர்ஸ் VFS/BLS மையம்",
               "te": "మీ సమీప మిషన్ యొక్క Passport Seva Kendra, లేదా దాని అవుట్‌సోర్స్ VFS/BLS కేంద్రం",
               "ml": "നിങ്ങളുടെ അടുത്തുള്ള മിഷന്റെ Passport Seva Kendra, അല്ലെങ്കിൽ അതിന്റെ ഔട്ട്‌സോഴ്‌സ് VFS/BLS കേന്ദ്രം"},
    phone=None, email=None,
    links=[
        {"href": "https://www.passportindia.gov.in/psp/Apply", "label": {"en": "↗ Apply — Passport Seva (passportindia.gov.in)", "hi": "↗ आवेदन करें — Passport Seva",
                                                                            "ta": "↗ விண்ணப்பிக்க — Passport Seva", "te": "↗ దరఖాస్తు చేయండి — Passport Seva", "ml": "↗ അപേക്ഷിക്കുക — Passport Seva"}},
        {"href": "https://mportal.passportindia.gov.in/mission/", "label": {"en": "↗ Find your mission's passport centre", "hi": "↗ अपने मिशन का पासपोर्ट केंद्र खोजें",
                                                                              "ta": "↗ உங்கள் தூதரக பாஸ்போர்ட் மையத்தைக் கண்டறியவும்", "te": "↗ మీ మిషన్ పాస్‌పోర్ట్ కేంద్రాన్ని కనుగొనండి", "ml": "↗ നിങ്ങളുടെ മിഷന്റെ പാസ്‌പോർട്ട് കേന്ദ്രം കണ്ടെത്തുക"}},
        {"href": "https://portal2.passportindia.gov.in/AppOnlineProject/fee/feeInput", "label": {"en": "↗ Current fee calculator", "hi": "↗ मौजूदा शुल्क कैलकुलेटर",
                                                                                                    "ta": "↗ தற்போதைய கட்டண கால்குலேட்டர்", "te": "↗ ప్రస్తుత రుసుము కాలిక్యులేటర్", "ml": "↗ നിലവിലെ ഫീസ് കാൽക്കുലേറ്റർ"}},
    ],
)

entry(
    category="passport", badge_official=True,
    search_en="lost stolen damaged passport emergency certificate",
    title={"en": "Lost, stolen or damaged passport", "hi": "खोया, चोरी हुआ या क्षतिग्रस्त पासपोर्ट", "ta": "தொலைந்த, திருடப்பட்ட அல்லது சேதமான பாஸ்போர்ட்",
           "te": "పోగొట్టుకున్న, దొంగిలించబడిన లేదా పాడైన పాస్‌పోర్ట్", "ml": "നഷ്ടപ്പെട്ട, മോഷ്ടിക്കപ്പെട്ട അല്ലെങ്കിൽ കേടായ പാസ്‌പോർട്ട്"},
    desc={"en": "Report the loss to local police first, then apply to your nearest mission for a replacement or, if you need to travel home urgently and there's no time for a full reissue, an Emergency Certificate valid for a single trip to India.",
          "hi": "पहले स्थानीय पुलिस को नुक़सान की सूचना दें, फिर बदलाव के लिए अपने नज़दीकी मिशन में आवेदन करें, या अगर तुरंत घर लौटना है और पूर्ण पुनः जारी के लिए समय नहीं है, तो भारत की एक यात्रा के लिए मान्य Emergency Certificate के लिए।",
          "ta": "முதலில் உள்ளூர் காவல்துறையிடம் இழப்பைப் புகாரளிக்கவும், பின்னர் மாற்றீட்டிற்கு உங்கள் அருகிலுள்ள தூதரகத்தில் விண்ணப்பிக்கவும், அல்லது அவசரமாக வீட்டிற்குச் செல்ல வேண்டி முழு மறு வழங்கலுக்கு நேரமில்லை என்றால், இந்தியாவிற்கு ஒரே பயணத்திற்கு செல்லுபடியாகும் Emergency Certificate க்கு விண்ணப்பிக்கவும்.",
          "te": "మొదట స్థానిక పోలీసులకు నష్టం గురించి తెలియజేయండి, తర్వాత భర్తీ కోసం మీ సమీప మిషన్‌లో దరఖాస్తు చేసుకోండి, లేదా అత్యవసరంగా ఇంటికి వెళ్లాల్సి వచ్చి పూర్తి రీఇష్యూకి సమయం లేకపోతే, భారత్‌కు ఒక్క ప్రయాణానికి మాత్రమే చెల్లుబాటు అయ్యే Emergency Certificate కోసం.",
          "ml": "ആദ്യം പ്രാദേശിക പോലീസിൽ നഷ്ടം റിപ്പോർട്ട് ചെയ്യുക, പിന്നീട് പകരം ലഭിക്കാൻ നിങ്ങളുടെ അടുത്തുള്ള മിഷനിൽ അപേക്ഷിക്കുക, അല്ലെങ്കിൽ അടിയന്തിരമായി നാട്ടിലേക്ക് പോകേണ്ടിവരികയും പൂർണ്ണ പുനർവിതരണത്തിന് സമയമില്ലാതിരിക്കുകയും ചെയ്താൽ, ഇന്ത്യയിലേക്കുള്ള ഒറ്റ യാത്രയ്ക്ക് സാധുതയുള്ള Emergency Certificate."},
    handles={"en": "police report · reissue · emergency travel", "hi": "पुलिस रिपोर्ट · पुनः जारी · आपातकालीन यात्रा", "ta": "காவல் புகார் · மறு வழங்கல் · அவசர பயணம்",
             "te": "పోలీసు రిపోర్ట్ · రీఇష్యూ · అత్యవసర ప్రయాణం", "ml": "പോലീസ് റിപ്പോർട്ട് · വീണ്ടും നൽകൽ · അടിയന്തിര യാത്ര"},
    steps={"en": ["File a police report (FIR) with local police first — you'll need this for everything that follows.",
                  "Apply on the Passport Seva portal for a replacement, selecting \"lost/damaged\" as the reason.",
                  "If you need to travel urgently and there's no time for a full reissue, ask the mission about an Emergency Certificate instead.",
                  "Attend your appointment with the police report, an affidavit of loss, and any ID you still have."],
           "hi": ["पहले स्थानीय पुलिस के पास एक पुलिस रिपोर्ट (FIR) दर्ज कराएँ — आगे की हर चीज़ के लिए यह ज़रूरी होगा।",
                  "\"खोया/क्षतिग्रस्त\" कारण चुनते हुए Passport Seva पोर्टल पर बदलाव के लिए आवेदन करें।",
                  "अगर तुरंत यात्रा करनी है और पूर्ण पुनः जारी के लिए समय नहीं है, तो इसके बजाय मिशन से Emergency Certificate के बारे में पूछें।",
                  "पुलिस रिपोर्ट, हानि का शपथपत्र, और जो भी पहचान पत्र आपके पास हो, उसके साथ अपनी अपॉइंटमेंट में जाएँ।"],
           "ta": ["முதலில் உள்ளூர் காவல்துறையிடம் காவல் புகார் (FIR) பதிவு செய்யவும் — இதற்குப் பின் வரும் அனைத்திற்கும் இது தேவைப்படும்.",
                  "\"தொலைந்தது/சேதமானது\" என்பதை காரணமாக தேர்ந்தெடுத்து Passport Seva போர்ட்டலில் மாற்றீட்டிற்கு விண்ணப்பிக்கவும்.",
                  "அவசரமாக பயணிக்க வேண்டும் மற்றும் முழு மறு வழங்கலுக்கு நேரமில்லை என்றால், அதற்குப் பதிலாக Emergency Certificate பற்றி தூதரகத்திடம் கேளுங்கள்.",
                  "காவல் புகார், இழப்பு உறுதிமொழி, மற்றும் உங்களிடம் இன்னும் உள்ள எந்த அடையாள அட்டையுடனும் உங்கள் அப்பாயிண்ட்மென்ட்டில் கலந்துகொள்ளுங்கள்."],
           "te": ["మొదట స్థానిక పోలీసులతో పోలీసు రిపోర్ట్ (FIR) దాఖలు చేయండి — తర్వాత జరిగే ప్రతిదానికీ ఇది అవసరం.",
                  "\"పోగొట్టుకున్నది/పాడైనది\" అనే కారణాన్ని ఎంచుకుని Passport Seva పోర్టల్‌లో భర్తీ కోసం దరఖాస్తు చేసుకోండి.",
                  "అత్యవసరంగా ప్రయాణించాల్సి వచ్చి పూర్తి రీఇష్యూకి సమయం లేకపోతే, బదులుగా Emergency Certificate గురించి మిషన్‌ను అడగండి.",
                  "పోలీసు రిపోర్ట్, నష్టం అఫిడవిట్, మరియు మీ వద్ద ఉన్న ఏదైనా గుర్తింపుతో మీ అపాయింట్‌మెంట్‌కు హాజరు కండి."],
           "ml": ["ആദ്യം പ്രാദേശിക പോലീസിൽ ഒരു പോലീസ് റിപ്പോർട്ട് (FIR) ഫയൽ ചെയ്യുക — തുടർന്നുള്ള എല്ലാറ്റിനും ഇത് ആവശ്യമാണ്.",
                  "\"നഷ്ടപ്പെട്ടത്/കേടായത്\" കാരണമായി തിരഞ്ഞെടുത്ത് Passport Seva പോർട്ടലിൽ പകരമുള്ളതിന് അപേക്ഷിക്കുക.",
                  "അടിയന്തിരമായി യാത്ര ചെയ്യേണ്ടിവരികയും പൂർണ്ണ പുനർവിതരണത്തിന് സമയമില്ലാതിരിക്കുകയും ചെയ്താൽ, പകരം Emergency Certificate നെക്കുറിച്ച് മിഷനോട് ചോദിക്കുക.",
                  "പോലീസ് റിപ്പോർട്ട്, നഷ്ടത്തിന്റെ സത്യവാങ്മൂലം, നിങ്ങളുടെ പക്കലുള്ള ഏതെങ്കിലും ഐഡിയുമായി നിങ്ങളുടെ അപ്പോയിന്റ്മെന്റിൽ ഹാജരാകുക."]},
    docs={"en": ["Police report / FIR copy", "Affidavit of loss", "Photocopy of the lost passport, if you have one", "Passport photos and proof of address"],
          "hi": ["पुलिस रिपोर्ट / FIR की प्रति", "हानि का शपथपत्र", "खोए हुए पासपोर्ट की फ़ोटोकॉपी, अगर हो", "पासपोर्ट फ़ोटो और पते का प्रमाण"],
          "ta": ["காவல் புகார் / FIR நகல்", "இழப்பு உறுதிமொழி", "தொலைந்த பாஸ்போர்ட்டின் நகல், இருந்தால்", "பாஸ்போர்ட் புகைப்படங்கள் மற்றும் முகவரி ஆதாரம்"],
          "te": ["పోలీసు రిపోర్ట్ / FIR కాపీ", "నష్టం అఫిడవిట్", "పోయిన పాస్‌పోర్ట్ ఫోటోకాపీ, ఉంటే", "పాస్‌పోర్ట్ ఫోటోలు మరియు చిరునామా రుజువు"],
          "ml": ["പോലീസ് റിപ്പോർട്ട് / FIR പകർപ്പ്", "നഷ്ടത്തിന്റെ സത്യവാങ്മൂലം", "നഷ്ടപ്പെട്ട പാസ്‌പോർട്ടിന്റെ ഫോട്ടോകോപ്പി, ഉണ്ടെങ്കിൽ", "പാസ്‌പോർട്ട് ഫോട്ടോകളും വിലാസ തെളിവും"]},
    note={"en": "Tatkaal (fast-track) service usually isn't available for lost/damaged cases — budget extra time.",
          "hi": "खोए/क्षतिग्रस्त मामलों के लिए आमतौर पर तत्काल (फ़ास्ट-ट्रैक) सेवा उपलब्ध नहीं होती — अतिरिक्त समय का बजट रखें।",
          "ta": "தொலைந்த/சேதமான வழக்குகளுக்கு பொதுவாக தத்கால் (விரைவு) சேவை கிடைக்காது — கூடுதல் நேரத்தை திட்டமிடுங்கள்.",
          "te": "పోగొట్టుకున్న/పాడైన కేసులకు సాధారణంగా తత్కాల్ (ఫాస్ట్-ట్రాక్) సేవ అందుబాటులో ఉండదు — అదనపు సమయాన్ని బడ్జెట్ చేయండి.",
          "ml": "നഷ്ടപ്പെട്ട/കേടായ കേസുകൾക്ക് സാധാരണയായി തത്കാൽ (ഫാസ്റ്റ്-ട്രാക്ക്) സേവനം ലഭ്യമല്ല — അധിക സമയം കണക്കാക്കുക."},
    location={"en": "Local police station first, then your nearest Indian Mission",
               "hi": "पहले स्थानीय पुलिस स्टेशन, फिर आपका नज़दीकी भारतीय मिशन",
               "ta": "முதலில் உள்ளூர் காவல் நிலையம், பின்னர் உங்கள் அருகிலுள்ள இந்திய தூதரகம்",
               "te": "మొదట స్థానిక పోలీసు స్టేషన్, తర్వాత మీ సమీప భారత మిషన్",
               "ml": "ആദ്യം പ്രാദേശിക പോലീസ് സ്റ്റേഷൻ, പിന്നീട് നിങ്ങളുടെ അടുത്തുള്ള ഇന്ത്യൻ മിഷൻ"},
    phone=None, email=None,
    links=[
        {"href": "https://www.mea.gov.in", "label": {"en": "↗ Locate your mission's consular page", "hi": "↗ अपने मिशन का वाणिज्य दूत पृष्ठ खोजें",
                                                        "ta": "↗ உங்கள் தூதரக துணைத்தூதரக பக்கத்தைக் கண்டறியவும்", "te": "↗ మీ మిషన్ కాన్సులర్ పేజీని కనుగొనండి", "ml": "↗ നിങ്ങളുടെ മിഷന്റെ കോൺസുലാർ പേജ് കണ്ടെത്തുക"}},
        {"href": "https://www.passportindia.gov.in/psp/Apply", "label": {"en": "↗ File a lost/damaged passport application", "hi": "↗ खोया/क्षतिग्रस्त पासपोर्ट आवेदन दाख़िल करें",
                                                                            "ta": "↗ தொலைந்த/சேதமான பாஸ்போர்ட் விண்ணப்பத்தைத் தாக்கல் செய்யவும்", "te": "↗ పోయిన/పాడైన పాస్‌పోర్ట్ దరఖాస్తు దాఖలు చేయండి", "ml": "↗ നഷ്ടപ്പെട്ട/കേടായ പാസ്‌പോർട്ട് അപേക്ഷ സമർപ്പിക്കുക"}},
    ],
)

entry(
    category="passport", badge_official=True,
    search_en="police clearance certificate pcc foreign employment",
    title={"en": "Police Clearance Certificate (PCC)", "hi": "पुलिस क्लीयरेंस सर्टिफिकेट (PCC)", "ta": "காவல் அனுமதி சான்றிதழ் (PCC)",
           "te": "పోలీసు క్లియరెన్స్ సర్టిఫికేట్ (PCC)", "ml": "പോലീസ് ക്ലിയറൻസ് സർട്ടിഫിക്കറ്റ് (PCC)"},
    desc={"en": "Needed for foreign employment, long-term visas, permanent residency or citizenship applications abroad. Indians already living overseas apply through the Passport Seva portal or their mission's PCC service rather than through India's local police.",
          "hi": "विदेशी नौकरी, दीर्घकालिक वीज़ा, स्थायी निवास या विदेश में नागरिकता आवेदन के लिए ज़रूरी। पहले से विदेश में रह रहे भारतीय भारत की स्थानीय पुलिस के बजाय Passport Seva पोर्टल या अपने मिशन की PCC सेवा के ज़रिए आवेदन करते हैं।",
          "ta": "வெளிநாட்டு வேலைவாய்ப்பு, நீண்ட கால விசாக்கள், நிரந்தர குடியிருப்பு அல்லது வெளிநாட்டில் குடியுரிமை விண்ணப்பங்களுக்கு தேவை. ஏற்கனவே வெளிநாட்டில் வாழும் இந்தியர்கள் இந்தியாவின் உள்ளூர் காவல்துறை மூலம் அல்லாமல் Passport Seva போர்ட்டல் அல்லது தங்கள் தூதரகத்தின் PCC சேவை மூலம் விண்ணப்பிக்கிறார்கள்.",
          "te": "విదేశీ ఉద్యోగం, దీర్ఘకాలిక వీసాలు, శాశ్వత నివాసం లేదా విదేశాల్లో పౌరసత్వ దరఖాస్తులకు అవసరం. ఇప్పటికే విదేశాల్లో నివసిస్తున్న భారతీయులు భారత్‌లోని స్థానిక పోలీసుల ద్వారా కాకుండా Passport Seva పోర్టల్ లేదా వారి మిషన్ యొక్క PCC సేవ ద్వారా దరఖాస్తు చేసుకుంటారు.",
          "ml": "വിദേശ തൊഴിൽ, ദീർഘകാല വിസകൾ, സ്ഥിരതാമസം അല്ലെങ്കിൽ വിദേശത്ത് പൗരത്വ അപേക്ഷകൾക്ക് ആവശ്യമാണ്. ഇതിനകം വിദേശത്ത് താമസിക്കുന്ന ഇന്ത്യക്കാർ ഇന്ത്യയിലെ പ്രാദേശിക പോലീസ് വഴിയല്ല, Passport Seva പോർട്ടൽ അല്ലെങ്കിൽ അവരുടെ മിഷന്റെ PCC സേവനം വഴിയാണ് അപേക്ഷിക്കുന്നത്."},
    handles={"en": "PR/visa proof · employer verification", "hi": "PR/वीज़ा प्रमाण · नियोक्ता सत्यापन", "ta": "PR/விசா ஆதாரம் · முதலாளி சரிபார்ப்பு",
             "te": "PR/వీసా రుజువు · యజమాని ధృవీకరణ", "ml": "PR/വിസ തെളിവ് · തൊഴിലുടമ പരിശോധന"},
    steps={"en": ["Start on the Passport Seva portal for missions and choose your country/region.",
                  "Register and fill the PCC application with your passport and current address details.",
                  "Submit the form and documents to your mission — online upload or in person, depending on the mission.",
                  "The mission forwards it for background verification in India — this is usually the longest step.",
                  "Collect the certificate in person, or request postal delivery once it's ready."],
           "hi": ["मिशनों के लिए Passport Seva पोर्टल पर शुरू करें और अपना देश/क्षेत्र चुनें।",
                  "अपने पासपोर्ट और वर्तमान पते के विवरण के साथ PCC आवेदन पंजीकृत करें और भरें।",
                  "फ़ॉर्म और दस्तावेज़ अपने मिशन को जमा करें — मिशन के अनुसार ऑनलाइन अपलोड या व्यक्तिगत रूप से।",
                  "मिशन इसे भारत में पृष्ठभूमि सत्यापन के लिए आगे भेजता है — यह आमतौर पर सबसे लंबा चरण होता है।",
                  "प्रमाणपत्र तैयार होने पर व्यक्तिगत रूप से लें, या डाक द्वारा डिलीवरी का अनुरोध करें।"],
           "ta": ["தூதரகங்களுக்கான Passport Seva போர்ட்டலில் தொடங்கி உங்கள் நாடு/பகுதியைத் தேர்ந்தெடுக்கவும்.",
                  "உங்கள் பாஸ்போர்ட் மற்றும் தற்போதைய முகவரி விவரங்களுடன் PCC விண்ணப்பத்தை பதிவு செய்து நிரப்பவும்.",
                  "படிவம் மற்றும் ஆவணங்களை உங்கள் தூதரகத்திடம் சமர்ப்பிக்கவும் — தூதரகத்தைப் பொறுத்து ஆன்லைன் பதிவேற்றம் அல்லது நேரில்.",
                  "தூதரகம் இதை இந்தியாவில் பின்னணி சரிபார்ப்பிற்கு அனுப்புகிறது — இது பொதுவாக மிக நீண்ட படி.",
                  "தயாரானதும் சான்றிதழை நேரில் பெறவும், அல்லது தபால் விநியோகத்தைக் கோரவும்."],
           "te": ["మిషన్ల కోసం Passport Seva పోర్టల్‌లో ప్రారంభించి మీ దేశం/ప్రాంతాన్ని ఎంచుకోండి.",
                  "మీ పాస్‌పోర్ట్ మరియు ప్రస్తుత చిరునామా వివరాలతో PCC దరఖాస్తును నమోదు చేసి పూరించండి.",
                  "ఫారం మరియు పత్రాలను మీ మిషన్‌కు సమర్పించండి — మిషన్‌ను బట్టి ఆన్‌లైన్ అప్‌లోడ్ లేదా వ్యక్తిగతంగా.",
                  "మిషన్ దీన్ని భారత్‌లో నేపథ్య ధృవీకరణ కోసం పంపుతుంది — ఇది సాధారణంగా అత్యంత సుదీర్ఘమైన దశ.",
                  "సిద్ధమైన తర్వాత ధృవపత్రాన్ని వ్యక్తిగతంగా తీసుకోండి, లేదా పోస్టల్ డెలివరీని అభ్యర్థించండి."],
           "ml": ["മിഷനുകൾക്കുള്ള Passport Seva പോർട്ടലിൽ തുടങ്ങി നിങ്ങളുടെ രാജ്യം/പ്രദേശം തിരഞ്ഞെടുക്കുക.",
                  "നിങ്ങളുടെ പാസ്‌പോർട്ടും നിലവിലെ വിലാസ വിവരങ്ങളും ഉപയോഗിച്ച് PCC അപേക്ഷ രജിസ്റ്റർ ചെയ്ത് പൂരിപ്പിക്കുക.",
                  "ഫോമും രേഖകളും നിങ്ങളുടെ മിഷന് സമർപ്പിക്കുക — മിഷനെ ആശ്രയിച്ച് ഓൺലൈൻ അപ്‌ലോഡ് അല്ലെങ്കിൽ നേരിട്ട്.",
                  "മിഷൻ ഇത് ഇന്ത്യയിൽ പശ്ചാത്തല പരിശോധനയ്ക്കായി അയക്കുന്നു — ഇത് സാധാരണയായി ഏറ്റവും ദൈർഘ്യമേറിയ ഘട്ടമാണ്.",
                  "തയ്യാറായിക്കഴിഞ്ഞാൽ സർട്ടിഫിക്കറ്റ് നേരിട്ട് വാങ്ങുക, അല്ലെങ്കിൽ തപാൽ ഡെലിവറി അഭ്യർത്ഥിക്കുക."]},
    docs={"en": ["Self-attested copies of your passport (bio page, last two pages, ECR/observations page)", "Proof of current residency abroad", "Proof of purpose — job offer, visa application, or PR application"],
          "hi": ["आपके पासपोर्ट की स्व-सत्यापित प्रतियाँ (बायो पृष्ठ, अंतिम दो पृष्ठ, ECR/टिप्पणी पृष्ठ)", "विदेश में वर्तमान निवास का प्रमाण", "उद्देश्य का प्रमाण — नौकरी प्रस्ताव, वीज़ा आवेदन, या PR आवेदन"],
          "ta": ["உங்கள் பாஸ்போர்ட்டின் சுய-சான்றளிக்கப்பட்ட நகல்கள் (பயோ பக்கம், கடைசி இரண்டு பக்கங்கள், ECR/அவதானிப்பு பக்கம்)", "வெளிநாட்டில் தற்போதைய குடியிருப்பின் ஆதாரம்", "நோக்கத்திற்கான ஆதாரம் — வேலை வாய்ப்பு, விசா விண்ணப்பம், அல்லது PR விண்ணப்பம்"],
          "te": ["మీ పాస్‌పోర్ట్ యొక్క స్వీయ-ధృవీకరించిన కాపీలు (బయో పేజీ, చివరి రెండు పేజీలు, ECR/అబ్జర్వేషన్ పేజీ)", "విదేశంలో ప్రస్తుత నివాసానికి రుజువు", "ప్రయోజనానికి రుజువు — ఉద్యోగ ఆఫర్, వీసా దరఖాస్తు, లేదా PR దరఖాస్తు"],
          "ml": ["നിങ്ങളുടെ പാസ്‌പോർട്ടിന്റെ സ്വയം സാക്ഷ്യപ്പെടുത്തിയ പകർപ്പുകൾ (ബയോ പേജ്, അവസാന രണ്ട് പേജുകൾ, ECR/നിരീക്ഷണ പേജ്)", "വിദേശത്ത് നിലവിലെ താമസത്തിന്റെ തെളിവ്", "ഉദ്ദേശ്യത്തിന്റെ തെളിവ് — ജോലി ഓഫർ, വിസ അപേക്ഷ, അല്ലെങ്കിൽ PR അപേക്ഷ"]},
    note={"en": "Apply well ahead of when you actually need it — verification often takes several weeks, longer than most other services here.",
          "hi": "जब वास्तव में ज़रूरत हो उससे काफ़ी पहले आवेदन करें — सत्यापन में अक्सर कई हफ़्ते लगते हैं, यहाँ की अधिकांश अन्य सेवाओं से ज़्यादा।",
          "ta": "உண்மையில் தேவைப்படுவதற்கு நன்கு முன்னதாக விண்ணப்பிக்கவும் — சரிபார்ப்பு பெரும்பாலும் பல வாரங்கள் எடுக்கும், இங்குள்ள மற்ற பெரும்பாலான சேவைகளை விட நீளமானது.",
          "te": "నిజంగా అవసరమయ్యే దానికంటే చాలా ముందుగానే దరఖాస్తు చేసుకోండి — ధృవీకరణ తరచుగా చాలా వారాలు పడుతుంది, ఇక్కడ ఉన్న చాలా ఇతర సేవల కంటే ఎక్కువ.",
          "ml": "യഥാർത്ഥത്തിൽ ആവശ്യമുള്ളതിന് വളരെ മുമ്പേ അപേക്ഷിക്കുക — പരിശോധന പലപ്പോഴും ആഴ്ചകൾ എടുക്കും, ഇവിടെയുള്ള മറ്റ് മിക്ക സേവനങ്ങളേക്കാളും കൂടുതൽ."},
    location={"en": "Your nearest mission's PCC service / VFS-BLS centre", "hi": "आपके नज़दीकी मिशन की PCC सेवा / VFS-BLS केंद्र",
               "ta": "உங்கள் அருகிலுள்ள தூதரகத்தின் PCC சேவை / VFS-BLS மையம்", "te": "మీ సమీప మిషన్ యొక్క PCC సేవ / VFS-BLS కేంద్రం",
               "ml": "നിങ്ങളുടെ അടുത്തുള്ള മിഷന്റെ PCC സേവനം / VFS-BLS കേന്ദ്രം"},
    phone=None, email=None,
    links=[
        {"href": "https://www.passportindia.gov.in", "label": {"en": "↗ Passport Seva — PCC application", "hi": "↗ Passport Seva — PCC आवेदन",
                                                                  "ta": "↗ Passport Seva — PCC விண்ணப்பம்", "te": "↗ Passport Seva — PCC దరఖాస్తు", "ml": "↗ Passport Seva — PCC അപേക്ഷ"}},
        {"href": "https://www.cgisf.gov.in/page/pcc-police-clearance-certificate-foreign-nationals/", "label": {"en": "↗ Example mission PCC guidance (San Francisco)", "hi": "↗ मिशन PCC मार्गदर्शन उदाहरण (सैन फ़्रांसिस्को)",
                                                                                                                   "ta": "↗ மாதிரி தூதரக PCC வழிகாட்டுதல் (சான் பிரான்சிஸ்கோ)", "te": "↗ మిషన్ PCC మార్గదర్శకత్వం ఉదాహరణ (శాన్ ఫ్రాన్సిస్కో)", "ml": "↗ മിഷൻ PCC മാർഗ്ഗനിർദ്ദേശ ഉദാഹരണം (സാൻ ഫ്രാൻസിസ്കോ)"}},
    ],
)

# ---- OCI & citizenship ----

entry(
    category="citizenship", badge_official=True,
    search_en="oci card new application overseas citizen of india",
    title={"en": "New OCI card", "hi": "नया OCI कार्ड", "ta": "புதிய OCI அட்டை", "te": "కొత్త OCI కార్డు", "ml": "പുതിയ OCI കാർഡ്"},
    desc={"en": "The Overseas Citizen of India card gives a lifelong multiple-entry visa and most of the rights of an Indian citizen (short of voting and government jobs) to those of Indian origin who have taken foreign citizenship. Applied for entirely online.",
          "hi": "Overseas Citizen of India कार्ड, विदेशी नागरिकता ले चुके भारतीय मूल के लोगों को आजीवन बहु-प्रवेश वीज़ा और भारतीय नागरिक के अधिकांश अधिकार (मतदान और सरकारी नौकरी को छोड़कर) देता है। पूरी तरह ऑनलाइन आवेदन।",
          "ta": "Overseas Citizen of India அட்டை, வெளிநாட்டு குடியுரிமை பெற்ற இந்திய வம்சாவளியினருக்கு வாழ்நாள் பல-நுழைவு விசா மற்றும் இந்திய குடிமகனின் பெரும்பாலான உரிமைகளை (வாக்களித்தல் மற்றும் அரசு வேலைகளைத் தவிர) வழங்குகிறது. முழுவதும் ஆன்லைனில் விண்ணப்பிக்கப்படுகிறது.",
          "te": "Overseas Citizen of India కార్డు, విదేశీ పౌరసత్వం తీసుకున్న భారత సంతతి వారికి జీవితకాల బహుళ-ప్రవేశ వీసా మరియు భారత పౌరుడి చాలా హక్కులను (ఓటు మరియు ప్రభుత్వ ఉద్యోగాలు మినహా) ఇస్తుంది. పూర్తిగా ఆన్‌లైన్‌లో దరఖాస్తు చేసుకోవచ్చు.",
          "ml": "Overseas Citizen of India കാർഡ്, വിദേശ പൗരത്വം സ്വീകരിച്ച ഇന്ത്യൻ വംശജർക്ക് ആജീവനാന്ത മൾട്ടിപ്പിൾ-എൻട്രി വിസയും ഇന്ത്യൻ പൗരന്റെ മിക്ക അവകാശങ്ങളും (വോട്ടും സർക്കാർ ജോലിയും ഒഴികെ) നൽകുന്നു. പൂർണ്ണമായും ഓൺലൈനിൽ അപേക്ഷിക്കാം."},
    handles={"en": "eligibility · new application · document list", "hi": "पात्रता · नया आवेदन · दस्तावेज़ सूची", "ta": "தகுதி · புதிய விண்ணப்பம் · ஆவண பட்டியல்",
             "te": "అర్హత · కొత్త దరఖాస్తు · పత్రాల జాబితా", "ml": "യോഗ്യത · പുതിയ അപേക്ഷ · രേഖകളുടെ പട്ടിക"},
    steps={"en": ["Check eligibility — broadly, former Indian citizens, their children/grandchildren, or foreign spouses of Indian citizens/OCI holders married 2+ years.",
                  "Fill the application at ociservices.gov.in and upload documents plus a photo in the required format (square, plain background).",
                  "Submit the originals in person at your jurisdictional mission/FRRO — no printouts needed, they scan the originals.",
                  "Give biometrics (fingerprints and photo) at the mission — required for everyone except under-12s and over-70s.",
                  "Wait roughly 30 days from acknowledgement; the mission emails you about any missing documents.",
                  "Your OCI is issued as a digital e-OCI card — download it from ociservices.gov.in once approved; physical booklets are no longer issued by default for new applications (as of July 2026)."],
           "hi": ["पात्रता जाँचें — मोटे तौर पर, पूर्व भारतीय नागरिक, उनके बच्चे/पोते-पोतियाँ, या 2+ साल से विवाहित भारतीय नागरिकों/OCI धारकों के विदेशी जीवनसाथी।",
                  "ociservices.gov.in पर आवेदन भरें और निर्धारित प्रारूप (चौकोर, सादा पृष्ठभूमि) में दस्तावेज़ और फ़ोटो अपलोड करें।",
                  "अपने क्षेत्राधिकार मिशन/FRRO पर व्यक्तिगत रूप से मूल दस्तावेज़ जमा करें — प्रिंटआउट की ज़रूरत नहीं, वे मूल स्कैन करते हैं।",
                  "मिशन पर बायोमेट्रिक (उंगलियों के निशान और फ़ोटो) दें — 12 वर्ष से कम और 70 वर्ष से अधिक को छोड़कर सभी के लिए अनिवार्य।",
                  "स्वीकृति से लगभग 30 दिन प्रतीक्षा करें; किसी छूटे दस्तावेज़ के बारे में मिशन ईमेल करता है।",
                  "आपका OCI एक डिजिटल e-OCI कार्ड के रूप में जारी होता है — मंज़ूरी मिलने के बाद इसे ociservices.gov.in से डाउनलोड करें; जुलाई 2026 से नए आवेदनों के लिए डिफ़ॉल्ट रूप से भौतिक बुकलेट जारी नहीं की जाती।"],
           "ta": ["தகுதியை சரிபார்க்கவும் — பரவலாக, முன்னாள் இந்திய குடிமக்கள், அவர்களது குழந்தைகள்/பேரக்குழந்தைகள், அல்லது 2+ ஆண்டுகள் திருமணமான இந்திய குடிமக்கள்/OCI வைத்திருப்பவர்களின் வெளிநாட்டு வாழ்க்கைத் துணைவர்.",
                  "ociservices.gov.in இல் விண்ணப்பத்தை நிரப்பி தேவையான வடிவத்தில் (சதுரம், வெற்று பின்னணி) ஆவணங்கள் மற்றும் புகைப்படத்தை பதிவேற்றவும்.",
                  "உங்கள் அதிகார வரம்பு தூதரகம்/FRRO இல் நேரில் மூலப்பிரதிகளை சமர்ப்பிக்கவும் — பிரிண்ட்அவுட் தேவையில்லை, அவர்கள் மூலப்பிரதிகளை ஸ்கேன் செய்கிறார்கள்.",
                  "தூதரகத்தில் பயோமெட்ரிக் (கைரேகைகள் மற்றும் புகைப்படம்) கொடுங்கள் — 12 வயதுக்குட்பட்டோர் மற்றும் 70 வயதுக்கு மேற்பட்டோர் தவிர அனைவருக்கும் தேவை.",
                  "ஒப்புதலிலிருந்து சுமார் 30 நாட்கள் காத்திருக்கவும்; விட்டுப்போன ஆவணங்கள் இருந்தால் தூதரகம் மின்னஞ்சல் அனுப்பும்.",
                  "உங்கள் OCI ஒரு டிஜிட்டல் e-OCI அட்டையாக வழங்கப்படுகிறது — ஒப்புதல் கிடைத்தவுடன் அதை ociservices.gov.in இலிருந்து பதிவிறக்கம் செய்யவும்; ஜூலை 2026 முதல் புதிய விண்ணப்பங்களுக்கு இயல்பாக இயற்பியல் புத்தகங்கள் வழங்கப்படுவதில்லை."],
           "te": ["అర్హతను తనిఖీ చేయండి — విస్తృతంగా, మాజీ భారత పౌరులు, వారి పిల్లలు/మనవలు, లేదా 2+ సంవత్సరాలు వివాహం చేసుకున్న భారత పౌరులు/OCI హోల్డర్ల విదేశీ జీవిత భాగస్వాములు.",
                  "ociservices.gov.in లో దరఖాస్తును పూరించి అవసరమైన ఫార్మాట్‌లో (చతురస్రం, ప్లెయిన్ బ్యాక్‌గ్రౌండ్) పత్రాలు మరియు ఫోటోను అప్‌లోడ్ చేయండి.",
                  "మీ అధికార పరిధి మిషన్/FRRO వద్ద వ్యక్తిగతంగా అసలు పత్రాలను సమర్పించండి — ప్రింటవుట్లు అవసరం లేదు, వారు అసలువాటిని స్కాన్ చేస్తారు.",
                  "మిషన్ వద్ద బయోమెట్రిక్స్ (వేలిముద్రలు మరియు ఫోటో) ఇవ్వండి — 12 ఏళ్లలోపు మరియు 70 ఏళ్లు పైబడిన వారు మినహా అందరికీ అవసరం.",
                  "ఆమోదం నుండి సుమారు 30 రోజులు వేచి ఉండండి; ఏదైనా పత్రాలు లేకపోతే మిషన్ మీకు ఇమెయిల్ చేస్తుంది.",
                  "మీ OCI డిజిటల్ e-OCI కార్డుగా జారీ చేయబడుతుంది — ఆమోదం పొందిన తర్వాత దాన్ని ociservices.gov.in నుండి డౌన్‌లోడ్ చేసుకోండి; జూలై 2026 నుండి కొత్త దరఖాస్తులకు డిఫాల్ట్‌గా భౌతిక బుక్‌లెట్‌లు జారీ చేయబడవు."],
           "ml": ["യോഗ്യത പരിശോധിക്കുക — വിശാലമായി, മുൻ ഇന്ത്യൻ പൗരന്മാർ, അവരുടെ കുട്ടികൾ/കൊച്ചുമക്കൾ, അല്ലെങ്കിൽ 2+ വർഷം വിവാഹിതരായ ഇന്ത്യൻ പൗരന്മാരുടെ/OCI ഉടമകളുടെ വിദേശ ജീവിതപങ്കാളികൾ.",
                  "ociservices.gov.in ൽ അപേക്ഷ പൂരിപ്പിച്ച് ആവശ്യമായ ഫോർമാറ്റിൽ (ചതുരം, പ്ലെയിൻ ബാക്ക്ഗ്രൗണ്ട്) രേഖകളും ഫോട്ടോയും അപ്‌ലോഡ് ചെയ്യുക.",
                  "നിങ്ങളുടെ അധികാരപരിധിയിലുള്ള മിഷൻ/FRRO ൽ നേരിട്ട് ഒറിജിനലുകൾ സമർപ്പിക്കുക — പ്രിന്റൗട്ട് വേണ്ട, അവർ ഒറിജിനലുകൾ സ്കാൻ ചെയ്യും.",
                  "മിഷനിൽ ബയോമെട്രിക്സ് (വിരലടയാളവും ഫോട്ടോയും) നൽകുക — 12 വയസ്സിന് താഴെയും 70 വയസ്സിന് മുകളിലും ഉള്ളവർ ഒഴികെ എല്ലാവർക്കും ആവശ്യമാണ്.",
                  "അംഗീകാരം ലഭിച്ച് ഏകദേശം 30 ദിവസം കാത്തിരിക്കുക; വിട്ടുപോയ രേഖകളെക്കുറിച്ച് മിഷൻ ഇമെയിൽ ചെയ്യും.",
                  "നിങ്ങളുടെ OCI ഒരു ഡിജിറ്റൽ e-OCI കാർഡായി നൽകപ്പെടുന്നു — അംഗീകാരം ലഭിച്ചാൽ ociservices.gov.in ൽ നിന്ന് അത് ഡൗൺലോഡ് ചെയ്യുക; 2026 ജൂലൈ മുതൽ പുതിയ അപേക്ഷകൾക്ക് സ്ഥിരസ്ഥിതിയായി ഫിസിക്കൽ ബുക്‌ലെറ്റുകൾ നൽകുന്നില്ല."]},
    docs={"en": ["Valid passport (6+ months validity) and naturalisation certificate", "Proof of Indian origin (old Indian passport, or parents'/grandparents' documents)", "Proof of current address", "Photograph to spec (square, min. 51×51mm, plain background)"],
          "hi": ["वैध पासपोर्ट (6+ माह की वैधता) और नागरिकता प्रमाणपत्र", "भारतीय मूल का प्रमाण (पुराना भारतीय पासपोर्ट, या माता-पिता/दादा-दादी के दस्तावेज़)", "वर्तमान पते का प्रमाण", "निर्धारित माप की फ़ोटो (चौकोर, न्यूनतम 51×51mm, सादा पृष्ठभूमि)"],
          "ta": ["செல்லுபடியாகும் பாஸ்போர்ட் (6+ மாத செல்லுபடி) மற்றும் குடியுரிமை சான்றிதழ்", "இந்திய வம்சாவளிக்கான ஆதாரம் (பழைய இந்திய பாஸ்போர்ட், அல்லது பெற்றோர்/பாட்டி-தாத்தா ஆவணங்கள்)", "தற்போதைய முகவரி ஆதாரம்", "குறிப்பிட்ட அளவு புகைப்படம் (சதுரம், குறைந்தது 51×51mm, வெற்று பின்னணி)"],
          "te": ["చెల్లుబాటు అయ్యే పాస్‌పోర్ట్ (6+ నెలల చెల్లుబాటు) మరియు నేచురలైజేషన్ సర్టిఫికేట్", "భారత మూలానికి రుజువు (పాత భారత పాస్‌పోర్ట్, లేదా తల్లిదండ్రుల/తాతల పత్రాలు)", "ప్రస్తుత చిరునామా రుజువు", "నిర్దేశిత ఫోటో (చతురస్రం, కనీసం 51×51mm, ప్లెయిన్ బ్యాక్‌గ్రౌండ్)"],
          "ml": ["സാധുവായ പാസ്‌പോർട്ട് (6+ മാസ സാധുത) നാച്വറലൈസേഷൻ സർട്ടിഫിക്കറ്റും", "ഇന്ത്യൻ വംശജത്വത്തിന്റെ തെളിവ് (പഴയ ഇന്ത്യൻ പാസ്‌പോർട്ട്, അല്ലെങ്കിൽ മാതാപിതാക്കളുടെ/മുത്തശ്ശിമുത്തശ്ശന്മാരുടെ രേഖകൾ)", "നിലവിലെ വിലാസത്തിന്റെ തെളിവ്", "നിർദ്ദിഷ്ട ഫോട്ടോ (ചതുരം, കുറഞ്ഞത് 51×51mm, പ്ലെയിൻ ബാക്ക്ഗ്രൗണ്ട്)"]},
    note={"en": "People with Pakistani or Bangladeshi ancestry are not eligible for OCI, regardless of other qualifying criteria.",
          "hi": "पाकिस्तानी या बांग्लादेशी वंश वाले लोग, अन्य योग्यता मानदंडों के बावजूद, OCI के लिए पात्र नहीं हैं।",
          "ta": "பாகிஸ்தான் அல்லது வங்காளதேச மூதாதையர் கொண்டவர்கள், மற்ற தகுதி அளவுகோல்கள் இருந்தாலும், OCI க்கு தகுதியற்றவர்கள்.",
          "te": "పాకిస్తానీ లేదా బంగ్లాదేశీ మూలాలు ఉన్నవారు, ఇతర అర్హత ప్రమాణాలు ఉన్నప్పటికీ, OCI కి అర్హులు కారు.",
          "ml": "പാകിസ്ഥാൻ അല്ലെങ്കിൽ ബംഗ്ലാദേശ് വംശജരായവർക്ക്, മറ്റ് യോഗ്യതാ മാനദണ്ഡങ്ങൾ ഉണ്ടെങ്കിലും, OCI ന് അർഹതയില്ല."},
    location={"en": "Your jurisdictional Indian Mission / FRRO", "hi": "आपका क्षेत्राधिकार भारतीय मिशन / FRRO",
               "ta": "உங்கள் அதிகார வரம்பு இந்திய தூதரகம் / FRRO", "te": "మీ అధికార పరిధి భారత మిషన్ / FRRO",
               "ml": "നിങ്ങളുടെ അധികാരപരിധിയിലുള്ള ഇന്ത്യൻ മിഷൻ / FRRO"},
    phone=None, email=None,
    links=[
        {"href": "https://ociservices.gov.in", "label": {"en": "↗ Apply — ociservices.gov.in", "hi": "↗ आवेदन करें — ociservices.gov.in",
                                                            "ta": "↗ விண்ணப்பிக்க — ociservices.gov.in", "te": "↗ దరఖాస్తు చేయండి — ociservices.gov.in", "ml": "↗ അപേക്ഷിക്കുക — ociservices.gov.in"}},
        {"href": "https://ociservices.gov.in/onlineOCI/faq", "label": {"en": "↗ OCI eligibility FAQ", "hi": "↗ OCI पात्रता FAQ",
                                                                         "ta": "↗ OCI தகுதி கேள்விகள்", "te": "↗ OCI అర్హత FAQ", "ml": "↗ OCI യോഗ്യത FAQ"}},
    ],
)

entry(
    category="citizenship", badge_official=True,
    search_en="oci renewal reissue mandatory update age 20 50",
    title={"en": "OCI renewal / reissue", "hi": "OCI नवीनीकरण / पुनः जारी", "ta": "OCI புதுப்பித்தல் / மறு வழங்கல்", "te": "OCI రెన్యువల్ / రీఇష్యూ", "ml": "OCI പുതുക്കൽ / വീണ്ടും നൽകൽ"},
    desc={"en": "An OCI card must be updated alongside a new passport if you were under 20 when it was first issued, and once more after you turn 50 — it isn't automatic. Since the July 2026 e-OCI rollout this update is done online at ociservices.gov.in rather than by submitting the physical booklet at a mission. Miscellaneous services also cover a lost card, spelling corrections and a new-passport update.",
          "hi": "अगर पहली बार जारी होने पर आपकी उम्र 20 वर्ष से कम थी, तो नए पासपोर्ट के साथ OCI कार्ड अपडेट कराना ज़रूरी है, और 50 वर्ष की उम्र के बाद एक बार फिर — यह अपने आप नहीं होता। जुलाई 2026 में ई-OCI शुरू होने के बाद से यह अपडेट भौतिक बुकलेट मिशन में जमा करने के बजाय ociservices.gov.in पर ऑनलाइन किया जाता है। विविध सेवाओं में खोया कार्ड, वर्तनी सुधार और नए पासपोर्ट अपडेट भी शामिल हैं।",
          "ta": "முதன்முதலில் வழங்கப்பட்டபோது உங்களுக்கு 20 வயதுக்கு குறைவாக இருந்தால், புதிய பாஸ்போர்ட்டுடன் OCI அட்டையை புதுப்பிக்க வேண்டும், 50 வயதுக்குப் பிறகு மீண்டும் ஒருமுறை — இது தானாக நடக்காது. ஜூலை 2026 இல் தொடங்கிய இ-OCI முறையின் பின், இந்த புதுப்பிப்பு தூதரகத்தில் இயற்பியல் புத்தகத்தை சமர்ப்பிப்பதற்குப் பதிலாக ociservices.gov.in இல் ஆன்லைனில் செய்யப்படுகிறது. இதர சேவைகளில் தொலைந்த அட்டை, எழுத்துப்பிழை திருத்தங்கள் மற்றும் புதிய பாஸ்போர்ட் புதுப்பிப்பும் அடங்கும்.",
          "te": "మొదటిసారి జారీ చేసినప్పుడు మీకు 20 ఏళ్లలోపు వయస్సు ఉంటే, కొత్త పాస్‌పోర్ట్‌తో పాటు OCI కార్డును అప్‌డేట్ చేయాలి, 50 ఏళ్లు దాటిన తర్వాత మరోసారి — ఇది ఆటోమేటిక్ కాదు. జూలై 2026లో ప్రారంభమైన ఇ-OCI విధానం నుండి, ఈ అప్‌డేట్ మిషన్‌లో భౌతిక బుక్‌లెట్ సమర్పించే బదులు ociservices.gov.in లో ఆన్‌లైన్‌లో చేయబడుతుంది. ఇతర సేవలలో పోగొట్టుకున్న కార్డు, స్పెల్లింగ్ దిద్దుబాట్లు మరియు కొత్త పాస్‌పోర్ట్ అప్‌డేట్ కూడా ఉన్నాయి.",
          "ml": "ആദ്യമായി നൽകിയപ്പോൾ നിങ്ങൾക്ക് 20 വയസ്സിന് താഴെയായിരുന്നെങ്കിൽ, പുതിയ പാസ്‌പോർട്ടിനൊപ്പം OCI കാർഡ് അപ്‌ഡേറ്റ് ചെയ്യണം, 50 വയസ്സിന് ശേഷം ഒരിക്കൽ കൂടി — ഇത് സ്വയമേവ നടക്കില്ല. 2026 ജൂലൈയിൽ ആരംഭിച്ച ഇ-OCI സംവിധാനത്തിന് ശേഷം, ഈ അപ്‌ഡേറ്റ് മിഷനിൽ ഫിസിക്കൽ ബുക്ക്‌ലെറ്റ് സമർപ്പിക്കുന്നതിന് പകരം ociservices.gov.in ൽ ഓൺലൈനായി ചെയ്യുന്നു. മറ്റ് സേവനങ്ങളിൽ നഷ്ടപ്പെട്ട കാർഡ്, അക്ഷരത്തെറ്റ് തിരുത്തലുകൾ, പുതിയ പാസ്‌പോർട്ട് അപ്‌ഡേറ്റ് എന്നിവയും ഉൾപ്പെടുന്നു."},
    handles={"en": "mandatory milestones · lost card · corrections", "hi": "अनिवार्य पड़ाव · खोया कार्ड · सुधार", "ta": "கட்டாய கட்டங்கள் · தொலைந்த அட்டை · திருத்தங்கள்",
             "te": "తప్పనిసరి మైలురాళ్లు · పోగొట్టుకున్న కార్డు · దిద్దుబాట్లు", "ml": "നിർബന്ധിത നാഴികക്കല്ലുകൾ · നഷ്ടപ്പെട്ട കാർഡ് · തിരുത്തലുകൾ"},
    steps={"en": ["Check whether you've hit a mandatory milestone — a new passport issued before age 20, or turning 50 — either one triggers a required OCI update.",
                  "Log in to ociservices.gov.in and select the miscellaneous services / passport update option.",
                  "Upload your new passport details and any changed information.",
                  "Submit online — since the July 2026 e-OCI rollout this is a digital update, not a physical-booklet mission submission; your updated e-OCI is issued once approved."],
           "hi": ["जाँचें कि क्या आप किसी अनिवार्य पड़ाव पर पहुँचे हैं — 20 वर्ष से पहले जारी नया पासपोर्ट, या 50 वर्ष का होना — दोनों में से कोई भी OCI अपडेट को अनिवार्य बनाता है।",
                  "ociservices.gov.in पर लॉग इन करें और विविध सेवाएँ / पासपोर्ट अपडेट विकल्प चुनें।",
                  "अपने नए पासपोर्ट का विवरण और कोई भी बदली जानकारी अपलोड करें।",
                  "ऑनलाइन सबमिट करें — जुलाई 2026 में ई-OCI शुरू होने के बाद से यह एक डिजिटल अपडेट है, न कि मिशन में भौतिक बुकलेट जमा करना; अनुमोदन के बाद आपका अपडेटेड ई-OCI जारी किया जाता है।"],
           "ta": ["நீங்கள் ஒரு கட்டாய கட்டத்தை அடைந்துள்ளீர்களா என்பதைச் சரிபார்க்கவும் — 20 வயதுக்கு முன் வழங்கப்பட்ட புதிய பாஸ்போர்ட், அல்லது 50 வயதாவது — இவை இரண்டில் ஏதேனும் ஒன்று OCI அப்டேட்டை கட்டாயமாக்கும்.",
                  "ociservices.gov.in இல் உள்நுழைந்து இதர சேவைகள் / பாஸ்போர்ட் அப்டேட் விருப்பத்தைத் தேர்ந்தெடுக்கவும்.",
                  "உங்கள் புதிய பாஸ்போர்ட் விவரங்கள் மற்றும் ஏதேனும் மாறிய தகவலை பதிவேற்றவும்.",
                  "ஆன்லைனில் சமர்ப்பிக்கவும் — ஜூலை 2026 இல் தொடங்கிய இ-OCI முறையின் பின், இது ஒரு டிஜிட்டல் அப்டேட், தூதரகத்தில் இயற்பியல் புத்தகத்தை சமர்ப்பிப்பது அல்ல; அனுமதிக்கப்பட்டவுடன் உங்கள் புதுப்பிக்கப்பட்ட இ-OCI வழங்கப்படும்."],
           "te": ["మీరు తప్పనిసరి మైలురాయిని చేరుకున్నారో లేదో తనిఖీ చేయండి — 20 ఏళ్లలోపు జారీ చేసిన కొత్త పాస్‌పోర్ట్, లేదా 50 ఏళ్లు నిండటం — ఈ రెండింటిలో ఏదైనా OCI అప్‌డేట్‌ను తప్పనిసరి చేస్తుంది.",
                  "ociservices.gov.in లో లాగిన్ అయి ఇతర సేవలు / పాస్‌పోర్ట్ అప్‌డేట్ ఎంపికను ఎంచుకోండి.",
                  "మీ కొత్త పాస్‌పోర్ట్ వివరాలు మరియు మారిన ఏదైనా సమాచారాన్ని అప్‌లోడ్ చేయండి.",
                  "ఆన్‌లైన్‌లో సమర్పించండి — జూలై 2026లో ప్రారంభమైన ఇ-OCI విధానం నుండి ఇది డిజిటల్ అప్‌డేట్, మిషన్‌లో భౌతిక బుక్‌లెట్ సమర్పణ కాదు; ఆమోదం పొందిన తర్వాత మీ అప్‌డేట్ చేసిన ఇ-OCI జారీ చేయబడుతుంది."],
           "ml": ["നിങ്ങൾ ഒരു നിർബന്ധിത നാഴികക്കല്ല് എത്തിയോ എന്ന് പരിശോധിക്കുക — 20 വയസ്സിന് മുമ്പ് നൽകിയ പുതിയ പാസ്‌പോർട്ട്, അല്ലെങ്കിൽ 50 വയസ്സാകുന്നത് — ഇവയിലേതെങ്കിലും OCI അപ്‌ഡേറ്റ് നിർബന്ധമാക്കും.",
                  "ociservices.gov.in ൽ ലോഗിൻ ചെയ്ത് മറ്റ് സേവനങ്ങൾ / പാസ്‌പോർട്ട് അപ്‌ഡേറ്റ് ഓപ്ഷൻ തിരഞ്ഞെടുക്കുക.",
                  "നിങ്ങളുടെ പുതിയ പാസ്‌പോർട്ട് വിവരങ്ങളും മാറിയ ഏതെങ്കിലും വിവരവും അപ്‌ലോഡ് ചെയ്യുക.",
                  "ഓൺലൈനായി സമർപ്പിക്കുക — 2026 ജൂലൈയിൽ ആരംഭിച്ച ഇ-OCI സംവിധാനത്തിന് ശേഷം ഇത് ഒരു ഡിജിറ്റൽ അപ്‌ഡേറ്റ് ആണ്, മിഷനിൽ ഫിസിക്കൽ ബുക്ക്‌ലെറ്റ് സമർപ്പിക്കൽ അല്ല; അംഗീകാരം ലഭിച്ചാൽ നിങ്ങളുടെ അപ്‌ഡേറ്റ് ചെയ്ത ഇ-OCI നൽകും."]},
    docs={"en": ["Current OCI card (physical booklet or digital e-OCI)", "New passport and passport photo", "Proof of the triggering event (new passport bio page)"],
          "hi": ["वर्तमान OCI कार्ड (भौतिक बुकलेट या डिजिटल ई-OCI)", "नया पासपोर्ट और पासपोर्ट फ़ोटो", "ट्रिगर करने वाली घटना का प्रमाण (नए पासपोर्ट का बायो पृष्ठ)"],
          "ta": ["தற்போதைய OCI அட்டை (இயற்பியல் புத்தகம் அல்லது டிஜிட்டல் இ-OCI)", "புதிய பாஸ்போர்ட் மற்றும் பாஸ்போர்ட் புகைப்படம்", "தூண்டும் நிகழ்வின் ஆதாரம் (புதிய பாஸ்போர்ட் பயோ பக்கம்)"],
          "te": ["ప్రస్తుత OCI కార్డు (భౌతిక బుక్‌లెట్ లేదా డిజిటల్ ఇ-OCI)", "కొత్త పాస్‌పోర్ట్ మరియు పాస్‌పోర్ట్ ఫోటో", "ట్రిగ్గర్ చేసే సంఘటనకు రుజువు (కొత్త పాస్‌పోర్ట్ బయో పేజీ)"],
          "ml": ["നിലവിലെ OCI കാർഡ് (ഫിസിക്കൽ ബുക്ക്‌ലെറ്റ് അല്ലെങ്കിൽ ഡിജിറ്റൽ ഇ-OCI)", "പുതിയ പാസ്‌പോർട്ടും പാസ്‌പോർട്ട് ഫോട്ടോയും", "കാരണമായ സംഭവത്തിന്റെ തെളിവ് (പുതിയ പാസ്‌പോർട്ട് ബയോ പേജ്)"]},
    note={"en": "This isn't automatic — many people only find out they needed to do this when it causes a problem at Indian immigration.",
          "hi": "यह अपने आप नहीं होता — कई लोगों को यह तभी पता चलता है जब भारतीय आव्रजन पर इससे समस्या होती है।",
          "ta": "இது தானாக நடக்காது — பல பேருக்கு இது இந்திய குடிவரவில் பிரச்சினை ஏற்படும்போது மட்டுமே தெரியவரும்.",
          "te": "ఇది ఆటోమేటిక్ కాదు — చాలామందికి భారత ఇమిగ్రేషన్ వద్ద సమస్య వచ్చినప్పుడే ఇది చేయాల్సి ఉందని తెలుస్తుంది.",
          "ml": "ഇത് സ്വയമേവ നടക്കില്ല — ഇന്ത്യൻ ഇമിഗ്രേഷനിൽ ഒരു പ്രശ്നം ഉണ്ടാകുമ്പോൾ മാത്രമാണ് പലർക്കും ഇത് ചെയ്യേണ്ടതായിരുന്നു എന്ന് അറിയുന്നത്."},
    location={"en": "Your jurisdictional Indian Mission", "hi": "आपका क्षेत्राधिकार भारतीय मिशन", "ta": "உங்கள் அதிகார வரம்பு இந்திய தூதரகம்",
               "te": "మీ అధికార పరిధి భారత మిషన్", "ml": "നിങ്ങളുടെ അധികാരപരിധിയിലുള്ള ഇന്ത്യൻ മിഷൻ"},
    phone=None, email=None,
    links=[{"href": "https://ociservices.gov.in/onlineOCI/miscFAQs", "label": {"en": "↗ OCI miscellaneous services FAQ", "hi": "↗ OCI विविध सेवाएँ FAQ",
                                                                                 "ta": "↗ OCI இதர சேவைகள் FAQ", "te": "↗ OCI ఇతర సేవల FAQ", "ml": "↗ OCI മറ്റ് സേവനങ്ങൾ FAQ"}}],
)

entry(
    category="citizenship", badge_official=True,
    search_en="surrender indian passport renunciation certificate foreign citizenship",
    title={"en": "Surrender passport & renunciation certificate", "hi": "पासपोर्ट समर्पण और त्याग प्रमाणपत्र", "ta": "பாஸ்போர்ட் ஒப்படைப்பு & துறப்பு சான்றிதழ்",
           "te": "పాస్‌పోర్ట్ సరెండర్ & పరిత్యాగ ధృవపత్రం", "ml": "പാസ്‌പോർട്ട് സറണ്ടർ, ത്യാഗ സർട്ടിഫിക്കറ്റ്"},
    desc={"en": "Indian law requires surrendering your Indian passport once you take another country's citizenship. Doing this promptly at your mission — often alongside an OCI application in the same visit — avoids penalties if you're later found still holding it.",
          "hi": "किसी अन्य देश की नागरिकता लेते ही भारतीय क़ानून के अनुसार आपका भारतीय पासपोर्ट समर्पित करना ज़रूरी है। अपने मिशन पर तुरंत ऐसा करना — अक्सर उसी यात्रा में OCI आवेदन के साथ — बाद में इसे रखे पाए जाने पर दंड से बचाता है।",
          "ta": "மற்றொரு நாட்டின் குடியுரிமையை நீங்கள் எடுத்தவுடன், உங்கள் இந்திய பாஸ்போர்ட்டை ஒப்படைக்குமாறு இந்திய சட்டம் கோருகிறது. உங்கள் தூதரகத்தில் உடனடியாக இதைச் செய்வது — பெரும்பாலும் அதே வருகையில் OCI விண்ணப்பத்துடன் — நீங்கள் பின்னர் அதை வைத்திருப்பது கண்டறியப்பட்டால் அபராதங்களைத் தவிர்க்கிறது.",
          "te": "మీరు మరొక దేశ పౌరసత్వం తీసుకున్న తర్వాత మీ భారత పాస్‌పోర్ట్‌ను సరెండర్ చేయాలని భారత చట్టం కోరుతుంది. మీ మిషన్‌లో వెంటనే దీన్ని చేయడం — తరచుగా అదే సందర్శనలో OCI దరఖాస్తుతో పాటు — మీరు తర్వాత ఇంకా దాన్ని కలిగి ఉన్నట్లు కనుగొనబడితే జరిమానాలను నివారిస్తుంది.",
          "ml": "മറ്റൊരു രാജ്യത്തിന്റെ പൗരത്വം സ്വീകരിച്ച ഉടനെ നിങ്ങളുടെ ഇന്ത്യൻ പാസ്‌പോർട്ട് സറണ്ടർ ചെയ്യണമെന്ന് ഇന്ത്യൻ നിയമം ആവശ്യപ്പെടുന്നു. നിങ്ങളുടെ മിഷനിൽ ഉടനടി ഇത് ചെയ്യുന്നത് — പലപ്പോഴും അതേ സന്ദർശനത്തിൽ OCI അപേക്ഷയോടൊപ്പം — പിന്നീട് അത് കൈവശം വച്ചതായി കണ്ടെത്തിയാൽ പിഴകൾ ഒഴിവാക്കുന്നു."},
    handles={"en": "surrender · renunciation certificate", "hi": "समर्पण · त्याग प्रमाणपत्र", "ta": "ஒப்படைப்பு · துறப்பு சான்றிதழ்",
             "te": "సరెండర్ · పరిత్యాగ ధృవపత్రం", "ml": "സറണ്ടർ · ത്യാഗ സർട്ടിഫിക്കറ്റ്"},
    steps={"en": ["Fill the Surrender of Indian Passport Certificate form (or the \"without passport\" declaration plus a loss affidavit if you no longer have it).",
                  "Gather proof of your new foreign citizenship.",
                  "Submit to your mission, often via VFS/BLS, ideally in the same visit as an OCI application.",
                  "Wait roughly 1–3 weeks for processing; the passport is stamped \"cancelled due to acquiring foreign nationality.\""],
           "hi": ["Surrender of Indian Passport Certificate फ़ॉर्म भरें (या अगर अब पासपोर्ट नहीं है तो \"बिना पासपोर्ट\" घोषणा और हानि शपथपत्र)।",
                  "अपनी नई विदेशी नागरिकता का प्रमाण इकट्ठा करें।",
                  "अपने मिशन में जमा करें, अक्सर VFS/BLS के ज़रिए, आदर्श रूप से OCI आवेदन की उसी यात्रा में।",
                  "प्रोसेसिंग के लिए लगभग 1–3 सप्ताह प्रतीक्षा करें; पासपोर्ट पर \"विदेशी नागरिकता प्राप्त करने के कारण रद्द\" की मोहर लगती है।"],
           "ta": ["Surrender of Indian Passport Certificate படிவத்தை நிரப்பவும் (அல்லது இனி பாஸ்போர்ட் இல்லையென்றால் \"பாஸ்போர்ட் இல்லாத\" பிரகடனம் மற்றும் இழப்பு உறுதிமொழி).",
                  "உங்கள் புதிய வெளிநாட்டு குடியுரிமையின் ஆதாரத்தை சேகரிக்கவும்.",
                  "உங்கள் தூதரகத்தில் சமர்ப்பிக்கவும், பெரும்பாலும் VFS/BLS மூலம், சிறந்தது OCI விண்ணப்பத்தின் அதே வருகையில்.",
                  "செயலாக்கத்திற்கு சுமார் 1–3 வாரங்கள் காத்திருக்கவும்; பாஸ்போர்ட்டில் \"வெளிநாட்டு குடியுரிமை பெற்றதால் ரத்து செய்யப்பட்டது\" என்ற முத்திரை பதிக்கப்படும்."],
           "te": ["Surrender of Indian Passport Certificate ఫారంను పూరించండి (లేదా ఇక పాస్‌పోర్ట్ లేకపోతే \"పాస్‌పోర్ట్ లేకుండా\" డిక్లరేషన్ మరియు నష్టం అఫిడవిట్).",
                  "మీ కొత్త విదేశీ పౌరసత్వానికి రుజువును సేకరించండి.",
                  "మీ మిషన్‌లో సమర్పించండి, తరచుగా VFS/BLS ద్వారా, ఆదర్శంగా OCI దరఖాస్తుతో అదే సందర్శనలో.",
                  "ప్రాసెసింగ్ కోసం సుమారు 1–3 వారాలు వేచి ఉండండి; పాస్‌పోర్ట్‌పై \"విదేశీ జాతీయత పొందడం వల్ల రద్దు చేయబడింది\" అని ముద్రించబడుతుంది."],
           "ml": ["Surrender of Indian Passport Certificate ഫോം പൂരിപ്പിക്കുക (അല്ലെങ്കിൽ ഇനി പാസ്‌പോർട്ട് ഇല്ലെങ്കിൽ \"പാസ്‌പോർട്ട് ഇല്ലാതെ\" പ്രഖ്യാപനവും നഷ്ട സത്യവാങ്മൂലവും).",
                  "നിങ്ങളുടെ പുതിയ വിദേശ പൗരത്വത്തിന്റെ തെളിവ് ശേഖരിക്കുക.",
                  "നിങ്ങളുടെ മിഷനിൽ സമർപ്പിക്കുക, പലപ്പോഴും VFS/BLS വഴി, അനുയോജ്യമായി OCI അപേക്ഷയുടെ അതേ സന്ദർശനത്തിൽ.",
                  "പ്രോസസ്സിംഗിന് ഏകദേശം 1–3 ആഴ്ച കാത്തിരിക്കുക; പാസ്‌പോർട്ടിൽ \"വിദേശ പൗരത്വം നേടിയതിനാൽ റദ്ദാക്കി\" എന്ന് സ്റ്റാമ്പ് ചെയ്യും."]},
    docs={"en": ["Original Indian passport (or a loss affidavit if you no longer have it)", "Proof of foreign citizenship", "Passport photos", "For minors: parental consent form"],
          "hi": ["मूल भारतीय पासपोर्ट (या अगर अब नहीं है तो हानि शपथपत्र)", "विदेशी नागरिकता का प्रमाण", "पासपोर्ट फ़ोटो", "नाबालिगों के लिए: माता-पिता सहमति फ़ॉर्म"],
          "ta": ["மூல இந்திய பாஸ்போர்ட் (அல்லது இனி இல்லையென்றால் இழப்பு உறுதிமொழி)", "வெளிநாட்டு குடியுரிமையின் ஆதாரம்", "பாஸ்போர்ட் புகைப்படங்கள்", "சிறார்களுக்கு: பெற்றோர் ஒப்புதல் படிவம்"],
          "te": ["అసలు భారత పాస్‌పోర్ట్ (లేదా ఇక లేకపోతే నష్టం అఫిడవిట్)", "విదేశీ పౌరసత్వానికి రుజువు", "పాస్‌పోర్ట్ ఫోటోలు", "మైనర్ల కోసం: తల్లిదండ్రుల సమ్మతి ఫారం"],
          "ml": ["ഒറിജിനൽ ഇന്ത്യൻ പാസ്‌പോർട്ട് (അല്ലെങ്കിൽ ഇനി ഇല്ലെങ്കിൽ നഷ്ട സത്യവാങ്മൂലം)", "വിദേശ പൗരത്വത്തിന്റെ തെളിവ്", "പാസ്‌പോർട്ട് ഫോട്ടോകൾ", "കുട്ടികൾക്ക്: മാതാപിതാക്കളുടെ സമ്മത ഫോം"]},
    note={"en": "Indian law requires this — holding onto an Indian passport after taking another citizenship can create real complications later, even if you never intend to use it.",
          "hi": "भारतीय क़ानून इसकी माँग करता है — दूसरी नागरिकता लेने के बाद भारतीय पासपोर्ट रखे रहना, भले ही इस्तेमाल का इरादा न हो, बाद में वास्तविक जटिलताएँ पैदा कर सकता है।",
          "ta": "இந்திய சட்டம் இதைக் கோருகிறது — மற்றொரு குடியுரிமையை எடுத்த பிறகு இந்திய பாஸ்போர்ட்டை வைத்திருப்பது, பயன்படுத்த நினைக்காவிட்டாலும், பின்னர் உண்மையான சிக்கல்களை உருவாக்கலாம்.",
          "te": "భారత చట్టం దీన్ని కోరుతుంది — మరొక పౌరసత్వం తీసుకున్న తర్వాత భారత పాస్‌పోర్ట్‌ను ఉంచుకోవడం, మీరు దాన్ని ఉపయోగించాలని అనుకోకపోయినా, తర్వాత నిజమైన సమస్యలను సృష్టించవచ్చు.",
          "ml": "ഇന്ത്യൻ നിയമം ഇത് ആവശ്യപ്പെടുന്നു — മറ്റൊരു പൗരത്വം സ്വീകരിച്ചതിന് ശേഷം ഇന്ത്യൻ പാസ്‌പോർട്ട് കൈവശം വയ്ക്കുന്നത്, ഉപയോഗിക്കാൻ ഉദ്ദേശിക്കുന്നില്ലെങ്കിലും, പിന്നീട് യഥാർത്ഥ സങ്കീർണ്ണതകൾ സൃഷ്ടിക്കാം."},
    location={"en": "Your jurisdictional Indian Mission, often via VFS/BLS", "hi": "आपका क्षेत्राधिकार भारतीय मिशन, अक्सर VFS/BLS के ज़रिए",
               "ta": "உங்கள் அதிகார வரம்பு இந்திய தூதரகம், பெரும்பாலும் VFS/BLS மூலம்", "te": "మీ అధికార పరిధి భారత మిషన్, తరచుగా VFS/BLS ద్వారా",
               "ml": "നിങ്ങളുടെ അധികാരപരിധിയിലുള്ള ഇന്ത്യൻ മിഷൻ, പലപ്പോഴും VFS/BLS വഴി"},
    phone=None, email=None,
    links=[
        {"href": "https://www.hcilondon.gov.in/page/consular-information/", "label": {"en": "↗ Example mission guidance (London)", "hi": "↗ मिशन मार्गदर्शन उदाहरण (लंदन)",
                                                                                         "ta": "↗ மாதிரி தூதரக வழிகாட்டுதல் (லண்டன்)", "te": "↗ మిషన్ మార్గదర్శకత్వం ఉదాహరణ (లండన్)", "ml": "↗ മിഷൻ മാർഗ്ഗനിർദ്ദേശ ഉദാഹരണം (ലണ്ടൻ)"}},
        {"href": "https://ociservices.gov.in", "label": {"en": "↗ Pair with an OCI application", "hi": "↗ OCI आवेदन के साथ जोड़ें",
                                                            "ta": "↗ OCI விண்ணப்பத்துடன் இணைக்கவும்", "te": "↗ OCI దరఖాస్తుతో జతచేయండి", "ml": "↗ OCI അപേക്ഷയുമായി ജോടിയാക്കുക"}},
    ],
)

# ---- Embassy & consular help ----

entry(
    category="consular", badge_official=True, toggle_key="how_to_use",
    search_en="find your high commission embassy consulate directory",
    title={"en": "Find your High Commission / Consulate", "hi": "अपना उच्चायोग / वाणिज्य दूतावास खोजें", "ta": "உங்கள் உயர் ஸ்தானிகராலயம் / தூதரகத்தைக் கண்டறியவும்",
           "te": "మీ హై కమిషన్ / కాన్సులేట్ కనుగొనండి", "ml": "നിങ്ങളുടെ ഹൈക്കമ്മീഷൻ / കോൺസുലേറ്റ് കണ്ടെത്തുക"},
    desc={"en": "The Ministry of External Affairs maintains the master directory of every Indian embassy, high commission and consulate abroad, with addresses, phone lines and jurisdiction maps for each.",
          "hi": "विदेश मंत्रालय विदेश में हर भारतीय दूतावास, उच्चायोग और वाणिज्य दूतावास की मुख्य निर्देशिका रखता है, जिसमें प्रत्येक के पते, फ़ोन लाइनें और क्षेत्राधिकार मानचित्र शामिल हैं।",
          "ta": "வெளிநாட்டு அமைச்சகம் வெளிநாட்டில் உள்ள ஒவ்வொரு இந்திய தூதரகம், உயர் ஸ்தானிகராலயம் மற்றும் துணைத்தூதரகத்தின் முதன்மை அடைவை பராமரிக்கிறது, ஒவ்வொன்றுக்கும் முகவரிகள், தொலைபேசி எண்கள் மற்றும் அதிகார வரம்பு வரைபடங்களுடன்.",
          "te": "విదేశీ వ్యవహారాల మంత్రిత్వ శాఖ విదేశాలలోని ప్రతి భారత రాయబార కార్యాలయం, హై కమిషన్ మరియు కాన్సులేట్ యొక్క మాస్టర్ డైరెక్టరీని నిర్వహిస్తుంది, ప్రతిదానికీ చిరునామాలు, ఫోన్ లైన్లు మరియు అధికార పరిధి మ్యాప్‌లతో సహా.",
          "ml": "വിദേശകാര്യ മന്ത്രാലയം വിദേശത്തുള്ള എല്ലാ ഇന്ത്യൻ എംബസി, ഹൈക്കമ്മീഷൻ, കോൺസുലേറ്റ് എന്നിവയുടെ പ്രധാന ഡയറക്ടറി സൂക്ഷിക്കുന്നു, ഓരോന്നിനും വിലാസങ്ങൾ, ഫോൺ ലൈനുകൾ, അധികാരപരിധി മാപ്പുകൾ എന്നിവയോടെ."},
    handles={"en": "address · phone · jurisdiction", "hi": "पता · फ़ोन · क्षेत्राधिकार", "ta": "முகவரி · தொலைபேசி · அதிகார வரம்பு",
             "te": "చిరునామా · ఫోన్ · అధికార పరిధి", "ml": "വിലാസം · ഫോൺ · അധികാരപരിധി"},
    steps={"en": ["Go to the MEA missions directory and search by country or city.",
                  "Note both your nearest mission and its specific jurisdiction — some countries have multiple consulates, each covering different regions.",
                  "Save its direct contact page, not just the general mea.gov.in number."],
           "hi": ["MEA मिशन निर्देशिका पर जाएँ और देश या शहर के अनुसार खोजें।",
                  "अपने नज़दीकी मिशन और उसके विशिष्ट क्षेत्राधिकार दोनों को नोट करें — कुछ देशों में कई वाणिज्य दूतावास हैं, प्रत्येक अलग-अलग क्षेत्रों को कवर करता है।",
                  "सिर्फ़ सामान्य mea.gov.in नंबर नहीं, इसका सीधा संपर्क पृष्ठ सहेजें।"],
           "ta": ["MEA தூதரக அடைவுக்குச் சென்று நாடு அல்லது நகரம் மூலம் தேடவும்.",
                  "உங்கள் அருகிலுள்ள தூதரகம் மற்றும் அதன் குறிப்பிட்ட அதிகார வரம்பு இரண்டையும் குறித்துக்கொள்ளுங்கள் — சில நாடுகளில் பல துணைத்தூதரகங்கள் உள்ளன, ஒவ்வொன்றும் வெவ்வேறு பகுதிகளை உள்ளடக்கியது.",
                  "பொதுவான mea.gov.in எண் மட்டுமல்ல, அதன் நேரடி தொடர்பு பக்கத்தை சேமிக்கவும்."],
           "te": ["MEA మిషన్ల డైరెక్టరీకి వెళ్లి దేశం లేదా నగరం ద్వారా శోధించండి.",
                  "మీ సమీప మిషన్ మరియు దాని నిర్దిష్ట అధికార పరిధిని రెండింటినీ గమనించండి — కొన్ని దేశాలలో బహుళ కాన్సులేట్‌లు ఉన్నాయి, ప్రతి ఒక్కటి వేర్వేరు ప్రాంతాలను కవర్ చేస్తుంది.",
                  "సాధారణ mea.gov.in నంబర్ మాత్రమే కాకుండా, దాని ప్రత్యక్ష సంప్రదింపు పేజీని సేవ్ చేసుకోండి."],
           "ml": ["MEA മിഷനുകളുടെ ഡയറക്ടറിയിലേക്ക് പോയി രാജ്യം അല്ലെങ്കിൽ നഗരം അനുസരിച്ച് തിരയുക.",
                  "നിങ്ങളുടെ അടുത്തുള്ള മിഷനും അതിന്റെ പ്രത്യേക അധികാരപരിധിയും കുറിക്കുക — ചില രാജ്യങ്ങളിൽ ഒന്നിലധികം കോൺസുലേറ്റുകൾ ഉണ്ട്, ഓരോന്നും വ്യത്യസ്ത പ്രദേശങ്ങൾ ഉൾക്കൊള്ളുന്നു.",
                  "പൊതുവായ mea.gov.in നമ്പർ മാത്രമല്ല, അതിന്റെ നേരിട്ടുള്ള ബന്ധപ്പെടൽ പേജ് സേവ് ചെയ്യുക."]},
    docs={"en": [], "hi": [], "ta": [], "te": [], "ml": []},
    note={"en": "Bookmark this before you need it — searching for it during an actual emergency wastes time.",
          "hi": "ज़रूरत पड़ने से पहले इसे बुकमार्क करें — वास्तविक आपातकाल के दौरान इसे खोजना समय बर्बाद करता है।",
          "ta": "தேவைப்படுவதற்கு முன் இதை புக்மார்க் செய்யவும் — உண்மையான அவசரகாலத்தில் இதைத் தேடுவது நேரத்தை வீணடிக்கும்.",
          "te": "అవసరమయ్యే ముందే దీన్ని బుక్‌మార్క్ చేసుకోండి — నిజమైన అత్యవసర సమయంలో దీన్ని వెతకడం సమయాన్ని వృథా చేస్తుంది.",
          "ml": "ആവശ്യമുള്ളതിന് മുമ്പേ ഇത് ബുക്ക്മാർക്ക് ചെയ്യുക — യഥാർത്ഥ അടിയന്തിര സാഹചര്യത്തിൽ ഇത് തിരയുന്നത് സമയം പാഴാക്കും."},
    location={"en": "Online directory — mea.gov.in", "hi": "ऑनलाइन निर्देशिका — mea.gov.in", "ta": "ஆன்லைன் அடைவு — mea.gov.in",
               "te": "ఆన్‌లైన్ డైరెక్టరీ — mea.gov.in", "ml": "ഓൺലൈൻ ഡയറക്ടറി — mea.gov.in"},
    phone=None, email=None,
    links=[
        {"href": "https://www.mea.gov.in", "label": {"en": "↗ mea.gov.in — Indian Missions Abroad", "hi": "↗ mea.gov.in — विदेश में भारतीय मिशन",
                                                        "ta": "↗ mea.gov.in — வெளிநாட்டு இந்திய தூதரகங்கள்", "te": "↗ mea.gov.in — విదేశాల్లో భారత మిషన్లు", "ml": "↗ mea.gov.in — വിദേശത്തെ ഇന്ത്യൻ മിഷനുകൾ"}},
        {"href": "https://igod.gov.in/int/INMISS/organizations", "label": {"en": "↗ Government directory listing (igod.gov.in)", "hi": "↗ सरकारी निर्देशिका सूची (igod.gov.in)",
                                                                              "ta": "↗ அரசு அடைவு பட்டியல் (igod.gov.in)", "te": "↗ ప్రభుత్వ డైరెక్టరీ జాబితా (igod.gov.in)", "ml": "↗ സർക്കാർ ഡയറക്ടറി പട്ടിക (igod.gov.in)"}},
    ],
)

entry(
    category="consular", badge_official=True,
    search_en="madad portal grievance complaint consular",
    title={"en": "MADAD — file a consular complaint", "hi": "MADAD — वाणिज्य दूत शिकायत दर्ज करें", "ta": "MADAD — துணைத்தூதரக புகார் தாக்கல் செய்யவும்",
           "te": "MADAD — కాన్సులర్ ఫిర్యాదు దాఖలు చేయండి", "ml": "MADAD — കോൺസുലാർ പരാതി ഫയൽ ചെയ്യുക"},
    desc={"en": "MADAD is the MEA's online grievance-tracking system for overseas Indians: passport delays, mission non-response, employer disputes and more, logged and tracked to resolution instead of sent into a general inbox.",
          "hi": "MADAD विदेश में रह रहे भारतीयों के लिए MEA की ऑनलाइन शिकायत-ट्रैकिंग प्रणाली है: पासपोर्ट में देरी, मिशन से जवाब न मिलना, नियोक्ता विवाद और अधिक, जो सामान्य इनबॉक्स में भेजने के बजाय दर्ज होकर समाधान तक ट्रैक किए जाते हैं।",
          "ta": "MADAD என்பது வெளிநாட்டு இந்தியர்களுக்கான MEA இன் ஆன்லைன் குறை-கண்காணிப்பு அமைப்பு: பாஸ்போர்ட் தாமதங்கள், தூதரக பதிலின்மை, முதலாளி தகராறுகள் மற்றும் பல, பொது இன்பாக்ஸிற்கு அனுப்புவதற்குப் பதிலாக பதிவு செய்யப்பட்டு தீர்வு வரை கண்காணிக்கப்படும்.",
          "te": "MADAD అనేది విదేశాల్లోని భారతీయుల కోసం MEA యొక్క ఆన్‌లైన్ ఫిర్యాదు-ట్రాకింగ్ వ్యవస్థ: పాస్‌పోర్ట్ ఆలస్యాలు, మిషన్ స్పందించకపోవడం, యజమాని వివాదాలు మరియు మరిన్ని, సాధారణ ఇన్‌బాక్స్‌కు పంపే బదులు నమోదు చేయబడి పరిష్కారం వరకు ట్రాక్ చేయబడతాయి.",
          "ml": "MADAD എന്നത് വിദേശ ഇന്ത്യക്കാർക്കായുള്ള MEA യുടെ ഓൺലൈൻ പരാതി-ട്രാക്കിംഗ് സംവിധാനമാണ്: പാസ്‌പോർട്ട് കാലതാമസങ്ങൾ, മിഷൻ പ്രതികരിക്കാത്തത്, തൊഴിലുടമ തർക്കങ്ങൾ എന്നിവയും അതിലേറെയും, ഒരു പൊതു ഇൻബോക്സിലേക്ക് അയക്കുന്നതിന് പകരം രേഖപ്പെടുത്തി പരിഹാരം വരെ ട്രാക്ക് ചെയ്യുന്നു."},
    handles={"en": "grievance tracking · status updates", "hi": "शिकायत ट्रैकिंग · स्थिति अपडेट", "ta": "குறை கண்காணிப்பு · நிலை புதுப்பிப்புகள்",
             "te": "ఫిర్యాదు ట్రాకింగ్ · స్థితి అప్‌డేట్‌లు", "ml": "പരാതി ട്രാക്കിംഗ് · സ്റ്റാറ്റസ് അപ്‌ഡേറ്റുകൾ"},
    steps={"en": ["Register at the MADAD portal with your name, date of birth, mobile number and email.",
                  "Verify your account via the confirmation link emailed to you.",
                  "File your grievance — for yourself or someone else — choosing the closest matching category (imprisonment, unpaid wages, mortal remains, and so on).",
                  "Save the reference number you're given and track status online."],
           "hi": ["अपना नाम, जन्मतिथि, मोबाइल नंबर और ईमेल के साथ MADAD पोर्टल पर पंजीकरण करें।",
                  "ईमेल किए गए पुष्टिकरण लिंक के ज़रिए अपना खाता सत्यापित करें।",
                  "अपनी शिकायत दर्ज करें — अपने लिए या किसी और के लिए — निकटतम मिलती श्रेणी चुनते हुए (कारावास, बकाया वेतन, पार्थिव शरीर, आदि)।",
                  "दिया गया संदर्भ नंबर सहेजें और ऑनलाइन स्थिति ट्रैक करें।"],
           "ta": ["உங்கள் பெயர், பிறந்த தேதி, மொபைல் எண் மற்றும் மின்னஞ்சலுடன் MADAD போர்ட்டலில் பதிவு செய்யவும்.",
                  "மின்னஞ்சல் செய்யப்பட்ட உறுதிப்படுத்தல் இணைப்பு மூலம் உங்கள் கணக்கை சரிபார்க்கவும்.",
                  "உங்கள் குறையை தாக்கல் செய்யவும் — உங்களுக்காக அல்லது வேறு யாருக்காகவும் — நெருங்கிய பொருந்தும் வகையை தேர்ந்தெடுத்து (சிறைவாசம், ஊதியம் கிடைக்காதது, உடல், முதலியன).",
                  "உங்களுக்கு வழங்கப்பட்ட குறிப்பு எண்ணை சேமித்து ஆன்லைனில் நிலையை கண்காணிக்கவும்."],
           "te": ["మీ పేరు, పుట్టిన తేదీ, మొబైల్ నంబర్ మరియు ఇమెయిల్‌తో MADAD పోర్టల్‌లో నమోదు చేసుకోండి.",
                  "మీకు ఇమెయిల్ చేయబడిన నిర్ధారణ లింక్ ద్వారా మీ ఖాతాను ధృవీకరించండి.",
                  "మీ ఫిర్యాదును దాఖలు చేయండి — మీ కోసం లేదా మరొకరి కోసం — దగ్గరగా సరిపోలే వర్గాన్ని ఎంచుకుని (జైలు శిక్ష, జీతం రాకపోవడం, మృతదేహం, మొదలైనవి).",
                  "మీకు ఇచ్చిన రిఫరెన్స్ నంబర్‌ను సేవ్ చేసుకుని ఆన్‌లైన్‌లో స్థితిని ట్రాక్ చేయండి."],
           "ml": ["നിങ്ങളുടെ പേര്, ജനനത്തീയതി, മൊബൈൽ നമ്പർ, ഇമെയിൽ എന്നിവയോടെ MADAD പോർട്ടലിൽ രജിസ്റ്റർ ചെയ്യുക.",
                  "നിങ്ങൾക്ക് ഇമെയിൽ ചെയ്ത സ്ഥിരീകരണ ലിങ്ക് വഴി നിങ്ങളുടെ അക്കൗണ്ട് സ്ഥിരീകരിക്കുക.",
                  "നിങ്ങളുടെ പരാതി ഫയൽ ചെയ്യുക — നിങ്ങൾക്കോ മറ്റാർക്കെങ്കിലുമോ വേണ്ടി — ഏറ്റവും അടുത്ത വിഭാഗം തിരഞ്ഞെടുത്ത് (തടവ്, ശമ്പളം കിട്ടാത്തത്, മൃതദേഹം, മുതലായവ).",
                  "നിങ്ങൾക്ക് ലഭിച്ച റഫറൻസ് നമ്പർ സേവ് ചെയ്ത് ഓൺലൈനിൽ സ്റ്റാറ്റസ് ട്രാക്ക് ചെയ്യുക."]},
    docs={"en": ["Basic ID details", "A clear description of the issue", "Any supporting documents (contract, correspondence)"],
          "hi": ["बुनियादी पहचान विवरण", "समस्या का स्पष्ट विवरण", "कोई भी सहायक दस्तावेज़ (अनुबंध, पत्राचार)"],
          "ta": ["அடிப்படை அடையாள விவரங்கள்", "பிரச்சினையின் தெளிவான விளக்கம்", "ஏதேனும் ஆதரவு ஆவணங்கள் (ஒப்பந்தம், கடிதப் பரிமாற்றம்)"],
          "te": ["ప్రాథమిక గుర్తింపు వివరాలు", "సమస్య యొక్క స్పష్టమైన వివరణ", "ఏదైనా సహాయక పత్రాలు (ఒప్పందం, ఉత్తర ప్రత్యుత్తరాలు)"],
          "ml": ["അടിസ്ഥാന ഐഡി വിവരങ്ങൾ", "പ്രശ്നത്തിന്റെ വ്യക്തമായ വിവരണം", "ഏതെങ്കിലും പിന്തുണാ രേഖകൾ (കരാർ, കത്തിടപാടുകൾ)"]},
    note={"en": "Cases are colour-coded by how long they've been open and escalate automatically up the chain — a MADAD complaint tends to get more traction than an email to a generic inbox.",
          "hi": "मामलों को कितने समय से खुले हैं इसके अनुसार रंग-कोडित किया जाता है और वे अपने आप श्रृंखला में ऊपर बढ़ते हैं — MADAD शिकायत सामान्य इनबॉक्स को ईमेल की तुलना में अधिक असर दिखाती है।",
          "ta": "வழக்குகள் எவ்வளவு காலமாக திறந்திருக்கின்றன என்பதைப் பொறுத்து வண்ண-குறியிடப்பட்டு தானாக சங்கிலியில் மேலே செல்கின்றன — ஒரு MADAD புகார் பொது இன்பாக்ஸிற்கு அனுப்பும் மின்னஞ்சலை விட அதிக கவனத்தைப் பெறும்.",
          "te": "కేసులు ఎంతకాలం తెరిచి ఉన్నాయో దాని ఆధారంగా రంగు-కోడ్ చేయబడి ఆటోమేటిక్‌గా చైన్‌లో పైకి ఎస్కలేట్ అవుతాయి — సాధారణ ఇన్‌బాక్స్‌కు ఇమెయిల్ కంటే MADAD ఫిర్యాదుకు ఎక్కువ ప్రాధాన్యత లభిస్తుంది.",
          "ml": "കേസുകൾ എത്ര കാലമായി തുറന്നിരിക്കുന്നു എന്നതനുസരിച്ച് നിറം-കോഡ് ചെയ്ത് ചെയിനിൽ സ്വയമേവ മുകളിലേക്ക് പോകുന്നു — ഒരു പൊതു ഇൻബോക്സിലേക്കുള്ള ഇമെയിലിനേക്കാൾ MADAD പരാതിക്ക് കൂടുതൽ ശ്രദ്ധ ലഭിക്കും."},
    location={"en": "Online portal", "hi": "ऑनलाइन पोर्टल", "ta": "ஆன்லைன் போர்ட்டல்", "te": "ఆన్‌లైన్ పోర్టల్", "ml": "ഓൺലൈൻ പോർട്ടൽ"},
    phone=None,
    email={"en": "helpline@mea.gov.in", "hi": "helpline@mea.gov.in", "ta": "helpline@mea.gov.in", "te": "helpline@mea.gov.in", "ml": "helpline@mea.gov.in"},
    links=[{"href": "https://www.mea.gov.in/consular-complaints-and-grievances", "label": {"en": "↗ File on MADAD via mea.gov.in", "hi": "↗ mea.gov.in के ज़रिए MADAD पर दर्ज करें",
                                                                                              "ta": "↗ mea.gov.in மூலம் MADAD இல் தாக்கல் செய்யவும்", "te": "↗ mea.gov.in ద్వారా MADAD లో దాఖలు చేయండి", "ml": "↗ mea.gov.in വഴി MADAD ൽ ഫയൽ ചെയ്യുക"}}],
)

entry(
    category="consular", badge_official=True,
    search_en="indian community welfare fund icwf emergency financial assistance",
    title={"en": "Indian Community Welfare Fund (ICWF)", "hi": "भारतीय समुदाय कल्याण कोष (ICWF)", "ta": "இந்திய சமூக நல நிதி (ICWF)",
           "te": "భారతీయ కమ్యూనిటీ వెల్ఫేర్ ఫండ్ (ICWF)", "ml": "ഇന്ത്യൻ കമ്മ്യൂണിറ്റി വെൽഫെയർ ഫണ്ട് (ICWF)"},
    desc={"en": "Emergency, need-based assistance run through missions: repatriating stranded or destitute workers, funding return of a body, legal aid, and shelter for women in distress — not a loan scheme, a genuine safety net for those with nowhere else to turn.",
          "hi": "मिशनों के ज़रिए चलाई जाने वाली आपातकालीन, ज़रूरत-आधारित सहायता: फंसे या निराश्रित कामगारों को स्वदेश भेजना, शव वापसी हेतु धन, क़ानूनी सहायता, और संकट में महिलाओं के लिए आश्रय — यह ऋण योजना नहीं, बल्कि उन लोगों के लिए वास्तविक सुरक्षा जाल है जिनके पास और कोई सहारा नहीं है।",
          "ta": "தூதரகங்கள் மூலம் இயங்கும் அவசர, தேவை அடிப்படையிலான உதவி: மாட்டிக்கொண்ட அல்லது வறிய தொழிலாளர்களை திரும்ப அனுப்புதல், உடல் திரும்புவதற்கு நிதி, சட்ட உதவி, மற்றும் துன்பத்தில் உள்ள பெண்களுக்கு தங்குமிடம் — இது கடன் திட்டம் அல்ல, வேறு எந்த வழியும் இல்லாதவர்களுக்கான உண்மையான பாதுகாப்பு வலை.",
          "te": "మిషన్ల ద్వారా నడిచే అత్యవసర, అవసర-ఆధారిత సహాయం: చిక్కుకుపోయిన లేదా నిరుపేద కార్మికులను తిరిగి పంపడం, మృతదేహం తిరిగి రావడానికి నిధులు, న్యాయ సహాయం, మరియు కష్టాల్లో ఉన్న మహిళలకు ఆశ్రయం — ఇది రుణ పథకం కాదు, మరెక్కడా ఆధారం లేనివారికి నిజమైన భద్రతా వలయం.",
          "ml": "മിഷനുകൾ വഴി നടത്തുന്ന അടിയന്തിര, ആവശ്യാധിഷ്ഠിത സഹായം: കുടുങ്ങിയ അല്ലെങ്കിൽ നിരാലംബരായ തൊഴിലാളികളെ തിരിച്ചയക്കൽ, മൃതദേഹം തിരികെ എത്തിക്കാൻ ധനസഹായം, നിയമ സഹായം, ദുരിതത്തിലുള്ള സ്ത്രീകൾക്ക് അഭയം — ഇത് ഒരു വായ്പാ പദ്ധതിയല്ല, മറ്റൊരു വഴിയുമില്ലാത്തവർക്കുള്ള യഥാർത്ഥ സുരക്ഷാ വല."},
    handles={"en": "repatriation · legal aid · shelter", "hi": "प्रत्यावर्तन · क़ानूनी सहायता · आश्रय", "ta": "திருப்பி அனுப்புதல் · சட்ட உதவி · தங்குமிடம்",
             "te": "తరలింపు · న్యాయ సహాయం · ఆశ్రయం", "ml": "തിരിച്ചയക്കൽ · നിയമ സഹായം · അഭയം"},
    steps={"en": ["Contact your nearest mission directly — there's no separate online application; a consular officer assesses each case individually.",
                  "Explain the emergency clearly: what's happened and what kind of help you need (lodging, airfare home, legal aid, medical care, repatriation).",
                  "An officer at the mission assesses eligibility and, if approved, arranges the specific assistance."],
           "hi": ["सीधे अपने नज़दीकी मिशन से संपर्क करें — कोई अलग ऑनलाइन आवेदन नहीं है; एक वाणिज्य दूत अधिकारी हर मामले का व्यक्तिगत रूप से आकलन करता है।",
                  "आपातकाल को स्पष्ट रूप से बताएँ: क्या हुआ और आपको किस तरह की मदद चाहिए (आवास, स्वदेश किराया, क़ानूनी सहायता, चिकित्सा देखभाल, प्रत्यावर्तन)।",
                  "मिशन का एक अधिकारी पात्रता का आकलन करता है और मंज़ूरी मिलने पर विशिष्ट सहायता की व्यवस्था करता है।"],
           "ta": ["உங்கள் அருகிலுள்ள தூதரகத்தை நேரடியாக தொடர்பு கொள்ளுங்கள் — தனி ஆன்லைன் விண்ணப்பம் இல்லை; ஒரு துணைத்தூதரக அதிகாரி ஒவ்வொரு வழக்கையும் தனித்தனியாக மதிப்பிடுவார்.",
                  "அவசரநிலையை தெளிவாக விளக்குங்கள்: என்ன நடந்தது மற்றும் உங்களுக்கு என்ன உதவி தேவை (தங்குமிடம், வீட்டிற்கு விமான கட்டணம், சட்ட உதவி, மருத்துவ பராமரிப்பு, திரும்ப அனுப்புதல்).",
                  "தூதரகத்தில் உள்ள ஒரு அதிகாரி தகுதியை மதிப்பிட்டு, அங்கீகரிக்கப்பட்டால், குறிப்பிட்ட உதவியை ஏற்பாடு செய்வார்."],
           "te": ["మీ సమీప మిషన్‌ను నేరుగా సంప్రదించండి — వేరే ఆన్‌లైన్ దరఖాస్తు లేదు; ఒక కాన్సులర్ అధికారి ప్రతి కేసును వ్యక్తిగతంగా అంచనా వేస్తారు.",
                  "అత్యవసర పరిస్థితిని స్పష్టంగా వివరించండి: ఏమి జరిగింది మరియు మీకు ఎలాంటి సహాయం కావాలి (వసతి, ఇంటికి విమాన ఛార్జీ, న్యాయ సహాయం, వైద్య సంరక్షణ, తరలింపు).",
                  "మిషన్‌లోని ఒక అధికారి అర్హతను అంచనా వేసి, ఆమోదిస్తే, నిర్దిష్ట సహాయాన్ని ఏర్పాటు చేస్తారు."],
           "ml": ["നിങ്ങളുടെ അടുത്തുള്ള മിഷനെ നേരിട്ട് ബന്ധപ്പെടുക — പ്രത്യേക ഓൺലൈൻ അപേക്ഷ ഇല്ല; ഒരു കോൺസുലാർ ഉദ്യോഗസ്ഥൻ ഓരോ കേസും വ്യക്തിഗതമായി വിലയിരുത്തുന്നു.",
                  "അടിയന്തിരാവസ്ഥ വ്യക്തമായി വിശദീകരിക്കുക: എന്താണ് സംഭവിച്ചത്, നിങ്ങൾക്ക് എന്ത് സഹായമാണ് വേണ്ടത് (താമസം, നാട്ടിലേക്കുള്ള വിമാന ചെലവ്, നിയമ സഹായം, മെഡിക്കൽ പരിചരണം, തിരിച്ചയക്കൽ).",
                  "മിഷനിലെ ഒരു ഉദ്യോഗസ്ഥൻ യോഗ്യത വിലയിരുത്തി, അംഗീകരിച്ചാൽ, നിർദ്ദിഷ്ട സഹായം ഏർപ്പാടാക്കുന്നു."]},
    docs={"en": ["Proof you entered the country legally (passport/visa)", "Whatever documents relate to the emergency itself"],
          "hi": ["आप क़ानूनी रूप से देश में प्रवेश किए इसका प्रमाण (पासपोर्ट/वीज़ा)", "आपातकाल से संबंधित जो भी दस्तावेज़ हों"],
          "ta": ["நீங்கள் சட்டப்பூர்வமாக நாட்டில் நுழைந்ததற்கான ஆதாரம் (பாஸ்போர்ட்/விசா)", "அவசரநிலையுடன் தொடர்புடைய எந்த ஆவணங்களும்"],
          "te": ["మీరు చట్టబద్ధంగా దేశంలోకి ప్రవేశించారని రుజువు (పాస్‌పోర్ట్/వీసా)", "అత్యవసర పరిస్థితికి సంబంధించిన ఏవైనా పత్రాలు"],
          "ml": ["നിങ്ങൾ നിയമപരമായി രാജ്യത്ത് പ്രവേശിച്ചു എന്നതിന്റെ തെളിവ് (പാസ്‌പോർട്ട്/വിസ)", "അടിയന്തിരാവസ്ഥയുമായി ബന്ധപ്പെട്ട എന്തെങ്കിലും രേഖകൾ"]},
    note={"en": "OCI and PIO cardholders generally aren't eligible for individual ICWF assistance — it's specifically for Indian citizens/passport holders in distress.",
          "hi": "OCI और PIO कार्डधारक आमतौर पर व्यक्तिगत ICWF सहायता के पात्र नहीं हैं — यह विशेष रूप से संकट में फँसे भारतीय नागरिकों/पासपोर्ट धारकों के लिए है।",
          "ta": "OCI மற்றும் PIO அட்டைதாரர்கள் பொதுவாக தனிப்பட்ட ICWF உதவிக்கு தகுதியற்றவர்கள் — இது குறிப்பாக துன்பத்தில் உள்ள இந்திய குடிமக்கள்/பாஸ்போர்ட் வைத்திருப்பவர்களுக்கானது.",
          "te": "OCI మరియు PIO కార్డుదారులు సాధారణంగా వ్యక్తిగత ICWF సహాయానికి అర్హులు కారు — ఇది ప్రత్యేకంగా కష్టాల్లో ఉన్న భారత పౌరులు/పాస్‌పోర్ట్ హోల్డర్ల కోసం.",
          "ml": "OCI, PIO കാർഡ് ഉടമകൾക്ക് സാധാരണയായി വ്യക്തിഗത ICWF സഹായത്തിന് അർഹതയില്ല — ഇത് പ്രത്യേകമായി ദുരിതത്തിലുള്ള ഇന്ത്യൻ പൗരന്മാർ/പാസ്‌പോർട്ട് ഉടമകൾക്ക് വേണ്ടിയുള്ളതാണ്."},
    location={"en": "Your nearest Indian Mission (assessed case-by-case, no online form)",
               "hi": "आपका नज़दीकी भारतीय मिशन (मामले-दर-मामले आकलन, कोई ऑनलाइन फ़ॉर्म नहीं)",
               "ta": "உங்கள் அருகிலுள்ள இந்திய தூதரகம் (வழக்கு வாரியாக மதிப்பீடு, ஆன்லைன் படிவம் இல்லை)",
               "te": "మీ సమీప భారత మిషన్ (కేసుల వారీగా అంచనా, ఆన్‌లైన్ ఫారం లేదు)",
               "ml": "നിങ്ങളുടെ അടുത്തുള്ള ഇന്ത്യൻ മിഷൻ (കേസ്-ബൈ-കേസ് വിലയിരുത്തൽ, ഓൺലൈൻ ഫോം ഇല്ല)"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/icwf", "label": {"en": "↗ ICWF details — mea.gov.in", "hi": "↗ ICWF विवरण — mea.gov.in",
                                                                "ta": "↗ ICWF விவரங்கள் — mea.gov.in", "te": "↗ ICWF వివరాలు — mea.gov.in", "ml": "↗ ICWF വിശദാംശങ്ങൾ — mea.gov.in"}}],
)

entry(
    category="consular", badge_official=True, toggle_key="how_to_use",
    search_en="pravasi bharatiya sahayata kendra helpline gulf workers",
    title={"en": "Pravasi Bharatiya Sahayata Kendra", "hi": "प्रवासी भारतीय सहायता केंद्र", "ta": "பிரவாசி பாரதிய சஹாயதா கேந்திரா",
           "te": "ప్రవాసీ భారతీయ సహాయతా కేంద్రం", "ml": "പ്രവാസി ഭാരതീയ സഹായതാ കേന്ദ്ര"},
    desc={"en": "Walk-in help desks at missions in several Gulf countries for workers in distress — unpaid salaries, passport confiscation by an employer, or exploitative contracts — staffed for exactly this kind of case.",
          "hi": "कई ख़ाड़ी देशों के मिशनों में संकटग्रस्त कामगारों के लिए वॉक-इन सहायता डेस्क — बकाया वेतन, नियोक्ता द्वारा पासपोर्ट ज़ब्त करना, या शोषणकारी अनुबंध — इसी तरह के मामलों के लिए तैनात।",
          "ta": "பல வளைகுடா நாடுகளில் உள்ள தூதரகங்களில் துன்பத்தில் உள்ள தொழிலாளர்களுக்கான வாக்-இன் உதவி மேசைகள் — ஊதியம் கிடைக்காதது, முதலாளியால் பாஸ்போர்ட் பறிமுதல், அல்லது சுரண்டல் ஒப்பந்தங்கள் — சரியாக இந்த வகை வழக்குகளுக்காக பணியாளர்கள்.",
          "te": "అనేక గల్ఫ్ దేశాలలోని మిషన్లలో కష్టాల్లో ఉన్న కార్మికుల కోసం వాక్-ఇన్ సహాయ డెస్క్‌లు — జీతం రాకపోవడం, యజమాని పాస్‌పోర్ట్ జప్తు చేయడం, లేదా దోపిడీ ఒప్పందాలు — సరిగ్గా ఈ రకమైన కేసుల కోసం సిబ్బంది.",
          "ml": "പല ഗൾഫ് രാജ്യങ്ങളിലെയും മിഷനുകളിൽ ദുരിതത്തിലുള്ള തൊഴിലാളികൾക്കായുള്ള വാക്-ഇൻ സഹായ ഡെസ്കുകൾ — ശമ്പളം കിട്ടാത്തത്, തൊഴിലുടമ പാസ്‌പോർട്ട് പിടിച്ചെടുക്കൽ, അല്ലെങ്കിൽ ചൂഷണപരമായ കരാറുകൾ — കൃത്യമായി ഇത്തരം കേസുകൾക്കായി ജീവനക്കാർ."},
    handles={"en": "labour disputes · in-person help desks", "hi": "श्रम विवाद · व्यक्तिगत सहायता डेस्क", "ta": "தொழிலாளர் தகராறுகள் · நேரடி உதவி மேசைகள்",
             "te": "కార్మిక వివాదాలు · వ్యక్తిగత సహాయ డెస్క్‌లు", "ml": "തൊഴിൽ തർക്കങ്ങൾ · നേരിട്ടുള്ള സഹായ ഡെസ്കുകൾ"},
    steps={"en": ["Locate the nearest Kendra via the mission page — these exist mainly in Gulf countries with large numbers of Indian workers.",
                  "Walk in during opening hours, or call ahead if the situation is urgent.",
                  "Describe the labour dispute or distress situation — passport confiscation, unpaid wages, an exploitative contract."],
           "hi": ["मिशन पृष्ठ के ज़रिए नज़दीकी केंद्र खोजें — ये मुख्य रूप से बड़ी संख्या में भारतीय कामगारों वाले ख़ाड़ी देशों में मौजूद हैं।",
                  "खुलने के समय के दौरान सीधे जाएँ, या स्थिति अत्यावश्यक हो तो पहले फ़ोन करें।",
                  "श्रम विवाद या संकट की स्थिति बताएँ — पासपोर्ट ज़ब्ती, बकाया वेतन, शोषणकारी अनुबंध।"],
           "ta": ["தூதரக பக்கம் மூலம் அருகிலுள்ள கேந்திராவைக் கண்டறியவும் — இவை முக்கியமாக அதிக எண்ணிக்கையிலான இந்திய தொழிலாளர்கள் உள்ள வளைகுடா நாடுகளில் உள்ளன.",
                  "திறந்திருக்கும் நேரத்தில் நேரடியாக செல்லுங்கள், அல்லது நிலைமை அவசரமானால் முன்கூட்டியே அழைக்கவும்.",
                  "தொழிலாளர் தகராறு அல்லது துன்ப நிலையை விவரிக்கவும் — பாஸ்போர்ட் பறிமுதல், ஊதியம் கிடைக்காதது, சுரண்டல் ஒப்பந்தம்."],
           "te": ["మిషన్ పేజీ ద్వారా సమీప కేంద్రాన్ని కనుగొనండి — ఇవి ప్రధానంగా పెద్ద సంఖ్యలో భారతీయ కార్మికులు ఉన్న గల్ఫ్ దేశాలలో ఉన్నాయి.",
                  "తెరిచి ఉండే సమయాల్లో నేరుగా వెళ్లండి, లేదా పరిస్థితి అత్యవసరమైతే ముందుగా కాల్ చేయండి.",
                  "కార్మిక వివాదం లేదా కష్ట పరిస్థితిని వివరించండి — పాస్‌పోర్ట్ జప్తు, జీతం రాకపోవడం, దోపిడీ ఒప్పందం."],
           "ml": ["മിഷൻ പേജ് വഴി അടുത്തുള്ള കേന്ദ്ര കണ്ടെത്തുക — ഇവ പ്രധാനമായും വലിയ തോതിൽ ഇന്ത്യൻ തൊഴിലാളികളുള്ള ഗൾഫ് രാജ്യങ്ങളിലാണ്.",
                  "തുറന്നിരിക്കുന്ന സമയത്ത് നേരിട്ട് പോകുക, അല്ലെങ്കിൽ സാഹചര്യം അടിയന്തിരമാണെങ്കിൽ മുൻകൂട്ടി വിളിക്കുക.",
                  "തൊഴിൽ തർക്കമോ ദുരിത സാഹചര്യമോ വിവരിക്കുക — പാസ്‌പോർട്ട് പിടിച്ചെടുക്കൽ, ശമ്പളം കിട്ടാത്തത്, ചൂഷണപരമായ കരാർ."]},
    docs={"en": ["Passport copy, if you have one", "Any contract or correspondence with your employer"],
          "hi": ["पासपोर्ट की प्रति, अगर हो", "नियोक्ता के साथ कोई अनुबंध या पत्राचार"],
          "ta": ["பாஸ்போர்ட் நகல், இருந்தால்", "உங்கள் முதலாளியுடன் ஏதேனும் ஒப்பந்தம் அல்லது கடிதப் பரிமாற்றம்"],
          "te": ["పాస్‌పోర్ట్ కాపీ, ఉంటే", "మీ యజమానితో ఏదైనా ఒప్పందం లేదా ఉత్తర ప్రత్యుత్తరాలు"],
          "ml": ["പാസ്‌പോർട്ട് പകർപ്പ്, ഉണ്ടെങ്കിൽ", "നിങ്ങളുടെ തൊഴിലുടമയുമായുള്ള ഏതെങ്കിലും കരാർ അല്ലെങ്കിൽ കത്തിടപാടുകൾ"]},
    note={"en": "These desks exist because many workers can't easily travel to a full mission — check whether one covers your city before assuming you need to go to the capital.",
          "hi": "ये डेस्क इसलिए मौजूद हैं क्योंकि कई कामगार पूरे मिशन तक आसानी से नहीं जा सकते — यह मान लेने से पहले कि आपको राजधानी जाना है, जाँचें कि क्या कोई आपके शहर को कवर करता है।",
          "ta": "பல தொழிலாளர்களால் ஒரு முழு தூதரகத்திற்கு எளிதாக பயணிக்க முடியாது என்பதால் இந்த மேசைகள் உள்ளன — தலைநகருக்குச் செல்ல வேண்டும் என்று கருதுவதற்கு முன், உங்கள் நகரத்தை ஏதேனும் ஒன்று உள்ளடக்குகிறதா என்று சரிபார்க்கவும்.",
          "te": "చాలా మంది కార్మికులు పూర్తి మిషన్‌కు సులభంగా ప్రయాణించలేరు కాబట్టి ఈ డెస్క్‌లు ఉన్నాయి — రాజధానికి వెళ్లాలని అనుకునే ముందు మీ నగరాన్ని ఏదైనా కవర్ చేస్తుందో లేదో తనిఖీ చేయండి.",
          "ml": "പല തൊഴിലാളികൾക്കും ഒരു മുഴുവൻ മിഷനിലേക്ക് എളുപ്പത്തിൽ യാത്ര ചെയ്യാൻ കഴിയാത്തതിനാലാണ് ഈ ഡെസ്കുകൾ ഉള്ളത് — തലസ്ഥാനത്തേക്ക് പോകണമെന്ന് കരുതുന്നതിന് മുമ്പ് നിങ്ങളുടെ നഗരം ഏതെങ്കിലും ഉൾക്കൊള്ളുന്നുണ്ടോ എന്ന് പരിശോധിക്കുക."},
    location={"en": "Selected missions in Gulf countries with large Indian worker populations",
               "hi": "बड़ी भारतीय कामगार आबादी वाले ख़ाड़ी देशों के चुनिंदा मिशन",
               "ta": "அதிக இந்திய தொழிலாளர் மக்கள்தொகை கொண்ட வளைகுடா நாடுகளில் தேர்ந்தெடுக்கப்பட்ட தூதரகங்கள்",
               "te": "పెద్ద భారతీయ కార్మిక జనాభా ఉన్న గల్ఫ్ దేశాలలో ఎంపిక చేసిన మిషన్లు",
               "ml": "വലിയ ഇന്ത്യൻ തൊഴിലാളി ജനസംഖ്യയുള്ള ഗൾഫ് രാജ്യങ്ങളിലെ തിരഞ്ഞെടുത്ത മിഷനുകൾ"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/owrc-and-pbsk.htm", "label": {"en": "↗ Kendra locations — mea.gov.in", "hi": "↗ केंद्र स्थान — mea.gov.in",
                                                                                     "ta": "↗ கேந்திரா இருப்பிடங்கள் — mea.gov.in", "te": "↗ కేంద్రం స్థానాలు — mea.gov.in", "ml": "↗ കേന്ദ്ര സ്ഥലങ്ങൾ — mea.gov.in"}}],
)

# ---- Documents & certification ----

entry(
    category="documents", badge_official=True,
    search_en="apostille attestation mea documents education degree",
    title={"en": "Apostille & attestation", "hi": "अपोस्टिल और सत्यापन", "ta": "அப்போஸ்டில் & சான்றளிப்பு", "te": "అపోస్టిల్ & ధృవీకరణ", "ml": "അപ്പോസ്റ്റിൽ, സാക്ഷ്യപ്പെടുത്തൽ"},
    desc={"en": "Degrees, marriage certificates and other Indian documents usually need an MEA apostille (for Hague Convention countries) or full attestation before a foreign government, employer or university will accept them.",
          "hi": "डिग्री, विवाह प्रमाणपत्र और अन्य भारतीय दस्तावेज़ों को किसी विदेशी सरकार, नियोक्ता या विश्वविद्यालय द्वारा स्वीकार किए जाने से पहले आमतौर पर MEA अपोस्टिल (हेग कन्वेंशन देशों के लिए) या पूर्ण सत्यापन की ज़रूरत होती है।",
          "ta": "பட்டங்கள், திருமண சான்றிதழ்கள் மற்றும் பிற இந்திய ஆவணங்களுக்கு பொதுவாக ஒரு வெளிநாட்டு அரசு, முதலாளி அல்லது பல்கலைக்கழகம் ஏற்றுக்கொள்வதற்கு முன் MEA அப்போஸ்டில் (ஹேக் ஒப்பந்த நாடுகளுக்கு) அல்லது முழு சான்றளிப்பு தேவை.",
          "te": "డిగ్రీలు, వివాహ ధృవపత్రాలు మరియు ఇతర భారతీయ పత్రాలకు సాధారణంగా విదేశీ ప్రభుత్వం, యజమాని లేదా విశ్వవిద్యాలయం అంగీకరించే ముందు MEA అపోస్టిల్ (హేగ్ ఒప్పంద దేశాల కోసం) లేదా పూర్తి ధృవీకరణ అవసరం.",
          "ml": "ബിരുദങ്ങൾ, വിവാഹ സർട്ടിഫിക്കറ്റുകൾ, മറ്റ് ഇന്ത്യൻ രേഖകൾ എന്നിവയ്ക്ക് സാധാരണയായി ഒരു വിദേശ സർക്കാരോ തൊഴിലുടമയോ സർവ്വകലാശാലയോ അംഗീകരിക്കുന്നതിന് മുമ്പ് MEA അപ്പോസ്റ്റിൽ (ഹേഗ് കൺവെൻഷൻ രാജ്യങ്ങൾക്ക്) അല്ലെങ്കിൽ പൂർണ്ണ സാക്ഷ്യപ്പെടുത്തൽ ആവശ്യമാണ്."},
    handles={"en": "education · personal · commercial docs", "hi": "शैक्षिक · व्यक्तिगत · वाणिज्यिक दस्तावेज़", "ta": "கல்வி · தனிப்பட்ட · வணிக ஆவணங்கள்",
             "te": "విద్య · వ్యక్తిగత · వాణిజ్య పత్రాలు", "ml": "വിദ്യാഭ്യാസം · വ്യക്തിഗതം · വാണിജ്യ രേഖകൾ"},
    steps={"en": ["Get the document attested at the right state-level authority first — the HRD department for education certificates, Home Department/GAD for personal certificates (birth, marriage, death), or the Chamber of Commerce for commercial documents.",
                  "Once state attestation is done, submit to an MEA-outsourced collection centre — MEA no longer takes walk-ins directly for most document types.",
                  "MEA affixes the apostille sticker and returns the document through the same centre."],
           "hi": ["पहले सही राज्य-स्तरीय प्राधिकरण से दस्तावेज़ सत्यापित कराएँ — शैक्षिक प्रमाणपत्रों के लिए HRD विभाग, व्यक्तिगत प्रमाणपत्रों (जन्म, विवाह, मृत्यु) के लिए गृह विभाग/GAD, या वाणिज्यिक दस्तावेज़ों के लिए वाणिज्य मंडल।",
                  "राज्य सत्यापन होने के बाद, MEA-आउटसोर्स संग्रह केंद्र में जमा करें — अधिकांश दस्तावेज़ प्रकारों के लिए MEA अब सीधे वॉक-इन नहीं लेता।",
                  "MEA अपोस्टिल स्टिकर लगाता है और उसी केंद्र के ज़रिए दस्तावेज़ लौटाता है।"],
           "ta": ["முதலில் சரியான மாநில-நிலை அதிகாரத்திடம் ஆவணத்தை சான்றளிக்கச் செய்யுங்கள் — கல்வி சான்றிதழ்களுக்கு HRD துறை, தனிப்பட்ட சான்றிதழ்களுக்கு (பிறப்பு, திருமணம், மரணம்) உள்துறை/GAD, அல்லது வணிக ஆவணங்களுக்கு வர்த்தக சபை.",
                  "மாநில சான்றளிப்பு முடிந்ததும், MEA-அவுட்சோர்ஸ் சேகரிப்பு மையத்தில் சமர்ப்பிக்கவும் — பெரும்பாலான ஆவண வகைகளுக்கு MEA இனி நேரடியாக வாக்-இன் ஏற்காது.",
                  "MEA அப்போஸ்டில் ஸ்டிக்கரை ஒட்டி அதே மையம் மூலம் ஆவணத்தைத் திருப்பி அளிக்கும்."],
           "te": ["మొదట సరైన రాష్ట్ర-స్థాయి అధికారి వద్ద పత్రాన్ని ధృవీకరించుకోండి — విద్యా ధృవపత్రాలకు HRD విభాగం, వ్యక్తిగత ధృవపత్రాలకు (జననం, వివాహం, మరణం) హోం విభాగం/GAD, లేదా వాణిజ్య పత్రాలకు చాంబర్ ఆఫ్ కామర్స్.",
                  "రాష్ట్ర ధృవీకరణ పూర్తయిన తర్వాత, MEA-అవుట్‌సోర్స్ కలెక్షన్ సెంటర్‌కు సమర్పించండి — చాలా పత్రాల రకాలకు MEA ఇక నేరుగా వాక్-ఇన్‌లను తీసుకోదు.",
                  "MEA అపోస్టిల్ స్టిక్కర్‌ను అతికించి అదే కేంద్రం ద్వారా పత్రాన్ని తిరిగి ఇస్తుంది."],
           "ml": ["ആദ്യം ശരിയായ സംസ്ഥാന-തല അധികാരിയിൽ രേഖ സാക്ഷ്യപ്പെടുത്തുക — വിദ്യാഭ്യാസ സർട്ടിഫിക്കറ്റുകൾക്ക് HRD വകുപ്പ്, വ്യക്തിഗത സർട്ടിഫിക്കറ്റുകൾക്ക് (ജനനം, വിവാഹം, മരണം) ഹോം വകുപ്പ്/GAD, അല്ലെങ്കിൽ വാണിജ്യ രേഖകൾക്ക് ചേംബർ ഓഫ് കൊമേഴ്‌സ്.",
                  "സംസ്ഥാന സാക്ഷ്യപ്പെടുത്തൽ കഴിഞ്ഞാൽ, MEA-ഔട്ട്‌സോഴ്‌സ് ശേഖരണ കേന്ദ്രത്തിൽ സമർപ്പിക്കുക — മിക്ക രേഖാ തരങ്ങൾക്കും MEA ഇനി നേരിട്ട് വാക്-ഇൻ സ്വീകരിക്കില്ല.",
                  "MEA അപ്പോസ്റ്റിൽ സ്റ്റിക്കർ പതിച്ച് അതേ കേന്ദ്രം വഴി രേഖ തിരികെ നൽകുന്നു."]},
    docs={"en": ["Original document plus a photocopy", "Passport copy and proof of address", "The state-attestation certificate from step 1"],
          "hi": ["मूल दस्तावेज़ और एक फ़ोटोकॉपी", "पासपोर्ट प्रति और पते का प्रमाण", "चरण 1 से राज्य-सत्यापन प्रमाणपत्र"],
          "ta": ["மூல ஆவணம் மற்றும் ஒரு நகல்", "பாஸ்போர்ட் நகல் மற்றும் முகவரி ஆதாரம்", "படி 1 இலிருந்து மாநில-சான்றளிப்பு சான்றிதழ்"],
          "te": ["అసలు పత్రం మరియు ఒక ఫోటోకాపీ", "పాస్‌పోర్ట్ కాపీ మరియు చిరునామా రుజువు", "దశ 1 నుండి రాష్ట్ర-ధృవీకరణ ధృవపత్రం"],
          "ml": ["ഒറിജിനൽ രേഖയും ഒരു ഫോട്ടോകോപ്പിയും", "പാസ്‌പോർട്ട് പകർപ്പും വിലാസ തെളിവും", "ഘട്ടം 1 ലെ സംസ്ഥാന-സാക്ഷ്യപ്പെടുത്തൽ സർട്ടിഫിക്കറ്റ്"]},
    note={"en": "An apostille only works for countries in the Hague Apostille Convention — for a non-member country you need full embassy attestation instead, a separate and longer process.",
          "hi": "अपोस्टिल केवल हेग अपोस्टिल कन्वेंशन के देशों के लिए काम करता है — ग़ैर-सदस्य देश के लिए इसके बजाय पूर्ण दूतावास सत्यापन चाहिए, जो अलग और लंबी प्रक्रिया है।",
          "ta": "அப்போஸ்டில் ஹேக் அப்போஸ்டில் ஒப்பந்த நாடுகளுக்கு மட்டுமே செயல்படும் — உறுப்பினர் அல்லாத நாட்டிற்கு அதற்கு பதிலாக முழு தூதரக சான்றளிப்பு தேவை, இது தனி மற்றும் நீண்ட செயல்முறை.",
          "te": "అపోస్టిల్ హేగ్ అపోస్టిల్ ఒప్పంద దేశాలకు మాత్రమే పనిచేస్తుంది — సభ్యేతర దేశానికి బదులుగా పూర్తి ఎంబసీ ధృవీకరణ అవసరం, ఇది వేరే మరియు సుదీర్ఘ ప్రక్రియ.",
          "ml": "അപ്പോസ്റ്റിൽ ഹേഗ് അപ്പോസ്റ്റിൽ കൺവെൻഷൻ രാജ്യങ്ങൾക്ക് മാത്രമേ പ്രവർത്തിക്കൂ — അംഗമല്ലാത്ത രാജ്യത്തിന് പകരം പൂർണ്ണ എംബസി സാക്ഷ്യപ്പെടുത്തൽ വേണം, ഇത് വേറിട്ടതും ദൈർഘ്യമേറിയതുമായ പ്രക്രിയയാണ്."},
    location={"en": "State attestation authority, then an MEA-outsourced collection centre", "hi": "राज्य सत्यापन प्राधिकरण, फिर MEA-आउटसोर्स संग्रह केंद्र",
               "ta": "மாநில சான்றளிப்பு அதிகாரம், பின்னர் MEA-அவுட்சோர்ஸ் சேகரிப்பு மையம்", "te": "రాష్ట్ర ధృవీకరణ అధికారి, తర్వాత MEA-అవుట్‌సోర్స్ కలెక్షన్ సెంటర్",
               "ml": "സംസ്ഥാന സാക്ഷ്യപ്പെടുത്തൽ അധികാരി, പിന്നീട് MEA-ഔട്ട്‌സോഴ്‌സ് ശേഖരണ കേന്ദ്രം"},
    phone=None, email=None,
    links=[{"href": "https://www.mea.gov.in/apostille-menu", "label": {"en": "↗ Apostille process — mea.gov.in", "hi": "↗ अपोस्टिल प्रक्रिया — mea.gov.in",
                                                                         "ta": "↗ அப்போஸ்டில் செயல்முறை — mea.gov.in", "te": "↗ అపోస్టిల్ ప్రక్రియ — mea.gov.in", "ml": "↗ അപ്പോസ്റ്റിൽ പ്രക്രിയ — mea.gov.in"}}],
)

entry(
    category="documents", badge_official=True,
    search_en="life certificate pensioners jeevan pramaan",
    title={"en": "Life certificate for pensioners", "hi": "पेंशनभोगियों के लिए जीवन प्रमाणपत्र", "ta": "ஓய்வூதியதாரர்களுக்கான வாழ்க்கை சான்றிதழ்", "te": "పింఛనుదారుల కోసం జీవన ధృవపత్రం", "ml": "പെൻഷൻകാർക്കുള്ള ജീവൻ സർട്ടിഫിക്കറ്റ്"},
    desc={"en": "NRI pensioners must submit an annual life certificate to keep an Indian pension running. It can be digitally verified through Jeevan Pramaan, or attested in person at a mission where digital verification isn't available.",
          "hi": "भारतीय पेंशन चालू रखने के लिए NRI पेंशनभोगियों को वार्षिक जीवन प्रमाणपत्र जमा करना ज़रूरी है। इसे Jeevan Pramaan के ज़रिए डिजिटल रूप से सत्यापित किया जा सकता है, या जहाँ डिजिटल सत्यापन उपलब्ध न हो वहाँ मिशन में व्यक्तिगत रूप से सत्यापित कराया जा सकता है।",
          "ta": "இந்திய ஓய்வூதியத்தை தொடர்ந்து பெற NRI ஓய்வூதியதாரர்கள் ஆண்டு வாழ்க்கை சான்றிதழை சமர்ப்பிக்க வேண்டும். இதை Jeevan Pramaan மூலம் டிஜிட்டல் முறையில் சரிபார்க்கலாம், அல்லது டிஜிட்டல் சரிபார்ப்பு இல்லாத இடத்தில் தூதரகத்தில் நேரில் சான்றளிக்கலாம்.",
          "te": "భారత పింఛన్ కొనసాగించడానికి NRI పింఛనుదారులు వార్షిక జీవన ధృవపత్రాన్ని సమర్పించాలి. దీన్ని Jeevan Pramaan ద్వారా డిజిటల్‌గా ధృవీకరించవచ్చు, లేదా డిజిటల్ ధృవీకరణ అందుబాటులో లేని చోట మిషన్‌లో వ్యక్తిగతంగా ధృవీకరించవచ్చు.",
          "ml": "ഇന്ത്യൻ പെൻഷൻ തുടരാൻ NRI പെൻഷൻകാർ വാർഷിക ജീവൻ സർട്ടിഫിക്കറ്റ് സമർപ്പിക്കണം. ഇത് Jeevan Pramaan വഴി ഡിജിറ്റലായി സ്ഥിരീകരിക്കാം, അല്ലെങ്കിൽ ഡിജിറ്റൽ സ്ഥിരീകരണം ലഭ്യമല്ലാത്തിടത്ത് ഒരു മിഷനിൽ നേരിട്ട് സാക്ഷ്യപ്പെടുത്താം."},
    handles={"en": "annual renewal · digital or in-person", "hi": "वार्षिक नवीनीकरण · डिजिटल या व्यक्तिगत", "ta": "ஆண்டு புதுப்பித்தல் · டிஜிட்டல் அல்லது நேரில்",
             "te": "వార్షిక పునరుద్ధరణ · డిజిటల్ లేదా వ్యక్తిగతంగా", "ml": "വാർഷിക പുതുക്കൽ · ഡിജിറ്റൽ അല്ലെങ്കിൽ നേരിട്ട്"},
    steps={"en": ["Simplest route: submit a Digital Life Certificate via Jeevan Pramaan using your Aadhaar number and registered mobile — no travel needed if this works for you.",
                  "If your pension-disbursing bank is on the RBI's approved list, its local branch or a bank officer abroad can sign the certificate instead.",
                  "Otherwise, get it signed by a notary, magistrate, banker, or Indian mission official, then send it to your pension-disbursing bank/authority in India yourself or through an authorised agent."],
           "hi": ["सबसे आसान तरीक़ा: अपने आधार नंबर और पंजीकृत मोबाइल का उपयोग करके Jeevan Pramaan के ज़रिए Digital Life Certificate जमा करें — अगर यह आपके लिए काम करे तो यात्रा की ज़रूरत नहीं।",
                  "अगर आपका पेंशन देने वाला बैंक RBI की स्वीकृत सूची में है, तो इसके बजाय उसकी स्थानीय शाखा या विदेश में बैंक अधिकारी प्रमाणपत्र पर हस्ताक्षर कर सकता है।",
                  "अन्यथा, इसे नोटरी, मजिस्ट्रेट, बैंकर, या भारतीय मिशन अधिकारी से हस्ताक्षरित कराएँ, फिर इसे स्वयं या अधिकृत एजेंट के ज़रिए भारत में अपने पेंशन देने वाले बैंक/प्राधिकरण को भेजें।"],
           "ta": ["எளிதான வழி: உங்கள் ஆதார் எண் மற்றும் பதிவு செய்யப்பட்ட மொபைலைப் பயன்படுத்தி Jeevan Pramaan மூலம் Digital Life Certificate ஐ சமர்ப்பிக்கவும் — இது உங்களுக்கு வேலை செய்தால் பயணம் தேவையில்லை.",
                  "உங்கள் ஓய்வூதியம் வழங்கும் வங்கி RBI இன் அங்கீகரிக்கப்பட்ட பட்டியலில் இருந்தால், அதற்கு பதிலாக அதன் உள்ளூர் கிளை அல்லது வெளிநாட்டில் உள்ள வங்கி அதிகாரி சான்றிதழில் கையெழுத்திடலாம்.",
                  "இல்லையெனில், நோட்டரி, மாஜிஸ்திரேட், வங்கியாளர், அல்லது இந்திய தூதரக அதிகாரி மூலம் கையெழுத்திடச் செய்து, பின்னர் அதை நீங்களே அல்லது அங்கீகரிக்கப்பட்ட முகவர் மூலம் இந்தியாவில் உங்கள் ஓய்வூதிய வங்கி/அதிகாரத்திற்கு அனுப்பவும்."],
           "te": ["సులభమైన మార్గం: మీ ఆధార్ నంబర్ మరియు నమోదిత మొబైల్ ఉపయోగించి Jeevan Pramaan ద్వారా Digital Life Certificate సమర్పించండి — ఇది మీకు పనిచేస్తే ప్రయాణం అవసరం లేదు.",
                  "మీ పింఛన్ చెల్లించే బ్యాంకు RBI ఆమోదించిన జాబితాలో ఉంటే, బదులుగా దాని స్థానిక శాఖ లేదా విదేశంలో ఉన్న బ్యాంకు అధికారి ధృవపత్రంపై సంతకం చేయవచ్చు.",
                  "లేకపోతే, దీన్ని నోటరీ, మేజిస్ట్రేట్, బ్యాంకర్, లేదా భారత మిషన్ అధికారి చేత సంతకం చేయించి, ఆపై దాన్ని మీరే లేదా అధీకృత ఏజెంట్ ద్వారా భారత్‌లోని మీ పింఛన్ చెల్లించే బ్యాంకు/అధికారానికి పంపండి."],
           "ml": ["ഏറ്റവും ലളിതമായ വഴി: നിങ്ങളുടെ ആധാർ നമ്പറും രജിസ്റ്റർ ചെയ്ത മൊബൈലും ഉപയോഗിച്ച് Jeevan Pramaan വഴി Digital Life Certificate സമർപ്പിക്കുക — ഇത് നിങ്ങൾക്ക് വേണ്ടിവന്നാൽ യാത്ര ആവശ്യമില്ല.",
                  "നിങ്ങളുടെ പെൻഷൻ നൽകുന്ന ബാങ്ക് RBI യുടെ അംഗീകൃത പട്ടികയിലാണെങ്കിൽ, പകരം അതിന്റെ പ്രാദേശിക ശാഖയോ വിദേശത്തുള്ള ബാങ്ക് ഉദ്യോഗസ്ഥനോ സർട്ടിഫിക്കറ്റിൽ ഒപ്പിടാം.",
                  "അല്ലെങ്കിൽ, ഇത് ഒരു നോട്ടറി, മജിസ്ട്രേറ്റ്, ബാങ്കർ, അല്ലെങ്കിൽ ഇന്ത്യൻ മിഷൻ ഉദ്യോഗസ്ഥൻ വഴി ഒപ്പിടുവിച്ച്, പിന്നീട് അത് നിങ്ങൾ തന്നെയോ അധികാരപ്പെടുത്തിയ ഏജന്റ് വഴിയോ ഇന്ത്യയിലെ നിങ്ങളുടെ പെൻഷൻ നൽകുന്ന ബാങ്ക്/അധികാരിക്ക് അയക്കുക."]},
    docs={"en": ["Aadhaar number linked to your pension account, and registered mobile number", "Or your Pension Payment Order (PPO) details, for the offline route"],
          "hi": ["आपके पेंशन खाते से जुड़ा आधार नंबर, और पंजीकृत मोबाइल नंबर", "या ऑफ़लाइन तरीक़े के लिए आपका Pension Payment Order (PPO) विवरण"],
          "ta": ["உங்கள் ஓய்வூதியக் கணக்குடன் இணைக்கப்பட்ட ஆதார் எண், மற்றும் பதிவு செய்யப்பட்ட மொபைல் எண்", "அல்லது ஆஃப்லைன் வழிக்கு உங்கள் Pension Payment Order (PPO) விவரங்கள்"],
          "te": ["మీ పింఛన్ ఖాతాకు లింక్ చేయబడిన ఆధార్ నంబర్, మరియు నమోదిత మొబైల్ నంబర్", "లేదా ఆఫ్‌లైన్ మార్గం కోసం మీ Pension Payment Order (PPO) వివరాలు"],
          "ml": ["നിങ്ങളുടെ പെൻഷൻ അക്കൗണ്ടുമായി ബന്ധിപ്പിച്ച ആധാർ നമ്പറും രജിസ്റ്റർ ചെയ്ത മൊബൈൽ നമ്പറും", "അല്ലെങ്കിൽ ഓഫ്‌ലൈൻ വഴിക്ക് നിങ്ങളുടെ Pension Payment Order (PPO) വിവരങ്ങൾ"]},
    note={"en": "This has to be done every year — missing it can pause your pension until it's submitted.",
          "hi": "यह हर साल करना ज़रूरी है — इसे न करने पर जमा होने तक आपकी पेंशन रुक सकती है।",
          "ta": "இது ஒவ்வொரு ஆண்டும் செய்யப்பட வேண்டும் — இதை தவற விட்டால் சமர்ப்பிக்கும் வரை உங்கள் ஓய்வூதியம் நிறுத்தப்படலாம்.",
          "te": "ఇది ప్రతి సంవత్సరం చేయాలి — దీన్ని మిస్ అయితే సమర్పించే వరకు మీ పింఛన్ ఆగిపోవచ్చు.",
          "ml": "ഇത് എല്ലാ വർഷവും ചെയ്യണം — ഇത് വിട്ടുപോയാൽ സമർപ്പിക്കുന്നത് വരെ നിങ്ങളുടെ പെൻഷൻ നിർത്തിവയ്ക്കാം."},
    location={"en": "Online (Jeevan Pramaan) or your mission / approved bank branch abroad",
               "hi": "ऑनलाइन (Jeevan Pramaan) या विदेश में आपका मिशन / स्वीकृत बैंक शाखा",
               "ta": "ஆன்லைன் (Jeevan Pramaan) அல்லது வெளிநாட்டில் உங்கள் தூதரகம் / அங்கீகரிக்கப்பட்ட வங்கி கிளை",
               "te": "ఆన్‌లైన్ (Jeevan Pramaan) లేదా విదేశంలో మీ మిషన్ / ఆమోదించబడిన బ్యాంకు శాఖ",
               "ml": "ഓൺലൈൻ (Jeevan Pramaan) അല്ലെങ്കിൽ വിദേശത്ത് നിങ്ങളുടെ മിഷൻ / അംഗീകൃത ബാങ്ക് ശാഖ"},
    phone=None, email=None,
    links=[{"href": "https://jeevanpramaan.gov.in", "label": {"en": "↗ Jeevan Pramaan — digital life certificate", "hi": "↗ Jeevan Pramaan — डिजिटल जीवन प्रमाणपत्र",
                                                                 "ta": "↗ Jeevan Pramaan — டிஜிட்டல் வாழ்க்கை சான்றிதழ்", "te": "↗ Jeevan Pramaan — డిజిటల్ జీవన ధృవపత్రం", "ml": "↗ Jeevan Pramaan — ഡിജിറ്റൽ ജീവൻ സർട്ടിഫിക്കറ്റ്"}}],
)

# ---- Voting rights ----

entry(
    category="voting", badge_official=True,
    search_en="nri overseas voter registration form 6a election commission",
    title={"en": "Register as an overseas elector", "hi": "प्रवासी मतदाता के रूप में पंजीकरण करें", "ta": "வெளிநாட்டு வாக்காளராக பதிவு செய்யவும்",
           "te": "విదేశీ ఓటరుగా నమోదు చేసుకోండి", "ml": "വിദേശ വോട്ടറായി രജിസ്റ്റർ ചെയ്യുക"},
    desc={"en": "Indian citizens who haven't taken another country's citizenship can register to vote from their home constituency using Form 6A on the Election Commission's portal — you still have to be physically present in India to cast the ballot.",
          "hi": "जिन भारतीय नागरिकों ने किसी अन्य देश की नागरिकता नहीं ली है, वे चुनाव आयोग के पोर्टल पर Form 6A का उपयोग करके अपने गृह निर्वाचन क्षेत्र से मतदान के लिए पंजीकरण कर सकते हैं — मतपत्र डालने के लिए फिर भी आपको भारत में शारीरिक रूप से मौजूद रहना होगा।",
          "ta": "மற்றொரு நாட்டின் குடியுரிமையை எடுக்காத இந்திய குடிமக்கள் தேர்தல் ஆணையத்தின் போர்ட்டலில் Form 6A ஐப் பயன்படுத்தி தங்கள் சொந்த தொகுதியிலிருந்து வாக்களிக்க பதிவு செய்யலாம் — வாக்களிக்க நீங்கள் இன்னும் இந்தியாவில் உடல் ரீதியாக இருக்க வேண்டும்.",
          "te": "మరొక దేశ పౌరసత్వం తీసుకోని భారత పౌరులు ఎన్నికల సంఘం పోర్టల్‌లో Form 6A ఉపయోగించి తమ స్వస్థల నియోజకవర్గం నుండి ఓటు వేయడానికి నమోదు చేసుకోవచ్చు — ఓటు వేయడానికి మీరు ఇప్పటికీ భారత్‌లో భౌతికంగా ఉండాలి.",
          "ml": "മറ്റൊരു രാജ്യത്തിന്റെ പൗരത്വം സ്വീകരിക്കാത്ത ഇന്ത്യൻ പൗരന്മാർക്ക് തിരഞ്ഞെടുപ്പ് കമ്മീഷന്റെ പോർട്ടലിൽ Form 6A ഉപയോഗിച്ച് സ്വന്തം മണ്ഡലത്തിൽ നിന്ന് വോട്ട് ചെയ്യാൻ രജിസ്റ്റർ ചെയ്യാം — വോട്ട് ചെയ്യാൻ നിങ്ങൾ ഇപ്പോഴും ഇന്ത്യയിൽ ശാരീരികമായി ഉണ്ടായിരിക്കണം."},
    handles={"en": "Form 6A · constituency mapping", "hi": "Form 6A · निर्वाचन क्षेत्र मानचित्रण", "ta": "Form 6A · தொகுதி வரைபடம்",
             "te": "Form 6A · నియోజకవర్గ మ్యాపింగ్", "ml": "Form 6A · മണ്ഡല മാപ്പിംഗ്"},
    steps={"en": ["Confirm you qualify: Indian citizen, 18 or older, and haven't taken another country's citizenship.",
                  "Get Form 6A from the Election Commission's site.",
                  "Fill in your passport details and the Indian address that determines your voting constituency.",
                  "Submit online via NVSP with scanned documents, or send/hand it to your nearest mission.",
                  "Once approved, you're added to the electoral roll for that constituency — you still vote in person at that specific polling station in India."],
           "hi": ["पुष्टि करें कि आप योग्य हैं: भारतीय नागरिक, 18 वर्ष या उससे अधिक, और किसी अन्य देश की नागरिकता नहीं ली हो।",
                  "चुनाव आयोग की साइट से Form 6A प्राप्त करें।",
                  "अपना पासपोर्ट विवरण और वह भारतीय पता भरें जो आपका मतदान निर्वाचन क्षेत्र तय करता है।",
                  "स्कैन किए गए दस्तावेज़ों के साथ NVSP के ज़रिए ऑनलाइन जमा करें, या अपने नज़दीकी मिशन को भेजें/सौंपें।",
                  "स्वीकृत होने पर, आपको उस निर्वाचन क्षेत्र की मतदाता सूची में जोड़ा जाता है — मतदान अभी भी आपको भारत के उस विशिष्ट मतदान केंद्र पर व्यक्तिगत रूप से करना होगा।"],
           "ta": ["நீங்கள் தகுதியுடையவரா என்பதை உறுதிப்படுத்தவும்: இந்திய குடிமகன், 18 அல்லது அதற்கு மேற்பட்டவர், மற்றும் மற்றொரு நாட்டின் குடியுரிமையை எடுக்காதவர்.",
                  "தேர்தல் ஆணையத்தின் தளத்திலிருந்து Form 6A ஐப் பெறவும்.",
                  "உங்கள் பாஸ்போர்ட் விவரங்கள் மற்றும் உங்கள் வாக்கு தொகுதியை நிர்ணயிக்கும் இந்திய முகவரியை நிரப்பவும்.",
                  "ஸ்கேன் செய்யப்பட்ட ஆவணங்களுடன் NVSP மூலம் ஆன்லைனில் சமர்ப்பிக்கவும், அல்லது உங்கள் அருகிலுள்ள தூதரகத்திற்கு அனுப்பவும்/கொடுக்கவும்.",
                  "அங்கீகரிக்கப்பட்டதும், நீங்கள் அந்த தொகுதியின் வாக்காளர் பட்டியலில் சேர்க்கப்படுவீர்கள் — வாக்களிக்க நீங்கள் இன்னும் இந்தியாவில் உள்ள அந்த குறிப்பிட்ட வாக்குச் சாவடியில் நேரில் செல்ல வேண்டும்."],
           "te": ["మీరు అర్హులో లేదో నిర్ధారించుకోండి: భారత పౌరుడు, 18 లేదా అంతకంటే ఎక్కువ వయస్సు, మరియు మరొక దేశ పౌరసత్వం తీసుకోలేదు.",
                  "ఎన్నికల సంఘం సైట్ నుండి Form 6A పొందండి.",
                  "మీ పాస్‌పోర్ట్ వివరాలు మరియు మీ ఓటింగ్ నియోజకవర్గాన్ని నిర్ణయించే భారతీయ చిరునామాను పూరించండి.",
                  "స్కాన్ చేసిన పత్రాలతో NVSP ద్వారా ఆన్‌లైన్‌లో సమర్పించండి, లేదా మీ సమీప మిషన్‌కు పంపండి/అందజేయండి.",
                  "ఆమోదించబడిన తర్వాత, మీరు ఆ నియోజకవర్గం యొక్క ఓటరు జాబితాలో చేర్చబడతారు — ఓటు వేయడానికి మీరు ఇప్పటికీ భారత్‌లోని ఆ నిర్దిష్ట పోలింగ్ స్టేషన్‌లో వ్యక్తిగతంగా వెళ్లాలి."],
           "ml": ["നിങ്ങൾ യോഗ്യനാണോ എന്ന് ഉറപ്പാക്കുക: ഇന്ത്യൻ പൗരൻ, 18 വയസ്സോ അതിൽ കൂടുതലോ, മറ്റൊരു രാജ്യത്തിന്റെ പൗരത്വം സ്വീകരിച്ചിട്ടില്ല.",
                  "തിരഞ്ഞെടുപ്പ് കമ്മീഷന്റെ സൈറ്റിൽ നിന്ന് Form 6A നേടുക.",
                  "നിങ്ങളുടെ പാസ്‌പോർട്ട് വിവരങ്ങളും നിങ്ങളുടെ വോട്ടിംഗ് മണ്ഡലം നിർണ്ണയിക്കുന്ന ഇന്ത്യൻ വിലാസവും പൂരിപ്പിക്കുക.",
                  "സ്കാൻ ചെയ്ത രേഖകളുമായി NVSP വഴി ഓൺലൈനിൽ സമർപ്പിക്കുക, അല്ലെങ്കിൽ നിങ്ങളുടെ അടുത്തുള്ള മിഷന് അയക്കുക/കൈമാറുക.",
                  "അംഗീകരിച്ചുകഴിഞ്ഞാൽ, നിങ്ങളെ ആ മണ്ഡലത്തിന്റെ വോട്ടർ പട്ടികയിൽ ചേർക്കും — വോട്ട് ചെയ്യാൻ നിങ്ങൾ ഇപ്പോഴും ഇന്ത്യയിലെ ആ പ്രത്യേക പോളിംഗ് സ്റ്റേഷനിൽ നേരിട്ട് പോകണം."]},
    docs={"en": ["Passport-size photo", "Self-attested passport pages (photo/detail page plus a valid visa page)"],
          "hi": ["पासपोर्ट साइज़ फ़ोटो", "स्व-सत्यापित पासपोर्ट पृष्ठ (फ़ोटो/विवरण पृष्ठ और वैध वीज़ा पृष्ठ)"],
          "ta": ["பாஸ்போர்ட் அளவு புகைப்படம்", "சுய-சான்றளிக்கப்பட்ட பாஸ்போர்ட் பக்கங்கள் (புகைப்படம்/விவர பக்கம் மற்றும் செல்லுபடியாகும் விசா பக்கம்)"],
          "te": ["పాస్‌పోర్ట్ సైజు ఫోటో", "స్వీయ-ధృవీకరించిన పాస్‌పోర్ట్ పేజీలు (ఫోటో/వివరాల పేజీ మరియు చెల్లుబాటు అయ్యే వీసా పేజీ)"],
          "ml": ["പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ", "സ്വയം സാക്ഷ്യപ്പെടുത്തിയ പാസ്‌പോർട്ട് പേജുകൾ (ഫോട്ടോ/വിവര പേജും സാധുവായ വിസ പേജും)"]},
    note={"en": "There's no postal or online voting for NRIs yet — registration only gets you onto the roll; casting the vote still means being physically present in India on polling day.",
          "hi": "NRI के लिए अभी तक कोई डाक या ऑनलाइन मतदान नहीं है — पंजीकरण से आप केवल सूची में शामिल होते हैं; मतदान के लिए अभी भी मतदान के दिन भारत में शारीरिक रूप से मौजूद होना होगा।",
          "ta": "NRI க்கு இன்னும் தபால் அல்லது ஆன்லைன் வாக்களிப்பு இல்லை — பதிவு உங்களை பட்டியலில் மட்டுமே சேர்க்கும்; வாக்களிப்பதற்கு வாக்குப்பதிவு நாளில் இந்தியாவில் உடல் ரீதியாக இருக்க வேண்டும்.",
          "te": "NRIల కోసం ఇంకా పోస్టల్ లేదా ఆన్‌లైన్ ఓటింగ్ లేదు — నమోదు మిమ్మల్ని జాబితాలో మాత్రమే చేరుస్తుంది; ఓటు వేయడానికి ఇప్పటికీ పోలింగ్ రోజున భారత్‌లో భౌతికంగా ఉండాలి.",
          "ml": "NRI കൾക്ക് ഇതുവരെ തപാൽ അല്ലെങ്കിൽ ഓൺലൈൻ വോട്ടിംഗ് ഇല്ല — രജിസ്ട്രേഷൻ നിങ്ങളെ പട്ടികയിൽ ഉൾപ്പെടുത്തുക മാത്രമേ ചെയ്യൂ; വോട്ട് ചെയ്യാൻ ഇപ്പോഴും പോളിംഗ് ദിവസം ഇന്ത്യയിൽ ശാരീരികമായി ഉണ്ടായിരിക്കണം."},
    location={"en": "Online (NVSP) or via your nearest Indian Mission", "hi": "ऑनलाइन (NVSP) या आपके नज़दीकी भारतीय मिशन के ज़रिए",
               "ta": "ஆன்லைன் (NVSP) அல்லது உங்கள் அருகிலுள்ள இந்திய தூதரகம் மூலம்", "te": "ఆన్‌లైన్ (NVSP) లేదా మీ సమీప భారత మిషన్ ద్వారా",
               "ml": "ഓൺലൈൻ (NVSP) അല്ലെങ്കിൽ നിങ്ങളുടെ അടുത്തുള്ള ഇന്ത്യൻ മിഷൻ വഴി"},
    phone=None, email=None,
    links=[
        {"href": "https://www.nvsp.in", "label": {"en": "↗ Register — nvsp.in", "hi": "↗ पंजीकरण करें — nvsp.in", "ta": "↗ பதிவு செய்யவும் — nvsp.in", "te": "↗ నమోదు చేసుకోండి — nvsp.in", "ml": "↗ രജിസ്റ്റർ ചെയ്യുക — nvsp.in"}},
        {"href": "https://eci.gov.in", "label": {"en": "↗ Election Commission of India", "hi": "↗ भारत निर्वाचन आयोग", "ta": "↗ இந்திய தேர்தல் ஆணையம்", "te": "↗ భారత ఎన్నికల సంఘం", "ml": "↗ ഇന്ത്യൻ തിരഞ്ഞെടുപ്പ് കമ്മീഷൻ"}},
    ],
)

# ---- Work & emigration ----

entry(
    category="work", badge_official=True,
    search_en="ecr emigration clearance emigrate portal gulf countries",
    title={"en": "Emigration clearance (ECR)", "hi": "उत्प्रवास मंज़ूरी (ECR)", "ta": "குடிபெயர்வு அனுமதி (ECR)", "te": "వలస అనుమతి (ECR)", "ml": "കുടിയേറ്റ അനുമതി (ECR)"},
    desc={"en": "Passport holders in the \"Emigration Check Required\" category need clearance before taking up work in a set list of countries, mostly in the Gulf. It's arranged online — no need to visit an emigration office in person.",
          "hi": "\"Emigration Check Required\" श्रेणी के पासपोर्ट धारकों को मुख्यतः ख़ाड़ी के कुछ निर्धारित देशों में काम शुरू करने से पहले मंज़ूरी चाहिए। यह ऑनलाइन व्यवस्थित है — व्यक्तिगत रूप से उत्प्रवास कार्यालय जाने की ज़रूरत नहीं।",
          "ta": "\"Emigration Check Required\" வகையிலான பாஸ்போர்ட் வைத்திருப்பவர்களுக்கு பெரும்பாலும் வளைகுடாவில் உள்ள ஒரு குறிப்பிட்ட நாடுகளின் பட்டியலில் வேலைக்குச் செல்வதற்கு முன் அனுமதி தேவை. இது ஆன்லைனில் ஏற்பாடு செய்யப்படுகிறது — நேரில் குடிபெயர்வு அலுவலகத்திற்குச் செல்ல வேண்டியதில்லை.",
          "te": "\"Emigration Check Required\" వర్గంలోని పాస్‌పోర్ట్ హోల్డర్లకు ఎక్కువగా గల్ఫ్‌లోని నిర్దిష్ట దేశాల జాబితాలో పని ప్రారంభించే ముందు అనుమతి అవసరం. ఇది ఆన్‌లైన్‌లో ఏర్పాటు చేయబడుతుంది — వ్యక్తిగతంగా వలస కార్యాలయాన్ని సందర్శించాల్సిన అవసరం లేదు.",
          "ml": "\"Emigration Check Required\" വിഭാഗത്തിലുള്ള പാസ്‌പോർട്ട് ഉടമകൾക്ക് കൂടുതലും ഗൾഫിലെ ഒരു നിശ്ചിത രാജ്യങ്ങളുടെ പട്ടികയിൽ ജോലി തുടങ്ങുന്നതിന് മുമ്പ് അനുമതി ആവശ്യമാണ്. ഇത് ഓൺലൈനിൽ ക്രമീകരിക്കുന്നു — നേരിട്ട് ഒരു കുടിയേറ്റ ഓഫീസ് സന്ദർശിക്കേണ്ട ആവശ്യമില്ല."},
    handles={"en": "ECR check · e-Migrate registration", "hi": "ECR जाँच · e-Migrate पंजीकरण", "ta": "ECR சரிபார்ப்பு · e-Migrate பதிவு",
             "te": "ECR తనిఖీ · e-Migrate నమోదు", "ml": "ECR പരിശോധന · e-Migrate രജിസ്ട്രേഷൻ"},
    steps={"en": ["Register a new account on emigrate.gov.in.",
                  "Buy Pravasi Bharatiya Bima Yojana (PBBY) insurance from an authorised insurer first — clearance can't be completed without a policy number.",
                  "Fill in job, employer and destination-country details exactly as they appear in your contract.",
                  "Upload your passport, visa, and signed employment contract.",
                  "Pay the processing fee online and wait for the Protector of Emigrants to review it.",
                  "Download your e-Sticker once approved — this is your emigration clearance."],
           "hi": ["emigrate.gov.in पर नया खाता पंजीकृत करें।",
                  "पहले किसी अधिकृत बीमाकर्ता से Pravasi Bharatiya Bima Yojana (PBBY) बीमा ख़रीदें — पॉलिसी नंबर के बिना मंज़ूरी पूरी नहीं हो सकती।",
                  "नौकरी, नियोक्ता और गंतव्य देश का विवरण बिल्कुल वैसे भरें जैसे आपके अनुबंध में हैं।",
                  "अपना पासपोर्ट, वीज़ा, और हस्ताक्षरित रोज़गार अनुबंध अपलोड करें।",
                  "ऑनलाइन प्रोसेसिंग शुल्क चुकाएँ और Protector of Emigrants द्वारा समीक्षा की प्रतीक्षा करें।",
                  "मंज़ूरी मिलने पर अपना e-Sticker डाउनलोड करें — यही आपकी उत्प्रवास मंज़ूरी है।"],
           "ta": ["emigrate.gov.in இல் புதிய கணக்கை பதிவு செய்யவும்.",
                  "முதலில் ஒரு அங்கீகரிக்கப்பட்ட காப்பீட்டாளரிடமிருந்து Pravasi Bharatiya Bima Yojana (PBBY) காப்பீட்டை வாங்கவும் — பாலிசி எண் இல்லாமல் அனுமதி முடிக்க முடியாது.",
                  "வேலை, முதலாளி மற்றும் இலக்கு நாடு விவரங்களை உங்கள் ஒப்பந்தத்தில் உள்ளபடியே சரியாக நிரப்பவும்.",
                  "உங்கள் பாஸ்போர்ட், விசா, மற்றும் கையொப்பமிடப்பட்ட வேலைவாய்ப்பு ஒப்பந்தத்தை பதிவேற்றவும்.",
                  "ஆன்லைனில் செயலாக்க கட்டணத்தை செலுத்தி Protector of Emigrants மதிப்பாய்வு செய்வதற்கு காத்திருக்கவும்.",
                  "அங்கீகரிக்கப்பட்டதும் உங்கள் e-Sticker ஐ பதிவிறக்கவும் — இதுவே உங்கள் குடிபெயர்வு அனுமதி."],
           "te": ["emigrate.gov.in లో కొత్త ఖాతాను నమోదు చేసుకోండి.",
                  "మొదట అధీకృత బీమా సంస్థ నుండి Pravasi Bharatiya Bima Yojana (PBBY) బీమాను కొనుగోలు చేయండి — పాలసీ నంబర్ లేకుండా అనుమతి పూర్తి కాదు.",
                  "ఉద్యోగం, యజమాని మరియు గమ్యస్థాన దేశ వివరాలను మీ ఒప్పందంలో ఉన్నట్లుగా ఖచ్చితంగా పూరించండి.",
                  "మీ పాస్‌పోర్ట్, వీసా, మరియు సంతకం చేసిన ఉద్యోగ ఒప్పందాన్ని అప్‌లోడ్ చేయండి.",
                  "ఆన్‌లైన్‌లో ప్రాసెసింగ్ రుసుము చెల్లించి Protector of Emigrants సమీక్ష కోసం వేచి ఉండండి.",
                  "ఆమోదించబడిన తర్వాత మీ e-Sticker డౌన్‌లోడ్ చేసుకోండి — ఇదే మీ వలస అనుమతి."],
           "ml": ["emigrate.gov.in ൽ പുതിയ അക്കൗണ്ട് രജിസ്റ്റർ ചെയ്യുക.",
                  "ആദ്യം ഒരു അംഗീകൃത ഇൻഷുറർ വഴി Pravasi Bharatiya Bima Yojana (PBBY) ഇൻഷുറൻസ് വാങ്ങുക — പോളിസി നമ്പർ ഇല്ലാതെ അനുമതി പൂർത്തിയാക്കാൻ കഴിയില്ല.",
                  "ജോലി, തൊഴിലുടമ, ലക്ഷ്യസ്ഥാന രാജ്യ വിവരങ്ങൾ നിങ്ങളുടെ കരാറിൽ ഉള്ളതുപോലെ കൃത്യമായി പൂരിപ്പിക്കുക.",
                  "നിങ്ങളുടെ പാസ്‌പോർട്ട്, വിസ, ഒപ്പിട്ട തൊഴിൽ കരാർ എന്നിവ അപ്‌ലോഡ് ചെയ്യുക.",
                  "ഓൺലൈനിൽ പ്രോസസ്സിംഗ് ഫീസ് അടച്ച് Protector of Emigrants അവലോകനത്തിനായി കാത്തിരിക്കുക.",
                  "അംഗീകരിച്ചുകഴിഞ്ഞാൽ നിങ്ങളുടെ e-Sticker ഡൗൺലോഡ് ചെയ്യുക — ഇതാണ് നിങ്ങളുടെ കുടിയേറ്റ അനുമതി."]},
    docs={"en": ["Passport scan and passport photo", "Visa copy and signed employment contract", "PBBY insurance policy number"],
          "hi": ["पासपोर्ट स्कैन और पासपोर्ट फ़ोटो", "वीज़ा प्रति और हस्ताक्षरित रोज़गार अनुबंध", "PBBY बीमा पॉलिसी नंबर"],
          "ta": ["பாஸ்போர்ட் ஸ்கேன் மற்றும் பாஸ்போர்ட் புகைப்படம்", "விசா நகல் மற்றும் கையொப்பமிடப்பட்ட வேலைவாய்ப்பு ஒப்பந்தம்", "PBBY காப்பீட்டு பாலிசி எண்"],
          "te": ["పాస్‌పోర్ట్ స్కాన్ మరియు పాస్‌పోర్ట్ ఫోటో", "వీసా కాపీ మరియు సంతకం చేసిన ఉద్యోగ ఒప్పందం", "PBBY బీమా పాలసీ నంబర్"],
          "ml": ["പാസ്‌പോർട്ട് സ്കാനും പാസ്‌പോർട്ട് ഫോട്ടോയും", "വിസ പകർപ്പും ഒപ്പിട്ട തൊഴിൽ കരാറും", "PBBY ഇൻഷുറൻസ് പോളിസി നമ്പർ"]},
    note={"en": "This only applies if your passport is marked ECR — check the back pages of your passport if you're not sure which category you're in.",
          "hi": "यह केवल तभी लागू होता है जब आपका पासपोर्ट ECR चिह्नित हो — अगर आपको यक़ीन नहीं कि आप किस श्रेणी में हैं तो पासपोर्ट के पिछले पृष्ठ जाँचें।",
          "ta": "உங்கள் பாஸ்போர்ட் ECR என்று குறிக்கப்பட்டிருந்தால் மட்டுமே இது பொருந்தும் — நீங்கள் எந்த வகையில் இருக்கிறீர்கள் என்று உறுதியில்லை என்றால் உங்கள் பாஸ்போர்ட்டின் பின் பக்கங்களை சரிபார்க்கவும்.",
          "te": "మీ పాస్‌పోర్ట్ ECR గుర్తు కలిగి ఉంటేనే ఇది వర్తిస్తుంది — మీరు ఏ వర్గంలో ఉన్నారో మీకు తెలియకపోతే మీ పాస్‌పోర్ట్ వెనుక పేజీలను తనిఖీ చేయండి.",
          "ml": "നിങ്ങളുടെ പാസ്‌പോർട്ട് ECR അടയാളപ്പെടുത്തിയിട്ടുണ്ടെങ്കിൽ മാത്രമേ ഇത് ബാധകമാകൂ — നിങ്ങൾ ഏത് വിഭാഗത്തിലാണെന്ന് ഉറപ്പില്ലെങ്കിൽ നിങ്ങളുടെ പാസ്‌പോർട്ടിന്റെ പിന്നിലെ പേജുകൾ പരിശോധിക്കുക."},
    location={"en": "Online (emigrate.gov.in) — no office visit needed", "hi": "ऑनलाइन (emigrate.gov.in) — कार्यालय जाने की ज़रूरत नहीं",
               "ta": "ஆன்லைன் (emigrate.gov.in) — அலுவலகம் செல்ல வேண்டியதில்லை", "te": "ఆన్‌లైన్ (emigrate.gov.in) — కార్యాలయాన్ని సందర్శించాల్సిన అవసరం లేదు",
               "ml": "ഓൺലൈൻ (emigrate.gov.in) — ഓഫീസ് സന്ദർശിക്കേണ്ട ആവശ്യമില്ല"},
    phone=None, email=None,
    links=[{"href": "https://emigrate.gov.in", "label": {"en": "↗ e-Migrate — emigrate.gov.in", "hi": "↗ e-Migrate — emigrate.gov.in", "ta": "↗ e-Migrate — emigrate.gov.in", "te": "↗ e-Migrate — emigrate.gov.in", "ml": "↗ e-Migrate — emigrate.gov.in"}}],
)

# ---- Tax & banking ----

entry(
    category="finance", badge_official=True,
    search_en="nri pan aadhaar linking income tax nre nro banking",
    title={"en": "PAN, tax filing & NRE/NRO basics", "hi": "PAN, कर दाख़िल करना और NRE/NRO मूल बातें", "ta": "PAN, வரி தாக்கல் & NRE/NRO அடிப்படைகள்",
           "te": "PAN, పన్ను ఫైలింగ్ & NRE/NRO ప్రాథమికాలు", "ml": "PAN, നികുതി ഫയലിംഗ്, NRE/NRO അടിസ്ഥാനങ്ങൾ"},
    desc={"en": "NRIs are generally exempt from mandatory PAN–Aadhaar linking, but rules have specific conditions worth checking directly. Indian income above the taxable threshold still needs a return filed, and savings held in India should sit in NRE/NRO accounts rather than a resident account.",
          "hi": "NRI आमतौर पर अनिवार्य PAN–आधार लिंकिंग से मुक्त हैं, लेकिन नियमों में विशिष्ट शर्तें हैं जिन्हें सीधे जाँचना उचित है। कर योग्य सीमा से अधिक भारतीय आय के लिए फिर भी रिटर्न दाख़िल करना ज़रूरी है, और भारत में रखी बचत को निवासी खाते के बजाय NRE/NRO खातों में रखना चाहिए।",
          "ta": "NRI கள் பொதுவாக கட்டாய PAN–ஆதார் இணைப்பிலிருந்து விலக்கு பெற்றுள்ளனர், ஆனால் விதிகளுக்கு நேரடியாக சரிபார்க்க வேண்டிய குறிப்பிட்ட நிபந்தனைகள் உள்ளன. வரி விதிக்கக்கூடிய வரம்பிற்கு மேல் இந்திய வருமானத்திற்கு இன்னும் ரிட்டர்ன் தாக்கல் செய்ய வேண்டும், மேலும் இந்தியாவில் வைத்திருக்கும் சேமிப்புகள் ஒரு குடியிருப்பாளர் கணக்கிற்குப் பதிலாக NRE/NRO கணக்குகளில் இருக்க வேண்டும்.",
          "te": "NRIలు సాధారణంగా తప్పనిసరి PAN–ఆధార్ లింకింగ్ నుండి మినహాయించబడ్డారు, కానీ నియమాలకు నేరుగా తనిఖీ చేయదగిన నిర్దిష్ట షరతులు ఉన్నాయి. పన్ను విధించదగిన పరిమితి కంటే ఎక్కువ భారతీయ ఆదాయానికి ఇప్పటికీ రిటర్న్ దాఖలు చేయాలి, మరియు భారత్‌లో ఉంచిన పొదుపులు నివాస ఖాతాకు బదులుగా NRE/NRO ఖాతాలలో ఉండాలి.",
          "ml": "NRI കൾ പൊതുവെ നിർബന്ധിത PAN–ആധാർ ലിങ്കിംഗിൽ നിന്ന് ഒഴിവാക്കപ്പെട്ടിരിക്കുന്നു, എന്നാൽ നിയമങ്ങൾക്ക് നേരിട്ട് പരിശോധിക്കേണ്ട പ്രത്യേക നിബന്ധനകളുണ്ട്. നികുതി പരിധിക്ക് മുകളിലുള്ള ഇന്ത്യൻ വരുമാനത്തിന് ഇപ്പോഴും റിട്ടേൺ ഫയൽ ചെയ്യേണ്ടതുണ്ട്, ഇന്ത്യയിൽ സൂക്ഷിച്ചിരിക്കുന്ന സമ്പാദ്യം ഒരു റെസിഡന്റ് അക്കൗണ്ടിന് പകരം NRE/NRO അക്കൗണ്ടുകളിൽ ആയിരിക്കണം."},
    handles={"en": "PAN status · e-filing · FEMA banking rules", "hi": "PAN स्थिति · ई-फ़ाइलिंग · FEMA बैंकिंग नियम", "ta": "PAN நிலை · மின்-தாக்கல் · FEMA வங்கி விதிகள்",
             "te": "PAN స్థితి · ఇ-ఫైలింగ్ · FEMA బ్యాంకింగ్ నియమాలు", "ml": "PAN സ്റ്റാറ്റസ് · ഇ-ഫയലിംഗ് · FEMA ബാങ്കിംഗ് നിയമങ്ങൾ"},
    steps={"en": ["Confirm your NRI/residential status for the tax year — this determines what income is taxable in India and whether PAN–Aadhaar linking applies to you.",
                  "If you have taxable Indian income, log in at the Income Tax e-filing portal with your PAN and file the applicable ITR form before the deadline.",
                  "Open an NRE account (for foreign earnings, fully repatriable) and/or an NRO account (for Indian-sourced income) with a bank offering NRI banking — most accept video KYC, some still require a branch visit.",
                  "Convert any existing resident savings account to NRO once your status changes — holding a regular resident account as an NRI isn't compliant."],
           "hi": ["कर वर्ष के लिए अपनी NRI/निवासी स्थिति की पुष्टि करें — यह तय करता है कि भारत में कौन-सी आय कर योग्य है और क्या PAN–आधार लिंकिंग आप पर लागू होती है।",
                  "अगर आपकी कर योग्य भारतीय आय है, तो अपने PAN से Income Tax e-filing पोर्टल पर लॉग इन करें और समय सीमा से पहले लागू ITR फ़ॉर्म दाख़िल करें।",
                  "NRI बैंकिंग देने वाले बैंक में NRE खाता (विदेशी कमाई के लिए, पूर्ण प्रत्यावर्तनीय) और/या NRO खाता (भारतीय स्रोत की आय के लिए) खोलें — अधिकांश वीडियो KYC स्वीकार करते हैं, कुछ को अभी भी शाखा जाने की ज़रूरत होती है।",
                  "स्थिति बदलते ही किसी भी मौजूदा निवासी बचत खाते को NRO में बदलें — NRI के रूप में सामान्य निवासी खाता रखना नियमानुसार नहीं है।"],
           "ta": ["வரி ஆண்டிற்கான உங்கள் NRI/குடியிருப்பு நிலையை உறுதிப்படுத்தவும் — இது இந்தியாவில் எந்த வருமானம் வரி விதிக்கப்படுகிறது மற்றும் PAN–ஆதார் இணைப்பு உங்களுக்கு பொருந்துமா என்பதை தீர்மானிக்கிறது.",
                  "உங்களிடம் வரி விதிக்கக்கூடிய இந்திய வருமானம் இருந்தால், உங்கள் PAN உடன் Income Tax e-filing போர்ட்டலில் உள்நுழைந்து காலக்கெடுவிற்கு முன் பொருந்தும் ITR படிவத்தை தாக்கல் செய்யவும்.",
                  "NRI வங்கி வழங்கும் வங்கியில் NRE கணக்கு (வெளிநாட்டு வருமானத்திற்கு, முழுமையாக திரும்ப அனுப்பக்கூடியது) மற்றும்/அல்லது NRO கணக்கு (இந்திய மூல வருமானத்திற்கு) திறக்கவும் — பெரும்பாலானவை வீடியோ KYC ஐ ஏற்கின்றன, சில இன்னும் கிளை வருகை தேவை.",
                  "உங்கள் நிலை மாறியதும் ஏதேனும் தற்போதைய குடியிருப்பாளர் சேமிப்புக் கணக்கை NRO ஆக மாற்றவும் — NRI ஆக இருக்கும்போது வழக்கமான குடியிருப்பாளர் கணக்கை வைத்திருப்பது விதிமுறைக்கு உட்பட்டதல்ல."],
           "te": ["పన్ను సంవత్సరానికి మీ NRI/నివాస స్థితిని నిర్ధారించుకోండి — ఇది భారత్‌లో ఏ ఆదాయం పన్ను విధించదగినదో మరియు PAN–ఆధార్ లింకింగ్ మీకు వర్తిస్తుందో లేదో నిర్ణయిస్తుంది.",
                  "మీకు పన్ను విధించదగిన భారతీయ ఆదాయం ఉంటే, మీ PAN తో Income Tax e-filing పోర్టల్‌లో లాగిన్ అయి గడువులోపు వర్తించే ITR ఫారంను దాఖలు చేయండి.",
                  "NRI బ్యాంకింగ్ అందించే బ్యాంకులో NRE ఖాతా (విదేశీ ఆదాయం కోసం, పూర్తిగా తిరిగి తీసుకోగలిగేది) మరియు/లేదా NRO ఖాతా (భారతీయ మూలం ఆదాయం కోసం) తెరవండి — చాలా వరకు వీడియో KYC ని అంగీకరిస్తాయి, కొన్నింటికి ఇప్పటికీ శాఖ సందర్శన అవసరం.",
                  "మీ స్థితి మారిన వెంటనే ఏదైనా ప్రస్తుత నివాస పొదుపు ఖాతాను NRO గా మార్చండి — NRI గా సాధారణ నివాస ఖాతాను ఉంచుకోవడం నిబంధనలకు అనుగుణంగా ఉండదు."],
           "ml": ["നികുതി വർഷത്തേക്കുള്ള നിങ്ങളുടെ NRI/റെസിഡന്റ് സ്റ്റാറ്റസ് സ്ഥിരീകരിക്കുക — ഇത് ഇന്ത്യയിൽ ഏത് വരുമാനമാണ് നികുതി വിധേയമെന്നും PAN–ആധാർ ലിങ്കിംഗ് നിങ്ങൾക്ക് ബാധകമാണോ എന്നും നിർണ്ണയിക്കുന്നു.",
                  "നിങ്ങൾക്ക് നികുതി വിധേയമായ ഇന്ത്യൻ വരുമാനം ഉണ്ടെങ്കിൽ, നിങ്ങളുടെ PAN ഉപയോഗിച്ച് Income Tax e-filing പോർട്ടലിൽ ലോഗിൻ ചെയ്ത് സമയപരിധിക്ക് മുമ്പ് ബാധകമായ ITR ഫോം ഫയൽ ചെയ്യുക.",
                  "NRI ബാങ്കിംഗ് നൽകുന്ന ബാങ്കിൽ NRE അക്കൗണ്ട് (വിദേശ വരുമാനത്തിന്, പൂർണ്ണമായും തിരിച്ചയക്കാവുന്നത്) കൂടാതെ/അല്ലെങ്കിൽ NRO അക്കൗണ്ട് (ഇന്ത്യൻ ഉറവിട വരുമാനത്തിന്) തുറക്കുക — മിക്കതും വീഡിയോ KYC സ്വീകരിക്കുന്നു, ചിലതിന് ഇപ്പോഴും ബ്രാഞ്ച് സന്ദർശനം ആവശ്യമാണ്.",
                  "നിങ്ങളുടെ സ്റ്റാറ്റസ് മാറിക്കഴിഞ്ഞാൽ നിലവിലുള്ള ഏതെങ്കിലും റെസിഡന്റ് സേവിംഗ്സ് അക്കൗണ്ട് NRO ആക്കി മാറ്റുക — NRI ആയിരിക്കുമ്പോൾ ഒരു സാധാരണ റെസിഡന്റ് അക്കൗണ്ട് കൈവശം വയ്ക്കുന്നത് നിയമാനുസൃതമല്ല."]},
    docs={"en": ["PAN and passport", "Overseas address proof and visa/residence permit copy", "Passport photos", "For tax filing: income details and any foreign tax paid, for DTAA relief"],
          "hi": ["PAN और पासपोर्ट", "विदेशी पते का प्रमाण और वीज़ा/निवास परमिट की प्रति", "पासपोर्ट फ़ोटो", "कर दाख़िल करने के लिए: आय विवरण और DTAA राहत हेतु कोई विदेशी कर चुकाया गया हो तो उसका विवरण"],
          "ta": ["PAN மற்றும் பாஸ்போர்ட்", "வெளிநாட்டு முகவரி ஆதாரம் மற்றும் விசா/குடியிருப்பு அனுமதி நகல்", "பாஸ்போர்ட் புகைப்படங்கள்", "வரி தாக்கலுக்கு: வருமான விவரங்கள் மற்றும் DTAA நிவாரணத்திற்கு ஏதேனும் வெளிநாட்டு வரி செலுத்தப்பட்டிருந்தால் அதன் விவரம்"],
          "te": ["PAN మరియు పాస్‌పోర్ట్", "విదేశీ చిరునామా రుజువు మరియు వీసా/నివాస అనుమతి కాపీ", "పాస్‌పోర్ట్ ఫోటోలు", "పన్ను ఫైలింగ్ కోసం: ఆదాయ వివరాలు మరియు DTAA ఉపశమనం కోసం చెల్లించిన ఏదైనా విదేశీ పన్ను"],
          "ml": ["PAN ഉം പാസ്‌പോർട്ടും", "വിദേശ വിലാസ തെളിവും വിസ/റെസിഡൻസ് പെർമിറ്റ് പകർപ്പും", "പാസ്‌പോർട്ട് ഫോട്ടോകൾ", "നികുതി ഫയലിംഗിന്: വരുമാന വിവരങ്ങളും DTAA ഇളവിന് അടച്ച ഏതെങ്കിലും വിദേശ നികുതിയും"]},
    note={"en": "Rules on PAN–Aadhaar linking and taxable thresholds change fairly often — check the e-filing portal directly rather than going by an old article.",
          "hi": "PAN–आधार लिंकिंग और कर योग्य सीमा के नियम काफ़ी बार बदलते हैं — किसी पुराने लेख के बजाय सीधे e-filing पोर्टल जाँचें।",
          "ta": "PAN–ஆதார் இணைப்பு மற்றும் வரி விதிக்கக்கூடிய வரம்புகள் பற்றிய விதிகள் அடிக்கடி மாறுகின்றன — ஒரு பழைய கட்டுரையை நம்புவதற்குப் பதிலாக நேரடியாக e-filing போர்ட்டலைச் சரிபார்க்கவும்.",
          "te": "PAN–ఆధార్ లింకింగ్ మరియు పన్ను విధించదగిన పరిమితులపై నియమాలు చాలా తరచుగా మారుతుంటాయి — పాత ఆర్టికల్ ఆధారంగా కాకుండా నేరుగా e-filing పోర్టల్‌ను తనిఖీ చేయండి.",
          "ml": "PAN–ആധാർ ലിങ്കിംഗിനെയും നികുതി പരിധികളെയും കുറിച്ചുള്ള നിയമങ്ങൾ വളരെ പതിവായി മാറുന്നു — ഒരു പഴയ ലേഖനം അടിസ്ഥാനമാക്കാതെ നേരിട്ട് e-filing പോർട്ടൽ പരിശോധിക്കുക."},
    location={"en": "Online (Income Tax e-filing portal) + your NRI-banking branch", "hi": "ऑनलाइन (Income Tax e-filing पोर्टल) + आपकी NRI-बैंकिंग शाखा",
               "ta": "ஆன்லைன் (Income Tax e-filing போர்ட்டல்) + உங்கள் NRI-வங்கி கிளை", "te": "ఆన్‌లైన్ (Income Tax e-filing పోర్టల్) + మీ NRI-బ్యాంకింగ్ శాఖ",
               "ml": "ഓൺലൈൻ (Income Tax e-filing പോർട്ടൽ) + നിങ്ങളുടെ NRI-ബാങ്കിംഗ് ബ്രാഞ്ച്"},
    phone=None, email=None,
    links=[
        {"href": "https://www.incometax.gov.in", "label": {"en": "↗ Income Tax e-filing portal", "hi": "↗ Income Tax e-filing पोर्टल", "ta": "↗ Income Tax e-filing போர்ட்டல்", "te": "↗ Income Tax e-filing పోర్టల్", "ml": "↗ Income Tax e-filing പോർട്ടൽ"}},
        {"href": "https://www.rbi.org.in", "label": {"en": "↗ RBI — NRI account & FEMA rules", "hi": "↗ RBI — NRI खाता और FEMA नियम", "ta": "↗ RBI — NRI கணக்கு & FEMA விதிகள்", "te": "↗ RBI — NRI ఖాతా & FEMA నియమాలు", "ml": "↗ RBI — NRI അക്കൗണ്ട്, FEMA നിയമങ്ങൾ"}},
    ],
)

# ---- Singapore: Immigration & ID ----

entry(
    category="sg_immigration", country="singapore", badge_official=True, passes=["EP", "SPass"],
    search_en="singapore employment pass s pass fin collection ica mom work permit",
    title={"en": "Collect your Employment/S Pass & FIN", "hi": "अपना Employment/S Pass और FIN प्राप्त करें", "ta": "உங்கள் Employment/S Pass மற்றும் FIN ஐப் பெறவும்",
           "te": "మీ Employment/S Pass & FIN తీసుకోండి", "ml": "നിങ്ങളുടെ Employment/S Pass, FIN എന്നിവ വാങ്ങുക"},
    desc={"en": "Once MOM approves your In-Principle Approval (IPA) and you land in Singapore, you collect the physical work pass card, which carries your FIN — the ID number almost every other Singapore service (bank, SingPass, phone line) will ask for. Dependants joining on a Dependant's Pass go through a separate ICA registration step.",
          "hi": "जब MOM आपकी In-Principle Approval (IPA) मंज़ूर कर देता है और आप सिंगापुर पहुँचते हैं, तो आप भौतिक वर्क पास कार्ड प्राप्त करते हैं, जिस पर आपका FIN होता है — यह पहचान संख्या लगभग हर दूसरी सिंगापुर सेवा (बैंक, SingPass, फ़ोन लाइन) माँगेगी। Dependant's Pass पर जुड़ने वाले आश्रितों को एक अलग ICA पंजीकरण चरण से गुज़रना होता है।",
          "ta": "MOM உங்கள் In-Principle Approval (IPA) ஐ அங்கீகரித்து நீங்கள் சிங்கப்பூரில் இறங்கியதும், உங்கள் FIN ஐ கொண்ட உடல் ரீதியான வேலை பாஸ் அட்டையை பெறுவீர்கள் — இந்த அடையாள எண்ணை கிட்டத்தட்ட மற்ற ஒவ்வொரு சிங்கப்பூர் சேவையும் (வங்கி, SingPass, தொலைபேசி இணைப்பு) கேட்கும். Dependant's Pass இல் சேரும் சார்ந்தோர் தனி ICA பதிவு படியை கடக்க வேண்டும்.",
          "te": "MOM మీ In-Principle Approval (IPA) ఆమోదించి మీరు సింగపూర్‌లో దిగిన తర్వాత, మీ FIN ఉన్న భౌతిక వర్క్ పాస్ కార్డును తీసుకుంటారు — దాదాపు ప్రతి ఇతర సింగపూర్ సేవ (బ్యాంకు, SingPass, ఫోన్ లైన్) ఈ గుర్తింపు నంబర్‌ను అడుగుతుంది. Dependant's Pass పై చేరే డిపెండెంట్లు వేరే ICA నమోదు దశ ద్వారా వెళ్తారు.",
          "ml": "MOM നിങ്ങളുടെ In-Principle Approval (IPA) അംഗീകരിച്ച് നിങ്ങൾ സിംഗപ്പൂരിൽ ഇറങ്ങിക്കഴിഞ്ഞാൽ, നിങ്ങളുടെ FIN ഉള്ള ഫിസിക്കൽ വർക്ക് പാസ് കാർഡ് വാങ്ങുന്നു — മിക്കവാറും എല്ലാ മറ്റ് സിംഗപ്പൂർ സേവനങ്ങളും (ബാങ്ക്, SingPass, ഫോൺ ലൈൻ) ഈ ഐഡി നമ്പർ ചോദിക്കും. Dependant's Pass ൽ ചേരുന്ന ആശ്രിതർ വേറൊരു ICA രജിസ്ട്രേഷൻ ഘട്ടത്തിലൂടെ കടന്നുപോകണം."},
    handles={"en": "IPA → pass collection · FIN · dependant registration", "hi": "IPA → पास संग्रह · FIN · आश्रित पंजीकरण",
             "ta": "IPA → பாஸ் சேகரிப்பு · FIN · சார்ந்தோர் பதிவு", "te": "IPA → పాస్ సేకరణ · FIN · డిపెండెంట్ నమోదు", "ml": "IPA → പാസ് ശേഖരണം · FIN · ആശ്രിത രജിസ്ട്രേഷൻ"},
    steps={"en": ["Before travelling, your employer applies for the pass and you receive an In-Principle Approval (IPA) letter — check its validity window and any medical-check condition.",
                  "Enter Singapore within the IPA's validity period, carrying the IPA letter and a passport-size photo.",
                  "Collect the pass card in person at MOM's Employment Pass Services Centre once your employer notifies you it's ready — bring your passport and the IPA letter.",
                  "Your FIN is printed on the card — save it, you'll need it for SingPass, banking, telco and more.",
                  "If your spouse/children are joining on a Dependant's Pass or Long-Term Visit Pass, they register separately with ICA after arrival."],
           "hi": ["यात्रा से पहले, आपका नियोक्ता पास के लिए आवेदन करता है और आपको In-Principle Approval (IPA) पत्र मिलता है — इसकी वैधता अवधि और किसी मेडिकल-जाँच शर्त की जाँच करें।",
                  "IPA की वैधता अवधि के भीतर IPA पत्र और पासपोर्ट साइज़ फ़ोटो के साथ सिंगापुर में प्रवेश करें।",
                  "नियोक्ता द्वारा तैयार होने की सूचना मिलने पर MOM के Employment Pass Services Centre में व्यक्तिगत रूप से पास कार्ड लें — अपना पासपोर्ट और IPA पत्र साथ लाएँ।",
                  "आपका FIN कार्ड पर छपा होता है — इसे सहेजें, SingPass, बैंकिंग, टेल्को और अन्य के लिए ज़रूरत होगी।",
                  "अगर आपका जीवनसाथी/बच्चे Dependant's Pass या Long-Term Visit Pass पर जुड़ रहे हैं, तो वे पहुँचने के बाद अलग से ICA में पंजीकरण कराते हैं।"],
           "ta": ["பயணத்திற்கு முன், உங்கள் முதலாளி பாஸிற்கு விண்ணப்பித்து உங்களுக்கு In-Principle Approval (IPA) கடிதம் கிடைக்கும் — அதன் செல்லுபடி காலம் மற்றும் ஏதேனும் மருத்துவ-பரிசோதனை நிபந்தனையை சரிபார்க்கவும்.",
                  "IPA இன் செல்லுபடி காலத்திற்குள் IPA கடிதம் மற்றும் பாஸ்போர்ட் அளவு புகைப்படத்துடன் சிங்கப்பூரில் நுழையவும்.",
                  "உங்கள் முதலாளி தயார் என்று தெரிவித்ததும் MOM இன் Employment Pass Services Centre இல் நேரில் பாஸ் அட்டையை பெறவும் — உங்கள் பாஸ்போர்ட் மற்றும் IPA கடிதத்தை கொண்டு வரவும்.",
                  "உங்கள் FIN அட்டையில் அச்சிடப்பட்டுள்ளது — அதை சேமிக்கவும், SingPass, வங்கி, டெல்கோ மற்றும் பலவற்றிற்கு தேவைப்படும்.",
                  "உங்கள் வாழ்க்கைத் துணைவர்/குழந்தைகள் Dependant's Pass அல்லது Long-Term Visit Pass இல் சேர்ந்தால், அவர்கள் வந்த பிறகு தனியாக ICA இல் பதிவு செய்ய வேண்டும்."],
           "te": ["ప్రయాణానికి ముందు, మీ యజమాని పాస్ కోసం దరఖాస్తు చేసి మీకు In-Principle Approval (IPA) లేఖ లభిస్తుంది — దాని చెల్లుబాటు వ్యవధి మరియు ఏదైనా వైద్య-పరీక్ష షరతును తనిఖీ చేయండి.",
                  "IPA చెల్లుబాటు వ్యవధిలోపు IPA లేఖ మరియు పాస్‌పోర్ట్ సైజు ఫోటోతో సింగపూర్‌లోకి ప్రవేశించండి.",
                  "మీ యజమాని సిద్ధమని తెలియజేసిన తర్వాత MOM యొక్క Employment Pass Services Centre వద్ద వ్యక్తిగతంగా పాస్ కార్డును తీసుకోండి — మీ పాస్‌పోర్ట్ మరియు IPA లేఖను తీసుకురండి.",
                  "మీ FIN కార్డుపై ముద్రించబడి ఉంటుంది — దాన్ని సేవ్ చేసుకోండి, SingPass, బ్యాంకింగ్, టెల్కో మరియు మరిన్నింటికి అవసరం.",
                  "మీ జీవిత భాగస్వామి/పిల్లలు Dependant's Pass లేదా Long-Term Visit Pass పై చేరుతుంటే, వారు వచ్చిన తర్వాత విడిగా ICA లో నమోదు చేసుకుంటారు."],
           "ml": ["യാത്രയ്ക്ക് മുമ്പ്, നിങ്ങളുടെ തൊഴിലുടമ പാസിന് അപേക്ഷിക്കുകയും നിങ്ങൾക്ക് In-Principle Approval (IPA) കത്ത് ലഭിക്കുകയും ചെയ്യും — അതിന്റെ സാധുതാ കാലയളവും ഏതെങ്കിലും മെഡിക്കൽ-പരിശോധന വ്യവസ്ഥയും പരിശോധിക്കുക.",
                  "IPA യുടെ സാധുതാ കാലയളവിനുള്ളിൽ IPA കത്തും പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോയുമായി സിംഗപ്പൂരിൽ പ്രവേശിക്കുക.",
                  "നിങ്ങളുടെ തൊഴിലുടമ തയ്യാറാണെന്ന് അറിയിച്ചുകഴിഞ്ഞാൽ MOM ന്റെ Employment Pass Services Centre ൽ നേരിട്ട് പാസ് കാർഡ് വാങ്ങുക — നിങ്ങളുടെ പാസ്‌പോർട്ടും IPA കത്തും കൊണ്ടുവരിക.",
                  "നിങ്ങളുടെ FIN കാർഡിൽ അച്ചടിച്ചിരിക്കുന്നു — അത് സേവ് ചെയ്യുക, SingPass, ബാങ്കിംഗ്, ടെൽകോ എന്നിവയ്ക്കും മറ്റും ആവശ്യമാണ്.",
                  "നിങ്ങളുടെ ജീവിതപങ്കാളി/കുട്ടികൾ Dependant's Pass അല്ലെങ്കിൽ Long-Term Visit Pass ൽ ചേരുകയാണെങ്കിൽ, അവർ എത്തിയ ശേഷം പ്രത്യേകം ICA യിൽ രജിസ്റ്റർ ചെയ്യണം."]},
    docs={"en": ["In-Principle Approval (IPA) letter", "Passport (original)", "Passport-size photo", "Any medical exam report if MOM required one"],
          "hi": ["In-Principle Approval (IPA) पत्र", "पासपोर्ट (मूल)", "पासपोर्ट साइज़ फ़ोटो", "अगर MOM ने माँगी हो तो कोई मेडिकल जाँच रिपोर्ट"],
          "ta": ["In-Principle Approval (IPA) கடிதம்", "பாஸ்போர்ட் (மூலம்)", "பாஸ்போர்ட் அளவு புகைப்படம்", "MOM கேட்டிருந்தால் ஏதேனும் மருத்துவ பரிசோதனை அறிக்கை"],
          "te": ["In-Principle Approval (IPA) లేఖ", "పాస్‌పోర్ట్ (అసలు)", "పాస్‌పోర్ట్ సైజు ఫోటో", "MOM అడిగితే ఏదైనా వైద్య పరీక్ష నివేదిక"],
          "ml": ["In-Principle Approval (IPA) കത്ത്", "പാസ്‌പോർട്ട് (ഒറിജിനൽ)", "പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ", "MOM ആവശ്യപ്പെട്ടെങ്കിൽ ഏതെങ്കിലും മെഡിക്കൽ പരിശോധന റിപ്പോർട്ട്"]},
    note={"en": "Your employer handles the application itself — this card is only about what you personally need to do once you land. Keep the physical pass card on you; it doubles as your day-to-day ID in Singapore.",
          "hi": "आवेदन आपका नियोक्ता ख़ुद संभालता है — यह कार्ड सिर्फ़ इस बारे में है कि पहुँचने के बाद आपको व्यक्तिगत रूप से क्या करना है। भौतिक पास कार्ड अपने पास रखें; यह सिंगापुर में आपकी रोज़मर्रा की पहचान भी है।",
          "ta": "விண்ணப்பத்தை உங்கள் முதலாளியே கையாள்கிறார் — இந்த அட்டை நீங்கள் தனிப்பட்ட முறையில் இறங்கியதும் என்ன செய்ய வேண்டும் என்பது பற்றியது மட்டுமே. உடல் ரீதியான பாஸ் அட்டையை உங்களிடம் வைத்திருங்கள்; இது சிங்கப்பூரில் உங்கள் அன்றாட அடையாள அட்டையாகவும் இருக்கும்.",
          "te": "దరఖాస్తును మీ యజమానే నిర్వహిస్తారు — ఈ కార్డు మీరు దిగిన తర్వాత వ్యక్తిగతంగా ఏమి చేయాలో మాత్రమే. భౌతిక పాస్ కార్డును మీ వద్ద ఉంచుకోండి; ఇది సింగపూర్‌లో మీ రోజువారీ గుర్తింపుగా కూడా పనిచేస్తుంది.",
          "ml": "അപേക്ഷ നിങ്ങളുടെ തൊഴിലുടമ തന്നെ കൈകാര്യം ചെയ്യുന്നു — ഈ കാർഡ് നിങ്ങൾ ഇറങ്ങിക്കഴിഞ്ഞാൽ വ്യക്തിപരമായി ചെയ്യേണ്ടതിനെക്കുറിച്ച് മാത്രമാണ്. ഫിസിക്കൽ പാസ് കാർഡ് നിങ്ങളുടെ പക്കൽ സൂക്ഷിക്കുക; ഇത് സിംഗപ്പൂരിൽ നിങ്ങളുടെ ദൈനംദിന ഐഡിയായും പ്രവർത്തിക്കുന്നു."},
    location={"en": "MOM Employment Pass Services Centre, 1500 Bendemeer Road, Singapore 339946",
               "hi": "MOM Employment Pass Services Centre, 1500 Bendemeer Road, सिंगापुर 339946",
               "ta": "MOM Employment Pass Services Centre, 1500 Bendemeer Road, சிங்கப்பூர் 339946",
               "te": "MOM Employment Pass Services Centre, 1500 Bendemeer Road, సింగపూర్ 339946",
               "ml": "MOM Employment Pass Services Centre, 1500 Bendemeer Road, സിംഗപ്പൂർ 339946"},
    phone=None,
    email={"en": "No general phone line published — use MOM's online enquiry form for case-specific questions",
            "hi": "कोई सामान्य फ़ोन लाइन प्रकाशित नहीं — मामला-विशिष्ट प्रश्नों के लिए MOM का ऑनलाइन पूछताछ फ़ॉर्म इस्तेमाल करें",
            "ta": "பொது தொலைபேசி எண் வெளியிடப்படவில்லை — வழக்கு-குறிப்பிட்ட கேள்விகளுக்கு MOM இன் ஆன்லைன் விசாரணை படிவத்தைப் பயன்படுத்தவும்",
            "te": "సాధారణ ఫోన్ లైన్ ప్రచురించబడలేదు — కేసు-నిర్దిష్ట ప్రశ్నల కోసం MOM యొక్క ఆన్‌లైన్ విచారణ ఫారంను ఉపయోగించండి",
            "ml": "പൊതു ഫോൺ ലൈൻ പ്രസിദ്ധീകരിച്ചിട്ടില്ല — കേസ്-നിർദ്ദിഷ്ട ചോദ്യങ്ങൾക്ക് MOM ന്റെ ഓൺലൈൻ അന്വേഷണ ഫോം ഉപയോഗിക്കുക"},
    links=[
        {"href": "https://www.mom.gov.sg/passes-and-permits", "label": {"en": "↗ MOM — passes & permits", "hi": "↗ MOM — पास और परमिट", "ta": "↗ MOM — பாஸ் & அனுமதிகள்", "te": "↗ MOM — పాస్‌లు & పర్మిట్లు", "ml": "↗ MOM — പാസുകളും പെർമിറ്റുകളും"}},
        {"href": "https://www.ica.gov.sg/reside/LTVP", "label": {"en": "↗ ICA — dependant pass registration", "hi": "↗ ICA — आश्रित पास पंजीकरण", "ta": "↗ ICA — சார்ந்தோர் பாஸ் பதிவு", "te": "↗ ICA — డిపెండెంట్ పాస్ నమోదు", "ml": "↗ ICA — ആശ്രിത പാസ് രജിസ്ട്രേഷൻ"}},
    ],
)

entry(
    category="sg_immigration", country="singapore", badge_official=True, passes=["EP", "SPass", "WP", "DP"],
    search_en="singpass activation foreign user account digital identity",
    title={"en": "Activate your SingPass account", "hi": "अपना SingPass खाता सक्रिय करें", "ta": "உங்கள் SingPass கணக்கை செயல்படுத்தவும்",
           "te": "మీ SingPass ఖాతాను యాక్టివేట్ చేయండి", "ml": "നിങ്ങളുടെ SingPass അക്കൗണ്ട് സജീവമാക്കുക"},
    desc={"en": "SingPass is the digital identity behind almost every Singapore government transaction — tax filing, CPF, HDB, healthcare bookings, even some banks use it for KYC. Once you have a FIN, activating it is one of the highest-value first steps.",
          "hi": "SingPass लगभग हर सिंगापुर सरकारी लेन-देन के पीछे की डिजिटल पहचान है — कर दाख़िल करना, CPF, HDB, स्वास्थ्य सेवा बुकिंग, यहाँ तक कि कुछ बैंक भी KYC के लिए इसका उपयोग करते हैं। FIN मिलते ही, इसे सक्रिय करना सबसे मूल्यवान पहले क़दमों में से एक है।",
          "ta": "SingPass என்பது கிட்டத்தட்ட ஒவ்வொரு சிங்கப்பூர் அரசு பரிவர்த்தனையின் பின்னால் உள்ள டிஜிட்டல் அடையாளம் — வரி தாக்கல், CPF, HDB, சுகாதார முன்பதிவுகள், சில வங்கிகள் கூட KYC க்கு இதைப் பயன்படுத்துகின்றன. FIN கிடைத்ததும், இதை செயல்படுத்துவது மிக மதிப்புமிக்க முதல் படிகளில் ஒன்று.",
          "te": "SingPass దాదాపు ప్రతి సింగపూర్ ప్రభుత్వ లావాదేవీ వెనుక ఉన్న డిజిటల్ గుర్తింపు — పన్ను ఫైలింగ్, CPF, HDB, ఆరోగ్య సంరక్షణ బుకింగ్‌లు, కొన్ని బ్యాంకులు కూడా KYC కోసం దీన్ని ఉపయోగిస్తాయి. మీకు FIN వచ్చిన వెంటనే, దీన్ని యాక్టివేట్ చేయడం అత్యంత విలువైన మొదటి దశలలో ఒకటి.",
          "ml": "ഏകദേശം എല്ലാ സിംഗപ്പൂർ സർക്കാർ ഇടപാടുകൾക്കും പിന്നിലുള്ള ഡിജിറ്റൽ ഐഡന്റിറ്റിയാണ് SingPass — നികുതി ഫയലിംഗ്, CPF, HDB, ആരോഗ്യ പരിരക്ഷാ ബുക്കിംഗുകൾ, ചില ബാങ്കുകൾ പോലും KYC ക്ക് ഇത് ഉപയോഗിക്കുന്നു. നിങ്ങൾക്ക് FIN ലഭിച്ചുകഴിഞ്ഞാൽ, ഇത് സജീവമാക്കുന്നത് ഏറ്റവും മൂല്യവത്തായ ആദ്യ ഘട്ടങ്ങളിലൊന്നാണ്."},
    handles={"en": "digital ID setup · face verification", "hi": "डिजिटल ID सेटअप · चेहरा सत्यापन", "ta": "டிஜிட்டல் ID அமைப்பு · முக சரிபார்ப்பு",
             "te": "డిజిటల్ ID సెటప్ · ఫేస్ వెరిఫికేషన్", "ml": "ഡിജിറ്റൽ ഐഡി സെറ്റപ്പ് · ഫേസ് വെരിഫിക്കേഷൻ"},
    steps={"en": ["Go to the Singpass website or app and choose to register as a foreigner (Singpass Foreign user Account / SFA) using your FIN.",
                  "Enter your registered mobile number and email to receive a one-time PIN.",
                  "Complete identity verification — this is usually a face verification step through the app, or in some cases in person at an ICA/Singpass counter.",
                  "Set your Singpass app PIN and enable the app on your phone — most day-to-day logins happen by scanning a QR code with the app rather than typing a password."],
           "hi": ["Singpass वेबसाइट या ऐप पर जाएँ और अपने FIN का उपयोग करके विदेशी के रूप में पंजीकरण (Singpass Foreign user Account / SFA) चुनें।",
                  "वन-टाइम PIN प्राप्त करने के लिए अपना पंजीकृत मोबाइल नंबर और ईमेल दर्ज करें।",
                  "पहचान सत्यापन पूरा करें — यह आमतौर पर ऐप के ज़रिए चेहरा सत्यापन चरण होता है, या कुछ मामलों में ICA/Singpass काउंटर पर व्यक्तिगत रूप से।",
                  "अपना Singpass ऐप PIN सेट करें और फ़ोन पर ऐप सक्षम करें — अधिकांश रोज़मर्रा के लॉगिन पासवर्ड टाइप करने के बजाय ऐप से QR कोड स्कैन करके होते हैं।"],
           "ta": ["Singpass இணையதளம் அல்லது ஆப்பிற்குச் சென்று உங்கள் FIN ஐப் பயன்படுத்தி வெளிநாட்டவராக பதிவு செய்ய (Singpass Foreign user Account / SFA) தேர்ந்தெடுக்கவும்.",
                  "ஒரு முறை PIN பெற உங்கள் பதிவு செய்யப்பட்ட மொபைல் எண் மற்றும் மின்னஞ்சலை உள்ளிடவும்.",
                  "அடையாள சரிபார்ப்பை முடிக்கவும் — இது பொதுவாக ஆப் மூலம் முக சரிபார்ப்பு படியாகும், அல்லது சில சமயங்களில் ICA/Singpass கவுன்டரில் நேரில்.",
                  "உங்கள் Singpass ஆப் PIN ஐ அமைத்து உங்கள் மொபைலில் ஆப்பை இயக்கவும் — பெரும்பாலான அன்றாட உள்நுழைவுகள் கடவுச்சொல் தட்டச்சு செய்வதற்குப் பதிலாக ஆப் மூலம் QR குறியீட்டை ஸ்கேன் செய்வதன் மூலம் நடக்கும்."],
           "te": ["Singpass వెబ్‌సైట్ లేదా యాప్‌కు వెళ్లి మీ FIN ఉపయోగించి విదేశీయుడిగా నమోదు (Singpass Foreign user Account / SFA) ఎంచుకోండి.",
                  "వన్-టైమ్ PIN పొందడానికి మీ నమోదిత మొబైల్ నంబర్ మరియు ఇమెయిల్‌ను నమోదు చేయండి.",
                  "గుర్తింపు ధృవీకరణను పూర్తి చేయండి — ఇది సాధారణంగా యాప్ ద్వారా ఫేస్ వెరిఫికేషన్ దశ, లేదా కొన్ని సందర్భాల్లో ICA/Singpass కౌంటర్ వద్ద వ్యక్తిగతంగా.",
                  "మీ Singpass యాప్ PINని సెట్ చేసి మీ ఫోన్‌లో యాప్‌ను ప్రారంభించండి — చాలా రోజువారీ లాగిన్‌లు పాస్‌వర్డ్ టైప్ చేయడానికి బదులుగా యాప్‌తో QR కోడ్‌ను స్కాన్ చేయడం ద్వారా జరుగుతాయి."],
           "ml": ["Singpass വെബ്‌സൈറ്റിലോ ആപ്പിലോ പോയി നിങ്ങളുടെ FIN ഉപയോഗിച്ച് വിദേശിയായി രജിസ്റ്റർ ചെയ്യുക (Singpass Foreign user Account / SFA) തിരഞ്ഞെടുക്കുക.",
                  "ഒറ്റത്തവണ PIN ലഭിക്കാൻ നിങ്ങളുടെ രജിസ്റ്റർ ചെയ്ത മൊബൈൽ നമ്പറും ഇമെയിലും നൽകുക.",
                  "ഐഡന്റിറ്റി വെരിഫിക്കേഷൻ പൂർത്തിയാക്കുക — ഇത് സാധാരണയായി ആപ്പ് വഴിയുള്ള ഫേസ് വെരിഫിക്കേഷൻ ഘട്ടമാണ്, അല്ലെങ്കിൽ ചില സന്ദർഭങ്ങളിൽ ICA/Singpass കൗണ്ടറിൽ നേരിട്ട്.",
                  "നിങ്ങളുടെ Singpass ആപ്പ് PIN സെറ്റ് ചെയ്ത് നിങ്ങളുടെ ഫോണിൽ ആപ്പ് പ്രവർത്തനക്ഷമമാക്കുക — മിക്ക ദൈനംദിന ലോഗിനുകളും പാസ്‌വേഡ് ടൈപ്പ് ചെയ്യുന്നതിന് പകരം ആപ്പ് ഉപയോഗിച്ച് QR കോഡ് സ്കാൻ ചെയ്യുന്നതിലൂടെയാണ്."]},
    docs={"en": ["FIN (from your work pass card)", "A Singapore mobile number", "A valid email address"],
          "hi": ["FIN (आपके वर्क पास कार्ड से)", "एक सिंगापुर मोबाइल नंबर", "एक वैध ईमेल पता"],
          "ta": ["FIN (உங்கள் வேலை பாஸ் அட்டையிலிருந்து)", "ஒரு சிங்கப்பூர் மொபைல் எண்", "ஒரு செல்லுபடியாகும் மின்னஞ்சல் முகவரி"],
          "te": ["FIN (మీ వర్క్ పాస్ కార్డు నుండి)", "ఒక సింగపూర్ మొబైల్ నంబర్", "చెల్లుబాటు అయ్యే ఇమెయిల్ చిరునామా"],
          "ml": ["FIN (നിങ്ങളുടെ വർക്ക് പാസ് കാർഡിൽ നിന്ന്)", "ഒരു സിംഗപ്പൂർ മൊബൈൽ നമ്പർ", "സാധുവായ ഇമെയിൽ വിലാസം"]},
    note={"en": "Do this early — many onward steps (bank KYC at some banks, IRAS, CPF, HDB rental checks) assume you already have Singpass working.",
          "hi": "इसे जल्दी करें — कई आगे के क़दम (कुछ बैंकों में बैंक KYC, IRAS, CPF, HDB किराया जाँच) मान लेते हैं कि आपका Singpass पहले से काम कर रहा है।",
          "ta": "இதை முன்கூட்டியே செய்யுங்கள் — பல அடுத்தடுத்த படிகள் (சில வங்கிகளில் வங்கி KYC, IRAS, CPF, HDB வாடகை சரிபார்ப்புகள்) உங்கள் Singpass ஏற்கனவே வேலை செய்கிறது என்று கருதுகின்றன.",
          "te": "దీన్ని ముందుగానే చేయండి — చాలా తర్వాతి దశలు (కొన్ని బ్యాంకుల్లో బ్యాంక్ KYC, IRAS, CPF, HDB అద్దె తనిఖీలు) మీ Singpass ఇప్పటికే పనిచేస్తుందని భావిస్తాయి.",
          "ml": "ഇത് നേരത്തെ ചെയ്യുക — പല തുടർ ഘട്ടങ്ങളും (ചില ബാങ്കുകളിലെ ബാങ്ക് KYC, IRAS, CPF, HDB വാടക പരിശോധനകൾ) നിങ്ങളുടെ Singpass ഇതിനകം പ്രവർത്തിക്കുന്നുവെന്ന് കരുതുന്നു."},
    location={"en": "Online (Singpass app/website); face verification at an ICA counter if the app step fails",
               "hi": "ऑनलाइन (Singpass ऐप/वेबसाइट); अगर ऐप चरण विफल हो तो ICA काउंटर पर चेहरा सत्यापन",
               "ta": "ஆன்லைன் (Singpass ஆப்/இணையதளம்); ஆப் படி தோல்வியடைந்தால் ICA கவுன்டரில் முக சரிபார்ப்பு",
               "te": "ఆన్‌లైన్ (Singpass యాప్/వెబ్‌సైట్); యాప్ దశ విఫలమైతే ICA కౌంటర్ వద్ద ఫేస్ వెరిఫికేషన్",
               "ml": "ഓൺലൈൻ (Singpass ആപ്പ്/വെബ്‌സൈറ്റ്); ആപ്പ് ഘട്ടം പരാജയപ്പെട്ടാൽ ICA കൗണ്ടറിൽ ഫേസ് വെരിഫിക്കേഷൻ"},
    phone=None, email=None,
    links=[{"href": "https://www.singpass.gov.sg", "label": {"en": "↗ Register — singpass.gov.sg", "hi": "↗ पंजीकरण करें — singpass.gov.sg", "ta": "↗ பதிவு செய்யவும் — singpass.gov.sg", "te": "↗ నమోదు చేసుకోండి — singpass.gov.sg", "ml": "↗ രജിസ്റ്റർ ചെയ്യുക — singpass.gov.sg"}}],
)

# ---- Singapore: Money, CPF & tax ----

entry(
    category="sg_money", country="singapore", badge_official=True, passes=["EP", "SPass", "WP", "DP"],
    search_en="singapore bank account opening dbs ocbc uob employment pass foreigner",
    title={"en": "Open a Singapore bank account", "hi": "सिंगापुर बैंक खाता खोलें", "ta": "சிங்கப்பூர் வங்கிக் கணக்கைத் திறக்கவும்",
           "te": "సింగపూర్ బ్యాంక్ ఖాతా తెరవండి", "ml": "സിംഗപ്പൂർ ബാങ്ക് അക്കൗണ്ട് തുറക്കുക"},
    desc={"en": "You'll need a local account for salary deposit and day-to-day spending. Some banks let new work-pass holders open an account online before or shortly after arrival; others require a branch visit once you have your pass card and a local address.",
          "hi": "वेतन जमा और रोज़मर्रा के ख़र्च के लिए आपको एक स्थानीय खाता चाहिए। कुछ बैंक नए वर्क-पास धारकों को पहुँचने से पहले या तुरंत बाद ऑनलाइन खाता खोलने देते हैं; अन्य को पास कार्ड और स्थानीय पता मिलने पर शाखा जाने की ज़रूरत होती है।",
          "ta": "ஊதிய வைப்பு மற்றும் அன்றாட செலவினங்களுக்கு உங்களுக்கு உள்ளூர் கணக்கு தேவை. சில வங்கிகள் புதிய வேலை-பாஸ் வைத்திருப்பவர்களை வருகைக்கு முன் அல்லது சிறிது நேரத்திற்குப் பிறகு ஆன்லைனில் கணக்கு திறக்க அனுமதிக்கின்றன; மற்றவை உங்கள் பாஸ் அட்டை மற்றும் உள்ளூர் முகவரி கிடைத்தவுடன் கிளை வருகையை கோருகின்றன.",
          "te": "జీతం జమ మరియు రోజువారీ ఖర్చుల కోసం మీకు స్థానిక ఖాతా అవసరం. కొన్ని బ్యాంకులు కొత్త వర్క్-పాస్ హోల్డర్లను రావడానికి ముందు లేదా వెంటనే ఆన్‌లైన్‌లో ఖాతా తెరవడానికి అనుమతిస్తాయి; మరికొన్నింటికి మీ పాస్ కార్డు మరియు స్థానిక చిరునామా వచ్చిన తర్వాత శాఖ సందర్శన అవసరం.",
          "ml": "ശമ്പള നിക്ഷേപത്തിനും ദൈനംദിന ചെലവുകൾക്കും നിങ്ങൾക്ക് ഒരു പ്രാദേശിക അക്കൗണ്ട് ആവശ്യമാണ്. ചില ബാങ്കുകൾ പുതിയ വർക്ക്-പാസ് ഉടമകളെ എത്തുന്നതിന് മുമ്പോ തൊട്ടുപിന്നാലെയോ ഓൺലൈനിൽ അക്കൗണ്ട് തുറക്കാൻ അനുവദിക്കുന്നു; മറ്റുള്ളവയ്ക്ക് നിങ്ങളുടെ പാസ് കാർഡും പ്രാദേശിക വിലാസവും ലഭിച്ചുകഴിഞ്ഞാൽ ബ്രാഞ്ച് സന്ദർശനം ആവശ്യമാണ്."},
    handles={"en": "salary account · online vs branch KYC", "hi": "वेतन खाता · ऑनलाइन बनाम शाखा KYC", "ta": "ஊதிய கணக்கு · ஆன்லைன் vs கிளை KYC",
             "te": "జీతం ఖాతా · ఆన్‌లైన్ vs శాఖ KYC", "ml": "ശമ്പള അക്കൗണ്ട് · ഓൺലൈൻ vs ബ്രാഞ്ച് KYC"},
    steps={"en": ["Check which bank your employer uses for payroll — opening there sometimes speeds up KYC.",
                  "For online opening (some banks support this for new EP/S Pass holders), apply via the bank's app with your passport and IPA/pass details.",
                  "For branch opening, book an appointment and bring your passport, pass card (or IPA if not yet collected), and proof of address.",
                  "Proof of address can be a tenancy agreement, or in its absence a letter from your employer confirming your Singapore address."],
           "hi": ["जाँचें कि आपका नियोक्ता पेरोल के लिए किस बैंक का उपयोग करता है — वहाँ खोलने से कभी-कभी KYC तेज़ हो जाती है।",
                  "ऑनलाइन खोलने के लिए (कुछ बैंक नए EP/S Pass धारकों के लिए इसे समर्थन करते हैं), अपने पासपोर्ट और IPA/पास विवरण के साथ बैंक के ऐप के ज़रिए आवेदन करें।",
                  "शाखा में खोलने के लिए, अपॉइंटमेंट बुक करें और अपना पासपोर्ट, पास कार्ड (या अभी न मिला हो तो IPA), और पते का प्रमाण साथ लाएँ।",
                  "पते का प्रमाण किराया अनुबंध हो सकता है, या इसके अभाव में आपके सिंगापुर पते की पुष्टि करने वाला नियोक्ता का पत्र।"],
           "ta": ["உங்கள் முதலாளி பேரோலுக்கு எந்த வங்கியைப் பயன்படுத்துகிறார் என்று சரிபார்க்கவும் — அங்கு திறப்பது சில நேரங்களில் KYC ஐ விரைவுபடுத்தும்.",
                  "ஆன்லைன் திறப்புக்கு (சில வங்கிகள் புதிய EP/S Pass வைத்திருப்பவர்களுக்கு இதை ஆதரிக்கின்றன), உங்கள் பாஸ்போர்ட் மற்றும் IPA/பாஸ் விவரங்களுடன் வங்கியின் ஆப் மூலம் விண்ணப்பிக்கவும்.",
                  "கிளையில் திறக்க, அப்பாயிண்ட்மென்ட் பதிவு செய்து உங்கள் பாஸ்போர்ட், பாஸ் அட்டை (அல்லது இன்னும் பெறவில்லை என்றால் IPA), மற்றும் முகவரி ஆதாரத்தை கொண்டு வரவும்.",
                  "முகவரி ஆதாரம் ஒரு குடியிருப்பு ஒப்பந்தமாக இருக்கலாம், அல்லது அது இல்லாத பட்சத்தில் உங்கள் சிங்கப்பூர் முகவரியை உறுதிப்படுத்தும் முதலாளியின் கடிதம்."],
           "te": ["మీ యజమాని పేరోల్ కోసం ఏ బ్యాంకు ఉపయోగిస్తారో తనిఖీ చేయండి — అక్కడ తెరవడం కొన్నిసార్లు KYC ని వేగవంతం చేస్తుంది.",
                  "ఆన్‌లైన్‌లో తెరవడానికి (కొన్ని బ్యాంకులు కొత్త EP/S Pass హోల్డర్లకు దీన్ని సపోర్ట్ చేస్తాయి), మీ పాస్‌పోర్ట్ మరియు IPA/పాస్ వివరాలతో బ్యాంకు యాప్ ద్వారా దరఖాస్తు చేసుకోండి.",
                  "శాఖలో తెరవడానికి, అపాయింట్‌మెంట్ బుక్ చేసుకుని మీ పాస్‌పోర్ట్, పాస్ కార్డు (లేదా ఇంకా తీసుకోకపోతే IPA), మరియు చిరునామా రుజువును తీసుకురండి.",
                  "చిరునామా రుజువు అద్దె ఒప్పందం కావచ్చు, లేదా అది లేకపోతే మీ సింగపూర్ చిరునామాను నిర్ధారించే యజమాని లేఖ."],
           "ml": ["നിങ്ങളുടെ തൊഴിലുടമ പേറോളിനായി ഏത് ബാങ്ക് ഉപയോഗിക്കുന്നുവെന്ന് പരിശോധിക്കുക — അവിടെ തുറക്കുന്നത് ചിലപ്പോൾ KYC വേഗത്തിലാക്കും.",
                  "ഓൺലൈൻ തുറക്കുന്നതിന് (ചില ബാങ്കുകൾ പുതിയ EP/S Pass ഉടമകൾക്ക് ഇത് പിന്തുണയ്ക്കുന്നു), നിങ്ങളുടെ പാസ്‌പോർട്ടും IPA/പാസ് വിവരങ്ങളും ഉപയോഗിച്ച് ബാങ്കിന്റെ ആപ്പ് വഴി അപേക്ഷിക്കുക.",
                  "ബ്രാഞ്ചിൽ തുറക്കുന്നതിന്, അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്ത് നിങ്ങളുടെ പാസ്‌പോർട്ട്, പാസ് കാർഡ് (അല്ലെങ്കിൽ ഇതുവരെ വാങ്ങിയില്ലെങ്കിൽ IPA), വിലാസ തെളിവ് എന്നിവ കൊണ്ടുവരിക.",
                  "വിലാസ തെളിവ് ഒരു വാടക കരാർ ആകാം, അല്ലെങ്കിൽ അതില്ലെങ്കിൽ നിങ്ങളുടെ സിംഗപ്പൂർ വിലാസം സ്ഥിരീകരിക്കുന്ന തൊഴിലുടമയുടെ കത്ത്."]},
    docs={"en": ["Passport", "Employment/S Pass card (or IPA letter if pending)", "Proof of address (tenancy agreement or employer letter)", "Initial deposit (varies by bank)"],
          "hi": ["पासपोर्ट", "Employment/S Pass कार्ड (या लंबित हो तो IPA पत्र)", "पते का प्रमाण (किराया अनुबंध या नियोक्ता पत्र)", "प्रारंभिक जमा (बैंक के अनुसार भिन्न)"],
          "ta": ["பாஸ்போர்ட்", "Employment/S Pass அட்டை (அல்லது நிலுவையில் இருந்தால் IPA கடிதம்)", "முகவரி ஆதாரம் (குடியிருப்பு ஒப்பந்தம் அல்லது முதலாளி கடிதம்)", "ஆரம்ப வைப்பு (வங்கியைப் பொறுத்து மாறுபடும்)"],
          "te": ["పాస్‌పోర్ట్", "Employment/S Pass కార్డు (లేదా పెండింగ్‌లో ఉంటే IPA లేఖ)", "చిరునామా రుజువు (అద్దె ఒప్పందం లేదా యజమాని లేఖ)", "ప్రారంభ డిపాజిట్ (బ్యాంకును బట్టి మారుతుంది)"],
          "ml": ["പാസ്‌പോർട്ട്", "Employment/S Pass കാർഡ് (അല്ലെങ്കിൽ പെൻഡിംഗ് ആണെങ്കിൽ IPA കത്ത്)", "വിലാസ തെളിവ് (വാടക കരാർ അല്ലെങ്കിൽ തൊഴിലുടമയുടെ കത്ത്)", "പ്രാരംഭ നിക്ഷേപം (ബാങ്ക് അനുസരിച്ച് വ്യത്യാസപ്പെടും)"]},
    note={"en": "Requirements and online-opening eligibility change bank to bank and change over time — confirm current requirements on the specific bank's website before your appointment.",
          "hi": "आवश्यकताएँ और ऑनलाइन-खोलने की पात्रता बैंक-दर-बैंक अलग होती है और समय के साथ बदलती है — अपॉइंटमेंट से पहले संबंधित बैंक की वेबसाइट पर मौजूदा आवश्यकताओं की पुष्टि करें।",
          "ta": "தேவைகள் மற்றும் ஆன்லைன்-திறப்பு தகுதி வங்கிக்கு வங்கி மாறுபடும் மற்றும் காலப்போக்கில் மாறும் — உங்கள் அப்பாயிண்ட்மென்ட்டிற்கு முன் குறிப்பிட்ட வங்கியின் இணையதளத்தில் தற்போதைய தேவைகளை உறுதிப்படுத்தவும்.",
          "te": "అవసరాలు మరియు ఆన్‌లైన్-తెరవడం అర్హత బ్యాంకును బట్టి మారుతుంది మరియు కాలక్రమేణా మారుతుంది — మీ అపాయింట్‌మెంట్‌కు ముందు నిర్దిష్ట బ్యాంకు వెబ్‌సైట్‌లో ప్రస్తుత అవసరాలను నిర్ధారించుకోండి.",
          "ml": "ആവശ്യകതകളും ഓൺലൈൻ-തുറക്കൽ യോഗ്യതയും ബാങ്ക് അനുസരിച്ച് വ്യത്യാസപ്പെടുകയും കാലക്രമേണ മാറുകയും ചെയ്യുന്നു — നിങ്ങളുടെ അപ്പോയിന്റ്മെന്റിന് മുമ്പ് നിർദ്ദിഷ്ട ബാങ്കിന്റെ വെബ്‌സൈറ്റിൽ നിലവിലെ ആവശ്യകതകൾ സ്ഥിരീകരിക്കുക."},
    location={"en": "Bank branch, or online via the bank's app (varies by bank)", "hi": "बैंक शाखा, या बैंक के ऐप के ज़रिए ऑनलाइन (बैंक के अनुसार भिन्न)",
               "ta": "வங்கி கிளை, அல்லது வங்கியின் ஆப் மூலம் ஆன்லைன் (வங்கியைப் பொறுத்து மாறுபடும்)", "te": "బ్యాంకు శాఖ, లేదా బ్యాంకు యాప్ ద్వారా ఆన్‌లైన్ (బ్యాంకును బట్టి మారుతుంది)",
               "ml": "ബാങ്ക് ബ്രാഞ്ച്, അല്ലെങ്കിൽ ബാങ്കിന്റെ ആപ്പ് വഴി ഓൺലൈൻ (ബാങ്ക് അനുസരിച്ച് വ്യത്യാസപ്പെടും)"},
    phone=None, email=None,
    links=[
        {"href": "https://www.dbs.com.sg", "label": {"en": "↗ DBS — personal banking", "hi": "↗ DBS — व्यक्तिगत बैंकिंग", "ta": "↗ DBS — தனிநபர் வங்கி", "te": "↗ DBS — పర్సనల్ బ్యాంకింగ్", "ml": "↗ DBS — പേഴ്‌സണൽ ബാങ്കിംഗ്"}},
        {"href": "https://www.ocbc.com", "label": {"en": "↗ OCBC — personal banking", "hi": "↗ OCBC — व्यक्तिगत बैंकिंग", "ta": "↗ OCBC — தனிநபர் வங்கி", "te": "↗ OCBC — పర్సనల్ బ్యాంకింగ్", "ml": "↗ OCBC — പേഴ്‌സണൽ ബാങ്കിംഗ്"}},
        {"href": "https://www.uob.com.sg", "label": {"en": "↗ UOB — personal banking", "hi": "↗ UOB — व्यक्तिगत बैंकिंग", "ta": "↗ UOB — தனிநபர் வங்கி", "te": "↗ UOB — పర్సనల్ బ్యాంకింగ్", "ml": "↗ UOB — പേഴ്‌സണൽ ബാങ്കിംഗ്"}},
    ],
)

entry(
    category="sg_money", country="singapore", badge_official=True, passes=["EP", "SPass"],
    search_en="cpf contribution iras income tax filing singapore employment pass",
    title={"en": "CPF & your first income tax filing", "hi": "CPF और आपका पहला आयकर दाख़िला", "ta": "CPF & உங்கள் முதல் வருமான வரி தாக்கல்",
           "te": "CPF & మీ మొదటి ఆదాయపు పన్ను ఫైలింగ్", "ml": "CPF, നിങ്ങളുടെ ആദ്യ ആദായനികുതി ഫയലിംഗ്"},
    desc={"en": "CPF (Central Provident Fund) contributions generally apply only to Singapore Citizens and PRs, not to Employment Pass or S Pass holders — so most work-pass holders won't see CPF deductions at all. What every work-pass holder does need to handle is annual income tax with IRAS, since Singapore has no automatic payroll tax deduction the way some countries do.",
          "hi": "CPF (Central Provident Fund) योगदान आमतौर पर केवल सिंगापुर नागरिकों और PR पर लागू होता है, Employment Pass या S Pass धारकों पर नहीं — इसलिए अधिकांश वर्क-पास धारकों को CPF कटौती बिल्कुल नहीं दिखेगी। हर वर्क-पास धारक को जिससे निपटना ज़रूरी है वह है IRAS के साथ वार्षिक आयकर, क्योंकि सिंगापुर में कुछ देशों की तरह स्वचालित पेरोल कर कटौती नहीं होती।",
          "ta": "CPF (Central Provident Fund) பங்களிப்புகள் பொதுவாக சிங்கப்பூர் குடிமக்கள் மற்றும் PR களுக்கு மட்டுமே பொருந்தும், Employment Pass அல்லது S Pass வைத்திருப்பவர்களுக்கு அல்ல — எனவே பெரும்பாலான வேலை-பாஸ் வைத்திருப்பவர்களுக்கு CPF கழிவுகள் தெரியாது. ஒவ்வொரு வேலை-பாஸ் வைத்திருப்பவரும் கையாள வேண்டியது IRAS உடன் ஆண்டு வருமான வரி, ஏனெனில் சில நாடுகளைப் போல சிங்கப்பூரில் தானியங்கி பேரோல் வரி கழிவு இல்லை.",
          "te": "CPF (Central Provident Fund) విరాళాలు సాధారణంగా సింగపూర్ పౌరులు మరియు PRలకు మాత్రమే వర్తిస్తాయి, Employment Pass లేదా S Pass హోల్డర్లకు కాదు — కాబట్టి చాలా వర్క్-పాస్ హోల్డర్లకు CPF మినహాయింపులు కనిపించవు. ప్రతి వర్క్-పాస్ హోల్డర్ నిర్వహించాల్సింది IRAS తో వార్షిక ఆదాయపు పన్ను, ఎందుకంటే కొన్ని దేశాల మాదిరిగా సింగపూర్‌లో ఆటోమేటిక్ పేరోల్ పన్ను మినహాయింపు లేదు.",
          "ml": "CPF (Central Provident Fund) സംഭാവനകൾ പൊതുവെ സിംഗപ്പൂർ പൗരന്മാർക്കും PR കൾക്കും മാത്രമേ ബാധകമാകൂ, Employment Pass അല്ലെങ്കിൽ S Pass ഉടമകൾക്കല്ല — അതിനാൽ മിക്ക വർക്ക്-പാസ് ഉടമകൾക്കും CPF കിഴിവുകൾ ഒട്ടും കാണില്ല. എല്ലാ വർക്ക്-പാസ് ഉടമകളും കൈകാര്യം ചെയ്യേണ്ടത് IRAS മായുള്ള വാർഷിക ആദായനികുതിയാണ്, കാരണം ചില രാജ്യങ്ങളിലേതുപോലെ സിംഗപ്പൂരിൽ ഓട്ടോമാറ്റിക് പേറോൾ നികുതി കിഴിവ് ഇല്ല."},
    handles={"en": "CPF applicability · IRAS e-filing · Form IR8A", "hi": "CPF प्रयोज्यता · IRAS ई-फ़ाइलिंग · Form IR8A",
             "ta": "CPF பொருந்தக்கூடிய தன்மை · IRAS மின்-தாக்கல் · Form IR8A", "te": "CPF వర్తింపు · IRAS ఇ-ఫైలింగ్ · Form IR8A", "ml": "CPF ബാധകത · IRAS ഇ-ഫയലിംഗ് · Form IR8A"},
    steps={"en": ["Confirm your CPF status — most EP/S Pass holders are not enrolled; check your payslip or ask HR if you're unsure.",
                  "Each year, your employer files a Form IR8A reporting your income to IRAS on your behalf.",
                  "IRAS sends a tax bill or, more often now, invites you to e-file via myTax Portal using your Singpass login.",
                  "Log in with Singpass, review the pre-filled income, add any reliefs/deductions you're eligible for, and submit before the deadline (typically mid-April).",
                  "Pay any tax owed via the methods IRAS lists — GIRO, PayNow, or bank transfer."],
           "hi": ["अपनी CPF स्थिति की पुष्टि करें — अधिकांश EP/S Pass धारक नामांकित नहीं हैं; अगर अनिश्चित हों तो अपनी वेतन पर्ची जाँचें या HR से पूछें।",
                  "हर साल, आपका नियोक्ता आपकी ओर से Form IR8A दाख़िल कर IRAS को आय की सूचना देता है।",
                  "IRAS कर बिल भेजता है या, अब अक्सर, आपके Singpass लॉगिन का उपयोग कर myTax Portal के ज़रिए ई-फ़ाइल करने को आमंत्रित करता है।",
                  "Singpass से लॉगिन करें, पहले से भरी आय की समीक्षा करें, अपनी पात्र कोई राहत/कटौती जोड़ें, और समय सीमा (आमतौर पर मध्य-अप्रैल) से पहले जमा करें।",
                  "IRAS द्वारा सूचीबद्ध तरीक़ों से बकाया कर चुकाएँ — GIRO, PayNow, या बैंक ट्रांसफ़र।"],
           "ta": ["உங்கள் CPF நிலையை உறுதிப்படுத்தவும் — பெரும்பாலான EP/S Pass வைத்திருப்பவர்கள் பதிவு செய்யப்படவில்லை; உறுதியில்லை என்றால் உங்கள் ஊதியப் பட்டியலைச் சரிபார்க்கவும் அல்லது HR ஐக் கேளுங்கள்.",
                  "ஒவ்வொரு ஆண்டும், உங்கள் முதலாளி உங்களுக்காக IRAS க்கு உங்கள் வருமானத்தை தெரிவிக்கும் Form IR8A ஐ தாக்கல் செய்வார்.",
                  "IRAS ஒரு வரி பில் அனுப்பும் அல்லது, இப்போது பெரும்பாலும், உங்கள் Singpass உள்நுழைவைப் பயன்படுத்தி myTax Portal மூலம் மின்-தாக்கல் செய்ய அழைக்கும்.",
                  "Singpass உடன் உள்நுழைந்து, முன்கூட்டியே நிரப்பப்பட்ட வருமானத்தை மதிப்பாய்வு செய்து, நீங்கள் தகுதியுள்ள ஏதேனும் நிவாரணங்கள்/கழிவுகளைச் சேர்த்து, காலக்கெடுவிற்கு முன் (பொதுவாக ஏப்ரல் நடுப்பகுதி) சமர்ப்பிக்கவும்.",
                  "IRAS பட்டியலிடும் முறைகள் மூலம் நிலுவையில் உள்ள வரியை செலுத்தவும் — GIRO, PayNow, அல்லது வங்கி பரிமாற்றம்."],
           "te": ["మీ CPF స్థితిని నిర్ధారించుకోండి — చాలా EP/S Pass హోల్డర్లు నమోదు కాలేదు; మీకు తెలియకపోతే మీ జీతం స్లిప్‌ను తనిఖీ చేయండి లేదా HR ని అడగండి.",
                  "ప్రతి సంవత్సరం, మీ యజమాని మీ తరపున IRAS కి మీ ఆదాయాన్ని నివేదిస్తూ Form IR8A ను దాఖలు చేస్తారు.",
                  "IRAS పన్ను బిల్లు పంపుతుంది లేదా, ఇప్పుడు తరచుగా, మీ Singpass లాగిన్ ఉపయోగించి myTax Portal ద్వారా ఇ-ఫైల్ చేయమని ఆహ్వానిస్తుంది.",
                  "Singpass తో లాగిన్ అయి, ముందుగా నింపిన ఆదాయాన్ని సమీక్షించి, మీకు అర్హత ఉన్న ఏవైనా మినహాయింపులు/తగ్గింపులను జోడించి, గడువులోపు (సాధారణంగా ఏప్రిల్ మధ్యలో) సమర్పించండి.",
                  "IRAS జాబితా చేసిన పద్ధతుల ద్వారా బాకీ ఉన్న పన్నును చెల్లించండి — GIRO, PayNow, లేదా బ్యాంక్ బదిలీ."],
           "ml": ["നിങ്ങളുടെ CPF സ്റ്റാറ്റസ് സ്ഥിരീകരിക്കുക — മിക്ക EP/S Pass ഉടമകളും എൻറോൾ ചെയ്തിട്ടില്ല; ഉറപ്പില്ലെങ്കിൽ നിങ്ങളുടെ ശമ്പള സ്ലിപ്പ് പരിശോധിക്കുക അല്ലെങ്കിൽ HR നോട് ചോദിക്കുക.",
                  "എല്ലാ വർഷവും, നിങ്ങളുടെ തൊഴിലുടമ നിങ്ങൾക്ക് വേണ്ടി IRAS ന് നിങ്ങളുടെ വരുമാനം റിപ്പോർട്ട് ചെയ്യുന്ന Form IR8A ഫയൽ ചെയ്യുന്നു.",
                  "IRAS ഒരു നികുതി ബിൽ അയക്കുന്നു അല്ലെങ്കിൽ, ഇപ്പോൾ കൂടുതലും, നിങ്ങളുടെ Singpass ലോഗിൻ ഉപയോഗിച്ച് myTax Portal വഴി ഇ-ഫയൽ ചെയ്യാൻ ക്ഷണിക്കുന്നു.",
                  "Singpass ഉപയോഗിച്ച് ലോഗിൻ ചെയ്ത്, മുൻകൂട്ടി പൂരിപ്പിച്ച വരുമാനം അവലോകനം ചെയ്ത്, നിങ്ങൾക്ക് അർഹതയുള്ള ഏതെങ്കിലും ഇളവുകൾ/കിഴിവുകൾ ചേർത്ത്, സമയപരിധിക്ക് മുമ്പ് (സാധാരണയായി ഏപ്രിൽ പകുതി) സമർപ്പിക്കുക.",
                  "IRAS പട്ടികപ്പെടുത്തുന്ന രീതികൾ വഴി കുടിശ്ശികയുള്ള നികുതി അടയ്ക്കുക — GIRO, PayNow, അല്ലെങ്കിൽ ബാങ്ക് ട്രാൻസ്ഫർ."]},
    docs={"en": ["Singpass login", "Form IR8A (filed by your employer — you don't submit this yourself)", "Details of any tax reliefs you're claiming"],
          "hi": ["Singpass लॉगिन", "Form IR8A (आपके नियोक्ता द्वारा दाख़िल — आप इसे स्वयं जमा नहीं करते)", "आपके द्वारा दावा की जा रही किसी कर राहत का विवरण"],
          "ta": ["Singpass உள்நுழைவு", "Form IR8A (உங்கள் முதலாளியால் தாக்கல் செய்யப்பட்டது — நீங்கள் இதை நீங்களே சமர்ப்பிக்க வேண்டாம்)", "நீங்கள் கோரும் ஏதேனும் வரி நிவாரணங்களின் விவரங்கள்"],
          "te": ["Singpass లాగిన్", "Form IR8A (మీ యజమాని దాఖలు చేస్తారు — మీరు దీన్ని మీరే సమర్పించాల్సిన అవసరం లేదు)", "మీరు క్లెయిమ్ చేస్తున్న ఏవైనా పన్ను మినహాయింపుల వివరాలు"],
          "ml": ["Singpass ലോഗിൻ", "Form IR8A (നിങ്ങളുടെ തൊഴിലുടമ ഫയൽ ചെയ്യുന്നു — നിങ്ങൾ ഇത് സ്വയം സമർപ്പിക്കേണ്ടതില്ല)", "നിങ്ങൾ ക്ലെയിം ചെയ്യുന്ന ഏതെങ്കിലും നികുതി ഇളവുകളുടെ വിവരങ്ങൾ"]},
    note={"en": "Leaving Singapore for good? Your employer must file a tax clearance (Form IR21) at least a month before your last working day — this can hold up your final paycheck until IRAS clears it, so flag your departure date to HR early.",
          "hi": "हमेशा के लिए सिंगापुर छोड़ रहे हैं? आपके नियोक्ता को आपके अंतिम कार्यदिवस से कम से कम एक महीने पहले कर क्लीयरेंस (Form IR21) दाख़िल करना ज़रूरी है — यह IRAS द्वारा मंज़ूर होने तक आपकी अंतिम तनख़्वाह रोक सकता है, इसलिए अपनी प्रस्थान तिथि जल्दी HR को बताएँ।",
          "ta": "எப்போதைக்குமாக சிங்கப்பூரை விட்டு வெளியேறுகிறீர்களா? உங்கள் கடைசி வேலை நாளுக்கு குறைந்தது ஒரு மாதத்திற்கு முன் உங்கள் முதலாளி வரி அனுமதி (Form IR21) தாக்கல் செய்ய வேண்டும் — இது IRAS அங்கீகரிக்கும் வரை உங்கள் இறுதி சம்பளத்தை தடுக்கலாம், எனவே உங்கள் புறப்பாடு தேதியை HR க்கு முன்கூட்டியே தெரிவிக்கவும்.",
          "te": "శాశ్వతంగా సింగపూర్ వదిలి వెళ్తున్నారా? మీ చివరి పని దినానికి కనీసం ఒక నెల ముందు మీ యజమాని పన్ను క్లియరెన్స్ (Form IR21) దాఖలు చేయాలి — ఇది IRAS క్లియర్ చేసే వరకు మీ చివరి జీతాన్ని ఆపవచ్చు, కాబట్టి మీ బయలుదేరే తేదీని HR కి ముందుగానే తెలియజేయండి.",
          "ml": "എന്നെന്നേക്കുമായി സിംഗപ്പൂർ വിടുകയാണോ? നിങ്ങളുടെ അവസാന ജോലി ദിവസത്തിന് ഒരു മാസമെങ്കിലും മുമ്പ് നിങ്ങളുടെ തൊഴിലുടമ നികുതി ക്ലിയറൻസ് (Form IR21) ഫയൽ ചെയ്യണം — ഇത് IRAS ക്ലിയർ ചെയ്യുന്നത് വരെ നിങ്ങളുടെ അവസാന ശമ്പളം തടഞ്ഞുവയ്ക്കാം, അതിനാൽ നിങ്ങളുടെ പോക്ക് തീയതി നേരത്തെ HR നെ അറിയിക്കുക."},
    location={"en": "Online — myTax Portal (IRAS)", "hi": "ऑनलाइन — myTax Portal (IRAS)", "ta": "ஆன்லைன் — myTax Portal (IRAS)", "te": "ఆన్‌లైన్ — myTax Portal (IRAS)", "ml": "ഓൺലൈൻ — myTax Portal (IRAS)"},
    phone=None, email=None,
    links=[
        {"href": "https://www.iras.gov.sg", "label": {"en": "↗ IRAS — myTax Portal", "hi": "↗ IRAS — myTax Portal", "ta": "↗ IRAS — myTax Portal", "te": "↗ IRAS — myTax Portal", "ml": "↗ IRAS — myTax Portal"}},
        {"href": "https://www.cpf.gov.sg", "label": {"en": "↗ CPF Board — who needs to contribute", "hi": "↗ CPF Board — किसे योगदान चाहिए", "ta": "↗ CPF Board — யாருக்கு பங்களிப்பு தேவை", "te": "↗ CPF Board — ఎవరు విరాళం ఇవ్వాలి", "ml": "↗ CPF Board — ആർക്കാണ് സംഭാവന വേണ്ടത്"}},
    ],
)

# ---- Singapore: Settling in ----

entry(
    category="sg_settling", country="singapore", badge_official=True,
    search_en="singapore driving licence conversion foreign indian licence basic theory test",
    title={"en": "Convert your driving licence", "hi": "अपना ड्राइविंग लाइसेंस बदलवाएँ", "ta": "உங்கள் ஓட்டுநர் உரிமத்தை மாற்றவும்",
           "te": "మీ డ్రైవింగ్ లైసెన్స్‌ను మార్చుకోండి", "ml": "നിങ്ങളുടെ ഡ്രൈവിംഗ് ലൈസൻസ് മാറ്റുക"},
    desc={"en": "Once you've been resident in Singapore for a year or more, your foreign licence stops being valid to drive on and you need to convert it to a Singapore licence — which, for an Indian licence, means passing Singapore's Basic Theory Test rather than a straight swap.",
          "hi": "एक साल या उससे अधिक समय तक सिंगापुर में रहने के बाद, आपका विदेशी लाइसेंस चलाने के लिए मान्य नहीं रह जाता और आपको इसे सिंगापुर लाइसेंस में बदलवाना ज़रूरी है — भारतीय लाइसेंस के लिए इसका मतलब है सीधे अदला-बदली के बजाय सिंगापुर की Basic Theory Test पास करना।",
          "ta": "நீங்கள் ஒரு வருடம் அல்லது அதற்கு மேல் சிங்கப்பூரில் வசித்திருந்தால், உங்கள் வெளிநாட்டு உரிமம் ஓட்ட செல்லுபடியாகாது மற்றும் அதை சிங்கப்பூர் உரிமமாக மாற்ற வேண்டும் — இந்திய உரிமத்திற்கு, இதன் பொருள் நேரடி மாற்றத்திற்குப் பதிலாக சிங்கப்பூரின் Basic Theory Test ஐ தேர்ச்சி பெறுவது.",
          "te": "మీరు ఒక సంవత్సరం లేదా అంతకంటే ఎక్కువ కాలం సింగపూర్‌లో నివసించిన తర్వాత, మీ విదేశీ లైసెన్స్ డ్రైవ్ చేయడానికి చెల్లదు మరియు దాన్ని సింగపూర్ లైసెన్స్‌గా మార్చుకోవాలి — భారత లైసెన్స్‌కు దీని అర్థం నేరుగా మార్పిడికి బదులుగా సింగపూర్ యొక్క Basic Theory Test పాస్ కావడం.",
          "ml": "നിങ്ങൾ ഒരു വർഷമോ അതിലധികമോ സിംഗപ്പൂരിൽ താമസിച്ചുകഴിഞ്ഞാൽ, നിങ്ങളുടെ വിദേശ ലൈസൻസ് ഓടിക്കാൻ സാധുതയില്ലാതാകും, അത് സിംഗപ്പൂർ ലൈസൻസാക്കി മാറ്റേണ്ടതുണ്ട് — ഇന്ത്യൻ ലൈസൻസിന്, ഇതിനർത്ഥം നേരിട്ടുള്ള മാറ്റത്തിന് പകരം സിംഗപ്പൂരിന്റെ Basic Theory Test പാസാകുക എന്നതാണ്."},
    handles={"en": "Basic Theory Test · licence conversion", "hi": "Basic Theory Test · लाइसेंस बदलाव", "ta": "Basic Theory Test · உரிம மாற்றம்",
             "te": "Basic Theory Test · లైసెన్స్ మార్పిడి", "ml": "Basic Theory Test · ലൈസൻസ് കൺവേർഷൻ"},
    steps={"en": ["Get an endorsement letter confirming your Indian licence's validity from the Indian High Commission in Singapore (with the payment receipt) — SPF requires this for Indian licences specifically.",
                  "Gather proof you held the licence for at least a year with 6+ months of physical presence in India, plus an official English translation if the licence isn't in English.",
                  "Study for and pass Singapore's Basic Theory Test (BTT) at a driving school or the Institute of Driving instructors.",
                  "Book a conversion appointment through the SPF e-Services portal.",
                  "Attend with your Indian licence, passport/work pass, BTT pass slip, and the HCI endorsement letter to complete the conversion."],
           "hi": ["सिंगापुर में भारतीय उच्चायोग से अपने भारतीय लाइसेंस की वैधता की पुष्टि करने वाला एक अनुमोदन पत्र प्राप्त करें (भुगतान रसीद सहित) — SPF को भारतीय लाइसेंस के लिए विशेष रूप से इसकी ज़रूरत है।",
                  "यह प्रमाण इकट्ठा करें कि आपके पास कम से कम एक साल से लाइसेंस था जिसमें भारत में 6+ महीने की शारीरिक उपस्थिति थी, साथ ही अगर लाइसेंस अंग्रेज़ी में नहीं है तो एक आधिकारिक अंग्रेज़ी अनुवाद।",
                  "ड्राइविंग स्कूल या Institute of Driving instructors में सिंगापुर के Basic Theory Test (BTT) की तैयारी करें और उसे पास करें।",
                  "SPF e-Services पोर्टल के ज़रिए बदलाव अपॉइंटमेंट बुक करें।",
                  "बदलाव पूरा करने के लिए अपने भारतीय लाइसेंस, पासपोर्ट/वर्क पास, BTT पास स्लिप, और HCI अनुमोदन पत्र के साथ जाएँ।"],
           "ta": ["சிங்கப்பூரில் உள்ள இந்திய உயர் ஸ்தானிகராலயத்திடமிருந்து உங்கள் இந்திய உரிமத்தின் செல்லுபடியை உறுதிப்படுத்தும் அனுமதி கடிதத்தைப் பெறவும் (கட்டண ரசீதுடன்) — SPF இந்திய உரிமங்களுக்கு குறிப்பாக இதை கோருகிறது.",
                  "இந்தியாவில் 6+ மாத உடல் ரீதியான வருகையுடன் குறைந்தது ஒரு வருடமாவது நீங்கள் உரிமத்தை வைத்திருந்தீர்கள் என்பதற்கான ஆதாரத்தை சேகரிக்கவும், மேலும் உரிமம் ஆங்கிலத்தில் இல்லையென்றால் ஒரு அதிகாரப்பூர்வ ஆங்கில மொழிபெயர்ப்பு.",
                  "ஓட்டுநர் பள்ளி அல்லது Institute of Driving instructors இல் சிங்கப்பூரின் Basic Theory Test (BTT) க்கு படித்து தேர்ச்சி பெறவும்.",
                  "SPF e-Services போர்ட்டல் மூலம் மாற்ற அப்பாயிண்ட்மென்ட்டை பதிவு செய்யவும்.",
                  "மாற்றத்தை முடிக்க உங்கள் இந்திய உரிமம், பாஸ்போர்ட்/வேலை பாஸ், BTT தேர்ச்சி சீட்டு, மற்றும் HCI அனுமதி கடிதத்துடன் கலந்துகொள்ளுங்கள்."],
           "te": ["సింగపూర్‌లోని భారత హై కమిషన్ నుండి మీ భారత లైసెన్స్ చెల్లుబాటును నిర్ధారించే ఆమోద లేఖను పొందండి (చెల్లింపు రసీదుతో) — SPF భారత లైసెన్స్‌ల కోసం ప్రత్యేకంగా దీన్ని కోరుతుంది.",
                  "భారత్‌లో 6+ నెలల భౌతిక ఉనికితో మీరు కనీసం ఒక సంవత్సరం లైసెన్స్ కలిగి ఉన్నారని రుజువును సేకరించండి, అలాగే లైసెన్స్ ఇంగ్లీష్‌లో లేకపోతే అధికారిక ఆంగ్ల అనువాదం.",
                  "డ్రైవింగ్ స్కూల్ లేదా Institute of Driving instructors వద్ద సింగపూర్ యొక్క Basic Theory Test (BTT) కోసం చదివి పాస్ అవ్వండి.",
                  "SPF e-Services పోర్టల్ ద్వారా మార్పిడి అపాయింట్‌మెంట్‌ను బుక్ చేసుకోండి.",
                  "మార్పిడిని పూర్తి చేయడానికి మీ భారత లైసెన్స్, పాస్‌పోర్ట్/వర్క్ పాస్, BTT పాస్ స్లిప్, మరియు HCI ఆమోద లేఖతో హాజరు కండి."],
           "ml": ["സിംഗപ്പൂരിലെ ഇന്ത്യൻ ഹൈക്കമ്മീഷനിൽ നിന്ന് നിങ്ങളുടെ ഇന്ത്യൻ ലൈസൻസിന്റെ സാധുത സ്ഥിരീകരിക്കുന്ന ഒരു എൻഡോഴ്‌സ്‌മെന്റ് കത്ത് വാങ്ങുക (പേയ്‌മെന്റ് രസീതോടെ) — SPF ഇന്ത്യൻ ലൈസൻസുകൾക്ക് പ്രത്യേകമായി ഇത് ആവശ്യപ്പെടുന്നു.",
                  "ഇന്ത്യയിൽ 6+ മാസത്തെ ശാരീരിക സാന്നിധ്യത്തോടെ കുറഞ്ഞത് ഒരു വർഷമെങ്കിലും നിങ്ങൾ ലൈസൻസ് കൈവശം വച്ചിരുന്നു എന്നതിന്റെ തെളിവ് ശേഖരിക്കുക, ലൈസൻസ് ഇംഗ്ലീഷിലല്ലെങ്കിൽ ഔദ്യോഗിക ഇംഗ്ലീഷ് പരിഭാഷയും.",
                  "ഒരു ഡ്രൈവിംഗ് സ്കൂളിലോ Institute of Driving instructors ലോ സിംഗപ്പൂരിന്റെ Basic Theory Test (BTT) ന് പഠിച്ച് പാസാകുക.",
                  "SPF e-Services പോർട്ടൽ വഴി കൺവേർഷൻ അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്യുക.",
                  "കൺവേർഷൻ പൂർത്തിയാക്കാൻ നിങ്ങളുടെ ഇന്ത്യൻ ലൈസൻസ്, പാസ്‌പോർട്ട്/വർക്ക് പാസ്, BTT പാസ് സ്ലിപ്പ്, HCI എൻഡോഴ്‌സ്‌മെന്റ് കത്ത് എന്നിവയുമായി ഹാജരാകുക."]},
    docs={"en": ["Valid Indian driving licence", "HCI Singapore endorsement letter (with payment receipt)", "Passport and work pass/FIN", "Passport-size photo (taken within 3 months)", "Official English translation, if the licence isn't in English", "Basic Theory Test pass slip"],
          "hi": ["वैध भारतीय ड्राइविंग लाइसेंस", "HCI सिंगापुर अनुमोदन पत्र (भुगतान रसीद सहित)", "पासपोर्ट और वर्क पास/FIN", "पासपोर्ट साइज़ फ़ोटो (3 माह के भीतर ली गई)", "अगर लाइसेंस अंग्रेज़ी में नहीं है तो आधिकारिक अंग्रेज़ी अनुवाद", "Basic Theory Test पास स्लिप"],
          "ta": ["செல்லுபடியாகும் இந்திய ஓட்டுநர் உரிமம்", "HCI சிங்கப்பூர் அனுமதி கடிதம் (கட்டண ரசீதுடன்)", "பாஸ்போர்ட் மற்றும் வேலை பாஸ்/FIN", "பாஸ்போர்ட் அளவு புகைப்படம் (3 மாதங்களுக்குள் எடுக்கப்பட்டது)", "உரிமம் ஆங்கிலத்தில் இல்லையென்றால் அதிகாரப்பூர்வ ஆங்கில மொழிபெயர்ப்பு", "Basic Theory Test தேர்ச்சி சீட்டு"],
          "te": ["చెల్లుబాటు అయ్యే భారత డ్రైవింగ్ లైసెన్స్", "HCI సింగపూర్ ఆమోద లేఖ (చెల్లింపు రసీదుతో)", "పాస్‌పోర్ట్ మరియు వర్క్ పాస్/FIN", "పాస్‌పోర్ట్ సైజు ఫోటో (3 నెలల్లోపు తీసినది)", "లైసెన్స్ ఇంగ్లీష్‌లో లేకపోతే అధికారిక ఆంగ్ల అనువాదం", "Basic Theory Test పాస్ స్లిప్"],
          "ml": ["സാധുവായ ഇന്ത്യൻ ഡ്രൈവിംഗ് ലൈസൻസ്", "HCI സിംഗപ്പൂർ എൻഡോഴ്‌സ്‌മെന്റ് കത്ത് (പേയ്‌മെന്റ് രസീതോടെ)", "പാസ്‌പോർട്ടും വർക്ക് പാസ്/FIN ഉം", "പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ (3 മാസത്തിനുള്ളിൽ എടുത്തത്)", "ലൈസൻസ് ഇംഗ്ലീഷിലല്ലെങ്കിൽ ഔദ്യോഗിക ഇംഗ്ലീഷ് പരിഭാഷ", "Basic Theory Test പാസ് സ്ലിപ്പ്"]},
    note={"en": "This is specific to Indian (and several other non-reciprocal-agreement) licences — some other nationalities get a more direct swap. Confirm the current checklist for Indian licences on SPF's site since requirements have shifted before.",
          "hi": "यह विशेष रूप से भारतीय (और कई अन्य ग़ैर-पारस्परिक-समझौता) लाइसेंसों पर लागू है — कुछ अन्य राष्ट्रीयताओं को अधिक सीधा बदलाव मिलता है। चूँकि आवश्यकताएँ पहले बदल चुकी हैं, SPF की साइट पर भारतीय लाइसेंस के लिए मौजूदा चेकलिस्ट की पुष्टि करें।",
          "ta": "இது இந்திய (மற்றும் பல பரஸ்பர-ஒப்பந்தமற்ற) உரிமங்களுக்கு குறிப்பிட்டது — சில பிற தேசியத்தவர்களுக்கு அதிக நேரடி மாற்றம் கிடைக்கும். தேவைகள் முன்பு மாறியிருப்பதால் SPF தளத்தில் இந்திய உரிமங்களுக்கான தற்போதைய சரிபார்ப்பு பட்டியலை உறுதிப்படுத்தவும்.",
          "te": "ఇది భారత (మరియు అనేక ఇతర పరస్పర-ఒప్పందం లేని) లైసెన్స్‌లకు ప్రత్యేకం — కొన్ని ఇతర జాతీయతలకు మరింత ప్రత్యక్ష మార్పిడి లభిస్తుంది. అవసరాలు గతంలో మారినందున SPF సైట్‌లో భారత లైసెన్స్‌ల కోసం ప్రస్తుత చెక్‌లిస్ట్‌ను నిర్ధారించుకోండి.",
          "ml": "ഇത് ഇന്ത്യൻ (കൂടാതെ പരസ്പര-കരാറില്ലാത്ത മറ്റ് പലതും) ലൈസൻസുകൾക്ക് പ്രത്യേകമാണ് — മറ്റ് ചില ദേശീയതകൾക്ക് കൂടുതൽ നേരിട്ടുള്ള മാറ്റം ലഭിക്കും. ആവശ്യകതകൾ മുമ്പ് മാറിയിട്ടുള്ളതിനാൽ SPF യുടെ സൈറ്റിൽ ഇന്ത്യൻ ലൈസൻസുകൾക്കുള്ള നിലവിലെ ചെക്ക്‌ലിസ്റ്റ് സ്ഥിരീകരിക്കുക."},
    location={"en": "SPF e-Services (booking) + Traffic Police / testing centre for the BTT",
               "hi": "SPF e-Services (बुकिंग) + BTT के लिए Traffic Police / परीक्षण केंद्र",
               "ta": "SPF e-Services (பதிவு) + BTT க்கான Traffic Police / சோதனை மையம்",
               "te": "SPF e-Services (బుకింగ్) + BTT కోసం ట్రాఫిక్ పోలీసు / టెస్టింగ్ సెంటర్",
               "ml": "SPF e-Services (ബുക്കിംഗ്) + BTT ക്കുള്ള ട്രാഫിക് പോലീസ്/ടെസ്റ്റിംഗ് സെന്റർ"},
    phone={"en": "SPF general (non-emergency) hotline: 1800-255-0000", "hi": "SPF सामान्य (ग़ैर-आपातकालीन) हेल्पलाइन: 1800-255-0000",
            "ta": "SPF பொது (அவசரமற்ற) உதவி எண்: 1800-255-0000", "te": "SPF సాధారణ (అత్యవసరం కాని) హెల్ప్‌లైన్: 1800-255-0000", "ml": "SPF പൊതു (അടിയന്തിരമല്ലാത്ത) ഹെൽപ്‌ലൈൻ: 1800-255-0000"},
    email=None,
    links=[{"href": "https://www.police.gov.sg/E-Services/Book-Appointment-to-Convert-Foreign-Driving-Licence", "label": {"en": "↗ SPF — book licence conversion appointment", "hi": "↗ SPF — लाइसेंस बदलाव अपॉइंटमेंट बुक करें",
                                                                                                                          "ta": "↗ SPF — உரிம மாற்ற அப்பாயிண்ட்மென்ட் பதிவு செய்யவும்", "te": "↗ SPF — లైసెన్స్ మార్పిడి అపాయింట్‌మెంట్ బుక్ చేయండి", "ml": "↗ SPF — ലൈസൻസ് കൺവേർഷൻ അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്യുക"}}],
)

entry(
    category="sg_settling", country="singapore", badge_official=True, passes=["EP", "SPass", "DP"],
    search_en="hdb rental foreigner employment pass minimum occupation period renting singapore",
    title={"en": "Renting a home as a foreigner", "hi": "विदेशी के रूप में घर किराए पर लेना", "ta": "வெளிநாட்டவராக வீட்டை வாடகைக்கு எடுத்தல்",
           "te": "విదేశీయుడిగా ఇల్లు అద్దెకు తీసుకోవడం", "ml": "വിദേശിയായി ഒരു വീട് വാടകയ്‌ക്കെടുക്കൽ"},
    desc={"en": "Foreigners on a work pass can't buy HDB flats and can't rent a whole HDB flat freely either — subletting rules restrict which flats can be rented to non-Malaysians/non-citizens and for how long. Most work-pass holders end up renting private condos or apartments instead, or an HDB room where the owner's quota allows it.",
          "hi": "वर्क पास पर विदेशी HDB फ़्लैट नहीं ख़रीद सकते और पूरे HDB फ़्लैट को स्वतंत्र रूप से किराए पर भी नहीं ले सकते — सबलेटिंग नियम प्रतिबंधित करते हैं कि कौन-से फ़्लैट ग़ैर-मलेशियाई/ग़ैर-नागरिकों को किराए पर दिए जा सकते हैं और कितने समय के लिए। अधिकांश वर्क-पास धारक इसके बजाय निजी कॉन्डो या अपार्टमेंट किराए पर लेते हैं, या जहाँ मालिक का कोटा अनुमति दे वहाँ HDB का एक कमरा।",
          "ta": "வேலை பாஸில் உள்ள வெளிநாட்டவர்கள் HDB அடுக்குமாடிகளை வாங்க முடியாது மற்றும் ஒரு முழு HDB அடுக்குமாடியை சுதந்திரமாக வாடகைக்கு எடுக்கவும் முடியாது — சப்லெட்டிங் விதிகள் மலேசியர்கள் அல்லாத/குடிமக்கள் அல்லாதவர்களுக்கு எந்த அடுக்குமாடிகள் வாடகைக்கு விடலாம் என்பதையும் எவ்வளவு காலத்திற்கு என்பதையும் கட்டுப்படுத்துகின்றன. பெரும்பாலான வேலை-பாஸ் வைத்திருப்பவர்கள் அதற்குப் பதிலாக தனியார் கான்டோ அல்லது அபார்ட்மென்ட்களை வாடகைக்கு எடுக்கிறார்கள், அல்லது உரிமையாளரின் ஒதுக்கீடு அனுமதிக்கும் இடத்தில் ஒரு HDB அறையை.",
          "te": "వర్క్ పాస్‌పై ఉన్న విదేశీయులు HDB ఫ్లాట్‌లను కొనలేరు మరియు పూర్తి HDB ఫ్లాట్‌ను స్వేచ్ఛగా అద్దెకు కూడా తీసుకోలేరు — సబ్‌లెట్టింగ్ నియమాలు మలేషియన్లు కాని/పౌరులు కాని వారికి ఏ ఫ్లాట్‌లు అద్దెకు ఇవ్వవచ్చు మరియు ఎంత కాలం అనేదానిపై పరిమితులు విధిస్తాయి. చాలా వర్క్-పాస్ హోల్డర్లు బదులుగా ప్రైవేట్ కాండోలు లేదా అపార్ట్‌మెంట్‌లను అద్దెకు తీసుకుంటారు, లేదా యజమాని కోటా అనుమతించే చోట HDB గదిని.",
          "ml": "വർക്ക് പാസിലുള്ള വിദേശികൾക്ക് HDB ഫ്ലാറ്റുകൾ വാങ്ങാൻ കഴിയില്ല, ഒരു മുഴുവൻ HDB ഫ്ലാറ്റ് സ്വതന്ത്രമായി വാടകയ്ക്കെടുക്കാനും കഴിയില്ല — സബ്‌ലെറ്റിംഗ് നിയമങ്ങൾ മലേഷ്യക്കാരല്ലാത്ത/പൗരന്മാരല്ലാത്തവർക്ക് ഏത് ഫ്ലാറ്റുകൾ എത്ര കാലത്തേക്ക് വാടകയ്ക്ക് നൽകാമെന്ന് നിയന്ത്രിക്കുന്നു. മിക്ക വർക്ക്-പാസ് ഉടമകളും പകരം സ്വകാര്യ കോണ്ടോകളോ അപ്പാർട്ട്മെന്റുകളോ വാടകയ്ക്കെടുക്കുന്നു, അല്ലെങ്കിൽ ഉടമയുടെ ക്വാട്ട അനുവദിക്കുന്നിടത്ത് ഒരു HDB മുറി."},
    handles={"en": "eligibility to rent HDB rooms/flats · private rental basics", "hi": "HDB कमरे/फ़्लैट किराए पर लेने की पात्रता · निजी किराया मूल बातें",
             "ta": "HDB அறைகள்/அடுக்குமாடிகளை வாடகைக்கு எடுக்கும் தகுதி · தனியார் வாடகை அடிப்படைகள்", "te": "HDB గదులు/ఫ్లాట్‌లను అద్దెకు తీసుకునే అర్హత · ప్రైవేట్ అద్దె ప్రాథమికాలు",
             "ml": "HDB മുറികൾ/ഫ്ലാറ്റുകൾ വാടകയ്‌ക്കെടുക്കാനുള്ള യോഗ്യത · സ്വകാര്യ വാടക അടിസ്ഥാനങ്ങൾ"},
    steps={"en": ["Decide between a private condo/apartment (no restrictions on foreign tenants) or an HDB room/flat (subject to HDB's subletting quotas and approval).",
                  "If considering an HDB room, check with the owner/agent that the flat isn't already at its non-citizen occupancy quota — HDB caps this per block and per flat type.",
                  "For any rental, agree terms and sign a Tenancy Agreement — have it stamped (stamp duty is payable, usually split or borne by the tenant by convention).",
                  "Register your new address for FIN/pass records where required, and use it to complete bank, Singpass and telco address updates."],
           "hi": ["निजी कॉन्डो/अपार्टमेंट (विदेशी किरायेदारों पर कोई प्रतिबंध नहीं) या HDB कमरा/फ़्लैट (HDB के सबलेटिंग कोटा और मंज़ूरी के अधीन) के बीच तय करें।",
                  "अगर HDB कमरे पर विचार कर रहे हैं, तो मालिक/एजेंट से जाँच लें कि फ़्लैट पहले से ही अपने ग़ैर-नागरिक अधिभोग कोटे पर तो नहीं है — HDB इसे प्रत्येक ब्लॉक और फ़्लैट प्रकार के अनुसार सीमित करता है।",
                  "किसी भी किराए के लिए, शर्तों पर सहमत हों और Tenancy Agreement पर हस्ताक्षर करें — इसे स्टैम्प कराएँ (स्टैम्प ड्यूटी देय है, आमतौर पर प्रथा अनुसार बाँटी जाती है या किरायेदार द्वारा वहन की जाती है)।",
                  "जहाँ आवश्यक हो वहाँ FIN/पास रिकॉर्ड के लिए अपना नया पता पंजीकृत करें, और बैंक, Singpass और टेल्को पता अपडेट पूरा करने के लिए इसका उपयोग करें।"],
           "ta": ["தனியார் கான்டோ/அபார்ட்மென்ட் (வெளிநாட்டு குடியிருப்பாளர்களுக்கு கட்டுப்பாடுகள் இல்லை) அல்லது HDB அறை/அடுக்குமாடி (HDB இன் சப்லெட்டிங் ஒதுக்கீடு மற்றும் அனுமதிக்கு உட்பட்டது) இடையே முடிவு செய்யவும்.",
                  "HDB அறையை பரிசீலிக்கிறீர்கள் என்றால், அடுக்குமாடி ஏற்கனவே அதன் குடிமகன் அல்லாத ஆக்கிரமிப்பு ஒதுக்கீட்டில் இல்லை என்பதை உரிமையாளர்/முகவரிடம் சரிபார்க்கவும் — HDB இதை ஒவ்வொரு தொகுதி மற்றும் அடுக்குமாடி வகைக்கும் வரம்பிடுகிறது.",
                  "எந்த வாடகைக்கும், விதிமுறைகளை ஒப்புக்கொண்டு Tenancy Agreement இல் கையெழுத்திடவும் — அதை முத்திரையிடச் செய்யவும் (முத்திரை கட்டணம் செலுத்த வேண்டும், வழக்கமாக பிரிக்கப்படுகிறது அல்லது வாடகைதாரரால் ஏற்கப்படுகிறது).",
                  "தேவைப்படும் இடத்தில் உங்கள் புதிய முகவரியை FIN/பாஸ் பதிவுகளுக்கு பதிவு செய்யவும், மேலும் வங்கி, Singpass மற்றும் டெல்கோ முகவரி புதுப்பிப்புகளை முடிக்க அதைப் பயன்படுத்தவும்."],
           "te": ["ప్రైవేట్ కాండో/అపార్ట్‌మెంట్ (విదేశీ అద్దెదారులపై పరిమితులు లేవు) లేదా HDB గది/ఫ్లాట్ (HDB యొక్క సబ్‌లెట్టింగ్ కోటాలు మరియు ఆమోదానికి లోబడి) మధ్య నిర్ణయించుకోండి.",
                  "HDB గదిని పరిశీలిస్తుంటే, ఫ్లాట్ ఇప్పటికే దాని పౌరులు కాని ఆక్యుపెన్సీ కోటాలో లేదని యజమాని/ఏజెంట్‌తో తనిఖీ చేయండి — HDB దీన్ని ప్రతి బ్లాక్ మరియు ఫ్లాట్ రకానికి పరిమితం చేస్తుంది.",
                  "ఏదైనా అద్దె కోసం, నిబంధనలను అంగీకరించి Tenancy Agreement పై సంతకం చేయండి — దాన్ని స్టాంప్ చేయించండి (స్టాంప్ డ్యూటీ చెల్లించాలి, సాధారణంగా సంప్రదాయం ప్రకారం విభజించబడుతుంది లేదా అద్దెదారు భరిస్తారు).",
                  "అవసరమైన చోట FIN/పాస్ రికార్డుల కోసం మీ కొత్త చిరునామాను నమోదు చేయండి, మరియు బ్యాంకు, Singpass మరియు టెల్కో చిరునామా అప్‌డేట్‌లను పూర్తి చేయడానికి దాన్ని ఉపయోగించండి."],
           "ml": ["സ്വകാര്യ കോണ്ടോ/അപ്പാർട്ട്മെന്റ് (വിദേശ വാടകക്കാർക്ക് നിയന്ത്രണങ്ങളില്ല) അല്ലെങ്കിൽ HDB മുറി/ഫ്ലാറ്റ് (HDB യുടെ സബ്‌ലെറ്റിംഗ് ക്വാട്ടകൾക്കും അംഗീകാരത്തിനും വിധേയം) എന്നിവയ്ക്കിടയിൽ തീരുമാനിക്കുക.",
                  "HDB മുറി പരിഗണിക്കുകയാണെങ്കിൽ, ഫ്ലാറ്റ് ഇതിനകം അതിന്റെ പൗരനല്ലാത്തവരുടെ ഒക്യുപൻസി ക്വാട്ടയിലല്ല എന്ന് ഉടമ/ഏജന്റിനോട് പരിശോധിക്കുക — HDB ഇത് ഓരോ ബ്ലോക്കിനും ഫ്ലാറ്റ് തരത്തിനും പരിമിതപ്പെടുത്തുന്നു.",
                  "ഏത് വാടകയ്ക്കും, നിബന്ധനകൾ അംഗീകരിച്ച് Tenancy Agreement ഒപ്പിടുക — അത് സ്റ്റാമ്പ് ചെയ്യിക്കുക (സ്റ്റാമ്പ് ഡ്യൂട്ടി അടയ്‌ക്കേണ്ടതുണ്ട്, സാധാരണയായി പതിവനുസരിച്ച് വിഭജിക്കപ്പെടുകയോ വാടകക്കാരൻ വഹിക്കുകയോ ചെയ്യുന്നു).",
                  "ആവശ്യമുള്ളിടത്ത് FIN/പാസ് രേഖകൾക്കായി നിങ്ങളുടെ പുതിയ വിലാസം രജിസ്റ്റർ ചെയ്യുക, ബാങ്ക്, Singpass, ടെൽകോ വിലാസ അപ്‌ഡേറ്റുകൾ പൂർത്തിയാക്കാൻ അത് ഉപയോഗിക്കുക."]},
    docs={"en": ["Passport and work pass card", "Signed, stamped Tenancy Agreement", "Security deposit (typically 1–2 months' rent)"],
          "hi": ["पासपोर्ट और वर्क पास कार्ड", "हस्ताक्षरित, स्टैम्प किया Tenancy Agreement", "सुरक्षा जमा (आमतौर पर 1–2 महीने का किराया)"],
          "ta": ["பாஸ்போர்ட் மற்றும் வேலை பாஸ் அட்டை", "கையொப்பமிடப்பட்ட, முத்திரையிடப்பட்ட Tenancy Agreement", "பாதுகாப்பு வைப்பு (பொதுவாக 1–2 மாத வாடகை)"],
          "te": ["పాస్‌పోర్ట్ మరియు వర్క్ పాస్ కార్డు", "సంతకం చేసిన, స్టాంప్ చేసిన Tenancy Agreement", "సెక్యూరిటీ డిపాజిట్ (సాధారణంగా 1–2 నెలల అద్దె)"],
          "ml": ["പാസ്‌പോർട്ടും വർക്ക് പാസ് കാർഡും", "ഒപ്പിട്ട, സ്റ്റാമ്പ് ചെയ്ത Tenancy Agreement", "സെക്യൂരിറ്റി ഡെപ്പോസിറ്റ് (സാധാരണയായി 1–2 മാസത്തെ വാടക)"]},
    note={"en": "HDB flats can't be bought by work-pass holders at all, and whole-flat/room rental to non-citizens is quota-capped and changes — always confirm current eligibility with HDB or the agent rather than assuming, before signing anything.",
          "hi": "वर्क-पास धारक HDB फ़्लैट बिल्कुल नहीं ख़रीद सकते, और ग़ैर-नागरिकों को पूरा फ़्लैट/कमरा किराए पर देना कोटा-सीमित है और बदलता रहता है — कुछ भी हस्ताक्षर करने से पहले, मान लेने के बजाय हमेशा HDB या एजेंट से मौजूदा पात्रता की पुष्टि करें।",
          "ta": "வேலை-பாஸ் வைத்திருப்பவர்கள் HDB அடுக்குமாடிகளை வாங்கவே முடியாது, மேலும் குடிமக்கள் அல்லாதவர்களுக்கு முழு அடுக்குமாடி/அறை வாடகை ஒதுக்கீட்டால் வரம்பிடப்பட்டு மாறுகிறது — எதிலும் கையெழுத்திடும் முன், கருதுவதற்குப் பதிலாக எப்போதும் HDB அல்லது முகவரிடம் தற்போதைய தகுதியை உறுதிப்படுத்தவும்.",
          "te": "వర్క్-పాస్ హోల్డర్లు HDB ఫ్లాట్‌లను అస్సలు కొనలేరు, మరియు పౌరులు కాని వారికి పూర్తి ఫ్లాట్/గది అద్దె కోటా-పరిమితం మరియు మారుతూ ఉంటుంది — దేనిపైనైనా సంతకం చేసే ముందు, ఊహించే బదులు ఎల్లప్పుడూ HDB లేదా ఏజెంట్‌తో ప్రస్తుత అర్హతను నిర్ధారించుకోండి.",
          "ml": "വർക്ക്-പാസ് ഉടമകൾക്ക് HDB ഫ്ലാറ്റുകൾ വാങ്ങാൻ ഒരിക്കലും കഴിയില്ല, പൗരന്മാരല്ലാത്തവർക്ക് മുഴുവൻ ഫ്ലാറ്റ്/മുറി വാടക ക്വാട്ട-പരിമിതവും മാറിക്കൊണ്ടിരിക്കുന്നതുമാണ് — എന്തെങ്കിലും ഒപ്പിടുന്നതിന് മുമ്പ്, ഊഹിക്കുന്നതിന് പകരം എപ്പോഴും HDB അല്ലെങ്കിൽ ഏജന്റുമായി നിലവിലെ യോഗ്യത സ്ഥിരീകരിക്കുക."},
    location={"en": "HDB Branch (for HDB rentals) or a private property agent", "hi": "HDB शाखा (HDB किराए के लिए) या निजी संपत्ति एजेंट",
               "ta": "HDB கிளை (HDB வாடகைக்கு) அல்லது தனியார் சொத்து முகவர்", "te": "HDB బ్రాంచ్ (HDB అద్దెల కోసం) లేదా ప్రైవేట్ ప్రాపర్టీ ఏజెంట్",
               "ml": "HDB ബ്രാഞ്ച് (HDB വാടകയ്ക്ക്) അല്ലെങ്കിൽ സ്വകാര്യ പ്രോപ്പർട്ടി ഏജന്റ്"},
    phone={"en": "HDB Branch Service Line: 1800 866 3066", "hi": "HDB शाखा सेवा लाइन: 1800 866 3066", "ta": "HDB கிளை சேவை எண்: 1800 866 3066",
            "te": "HDB బ్రాంచ్ సర్వీస్ లైన్: 1800 866 3066", "ml": "HDB ബ്രാഞ്ച് സർവീസ് ലൈൻ: 1800 866 3066"},
    email=None,
    links=[
        {"href": "https://www.hdb.gov.sg/residential/renting-a-flat/renting-from-the-open-market/eligibility", "label": {"en": "↗ HDB — renting eligibility", "hi": "↗ HDB — किराए की पात्रता", "ta": "↗ HDB — வாடகை தகுதி", "te": "↗ HDB — అద్దె అర్హత", "ml": "↗ HDB — വാടക യോഗ്യത"}},
    ],
)

entry(
    category="sg_settling", country="singapore", badge_official=True, passes=["EP", "SPass", "DP"],
    search_en="enrolling child school moe primary registration international student aeis",
    title={"en": "Enrolling your child in school", "hi": "अपने बच्चे को स्कूल में दाख़िल कराना", "ta": "உங்கள் குழந்தையை பள்ளியில் சேர்த்தல்",
           "te": "మీ పిల్లలను పాఠశాలలో చేర్చడం", "ml": "നിങ്ങളുടെ കുട്ടിയെ സ്കൂളിൽ ചേർക്കൽ"},
    desc={"en": "Singapore's government schools prioritise citizens and PRs, so most work-pass families either apply directly to a private/international school or go through MOE's separate international-student pathways — each with different costs, timelines and odds of a place.",
          "hi": "सिंगापुर के सरकारी स्कूल नागरिकों और PR धारकों को प्राथमिकता देते हैं, इसलिए अधिकांश वर्क-पास परिवार या तो सीधे किसी निजी/अंतरराष्ट्रीय स्कूल में आवेदन करते हैं या MOE के अलग अंतरराष्ट्रीय-छात्र मार्गों से गुज़रते हैं — हर एक की लागत, समय-सीमा और सीट मिलने की संभावना अलग-अलग होती है।",
          "ta": "சிங்கப்பூரின் அரசு பள்ளிகள் குடிமக்கள் மற்றும் PR வைத்திருப்பவர்களுக்கு முன்னுரிமை அளிக்கின்றன, எனவே பெரும்பாலான வேலை-பாஸ் குடும்பங்கள் நேரடியாக ஒரு தனியார்/சர்வதேச பள்ளியில் விண்ணப்பிக்கின்றன அல்லது MOE இன் தனித்தனி சர்வதேச-மாணவர் வழிகள் மூலம் செல்கின்றன — ஒவ்வொன்றும் வெவ்வேறு செலவு, காலவரையறை மற்றும் இட வாய்ப்பு கொண்டவை.",
          "te": "సింగపూర్ ప్రభుత్వ పాఠశాలలు పౌరులకు మరియు PR హోల్డర్లకు ప్రాధాన్యత ఇస్తాయి, కాబట్టి చాలా వర్క్-పాస్ కుటుంబాలు నేరుగా ప్రైవేట్/అంతర్జాతీయ పాఠశాలలో దరఖాస్తు చేసుకుంటాయి లేదా MOE యొక్క ప్రత్యేక అంతర్జాతీయ-విద్యార్థి మార్గాల ద్వారా వెళ్తాయి — ప్రతి దానికి వేర్వేరు ఖర్చు, కాలవ్యవధి మరియు సీటు దొరికే అవకాశం ఉంటుంది.",
          "ml": "സിംഗപ്പൂരിലെ സർക്കാർ സ്കൂളുകൾ പൗരന്മാർക്കും PR ഉടമകൾക്കും മുൻഗണന നൽകുന്നു, അതിനാൽ മിക്ക വർക്ക്-പാസ് കുടുംബങ്ങളും നേരിട്ട് ഒരു സ്വകാര്യ/അന്താരാഷ്ട്ര സ്കൂളിൽ അപേക്ഷിക്കുകയോ MOE യുടെ പ്രത്യേക അന്താരാഷ്ട്ര-വിദ്യാർത്ഥി മാർഗങ്ങളിലൂടെ പോകുകയോ ചെയ്യുന്നു — ഓരോന്നിനും വ്യത്യസ്ത ചെലവും സമയക്രമവും സീറ്റ് ലഭിക്കാനുള്ള സാധ്യതയുമുണ്ട്."},
    handles={"en": "P1 international pathway · AEIS/S-AEIS · private schools", "hi": "P1 अंतरराष्ट्रीय मार्ग · AEIS/S-AEIS · निजी स्कूल",
             "ta": "P1 சர்வதேச வழி · AEIS/S-AEIS · தனியார் பள்ளிகள்", "te": "P1 అంతర్జాతీయ మార్గం · AEIS/S-AEIS · ప్రైవేట్ పాఠశాలలు",
             "ml": "P1 അന്താരാഷ്ട്ര മാർഗം · AEIS/S-AEIS · സ്വകാര്യ സ്കൂളുകൾ"},
    steps={"en": ["For the simplest, most predictable route, apply directly to a private or international school of your choice — there's no MOE process to go through, just the school's own admissions and fees, which are Singapore's highest.",
                  "If you want a government/aided school and your child is starting Primary 1, submit an online 'interest' form to MOE during its international-student registration window (typically a short window in May) — a place isn't guaranteed, since Singapore Citizens and PRs are given priority first.",
                  "For entry into Primary 2–5 or Secondary 1–3, your child generally has to sit MOE's Admissions Exercise for International Students (AEIS), usually held around September–October, or the supplementary S-AEIS round around February–March — again, passing the test doesn't guarantee a seat if none is available.",
                  "For Junior College after Secondary school, international students apply directly to the JC of their choice, typically in December.",
                  "Registration windows, test dates and required documents change every year — check MOE's international-student pages directly before you plan around any date."],
           "hi": ["सबसे सरल और अनुमानित रास्ते के लिए, सीधे अपनी पसंद के किसी निजी या अंतरराष्ट्रीय स्कूल में आवेदन करें — इसमें MOE की कोई प्रक्रिया नहीं होती, बस स्कूल का अपना दाख़िला और शुल्क होता है, जो सिंगापुर में सबसे ज़्यादा होता है।",
                  "अगर आप सरकारी/सहायता-प्राप्त स्कूल चाहते हैं और आपका बच्चा Primary 1 शुरू कर रहा है, तो MOE की अंतरराष्ट्रीय-छात्र पंजीकरण अवधि (आमतौर पर मई में एक छोटी सी अवधि) के दौरान ऑनलाइन 'रुचि' फ़ॉर्म भरें — सीट की गारंटी नहीं है, क्योंकि सिंगापुर के नागरिकों और PR धारकों को पहले प्राथमिकता दी जाती है।",
                  "Primary 2–5 या Secondary 1–3 में दाख़िले के लिए, आपके बच्चे को आमतौर पर MOE की Admissions Exercise for International Students (AEIS) देनी होती है, जो आमतौर पर सितंबर–अक्टूबर के आसपास होती है, या फ़रवरी–मार्च के आसपास होने वाला पूरक S-AEIS राउंड — यहाँ भी, परीक्षा पास करने का मतलब सीट की गारंटी नहीं, अगर कोई सीट उपलब्ध न हो।",
                  "Secondary स्कूल के बाद Junior College के लिए, अंतरराष्ट्रीय छात्र सीधे अपनी पसंद के JC में आवेदन करते हैं, आमतौर पर दिसंबर में।",
                  "पंजीकरण की अवधि, परीक्षा की तारीख़ें और ज़रूरी दस्तावेज़ हर साल बदलते हैं — किसी भी तारीख़ के हिसाब से योजना बनाने से पहले MOE के अंतरराष्ट्रीय-छात्र पन्नों को सीधे जाँच लें।"],
           "ta": ["மிக எளிதான, முன்கூட்டியே தெரிந்துகொள்ளக்கூடிய வழிக்கு, உங்கள் விருப்பப்படி ஒரு தனியார் அல்லது சர்வதேச பள்ளியில் நேரடியாக விண்ணப்பிக்கவும் — இதில் MOE செயல்முறை எதுவும் இல்லை, பள்ளியின் சொந்த சேர்க்கை மற்றும் கட்டணம் மட்டுமே, இது சிங்கப்பூரில் அதிக செலவு கொண்டது.",
                  "நீங்கள் ஒரு அரசு/உதவி பெறும் பள்ளியை விரும்பினால், உங்கள் குழந்தை Primary 1 தொடங்குகிறது என்றால், MOE இன் சர்வதேச-மாணவர் பதிவு காலத்தில் (பொதுவாக மே மாதத்தில் ஒரு குறுகிய காலம்) ஆன்லைனில் 'ஆர்வம்' படிவத்தை சமர்ப்பிக்கவும் — இட உத்தரவாதம் இல்லை, ஏனெனில் சிங்கப்பூர் குடிமக்கள் மற்றும் PR வைத்திருப்பவர்களுக்கு முதலில் முன்னுரிமை அளிக்கப்படுகிறது.",
                  "Primary 2–5 அல்லது Secondary 1–3 இல் சேர்க்கைக்கு, உங்கள் குழந்தை பொதுவாக MOE இன் Admissions Exercise for International Students (AEIS) தேர்வை எழுத வேண்டும், இது பொதுவாக செப்டம்பர்–அக்டோபர் சுற்றி நடத்தப்படுகிறது, அல்லது பிப்ரவரி–மார்ச் சுற்றி நடக்கும் கூடுதல் S-AEIS சுற்று — இங்கும், தேர்வில் தேர்ச்சி பெறுவது இட வாய்ப்பு இல்லையென்றால் இடத்தை உத்தரவாதம் செய்யாது.",
                  "Secondary பள்ளிக்குப் பிறகு Junior College க்கு, சர்வதேச மாணவர்கள் தங்கள் விருப்பமான JC இல் நேரடியாக விண்ணப்பிக்கிறார்கள், பொதுவாக டிசம்பரில்.",
                  "பதிவு காலங்கள், தேர்வு தேதிகள் மற்றும் தேவையான ஆவணங்கள் ஒவ்வொரு ஆண்டும் மாறுகின்றன — எந்த தேதியையும் வைத்து திட்டமிடுவதற்கு முன் MOE இன் சர்வதேச-மாணவர் பக்கங்களை நேரடியாக சரிபார்க்கவும்."],
           "te": ["అత్యంత సరళమైన, అంచనా వేయగల మార్గం కోసం, మీకు నచ్చిన ప్రైవేట్ లేదా అంతర్జాతీయ పాఠశాలలో నేరుగా దరఖాస్తు చేసుకోండి — దీనికి MOE ప్రక్రియ అవసరం లేదు, పాఠశాల యొక్క సొంత అడ్మిషన్ మరియు ఫీజులు మాత్రమే ఉంటాయి, ఇవి సింగపూర్‌లో అత్యధికం.",
                  "మీరు ప్రభుత్వ/సహాయక పాఠశాలను కోరుకుంటే మరియు మీ పిల్లవాడు Primary 1 ప్రారంభిస్తుంటే, MOE యొక్క అంతర్జాతీయ-విద్యార్థి నమోదు కాలంలో (సాధారణంగా మేలో ఒక చిన్న కాలం) ఆన్‌లైన్ 'ఆసక్తి' ఫారంను సమర్పించండి — సీటు హామీ ఇవ్వబడదు, ఎందుకంటే సింగపూర్ పౌరులు మరియు PR హోల్డర్లకు మొదట ప్రాధాన్యత ఇవ్వబడుతుంది.",
                  "Primary 2–5 లేదా Secondary 1–3 లో ప్రవేశానికి, మీ పిల్లవాడు సాధారణంగా MOE యొక్క Admissions Exercise for International Students (AEIS) పరీక్ష రాయాలి, ఇది సాధారణంగా సెప్టెంబర్–అక్టోబర్ నెలల్లో జరుగుతుంది, లేదా ఫిబ్రవరి–మార్చిలో జరిగే అనుబంధ S-AEIS రౌండ్ — ఇక్కడ కూడా, పరీక్షలో ఉత్తీర్ణత సాధించడం సీటు ఖాళీ లేకపోతే హామీ ఇవ్వదు.",
                  "Secondary పాఠశాల తర్వాత Junior College కోసం, అంతర్జాతీయ విద్యార్థులు తమకు నచ్చిన JC కి నేరుగా దరఖాస్తు చేసుకుంటారు, సాధారణంగా డిసెంబర్‌లో.",
                  "నమోదు కాలాలు, పరీక్ష తేదీలు మరియు అవసరమైన పత్రాలు ప్రతి సంవత్సరం మారుతూ ఉంటాయి — ఏదైనా తేదీ ఆధారంగా ప్రణాళిక వేసుకునే ముందు MOE యొక్క అంతర్జాతీయ-విద్యార్థి పేజీలను నేరుగా తనిఖీ చేయండి."],
           "ml": ["ഏറ്റവും ലളിതവും പ്രവചനാത്മകവുമായ വഴിക്ക്, നിങ്ങൾക്ക് ഇഷ്ടമുള്ള ഒരു സ്വകാര്യ അല്ലെങ്കിൽ അന്താരാഷ്ട്ര സ്കൂളിൽ നേരിട്ട് അപേക്ഷിക്കുക — ഇതിന് MOE പ്രക്രിയ ആവശ്യമില്ല, സ്കൂളിന്റെ സ്വന്തം അഡ്മിഷനും ഫീസും മാത്രം, ഇത് സിംഗപ്പൂരിലെ ഏറ്റവും ഉയർന്നതാണ്.",
                  "നിങ്ങൾക്ക് ഒരു സർക്കാർ/സഹായക സ്കൂൾ വേണമെങ്കിൽ, നിങ്ങളുടെ കുട്ടി Primary 1 തുടങ്ങുകയാണെങ്കിൽ, MOE യുടെ അന്താരാഷ്ട്ര-വിദ്യാർത്ഥി രജിസ്ട്രേഷൻ കാലയളവിൽ (സാധാരണയായി മേയിൽ ഒരു ചെറിയ കാലയളവ്) ഓൺലൈനായി ഒരു 'താൽപര്യം' ഫോം സമർപ്പിക്കുക — സീറ്റ് ഉറപ്പില്ല, കാരണം സിംഗപ്പൂർ പൗരന്മാർക്കും PR ഉടമകൾക്കും ആദ്യം മുൻഗണന നൽകുന്നു.",
                  "Primary 2–5 അല്ലെങ്കിൽ Secondary 1–3 ൽ പ്രവേശനത്തിന്, നിങ്ങളുടെ കുട്ടി സാധാരണയായി MOE യുടെ Admissions Exercise for International Students (AEIS) പരീക്ഷ എഴുതേണ്ടിവരും, ഇത് സാധാരണയായി സെപ്റ്റംബർ–ഒക്ടോബർ മാസങ്ങളിൽ നടക്കുന്നു, അല്ലെങ്കിൽ ഫെബ്രുവരി–മാർച്ചിൽ നടക്കുന്ന അനുബന്ധ S-AEIS റൗണ്ട് — ഇവിടെയും, പരീക്ഷ പാസായതുകൊണ്ട് സീറ്റ് ഒഴിവില്ലെങ്കിൽ ഉറപ്പില്ല.",
                  "Secondary സ്കൂളിന് ശേഷം Junior College ന്, അന്താരാഷ്ട്ര വിദ്യാർത്ഥികൾ അവർക്ക് ഇഷ്ടമുള്ള JC ൽ നേരിട്ട് അപേക്ഷിക്കുന്നു, സാധാരണയായി ഡിസംബറിൽ.",
                  "രജിസ്ട്രേഷൻ കാലയളവുകൾ, പരീക്ഷാ തീയതികൾ, ആവശ്യമായ രേഖകൾ എന്നിവ ഓരോ വർഷവും മാറുന്നു — ഏതെങ്കിലും തീയതി വച്ച് ആസൂത്രണം ചെയ്യുന്നതിന് മുമ്പ് MOE യുടെ അന്താരാഷ്ട്ര-വിദ്യാർത്ഥി പേജുകൾ നേരിട്ട് പരിശോധിക്കുക."]},
    docs={"en": ["Child's passport and Dependant's Pass/Student's Pass", "Birth certificate", "Previous school transcripts or report cards (with an official English translation if not already in English)", "Passport-size photo"],
          "hi": ["बच्चे का पासपोर्ट और Dependant's Pass/Student's Pass", "जन्म प्रमाणपत्र", "पिछले स्कूल की मार्कशीट या रिपोर्ट कार्ड (अगर अंग्रेज़ी में नहीं हैं तो आधिकारिक अंग्रेज़ी अनुवाद सहित)", "पासपोर्ट साइज़ फ़ोटो"],
          "ta": ["குழந்தையின் பாஸ்போர்ட் மற்றும் Dependant's Pass/Student's Pass", "பிறப்புச் சான்றிதழ்", "முந்தைய பள்ளியின் மதிப்பெண் பட்டியல் அல்லது அறிக்கை அட்டை (ஆங்கிலத்தில் இல்லையென்றால் அதிகாரப்பூர்வ ஆங்கில மொழிபெயர்ப்புடன்)", "பாஸ்போர்ட் அளவு புகைப்படம்"],
          "te": ["పిల్లల పాస్‌పోర్ట్ మరియు Dependant's Pass/Student's Pass", "జనన ధృవీకరణ పత్రం", "మునుపటి పాఠశాల మార్కుల జాబితా లేదా రిపోర్ట్ కార్డు (ఇంగ్లీష్‌లో లేకపోతే అధికారిక ఇంగ్లీష్ అనువాదంతో)", "పాస్‌పోర్ట్ సైజు ఫోటో"],
          "ml": ["കുട്ടിയുടെ പാസ്‌പോർട്ടും Dependant's Pass/Student's Pass ഉം", "ജനന സർട്ടിഫിക്കറ്റ്", "മുൻ സ്കൂളിന്റെ മാർക്ക് ലിസ്റ്റ് അല്ലെങ്കിൽ റിപ്പോർട്ട് കാർഡ് (ഇംഗ്ലീഷിലല്ലെങ്കിൽ ഔദ്യോഗിക ഇംഗ്ലീഷ് പരിഭാഷയോടെ)", "പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ"]},
    note={"en": "If your child needs a school seat quickly and you can't wait out MOE's process, a private or international school is usually the more reliable near-term option, even though it costs more.",
          "hi": "अगर आपके बच्चे को जल्दी सीट चाहिए और आप MOE की प्रक्रिया के लिए इंतज़ार नहीं कर सकते, तो निजी या अंतरराष्ट्रीय स्कूल आमतौर पर ज़्यादा भरोसेमंद निकट-अवधि विकल्प होता है, भले ही इसकी लागत ज़्यादा हो।",
          "ta": "உங்கள் குழந்தைக்கு விரைவாக ஒரு இடம் தேவைப்பட்டு MOE இன் செயல்முறைக்காக காத்திருக்க முடியாவிட்டால், அதிக செலவு ஆனாலும் ஒரு தனியார் அல்லது சர்வதேச பள்ளி பொதுவாக நம்பகமான குறுகிய-கால தேர்வாக இருக்கும்.",
          "te": "మీ పిల్లలకు త్వరగా సీటు కావాలి మరియు MOE ప్రక్రియ కోసం వేచి ఉండలేకపోతే, ఖర్చు ఎక్కువైనా ప్రైవేట్ లేదా అంతర్జాతీయ పాఠశాల సాధారణంగా మరింత నమ్మదగిన స్వల్పకాలిక ఎంపిక.",
          "ml": "നിങ്ങളുടെ കുട്ടിക്ക് വേഗത്തിൽ ഒരു സീറ്റ് വേണമെങ്കിലും MOE യുടെ പ്രക്രിയയ്ക്കായി കാത്തിരിക്കാൻ കഴിയുന്നില്ലെങ്കിലും, ചെലവ് കൂടുതലാണെങ്കിലും ഒരു സ്വകാര്യ അല്ലെങ്കിൽ അന്താരാഷ്ട്ര സ്കൂൾ സാധാരണയായി കൂടുതൽ വിശ്വസനീയമായ ഹ്രസ്വകാല ഓപ്ഷനാണ്."},
    location={"en": "Apply online via MOE (government-school pathway) or directly with the school of your choice (private/international pathway)",
               "hi": "MOE के ज़रिए ऑनलाइन आवेदन करें (सरकारी-स्कूल मार्ग) या सीधे अपनी पसंद के स्कूल से संपर्क करें (निजी/अंतरराष्ट्रीय मार्ग)",
               "ta": "MOE வழியாக ஆன்லைனில் விண்ணப்பிக்கவும் (அரசு-பள்ளி வழி) அல்லது உங்கள் விருப்பமான பள்ளியை நேரடியாக தொடர்பு கொள்ளவும் (தனியார்/சர்வதேச வழி)",
               "te": "MOE ద్వారా ఆన్‌లైన్‌లో దరఖాస్తు చేసుకోండి (ప్రభుత్వ-పాఠశాల మార్గం) లేదా మీకు నచ్చిన పాఠశాలను నేరుగా సంప్రదించండి (ప్రైవేట్/అంతర్జాతీయ మార్గం)",
               "ml": "MOE വഴി ഓൺലൈനായി അപേക്ഷിക്കുക (സർക്കാർ-സ്കൂൾ മാർഗം) അല്ലെങ്കിൽ നിങ്ങൾക്ക് ഇഷ്ടമുള്ള സ്കൂളുമായി നേരിട്ട് ബന്ധപ്പെടുക (സ്വകാര്യ/അന്താരാഷ്ട്ര മാർഗം)"},
    phone=None, email=None,
    links=[
        {"href": "https://www.moe.gov.sg/international-students", "label": {"en": "↗ MOE — international students", "hi": "↗ MOE — अंतरराष्ट्रीय छात्र", "ta": "↗ MOE — சர்வதேச மாணவர்கள்", "te": "↗ MOE — అంతర్జాతీయ విద్యార్థులు", "ml": "↗ MOE — അന്താരാഷ്ട്ര വിദ്യാർത്ഥികൾ"}},
        {"href": "https://www.moe.gov.sg/primary/p1-registration/international-students", "label": {"en": "↗ MOE — P1 registration, international students", "hi": "↗ MOE — P1 पंजीकरण, अंतरराष्ट्रीय छात्र", "ta": "↗ MOE — P1 பதிவு, சர்வதேச மாணவர்கள்", "te": "↗ MOE — P1 నమోదు, అంతర్జాతీయ విద్యార్థులు", "ml": "↗ MOE — P1 രജിസ്ട്രേഷൻ, അന്താരാഷ്ട്ര വിദ്യാർത്ഥികൾ"}},
        {"href": "https://www.moe.gov.sg/international-students/aeis", "label": {"en": "↗ MOE — AEIS / S-AEIS", "hi": "↗ MOE — AEIS / S-AEIS", "ta": "↗ MOE — AEIS / S-AEIS", "te": "↗ MOE — AEIS / S-AEIS", "ml": "↗ MOE — AEIS / S-AEIS"}},
    ],
)

entry(
    category="sg_settling", country="singapore", badge_official=True, passes=["EP", "SPass", "WP"],
    search_en="medical insurance work permit s pass mom requirement healthcare foreigner medisave",
    title={"en": "Medical insurance for work pass holders", "hi": "वर्क पास धारकों के लिए मेडिकल बीमा", "ta": "வேலை பாஸ் வைத்திருப்பவர்களுக்கான மருத்துவ காப்பீடு",
           "te": "వర్క్ పాస్ హోల్డర్ల కోసం వైద్య బీమా", "ml": "വർക്ക് പാസ് ഉടമകൾക്കുള്ള മെഡിക്കൽ ഇൻഷുറൻസ്"},
    desc={"en": "As a foreigner without PR status, you don't have access to MediSave or CPF-linked healthcare subsidies — so the insurance your employer provides (or doesn't) matters a lot more here than it might have back home.",
          "hi": "PR दर्जा न होने के कारण, विदेशी के रूप में आपको MediSave या CPF से जुड़ी स्वास्थ्य सब्सिडी नहीं मिलती — इसलिए आपका नियोक्ता जो बीमा देता है (या नहीं देता), वह यहाँ आपके गृह देश की तुलना में कहीं ज़्यादा मायने रखता है।",
          "ta": "PR அந்தஸ்து இல்லாத வெளிநாட்டவராக, உங்களுக்கு MediSave அல்லது CPF-தொடர்பான சுகாதார மானியங்கள் கிடைக்காது — எனவே உங்கள் முதலாளி வழங்கும் (அல்லது வழங்காத) காப்பீடு உங்கள் சொந்த நாட்டை விட இங்கு மிக முக்கியமானது.",
          "te": "PR హోదా లేని విదేశీయుడిగా, మీకు MediSave లేదా CPF-అనుసంధానిత ఆరోగ్య సబ్సిడీలు అందుబాటులో ఉండవు — కాబట్టి మీ యజమాని అందించే (లేదా అందించని) బీమా ఇక్కడ మీ సొంత దేశంలో కంటే చాలా ఎక్కువ ప్రాముఖ్యత కలిగి ఉంటుంది.",
          "ml": "PR പദവിയില്ലാത്ത ഒരു വിദേശിയെന്ന നിലയിൽ, നിങ്ങൾക്ക് MediSave അല്ലെങ്കിൽ CPF-ബന്ധിത ആരോഗ്യ സബ്‌സിഡികൾ ലഭ്യമല്ല — അതിനാൽ നിങ്ങളുടെ തൊഴിലുടമ നൽകുന്ന (അല്ലെങ്കിൽ നൽകാത്ത) ഇൻഷുറൻസ് ഇവിടെ നിങ്ങളുടെ സ്വന്തം നാട്ടിലേതിനേക്കാൾ വളരെ പ്രധാനമാണ്."},
    handles={"en": "employer-provided cover · MOM requirement (WP/S Pass) · private top-ups", "hi": "नियोक्ता-प्रदत्त कवर · MOM आवश्यकता (WP/S Pass) · निजी टॉप-अप",
             "ta": "முதலாளி வழங்கும் காப்பீடு · MOM தேவை (WP/S Pass) · தனியார் கூடுதல் காப்பீடு", "te": "యజమాని అందించే కవర్ · MOM అవసరం (WP/S Pass) · ప్రైవేట్ టాప్-అప్‌లు",
             "ml": "തൊഴിലുടമ നൽകുന്ന കവർ · MOM ആവശ്യകത (WP/S Pass) · സ്വകാര്യ ടോപ്പ്-അപ്പുകൾ"},
    steps={"en": ["If you hold a Work Permit or S Pass, your employer is legally required to buy and maintain medical insurance covering at least S$60,000 a year in inpatient care and day surgery for you, for as long as your pass is valid — and they cannot pass this cost on to you.",
                  "Ask your HR/employer for your policy number, insurer name, and the claims process, so you're not scrambling to find this information during an actual hospital visit.",
                  "If you hold an Employment Pass, check what medical coverage your employer provides — this exact S$60,000 minimum isn't mandated by MOM for EP holders the way it is for Work Permit and S Pass holders, so coverage varies company to company.",
                  "Remember that the mandated minimum covers inpatient care and day surgery only — it typically doesn't cover routine outpatient GP visits, dental care, or your family members, so budget for those separately or ask if your employer's plan extends further.",
                  "Register with a GP clinic near your home for everyday care, and keep your insurance card and policy documents somewhere you can find quickly."],
           "hi": ["अगर आपके पास Work Permit या S Pass है, तो आपके नियोक्ता के लिए क़ानूनन ज़रूरी है कि वह आपके लिए कम से कम S$60,000 प्रति वर्ष का मेडिकल बीमा ख़रीदे और बनाए रखे, जो अस्पताल में भर्ती (inpatient) और डे-सर्जरी को कवर करे, जब तक आपका पास वैध है — और वे यह लागत आप पर नहीं डाल सकते।",
                  "अपने HR/नियोक्ता से अपनी पॉलिसी नंबर, बीमा कंपनी का नाम, और दावा प्रक्रिया के बारे में पूछें, ताकि असली अस्पताल जाने की स्थिति में आपको यह जानकारी ढूँढ़नी न पड़े।",
                  "अगर आपके पास Employment Pass है, तो जाँच लें कि आपका नियोक्ता कौन-सा मेडिकल कवर देता है — यह ठीक S$60,000 की न्यूनतम राशि MOM द्वारा EP धारकों के लिए अनिवार्य नहीं है, जैसा Work Permit और S Pass धारकों के लिए है, इसलिए कवर हर कंपनी में अलग-अलग होता है।",
                  "याद रखें कि अनिवार्य न्यूनतम केवल अस्पताल भर्ती और डे-सर्जरी को कवर करता है — इसमें आमतौर पर सामान्य आउटपेशेंट GP विज़िट, डेंटल केयर, या आपके परिवार के सदस्य शामिल नहीं होते, इसलिए इनके लिए अलग से बजट बनाएँ या अपने नियोक्ता से पूछें कि क्या उनकी योजना इससे आगे तक फैली है।",
                  "रोज़मर्रा की देखभाल के लिए अपने घर के पास किसी GP क्लिनिक में पंजीकरण कराएँ, और अपना बीमा कार्ड व पॉलिसी दस्तावेज़ ऐसी जगह रखें जहाँ आप उन्हें जल्दी ढूँढ़ सकें।"],
           "ta": ["உங்களிடம் Work Permit அல்லது S Pass இருந்தால், உங்கள் பாஸ் செல்லுபடியாகும் வரை, ஆண்டுக்கு குறைந்தபட்சம் S$60,000 உள்நோயாளி பராமரிப்பு மற்றும் டே-சர்ஜரிக்கான மருத்துவ காப்பீட்டை உங்கள் முதலாளி வாங்கி பராமரிக்க வேண்டியது சட்டப்படி கட்டாயம் — இந்த செலவை அவர்கள் உங்கள் மீது சுமத்த முடியாது.",
                  "உண்மையான மருத்துவமனை வருகையின்போது இந்த தகவலை தேட வேண்டியிராமல் இருக்க, உங்கள் காப்பீட்டு எண், காப்பீட்டு நிறுவனத்தின் பெயர், மற்றும் உரிமைகோரல் செயல்முறையை உங்கள் HR/முதலாளியிடம் கேளுங்கள்.",
                  "உங்களிடம் Employment Pass இருந்தால், உங்கள் முதலாளி என்ன மருத்துவ காப்பீட்டை வழங்குகிறார் என்பதை சரிபார்க்கவும் — இந்த சரியான S$60,000 குறைந்தபட்ச தொகை Work Permit மற்றும் S Pass வைத்திருப்பவர்களுக்கு போல EP வைத்திருப்பவர்களுக்கு MOM ஆல் கட்டாயப்படுத்தப்படவில்லை, எனவே காப்பீடு ஒவ்வொரு நிறுவனத்திற்கும் வேறுபடும்.",
                  "கட்டாய குறைந்தபட்சம் உள்நோயாளி பராமரிப்பு மற்றும் டே-சர்ஜரியை மட்டுமே உள்ளடக்கும் என்பதை நினைவில் கொள்ளுங்கள் — இது பொதுவாக வழக்கமான வெளிநோயாளி GP வருகைகள், பல் சிகிச்சை, அல்லது உங்கள் குடும்ப உறுப்பினர்களை உள்ளடக்காது, எனவே அவற்றுக்கு தனியாக பட்ஜெட் செய்யுங்கள் அல்லது உங்கள் முதலாளியின் திட்டம் அதற்கு அப்பால் நீட்டிக்கிறதா எனக் கேளுங்கள்.",
                  "அன்றாட பராமரிப்புக்காக உங்கள் வீட்டிற்கு அருகில் உள்ள ஒரு GP கிளினிக்கில் பதிவு செய்யுங்கள், உங்கள் காப்பீட்டு அட்டை மற்றும் பாலிசி ஆவணங்களை நீங்கள் விரைவாகக் கண்டுபிடிக்கக்கூடிய இடத்தில் வைத்திருங்கள்."],
           "te": ["మీకు Work Permit లేదా S Pass ఉంటే, మీ పాస్ చెల్లుబాటులో ఉన్నంత కాలం, సంవత్సరానికి కనీసం S$60,000 ఇన్‌పేషెంట్ కేర్ మరియు డే-సర్జరీని కవర్ చేసే వైద్య బీమాను మీ యజమాని కొనుగోలు చేసి నిర్వహించడం చట్టబద్ధంగా తప్పనిసరి — ఈ ఖర్చును వారు మీపై మోపలేరు.",
                  "అసలైన ఆసుపత్రి సందర్శన సమయంలో ఈ సమాచారం కోసం వెతకకుండా ఉండటానికి, మీ పాలసీ నంబర్, ఇన్సూరర్ పేరు, క్లెయిమ్ ప్రక్రియను మీ HR/యజమానిని అడగండి.",
                  "మీకు Employment Pass ఉంటే, మీ యజమాని ఏ వైద్య కవరేజీని అందిస్తారో తనిఖీ చేయండి — Work Permit మరియు S Pass హోల్డర్లకు వర్తించే ఈ ఖచ్చితమైన S$60,000 కనీస మొత్తం EP హోల్డర్లకు MOM తప్పనిసరి చేయలేదు, కాబట్టి కవరేజీ కంపెనీని బట్టి మారుతుంది.",
                  "తప్పనిసరి కనీస మొత్తం ఇన్‌పేషెంట్ కేర్ మరియు డే-సర్జరీని మాత్రమే కవర్ చేస్తుందని గుర్తుంచుకోండి — ఇది సాధారణంగా రొటీన్ అవుట్‌పేషెంట్ GP సందర్శనలు, దంత సంరక్షణ, లేదా మీ కుటుంబ సభ్యులను కవర్ చేయదు, కాబట్టి వాటికి విడిగా బడ్జెట్ వేసుకోండి లేదా మీ యజమాని ప్లాన్ దానికి మించి విస్తరిస్తుందా అని అడగండి.",
                  "రోజువారీ సంరక్షణ కోసం మీ ఇంటికి సమీపంలో ఉన్న GP క్లినిక్‌లో నమోదు చేసుకోండి, మీ బీమా కార్డు మరియు పాలసీ పత్రాలను మీరు త్వరగా కనుగొనగల చోట ఉంచుకోండి."],
           "ml": ["നിങ്ങൾക്ക് Work Permit അല്ലെങ്കിൽ S Pass ഉണ്ടെങ്കിൽ, നിങ്ങളുടെ പാസ് സാധുവായിരിക്കുന്നിടത്തോളം, വർഷത്തിൽ കുറഞ്ഞത് S$60,000 ഇൻപേഷ്യന്റ് കെയറും ഡേ-സർജറിയും ഉൾക്കൊള്ളുന്ന മെഡിക്കൽ ഇൻഷുറൻസ് നിങ്ങളുടെ തൊഴിലുടമ വാങ്ങി പരിപാലിക്കേണ്ടത് നിയമപരമായി നിർബന്ധമാണ് — ഈ ചെലവ് അവർക്ക് നിങ്ങളുടെ മേൽ ചുമത്താൻ കഴിയില്ല.",
                  "യഥാർത്ഥ ആശുപത്രി സന്ദർശന സമയത്ത് ഈ വിവരങ്ങൾ തിരയേണ്ടി വരാതിരിക്കാൻ, നിങ്ങളുടെ പോളിസി നമ്പർ, ഇൻഷുറർ പേര്, ക്ലെയിം പ്രക്രിയ എന്നിവ നിങ്ങളുടെ HR/തൊഴിലുടമയോട് ചോദിക്കുക.",
                  "നിങ്ങൾക്ക് Employment Pass ഉണ്ടെങ്കിൽ, നിങ്ങളുടെ തൊഴിലുടമ എന്ത് മെഡിക്കൽ കവറേജ് നൽകുന്നു എന്ന് പരിശോധിക്കുക — Work Permit, S Pass ഉടമകൾക്കുള്ളതു പോലെ ഈ കൃത്യമായ S$60,000 മിനിമം തുക EP ഉടമകൾക്ക് MOM നിർബന്ധമാക്കിയിട്ടില്ല, അതിനാൽ കവറേജ് ഓരോ കമ്പനിക്കും വ്യത്യസ്തമാണ്.",
                  "നിർബന്ധിത മിനിമം ഇൻപേഷ്യന്റ് കെയറും ഡേ-സർജറിയും മാത്രമേ ഉൾക്കൊള്ളൂ എന്ന് ഓർക്കുക — ഇത് സാധാരണയായി പതിവ് ഔട്ട്പേഷ്യന്റ് GP സന്ദർശനങ്ങൾ, ദന്ത സംരക്ഷണം, അല്ലെങ്കിൽ നിങ്ങളുടെ കുടുംബാംഗങ്ങളെ ഉൾക്കൊള്ളില്ല, അതിനാൽ അതിനായി പ്രത്യേകം ബജറ്റ് ചെയ്യുക അല്ലെങ്കിൽ നിങ്ങളുടെ തൊഴിലുടമയുടെ പ്ലാൻ അതിനപ്പുറം വ്യാപിക്കുന്നുണ്ടോ എന്ന് ചോദിക്കുക.",
                  "ദൈനംദിന പരിചരണത്തിനായി നിങ്ങളുടെ വീടിനടുത്തുള്ള ഒരു GP ക്ലിനിക്കിൽ രജിസ്റ്റർ ചെയ്യുക, നിങ്ങളുടെ ഇൻഷുറൻസ് കാർഡും പോളിസി രേഖകളും വേഗത്തിൽ കണ്ടെത്താൻ കഴിയുന്ന സ്ഥലത്ത് സൂക്ഷിക്കുക."]},
    docs={"en": ["Your work pass card", "Insurance policy document/card from your employer", "Passport"],
          "hi": ["आपका वर्क पास कार्ड", "आपके नियोक्ता से बीमा पॉलिसी दस्तावेज़/कार्ड", "पासपोर्ट"],
          "ta": ["உங்கள் வேலை பாஸ் அட்டை", "உங்கள் முதலாளியிடமிருந்து காப்பீட்டு பாலிசி ஆவணம்/அட்டை", "பாஸ்போர்ட்"],
          "te": ["మీ వర్క్ పాస్ కార్డు", "మీ యజమాని నుండి బీమా పాలసీ పత్రం/కార్డు", "పాస్‌పోర్ట్"],
          "ml": ["നിങ്ങളുടെ വർക്ക് പാസ് കാർഡ്", "നിങ്ങളുടെ തൊഴിലുടമയിൽ നിന്നുള്ള ഇൻഷുറൻസ് പോളിസി രേഖ/കാർഡ്", "പാസ്‌പോർട്ട്"]},
    note={"en": "Because you won't have MediSave to fall back on, a gap in employer coverage is a real out-of-pocket risk — it's worth confirming what's covered before you need it, not after.",
          "hi": "क्योंकि आपके पास MediSave का सहारा नहीं होगा, नियोक्ता के कवर में कोई कमी असल में आपकी अपनी जेब का जोखिम बन जाती है — इसकी ज़रूरत पड़ने से पहले ही यह पुष्टि कर लेना बेहतर है कि क्या कवर है, बाद में नहीं।",
          "ta": "உங்களிடம் MediSave நம்பிக்கை இல்லாததால், முதலாளியின் காப்பீட்டில் உள்ள இடைவெளி உண்மையான சொந்த-செலவு ஆபத்தாக இருக்கும் — இது தேவைப்படுவதற்கு முன்பே என்ன உள்ளடக்கப்பட்டுள்ளது என்பதை உறுதிப்படுத்துவது நல்லது, தேவைப்பட்ட பிறகு அல்ல.",
          "te": "మీకు MediSave ఆధారం ఉండదు కాబట్టి, యజమాని కవరేజీలో ఏదైనా లోపం నిజమైన జేబు నుండి చెల్లించే ప్రమాదంగా మారుతుంది — అవసరం రాకముందే ఏమి కవర్ అవుతుందో నిర్ధారించుకోవడం మంచిది, తర్వాత కాదు.",
          "ml": "നിങ്ങൾക്ക് MediSave ഇല്ലാത്തതിനാൽ, തൊഴിലുടമയുടെ കവറേജിലെ ഒരു വിടവ് യഥാർത്ഥ പോക്കറ്റ് ചെലവ് അപകടസാധ്യതയാണ് — ഇത് ആവശ്യമായി വരുന്നതിന് മുമ്പ് എന്താണ് കവർ ചെയ്യുന്നതെന്ന് സ്ഥിരീകരിക്കുന്നത് നല്ലതാണ്, ശേഷമല്ല."},
    location={"en": "Your employer's HR department (mandated cover); private insurers for anything beyond it",
               "hi": "आपके नियोक्ता का HR विभाग (अनिवार्य कवर); इससे आगे के लिए निजी बीमा कंपनियाँ",
               "ta": "உங்கள் முதலாளியின் HR துறை (கட்டாய காப்பீடு); அதற்கு அப்பால் தனியார் காப்பீட்டு நிறுவனங்கள்",
               "te": "మీ యజమాని HR విభాగం (తప్పనిసరి కవరేజీ); దానికి మించినదానికి ప్రైవేట్ ఇన్సూరర్లు",
               "ml": "നിങ്ങളുടെ തൊഴിലുടമയുടെ HR വകുപ്പ് (നിർബന്ധിത കവറേജ്); അതിനപ്പുറമുള്ളതിന് സ്വകാര്യ ഇൻഷുറർമാർ"},
    phone=None, email=None,
    links=[
        {"href": "https://www.mom.gov.sg/passes-and-permits/s-pass/medical-insurance", "label": {"en": "↗ MOM — S Pass medical insurance", "hi": "↗ MOM — S Pass मेडिकल बीमा", "ta": "↗ MOM — S Pass மருத்துவ காப்பீடு", "te": "↗ MOM — S Pass వైద్య బీమా", "ml": "↗ MOM — S Pass മെഡിക്കൽ ഇൻഷുറൻസ്"}},
        {"href": "https://www.mom.gov.sg/faq/work-permit-for-foreign-worker/are-the-enhanced-medical-insurance-requirements-compulsory", "label": {"en": "↗ MOM — FAQ on medical insurance rules", "hi": "↗ MOM — मेडिकल बीमा नियम FAQ", "ta": "↗ MOM — மருத்துவ காப்பீடு விதிகள் FAQ", "te": "↗ MOM — వైద్య బీమా నియమాల FAQ", "ml": "↗ MOM — മെഡിക്കൽ ഇൻഷുറൻസ് ചട്ടങ്ങൾ FAQ"}},
    ],
)

entry(
    category="sg_consular", country="singapore", badge_official=True,
    search_en="bls international singapore oci passport renewal visa centre anson road sim lim tower",
    toggle_key="how_to_use",
    title={"en": "OCI & passport services from Singapore", "hi": "सिंगापुर से OCI और पासपोर्ट सेवाएँ", "ta": "சிங்கப்பூரிலிருந்து OCI & பாஸ்போர்ட் சேவைகள்",
           "te": "సింగపూర్ నుండి OCI & పాస్‌పోర్ట్ సేవలు", "ml": "സിംഗപ്പൂരിൽ നിന്നുള്ള OCI, പാസ്‌പോർട്ട് സേവനങ്ങൾ"},
    desc={"en": "The Passport, OCI and PCC services described earlier in this guide are handled in Singapore through BLS International's outsourced centres, not the High Commission counter directly — here's exactly where to go.",
          "hi": "इस गाइड में पहले बताई गई पासपोर्ट, OCI और PCC सेवाएँ सिंगापुर में BLS इंटरनेशनल के आउटसोर्स्ड केंद्रों के ज़रिए संभाली जाती हैं, सीधे उच्चायोग के काउंटर से नहीं — यहाँ बताया गया है कि बिल्कुल कहाँ जाना है।",
          "ta": "இந்த வழிகாட்டியில் முன்பு விவரிக்கப்பட்ட பாஸ்போர்ட், OCI மற்றும் PCC சேவைகள் சிங்கப்பூரில் BLS இன்டர்நேஷனலின் அவுட்சோர்ஸ் செய்யப்பட்ட மையங்கள் மூலம் கையாளப்படுகின்றன, நேரடியாக உயர்ஸ்தானிகர் அலுவலக கவுன்டரில் அல்ல — சரியாக எங்கு செல்ல வேண்டும் என்பது இங்கே.",
          "te": "ఈ గైడ్‌లో ముందు వివరించిన పాస్‌పోర్ట్, OCI మరియు PCC సేవలు సింగపూర్‌లో BLS ఇంటర్నేషనల్ యొక్క అవుట్‌సోర్స్డ్ కేంద్రాల ద్వారా నిర్వహించబడతాయి, నేరుగా హైకమిషన్ కౌంటర్ ద్వారా కాదు — సరిగ్గా ఎక్కడికి వెళ్లాలో ఇక్కడ ఉంది.",
          "ml": "ഈ ഗൈഡിൽ നേരത്തെ വിവരിച്ച പാസ്‌പോർട്ട്, OCI, PCC സേവനങ്ങൾ സിംഗപ്പൂരിൽ BLS ഇന്റർനാഷണലിന്റെ ഔട്ട്‌സോഴ്‌സ്ഡ് കേന്ദ്രങ്ങൾ വഴിയാണ് കൈകാര്യം ചെയ്യുന്നത്, നേരിട്ട് ഹൈക്കമ്മീഷൻ കൗണ്ടറിലല്ല — കൃത്യമായി എവിടെ പോകണം എന്നത് ഇതാ."},
    handles={"en": "BLS International · document submission · booklet collection", "hi": "BLS इंटरनेशनल · दस्तावेज़ जमा करना · बुकलेट संग्रह",
             "ta": "BLS இன்டர்நேஷனல் · ஆவண சமர்ப்பிப்பு · புத்தக சேகரிப்பு", "te": "BLS ఇంటర్నేషనల్ · పత్రాల సమర్పణ · బుక్‌లెట్ సేకరణ",
             "ml": "BLS ഇന്റർനാഷണൽ · രേഖ സമർപ്പണം · ബുക്ക്‌ലെറ്റ് ശേഖരണം"},
    steps={"en": ["For most passport, OCI, PCC and visa-related document submissions, book an appointment and go to a BLS International Singapore centre — either the CBD centre (Anson Road) or the Little India centre (Sim Lim Tower); both handle the same range of services.",
                  "Both centres take document/visa submissions on weekday mornings only (roughly 9:00 AM–1:00 PM for visa submissions, 9:00 AM–3:45 PM for other document submissions) — plan to arrive early, as slots fill up.",
                  "Track your application status online through BLS's tracking portal rather than calling repeatedly — phone lines are often busy during peak hours.",
                  "For collecting a completed passport booklet or physical OCI card directly (rather than through BLS), or for anything that specifically needs the High Commission itself, the HCI Singapore office is at 31 Grange Road.",
                  "If you have a genuine emergency — a lost passport, a medical situation, or a death requiring urgent document work — BLS's emergency line is for exactly this, not routine queries."],
           "hi": ["अधिकांश पासपोर्ट, OCI, PCC और वीज़ा-संबंधी दस्तावेज़ जमा करने के लिए, अपॉइंटमेंट बुक करें और BLS इंटरनेशनल सिंगापुर के किसी केंद्र पर जाएँ — या तो CBD केंद्र (Anson Road) या लिटिल इंडिया केंद्र (Sim Lim Tower); दोनों समान सेवाएँ देते हैं।",
                  "दोनों केंद्र दस्तावेज़/वीज़ा जमा करना केवल कार्यदिवस की सुबह लेते हैं (वीज़ा जमा के लिए लगभग सुबह 9:00–दोपहर 1:00 बजे, अन्य दस्तावेज़ जमा के लिए सुबह 9:00–दोपहर 3:45 बजे) — जल्दी पहुँचने की योजना बनाएँ, क्योंकि स्लॉट भर जाते हैं।",
                  "बार-बार फ़ोन करने के बजाय BLS के ट्रैकिंग पोर्टल के ज़रिए ऑनलाइन अपनी आवेदन स्थिति ट्रैक करें — व्यस्त समय में फ़ोन लाइनें अक्सर व्यस्त रहती हैं।",
                  "पूर्ण पासपोर्ट बुकलेट या भौतिक OCI कार्ड सीधे लेने के लिए (BLS के बजाय), या किसी ऐसी चीज़ के लिए जिसके लिए विशेष रूप से उच्चायोग की ज़रूरत हो, HCI सिंगापुर कार्यालय 31 Grange Road पर है।",
                  "अगर आपके पास कोई वास्तविक आपातकाल है — खोया हुआ पासपोर्ट, कोई चिकित्सा स्थिति, या मृत्यु जिसके लिए तत्काल दस्तावेज़ी काम चाहिए — BLS की आपातकालीन लाइन ठीक इसी के लिए है, सामान्य सवालों के लिए नहीं।"],
           "ta": ["பெரும்பாலான பாஸ்போர்ட், OCI, PCC மற்றும் விசா தொடர்பான ஆவண சமர்ப்பிப்புகளுக்கு, ஒரு அப்பாயின்ட்மென்ட் பதிவு செய்து BLS இன்டர்நேஷனல் சிங்கப்பூர் மையத்திற்குச் செல்லுங்கள் — CBD மையம் (Anson Road) அல்லது லிட்டில் இந்தியா மையம் (Sim Lim Tower); இரண்டும் ஒரே வகையான சேவைகளை வழங்குகின்றன.",
                  "இரண்டு மையங்களும் வார நாள் காலை நேரங்களில் மட்டுமே ஆவணம்/விசா சமர்ப்பிப்புகளை எடுக்கின்றன (விசா சமர்ப்பிப்புக்கு தோராயமாக காலை 9:00–மதியம் 1:00; மற்ற ஆவண சமர்ப்பிப்புக்கு காலை 9:00–மதியம் 3:45) — ஸ்லாட்கள் நிரம்பிவிடுவதால் சீக்கிரம் வர திட்டமிடுங்கள்.",
                  "மீண்டும் மீண்டும் அழைப்பதற்குப் பதிலாக BLS இன் டிராக்கிங் போர்ட்டல் மூலம் உங்கள் விண்ணப்ப நிலையை ஆன்லைனில் கண்காணிக்கவும் — உச்ச நேரங்களில் தொலைபேசி வரிசைகள் அடிக்கடி பிஸியாக இருக்கும்.",
                  "முடிக்கப்பட்ட பாஸ்போர்ட் புத்தகம் அல்லது உடல் ரீதியான OCI அட்டையை நேரடியாக பெற (BLS மூலம் அல்லாமல்), அல்லது குறிப்பாக உயர்ஸ்தானிகர் அலுவலகமே தேவைப்படும் எதற்கும், HCI சிங்கப்பூர் அலுவலகம் 31 Grange Road இல் உள்ளது.",
                  "உங்களுக்கு உண்மையான அவசரநிலை இருந்தால் — தொலைந்த பாஸ்போர்ட், மருத்துவ நிலைமை, அல்லது அவசர ஆவண வேலை தேவைப்படும் மரணம் — BLS இன் அவசர வரி இதற்காகவே உள்ளது, வழக்கமான கேள்விகளுக்கு அல்ல."],
           "te": ["చాలా పాస్‌పోర్ట్, OCI, PCC మరియు వీసా సంబంధిత పత్రాల సమర్పణల కోసం, అపాయింట్‌మెంట్ బుక్ చేసుకుని BLS ఇంటర్నేషనల్ సింగపూర్ కేంద్రానికి వెళ్లండి — CBD కేంద్రం (Anson Road) లేదా లిటిల్ ఇండియా కేంద్రం (Sim Lim Tower); రెండూ ఒకే రకమైన సేవలను నిర్వహిస్తాయి.",
                  "రెండు కేంద్రాలు వారంరోజు ఉదయం మాత్రమే పత్రాలు/వీసా సమర్పణలను తీసుకుంటాయి (వీసా సమర్పణకు దాదాపు ఉదయం 9:00–మధ్యాహ్నం 1:00; ఇతర పత్రాల సమర్పణకు ఉదయం 9:00–మధ్యాహ్నం 3:45) — స్లాట్‌లు నిండిపోతాయి కాబట్టి ముందుగా చేరుకునేలా ప్లాన్ చేసుకోండి.",
                  "పదే పదే ఫోన్ చేయడానికి బదులుగా BLS ట్రాకింగ్ పోర్టల్ ద్వారా ఆన్‌లైన్‌లో మీ దరఖాస్తు స్థితిని ట్రాక్ చేయండి — పీక్ సమయాల్లో ఫోన్ లైన్లు తరచుగా బిజీగా ఉంటాయి.",
                  "పూర్తయిన పాస్‌పోర్ట్ బుక్‌లెట్ లేదా భౌతిక OCI కార్డును నేరుగా తీసుకోవడానికి (BLS ద్వారా కాకుండా), లేదా ప్రత్యేకంగా హైకమిషన్ అవసరమయ్యే దేనికైనా, HCI సింగపూర్ కార్యాలయం 31 Grange Road వద్ద ఉంది.",
                  "మీకు నిజమైన అత్యవసర పరిస్థితి ఉంటే — పోగొట్టుకున్న పాస్‌పోర్ట్, వైద్య పరిస్థితి, లేదా అత్యవసర పత్రాల పని అవసరమైన మరణం — BLS యొక్క అత్యవసర లైన్ సరిగ్గా దీని కోసమే, సాధారణ ప్రశ్నల కోసం కాదు."],
           "ml": ["മിക്ക പാസ്‌പോർട്ട്, OCI, PCC, വിസ സംബന്ധിയായ രേഖാ സമർപ്പണങ്ങൾക്കും, ഒരു അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്ത് BLS ഇന്റർനാഷണൽ സിംഗപ്പൂർ കേന്ദ്രത്തിലേക്ക് പോകുക — CBD കേന്ദ്രം (Anson Road) അല്ലെങ്കിൽ ലിറ്റിൽ ഇന്ത്യ കേന്ദ്രം (Sim Lim Tower); രണ്ടും ഒരേ സേവനങ്ങൾ കൈകാര്യം ചെയ്യുന്നു.",
                  "രണ്ട് കേന്ദ്രങ്ങളും പ്രവൃത്തി ദിവസങ്ങളിലെ രാവിലെ മാത്രമേ രേഖ/വിസ സമർപ്പണങ്ങൾ സ്വീകരിക്കൂ (വിസ സമർപ്പണത്തിന് ഏകദേശം രാവിലെ 9:00–ഉച്ചയ്ക്ക് 1:00; മറ്റ് രേഖാ സമർപ്പണത്തിന് രാവിലെ 9:00–ഉച്ചയ്ക്ക് 3:45) — സ്ലോട്ടുകൾ നിറയുന്നതിനാൽ നേരത്തെ എത്താൻ പദ്ധതിയിടുക.",
                  "വീണ്ടും വീണ്ടും വിളിക്കുന്നതിന് പകരം BLS ന്റെ ട്രാക്കിംഗ് പോർട്ടൽ വഴി നിങ്ങളുടെ അപേക്ഷയുടെ സ്ഥിതി ഓൺലൈനിൽ ട്രാക്ക് ചെയ്യുക — തിരക്കുള്ള സമയങ്ങളിൽ ഫോൺ ലൈനുകൾ പലപ്പോഴും തിരക്കിലായിരിക്കും.",
                  "പൂർത്തിയായ പാസ്‌പോർട്ട് ബുക്ക്‌ലെറ്റ് അല്ലെങ്കിൽ ഫിസിക്കൽ OCI കാർഡ് നേരിട്ട് ശേഖരിക്കാൻ (BLS വഴിയല്ലാതെ), അല്ലെങ്കിൽ പ്രത്യേകമായി ഹൈക്കമ്മീഷൻ തന്നെ ആവശ്യമുള്ള എന്തിനും, HCI സിംഗപ്പൂർ ഓഫീസ് 31 Grange Road ൽ ആണ്.",
                  "നിങ്ങൾക്ക് യഥാർത്ഥ അടിയന്തരാവസ്ഥ ഉണ്ടെങ്കിൽ — നഷ്ടപ്പെട്ട പാസ്‌പോർട്ട്, ഒരു മെഡിക്കൽ സാഹചര്യം, അല്ലെങ്കിൽ അടിയന്തിര രേഖാ ജോലി ആവശ്യമുള്ള മരണം — BLS ന്റെ എമർജൻസി ലൈൻ കൃത്യമായി ഇതിന് വേണ്ടിയാണ്, പതിവ് അന്വേഷണങ്ങൾക്കല്ല."]},
    docs={"en": ["Whatever the specific service requires (see the Passport/OCI cards above)", "Appointment confirmation", "Payment receipt"],
          "hi": ["जो भी विशिष्ट सेवा के लिए ज़रूरी हो (ऊपर पासपोर्ट/OCI कार्ड देखें)", "अपॉइंटमेंट पुष्टि", "भुगतान रसीद"],
          "ta": ["குறிப்பிட்ட சேவைக்கு தேவையானது எதுவாக இருந்தாலும் (மேலே பாஸ்போர்ட்/OCI அட்டைகளைப் பார்க்கவும்)", "அப்பாயின்ட்மென்ட் உறுதிப்படுத்தல்", "கட்டண ரசீது"],
          "te": ["నిర్దిష్ట సేవకు ఏది అవసరమైనా (పైన పాస్‌పోర్ట్/OCI కార్డులు చూడండి)", "అపాయింట్‌మెంట్ నిర్ధారణ", "చెల్లింపు రసీదు"],
          "ml": ["നിർദ്ദിഷ്ട സേവനത്തിന് എന്ത് ആവശ്യമായാലും (മുകളിൽ പാസ്‌പോർട്ട്/OCI കാർഡുകൾ കാണുക)", "അപ്പോയിന്റ്മെന്റ് സ്ഥിരീകരണം", "പേയ്‌മെന്റ് രസീത്"]},
    note={"en": "BLS is a private outsourced partner, not the High Commission itself — for policy questions, delays, or anything BLS can't resolve, escalate to the High Commission through MADAD (see the consular section above).",
          "hi": "BLS एक निजी आउटसोर्स्ड भागीदार है, उच्चायोग स्वयं नहीं — नीति संबंधी सवालों, देरी, या किसी भी ऐसी चीज़ के लिए जिसे BLS हल न कर सके, MADAD के ज़रिए उच्चायोग तक पहुँचें (ऊपर वाणिज्य दूतावास खंड देखें)।",
          "ta": "BLS ஒரு தனியார் அவுட்சோர்ஸ் பங்குதாரர், உயர்ஸ்தானிகர் அலுவலகம் அல்ல — கொள்கை கேள்விகள், தாமதங்கள், அல்லது BLS தீர்க்க முடியாத எதற்கும், MADAD மூலம் உயர்ஸ்தானிகர் அலுவலகத்திற்கு உயர்த்தவும் (மேலே உள்ள துணைத்தூதரக பிரிவைப் பார்க்கவும்).",
          "te": "BLS ఒక ప్రైవేట్ అవుట్‌సోర్స్డ్ భాగస్వామి, హైకమిషన్ కాదు — విధాన ప్రశ్నలు, ఆలస్యాలు, లేదా BLS పరిష్కరించలేని దేనికైనా, MADAD ద్వారా హైకమిషన్‌కు తెలియజేయండి (పైన కాన్సులర్ విభాగం చూడండి).",
          "ml": "BLS ഒരു സ്വകാര്യ ഔട്ട്‌സോഴ്‌സ്ഡ് പങ്കാളിയാണ്, ഹൈക്കമ്മീഷൻ അല്ല — നയപരമായ ചോദ്യങ്ങൾ, കാലതാമസങ്ങൾ, അല്ലെങ്കിൽ BLS ന് പരിഹരിക്കാൻ കഴിയാത്ത എന്തിനും, MADAD വഴി ഹൈക്കമ്മീഷനിലേക്ക് ഉയർത്തുക (മുകളിലുള്ള കോൺസുലാർ വിഭാഗം കാണുക)."},
    location={"en": "BLS International Singapore — CBD: Unit 30-08, 10 Anson Road, S(079903); Little India: Unit 14-02/04/05, Sim Lim Tower, 10 Jalan Besar, S(208787). High Commission of India: 31 Grange Road, S(239702)",
               "hi": "BLS इंटरनेशनल सिंगापुर — CBD: Unit 30-08, 10 Anson Road, S(079903); लिटिल इंडिया: Unit 14-02/04/05, Sim Lim Tower, 10 Jalan Besar, S(208787)। भारतीय उच्चायोग: 31 Grange Road, S(239702)",
               "ta": "BLS இன்டர்நேஷனல் சிங்கப்பூர் — CBD: Unit 30-08, 10 Anson Road, S(079903); லிட்டில் இந்தியா: Unit 14-02/04/05, Sim Lim Tower, 10 Jalan Besar, S(208787). இந்திய உயர்ஸ்தானிகர் அலுவலகம்: 31 Grange Road, S(239702)",
               "te": "BLS ఇంటర్నేషనల్ సింగపూర్ — CBD: Unit 30-08, 10 Anson Road, S(079903); లిటిల్ ఇండియా: Unit 14-02/04/05, Sim Lim Tower, 10 Jalan Besar, S(208787). భారత హైకమిషన్: 31 Grange Road, S(239702)",
               "ml": "BLS ഇന്റർനാഷണൽ സിംഗപ്പൂർ — CBD: Unit 30-08, 10 Anson Road, S(079903); ലിറ്റിൽ ഇന്ത്യ: Unit 14-02/04/05, Sim Lim Tower, 10 Jalan Besar, S(208787). ഇന്ത്യൻ ഹൈക്കമ്മീഷൻ: 31 Grange Road, S(239702)"},
    phone={"en": "BLS: +65 3163 5611 / +65 3163 2615 · Emergency: +65 8402 0819 · High Commission: +65 6737 6777",
           "hi": "BLS: +65 3163 5611 / +65 3163 2615 · आपातकाल: +65 8402 0819 · उच्चायोग: +65 6737 6777",
           "ta": "BLS: +65 3163 5611 / +65 3163 2615 · அவசரம்: +65 8402 0819 · உயர்ஸ்தானிகர் அலுவலகம்: +65 6737 6777",
           "te": "BLS: +65 3163 5611 / +65 3163 2615 · అత్యవసరం: +65 8402 0819 · హైకమిషన్: +65 6737 6777",
           "ml": "BLS: +65 3163 5611 / +65 3163 2615 · അടിയന്തരം: +65 8402 0819 · ഹൈക്കമ്മീഷൻ: +65 6737 6777"},
    email={"en": "Infosg@blsinternational.net / info@blsindia.sg", "hi": "Infosg@blsinternational.net / info@blsindia.sg",
           "ta": "Infosg@blsinternational.net / info@blsindia.sg", "te": "Infosg@blsinternational.net / info@blsindia.sg",
           "ml": "Infosg@blsinternational.net / info@blsindia.sg"},
    links=[
        {"href": "https://www.blsinternational.com/india/singapore/", "label": {"en": "↗ BLS International — Singapore", "hi": "↗ BLS इंटरनेशनल — सिंगापुर", "ta": "↗ BLS இன்டர்நேஷனல் — சிங்கப்பூர்", "te": "↗ BLS ఇంటర్నేషనల్ — సింగపూర్", "ml": "↗ BLS ഇന്റർനാഷണൽ — സിംഗപ്പൂർ"}},
        {"href": "https://www.hcisingapore.gov.in", "label": {"en": "↗ High Commission of India, Singapore", "hi": "↗ भारतीय उच्चायोग, सिंगापुर", "ta": "↗ இந்திய உயர்ஸ்தானிகர் அலுவலகம், சிங்கப்பூர்", "te": "↗ భారత హైకమిషన్, సింగపూర్", "ml": "↗ ഇന്ത്യൻ ഹൈക്കമ്മീഷൻ, സിംഗപ്പൂർ"}},
    ],
)

# ---- Singapore: mobile number (Settling in) ----

entry(
    category="sg_settling", country="singapore", badge_official=True,
    search_en="singapore sim card mobile number prepaid postpaid telco fin registration",
    title={"en": "Getting a Singapore mobile number", "hi": "सिंगापुर मोबाइल नंबर लेना", "ta": "சிங்கப்பூர் மொபைல் எண் பெறுதல்",
           "te": "సింగపూర్ మొబైల్ నంబర్ పొందడం", "ml": "സിംഗപ്പൂർ മൊബൈൽ നമ്പർ നേടൽ"},
    desc={"en": "A local number makes almost everything easier — SingPass 2FA, delivery apps, work calls — and getting one is one of the simplest things to sort out in your first week.",
          "hi": "एक स्थानीय नंबर लगभग हर चीज़ को आसान बना देता है — SingPass 2FA, डिलीवरी ऐप, काम की कॉलें — और इसे पाना आपके पहले हफ़्ते में सबसे आसान कामों में से एक है।",
          "ta": "ஒரு உள்ளூர் எண் கிட்டத்தட்ட எல்லாவற்றையும் எளிதாக்குகிறது — SingPass 2FA, டெலிவரி ஆப்கள், வேலை அழைப்புகள் — இதைப் பெறுவது உங்கள் முதல் வாரத்தில் சரிசெய்ய வேண்டிய எளிதான விஷயங்களில் ஒன்று.",
          "te": "ఒక స్థానిక నంబర్ దాదాపు ప్రతిదాన్ని సులభతరం చేస్తుంది — SingPass 2FA, డెలివరీ యాప్‌లు, పని కాల్‌లు — దీన్ని పొందడం మీ మొదటి వారంలో సర్దుకోవాల్సిన సులభమైన పనుల్లో ఒకటి.",
          "ml": "ഒരു പ്രാദേശിക നമ്പർ മിക്കവാറും എല്ലാം എളുപ്പമാക്കുന്നു — SingPass 2FA, ഡെലിവറി ആപ്പുകൾ, ജോലി കോളുകൾ — ഇത് നേടുന്നത് നിങ്ങളുടെ ആദ്യ ആഴ്ചയിൽ ശരിയാക്കാവുന്ന ഏറ്റവും ലളിതമായ കാര്യങ്ങളിലൊന്നാണ്."},
    handles={"en": "prepaid SIM · postpaid line · telco registration", "hi": "प्रीपेड SIM · पोस्टपेड लाइन · टेल्को पंजीकरण",
             "ta": "prepaid SIM · postpaid இணைப்பு · டெல்கோ பதிவு", "te": "prepaid SIM · postpaid లైన్ · టెల్కో నమోదు",
             "ml": "prepaid SIM · postpaid ലൈൻ · ടെൽകോ രജിസ്ട്രേഷൻ"},
    steps={"en": ["For an instant number with no paperwork fuss, buy a prepaid SIM (Singtel hi!SIM, StarHub, M1, or Circles.Life) from a telco kiosk at Changi Airport, a 7-Eleven, or a telco retail shop — you just need to show your passport for registration, no FIN or pass required.",
                  "If you'd rather have a postpaid line (usually cheaper per GB, with a proper monthly bill), you can apply once you have your FIN and at least a few months left on your pass — most telcos want your pass valid for close to the plan's contract length.",
                  "Bring your passport (and work pass card once you have it) to a telco retail shop; postpaid plans usually also need a local billing address, and sometimes a deposit if you don't yet have a Singapore credit history.",
                  "Top up or activate the SIM at the shop before you leave — you'll be online immediately, which makes everything else on this list (SingPass, banking, maps) much easier.",
                  "If your prepaid SIM's validity is about to run out, top up before it expires — a lapsed prepaid number is usually given away to someone else after a grace period, and you'd lose it."],
           "hi": ["बिना काग़ज़ी झंझट के तुरंत नंबर के लिए, Changi हवाई अड्डे के टेल्को कियोस्क, किसी 7-Eleven, या टेल्को की दुकान से प्रीपेड SIM (Singtel hi!SIM, StarHub, M1, या Circles.Life) ख़रीदें — पंजीकरण के लिए बस पासपोर्ट दिखाना होता है, FIN या पास की ज़रूरत नहीं।",
                  "अगर आप पोस्टपेड लाइन चाहते हैं (आमतौर पर प्रति GB सस्ती, सही मासिक बिल के साथ), तो FIN मिलने और पास में कम से कम कुछ महीने बचे होने पर आवेदन कर सकते हैं — अधिकांश टेल्को चाहते हैं कि आपका पास प्लान की अनुबंध अवधि के क़रीब तक वैध हो।",
                  "अपना पासपोर्ट (और वर्क पास कार्ड मिलने पर वह भी) टेल्को की दुकान पर ले जाएँ; पोस्टपेड प्लान के लिए आमतौर पर स्थानीय बिलिंग पता भी चाहिए, और अगर आपका सिंगापुर क्रेडिट इतिहास नहीं है तो कभी-कभी जमा राशि भी।",
                  "दुकान से निकलने से पहले SIM टॉप-अप या सक्रिय करा लें — आप तुरंत ऑनलाइन हो जाएँगे, जिससे इस सूची की बाक़ी हर चीज़ (SingPass, बैंकिंग, मैप्स) बहुत आसान हो जाती है।",
                  "अगर आपके प्रीपेड SIM की वैधता ख़त्म होने वाली है, तो समाप्त होने से पहले टॉप-अप कर लें — समाप्त हो चुका प्रीपेड नंबर आमतौर पर एक निश्चित अवधि बाद किसी और को दे दिया जाता है, और आप उसे खो देंगे।"],
           "ta": ["காகித சிக்கல் இல்லாமல் உடனடி எண்ணுக்கு, Changi விமான நிலைய டெல்கோ கியோஸ்க், ஒரு 7-Eleven, அல்லது டெல்கோ கடையிலிருந்து prepaid SIM (Singtel hi!SIM, StarHub, M1, அல்லது Circles.Life) வாங்கவும் — பதிவுக்கு பாஸ்போர்ட்டைக் காட்டினால் போதும், FIN அல்லது பாஸ் தேவையில்லை.",
                  "நீங்கள் postpaid இணைப்பை விரும்பினால் (பொதுவாக GB க்கு மலிவானது, சரியான மாத பில்லுடன்), உங்கள் FIN கிடைத்து பாஸில் குறைந்தது சில மாதங்கள் மீதமிருந்தால் விண்ணப்பிக்கலாம் — பெரும்பாலான டெல்கோக்கள் உங்கள் பாஸ் திட்டத்தின் ஒப்பந்த காலத்திற்கு நெருக்கமாக செல்லுபடியாக இருக்க வேண்டும் என விரும்புகின்றன.",
                  "உங்கள் பாஸ்போர்ட்டை (மற்றும் வேலை பாஸ் அட்டை கிடைத்தவுடன் அதையும்) டெல்கோ கடைக்கு எடுத்துச் செல்லுங்கள்; postpaid திட்டங்களுக்கு பொதுவாக உள்ளூர் பில்லிங் முகவரியும், சிங்கப்பூர் கடன் வரலாறு இல்லையென்றால் சில நேரங்களில் வைப்புத்தொகையும் தேவை.",
                  "கடையை விட்டு வெளியேறுவதற்கு முன் SIM ஐ டாப்-அப் செய்யவும் அல்லது செயல்படுத்தவும் — நீங்கள் உடனடியாக ஆன்லைனில் இருப்பீர்கள், இது இந்தப் பட்டியலில் உள்ள மற்ற அனைத்தையும் (SingPass, வங்கி, வரைபடங்கள்) மிக எளிதாக்கும்.",
                  "உங்கள் prepaid SIM இன் செல்லுபடியாகும் தன்மை முடிவடையப் போகிறது என்றால், அது காலாவதியாகும் முன் டாப்-அப் செய்யவும் — காலாவதியான prepaid எண் பொதுவாக ஒரு அவகாசத்திற்குப் பிறகு வேறொருவருக்குக் கொடுக்கப்படும், நீங்கள் அதை இழப்பீர்கள்."],
           "te": ["కాగితం తలనొప్పి లేకుండా తక్షణ నంబర్ కోసం, Changi విమానాశ్రయంలోని టెల్కో కియోస్క్, ఒక 7-Eleven, లేదా టెల్కో దుకాణం నుండి prepaid SIM (Singtel hi!SIM, StarHub, M1, లేదా Circles.Life) కొనండి — నమోదుకు పాస్‌పోర్ట్ చూపిస్తే సరిపోతుంది, FIN లేదా పాస్ అవసరం లేదు.",
                  "మీరు postpaid లైన్ కోరుకుంటే (సాధారణంగా GB కి చౌక, సరైన నెలవారీ బిల్లుతో), మీ FIN వచ్చి పాస్‌లో కనీసం కొన్ని నెలలు మిగిలి ఉంటే దరఖాస్తు చేసుకోవచ్చు — చాలా టెల్కోలు మీ పాస్ ప్లాన్ ఒప్పంద కాలానికి దగ్గరగా చెల్లుబాటులో ఉండాలని కోరుకుంటాయి.",
                  "మీ పాస్‌పోర్ట్‌ను (వర్క్ పాస్ కార్డు వచ్చాక దాన్ని కూడా) టెల్కో దుకాణానికి తీసుకెళ్లండి; postpaid ప్లాన్‌లకు సాధారణంగా స్థానిక బిల్లింగ్ చిరునామా కూడా అవసరం, మీకు సింగపూర్ క్రెడిట్ చరిత్ర లేకపోతే కొన్నిసార్లు డిపాజిట్ కూడా.",
                  "దుకాణం విడిచిపెట్టే ముందు SIM టాప్-అప్ చేయండి లేదా యాక్టివేట్ చేయండి — మీరు వెంటనే ఆన్‌లైన్‌లోకి వస్తారు, ఇది ఈ జాబితాలోని మిగతావన్నీ (SingPass, బ్యాంకింగ్, మ్యాప్‌లు) చాలా సులభతరం చేస్తుంది.",
                  "మీ prepaid SIM చెల్లుబాటు ముగియబోతుంటే, అది గడువు ముగియకముందే టాప్-అప్ చేయండి — గడువు ముగిసిన prepaid నంబర్ సాధారణంగా కొంత గడువు తర్వాత మరొకరికి ఇవ్వబడుతుంది, మీరు దాన్ని కోల్పోతారు."],
           "ml": ["പേപ്പർ ജോലിയില്ലാതെ ഉടനടി നമ്പറിന്, Changi എയർപോർട്ടിലെ ടെൽകോ കിയോസ്ക്, ഒരു 7-Eleven, അല്ലെങ്കിൽ ടെൽകോ കടയിൽ നിന്ന് prepaid SIM (Singtel hi!SIM, StarHub, M1, അല്ലെങ്കിൽ Circles.Life) വാങ്ങുക — രജിസ്ട്രേഷന് പാസ്‌പോർട്ട് കാണിച്ചാൽ മതി, FIN അല്ലെങ്കിൽ പാസ് ആവശ്യമില്ല.",
                  "നിങ്ങൾക്ക് postpaid ലൈൻ വേണമെങ്കിൽ (സാധാരണയായി GB ന് വിലക്കുറവ്, ശരിയായ പ്രതിമാസ ബില്ലോടെ), നിങ്ങളുടെ FIN ലഭിച്ച് പാസിൽ കുറഞ്ഞത് കുറച്ച് മാസങ്ങൾ ബാക്കിയുണ്ടെങ്കിൽ അപേക്ഷിക്കാം — മിക്ക ടെൽകോകളും നിങ്ങളുടെ പാസ് പ്ലാനിന്റെ കരാർ കാലയളവിനോട് അടുത്ത് സാധുവായിരിക്കണമെന്ന് ആഗ്രഹിക്കുന്നു.",
                  "നിങ്ങളുടെ പാസ്‌പോർട്ട് (വർക്ക് പാസ് കാർഡ് ലഭിച്ചാൽ അതും) ടെൽകോ കടയിലേക്ക് കൊണ്ടുപോകുക; postpaid പ്ലാനുകൾക്ക് സാധാരണയായി പ്രാദേശിക ബില്ലിംഗ് വിലാസവും, സിംഗപ്പൂർ ക്രെഡിറ്റ് ചരിത്രമില്ലെങ്കിൽ ചിലപ്പോൾ ഡെപ്പോസിറ്റും ആവശ്യമാണ്.",
                  "കട വിടുന്നതിന് മുമ്പ് SIM ടോപ്പ്-അപ്പ് ചെയ്യുക അല്ലെങ്കിൽ സജീവമാക്കുക — നിങ്ങൾ ഉടനടി ഓൺലൈനിൽ ആകും, ഇത് ഈ ലിസ്റ്റിലെ മറ്റെല്ലാം (SingPass, ബാങ്കിംഗ്, മാപ്പുകൾ) വളരെ എളുപ്പമാക്കും.",
                  "നിങ്ങളുടെ prepaid SIM ന്റെ സാധുത അവസാനിക്കാൻ പോകുകയാണെങ്കിൽ, അത് കാലഹരണപ്പെടുന്നതിന് മുമ്പ് ടോപ്പ്-അപ്പ് ചെയ്യുക — കാലഹരണപ്പെട്ട prepaid നമ്പർ സാധാരണയായി കുറച്ച് സമയത്തിന് ശേഷം മറ്റൊരാൾക്ക് നൽകും, നിങ്ങൾക്കത് നഷ്ടപ്പെടും."]},
    docs={"en": ["Passport", "FIN / work pass card (for postpaid plans)", "Local billing address (for postpaid plans)"],
          "hi": ["पासपोर्ट", "FIN / वर्क पास कार्ड (पोस्टपेड प्लान के लिए)", "स्थानीय बिलिंग पता (पोस्टपेड प्लान के लिए)"],
          "ta": ["பாஸ்போர்ட்", "FIN / வேலை பாஸ் அட்டை (postpaid திட்டங்களுக்கு)", "உள்ளூர் பில்லிங் முகவரி (postpaid திட்டங்களுக்கு)"],
          "te": ["పాస్‌పోర్ట్", "FIN / వర్క్ పాస్ కార్డు (postpaid ప్లాన్‌ల కోసం)", "స్థానిక బిల్లింగ్ చిరునామా (postpaid ప్లాన్‌ల కోసం)"],
          "ml": ["പാസ്‌പോർട്ട്", "FIN / വർക്ക് പാസ് കാർഡ് (postpaid പ്ലാനുകൾക്ക്)", "പ്രാദേശിക ബില്ലിംഗ് വിലാസം (postpaid പ്ലാനുകൾക്ക്)"]},
    note={"en": "A prepaid SIM works from day one, even before your work pass is issued — a practical first stop straight after landing, before you've sorted anything else.",
          "hi": "प्रीपेड SIM पहले दिन से ही काम करता है, वर्क पास मिलने से पहले भी — यह लैंड करने के तुरंत बाद, बाक़ी सब सुलझाने से पहले, एक व्यावहारिक पहला पड़ाव है।",
          "ta": "prepaid SIM முதல் நாளிலிருந்தே வேலை செய்கிறது, உங்கள் வேலை பாஸ் வழங்கப்படுவதற்கு முன்பே — தரையிறங்கியவுடன், மற்ற எதையும் சரிசெய்வதற்கு முன், நடைமுறையான முதல் நிறுத்தம்.",
          "te": "మీ వర్క్ పాస్ జారీ కావడానికి ముందు కూడా prepaid SIM మొదటి రోజు నుండే పనిచేస్తుంది — దిగిన వెంటనే, మిగతావన్నీ సర్దుకునే ముందు, ఆచరణాత్మకమైన మొదటి మజిలీ.",
          "ml": "നിങ്ങളുടെ വർക്ക് പാസ് നൽകുന്നതിന് മുമ്പുപോലും prepaid SIM ആദ്യ ദിവസം മുതൽ പ്രവർത്തിക്കുന്നു — ഇറങ്ങിയ ഉടനെ, മറ്റെല്ലാം ശരിയാക്കുന്നതിന് മുമ്പുള്ള പ്രായോഗികമായ ആദ്യ നിലയമാണിത്."},
    location={"en": "Telco kiosks at Changi Airport arrivals, or any Singtel/StarHub/M1/Circles.Life retail shop",
               "hi": "Changi हवाई अड्डे के आगमन क्षेत्र में टेल्को कियोस्क, या कोई भी Singtel/StarHub/M1/Circles.Life दुकान",
               "ta": "Changi விமான நிலைய வருகை பகுதியில் உள்ள டெல்கோ கியோஸ்க்குகள், அல்லது எந்த Singtel/StarHub/M1/Circles.Life கடையும்",
               "te": "Changi విమానాశ్రయం రాక ప్రాంతంలోని టెల్కో కియోస్క్‌లు, లేదా ఏదైనా Singtel/StarHub/M1/Circles.Life దుకాణం",
               "ml": "Changi എയർപോർട്ട് അറൈവൽസിലെ ടെൽകോ കിയോസ്കുകൾ, അല്ലെങ്കിൽ ഏതെങ്കിലും Singtel/StarHub/M1/Circles.Life കട"},
    phone=None, email=None,
    links=[
        {"href": "https://www.singtel.com/personal/products-services/mobile/prepaid-plans/hi-sim-cards", "label": {"en": "↗ Singtel — prepaid SIM", "hi": "↗ Singtel — प्रीपेड SIM", "ta": "↗ Singtel — prepaid SIM", "te": "↗ Singtel — prepaid SIM", "ml": "↗ Singtel — prepaid SIM"}},
        {"href": "https://www.m1.com.sg/mobile/prepaid-plans/tourist-sim", "label": {"en": "↗ M1 — prepaid SIM", "hi": "↗ M1 — प्रीपेड SIM", "ta": "↗ M1 — prepaid SIM", "te": "↗ M1 — prepaid SIM", "ml": "↗ M1 — prepaid SIM"}},
    ],
)

# ---- Singapore: Laws & what not to do ----

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore drug laws possession trafficking death penalty misuse of drugs act",
    title={"en": "Zero-tolerance drug laws", "hi": "ज़ीरो-टॉलरेंस ड्रग क़ानून", "ta": "பூஜ்ஜிய-சகிப்புத்தன்மை போதைப்பொருள் சட்டங்கள்",
           "te": "జీరో-టాలరెన్స్ డ్రగ్ చట్టాలు", "ml": "പൂജ്യം-സഹിഷ്ണുത മയക്കുമരുന്ന് നിയമങ്ങൾ"},
    desc={"en": "Singapore has some of the strictest drug laws in the world, and they apply to everyone on Singapore soil regardless of nationality or how long you're staying — this is not an area where the usual assumptions from home apply.",
          "hi": "सिंगापुर के ड्रग क़ानून दुनिया के सबसे सख़्त क़ानूनों में से हैं, और ये सिंगापुर की धरती पर मौजूद हर व्यक्ति पर लागू होते हैं, चाहे राष्ट्रीयता कुछ भी हो या ठहरने की अवधि कितनी भी — यह वह क्षेत्र नहीं है जहाँ घर के सामान्य अनुमान लागू होते हों।",
          "ta": "சிங்கப்பூரில் உலகின் மிகக் கடுமையான போதைப்பொருள் சட்டங்கள் சிலவற்றைக் கொண்டுள்ளது, மேலும் அவை தேசியம் அல்லது தங்கியிருக்கும் காலம் எதுவாக இருந்தாலும் சிங்கப்பூர் மண்ணில் இருக்கும் அனைவருக்கும் பொருந்தும் — இது சொந்த நாட்டின் வழக்கமான அனுமானங்கள் பொருந்தும் பகுதி அல்ல.",
          "te": "సింగపూర్‌లో ప్రపంచంలోనే అత్యంత కఠినమైన మాదకద్రవ్యాల చట్టాలు కొన్ని ఉన్నాయి, ఇవి జాతీయత లేదా ఉండే వ్యవధితో సంబంధం లేకుండా సింగపూర్ నేలపై ఉన్న ప్రతి ఒక్కరికీ వర్తిస్తాయి — ఇది స్వదేశపు సాధారణ అంచనాలు వర్తించే ప్రాంతం కాదు.",
          "ml": "സിംഗപ്പൂരിൽ ലോകത്തിലെ ഏറ്റവും കർശനമായ മയക്കുമരുന്ന് നിയമങ്ങളിൽ ചിലതുണ്ട്, ദേശീയതയോ താമസ കാലയളവോ പരിഗണിക്കാതെ സിംഗപ്പൂർ മണ്ണിലുള്ള എല്ലാവർക്കും ഇവ ബാധകമാണ് — സ്വദേശത്തെ പതിവ് ധാരണകൾ ബാധകമാകുന്ന മേഖലയല്ല ഇത്."},
    handles={"en": "consumption · possession · trafficking", "hi": "सेवन · कब्ज़ा · तस्करी", "ta": "பயன்பாடு · வைத்திருத்தல் · கடத்தல்",
             "te": "సేవనం · స్వాధీనం · అక్రమ రవాణా", "ml": "ഉപയോഗം · കൈവശം വയ്ക്കൽ · കടത്ത്"},
    steps={"en": ["The law applies to anyone in Singapore, Indian citizens included — pleading unfamiliarity with local law is not a defence.",
                  "Even a small, personal-use quantity can lead to prosecution — Singapore does not distinguish ‘just for me’ from possession as generously as some other countries do.",
                  "Some medicines that are freely available or prescribed in India — certain cough syrups, sleeping pills, and ADHD medication among them — contain substances that are controlled in Singapore; check the Health Sciences Authority's rules before you travel with any prescription medicine, and carry your prescription.",
                  "Trafficking above set quantity thresholds (for example, more than 15g of diamorphine/heroin or more than 250g of methamphetamine) carries a mandatory death sentence under the Misuse of Drugs Act — even for someone acting only as a courier."],
           "hi": ["यह क़ानून सिंगापुर में मौजूद हर व्यक्ति पर लागू होता है, भारतीय नागरिक भी शामिल — स्थानीय क़ानून की जानकारी न होने का बहाना बचाव नहीं है।",
                  "थोड़ी-सी, निजी उपयोग की मात्रा भी मुक़दमे तक ले जा सकती है — सिंगापुर 'सिर्फ़ मेरे लिए' को कब्ज़े से उतनी उदारता से अलग नहीं मानता जितना कुछ और देश मानते हैं।",
                  "भारत में आसानी से मिलने वाली या डॉक्टर द्वारा लिखी गई कुछ दवाएँ — कुछ कफ़ सिरप, नींद की गोलियाँ, और ADHD की दवा भी — ऐसे तत्व रखती हैं जो सिंगापुर में नियंत्रित हैं; कोई भी प्रिस्क्रिप्शन दवा ले जाने से पहले Health Sciences Authority के नियम जाँच लें, और अपना प्रिस्क्रिप्शन साथ रखें।",
                  "तय मात्रा-सीमा से ज़्यादा तस्करी (जैसे 15 ग्राम से ज़्यादा डायमॉर्फ़ीन/हेरोइन या 250 ग्राम से ज़्यादा मेथामफेटामाइन) पर Misuse of Drugs Act के तहत अनिवार्य मृत्युदंड है — भले ही व्यक्ति केवल कूरियर की भूमिका में हो।"],
           "ta": ["இந்தச் சட்டம் சிங்கப்பூரில் உள்ள அனைவருக்கும் பொருந்தும், இந்திய குடிமக்கள் உட்பட — உள்ளூர் சட்டம் தெரியாது என்று சொல்வது பாதுகாப்பு அல்ல.",
                  "சிறிய, தனிப்பட்ட பயன்பாட்டு அளவு கூட வழக்குக்கு வழிவகுக்கும் — 'எனக்கு மட்டும்' என்பதை வைத்திருத்தலிலிருந்து சில நாடுகள் பிரிப்பது போல் சிங்கப்பூர் தாராளமாக பிரிக்காது.",
                  "இந்தியாவில் சுலபமாகக் கிடைக்கும் அல்லது மருத்துவரால் பரிந்துரைக்கப்படும் சில மருந்துகள் — சில இருமல் சிரப்புகள், தூக்க மாத்திரைகள், ADHD மருந்து உட்பட — சிங்கப்பூரில் கட்டுப்படுத்தப்பட்ட பொருட்களைக் கொண்டுள்ளன; எந்த மருந்துச்சீட்டு மருந்துடனும் பயணிக்கும் முன் Health Sciences Authority இன் விதிகளைச் சரிபார்க்கவும், உங்கள் மருந்துச்சீட்டை எடுத்துச் செல்லவும்.",
                  "நிர்ணயிக்கப்பட்ட அளவு வரம்புகளுக்கு மேல் கடத்துதல் (எடுத்துக்காட்டாக 15g க்கு மேல் டையமார்பின்/ஹெராயின் அல்லது 250g க்கு மேல் மெத்தாம்பெட்டமைன்) Misuse of Drugs Act இன் கீழ் கட்டாய மரண தண்டனையைக் கொண்டுள்ளது — ஒருவர் வெறும் கூரியராகச் செயல்பட்டாலும் கூட."],
           "te": ["ఈ చట్టం సింగపూర్‌లో ఉన్న ప్రతి ఒక్కరికీ వర్తిస్తుంది, భారత పౌరులతో సహా — స్థానిక చట్టం తెలియదని చెప్పడం సాకుగా పనికిరాదు.",
                  "చిన్న, వ్యక్తిగత వినియోగ పరిమాణం కూడా విచారణకు దారితీయవచ్చు — 'నా కోసం మాత్రమే' అనేదాన్ని కొన్ని ఇతర దేశాలు వేరు చేసినంత ఉదారంగా సింగపూర్ స్వాధీనం నుండి వేరు చేయదు.",
                  "భారతదేశంలో సులభంగా లభించే లేదా వైద్యులు సూచించే కొన్ని మందులు — కొన్ని దగ్గు సిరప్‌లు, నిద్ర మాత్రలు, ADHD మందులతో సహా — సింగపూర్‌లో నియంత్రిత పదార్థాలను కలిగి ఉంటాయి; ఏదైనా ప్రిస్క్రిప్షన్ మందుతో ప్రయాణించే ముందు Health Sciences Authority నియమాలను తనిఖీ చేయండి, మీ ప్రిస్క్రిప్షన్‌ను వెంట తీసుకెళ్లండి.",
                  "నిర్ణీత పరిమాణ పరిమితులకు మించి అక్రమ రవాణా (ఉదాహరణకు 15g కంటే ఎక్కువ డయమార్ఫిన్/హెరాయిన్ లేదా 250g కంటే ఎక్కువ మెథాంఫేటమిన్) Misuse of Drugs Act కింద తప్పనిసరి మరణశిక్షను కలిగి ఉంటుంది — ఒక వ్యక్తి కేవలం క్యారియర్‌గా వ్యవహరించినా సరే."],
           "ml": ["ഈ നിയമം സിംഗപ്പൂരിലുള്ള എല്ലാവർക്കും ബാധകമാണ്, ഇന്ത്യൻ പൗരന്മാർ ഉൾപ്പെടെ — പ്രാദേശിക നിയമം അറിയില്ലായിരുന്നു എന്നത് ഒരു ന്യായീകരണമല്ല.",
                  "ചെറിയ, വ്യക്തിഗത ഉപയോഗത്തിനുള്ള അളവ് പോലും പ്രോസിക്യൂഷനിലേക്ക് നയിച്ചേക്കാം — 'എനിക്ക് വേണ്ടി മാത്രം' എന്നതിനെ മറ്റ് ചില രാജ്യങ്ങൾ ചെയ്യുന്നത്ര ഉദാരമായി സിംഗപ്പൂർ കൈവശം വയ്ക്കുന്നതിൽ നിന്ന് വേർതിരിക്കില്ല.",
                  "ഇന്ത്യയിൽ എളുപ്പത്തിൽ ലഭ്യമോ ഡോക്ടർ നിർദ്ദേശിക്കുന്നതോ ആയ ചില മരുന്നുകൾ — ചില ചുമ സിറപ്പുകൾ, ഉറക്ക ഗുളികകൾ, ADHD മരുന്ന് ഉൾപ്പെടെ — സിംഗപ്പൂരിൽ നിയന്ത്രിത പദാർത്ഥങ്ങൾ ഉൾക്കൊള്ളുന്നു; ഏതെങ്കിലും പ്രിസ്ക്രിപ്ഷൻ മരുന്നുമായി യാത്ര ചെയ്യുന്നതിന് മുമ്പ് Health Sciences Authority യുടെ നിയമങ്ങൾ പരിശോധിക്കുക, നിങ്ങളുടെ പ്രിസ്ക്രിപ്ഷൻ കൂടെ കൊണ്ടുപോകുക.",
                  "നിശ്ചിത അളവ് പരിധികൾക്ക് മുകളിൽ കടത്തുന്നത് (ഉദാഹരണത്തിന് 15g ൽ കൂടുതൽ ഡയമോർഫിൻ/ഹെറോയിൻ അല്ലെങ്കിൽ 250g ൽ കൂടുതൽ മെത്താംഫെറ്റാമിൻ) Misuse of Drugs Act പ്രകാരം നിർബന്ധിത വധശിക്ഷ വഹിക്കുന്നു — ഒരാൾ കേവലം ഒരു കൊറിയറായി മാത്രം പ്രവർത്തിച്ചാലും."]},
    docs={"en": ["Consumption: up to 10 years' jail and a $20,000 fine; repeat offenders face a mandatory minimum sentence and caning.",
                 "Possession: up to 10 years' jail or a $20,000 fine for typical quantities; larger quantities of drugs like cannabis, cocaine or methamphetamine can mean up to 30 years and 15 strokes of the cane.",
                 "Trafficking: ranges from long imprisonment with caning, up to the mandatory death penalty above the threshold quantities."],
          "hi": ["सेवन: 10 साल तक की जेल और $20,000 का जुर्माना; बार-बार अपराध करने वालों को अनिवार्य न्यूनतम सज़ा और कोड़े।",
                 "कब्ज़ा: सामान्य मात्रा के लिए 10 साल तक की जेल या $20,000 का जुर्माना; भांग, कोकीन या मेथामफेटामाइन जैसी दवाओं की बड़ी मात्रा पर 30 साल तक और 15 कोड़े हो सकते हैं।",
                 "तस्करी: कोड़ों सहित लंबी क़ैद से लेकर, तय सीमा से ज़्यादा मात्रा पर अनिवार्य मृत्युदंड तक।"],
          "ta": ["பயன்பாடு: 10 ஆண்டுகள் வரை சிறை மற்றும் $20,000 அபராதம்; மீண்டும் மீண்டும் குற்றம் செய்பவர்கள் கட்டாய குறைந்தபட்ச தண்டனை மற்றும் கசையடியை எதிர்கொள்வர்.",
                 "வைத்திருத்தல்: வழக்கமான அளவுகளுக்கு 10 ஆண்டுகள் வரை சிறை அல்லது $20,000 அபராதம்; கஞ்சா, கொக்கைன் அல்லது மெத்தாம்பெட்டமைன் போன்ற பெரிய அளவு போதைப்பொருட்களுக்கு 30 ஆண்டுகள் வரையும் 15 கசையடிகளும் கிடைக்கலாம்.",
                 "கடத்தல்: கசையடியுடன் கூடிய நீண்ட சிறை முதல், வரம்பு அளவுகளுக்கு மேல் கட்டாய மரண தண்டனை வரை."],
          "te": ["సేవనం: 10 సంవత్సరాల వరకు జైలు మరియు $20,000 జరిమానా; పదేపదే నేరం చేసేవారికి తప్పనిసరి కనీస శిక్ష మరియు కొరడా దెబ్బలు.",
                 "స్వాధీనం: సాధారణ పరిమాణాలకు 10 సంవత్సరాల వరకు జైలు లేదా $20,000 జరిమానా; గంజాయి, కొకైన్ లేదా మెథాంఫేటమిన్ వంటి పెద్ద పరిమాణాలకు 30 సంవత్సరాల వరకు మరియు 15 కొరడా దెబ్బలు కావచ్చు.",
                 "అక్రమ రవాణా: కొరడా దెబ్బలతో కూడిన సుదీర్ఘ జైలు శిక్ష నుండి, పరిమితి పరిమాణాలకు మించి తప్పనిసరి మరణశిక్ష వరకు."],
          "ml": ["ഉപയോഗം: 10 വർഷം വരെ ജയിലും $20,000 പിഴയും; ആവർത്തിച്ചുള്ള കുറ്റവാളികൾക്ക് നിർബന്ധിത കുറഞ്ഞ ശിക്ഷയും ചമ്മട്ടിയടിയും.",
                 "കൈവശം വയ്ക്കൽ: സാധാരണ അളവുകൾക്ക് 10 വർഷം വരെ ജയിൽ അല്ലെങ്കിൽ $20,000 പിഴ; കഞ്ചാവ്, കൊക്കെയ്ൻ അല്ലെങ്കിൽ മെത്താംഫെറ്റാമിൻ പോലുള്ള വലിയ അളവുകൾക്ക് 30 വർഷം വരെയും 15 ചമ്മട്ടിയടികളും ലഭിക്കാം.",
                 "കടത്ത്: ചമ്മട്ടിയടിയോടുകൂടിയ ദീർഘകാല ജയിൽ ശിക്ഷ മുതൽ, പരിധി അളവുകൾക്ക് മുകളിൽ നിർബന്ധിത വധശിക്ഷ വരെ."]},
    note={"en": "If you're taking any regular medication, check it against Singapore's controlled-drug rules (via the Health Sciences Authority) before you fly, and always travel with your original prescription — this has caught out travellers who never intended to break any law.",
          "hi": "अगर आप कोई नियमित दवा लेते हैं, तो उड़ान भरने से पहले Health Sciences Authority के ज़रिए सिंगापुर के नियंत्रित-ड्रग नियमों से उसे जाँच लें, और हमेशा अपना मूल प्रिस्क्रिप्शन साथ रखें — इसने ऐसे यात्रियों को भी फँसाया है जिनका क़ानून तोड़ने का कोई इरादा नहीं था।",
          "ta": "நீங்கள் ஏதேனும் வழக்கமான மருந்து எடுத்துக்கொண்டால், பறப்பதற்கு முன் Health Sciences Authority வழியாக சிங்கப்பூரின் கட்டுப்படுத்தப்பட்ட-போதைப்பொருள் விதிகளுடன் அதைச் சரிபார்க்கவும், எப்போதும் உங்கள் அசல் மருந்துச்சீட்டுடன் பயணிக்கவும் — இது சட்டத்தை மீற எண்ணாத பயணிகளையும் சிக்க வைத்துள்ளது.",
          "te": "మీరు ఏదైనా క్రమమైన మందు తీసుకుంటుంటే, ప్రయాణించే ముందు Health Sciences Authority ద్వారా సింగపూర్ నియంత్రిత-మాదకద్రవ్య నియమాలతో దాన్ని తనిఖీ చేయండి, ఎల్లప్పుడూ మీ అసలు ప్రిస్క్రిప్షన్‌తో ప్రయాణించండి — చట్టాన్ని ఉల్లంఘించాలని అనుకోని ప్రయాణికులను కూడా ఇది ఇరికించింది.",
          "ml": "നിങ്ങൾ പതിവായി ഏതെങ്കിലും മരുന്ന് കഴിക്കുന്നുണ്ടെങ്കിൽ, പറക്കുന്നതിന് മുമ്പ് Health Sciences Authority വഴി സിംഗപ്പൂരിന്റെ നിയന്ത്രിത-മയക്കുമരുന്ന് നിയമങ്ങളുമായി അത് പരിശോധിക്കുക, എപ്പോഴും നിങ്ങളുടെ യഥാർത്ഥ പ്രിസ്ക്രിപ്ഷനുമായി യാത്ര ചെയ്യുക — നിയമം ലംഘിക്കാൻ ഒരിക്കലും ഉദ്ദേശിക്കാത്ത യാത്രക്കാരെപ്പോലും ഇത് കുടുക്കിയിട്ടുണ്ട്."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.cnb.gov.sg/", "label": {"en": "↗ Central Narcotics Bureau", "hi": "↗ Central Narcotics Bureau", "ta": "↗ Central Narcotics Bureau", "te": "↗ Central Narcotics Bureau", "ml": "↗ Central Narcotics Bureau"}},
        {"href": "https://www.hsa.gov.sg/travelling-with-medication-and-medical-devices/personal-medications/", "label": {"en": "↗ HSA — travelling with medication", "hi": "↗ HSA — दवा के साथ यात्रा", "ta": "↗ HSA — மருந்துடன் பயணித்தல்", "te": "↗ HSA — మందుతో ప్రయాణం", "ml": "↗ HSA — മരുന്നുമായുള്ള യാത്ര"}},
    ],
)

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore vandalism act caning graffiti spray paint public property",
    title={"en": "Vandalism carries mandatory caning", "hi": "बर्बरता (वैंडलिज़्म) पर अनिवार्य कोड़े", "ta": "சொத்து சேதத்திற்கு (Vandalism) கட்டாய கசையடி",
           "te": "వందలిజం (ఆస్తి విధ్వంసం)కు తప్పనిసరి కొరడా దెబ్బలు", "ml": "വാൻഡലിസത്തിന് (സ്വത്ത് നശിപ്പിക്കൽ) നിർബന്ധിത ചമ്മട്ടിയടി"},
    desc={"en": "Singapore's Vandalism Act treats graffiti, spray-painting, and defacing property as a serious offence — for many forms of vandalism, caning isn't just a possible penalty, it's a mandatory one.",
          "hi": "सिंगापुर का Vandalism Act ग्रैफ़िटी, स्प्रे-पेंटिंग, और संपत्ति को नुक़सान पहुँचाने को गंभीर अपराध मानता है — बर्बरता के कई रूपों में कोड़े केवल संभावित सज़ा नहीं, बल्कि अनिवार्य सज़ा हैं।",
          "ta": "சிங்கப்பூரின் Vandalism Act, சுவரெழுத்து, ஸ்ப்ரே-பெயிண்டிங், மற்றும் சொத்தை சிதைப்பதை கடுமையான குற்றமாகக் கருதுகிறது — பல வகையான சேதங்களுக்கு கசையடி வெறும் சாத்தியமான தண்டனை அல்ல, கட்டாயமான தண்டனையாகும்.",
          "te": "సింగపూర్ Vandalism Act గ్రాఫిటీ, స్ప్రే-పెయింటింగ్, మరియు ఆస్తిని విరూపం చేయడాన్ని తీవ్రమైన నేరంగా పరిగణిస్తుంది — అనేక రకాల విధ్వంసానికి కొరడా దెబ్బలు కేవలం సాధ్యమయ్యే శిక్ష కాదు, తప్పనిసరి శిక్ష.",
          "ml": "സിംഗപ്പൂരിന്റെ Vandalism Act ഗ്രാഫിറ്റി, സ്പ്രേ-പെയിന്റിംഗ്, സ്വത്ത് വികൃതമാക്കൽ എന്നിവയെ ഗുരുതരമായ കുറ്റമായി കണക്കാക്കുന്നു — പല തരം നശീകരണങ്ങൾക്കും ചമ്മട്ടിയടി വെറും സാധ്യതയുള്ള ശിക്ഷയല്ല, നിർബന്ധിതമായ ശിക്ഷയാണ്."},
    handles={"en": "graffiti · stickers · defacing property", "hi": "ग्रैफ़िटी · स्टिकर · संपत्ति को नुक़सान", "ta": "சுவரெழுத்து · ஸ்டிக்கர்கள் · சொத்து சேதம்",
             "te": "గ్రాఫిటీ · స్టిక్కర్లు · ఆస్తి విరూపణ", "ml": "ഗ്രാഫിറ്റി · സ്റ്റിക്കറുകൾ · സ്വത്ത് നശിപ്പിക്കൽ"},
    steps={"en": ["The Vandalism Act 1966 covers writing, drawing, painting, marking, or affixing anything (including posters and stickers) on property without the owner's consent, in a public place or visible from one.",
                  "If the act uses an “indelible substance” — spray paint, permanent marker, tar — or damages public property, caning becomes mandatory on conviction, on top of any jail term or fine.",
                  "It doesn't matter whether you think of it as art or a harmless prank — tourists and visitors have been caned in Singapore for spray-painting trains and cars.",
                  "Caning is applied to male offenders aged 16 and above; it is enforced, not just written into the law as a theoretical maximum."],
           "hi": ["Vandalism Act 1966 में किसी संपत्ति पर मालिक की सहमति के बिना कुछ भी लिखना, बनाना, रंगना, चिह्नित करना, या चिपकाना (पोस्टर और स्टिकर सहित) शामिल है, अगर वह सार्वजनिक स्थान में हो या वहाँ से दिखता हो।",
                  "अगर इस काम में कोई “अमिट पदार्थ” — जैसे स्प्रे पेंट, परमानेंट मार्कर, टार — इस्तेमाल हो, या सार्वजनिक संपत्ति को नुक़सान पहुँचे, तो दोषी पाए जाने पर जुर्माने या जेल के अलावा कोड़े अनिवार्य हो जाते हैं।",
                  "इससे फ़र्क़ नहीं पड़ता कि आप इसे कला मानते हैं या मामूली शरारत — पर्यटकों और आगंतुकों को ट्रेनों और कारों पर स्प्रे-पेंट करने के लिए सिंगापुर में कोड़े लगाए जा चुके हैं।",
                  "कोड़े 16 साल या उससे अधिक उम्र के पुरुष अपराधियों पर लगाए जाते हैं; यह क़ानून में सिर्फ़ लिखी अधिकतम सज़ा नहीं है, बल्कि लागू भी की जाती है।"],
           "ta": ["Vandalism Act 1966, உரிமையாளரின் ஒப்புதல் இல்லாமல் ஒரு பொது இடத்தில் அல்லது அங்கிருந்து தெரியும் இடத்தில் சொத்தில் எதையும் எழுதுவது, வரைவது, வண்ணம் தீட்டுவது, குறியிடுவது, அல்லது ஒட்டுவது (சுவரொட்டிகள் மற்றும் ஸ்டிக்கர்கள் உட்பட) ஆகியவற்றை உள்ளடக்குகிறது.",
                  "செயலில் “அழியாத பொருள்” — ஸ்ப்ரே பெயிண்ட், நிரந்தர மார்க்கர், தார் — பயன்படுத்தப்பட்டால் அல்லது பொது சொத்திற்கு சேதம் ஏற்பட்டால், குற்றவாளி எனத் தீர்ப்பளிக்கப்பட்டவுடன் அபராதம் அல்லது சிறையுடன் கூடுதலாக கசையடி கட்டாயமாகிறது.",
                  "இதை நீங்கள் கலை என நினைத்தாலும் சரி, சிறு குறும்பு என நினைத்தாலும் சரி — ரயில்கள் மற்றும் கார்களில் ஸ்ப்ரே-பெயிண்ட் செய்ததற்காக சுற்றுலாப் பயணிகள் மற்றும் வருகையாளர்கள் சிங்கப்பூரில் கசையடி பெற்றுள்ளனர்.",
                  "கசையடி 16 வயது மற்றும் அதற்கு மேற்பட்ட ஆண் குற்றவாளிகளுக்குப் பயன்படுத்தப்படுகிறது; இது சட்டத்தில் எழுதப்பட்ட ஒரு கோட்பாட்டு அதிகபட்ச தண்டனை மட்டுமல்ல — இது நடைமுறையில் அமல்படுத்தப்படுகிறது."],
           "te": ["Vandalism Act 1966 యజమాని అనుమతి లేకుండా ఆస్తిపై ఏదైనా వ్రాయడం, గీయడం, రంగు వేయడం, గుర్తు పెట్టడం, లేదా అంటించడం (పోస్టర్లు మరియు స్టిక్కర్లతో సహా), అది బహిరంగ ప్రదేశంలో లేదా అక్కడి నుండి కనిపించేలా ఉంటే, కవర్ చేస్తుంది.",
                  "ఈ చర్యలో “చెరగని పదార్థం” — స్ప్రే పెయింట్, శాశ్వత మార్కర్, తారు — ఉపయోగించినా లేదా ప్రభుత్వ ఆస్తికి నష్టం జరిగినా, దోషిగా నిర్ధారించబడిన తర్వాత జరిమానా లేదా జైలుతో పాటు కొరడా దెబ్బలు తప్పనిసరి అవుతాయి.",
                  "మీరు దాన్ని కళగా భావించినా లేదా చిన్న అల్లరిగా భావించినా తేడా లేదు — రైళ్లు మరియు కార్లపై స్ప్రే-పెయింట్ చేసినందుకు పర్యాటకులు మరియు సందర్శకులు సింగపూర్‌లో కొరడా దెబ్బలు అనుభవించారు.",
                  "కొరడా దెబ్బలు 16 సంవత్సరాలు మరియు అంతకంటే ఎక్కువ వయస్సు గల పురుష నేరస్థులకు వర్తింపజేయబడతాయి; ఇది చట్టంలో రాసిన కేవలం సైద్ధాంతిక గరిష్ట శిక్ష మాత్రమే కాదు — ఇది అమలు చేయబడుతుంది."],
           "ml": ["ഉടമയുടെ സമ്മതമില്ലാതെ ഒരു പൊതു സ്ഥലത്തോ അവിടെ നിന്ന് കാണാവുന്നിടത്തോ സ്വത്തിൽ എന്തെങ്കിലും എഴുതുകയോ വരയ്ക്കുകയോ പെയിന്റ് ചെയ്യുകയോ അടയാളപ്പെടുത്തുകയോ ഒട്ടിക്കുകയോ (പോസ്റ്ററുകളും സ്റ്റിക്കറുകളും ഉൾപ്പെടെ) ചെയ്യുന്നത് Vandalism Act 1966 ഉൾക്കൊള്ളുന്നു.",
                  "പ്രവൃത്തിയിൽ ഒരു “മായാത്ത പദാർത്ഥം” — സ്പ്രേ പെയിന്റ്, സ്ഥിരമായ മാർക്കർ, ടാർ — ഉപയോഗിച്ചാലോ പൊതു സ്വത്തിന് നാശം സംഭവിച്ചാലോ, ശിക്ഷിക്കപ്പെട്ടാൽ പിഴയ്ക്കോ ജയിലിനോ പുറമെ ചമ്മട്ടിയടി നിർബന്ധമാകുന്നു.",
                  "ഇത് കലയായി കരുതിയാലും ചെറിയ കുസൃതിയായി കരുതിയാലും വ്യത്യാസമില്ല — ട്രെയിനുകളിലും കാറുകളിലും സ്പ്രേ-പെയിന്റ് ചെയ്തതിന് സഞ്ചാരികളും സന്ദർശകരും സിംഗപ്പൂരിൽ ചമ്മട്ടിയടി അനുഭവിച്ചിട്ടുണ്ട്.",
                  "16 വയസ്സും അതിന് മുകളിലുമുള്ള പുരുഷ കുറ്റവാളികൾക്കാണ് ചമ്മട്ടിയടി നടപ്പിലാക്കുന്നത്; ഇത് നിയമത്തിൽ എഴുതിവച്ച ഒരു സൈദ്ധാന്തിക പരമാവധി ശിക്ഷ മാത്രമല്ല — ഇത് നടപ്പിലാക്കപ്പെടുന്നു."]},
    docs={"en": ["Standard vandalism: fine up to $2,000 and/or jail up to 3 years.",
                 "Vandalism using an indelible substance, or on public property: mandatory 3 to 8 strokes of the cane, in addition to the fine or jail term.",
                 "Repeat offences and organised vandalism (e.g. planned graffiti “missions”) attract higher penalties."],
          "hi": ["सामान्य बर्बरता: $2,000 तक जुर्माना और/या 3 साल तक जेल।",
                 "अमिट पदार्थ से या सार्वजनिक संपत्ति पर बर्बरता: जुर्माने या जेल के अलावा अनिवार्य रूप से 3 से 8 कोड़े।",
                 "बार-बार अपराध और सुनियोजित बर्बरता (जैसे योजनाबद्ध ग्रैफ़िटी “मिशन”) पर और सख़्त सज़ा।"],
          "ta": ["வழக்கமான சேதம்: $2,000 வரை அபராதம் மற்றும்/அல்லது 3 ஆண்டுகள் வரை சிறை.",
                 "அழியாத பொருள் மூலம் அல்லது பொது சொத்தில் ஏற்படுத்தப்படும் சேதம்: அபராதம் அல்லது சிறைத் தண்டனையுடன் கூடுதலாக கட்டாயமாக 3 முதல் 8 கசையடிகள்.",
                 "மீண்டும் மீண்டும் செய்யப்படும் குற்றங்கள் மற்றும் திட்டமிட்ட சேதங்கள் (எ.கா. திட்டமிடப்பட்ட சுவரெழுத்து “மிஷன்கள்”) அதிக தண்டனையைப் பெறும்."],
          "te": ["సాధారణ విధ్వంసం: $2,000 వరకు జరిమానా మరియు/లేదా 3 సంవత్సరాల వరకు జైలు.",
                 "చెరగని పదార్థంతో లేదా ప్రభుత్వ ఆస్తిపై విధ్వంసం: జరిమానా లేదా జైలుతో పాటు తప్పనిసరిగా 3 నుండి 8 కొరడా దెబ్బలు.",
                 "పునరావృత నేరాలు మరియు ప్రణాళికాబద్ధమైన విధ్వంసం (ఉదా. ప్రణాళికాబద్ధమైన గ్రాఫిటీ “మిషన్లు”) మరింత కఠినమైన శిక్షలను పొందుతాయి."],
          "ml": ["സാധാരണ നശീകരണം: $2,000 വരെ പിഴയും/അല്ലെങ്കിൽ 3 വർഷം വരെ ജയിലും.",
                 "മായാത്ത പദാർത്ഥം ഉപയോഗിച്ചോ പൊതു സ്വത്തിലോ ഉള്ള നശീകരണം: പിഴയ്‌ക്കോ ജയിലിനോ പുറമെ നിർബന്ധമായും 3 മുതൽ 8 വരെ ചമ്മട്ടിയടി.",
                 "ആവർത്തിച്ചുള്ള കുറ്റങ്ങളും ആസൂത്രിത നശീകരണവും (ഉദാ. ആസൂത്രിതമായ ഗ്രാഫിറ്റി “മിഷനുകൾ”) കൂടുതൽ കടുത്ത ശിക്ഷകൾ വരുത്തിവയ്ക്കും."]},
    note={"en": "Treat any urge to spray-paint, sticker, or “tag” property in Singapore as a serious legal risk, not a minor prank — this is one of the few laws that visibly surprises Indian visitors and residents.",
          "hi": "सिंगापुर में किसी भी संपत्ति पर स्प्रे-पेंट, स्टिकर, या “टैग” लगाने की इच्छा को एक गंभीर क़ानूनी जोखिम मानें, मामूली शरारत नहीं — यह उन कुछ क़ानूनों में से एक है जो भारतीय आगंतुकों और निवासियों को सबसे ज़्यादा चौंकाता है।",
          "ta": "சிங்கப்பூரில் எந்த சொத்திலும் ஸ்ப்ரே-பெயிண்ட், ஸ்டிக்கர் ஒட்டுதல், அல்லது “டேக்” செய்ய வேண்டும் என்ற எந்த ஆசையையும் ஒரு சிறு குறும்பாக அல்ல, கடுமையான சட்டப் பிரச்சினையாகக் கருதுங்கள் — இது இந்திய வருகையாளர்கள் மற்றும் குடியிருப்பாளர்களை மிகவும் ஆச்சரியப்படுத்தும் சில சட்டங்களில் ஒன்று.",
          "te": "సింగపూర్‌లో ఏదైనా ఆస్తిపై స్ప్రే-పెయింట్, స్టిక్కర్ వేయడం, లేదా “ట్యాగ్” చేయాలనే ఏ కోరికనైనా చిన్న అల్లరిగా కాకుండా తీవ్రమైన చట్టపరమైన ప్రమాదంగా పరిగణించండి — భారతీయ సందర్శకులు మరియు నివాసితులను అత్యంత ఆశ్చర్యపరిచే కొన్ని చట్టాలలో ఇది ఒకటి.",
          "ml": "സിംഗപ്പൂരിൽ ഏതെങ്കിലും സ്വത്തിൽ സ്പ്രേ-പെയിന്റ് ചെയ്യാനോ സ്റ്റിക്കർ ഒട്ടിക്കാനോ “ടാഗ്” ചെയ്യാനോ തോന്നുന്ന ഏത് ആഗ്രഹത്തെയും ചെറിയ കുസൃതിയായല്ല, ഗുരുതരമായ നിയമ അപകടസാധ്യതയായി കണക്കാക്കുക — ഇന്ത്യൻ സന്ദർശകരെയും താമസക്കാരെയും ഏറ്റവുമധികം ഞെട്ടിക്കുന്ന ചുരുക്കം ചില നിയമങ്ങളിൽ ഒന്നാണിത്."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://sso.agc.gov.sg/Act/VA1966", "label": {"en": "↗ Vandalism Act 1966 (full text)", "hi": "↗ Vandalism Act 1966 (पूरा पाठ)", "ta": "↗ Vandalism Act 1966 (முழு உரை)", "te": "↗ Vandalism Act 1966 (పూర్తి పాఠం)", "ml": "↗ Vandalism Act 1966 (മുഴുവൻ വാചകം)"}},
    ],
)

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore vaping e-cigarette ban etomidate kpod penalty 2026",
    title={"en": "Vaping is banned — and getting stricter", "hi": "वेपिंग प्रतिबंधित है — और सख़्ती और बढ़ रही है", "ta": "வேப்பிங் தடைசெய்யப்பட்டுள்ளது — மேலும் கடுமையாகிக்கொண்டிருக்கிறது",
           "te": "వేపింగ్ నిషేధించబడింది — మరింత కఠినంగా మారుతోంది", "ml": "വേപ്പിംഗ് നിരോധിച്ചിരിക്കുന്നു — കൂടുതൽ കർശനമാകുന്നു"},
    desc={"en": "Vaping is illegal in Singapore for everyone, not just minors — simply possessing or using an e-cigarette can mean a heavy fine, and a law in force from May 2026 makes laced vapes a jailable, canable offence.",
          "hi": "सिंगापुर में वेपिंग सभी के लिए ग़ैरक़ानूनी है, सिर्फ़ नाबालिगों के लिए नहीं — केवल ई-सिगरेट रखना या इस्तेमाल करना भारी जुर्माने का कारण बन सकता है, और मई 2026 से लागू एक क़ानून मिलावटी वेप को जेल और कोड़ों तक ले जाने वाला अपराध बना देता है।",
          "ta": "சிங்கப்பூரில் வேப்பிங் அனைவருக்கும் சட்டவிரோதமானது, சிறார்களுக்கு மட்டும் அல்ல — ஒரு மின்-சிகரெட்டை வைத்திருப்பது அல்லது பயன்படுத்துவது கூட கடுமையான அபராதத்திற்கு வழிவகுக்கும், மேலும் மே 2026 முதல் நடைமுறையில் உள்ள ஒரு சட்டம் கலப்படமான வேப்களை சிறை மற்றும் கசையடி பெறக்கூடிய குற்றமாக ஆக்குகிறது.",
          "te": "సింగపూర్‌లో వేపింగ్ అందరికీ చట్టవిరుద్ధం, మైనర్లకు మాత్రమే కాదు — ఒక ఇ-సిగరెట్‌ను కలిగి ఉండటం లేదా వాడటం కూడా భారీ జరిమానాకు దారితీయవచ్చు, మరియు మే 2026 నుండి అమల్లోకి వచ్చిన చట్టం కల్తీ వేప్‌లను జైలు, కొరడా దెబ్బలు విధించే నేరంగా చేస్తుంది.",
          "ml": "സിംഗപ്പൂരിൽ വേപ്പിംഗ് എല്ലാവർക്കും നിയമവിരുദ്ധമാണ്, പ്രായപൂർത്തിയാകാത്തവർക്ക് മാത്രമല്ല — ഒരു ഇ-സിഗരറ്റ് കൈവശം വയ്ക്കുന്നതോ ഉപയോഗിക്കുന്നതോ പോലും കനത്ത പിഴയ്ക്ക് കാരണമാകാം, കൂടാതെ 2026 മേയ് മുതൽ പ്രാബല്യത്തിലുള്ള ഒരു നിയമം മായം ചേർത്ത വേപ്പുകളെ ജയിലും ചമ്മട്ടിയടിയും ലഭിക്കാവുന്ന കുറ്റമാക്കുന്നു."},
    handles={"en": "e-cigarettes · vape pods · Kpods", "hi": "ई-सिगरेट · वेप पॉड्स · Kpods", "ta": "மின்-சிகரெட்டுகள் · வேப் பாட்கள் · Kpods",
             "te": "ఇ-సిగరెట్లు · వేప్ పాడ్‌లు · Kpods", "ml": "ഇ-സിഗരറ്റുകൾ · വേപ്പ് പോഡുകൾ · Kpods"},
    steps={"en": ["Importing, distributing, selling, or using e-cigarettes and vaporisers is illegal in Singapore for anyone, of any age, under the Tobacco (Control of Advertisements and Sale) Act.",
                  "From 1 May 2026, the Vaping (Control of Device and Substance) Act makes it a specific offence to possess, use, or be under the influence of a “prohibited vaping substance.”",
                  "Some vapes seized in Singapore (often called “Kpods”) have been found laced with etomidate, an anaesthetic drug — possessing or using these is treated far more seriously than an ordinary vape."],
           "hi": ["Tobacco (Control of Advertisements and Sale) Act के तहत ई-सिगरेट और वेपोराइज़र का आयात, वितरण, बिक्री, या इस्तेमाल सिंगापुर में किसी भी उम्र के व्यक्ति के लिए ग़ैरक़ानूनी है।",
                  "1 मई 2026 से, Vaping (Control of Device and Substance) Act किसी “प्रतिबंधित वेपिंग पदार्थ” को रखना, इस्तेमाल करना, या उसके नशे में होना एक अलग अपराध बनाता है।",
                  "सिंगापुर में ज़ब्त किए गए कुछ वेप (अक्सर “Kpods” कहलाते हैं) में एटोमिडेट नामक एनेस्थीसिया दवा मिली पाई गई है — इन्हें रखना या इस्तेमाल करना सामान्य वेप की तुलना में कहीं अधिक गंभीरता से लिया जाता है।"],
           "ta": ["Tobacco (Control of Advertisements and Sale) Act இன் கீழ், மின்-சிகரெட்டுகள் மற்றும் ஆவியாக்கிகளை இறக்குமதி செய்வது, விநியோகிப்பது, விற்பது, அல்லது பயன்படுத்துவது சிங்கப்பூரில் எந்த வயதினருக்கும் சட்டவிரோதமானது.",
                  "1 மே 2026 முதல், Vaping (Control of Device and Substance) Act ஒரு “தடைசெய்யப்பட்ட வேப்பிங் பொருளை” வைத்திருப்பது, பயன்படுத்துவது, அல்லது அதன் தாக்கத்தில் இருப்பதை தனி குற்றமாக ஆக்குகிறது.",
                  "சிங்கப்பூரில் பறிமுதல் செய்யப்பட்ட சில வேப்கள் (பெரும்பாலும் “Kpods” எனப்படும்) எடோமிடேட் எனும் மயக்க மருந்துடன் கலக்கப்பட்டதாகக் கண்டறியப்பட்டுள்ளன — இவற்றை வைத்திருப்பது அல்லது பயன்படுத்துவது சாதாரண வேப்பை விட மிகவும் தீவிரமாக நடத்தப்படுகிறது."],
           "te": ["Tobacco (Control of Advertisements and Sale) Act ప్రకారం, ఇ-సిగరెట్లు మరియు వేపొరైజర్‌లను దిగుమతి చేయడం, పంపిణీ చేయడం, అమ్మడం, లేదా వాడటం సింగపూర్‌లో ఏ వయస్సు వారికైనా చట్టవిరుద్ధం.",
                  "1 మే 2026 నుండి, Vaping (Control of Device and Substance) Act “నిషేధిత వేపింగ్ పదార్థాన్ని” కలిగి ఉండటం, వాడటం, లేదా దాని ప్రభావంలో ఉండటం ప్రత్యేక నేరంగా చేస్తుంది.",
                  "సింగపూర్‌లో స్వాధీనం చేసుకున్న కొన్ని వేప్‌లు (తరచుగా “Kpods” అని పిలుస్తారు) ఎటోమిడేట్ అనే మత్తుమందుతో కలిపి ఉన్నట్లు కనుగొనబడ్డాయి — వీటిని కలిగి ఉండటం లేదా వాడటం సాధారణ వేప్ కంటే చాలా తీవ్రంగా పరిగణించబడుతుంది."],
           "ml": ["Tobacco (Control of Advertisements and Sale) Act പ്രകാരം, ഇ-സിഗരറ്റുകളും വേപറൈസറുകളും ഇറക്കുമതി ചെയ്യുന്നതോ വിതരണം ചെയ്യുന്നതോ വിൽക്കുന്നതോ ഉപയോഗിക്കുന്നതോ സിംഗപ്പൂരിൽ ഏത് പ്രായക്കാർക്കും നിയമവിരുദ്ധമാണ്.",
                  "2026 മേയ് 1 മുതൽ, Vaping (Control of Device and Substance) Act ഒരു “നിരോധിത വേപ്പിംഗ് പദാർത്ഥം” കൈവശം വയ്ക്കുന്നതോ ഉപയോഗിക്കുന്നതോ അതിന്റെ സ്വാധീനത്തിലായിരിക്കുന്നതോ പ്രത്യേക കുറ്റമാക്കുന്നു.",
                  "സിംഗപ്പൂരിൽ പിടിച്ചെടുത്ത ചില വേപ്പുകളിൽ (പലപ്പോഴും “Kpods” എന്ന് വിളിക്കപ്പെടുന്നു) എറ്റോമിഡേറ്റ് എന്ന അനസ്തേഷ്യ മരുന്ന് കലർത്തിയതായി കണ്ടെത്തിയിട്ടുണ്ട് — ഇവ കൈവശം വയ്ക്കുന്നതോ ഉപയോഗിക്കുന്നതോ സാധാരണ വേപ്പിനെക്കാൾ വളരെ ഗൗരവമായി കണക്കാക്കപ്പെടുന്നു."]},
    docs={"en": ["Possessing or using an ordinary prohibited e-vaporiser/vaping substance: fine up to $10,000.",
                 "Possessing or using an etomidate-laced (“Kpod”) vape: fine up to $20,000, and/or jail up to 10 years.",
                 "Importing, selling, or supplying etomidate-laced vapes: mandatory jail plus caning."],
          "hi": ["सामान्य प्रतिबंधित ई-वेपोराइज़र/वेपिंग पदार्थ रखना या इस्तेमाल करना: $10,000 तक जुर्माना।",
                 "एटोमिडेट-मिश्रित (“Kpod”) वेप रखना या इस्तेमाल करना: $20,000 तक जुर्माना, और/या 10 साल तक जेल।",
                 "एटोमिडेट-मिश्रित वेप का आयात, बिक्री, या आपूर्ति: अनिवार्य जेल के साथ कोड़े।"],
          "ta": ["சாதாரண தடைசெய்யப்பட்ட மின்-ஆவியாக்கி/வேப்பிங் பொருளை வைத்திருத்தல் அல்லது பயன்படுத்துதல்: $10,000 வரை அபராதம்.",
                 "எடோமிடேட்-கலந்த (“Kpod”) வேப்பை வைத்திருத்தல் அல்லது பயன்படுத்துதல்: $20,000 வரை அபராதம், மற்றும்/அல்லது 10 ஆண்டுகள் வரை சிறை.",
                 "எடோமிடேட்-கலந்த வேப்களை இறக்குமதி செய்தல், விற்றல், அல்லது வழங்குதல்: கட்டாய சிறையுடன் கசையடி."],
          "te": ["సాధారణ నిషేధిత ఇ-వేపొరైజర్/వేపింగ్ పదార్థాన్ని కలిగి ఉండటం లేదా వాడటం: $10,000 వరకు జరిమానా.",
                 "ఎటోమిడేట్-కలిపిన (“Kpod”) వేప్‌ను కలిగి ఉండటం లేదా వాడటం: $20,000 వరకు జరిమానా, మరియు/లేదా 10 సంవత్సరాల వరకు జైలు.",
                 "ఎటోమిడేట్-కలిపిన వేప్‌లను దిగుమతి చేయడం, అమ్మడం, లేదా సరఫరా చేయడం: తప్పనిసరి జైలుతో పాటు కొరడా దెబ్బలు."],
          "ml": ["സാധാരണ നിരോധിത ഇ-വേപറൈസർ/വേപ്പിംഗ് പദാർത്ഥം കൈവശം വയ്ക്കുന്നതോ ഉപയോഗിക്കുന്നതോ: $10,000 വരെ പിഴ.",
                 "എറ്റോമിഡേറ്റ്-കലർത്തിയ (“Kpod”) വേപ്പ് കൈവശം വയ്ക്കുന്നതോ ഉപയോഗിക്കുന്നതോ: $20,000 വരെ പിഴയും/അല്ലെങ്കിൽ 10 വർഷം വരെ ജയിലും.",
                 "എറ്റോമിഡേറ്റ്-കലർത്തിയ വേപ്പുകൾ ഇറക്കുമതി ചെയ്യുന്നതോ വിൽക്കുന്നതോ വിതരണം ചെയ്യുന്നതോ: നിർബന്ധിത ജയിലും ചമ്മട്ടിയടിയും."]},
    note={"en": "If you already vape, don't bring vapes or pods into Singapore and don't buy them here. If you want help to quit, the Health Promotion Board's QuitLine (1800 438 2000) is free and doesn't ask about your immigration status.",
          "hi": "अगर आप पहले से वेप करते हैं, तो सिंगापुर में वेप या पॉड्स न लाएँ और यहाँ न ख़रीदें। अगर छोड़ना चाहते हैं, तो Health Promotion Board की QuitLine (1800 438 2000) मुफ़्त है और आपकी इमिग्रेशन स्थिति नहीं पूछती।",
          "ta": "நீங்கள் ஏற்கனவே வேப் செய்தால், சிங்கப்பூருக்கு வேப் அல்லது பாட்களைக் கொண்டு வர வேண்டாம், இங்கு வாங்கவும் வேண்டாம். நிறுத்த உதவி தேவைப்பட்டால், Health Promotion Board இன் QuitLine (1800 438 2000) இலவசம், மேலும் உங்கள் குடியேற்ற நிலையைப் பற்றி கேட்காது.",
          "te": "మీరు ఇప్పటికే వేప్ చేస్తుంటే, సింగపూర్‌కు వేప్‌లు లేదా పాడ్‌లను తీసుకురావద్దు మరియు ఇక్కడ కొనవద్దు. మానేయాలనుకుంటే, Health Promotion Board యొక్క QuitLine (1800 438 2000) ఉచితం మరియు మీ ఇమ్మిగ్రేషన్ స్థితి గురించి అడగదు.",
          "ml": "നിങ്ങൾ ഇതിനകം വേപ്പ് ചെയ്യുന്നുണ്ടെങ്കിൽ, സിംഗപ്പൂരിലേക്ക് വേപ്പുകളോ പോഡുകളോ കൊണ്ടുവരരുത്, ഇവിടെ വാങ്ങുകയും ചെയ്യരുത്. നിർത്താൻ സഹായം വേണമെങ്കിൽ, Health Promotion Board ന്റെ QuitLine (1800 438 2000) സൗജന്യമാണ്, നിങ്ങളുടെ ഇമിഗ്രേഷൻ നിലയെക്കുറിച്ച് ചോദിക്കുന്നില്ല."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.gov.sg/stopvaping-penalties/", "label": {"en": "↗ gov.sg — vaping penalties explained", "hi": "↗ gov.sg — वेपिंग दंड की जानकारी", "ta": "↗ gov.sg — வேப்பிங் தண்டனைகள் விளக்கம்", "te": "↗ gov.sg — వేపింగ్ శిక్షల వివరణ", "ml": "↗ gov.sg — വേപ്പിംഗ് ശിക്ഷകൾ വിശദീകരണം"}},
    ],
)

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore work pass moonlighting employment act unauthorised employment EFMA side job",
    title={"en": "Working outside your named employer is illegal", "hi": "अपने नामित नियोक्ता के अलावा काम करना ग़ैरक़ानूनी है", "ta": "உங்கள் பெயரிடப்பட்ட முதலாளிக்கு வெளியே வேலை செய்வது சட்டவிரோதம்",
           "te": "మీ పేరు మీద ఉన్న యజమాని కాకుండా ఇతరుల వద్ద పనిచేయడం చట్టవిరుద్ధం", "ml": "നിങ്ങളുടെ പേരിലുള്ള തൊഴിലുടമയ്ക്ക് പുറത്ത് ജോലി ചെയ്യുന്നത് നിയമവിരുദ്ധം"},
    desc={"en": "Your work pass — Employment Pass, S Pass, or Work Permit — ties you to one specific employer doing one specific job. Taking any other paid work, even a small side-gig, without a separate pass is a criminal offence under the Employment of Foreign Manpower Act.",
          "hi": "आपका वर्क पास — Employment Pass, S Pass, या Work Permit — आपको एक ख़ास नियोक्ता के लिए एक ख़ास काम से जोड़ता है। बिना अलग पास के कोई भी अन्य भुगतान वाला काम, यहाँ तक कि छोटा साइड-गिग भी, Employment of Foreign Manpower Act के तहत आपराधिक अपराध है।",
          "ta": "உங்கள் வேலை அனுமதி — Employment Pass, S Pass, அல்லது Work Permit — உங்களை ஒரு குறிப்பிட்ட முதலாளியுடன் ஒரு குறிப்பிட்ட வேலைக்காக இணைக்கிறது. தனி அனுமதி இல்லாமல் வேறு எந்த ஊதிய வேலையும், சிறிய பக்க வேலை கூட, Employment of Foreign Manpower Act இன் கீழ் குற்றவியல் குற்றமாகும்.",
          "te": "మీ వర్క్ పాస్ — Employment Pass, S Pass, లేదా Work Permit — మిమ్మల్ని ఒక నిర్దిష్ట యజమానికి ఒక నిర్దిష్ట పనితో అనుసంధానిస్తుంది. వేరే పాస్ లేకుండా ఏదైనా ఇతర చెల్లింపు పని చేయడం, చిన్న సైడ్-గిగ్ అయినా సరే, Employment of Foreign Manpower Act ప్రకారం నేరపూరిత నేరం.",
          "ml": "നിങ്ങളുടെ വർക്ക് പാസ് — Employment Pass, S Pass, അല്ലെങ്കിൽ Work Permit — നിങ്ങളെ ഒരു നിശ്ചിത തൊഴിലുടമയുമായി ഒരു നിശ്ചിത ജോലിക്കായി ബന്ധിപ്പിക്കുന്നു. പ്രത്യേക പാസ് ഇല്ലാതെ മറ്റേതെങ്കിലും ശമ്പളമുള്ള ജോലി, ചെറിയ സൈഡ്-ഗിഗ് ആണെങ്കിൽ പോലും, Employment of Foreign Manpower Act പ്രകാരം ക്രിമിനൽ കുറ്റമാണ്."},
    handles={"en": "moonlighting · side jobs · unauthorised work", "hi": "मूनलाइटिंग · साइड जॉब · अनधिकृत काम", "ta": "மூன்லைட்டிங் · பக்க வேலைகள் · அங்கீகரிக்கப்படாத வேலை",
             "te": "మూన్‌లైటింగ్ · సైడ్ జాబ్‌లు · అనధికారిక పని", "ml": "മൂൺലൈറ്റിംഗ് · സൈഡ് ജോലികൾ · അനധികൃത ജോലി"},
    steps={"en": ["Working for any employer other than the one named on your pass — including freelance, gig, or informal “cash-in-hand” work — is illegal, even if it's unpaid or one-off.",
                  "This covers work that can feel harmless: driving for a ride-hailing app, tutoring on weekends, or helping a friend's business all count as unauthorised employment without the right pass.",
                  "Employers who knowingly engage someone without the correct pass are prosecuted too — but “the employer offered it” is not a defence for the worker.",
                  "Beyond the court penalty, MOM can cancel your existing pass, and future work-pass applications (yours, or a new employer's on your behalf) can be refused."],
           "hi": ["आपके पास पर दर्ज नियोक्ता के अलावा किसी और के लिए काम करना — फ़्रीलांस, गिग, या अनौपचारिक “कैश-इन-हैंड” काम सहित — ग़ैरक़ानूनी है, चाहे वह अवैतनिक हो या एक बार का ही क्यों न हो।",
                  "इसमें वह काम भी शामिल है जो हानिरहित लग सकता है: राइड-हेलिंग ऐप के लिए गाड़ी चलाना, वीकेंड पर ट्यूशन पढ़ाना, या किसी दोस्त के व्यवसाय में मदद करना — सही पास के बिना ये सभी अनधिकृत रोज़गार माने जाते हैं।",
                  "जानबूझकर बिना सही पास वाले व्यक्ति को काम पर रखने वाले नियोक्ताओं पर भी मुक़दमा चलता है — लेकिन “नियोक्ता ने ही ऑफ़र किया था” कर्मचारी के लिए बचाव नहीं है।",
                  "अदालती सज़ा के अलावा, MOM आपका मौजूदा पास रद्द कर सकता है, और भविष्य के वर्क-पास आवेदन (आपके ख़ुद के, या आपकी ओर से किसी नए नियोक्ता के) अस्वीकार किए जा सकते हैं।"],
           "ta": ["உங்கள் அனுமதியில் பெயரிடப்பட்டவரைத் தவிர வேறு எந்த முதலாளிக்கும் வேலை செய்வது — ஃப்ரீலான்ஸ், கிக், அல்லது முறைசாரா “பணமாக” வேலை உட்பட — சட்டவிரோதமானது, அது ஊதியமில்லாதது அல்லது ஒரு முறை மட்டுமே செய்யப்பட்டதாக இருந்தாலும் சரி.",
                  "தீங்கற்றதாகத் தோன்றக்கூடிய வேலையும் இதில் அடங்கும்: ரைடு-ஹெய்லிங் ஆப்பிற்கு வாகனம் ஓட்டுவது, வார இறுதியில் டியூஷன் சொல்லிக்கொடுப்பது, அல்லது ஒரு நண்பரின் வணிகத்திற்கு உதவுவது — சரியான அனுமதி இல்லாமல் இவை அனைத்தும் அங்கீகரிக்கப்படாத வேலையாகக் கருதப்படும்.",
                  "சரியான அனுமதி இல்லாத ஒருவரை அறிந்தே பணியமர்த்தும் முதலாளிகளும் வழக்குக்கு உள்ளாக்கப்படுவார்கள் — ஆனால் “முதலாளி தானே வழங்கினார்” என்பது தொழிலாளிக்கு பாதுகாப்பு அல்ல.",
                  "நீதிமன்ற தண்டனையைத் தாண்டி, MOM உங்கள் தற்போதைய அனுமதியை ரத்து செய்யலாம், மேலும் எதிர்கால வேலை-அனுமதி விண்ணப்பங்கள் (உங்களுடையது, அல்லது உங்களுக்காக ஒரு புதிய முதலாளியினுடையது) நிராகரிக்கப்படலாம்."],
           "te": ["మీ పాస్‌పై పేర్కొన్న యజమాని కాకుండా మరెవరికైనా పని చేయడం — ఫ్రీలాన్స్, గిగ్, లేదా అనధికారిక “నగదు” పనితో సహా — చట్టవిరుద్ధం, అది చెల్లించనిదైనా లేదా ఒకసారి మాత్రమే చేసినదైనా సరే.",
                  "హానిచేయనిదిగా అనిపించే పని కూడా ఇందులో ఉంటుంది: రైడ్-హెయిలింగ్ యాప్ కోసం డ్రైవింగ్ చేయడం, వారాంతాల్లో ట్యూషన్ చెప్పడం, లేదా స్నేహితుడి వ్యాపారానికి సహాయం చేయడం — సరైన పాస్ లేకుండా ఇవన్నీ అనధికారిక ఉపాధిగా పరిగణించబడతాయి.",
                  "సరైన పాస్ లేని వ్యక్తిని తెలిసి నియమించుకునే యజమానులపై కూడా విచారణ జరుగుతుంది — కానీ “యజమానే ఇచ్చాడు” అనేది కార్మికుడికి రక్షణ కాదు.",
                  "కోర్టు శిక్షకు అదనంగా, MOM మీ ప్రస్తుత పాస్‌ను రద్దు చేయవచ్చు, మరియు భవిష్యత్తు వర్క్-పాస్ దరఖాస్తులు (మీ స్వంతవి, లేదా మీ తరపున కొత్త యజమాని వేసేవి) తిరస్కరించబడవచ్చు."],
           "ml": ["നിങ്ങളുടെ പാസിൽ പേരുള്ള തൊഴിലുടമയ്ക്ക് പുറമെ മറ്റാർക്കെങ്കിലും വേണ്ടി ജോലി ചെയ്യുന്നത് — ഫ്രീലാൻസ്, ഗിഗ്, അല്ലെങ്കിൽ അനൗപചാരികമായ “പണത്തിന്” ജോലി ഉൾപ്പെടെ — നിയമവിരുദ്ധമാണ്, അത് പ്രതിഫലമില്ലാത്തതോ ഒറ്റത്തവണ മാത്രമോ ആയാലും.",
                  "ദോഷകരമല്ലെന്ന് തോന്നാവുന്ന ജോലിയും ഇതിൽ ഉൾപ്പെടുന്നു: റൈഡ്-ഹെയിലിംഗ് ആപ്പിന് വേണ്ടി ഡ്രൈവ് ചെയ്യുന്നത്, വാരാന്ത്യങ്ങളിൽ ട്യൂഷൻ പഠിപ്പിക്കുന്നത്, അല്ലെങ്കിൽ ഒരു സുഹൃത്തിന്റെ ബിസിനസ്സിനെ സഹായിക്കുന്നത് — ശരിയായ പാസ് ഇല്ലാതെ ഇവയെല്ലാം അനധികൃത തൊഴിലായി കണക്കാക്കപ്പെടും.",
                  "ശരിയായ പാസ് ഇല്ലാത്ത ഒരാളെ അറിഞ്ഞുകൊണ്ട് നിയമിക്കുന്ന തൊഴിലുടമകൾക്കും വിചാരണ നേരിടേണ്ടിവരും — എന്നാൽ “തൊഴിലുടമ തന്നെയാണ് വാഗ്ദാനം ചെയ്തത്” എന്നത് തൊഴിലാളിക്ക് ഒരു പ്രതിരോധമല്ല.",
                  "കോടതി ശിക്ഷയ്ക്ക് പുറമെ, MOM ന് നിങ്ങളുടെ നിലവിലെ പാസ് റദ്ദാക്കാം, കൂടാതെ ഭാവിയിലെ വർക്ക്-പാസ് അപേക്ഷകൾ (നിങ്ങളുടേത്, അല്ലെങ്കിൽ നിങ്ങൾക്കുവേണ്ടി ഒരു പുതിയ തൊഴിലുടമയുടേത്) നിരസിക്കപ്പെടാം."]},
    docs={"en": ["Worker: fine up to $20,000, and/or jail up to 2 years, or both.",
                 "Practical consequences beyond the courtroom: pass cancellation, repatriation, and a ban on re-entry or future passes.",
                 "An employer who engages you unlawfully faces separate, often heavier, penalties of their own under the same Act."],
          "hi": ["कर्मचारी: $20,000 तक जुर्माना, और/या 2 साल तक जेल, या दोनों।",
                 "अदालत से परे व्यावहारिक परिणाम: पास रद्द होना, वापस भेजा जाना, और पुनः प्रवेश या भविष्य के पास पर प्रतिबंध।",
                 "आपको ग़ैरक़ानूनी रूप से काम पर रखने वाले नियोक्ता पर भी उसी क़ानून के तहत अलग, अक्सर ज़्यादा सख़्त, सज़ा लागू होती है।"],
          "ta": ["தொழிலாளி: $20,000 வரை அபராதம், மற்றும்/அல்லது 2 ஆண்டுகள் வரை சிறை, அல்லது இரண்டும்.",
                 "நீதிமன்றத்திற்கு அப்பாற்பட்ட நடைமுறை விளைவுகள்: அனுமதி ரத்து, நாடு திரும்ப அனுப்பப்படுதல், மற்றும் மீண்டும் நுழைவு அல்லது எதிர்கால அனுமதிகள் மீதான தடை.",
                 "உங்களை சட்டவிரோதமாக பணியமர்த்தும் ஒரு முதலாளி அதே சட்டத்தின் கீழ் தனித்தனியான, பெரும்பாலும் கடுமையான, தண்டனைகளை எதிர்கொள்வார்."],
          "te": ["కార్మికుడు: $20,000 వరకు జరిమానా, మరియు/లేదా 2 సంవత్సరాల వరకు జైలు, లేదా రెండూ.",
                 "కోర్టుకు మించిన ఆచరణాత్మక పరిణామాలు: పాస్ రద్దు, స్వదేశానికి పంపడం, మరియు తిరిగి ప్రవేశం లేదా భవిష్యత్తు పాస్‌లపై నిషేధం.",
                 "మిమ్మల్ని చట్టవిరుద్ధంగా నియమించుకున్న యజమాని అదే చట్టం కింద ప్రత్యేకమైన, తరచుగా కఠినమైన, శిక్షలను ఎదుర్కొంటారు."],
          "ml": ["തൊഴിലാളി: $20,000 വരെ പിഴയും/അല്ലെങ്കിൽ 2 വർഷം വരെ ജയിലും, അല്ലെങ്കിൽ രണ്ടും.",
                 "കോടതിക്ക് അപ്പുറമുള്ള പ്രായോഗിക പരിണതഫലങ്ങൾ: പാസ് റദ്ദാക്കൽ, സ്വദേശത്തേക്ക് തിരിച്ചയക്കൽ, തിരിച്ചുവരവിനോ ഭാവിയിലെ പാസുകൾക്കോ ഉള്ള വിലക്ക്.",
                 "നിങ്ങളെ നിയമവിരുദ്ധമായി നിയമിക്കുന്ന ഒരു തൊഴിലുടമ അതേ നിയമപ്രകാരം പ്രത്യേകവും പലപ്പോഴും കടുത്തതുമായ ശിക്ഷകൾ നേരിടും."]},
    note={"en": "If you want extra income, the only safe route is checking with your current employer or MOM first — never assume a “small” side job is fine just because it's informal or unpaid.",
          "hi": "अगर आपको अतिरिक्त आय चाहिए, तो सबसे सुरक्षित तरीक़ा है अपने मौजूदा नियोक्ता या MOM से पहले पूछना — कभी यह न मान लें कि कोई “छोटा” साइड जॉब सिर्फ़ इसलिए ठीक है क्योंकि वह अनौपचारिक या अवैतनिक है।",
          "ta": "உங்களுக்கு கூடுதல் வருமானம் தேவைப்பட்டால், பாதுகாப்பான ஒரே வழி உங்கள் தற்போதைய முதலாளி அல்லது MOM இடம் முதலில் சரிபார்ப்பதுதான் — ஒரு “சிறிய” பக்க வேலை முறைசாரா அல்லது ஊதியமற்றது என்பதால் மட்டும் அது சரியென்று ஒருபோதும் நினைக்க வேண்டாம்.",
          "te": "మీకు అదనపు ఆదాయం కావాలంటే, సురక్షితమైన ఏకైక మార్గం మీ ప్రస్తుత యజమాని లేదా MOM తో ముందుగా తనిఖీ చేయడమే — ఒక “చిన్న” సైడ్ జాబ్ అనధికారికమైనది లేదా చెల్లించనిదైనంత మాత్రాన అది సరైనదని ఎప్పుడూ అనుకోవద్దు.",
          "ml": "നിങ്ങൾക്ക് അധിക വരുമാനം വേണമെങ്കിൽ, സുരക്ഷിതമായ ഒരേയൊരു വഴി നിങ്ങളുടെ നിലവിലെ തൊഴിലുടമയോടോ MOM നോടോ ആദ്യം ചോദിക്കുക എന്നതാണ് — ഒരു “ചെറിയ” സൈഡ് ജോലി അനൗപചാരികമോ പ്രതിഫലമില്ലാത്തതോ ആയതുകൊണ്ട് മാത്രം അത് ശരിയാണെന്ന് ഒരിക്കലും കരുതരുത്."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://sso.agc.gov.sg/Act/EFMA1990", "label": {"en": "↗ Employment of Foreign Manpower Act (full text)", "hi": "↗ Employment of Foreign Manpower Act (पूरा पाठ)", "ta": "↗ Employment of Foreign Manpower Act (முழு உரை)", "te": "↗ Employment of Foreign Manpower Act (పూర్తి పాఠం)", "ml": "↗ Employment of Foreign Manpower Act (മുഴുവൻ വാചകം)"}},
    ],
)

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore overstay pass penalty caning immigration act repatriation ban",
    title={"en": "Overstaying your pass has severe, non-negotiable penalties", "hi": "अपने पास की अवधि से अधिक रुकने पर सख़्त, बिना समझौते वाली सज़ा", "ta": "உங்கள் அனுமதி காலாவதியான பிறகு தங்குவதற்கு கடுமையான, பேச்சுவார்த்தைக்கு இடமில்லாத தண்டனைகள்",
           "te": "మీ పాస్ గడువు దాటిన తర్వాత ఉండటానికి తీవ్రమైన, రాజీలేని శిక్షలు", "ml": "പാസിന്റെ കാലാവധി കഴിഞ്ഞ് തങ്ങുന്നതിന് കടുത്തതും വിട്ടുവീഴ്ചയില്ലാത്തതുമായ ശിക്ഷകൾ"},
    desc={"en": "Staying in Singapore even one day past your pass's validity is an offence under the Immigration Act — the penalties escalate sharply after 90 days, and the decision to repatriate or ban you is made by the Ministry of Home Affairs, not a court you can appeal to.",
          "hi": "अपने पास की वैधता समाप्त होने के बाद एक दिन भी सिंगापुर में रुकना Immigration Act के तहत अपराध है — 90 दिनों के बाद सज़ा तेज़ी से बढ़ जाती है, और आपको वापस भेजने या प्रतिबंधित करने का फ़ैसला Ministry of Home Affairs लेता है, किसी ऐसी अदालत में नहीं जहाँ आप अपील कर सकें।",
          "ta": "உங்கள் அனுமதியின் செல்லுபடியாகும் காலம் முடிந்த பிறகு ஒரு நாள் கூட சிங்கப்பூரில் தங்குவது Immigration Act இன் கீழ் ஒரு குற்றமாகும் — 90 நாட்களுக்குப் பிறகு தண்டனைகள் கடுமையாக அதிகரிக்கின்றன, மேலும் உங்களை நாடு திருப்பி அனுப்புவது அல்லது தடை செய்வது பற்றிய முடிவை Ministry of Home Affairs எடுக்கிறது, நீங்கள் மேல்முறையீடு செய்யக்கூடிய நீதிமன்றம் அல்ல.",
          "te": "మీ పాస్ చెల్లుబాటు ముగిసిన తర్వాత ఒక్క రోజు కూడా సింగపూర్‌లో ఉండటం Immigration Act ప్రకారం నేరం — 90 రోజుల తర్వాత శిక్షలు వేగంగా పెరుగుతాయి, మరియు మిమ్మల్ని స్వదేశానికి పంపడం లేదా నిషేధించడం అనే నిర్ణయం Ministry of Home Affairs తీసుకుంటుంది, మీరు అప్పీల్ చేయగల కోర్టు కాదు.",
          "ml": "നിങ്ങളുടെ പാസിന്റെ കാലാവധി കഴിഞ്ഞ് ഒരു ദിവസം പോലും സിംഗപ്പൂരിൽ തങ്ങുന്നത് Immigration Act പ്രകാരം ഒരു കുറ്റമാണ് — 90 ദിവസങ്ങൾക്ക് ശേഷം ശിക്ഷകൾ കുത്തനെ വർദ്ധിക്കുന്നു, കൂടാതെ നിങ്ങളെ സ്വദേശത്തേക്ക് അയക്കണോ വിലക്കണോ എന്ന തീരുമാനം എടുക്കുന്നത് Ministry of Home Affairs ആണ്, നിങ്ങൾക്ക് അപ്പീൽ നൽകാൻ കഴിയുന്ന ഒരു കോടതിയല്ല."},
    handles={"en": "overstaying · visa expiry · Immigration Act", "hi": "ओवरस्टे · वीज़ा समाप्ति · Immigration Act", "ta": "ஓவர்ஸ்டே · விசா காலாவதி · Immigration Act",
             "te": "ఓవర్‌స్టే · వీసా గడువు · Immigration Act", "ml": "ഓവർസ്റ്റേ · വിസ കാലാവധി · Immigration Act"},
    steps={"en": ["Always check your pass's exact expiry date yourself — don't assume it matches your job or course end date, and don't rely on an employer or agent to track it for you.",
                  "Overstaying for 90 days or less: up to $4,000 fine and/or up to 6 months' jail.",
                  "Overstaying for more than 90 days: at least 3 strokes of the cane are mandatory (a fine up to $6,000 applies only in the rare case caning cannot be carried out — for example, on medical grounds), on top of up to 6 months' jail.",
                  "Once caught, the Ministry of Home Affairs can order repatriation and a re-entry ban — this is an administrative decision, and it is not open to appeal the way a court sentence can be."],
           "hi": ["अपने पास की सही समाप्ति तिथि ख़ुद जाँचें — यह मान न लें कि यह आपकी नौकरी या कोर्स ख़त्म होने की तारीख़ से मेल खाती है, और इसे ट्रैक करने के लिए किसी नियोक्ता या एजेंट पर निर्भर न रहें।",
                  "90 दिन या उससे कम ओवरस्टे: $4,000 तक जुर्माना और/या 6 महीने तक जेल।",
                  "90 दिन से ज़्यादा ओवरस्टे: कम से कम 3 कोड़े अनिवार्य हैं (केवल उस दुर्लभ स्थिति में $6,000 तक जुर्माना लागू होता है जब कोड़े नहीं मारे जा सकते — जैसे चिकित्सीय कारणों से), 6 महीने तक की जेल के अलावा।",
                  "पकड़े जाने पर, Ministry of Home Affairs वापस भेजने और पुनः प्रवेश पर प्रतिबंध का आदेश दे सकता है — यह एक प्रशासनिक फ़ैसला है, और यह उस तरह अपील के लिए खुला नहीं है जैसे अदालती सज़ा हो सकती है।"],
           "ta": ["உங்கள் அனுமதியின் சரியான காலாவதி தேதியை நீங்களே சரிபார்க்கவும் — இது உங்கள் வேலை அல்லது படிப்பு முடியும் தேதியுடன் பொருந்தும் என்று கருதாதீர்கள், மேலும் அதைக் கண்காணிக்க ஒரு முதலாளி அல்லது முகவரை நம்பாதீர்கள்.",
                  "90 நாட்கள் அல்லது அதற்கும் குறைவான ஓவர்ஸ்டே: $4,000 வரை அபராதம் மற்றும்/அல்லது 6 மாதங்கள் வரை சிறை.",
                  "90 நாட்களுக்கு மேல் ஓவர்ஸ்டே: குறைந்தபட்சம் 3 கசையடிகள் கட்டாயம் (கசையடி நிறைவேற்ற முடியாத அரிதான சூழ்நிலையில் மட்டும் — எடுத்துக்காட்டாக மருத்துவ காரணங்களுக்காக — $6,000 வரை அபராதம் பொருந்தும்), 6 மாதங்கள் வரை சிறையுடன் கூடுதலாக.",
                  "பிடிக்கப்பட்டவுடன், Ministry of Home Affairs நாடு திருப்பி அனுப்புதல் மற்றும் மீண்டும் நுழைவதற்கான தடையை உத்தரவிடலாம் — இது ஒரு நிர்வாக முடிவு, மேலும் இது நீதிமன்ற தண்டனை போல மேல்முறையீட்டுக்கு உட்பட்டதல்ல."],
           "te": ["మీ పాస్ యొక్క ఖచ్చితమైన గడువు తేదీని మీరే తనిఖీ చేసుకోండి — ఇది మీ ఉద్యోగం లేదా కోర్సు ముగింపు తేదీతో సరిపోతుందని అనుకోకండి, మరియు దాన్ని ట్రాక్ చేయడానికి యజమాని లేదా ఏజెంట్‌పై ఆధారపడకండి.",
                  "90 రోజులు లేదా అంతకంటే తక్కువ ఓవర్‌స్టే: $4,000 వరకు జరిమానా మరియు/లేదా 6 నెలల వరకు జైలు.",
                  "90 రోజులకు మించి ఓవర్‌స్టే: కనీసం 3 కొరడా దెబ్బలు తప్పనిసరి (కొరడా దెబ్బలు అమలు చేయలేని అరుదైన సందర్భంలో మాత్రమే — ఉదాహరణకు వైద్య కారణాల వల్ల — $6,000 వరకు జరిమానా వర్తిస్తుంది), 6 నెలల వరకు జైలుకు అదనంగా.",
                  "పట్టుబడిన తర్వాత, Ministry of Home Affairs స్వదేశానికి పంపడం మరియు తిరిగి ప్రవేశంపై నిషేధాన్ని ఆదేశించవచ్చు — ఇది పరిపాలనాపరమైన నిర్ణయం, మరియు కోర్టు శిక్షలా అప్పీల్‌కు తెరిచి ఉండదు."],
           "ml": ["നിങ്ങളുടെ പാസിന്റെ കൃത്യമായ കാലാവധി തീയതി നിങ്ങൾ തന്നെ പരിശോധിക്കുക — ഇത് നിങ്ങളുടെ ജോലി അല്ലെങ്കിൽ കോഴ്‌സ് അവസാനിക്കുന്ന തീയതിയുമായി പൊരുത്തപ്പെടുമെന്ന് കരുതരുത്, ഇത് ട്രാക്ക് ചെയ്യാൻ ഒരു തൊഴിലുടമയെയോ ഏജന്റിനെയോ ആശ്രയിക്കരുത്.",
                  "90 ദിവസമോ അതിൽ കുറവോ ഓവർസ്റ്റേ: $4,000 വരെ പിഴയും/അല്ലെങ്കിൽ 6 മാസം വരെ ജയിലും.",
                  "90 ദിവസത്തിൽ കൂടുതൽ ഓവർസ്റ്റേ: കുറഞ്ഞത് 3 ചമ്മട്ടിയടി നിർബന്ധമാണ് (ചമ്മട്ടിയടി നടപ്പിലാക്കാൻ കഴിയാത്ത അപൂർവ സാഹചര്യത്തിൽ മാത്രം — ഉദാഹരണത്തിന് ആരോഗ്യപരമായ കാരണങ്ങളാൽ — $6,000 വരെ പിഴ ബാധകമാകും), 6 മാസം വരെ ജയിലിന് പുറമെ.",
                  "പിടിക്കപ്പെട്ടുകഴിഞ്ഞാൽ, Ministry of Home Affairs സ്വദേശത്തേക്ക് അയക്കാനും തിരിച്ചുവരവിനുള്ള വിലക്കിനും ഉത്തരവിടാം — ഇത് ഒരു ഭരണപരമായ തീരുമാനമാണ്, കോടതി വിധി പോലെ അപ്പീലിന് തുറന്നതല്ല."]},
    docs={"en": ["≤ 90 days overstay: fine up to $4,000, and/or jail up to 6 months.",
                 "> 90 days overstay: mandatory caning (at least 3 strokes), plus jail up to 6 months.",
                 "Repatriation and a ban on future entry to Singapore, at the Ministry's discretion."],
          "hi": ["≤ 90 दिन ओवरस्टे: $4,000 तक जुर्माना, और/या 6 महीने तक जेल।",
                 "> 90 दिन ओवरस्टे: अनिवार्य कोड़े (कम से कम 3), साथ में 6 महीने तक जेल।",
                 "मंत्रालय के विवेक पर, वापस भेजना और भविष्य में सिंगापुर में प्रवेश पर प्रतिबंध।"],
          "ta": ["≤ 90 நாட்கள் ஓவர்ஸ்டே: $4,000 வரை அபராதம், மற்றும்/அல்லது 6 மாதங்கள் வரை சிறை.",
                 "> 90 நாட்கள் ஓவர்ஸ்டே: கட்டாய கசையடி (குறைந்தபட்சம் 3), 6 மாதங்கள் வரை சிறையுடன்.",
                 "அமைச்சகத்தின் விருப்பப்படி, நாடு திருப்பி அனுப்புதல் மற்றும் சிங்கப்பூருக்கு எதிர்கால நுழைவுக்கான தடை."],
          "te": ["≤ 90 రోజుల ఓవర్‌స్టే: $4,000 వరకు జరిమానా, మరియు/లేదా 6 నెలల వరకు జైలు.",
                 "> 90 రోజుల ఓవర్‌స్టే: తప్పనిసరి కొరడా దెబ్బలు (కనీసం 3), 6 నెలల వరకు జైలుతో పాటు.",
                 "మంత్రిత్వ శాఖ విచక్షణ మేరకు, స్వదేశానికి పంపడం మరియు సింగపూర్‌లోకి భవిష్యత్తు ప్రవేశంపై నిషేధం."],
          "ml": ["≤ 90 ദിവസം ഓവർസ്റ്റേ: $4,000 വരെ പിഴയും/അല്ലെങ്കിൽ 6 മാസം വരെ ജയിലും.",
                 "> 90 ദിവസം ഓവർസ്റ്റേ: നിർബന്ധിത ചമ്മട്ടിയടി (കുറഞ്ഞത് 3), 6 മാസം വരെ ജയിലിനൊപ്പം.",
                 "മന്ത്രാലയത്തിന്റെ വിവേചനാധികാരപ്രകാരം, സ്വദേശത്തേക്ക് അയക്കലും സിംഗപ്പൂരിലേക്കുള്ള ഭാവി പ്രവേശനത്തിനുള്ള വിലക്കും."]},
    note={"en": "If your pass is close to expiring and your renewal or exit is delayed for any reason, contact ICA before the expiry date, not after — explaining a problem in advance is treated very differently from being caught after the fact.",
          "hi": "अगर आपका पास समाप्त होने वाला है और किसी कारण से आपका नवीनीकरण या बाहर जाना विलंबित हो रहा है, तो समाप्ति तिथि से पहले ICA से संपर्क करें, बाद में नहीं — पहले से समस्या बताना, बाद में पकड़े जाने से बिल्कुल अलग तरह से देखा जाता है।",
          "ta": "உங்கள் அனுமதி காலாவதியாக நெருங்கிக் கொண்டிருந்தால், ஏதேனும் காரணத்தால் உங்கள் புதுப்பித்தல் அல்லது வெளியேறுதல் தாமதமாகிறது என்றால், காலாவதி தேதிக்கு முன் ICA-ஐ தொடர்பு கொள்ளுங்கள், பிறகு அல்ல — முன்கூட்டியே ஒரு பிரச்சினையை விளக்குவது, பிறகு பிடிபடுவதை விட முற்றிலும் வித்தியாசமாக நடத்தப்படும்.",
          "te": "మీ పాస్ గడువు ముగియడానికి దగ్గరగా ఉండి, ఏదైనా కారణం వల్ల మీ పునరుద్ధరణ లేదా నిష్క్రమణ ఆలస్యం అవుతుంటే, గడువు తేదీకి ముందే ICAని సంప్రదించండి, తర్వాత కాదు — ముందుగానే సమస్యను వివరించడం, తర్వాత పట్టుబడటం కంటే చాలా భిన్నంగా పరిగణించబడుతుంది.",
          "ml": "നിങ്ങളുടെ പാസ് കാലാവധി കഴിയാൻ അടുത്തിരിക്കുകയും ഏതെങ്കിലും കാരണത്താൽ നിങ്ങളുടെ പുതുക്കൽ അല്ലെങ്കിൽ പുറത്തുപോക്ക് വൈകുകയും ചെയ്യുന്നുവെങ്കിൽ, കാലാവധി തീയതിക്ക് മുമ്പ് ICA യെ ബന്ധപ്പെടുക, അതിനുശേഷമല്ല — മുൻകൂട്ടി ഒരു പ്രശ്നം വിശദീകരിക്കുന്നത്, പിന്നീട് പിടിക്കപ്പെടുന്നതിനെക്കാൾ വളരെ വ്യത്യസ്തമായി പരിഗണിക്കപ്പെടും."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://eservices.ica.gov.sg/ipienquiry/web/icheck/landing", "label": {"en": "↗ ICA — check your pass validity", "hi": "↗ ICA — अपने पास की वैधता जाँचें", "ta": "↗ ICA — உங்கள் அனுமதியின் செல்லுபடியை சரிபார்க்கவும்", "te": "↗ ICA — మీ పాస్ చెల్లుబాటును తనిఖీ చేయండి", "ml": "↗ ICA — നിങ്ങളുടെ പാസിന്റെ സാധുത പരിശോധിക്കുക"}},
        {"href": "https://sso.agc.gov.sg/Act/IA1959", "label": {"en": "↗ Immigration Act 1959 (full text)", "hi": "↗ Immigration Act 1959 (पूरा पाठ)", "ta": "↗ Immigration Act 1959 (முழு உரை)", "te": "↗ Immigration Act 1959 (పూర్తి పాఠం)", "ml": "↗ Immigration Act 1959 (മുഴുവൻ വാചകം)"}},
    ],
)

entry(
    category="sg_laws", country="singapore", badge_official=True, toggle_key="what_to_know",
    steps_label_key="key_facts", docs_label_key="penalties",
    search_en="singapore littering jaywalking smoking fine mrt eating drinking everyday laws",
    title={"en": "Everyday fines you should know", "hi": "रोज़मर्रा के जुर्माने जो आपको पता होने चाहिए", "ta": "நீங்கள் தெரிந்திருக்க வேண்டிய அன்றாட அபராதங்கள்",
           "te": "మీకు తెలిసి ఉండాల్సిన నిత్య జరిమానాలు", "ml": "നിങ്ങൾ അറിഞ്ഞിരിക്കേണ്ട ദൈനംദിന പിഴകൾ"},
    desc={"en": "Singapore enforces a set of everyday rules strictly and consistently — most visitors and residents never encounter a serious crime, but small fines for littering, jaywalking, smoking in the wrong place, or eating on the train catch people who simply didn't know the rule.",
          "hi": "सिंगापुर रोज़मर्रा के कुछ नियमों को सख़्ती और लगातार लागू करता है — ज़्यादातर आगंतुक और निवासी कभी किसी गंभीर अपराध का सामना नहीं करते, लेकिन कूड़ा फेंकने, जेवॉकिंग, ग़लत जगह धूम्रपान करने, या ट्रेन में खाने पर छोटे जुर्माने उन लोगों को पकड़ लेते हैं जिन्हें बस नियम पता नहीं था।",
          "ta": "சிங்கப்பூர் சில அன்றாட விதிகளை கடுமையாகவும் தொடர்ச்சியாகவும் அமல்படுத்துகிறது — பெரும்பாலான வருகையாளர்களும் குடியிருப்பாளர்களும் ஒருபோதும் ஒரு தீவிர குற்றத்தை எதிர்கொள்வதில்லை, ஆனால் குப்பை போடுதல், ஜேவாக்கிங், தவறான இடத்தில் புகைபிடித்தல், அல்லது ரயிலில் சாப்பிடுதல் ஆகியவற்றுக்கான சிறிய அபராதங்கள் விதியை அறியாதவர்களைப் பிடிக்கின்றன.",
          "te": "సింగపూర్ కొన్ని రోజువారీ నియమాలను కఠినంగా మరియు స్థిరంగా అమలు చేస్తుంది — చాలా మంది సందర్శకులు మరియు నివాసితులు ఎప్పుడూ తీవ్రమైన నేరాన్ని ఎదుర్కోరు, కానీ చెత్త వేయడం, జేవాకింగ్, తప్పు స్థలంలో ధూమపానం, లేదా రైల్లో తినడం వంటి వాటికి చిన్న జరిమానాలు నియమం తెలియని వారిని పట్టుకుంటాయి.",
          "ml": "സിംഗപ്പൂർ ചില ദൈനംദിന നിയമങ്ങൾ കർശനമായും സ്ഥിരമായും നടപ്പിലാക്കുന്നു — മിക്ക സന്ദർശകരും താമസക്കാരും ഒരിക്കലും ഗുരുതരമായ കുറ്റകൃത്യം നേരിടില്ല, പക്ഷേ മാലിന്യം വലിച്ചെറിയൽ, ജെയ്‌വാക്കിംഗ്, തെറ്റായ സ്ഥലത്ത് പുകവലി, അല്ലെങ്കിൽ ട്രെയിനിൽ ഭക്ഷണം കഴിക്കൽ എന്നിവയ്ക്കുള്ള ചെറിയ പിഴകൾ നിയമം അറിയാത്തവരെ പിടികൂടുന്നു."},
    handles={"en": "littering · jaywalking · smoking · MRT rules", "hi": "कूड़ा फेंकना · जेवॉकिंग · धूम्रपान · MRT नियम", "ta": "குப்பை போடுதல் · ஜேவாக்கிங் · புகைபிடித்தல் · MRT விதிகள்",
             "te": "చెత్త వేయడం · జేవాకింగ్ · ధూమపానం · MRT నియమాలు", "ml": "മാലിന്യം വലിച്ചെറിയൽ · ജെയ്‌വാക്കിംഗ് · പുകവലി · MRT നിയമങ്ങൾ"},
    steps={"en": ["Littering — dropping even a cigarette butt or a tissue — is a strict-liability offence: fines start at $300 for a first offence and rise sharply for repeat offenders, and a Corrective Work Order (public litter-picking, in a vest, sometimes photographed) can be imposed alongside or instead of a fine.",
                  "Jaywalking — crossing within 50 metres of a designated crossing or footbridge instead of using it — carries a fine (around $50 for a first offence, higher on prosecution) and applies even on quiet roads with no traffic in sight.",
                  "Smoking is banned outside specifically marked yellow-box smoking areas — this includes most bus stops, parks, and building entrances — with fines around $200 per offence; the ban has been extended to more outdoor public areas in recent years.",
                  "Eating or drinking anything, including plain water, in an MRT/LRT train or in a paid area of a station is banned and can draw a fine of up to $500 — a rule that surprises many first-time visitors."],
           "hi": ["कूड़ा फेंकना — यहाँ तक कि सिगरेट का टुकड़ा या टिशू गिराना भी — एक सख़्त-दायित्व वाला अपराध है: पहली बार पर जुर्माना $300 से शुरू होता है और बार-बार अपराध करने पर तेज़ी से बढ़ता है, और जुर्माने के साथ या उसकी जगह Corrective Work Order (जनता के सामने कूड़ा उठाना, वेस्ट पहनकर, कभी-कभी फ़ोटो खींची जाती है) भी लगाया जा सकता है।",
                  "जेवॉकिंग — निर्धारित क्रॉसिंग या फ़ुटब्रिज के 50 मीटर के भीतर उसका इस्तेमाल किए बिना सड़क पार करना — जुर्माने का कारण बनता है (पहली बार लगभग $50, मुक़दमे पर ज़्यादा) और यह उन शांत सड़कों पर भी लागू होता है जहाँ कोई ट्रैफ़िक नज़र नहीं आता।",
                  "पीले-बॉक्स से चिह्नित धूम्रपान क्षेत्रों के बाहर धूम्रपान प्रतिबंधित है — इसमें ज़्यादातर बस स्टॉप, पार्क, और इमारतों के प्रवेश द्वार शामिल हैं — जुर्माना लगभग $200 प्रति अपराध है; हाल के वर्षों में यह प्रतिबंध और खुले सार्वजनिक क्षेत्रों तक बढ़ाया गया है।",
                  "MRT/LRT ट्रेन में या स्टेशन के पेड एरिया में कुछ भी खाना या पीना, यहाँ तक कि सादा पानी भी, प्रतिबंधित है और $500 तक का जुर्माना लग सकता है — यह नियम कई पहली बार आने वाले आगंतुकों को चौंका देता है।"],
           "ta": ["குப்பை போடுதல் — ஒரு சிகரெட் துண்டு அல்லது டிஷ்யூவைக் கீழே போடுவது கூட — ஒரு கடும்-பொறுப்பு குற்றமாகும்: முதல் குற்றத்திற்கு அபராதம் $300 இலிருந்து தொடங்கி மீண்டும் மீண்டும் செய்பவர்களுக்கு வேகமாக அதிகரிக்கிறது, மேலும் அபராதத்துடன் அல்லது அதற்குப் பதிலாக Corrective Work Order (பொதுவில் குப்பை பொறுக்குதல், வெஸ்ட் அணிந்து, சில நேரங்களில் புகைப்படம் எடுக்கப்படும்) விதிக்கப்படலாம்.",
                  "ஜேவாக்கிங் — நியமிக்கப்பட்ட கிராசிங் அல்லது மேம்பாலத்தை பயன்படுத்தாமல் அதன் 50 மீட்டருக்குள் சாலையைக் கடப்பது — அபராதத்தை ஏற்படுத்துகிறது (முதல் குற்றத்திற்கு சுமார் $50, வழக்குத் தொடரப்பட்டால் அதிகம்) மேலும் போக்குவரத்து தெரியாத அமைதியான சாலைகளிலும் இது பொருந்தும்.",
                  "மஞ்சள்-பெட்டி குறியிடப்பட்ட புகைபிடிக்கும் பகுதிகளுக்கு வெளியே புகைபிடிப்பது தடைசெய்யப்பட்டுள்ளது — இதில் பெரும்பாலான பேருந்து நிறுத்தங்கள், பூங்காக்கள், மற்றும் கட்டிட நுழைவாயில்கள் அடங்கும் — ஒரு குற்றத்திற்கு அபராதம் சுமார் $200; சமீபத்திய ஆண்டுகளில் இந்த தடை மேலும் திறந்தவெளி பொது இடங்களுக்கு விரிவுபடுத்தப்பட்டுள்ளது.",
                  "MRT/LRT ரயிலில் அல்லது நிலையத்தின் பணம் செலுத்தப்பட்ட பகுதியில் எதையும் சாப்பிடுவது அல்லது குடிப்பது, சாதாரண தண்ணீர் உட்பட, தடைசெய்யப்பட்டுள்ளது, மேலும் $500 வரை அபராதத்தை ஏற்படுத்தலாம் — இந்த விதி முதன்முறையாக வருபவர்கள் பலரை ஆச்சரியப்படுத்துகிறது."],
           "te": ["చెత్త వేయడం — ఒక సిగరెట్ ముక్క లేదా టిష్యూ పడేయడం కూడా — ఇది కఠిన-బాధ్యత నేరం: మొదటి నేరానికి జరిమానా $300 నుండి మొదలవుతుంది మరియు పునరావృత నేరస్థులకు వేగంగా పెరుగుతుంది, మరియు జరిమానాతో పాటు లేదా దానికి బదులుగా Corrective Work Order (బహిరంగంగా చెత్త ఏరడం, వెస్ట్ ధరించి, కొన్నిసార్లు ఫోటో తీయబడుతుంది) విధించవచ్చు.",
                  "జేవాకింగ్ — నిర్దేశిత క్రాసింగ్ లేదా ఫుట్‌బ్రిడ్జికి 50 మీటర్ల లోపు దాన్ని ఉపయోగించకుండా రోడ్డు దాటడం — జరిమానాకు దారితీస్తుంది (మొదటి నేరానికి సుమారు $50, కోర్టులో విచారణ జరిగితే ఎక్కువ) మరియు ట్రాఫిక్ కనిపించని నిశ్శబ్ద రోడ్లపై కూడా ఇది వర్తిస్తుంది.",
                  "పసుపు-పెట్టె గుర్తు పెట్టిన ధూమపాన ప్రాంతాలకు వెలుపల ధూమపానం నిషేధించబడింది — ఇందులో చాలా బస్ స్టాప్‌లు, పార్కులు, మరియు భవనాల ప్రవేశద్వారాలు ఉన్నాయి — నేరానికి జరిమానా సుమారు $200; ఇటీవలి సంవత్సరాలలో ఈ నిషేధం మరిన్ని బహిరంగ ప్రదేశాలకు విస్తరించబడింది.",
                  "MRT/LRT రైల్లో లేదా స్టేషన్ చెల్లింపు ప్రాంతంలో ఏదైనా తినడం లేదా త్రాగడం, సాదా నీరుతో సహా, నిషేధించబడింది మరియు $500 వరకు జరిమానాకు దారితీయవచ్చు — ఈ నియమం మొదటిసారి వచ్చే చాలా మంది సందర్శకులను ఆశ్చర్యపరుస్తుంది."],
           "ml": ["മാലിന്യം വലിച്ചെറിയൽ — ഒരു സിഗരറ്റ് കുറ്റിയോ ടിഷ്യുവോ താഴെയിടുന്നത് പോലും — ഇത് കർശന-ബാധ്യതാ കുറ്റമാണ്: ആദ്യ കുറ്റത്തിന് പിഴ $300 മുതൽ ആരംഭിച്ച് ആവർത്തിക്കുന്നവർക്ക് വേഗത്തിൽ ഉയരുന്നു, കൂടാതെ പിഴയോടൊപ്പമോ അതിനുപകരമോ Corrective Work Order (പൊതുവായി മാലിന്യം പെറുക്കൽ, വെസ്റ്റ് ധരിച്ച്, ചിലപ്പോൾ ഫോട്ടോ എടുക്കപ്പെടും) ചുമത്താം.",
                  "ജെയ്‌വാക്കിംഗ് — നിശ്ചയിച്ച ക്രോസിംഗിന്റെയോ നടപ്പാലത്തിന്റെയോ 50 മീറ്ററിനുള്ളിൽ അത് ഉപയോഗിക്കാതെ റോഡ് മുറിച്ചുകടക്കുന്നത് — പിഴയ്ക്ക് കാരണമാകുന്നു (ആദ്യ കുറ്റത്തിന് ഏകദേശം $50, കോടതിയിൽ വിചാരണ ചെയ്താൽ കൂടുതൽ) കൂടാതെ ട്രാഫിക് കാണാത്ത ശാന്തമായ റോഡുകളിലും ഇത് ബാധകമാണ്.",
                  "മഞ്ഞ-ബോക്സ് അടയാളപ്പെടുത്തിയ പുകവലി പ്രദേശങ്ങൾക്ക് പുറത്ത് പുകവലി നിരോധിച്ചിരിക്കുന്നു — ഇതിൽ മിക്ക ബസ് സ്റ്റോപ്പുകളും പാർക്കുകളും കെട്ടിട പ്രവേശന കവാടങ്ങളും ഉൾപ്പെടുന്നു — ഒരു കുറ്റത്തിന് പിഴ ഏകദേശം $200; സമീപ വർഷങ്ങളിൽ ഈ നിരോധനം കൂടുതൽ പുറംസ്ഥല പൊതു ഇടങ്ങളിലേക്ക് വ്യാപിപ്പിച്ചു.",
                  "MRT/LRT ട്രെയിനിലോ സ്റ്റേഷന്റെ പണമടച്ച ഭാഗത്തോ എന്തെങ്കിലും കഴിക്കുന്നതോ കുടിക്കുന്നതോ, സാധാരണ വെള്ളം ഉൾപ്പെടെ, നിരോധിച്ചിരിക്കുന്നു, കൂടാതെ $500 വരെ പിഴ ചുമത്താം — ഈ നിയമം ആദ്യമായി വരുന്ന പല സന്ദർശകരെയും ഞെട്ടിക്കുന്നു."]},
    docs={"en": ["Littering: fine from $300 (first offence) up to $2,000–$10,000 for repeat/court cases, plus possible Corrective Work Order.",
                 "Jaywalking: fine around $50 (composition), higher if prosecuted in court.",
                 "Smoking outside designated areas: fine around $200 per offence.",
                 "Eating/drinking on the MRT/LRT (paid areas and trains): fine up to $500."],
          "hi": ["कूड़ा फेंकना: पहली बार $300 से लेकर बार-बार/अदालती मामलों के लिए $2,000–$10,000 तक जुर्माना, साथ में संभावित Corrective Work Order।",
                 "जेवॉकिंग: लगभग $50 जुर्माना (कंपोज़िशन), अदालत में मुक़दमा चलने पर ज़्यादा।",
                 "निर्धारित क्षेत्रों के बाहर धूम्रपान: लगभग $200 प्रति अपराध जुर्माना।",
                 "MRT/LRT में खाना/पीना (पेड एरिया और ट्रेनों में): $500 तक जुर्माना।"],
          "ta": ["குப்பை போடுதல்: முதல் குற்றத்திற்கு $300 முதல் மீண்டும் மீண்டும்/நீதிமன்ற வழக்குகளுக்கு $2,000–$10,000 வரை அபராதம், மேலும் Corrective Work Order விதிக்கப்படலாம்.",
                 "ஜேவாக்கிங்: சுமார் $50 அபராதம் (compositions), நீதிமன்றத்தில் வழக்குத் தொடரப்பட்டால் அதிகம்.",
                 "நியமிக்கப்பட்ட பகுதிகளுக்கு வெளியே புகைபிடித்தல்: ஒரு குற்றத்திற்கு சுமார் $200 அபராதம்.",
                 "MRT/LRT இல் சாப்பிடுதல்/குடித்தல் (பணம் செலுத்தப்பட்ட பகுதிகள் மற்றும் ரயில்களில்): $500 வரை அபராதம்."],
          "te": ["చెత్త వేయడం: మొదటి నేరానికి $300 నుండి పునరావృత/కోర్టు కేసులకు $2,000–$10,000 వరకు జరిమానా, అదనంగా Corrective Work Order విధించవచ్చు.",
                 "జేవాకింగ్: సుమారు $50 జరిమానా (compositions), కోర్టులో విచారణ జరిగితే ఎక్కువ.",
                 "నిర్దేశిత ప్రాంతాలకు వెలుపల ధూమపానం: నేరానికి సుమారు $200 జరిమానా.",
                 "MRT/LRTలో తినడం/త్రాగడం (చెల్లింపు ప్రాంతాలు మరియు రైళ్లలో): $500 వరకు జరిమానా."],
          "ml": ["മാലിന്യം വലിച്ചെറിയൽ: ആദ്യ കുറ്റത്തിന് $300 മുതൽ ആവർത്തിച്ചുള്ള/കോടതി കേസുകൾക്ക് $2,000–$10,000 വരെ പിഴ, കൂടാതെ Corrective Work Order ചുമത്താം.",
                 "ജെയ്‌വാക്കിംഗ്: ഏകദേശം $50 പിഴ (compositions), കോടതിയിൽ വിചാരണ ചെയ്താൽ കൂടുതൽ.",
                 "നിശ്ചിത പ്രദേശങ്ങൾക്ക് പുറത്ത് പുകവലി: ഒരു കുറ്റത്തിന് ഏകദേശം $200 പിഴ.",
                 "MRT/LRTൽ ഭക്ഷണം/പാനീയം (പണമടച്ച ഭാഗങ്ങളും ട്രെയിനുകളും): $500 വരെ പിഴ."]},
    note={"en": "None of these are enforced through warnings the way some countries do it — carry a small bag for your own litter, use marked crossings, check for the yellow smoking-permitted boxes, and finish your drink before you tap in at the MRT gantry.",
          "hi": "इनमें से कोई भी कुछ देशों की तरह चेतावनी देकर लागू नहीं किया जाता — अपने कूड़े के लिए एक छोटा बैग रखें, चिह्नित क्रॉसिंग का इस्तेमाल करें, पीले धूम्रपान-अनुमति बॉक्स देखें, और MRT गेट पर टैप करने से पहले अपना पेय ख़त्म करें।",
          "ta": "இவற்றில் எதுவும் சில நாடுகள் செய்வது போல் எச்சரிக்கை மூலம் அமல்படுத்தப்படுவதில்லை — உங்கள் சொந்த குப்பைக்கு ஒரு சிறிய பையை எடுத்துச் செல்லுங்கள், குறியிடப்பட்ட கிராசிங்குகளை பயன்படுத்துங்கள், மஞ்சள் புகைபிடிக்க-அனுமதிக்கப்பட்ட பெட்டிகளை சரிபார்க்கவும், மேலும் MRT நுழைவாயிலில் தட்டுவதற்கு முன் உங்கள் பானத்தை முடித்துவிடுங்கள்.",
          "te": "వీటిలో ఏదీ కొన్ని దేశాలు చేసేలా హెచ్చరికల ద్వారా అమలు చేయబడదు — మీ స్వంత చెత్త కోసం ఒక చిన్న సంచిని తీసుకెళ్లండి, గుర్తించిన క్రాసింగ్‌లను ఉపయోగించండి, పసుపు ధూమపాన-అనుమతి పెట్టెలను తనిఖీ చేయండి, మరియు MRT గేటు వద్ద ట్యాప్ చేయడానికి ముందు మీ పానీయాన్ని పూర్తి చేయండి.",
          "ml": "ഇവയൊന്നും ചില രാജ്യങ്ങൾ ചെയ്യുന്നതുപോലെ മുന്നറിയിപ്പുകളിലൂടെയല്ല നടപ്പിലാക്കുന്നത് — നിങ്ങളുടെ സ്വന്തം മാലിന്യത്തിനായി ഒരു ചെറിയ ബാഗ് കൊണ്ടുപോകുക, അടയാളപ്പെടുത്തിയ ക്രോസിംഗുകൾ ഉപയോഗിക്കുക, മഞ്ഞ പുകവലി-അനുവദനീയമായ ബോക്സുകൾ പരിശോധിക്കുക, MRT ഗേറ്റിൽ ടാപ്പ് ചെയ്യുന്നതിന് മുമ്പ് നിങ്ങളുടെ പാനീയം തീർക്കുക."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.nea.gov.sg/our-services/smoking-prohibition/overview", "label": {"en": "↗ NEA — smoking prohibition rules", "hi": "↗ NEA — धूम्रपान प्रतिबंध नियम", "ta": "↗ NEA — புகைபிடித்தல் தடை விதிகள்", "te": "↗ NEA — ధూమపాన నిషేధ నియమాలు", "ml": "↗ NEA — പുകവലി നിരോധന നിയമങ്ങൾ"}},
        {"href": "https://sso.agc.gov.sg/Act/RTSA1995", "label": {"en": "↗ Rapid Transit Systems Act (MRT/LRT rules)", "hi": "↗ Rapid Transit Systems Act (MRT/LRT नियम)", "ta": "↗ Rapid Transit Systems Act (MRT/LRT விதிகள்)", "te": "↗ Rapid Transit Systems Act (MRT/LRT నియమాలు)", "ml": "↗ Rapid Transit Systems Act (MRT/LRT നിയമങ്ങൾ)"}},
    ],
)

entry(
    category="sg_workpermit", country="singapore", badge_official=True,
    search_en="singapore work permit foreign worker what is levy quota dependant",
    title={"en": "What a Work Permit is, and who holds one", "hi": "Work Permit क्या है, और यह किसके पास होता है", "ta": "Work Permit என்றால் என்ன, யாரிடம் இது இருக்கும்",
           "te": "Work Permit అంటే ఏమిటి, ఎవరు దీన్ని కలిగి ఉంటారు", "ml": "എന്താണ് വർക്ക് പെർമിറ്റ്, ആരാണ് ഇത് കൈവശം വയ്ക്കുന്നത്"},
    desc={"en": "The Work Permit is Singapore's pass for lower- and semi-skilled foreign workers — mainly in construction, manufacturing, marine, process, and services sectors, and for foreign domestic workers — and it works differently from an Employment Pass or S Pass in a few important ways.",
          "hi": "Work Permit सिंगापुर का वह पास है जो कम- और अर्ध-कुशल विदेशी श्रमिकों के लिए है — मुख्यतः निर्माण, विनिर्माण, मरीन, प्रोसेस, और सेवा क्षेत्रों में, और विदेशी घरेलू कामगारों के लिए — और यह Employment Pass या S Pass से कुछ महत्वपूर्ण तरीक़ों से अलग तरह से काम करता है।",
          "ta": "Work Permit என்பது குறைந்த- மற்றும் அரை-திறன் கொண்ட வெளிநாட்டு தொழிலாளர்களுக்கான சிங்கப்பூர் அனுமதி — முக்கியமாக கட்டுமானம், உற்பத்தி, மரைன், செயலாக்கம், மற்றும் சேவைத் துறைகளில், மற்றும் வெளிநாட்டு வீட்டுப் பணியாளர்களுக்கும் — மேலும் இது Employment Pass அல்லது S Pass இலிருந்து சில முக்கியமான வழிகளில் வித்தியாசமாக செயல்படுகிறது.",
          "te": "Work Permit అనేది తక్కువ- మరియు అర్ధ-నైపుణ్యం గల విదేశీ కార్మికుల కోసం సింగపూర్ పాస్ — ప్రధానంగా నిర్మాణం, తయారీ, మెరైన్, ప్రాసెస్, మరియు సేవా రంగాలలో, మరియు విదేశీ గృహ కార్మికుల కోసం — మరియు ఇది Employment Pass లేదా S Pass నుండి కొన్ని ముఖ్యమైన విధాలుగా భిన్నంగా పనిచేస్తుంది.",
          "ml": "കുറഞ്ഞ- ഇടത്തരം- വൈദഗ്ധ്യമുള്ള വിദേശ തൊഴിലാളികൾക്കുള്ള സിംഗപ്പൂരിന്റെ പാസാണ് വർക്ക് പെർമിറ്റ് — പ്രധാനമായും നിർമ്മാണം, ഉൽപ്പാദനം, മറൈൻ, പ്രോസസ്, സേവന മേഖലകളിൽ, കൂടാതെ വിദേശ ഗാർഹിക തൊഴിലാളികൾക്കും — ഇത് Employment Pass അല്ലെങ്കിൽ S Pass ൽ നിന്ന് ചില പ്രധാന കാര്യങ്ങളിൽ വ്യത്യസ്തമായി പ്രവർത്തിക്കുന്നു."},
    handles={"en": "construction · manufacturing · services · domestic work", "hi": "निर्माण · विनिर्माण · सेवाएँ · घरेलू काम", "ta": "கட்டுமானம் · உற்பத்தி · சேவைகள் · வீட்டு வேலை",
             "te": "నిర్మాణం · తయారీ · సేవలు · గృహ పని", "ml": "നിർമ്മാണം · ഉൽപ്പാദനം · സേവനങ്ങൾ · ഗാർഹിക ജോലി"},
    steps={"en": ["Your employer applies for and holds the Work Permit — you don't apply yourself, and the permit is tied to that one employer and that one job.",
                  "Employers pay a monthly levy for each Work Permit holder and must stay within a quota (the “dependency ratio ceiling”) — this affects hiring decisions, but it's the employer's obligation, not yours.",
                  "Before the permit is issued, you'll go through a medical check-up and biometric (fingerprint/iris) registration — both are compulsory, not optional.",
                  "Work Permit holders generally cannot bring dependants to Singapore on this pass, and need MOM's written approval before marrying a Singapore Citizen or Permanent Resident while holding the permit."],
           "hi": ["आपका नियोक्ता Work Permit के लिए आवेदन करता है और उसे रखता है — आप ख़ुद आवेदन नहीं करते, और यह परमिट उस एक नियोक्ता और उस एक काम से जुड़ा होता है।",
                  "नियोक्ता हर Work Permit धारक के लिए मासिक लेवी चुकाते हैं और एक कोटा (“डिपेंडेंसी रेशियो सीलिंग”) के भीतर रहना होता है — यह भर्ती के फ़ैसलों को प्रभावित करता है, लेकिन यह नियोक्ता का दायित्व है, आपका नहीं।",
                  "परमिट जारी होने से पहले, आपकी मेडिकल जाँच और बायोमेट्रिक (फिंगरप्रिंट/आइरिस) पंजीकरण होगा — दोनों अनिवार्य हैं, वैकल्पिक नहीं।",
                  "Work Permit धारक आम तौर पर इस पास पर आश्रितों को सिंगापुर नहीं ला सकते, और परमिट रखते हुए किसी सिंगापुर नागरिक या स्थायी निवासी से शादी करने से पहले MOM की लिखित मंज़ूरी चाहिए।"],
           "ta": ["உங்கள் முதலாளி Work Permit-க்கு விண்ணப்பித்து அதை வைத்திருக்கிறார் — நீங்கள் நேரடியாக விண்ணப்பிக்க வேண்டாம், மேலும் இந்த அனுமதி அந்த ஒரு முதலாளி மற்றும் அந்த ஒரு வேலையுடன் மட்டுமே இணைக்கப்பட்டுள்ளது.",
                  "முதலாளிகள் ஒவ்வொரு Work Permit வைத்திருப்பவருக்கும் மாதாந்திர லெவி செலுத்துகிறார்கள், மேலும் ஒரு ஒதுக்கீட்டிற்குள் (“dependency ratio ceiling”) இருக்க வேண்டும் — இது வேலைவாய்ப்பு முடிவுகளை பாதிக்கிறது, ஆனால் இது முதலாளியின் கடமை, உங்களுடையது அல்ல.",
                  "அனுமதி வழங்கப்படுவதற்கு முன், நீங்கள் ஒரு மருத்துவ பரிசோதனை மற்றும் பயோமெட்ரிக் (கைரேகை/கண்மணி) பதிவை மேற்கொள்வீர்கள் — இரண்டும் கட்டாயமானவை, விருப்பமானவை அல்ல.",
                  "Work Permit வைத்திருப்பவர்கள் பொதுவாக இந்த அனுமதியில் சார்ந்தோரை சிங்கப்பூருக்கு அழைத்து வர முடியாது, மேலும் அனுமதியை வைத்திருக்கும்போது ஒரு சிங்கப்பூர் குடிமகன் அல்லது நிரந்தர வதிவிடையாளரை மணக்க MOM இன் எழுத்துப்பூர்வ ஒப்புதல் தேவை."],
           "te": ["మీ యజమాని Work Permit కోసం దరఖాస్తు చేసి దాన్ని కలిగి ఉంటారు — మీరు స్వయంగా దరఖాస్తు చేయరు, మరియు ఈ పర్మిట్ ఆ ఒక్క యజమాని మరియు ఆ ఒక్క పనితో మాత్రమే ముడిపడి ఉంటుంది.",
                  "యజమానులు ప్రతి Work Permit హోల్డర్ కోసం నెలవారీ లెవీ చెల్లిస్తారు మరియు కోటా (“dependency ratio ceiling”) లోపల ఉండాలి — ఇది నియామక నిర్ణయాలను ప్రభావితం చేస్తుంది, కానీ ఇది యజమాని బాధ్యత, మీది కాదు.",
                  "పర్మిట్ జారీ చేయడానికి ముందు, మీరు వైద్య పరీక్ష మరియు బయోమెట్రిక్ (వేలిముద్ర/ఐరిస్) నమోదు ద్వారా వెళ్తారు — రెండూ తప్పనిసరి, ఐచ్ఛికం కాదు.",
                  "Work Permit హోల్డర్లు సాధారణంగా ఈ పాస్‌పై డిపెండెంట్లను సింగపూర్‌కు తీసుకురాలేరు, మరియు పర్మిట్ కలిగి ఉన్నప్పుడు సింగపూర్ పౌరుడు లేదా శాశ్వత నివాసిని వివాహం చేసుకునే ముందు MOM యొక్క వ్రాతపూర్వక ఆమోదం అవసరం."],
           "ml": ["നിങ്ങളുടെ തൊഴിലുടമ വർക്ക് പെർമിറ്റിന് അപേക്ഷിച്ച് അത് കൈവശം വയ്ക്കുന്നു — നിങ്ങൾ നേരിട്ട് അപേക്ഷിക്കുന്നില്ല, ഈ പെർമിറ്റ് ആ ഒരു തൊഴിലുടമയോടും ആ ഒരു ജോലിയോടും മാത്രമേ ബന്ധപ്പെട്ടിരിക്കുന്നുള്ളൂ.",
                  "തൊഴിലുടമകൾ ഓരോ വർക്ക് പെർമിറ്റ് ഉടമയ്ക്കും പ്രതിമാസ ലെവി അടയ്ക്കുകയും ഒരു ക്വാട്ടയ്ക്കുള്ളിൽ (“dependency ratio ceiling”) നിൽക്കുകയും വേണം — ഇത് നിയമന തീരുമാനങ്ങളെ ബാധിക്കുന്നു, പക്ഷേ ഇത് തൊഴിലുടമയുടെ ബാധ്യതയാണ്, നിങ്ങളുടേതല്ല.",
                  "പെർമിറ്റ് നൽകുന്നതിന് മുമ്പ്, നിങ്ങൾ ഒരു മെഡിക്കൽ പരിശോധനയ്ക്കും ബയോമെട്രിക് (വിരലടയാളം/ഐറിസ്) രജിസ്ട്രേഷനും വിധേയരാകും — രണ്ടും നിർബന്ധമാണ്, ഐച്ഛികമല്ല.",
                  "വർക്ക് പെർമിറ്റ് ഉടമകൾക്ക് സാധാരണയായി ഈ പാസിൽ ആശ്രിതരെ സിംഗപ്പൂരിലേക്ക് കൊണ്ടുവരാൻ കഴിയില്ല, കൂടാതെ പെർമിറ്റ് കൈവശം വച്ചിരിക്കുമ്പോൾ ഒരു സിംഗപ്പൂർ പൗരനെയോ സ്ഥിരതാമസക്കാരനെയോ വിവാഹം കഴിക്കുന്നതിന് മുമ്പ് MOM ന്റെ രേഖാമൂലമുള്ള അനുമതി ആവശ്യമാണ്."]},
    docs={"en": ["Keep your In-Principle Approval (IPA) letter and Work Permit card safe — you'll need them for almost every official interaction, from medical check-ups to opening a bank account.",
                 "Your permit is sector-specific — check with your employer or MOM before assuming you can switch industries.",
                 "MOM's website lists which sectors and source countries are currently eligible for Work Permit holders."],
          "hi": ["अपना In-Principle Approval (IPA) पत्र और Work Permit कार्ड सुरक्षित रखें — मेडिकल जाँच से लेकर बैंक खाता खोलने तक, लगभग हर आधिकारिक काम में इनकी ज़रूरत पड़ेगी।",
                 "आपका परमिट सेक्टर-विशिष्ट है — यह मान लेने से पहले कि आप उद्योग बदल सकते हैं, अपने नियोक्ता या MOM से जाँच करें।",
                 "MOM की वेबसाइट बताती है कि Work Permit धारकों के लिए वर्तमान में कौन-से सेक्टर और स्रोत देश पात्र हैं।"],
          "ta": ["உங்கள் In-Principle Approval (IPA) கடிதத்தையும் Work Permit அட்டையையும் பாதுகாப்பாக வைத்திருங்கள் — மருத்துவ பரிசோதனை முதல் வங்கி கணக்கு திறத்தல் வரை, கிட்டத்தட்ட ஒவ்வொரு அதிகாரப்பூர்வ செயலிலும் இவை தேவைப்படும்.",
                 "உங்கள் அனுமதி துறை-குறிப்பிட்டது — நீங்கள் தொழில்துறையை மாற்றலாம் என்று கருதுவதற்கு முன், உங்கள் முதலாளி அல்லது MOM இடம் சரிபார்க்கவும்.",
                 "Work Permit வைத்திருப்பவர்களுக்கு தற்போது தகுதியான துறைகள் மற்றும் மூல நாடுகள் எவை என்பதை MOM இன் இணையதளம் பட்டியலிடுகிறது."],
          "te": ["మీ In-Principle Approval (IPA) లేఖ మరియు Work Permit కార్డును సురక్షితంగా ఉంచుకోండి — వైద్య పరీక్షల నుండి బ్యాంక్ ఖాతా తెరవడం వరకు, దాదాపు ప్రతి అధికారిక పనిలో ఇవి అవసరం అవుతాయి.",
                 "మీ పర్మిట్ రంగం-నిర్దిష్టమైనది — మీరు పరిశ్రమలను మార్చుకోవచ్చని అనుకునే ముందు మీ యజమాని లేదా MOM తో తనిఖీ చేయండి.",
                 "Work Permit హోల్డర్లకు ప్రస్తుతం ఏ రంగాలు మరియు మూల దేశాలు అర్హత కలిగి ఉన్నాయో MOM వెబ్‌సైట్ జాబితా చేస్తుంది."],
          "ml": ["നിങ്ങളുടെ In-Principle Approval (IPA) കത്തും വർക്ക് പെർമിറ്റ് കാർഡും സുരക്ഷിതമായി സൂക്ഷിക്കുക — മെഡിക്കൽ പരിശോധനകൾ മുതൽ ബാങ്ക് അക്കൗണ്ട് തുറക്കൽ വരെ, മിക്കവാറും എല്ലാ ഔദ്യോഗിക കാര്യങ്ങൾക്കും ഇവ ആവശ്യമായി വരും.",
                 "നിങ്ങളുടെ പെർമിറ്റ് മേഖല-നിർദ്ദിഷ്ടമാണ് — നിങ്ങൾക്ക് വ്യവസായങ്ങൾ മാറാൻ കഴിയുമെന്ന് കരുതുന്നതിന് മുമ്പ് നിങ്ങളുടെ തൊഴിലുടമയോടോ MOM നോടോ പരിശോധിക്കുക.",
                 "വർക്ക് പെർമിറ്റ് ഉടമകൾക്ക് നിലവിൽ യോഗ്യതയുള്ള മേഖലകളും ഉറവിട രാജ്യങ്ങളും MOM ന്റെ വെബ്‌സൈറ്റ് പട്ടികപ്പെടുത്തുന്നു."]},
    note={"en": "If anything on your permit looks wrong — your name, employer, or sector — flag it with your employer or MOM immediately; small errors get much harder to fix later.",
          "hi": "अगर आपके परमिट पर कुछ भी ग़लत दिखे — आपका नाम, नियोक्ता, या सेक्टर — तुरंत अपने नियोक्ता या MOM को बताएँ; छोटी ग़लतियाँ बाद में ठीक करना कहीं ज़्यादा मुश्क़िल हो जाता है।",
          "ta": "உங்கள் அனுமதியில் ஏதேனும் தவறாகத் தெரிந்தால் — உங்கள் பெயர், முதலாளி, அல்லது துறை — உடனடியாக உங்கள் முதலாளி அல்லது MOM இடம் தெரிவிக்கவும்; சிறிய பிழைகள் பின்னர் சரிசெய்வது மிகவும் கடினமாகிவிடும்.",
          "te": "మీ పర్మిట్‌పై ఏదైనా తప్పుగా కనిపిస్తే — మీ పేరు, యజమాని, లేదా రంగం — వెంటనే మీ యజమాని లేదా MOMకి తెలియజేయండి; చిన్న తప్పులు తర్వాత సరిదిద్దడం చాలా కష్టమవుతుంది.",
          "ml": "നിങ്ങളുടെ പെർമിറ്റിൽ എന്തെങ്കിലും തെറ്റായി തോന്നിയാൽ — നിങ്ങളുടെ പേര്, തൊഴിലുടമ, അല്ലെങ്കിൽ മേഖല — ഉടൻ നിങ്ങളുടെ തൊഴിലുടമയെയോ MOM നെയോ അറിയിക്കുക; ചെറിയ പിശകുകൾ പിന്നീട് ശരിയാക്കാൻ വളരെ ബുദ്ധിമുട്ടാകും."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-worker/sector-specific-rules/work-permit-conditions", "label": {"en": "↗ MOM — Work Permit conditions", "hi": "↗ MOM — Work Permit शर्तें", "ta": "↗ MOM — Work Permit நிபந்தனைகள்", "te": "↗ MOM — Work Permit నిబంధనలు", "ml": "↗ MOM — വർക്ക് പെർമിറ്റ് വ്യവസ്ഥകൾ"}},
    ],
)

entry(
    category="sg_workpermit", country="singapore", badge_official=True,
    search_en="singapore work permit dormitory housing FEDA employer arranged accommodation",
    title={"en": "Where you'll live: employer-arranged housing", "hi": "आप कहाँ रहेंगे: नियोक्ता-व्यवस्थित आवास", "ta": "நீங்கள் எங்கு வசிப்பீர்கள்: முதலாளி-ஏற்பாடு செய்யும் வீட்டுவசதி",
           "te": "మీరు ఎక్కడ నివసిస్తారు: యజమాని-ఏర్పాటు చేసిన నివాసం", "ml": "നിങ്ങൾ എവിടെ താമസിക്കും: തൊഴിലുടമ ഏർപ്പാടാക്കുന്ന താമസസൗകര്യം"},
    desc={"en": "Housing for Work Permit holders isn't something you arrange yourself the way an Employment Pass holder might — your employer must show proof of acceptable accommodation before your permit is even issued.",
          "hi": "Work Permit धारकों के लिए आवास कोई ऐसी चीज़ नहीं है जिसे आप ख़ुद तय करते हैं, जैसे Employment Pass धारक कर सकता है — आपका परमिट जारी होने से पहले ही आपके नियोक्ता को स्वीकार्य आवास का प्रमाण देना होता है।",
          "ta": "Employment Pass வைத்திருப்பவர் செய்யக்கூடியது போல் Work Permit வைத்திருப்பவர்களுக்கான வீட்டுவசதி நீங்களே ஏற்பாடு செய்யக்கூடிய ஒன்று அல்ல — உங்கள் அனுமதி வழங்கப்படுவதற்கு முன்பே உங்கள் முதலாளி ஏற்றுக்கொள்ளத்தக்க வீட்டுவசதியை நிரூபிக்க வேண்டும்.",
          "te": "Employment Pass హోల్డర్ చేయగలిగినట్లుగా Work Permit హోల్డర్ల కోసం నివాసం మీరు స్వయంగా ఏర్పాటు చేసుకునేది కాదు — మీ పర్మిట్ జారీ కావడానికి ముందే మీ యజమాని ఆమోదయోగ్యమైన వసతికి రుజువు చూపించాలి.",
          "ml": "Employment Pass ഉടമയ്ക്ക് ചെയ്യാൻ കഴിയുന്നത് പോലെ Work Permit ഉടമകൾക്കുള്ള താമസസൗകര്യം നിങ്ങൾ സ്വയം ഏർപ്പാടാക്കുന്ന ഒന്നല്ല — നിങ്ങളുടെ പെർമിറ്റ് നൽകുന്നതിന് മുമ്പ് തന്നെ നിങ്ങളുടെ തൊഴിലുടമ സ്വീകാര്യമായ താമസത്തിന്റെ തെളിവ് കാണിക്കണം."},
    handles={"en": "dormitories · housing · accommodation", "hi": "डॉर्मिटरी · आवास · रहने की व्यवस्था", "ta": "டார்மிட்டரிகள் · வீட்டுவசதி · தங்குமிடம்",
             "te": "డార్మిటరీలు · నివాసం · వసతి", "ml": "ഡോർമിറ്ററികൾ · താമസസൗകര്യം · വാസസ്ഥലം"},
    steps={"en": ["Your employer must arrange and prove acceptable housing before MOM issues your Work Permit — this is a legal requirement on them, not a favour.",
                  "Large purpose-built dormitories (housing 1,000+ workers) must be licensed under the Foreign Employee Dormitories Act (FEDA), which sets minimum standards for space, sanitation, fire safety, and amenities.",
                  "MOM publishes a list of dormitories as a reference, but staying at a listed dormitory isn't compulsory — your employer can use other MOM-approved housing types too.",
                  "If your living conditions seem unsafe, overcrowded, or unsanitary, you can raise it with MOM directly — conditions well below the legal standard are something MOM investigates and acts on."],
           "hi": ["MOM आपका Work Permit जारी करने से पहले आपके नियोक्ता को स्वीकार्य आवास तय करना और साबित करना ज़रूरी है — यह उन पर एक क़ानूनी दायित्व है, कोई एहसान नहीं।",
                  "बड़े, ख़ास तौर पर बनाए गए डॉर्मिटरी (1,000+ श्रमिकों को रखने वाले) को Foreign Employee Dormitories Act (FEDA) के तहत लाइसेंस लेना होता है, जो जगह, स्वच्छता, अग्नि सुरक्षा, और सुविधाओं के न्यूनतम मानक तय करता है।",
                  "MOM संदर्भ के लिए डॉर्मिटरी की एक सूची प्रकाशित करता है, लेकिन सूचीबद्ध डॉर्मिटरी में रहना अनिवार्य नहीं है — आपका नियोक्ता अन्य MOM-अनुमोदित आवास प्रकारों का भी इस्तेमाल कर सकता है।",
                  "अगर आपकी रहने की स्थिति असुरक्षित, भीड़भाड़ वाली, या अस्वच्छ लगे, तो आप इसे सीधे MOM के सामने उठा सकते हैं — क़ानूनी मानक से काफ़ी कम स्थितियों की MOM जाँच करता है और कार्रवाई करता है।"],
           "ta": ["MOM உங்கள் Work Permit-ஐ வழங்குவதற்கு முன், உங்கள் முதலாளி ஏற்றுக்கொள்ளத்தக்க வீட்டுவசதியை ஏற்பாடு செய்து நிரூபிக்க வேண்டும் — இது அவர்கள் மீதான ஒரு சட்டப்பூர்வ கடமை, ஒரு உதவி அல்ல.",
                  "பெரிய, சிறப்பாக கட்டப்பட்ட டார்மிட்டரிகள் (1,000+ தொழிலாளர்களை வைத்திருப்பவை) Foreign Employee Dormitories Act (FEDA) இன் கீழ் உரிமம் பெற்றிருக்க வேண்டும், இது இடம், சுகாதாரம், தீ பாதுகாப்பு, மற்றும் வசதிகளுக்கான குறைந்தபட்ச தரங்களை நிர்ணயிக்கிறது.",
                  "MOM ஒரு குறிப்பாக டார்மிட்டரிகளின் பட்டியலை வெளியிடுகிறது, ஆனால் பட்டியலிடப்பட்ட டார்மிட்டரியில் தங்குவது கட்டாயமல்ல — உங்கள் முதலாளி பிற MOM-அங்கீகரிக்கப்பட்ட வீட்டுவசதி வகைகளையும் பயன்படுத்தலாம்.",
                  "உங்கள் வாழ்க்கை நிலைமைகள் பாதுகாப்பற்றதாக, நெரிசலானதாக, அல்லது சுகாதாரமற்றதாக தோன்றினால், நீங்கள் அதை நேரடியாக MOM இடம் தெரிவிக்கலாம் — சட்டத் தரத்திற்கு மிகவும் குறைவான நிலைமைகளை MOM விசாரித்து நடவடிக்கை எடுக்கிறது."],
           "te": ["MOM మీ Work Permit జారీ చేయడానికి ముందు మీ యజమాని ఆమోదయోగ్యమైన వసతిని ఏర్పాటు చేసి రుజువు చూపించాలి — ఇది వారిపై చట్టపరమైన బాధ్యత, ఒక సహాయం కాదు.",
                  "పెద్ద, ప్రత్యేకంగా నిర్మించిన డార్మిటరీలు (1,000+ మంది కార్మికులను కలిగి ఉన్నవి) Foreign Employee Dormitories Act (FEDA) కింద లైసెన్స్ కలిగి ఉండాలి, ఇది స్థలం, పరిశుభ్రత, అగ్ని భద్రత, మరియు సౌకర్యాలకు కనీస ప్రమాణాలను నిర్దేశిస్తుంది.",
                  "MOM సూచన కోసం డార్మిటరీల జాబితాను ప్రచురిస్తుంది, కానీ జాబితా చేయబడిన డార్మిటరీలో ఉండటం తప్పనిసరి కాదు — మీ యజమాని ఇతర MOM-ఆమోదించిన వసతి రకాలను కూడా ఉపయోగించవచ్చు.",
                  "మీ నివాస పరిస్థితులు అసురక్షితంగా, రద్దీగా, లేదా అపరిశుభ్రంగా అనిపిస్తే, మీరు దాన్ని నేరుగా MOMకి తెలియజేయవచ్చు — చట్టపరమైన ప్రమాణం కంటే చాలా తక్కువ పరిస్థితులను MOM పరిశోధించి చర్య తీసుకుంటుంది."],
           "ml": ["MOM നിങ്ങളുടെ Work Permit നൽകുന്നതിന് മുമ്പ് നിങ്ങളുടെ തൊഴിലുടമ സ്വീകാര്യമായ താമസസൗകര്യം ഒരുക്കി തെളിയിക്കണം — ഇത് അവരുടെ മേലുള്ള ഒരു നിയമപരമായ ബാധ്യതയാണ്, ഒരു ഔദാര്യമല്ല.",
                  "വലിയ, പ്രത്യേകം നിർമ്മിച്ച ഡോർമിറ്ററികൾ (1,000+ തൊഴിലാളികളെ ഉൾക്കൊള്ളുന്നവ) Foreign Employee Dormitories Act (FEDA) പ്രകാരം ലൈസൻസുള്ളതായിരിക്കണം, ഇത് സ്ഥലം, ശുചിത്വം, അഗ്നി സുരക്ഷ, സൗകര്യങ്ങൾ എന്നിവയ്ക്കുള്ള കുറഞ്ഞ മാനദണ്ഡങ്ങൾ നിശ്ചയിക്കുന്നു.",
                  "MOM റഫറൻസിനായി ഡോർമിറ്ററികളുടെ ഒരു പട്ടിക പ്രസിദ്ധീകരിക്കുന്നു, പക്ഷേ പട്ടികയിലുള്ള ഒരു ഡോർമിറ്ററിയിൽ താമസിക്കൽ നിർബന്ധമല്ല — നിങ്ങളുടെ തൊഴിലുടമയ്ക്ക് മറ്റ് MOM-അംഗീകൃത താമസ തരങ്ങളും ഉപയോഗിക്കാം.",
                  "നിങ്ങളുടെ താമസ സാഹചര്യങ്ങൾ അരക്ഷിതമോ തിരക്കേറിയതോ ശുചിത്വമില്ലാത്തതോ ആയി തോന്നിയാൽ, നിങ്ങൾക്ക് ഇത് നേരിട്ട് MOM നോട് ഉന്നയിക്കാം — നിയമപരമായ നിലവാരത്തേക്കാൾ വളരെ താഴെയുള്ള അവസ്ഥകൾ MOM അന്വേഷിച്ച് നടപടിയെടുക്കുന്നു."]},
    docs={"en": ["Know your dormitory or housing address and keep it written down somewhere safe — you'll need it for many official forms.",
                 "Large dormitories over a certain size must hold a valid FEDA licence — you can ask your employer or check with MOM if you're unsure.",
                 "Overcrowding, blocked fire exits, and unsanitary conditions are all things you can report, not things you have to accept."],
          "hi": ["अपने डॉर्मिटरी या आवास का पता जानें और उसे कहीं सुरक्षित लिख कर रखें — कई आधिकारिक फ़ॉर्मों में आपको इसकी ज़रूरत पड़ेगी।",
                 "एक निश्चित आकार से बड़े डॉर्मिटरी के पास वैध FEDA लाइसेंस होना ज़रूरी है — अगर आप निश्चित नहीं हैं, तो अपने नियोक्ता से पूछें या MOM से जाँच करें।",
                 "भीड़भाड़, अवरुद्ध अग्नि निकास, और अस्वच्छ स्थितियाँ — ये सब ऐसी चीज़ें हैं जिनकी आप शिक़ायत कर सकते हैं, जिन्हें स्वीकार करना ज़रूरी नहीं है।"],
          "ta": ["உங்கள் டார்மிட்டரி அல்லது வீட்டுவசதி முகவரியை தெரிந்துவைத்து, அதை பாதுகாப்பாக எங்காவது எழுதி வையுங்கள் — பல அதிகாரப்பூர்வ படிவங்களுக்கு இது தேவைப்படும்.",
                 "ஒரு குறிப்பிட்ட அளவுக்கு மேற்பட்ட பெரிய டார்மிட்டரிகள் செல்லுபடியாகும் FEDA உரிமத்தை வைத்திருக்க வேண்டும் — உங்களுக்கு உறுதியில்லை என்றால் உங்கள் முதலாளியிடம் கேளுங்கள் அல்லது MOM இடம் சரிபார்க்கவும்.",
                 "நெரிசல், தடுக்கப்பட்ட தீ வெளியேறும் வழிகள், மற்றும் சுகாதாரமற்ற நிலைமைகள் — இவை அனைத்தும் நீங்கள் புகார் அளிக்கக்கூடியவை, ஏற்றுக்கொள்ள வேண்டியவை அல்ல."],
          "te": ["మీ డార్మిటరీ లేదా నివాస చిరునామాను తెలుసుకుని, దాన్ని ఎక్కడైనా సురక్షితంగా రాసి ఉంచుకోండి — చాలా అధికారిక ఫారాలకు ఇది అవసరం అవుతుంది.",
                 "ఒక నిర్దిష్ట పరిమాణానికి మించిన పెద్ద డార్మిటరీలు చెల్లుబాటు అయ్యే FEDA లైసెన్స్ కలిగి ఉండాలి — మీకు ఖచ్చితంగా తెలియకపోతే మీ యజమానిని అడగండి లేదా MOMతో తనిఖీ చేయండి.",
                 "రద్దీ, అడ్డుకున్న అగ్నిమాపక నిష్క్రమణలు, మరియు అపరిశుభ్ర పరిస్థితులు — ఇవన్నీ మీరు నివేదించగలిగేవి, తప్పనిసరిగా అంగీకరించాల్సినవి కావు."],
          "ml": ["നിങ്ങളുടെ ഡോർമിറ്ററി അല്ലെങ്കിൽ താമസ വിലാസം അറിഞ്ഞിരിക്കുകയും അത് സുരക്ഷിതമായി എവിടെയെങ്കിലും എഴുതി സൂക്ഷിക്കുകയും ചെയ്യുക — പല ഔദ്യോഗിക ഫോമുകൾക്കും ഇത് ആവശ്യമായി വരും.",
                 "ഒരു നിശ്ചിത വലുപ്പത്തിൽ കൂടുതലുള്ള വലിയ ഡോർമിറ്ററികൾക്ക് സാധുവായ FEDA ലൈസൻസ് ഉണ്ടായിരിക്കണം — നിങ്ങൾക്ക് ഉറപ്പില്ലെങ്കിൽ നിങ്ങളുടെ തൊഴിലുടമയോട് ചോദിക്കുക അല്ലെങ്കിൽ MOM മായി പരിശോധിക്കുക.",
                 "തിരക്ക്, തടസ്സപ്പെട്ട അഗ്നി നിർഗമന വഴികൾ, ശുചിത്വമില്ലാത്ത അവസ്ഥകൾ — ഇവയെല്ലാം നിങ്ങൾക്ക് റിപ്പോർട്ട് ചെയ്യാവുന്നവയാണ്, നിർബന്ധമായി അംഗീകരിക്കേണ്ടവയല്ല."]},
    note={"en": "If you're ever unsure whether your housing meets the required standard, MOM's dormitory and housing pages are a good starting point, and TWC2/HOME (see the “help you can reach” card) can advise as well.",
          "hi": "अगर आपको कभी यह यक़ीन न हो कि आपका आवास ज़रूरी मानक पूरा करता है या नहीं, तो MOM के डॉर्मिटरी और आवास पेज एक अच्छी शुरुआत हैं, और TWC2/HOME (“आप जिस मदद तक पहुँच सकते हैं” कार्ड देखें) भी सलाह दे सकते हैं।",
          "ta": "உங்கள் வீட்டுவசதி தேவையான தரத்தை பூர்த்தி செய்கிறதா என்று உங்களுக்கு எப்போதாவது சந்தேகம் இருந்தால், MOM இன் டார்மிட்டரி மற்றும் வீட்டுவசதி பக்கங்கள் ஒரு நல்ல தொடக்கமாகும், மேலும் TWC2/HOME (“நீங்கள் அடையக்கூடிய உதவி” கார்டைப் பார்க்கவும்) ஆலோசனை வழங்கவும் முடியும்.",
          "te": "మీ నివాసం అవసరమైన ప్రమాణాన్ని అందుకుంటుందో లేదో మీకు ఎప్పుడైనా అనుమానం ఉంటే, MOM యొక్క డార్మిటరీ మరియు వసతి పేజీలు మంచి ప్రారంభం, మరియు TWC2/HOME (“మీరు చేరుకోగల సహాయం” కార్డును చూడండి) కూడా సలహా ఇవ్వగలవు.",
          "ml": "നിങ്ങളുടെ താമസം ആവശ്യമായ നിലവാരം പാലിക്കുന്നുണ്ടോ എന്ന് നിങ്ങൾക്ക് എപ്പോഴെങ്കിലും സംശയമുണ്ടെങ്കിൽ, MOM ന്റെ ഡോർമിറ്ററി, താമസ പേജുകൾ നല്ലൊരു തുടക്കമാണ്, കൂടാതെ TWC2/HOME (“നിങ്ങൾക്ക് എത്തിച്ചേരാവുന്ന സഹായം” കാർഡ് കാണുക) ഉപദേശം നൽകാനും കഴിയും."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://file.go.gov.sg/fedafaqs.pdf", "label": {"en": "↗ FEDA — dormitory licensing FAQ (PDF)", "hi": "↗ FEDA — डॉर्मिटरी लाइसेंसिंग FAQ (PDF)", "ta": "↗ FEDA — டார்மிட்டரி உரிமம் FAQ (PDF)", "te": "↗ FEDA — డార్మిటరీ లైసెన్సింగ్ FAQ (PDF)", "ml": "↗ FEDA — ഡോർമിറ്ററി ലൈസൻസിംഗ് FAQ (PDF)"}},
        {"href": "https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-worker/housing/requirements-for-dormitory-operators", "label": {"en": "↗ MOM — dormitory housing requirements", "hi": "↗ MOM — डॉर्मिटरी आवास आवश्यकताएँ", "ta": "↗ MOM — டார்மிட்டரி வீட்டுவசதி தேவைகள்", "te": "↗ MOM — డార్మిటరీ నివాస అవసరాలు", "ml": "↗ MOM — ഡോർമിറ്ററി താമസ ആവശ്യകതകൾ"}},
    ],
)

entry(
    category="sg_workpermit", country="singapore", badge_official=True,
    search_en="singapore work permit changing employer transfer consent IPA",
    title={"en": "Changing employers on a Work Permit", "hi": "Work Permit पर नियोक्ता बदलना", "ta": "Work Permit-இல் முதலாளியை மாற்றுதல்",
           "te": "Work Permit లో యజమానిని మార్చడం", "ml": "വർക്ക് പെർമിറ്റിൽ തൊഴിലുടമയെ മാറ്റുന്നത്"},
    desc={"en": "You can transfer to a new employer on a Work Permit, but the process is different from resigning and job-hunting the way you might elsewhere — doing it in the wrong order can leave you without a valid pass.",
          "hi": "Work Permit पर आप नए नियोक्ता के पास ट्रांसफ़र हो सकते हैं, लेकिन यह प्रक्रिया इस्तीफ़ा देकर ख़ुद नौकरी ढूँढने जैसी नहीं है — ग़लत क्रम में यह करने से आप बिना वैध पास के रह सकते हैं।",
          "ta": "Work Permit-இல் நீங்கள் ஒரு புதிய முதலாளிக்கு மாற்றப்படலாம், ஆனால் இந்த செயல்முறை நீங்கள் வேறு இடங்களில் ராஜினாமா செய்து வேலை தேடுவது போல் இல்லை — இதை தவறான வரிசையில் செய்வது உங்களை செல்லுபடியாகும் அனுமதி இல்லாமல் விட்டுவிடலாம்.",
          "te": "Work Permit లో మీరు కొత్త యజమానికి బదిలీ కావచ్చు, కానీ ఈ ప్రక్రియ మీరు వేరే చోట రాజీనామా చేసి ఉద్యోగం వెతుక్కునేలా ఉండదు — దీన్ని తప్పు క్రమంలో చేయడం మిమ్మల్ని చెల్లుబాటు అయ్యే పాస్ లేకుండా వదిలేయవచ్చు.",
          "ml": "വർക്ക് പെർമിറ്റിൽ നിങ്ങൾക്ക് ഒരു പുതിയ തൊഴിലുടമയിലേക്ക് മാറാൻ കഴിയും, പക്ഷേ ഈ പ്രക്രിയ നിങ്ങൾ മറ്റെവിടെയെങ്കിലും ചെയ്യുന്നത് പോലെ രാജിവച്ച് സ്വയം ജോലി തിരയുന്നത് പോലെയല്ല — ഇത് തെറ്റായ ക്രമത്തിൽ ചെയ്യുന്നത് നിങ്ങളെ സാധുവായ പാസ് ഇല്ലാതെ വിടാം."},
    handles={"en": "job transfer · new employer · consent", "hi": "जॉब ट्रांसफ़र · नया नियोक्ता · सहमति", "ta": "வேலை மாற்றம் · புதிய முதலாளி · ஒப்புதல்",
             "te": "ఉద్యోగ బదిలీ · కొత్త యజమాని · అనుమతి", "ml": "ജോലി മാറ്റം · പുതിയ തൊഴിലുടമ · സമ്മതം"},
    steps={"en": ["A new employer applies to MOM for you, not the other way around — you cannot simply hand in your notice and look for work on your own.",
                  "If your current employer consents to the transfer, MOM can approve it quickly — a formal consent/declaration form is signed by your current employer.",
                  "If your current employer does not consent, a transfer is still sometimes possible, but only after a longer pre-approval window and MOM's own assessment — this is not guaranteed and can take significantly more time.",
                  "Do not resign or leave your current job before your new employer has an In-Principle Approval (IPA) for you — resigning first can leave you with no valid pass and no legal way to keep working while the transfer is sorted out."],
           "hi": ["नया नियोक्ता आपके लिए MOM से आवेदन करता है, न कि इसका उल्टा — आप बस इस्तीफ़ा देकर अपने आप नौकरी नहीं ढूँढ सकते।",
                  "अगर आपका मौजूदा नियोक्ता ट्रांसफ़र के लिए सहमत होता है, तो MOM इसे जल्दी मंज़ूर कर सकता है — आपके मौजूदा नियोक्ता द्वारा एक औपचारिक सहमति/घोषणा फ़ॉर्म पर हस्ताक्षर किए जाते हैं।",
                  "अगर आपका मौजूदा नियोक्ता सहमत नहीं होता, तो भी कभी-कभी ट्रांसफ़र संभव है, लेकिन केवल एक लंबी पूर्व-अनुमोदन अवधि और MOM की अपनी समीक्षा के बाद — यह गारंटीशुदा नहीं है और इसमें काफ़ी ज़्यादा समय लग सकता है।",
                  "अपने नए नियोक्ता के पास आपके लिए In-Principle Approval (IPA) होने से पहले अपनी मौजूदा नौकरी से इस्तीफ़ा न दें या न छोड़ें — पहले इस्तीफ़ा देने से आप बिना वैध पास के और ट्रांसफ़र सुलझने तक काम करने के किसी क़ानूनी तरीक़े के बिना रह सकते हैं।"],
           "ta": ["ஒரு புதிய முதலாளி உங்களுக்காக MOM இடம் விண்ணப்பிக்கிறார், நீங்கள் அல்ல — நீங்கள் வெறுமனே ராஜினாமா கடிதத்தை கொடுத்துவிட்டு தானாகவே வேலை தேட முடியாது.",
                  "உங்கள் தற்போதைய முதலாளி மாற்றத்திற்கு ஒப்புக்கொண்டால், MOM இதை விரைவாக அங்கீகரிக்க முடியும் — உங்கள் தற்போதைய முதலாளியால் ஒரு முறையான ஒப்புதல்/அறிவிப்பு படிவம் கையொப்பமிடப்படுகிறது.",
                  "உங்கள் தற்போதைய முதலாளி ஒப்புக்கொள்ளவில்லை என்றால், சில நேரங்களில் இன்னும் மாற்றம் சாத்தியமாகும், ஆனால் நீண்ட முன்-அங்கீகார காலத்திற்குப் பிறகும் MOM இன் சொந்த மதிப்பீட்டிற்குப் பிறகும் மட்டுமே — இது உத்தரவாதம் இல்லை, மேலும் இதற்கு கணிசமான கூடுதல் நேரம் ஆகலாம்.",
                  "உங்கள் புதிய முதலாளிக்கு உங்களுக்காக In-Principle Approval (IPA) கிடைப்பதற்கு முன் உங்கள் தற்போதைய வேலையை ராஜினாமா செய்யவோ விட்டுவிடவோ வேண்டாம் — முதலில் ராஜினாமா செய்வது உங்களை செல்லுபடியாகும் அனுமதி இல்லாமலும், மாற்றம் தீர்க்கப்படும் வரை வேலை செய்வதற்கான சட்டப்பூர்வ வழி இல்லாமலும் விட்டுவிடலாம்."],
           "te": ["కొత్త యజమాని మీ కోసం MOM కి దరఖాస్తు చేస్తారు, మీరు కాదు — మీరు కేవలం రాజీనామా ఇచ్చి మీ స్వంతంగా ఉద్యోగం వెతుక్కోలేరు.",
                  "మీ ప్రస్తుత యజమాని బదిలీకి అంగీకరిస్తే, MOM దీన్ని త్వరగా ఆమోదించగలదు — మీ ప్రస్తుత యజమాని ద్వారా ఒక అధికారిక అనుమతి/డిక్లరేషన్ ఫారంపై సంతకం చేయబడుతుంది.",
                  "మీ ప్రస్తుత యజమాని అంగీకరించకపోతే, కొన్నిసార్లు బదిలీ ఇప్పటికీ సాధ్యమే, కానీ దీర్ఘకాలిక ముందస్తు-ఆమోద వ్యవధి మరియు MOM స్వంత మదింపు తర్వాత మాత్రమే — ఇది హామీ కాదు మరియు గణనీయంగా ఎక్కువ సమయం పట్టవచ్చు.",
                  "మీ కొత్త యజమానికి మీ కోసం In-Principle Approval (IPA) రాకముందే మీ ప్రస్తుత ఉద్యోగానికి రాజీనామా చేయవద్దు లేదా వదిలిపెట్టవద్దు — ముందుగా రాజీనామా చేయడం వల్ల మీరు చెల్లుబాటు అయ్యే పాస్ లేకుండా మరియు బదిలీ పరిష్కారమయ్యే వరకు పనిచేయడానికి ఎటువంటి చట్టపరమైన మార్గం లేకుండా మిగిలిపోవచ్చు."],
           "ml": ["ഒരു പുതിയ തൊഴിലുടമ നിങ്ങൾക്കുവേണ്ടി MOM ന് അപേക്ഷിക്കുന്നു, മറിച്ചല്ല — നിങ്ങൾക്ക് വെറുതെ രാജി കൊടുത്ത് സ്വന്തമായി ജോലി തിരയാൻ കഴിയില്ല.",
                  "നിങ്ങളുടെ നിലവിലെ തൊഴിലുടമ മാറ്റത്തിന് സമ്മതിച്ചാൽ, MOM ന് ഇത് വേഗത്തിൽ അംഗീകരിക്കാൻ കഴിയും — നിങ്ങളുടെ നിലവിലെ തൊഴിലുടമ ഒരു ഔപചാരിക സമ്മത/പ്രഖ്യാപന ഫോറത്തിൽ ഒപ്പിടുന്നു.",
                  "നിങ്ങളുടെ നിലവിലെ തൊഴിലുടമ സമ്മതിക്കുന്നില്ലെങ്കിൽ, ചിലപ്പോൾ ഇപ്പോഴും ഒരു മാറ്റം സാധ്യമാണ്, പക്ഷേ ദൈർഘ്യമേറിയ മുൻകൂർ അംഗീകാര കാലയളവിനും MOM ന്റെ സ്വന്തം വിലയിരുത്തലിനും ശേഷം മാത്രം — ഇത് ഉറപ്പില്ല, കൂടാതെ ഗണ്യമായി കൂടുതൽ സമയമെടുക്കാം.",
                  "നിങ്ങളുടെ പുതിയ തൊഴിലുടമയ്ക്ക് നിങ്ങൾക്കായി In-Principle Approval (IPA) ലഭിക്കുന്നതിന് മുമ്പ് നിങ്ങളുടെ നിലവിലെ ജോലി രാജിവയ്ക്കുകയോ ഉപേക്ഷിക്കുകയോ ചെയ്യരുത് — ആദ്യം രാജിവയ്ക്കുന്നത് നിങ്ങളെ സാധുവായ പാസ് ഇല്ലാതെയും മാറ്റം പരിഹരിക്കപ്പെടുന്നതുവരെ ജോലി ചെയ്യാൻ നിയമപരമായ മാർഗമില്ലാതെയും വിടാം."]},
    docs={"en": ["Ask your new employer for written confirmation of IPA status before making any decision about your current job.",
                 "If your current employer is unwilling to consent and you believe it's unreasonable (for example, to pressure you to stay), TADM and the organisations on the “help you can reach” card can advise on your options.",
                 "Keep copies of any consent forms, IPA letters, and correspondence about your transfer."],
          "hi": ["अपनी मौजूदा नौकरी के बारे में कोई भी फ़ैसला लेने से पहले अपने नए नियोक्ता से IPA स्थिति की लिखित पुष्टि माँगें।",
                 "अगर आपका मौजूदा नियोक्ता सहमत होने को तैयार नहीं है और आपको लगता है कि यह अनुचित है (जैसे, आपको रुकने के लिए दबाव डालने के लिए), तो TADM और “आप जिस मदद तक पहुँच सकते हैं” कार्ड की संस्थाएँ आपके विकल्पों पर सलाह दे सकती हैं।",
                 "अपने ट्रांसफ़र से जुड़े किसी भी सहमति फ़ॉर्म, IPA पत्र, और पत्राचार की प्रतियाँ रखें।"],
          "ta": ["உங்கள் தற்போதைய வேலை பற்றி எந்த முடிவும் எடுப்பதற்கு முன், உங்கள் புதிய முதலாளியிடம் IPA நிலையை எழுத்துப்பூர்வமாக உறுதிப்படுத்தச் சொல்லுங்கள்.",
                 "உங்கள் தற்போதைய முதலாளி ஒப்புக்கொள்ள தயாராக இல்லை என்றால் மற்றும் இது நியாயமற்றது என்று நீங்கள் நினைத்தால் (உதாரணமாக, உங்களை தங்க வைக்க அழுத்தம் கொடுக்க), TADM மற்றும் “நீங்கள் அடையக்கூடிய உதவி” கார்டிலுள்ள அமைப்புகள் உங்கள் விருப்பங்களைப் பற்றி ஆலோசனை வழங்க முடியும்.",
                 "உங்கள் மாற்றம் தொடர்பான எந்த ஒப்புதல் படிவங்கள், IPA கடிதங்கள், மற்றும் கடிதப் பரிமாற்றங்களின் நகல்களை வைத்திருங்கள்."],
          "te": ["మీ ప్రస్తుత ఉద్యోగం గురించి ఏదైనా నిర్ణయం తీసుకునే ముందు మీ కొత్త యజమాని నుండి IPA స్థితి యొక్క వ్రాతపూర్వక నిర్ధారణ కోరండి.",
                 "మీ ప్రస్తుత యజమాని అంగీకరించడానికి ఇష్టపడకపోతే మరియు ఇది అసమంజసమని మీరు భావిస్తే (ఉదాహరణకు, మిమ్మల్ని ఉండమని ఒత్తిడి చేయడానికి), TADM మరియు “మీరు చేరుకోగల సహాయం” కార్డులోని సంస్థలు మీ ఎంపికలపై సలహా ఇవ్వగలవు.",
                 "మీ బదిలీకి సంబంధించిన ఏవైనా అనుమతి ఫారాలు, IPA లేఖలు, మరియు ఉత్తర ప్రత్యుత్తరాల కాపీలను ఉంచుకోండి."],
          "ml": ["നിങ്ങളുടെ നിലവിലെ ജോലിയെക്കുറിച്ച് എന്തെങ്കിലും തീരുമാനമെടുക്കുന്നതിന് മുമ്പ് നിങ്ങളുടെ പുതിയ തൊഴിലുടമയോട് IPA നിലയുടെ രേഖാമൂലമുള്ള സ്ഥിരീകരണം ചോദിക്കുക.",
                 "നിങ്ങളുടെ നിലവിലെ തൊഴിലുടമ സമ്മതിക്കാൻ തയ്യാറല്ലെങ്കിൽ, ഇത് ന്യായരഹിതമാണെന്ന് നിങ്ങൾ കരുതുന്നുവെങ്കിൽ (ഉദാഹരണത്തിന്, നിങ്ങളെ തുടരാൻ സമ്മർദ്ദം ചെലുത്താൻ), TADM ഉം “നിങ്ങൾക്ക് എത്തിച്ചേരാവുന്ന സഹായം” കാർഡിലെ സംഘടനകളും നിങ്ങളുടെ ഓപ്ഷനുകളെക്കുറിച്ച് ഉപദേശിക്കാൻ കഴിയും.",
                 "നിങ്ങളുടെ മാറ്റവുമായി ബന്ധപ്പെട്ട ഏതെങ്കിലും സമ്മത ഫോറങ്ങൾ, IPA കത്തുകൾ, കത്തിടപാടുകൾ എന്നിവയുടെ പകർപ്പുകൾ സൂക്ഷിക്കുക."]},
    note={"en": "The single most common way transfers go wrong is doing things in the wrong order — always secure the new pass before giving up the old one.",
          "hi": "ट्रांसफ़र के गड़बड़ होने का सबसे आम तरीक़ा है ग़लत क्रम में काम करना — हमेशा पुराने पास को छोड़ने से पहले नए पास को सुरक्षित करें।",
          "ta": "மாற்றங்கள் தவறாகச் செல்வதற்கு மிகவும் பொதுவான வழி தவறான வரிசையில் விஷயங்களைச் செய்வதுதான் — பழைய அனுமதியை விடுவதற்கு முன் எப்போதும் புதிய அனுமதியைப் பாதுகாக்கவும்.",
          "te": "బదిలీలు తప్పుగా జరగడానికి అత్యంత సాధారణ మార్గం తప్పు క్రమంలో పనులు చేయడమే — పాత పాస్‌ను వదులుకునే ముందు ఎల్లప్పుడూ కొత్త పాస్‌ను భద్రపరచుకోండి.",
          "ml": "മാറ്റങ്ങൾ തെറ്റാകാനുള്ള ഏറ്റവും സാധാരണമായ വഴി തെറ്റായ ക്രമത്തിൽ കാര്യങ്ങൾ ചെയ്യുന്നതാണ് — പഴയ പാസ് ഉപേക്ഷിക്കുന്നതിന് മുമ്പ് എപ്പോഴും പുതിയ പാസ് ഉറപ്പാക്കുക."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-worker", "label": {"en": "↗ MOM — Work Permit for Foreign Worker", "hi": "↗ MOM — Work Permit for Foreign Worker", "ta": "↗ MOM — Work Permit for Foreign Worker", "te": "↗ MOM — Work Permit for Foreign Worker", "ml": "↗ MOM — Work Permit for Foreign Worker"}},
    ],
)

entry(
    category="sg_workpermit", country="singapore", badge_official=True,
    search_en="singapore work permit salary payslip itemised deduction rights",
    title={"en": "Salary, payslips & your rights", "hi": "वेतन, पेस्लिप, और आपके अधिकार", "ta": "சம்பளம், ஊதியச் சீட்டுகள், மற்றும் உங்கள் உரிமைகள்",
           "te": "జీతం, పేస్లిప్‌లు, మరియు మీ హక్కులు", "ml": "ശമ്പളം, പേസ്ലിപ്പുകൾ, നിങ്ങളുടെ അവകാശങ്ങൾ"},
    desc={"en": "Singapore law requires your employer to pay you on time and give you an itemised payslip for every payment — knowing what's required helps you spot a problem early, before unpaid wages pile up.",
          "hi": "सिंगापुर का क़ानून आपके नियोक्ता को समय पर भुगतान करने और हर भुगतान के लिए एक विस्तृत पेस्लिप देने की आवश्यकता रखता है — यह जानना कि क्या ज़रूरी है, आपको समस्या को जल्दी पहचानने में मदद करता है, इससे पहले कि बक़ाया वेतन जमा हो जाए।",
          "ta": "சிங்கப்பூர் சட்டம் உங்கள் முதலாளி உங்களுக்கு சரியான நேரத்தில் ஊதியம் வழங்கவும், ஒவ்வொரு கட்டணத்திற்கும் ஒரு விவரமான ஊதியச் சீட்டு வழங்கவும் தேவைப்படுத்துகிறது — என்ன தேவை என்பதை அறிவது, செலுத்தப்படாத ஊதியம் குவியும் முன்பே ஒரு பிரச்சினையை முன்கூட்டியே கண்டறிய உதவும்.",
          "te": "సింగపూర్ చట్టం మీ యజమాని మీకు సకాలంలో చెల్లించాలని మరియు ప్రతి చెల్లింపుకు ఒక వివరణాత్మక పేస్లిప్ ఇవ్వాలని కోరుతుంది — ఏమి అవసరమో తెలుసుకోవడం, చెల్లించని వేతనాలు పేరుకుపోకముందే సమస్యను ముందుగానే గుర్తించడంలో సహాయపడుతుంది.",
          "ml": "നിങ്ങളുടെ തൊഴിലുടമ സമയത്ത് ശമ്പളം നൽകാനും ഓരോ പേയ്‌മെന്റിനും ഒരു വിശദമായ പേസ്ലിപ്പ് നൽകാനും സിംഗപ്പൂർ നിയമം ആവശ്യപ്പെടുന്നു — എന്താണ് ആവശ്യമെന്ന് അറിയുന്നത്, കുടിശ്ശികയായ ശമ്പളം കുന്നുകൂടുന്നതിനുമുമ്പ് ഒരു പ്രശ്നം നേരത്തെ കണ്ടെത്താൻ നിങ്ങളെ സഹായിക്കുന്നു."},
    handles={"en": "salary · payslips · deductions", "hi": "वेतन · पेस्लिप · कटौती", "ta": "சம்பளம் · ஊதியச் சீட்டுகள் · கழிவுகள்",
             "te": "జీతం · పేస్లిప్‌లు · తగ్గింపులు", "ml": "ശമ്പളം · പേസ്ലിപ്പുകൾ · കിഴിവുകൾ"},
    steps={"en": ["Your employer must give you an itemised payslip, in either digital or paper form, every time you're paid — it must show a breakdown, not just a final total.",
                  "Salary for a completed pay period must be paid within 7 days after the end of that period; overtime pay has its own deadline, generally within 14 days.",
                  "Only certain deductions are legally allowed — for example, CPF (where applicable), income tax, and agreed items like accommodation or amenities within limits. Your employer cannot simply deduct whatever they choose.",
                  "Keep your own copies of every payslip, whether or not your employer keeps records — this is your best evidence if a dispute ever comes up."],
           "hi": ["आपका नियोक्ता आपको हर बार भुगतान करते समय, डिजिटल या काग़ज़ी रूप में, एक विस्तृत पेस्लिप देना ज़रूरी है — इसमें केवल अंतिम राशि नहीं, बल्कि पूरा विवरण दिखना चाहिए।",
                  "पूरी हुई वेतन अवधि का वेतन उस अवधि के ख़त्म होने के 7 दिनों के भीतर दिया जाना चाहिए; ओवरटाइम भुगतान की अपनी अलग समय-सीमा है, आम तौर पर 14 दिनों के भीतर।",
                  "क़ानूनी रूप से केवल कुछ ही कटौतियों की अनुमति है — जैसे CPF (जहाँ लागू हो), आयकर, और सीमाओं के भीतर आवास या सुविधाओं जैसी सहमत वस्तुएँ। आपका नियोक्ता मनमानी कटौती नहीं कर सकता।",
                  "हर पेस्लिप की अपनी प्रति रखें, चाहे आपका नियोक्ता रिकॉर्ड रखे या न रखे — अगर कभी कोई विवाद हो तो यह आपका सबसे अच्छा सबूत है।"],
           "ta": ["உங்கள் முதலாளி உங்களுக்கு ஊதியம் வழங்கும் ஒவ்வொரு முறையும், டிஜிட்டல் அல்லது காகித வடிவத்தில், ஒரு விவரமான ஊதியச் சீட்டு வழங்க வேண்டும் — இது இறுதி மொத்தத் தொகையை மட்டும் அல்ல, ஒரு முழு விவரப் பட்டியலைக் காட்ட வேண்டும்.",
                  "முடிந்த ஊதிய காலத்திற்கான சம்பளம் அந்த காலம் முடிவடைந்த 7 நாட்களுக்குள் செலுத்தப்பட வேண்டும்; கூடுதல் நேர ஊதியத்திற்கு அதன் சொந்த காலக்கெடு உள்ளது, பொதுவாக 14 நாட்களுக்குள்.",
                  "சட்டப்படி சில கழிவுகள் மட்டுமே அனுமதிக்கப்படுகின்றன — உதாரணமாக CPF (பொருந்தும் இடத்தில்), வருமான வரி, மற்றும் வரம்புகளுக்குள் தங்குமிடம் அல்லது வசதிகள் போன்ற ஒப்புக்கொள்ளப்பட்ட பொருட்கள். உங்கள் முதலாளி தானாக விரும்பியதை கழிக்க முடியாது.",
                  "உங்கள் முதலாளி பதிவுகளை வைத்திருந்தாலும் இல்லாவிட்டாலும், ஒவ்வொரு ஊதியச் சீட்டின் சொந்த நகல்களையும் வைத்திருங்கள் — எப்போதாவது ஒரு தகராறு ஏற்பட்டால் இது உங்கள் சிறந்த ஆதாரம்."],
           "te": ["మీ యజమాని మీకు చెల్లించిన ప్రతిసారీ, డిజిటల్ లేదా కాగితం రూపంలో, ఒక వివరణాత్మక పేస్లిప్ ఇవ్వాలి — ఇది కేవలం చివరి మొత్తాన్ని కాకుండా, పూర్తి విభజనను చూపించాలి.",
                  "పూర్తయిన వేతన కాలానికి జీతం ఆ కాలం ముగిసిన 7 రోజుల్లోపు చెల్లించాలి; ఓవర్‌టైమ్ చెల్లింపుకు దాని స్వంత గడువు ఉంటుంది, సాధారణంగా 14 రోజుల్లోపు.",
                  "చట్టపరంగా కొన్ని తగ్గింపులు మాత్రమే అనుమతించబడతాయి — ఉదాహరణకు CPF (వర్తించే చోట), ఆదాయపు పన్ను, మరియు పరిమితుల్లో వసతి లేదా సౌకర్యాలు వంటి అంగీకరించిన అంశాలు. మీ యజమాని తనకు నచ్చినది ఏదైనా తగ్గించలేరు.",
                  "మీ యజమాని రికార్డులు ఉంచినా ఉంచకపోయినా, ప్రతి పేస్లిప్ యొక్క మీ స్వంత కాపీలను ఉంచుకోండి — ఎప్పుడైనా వివాదం వస్తే ఇది మీ ఉత్తమ సాక్ష్యం."],
           "ml": ["നിങ്ങളുടെ തൊഴിലുടമ നിങ്ങൾക്ക് ശമ്പളം നൽകുന്ന ഓരോ തവണയും, ഡിജിറ്റൽ അല്ലെങ്കിൽ പേപ്പർ രൂപത്തിൽ, ഒരു വിശദമായ പേസ്ലിപ്പ് നൽകണം — ഇത് അന്തിമ തുക മാത്രമല്ല, ഒരു പൂർണ്ണ വിഭജനം കാണിക്കണം.",
                  "പൂർത്തിയായ ശമ്പള കാലയളവിനുള്ള ശമ്പളം ആ കാലയളവ് അവസാനിച്ച് 7 ദിവസത്തിനുള്ളിൽ നൽകണം; ഓവർടൈം പേയ്‌മെന്റിന് അതിന്റേതായ സമയപരിധിയുണ്ട്, സാധാരണയായി 14 ദിവസത്തിനുള്ളിൽ.",
                  "നിയമപരമായി ചില കിഴിവുകൾ മാത്രമേ അനുവദനീയമായുള്ളൂ — ഉദാഹരണത്തിന് CPF (ബാധകമായിടത്ത്), ആദായനികുതി, പരിധിക്കുള്ളിൽ താമസസൗകര്യം അല്ലെങ്കിൽ സൗകര്യങ്ങൾ പോലുള്ള അംഗീകരിച്ച ഇനങ്ങൾ. നിങ്ങളുടെ തൊഴിലുടമയ്ക്ക് ഇഷ്ടമുള്ളത് വെറുതെ കിഴിക്കാൻ കഴിയില്ല.",
                  "നിങ്ങളുടെ തൊഴിലുടമ രേഖകൾ സൂക്ഷിച്ചാലും ഇല്ലെങ്കിലും, ഓരോ പേസ്ലിപ്പിന്റെയും സ്വന്തം പകർപ്പുകൾ സൂക്ഷിക്കുക — എപ്പോഴെങ്കിലും ഒരു തർക്കം ഉണ്ടായാൽ ഇതാണ് നിങ്ങളുടെ ഏറ്റവും നല്ല തെളിവ്."]},
    docs={"en": ["Compare your payslip against your actual hours and agreed salary regularly — small, repeated shortfalls are easier to fix early.",
                 "If deductions appear that you didn't agree to, ask your employer for a written explanation before assuming it's a mistake.",
                 "Unpaid or late salary is one of the most common reasons workers approach TADM — see the “help you can reach” card if this happens to you."],
          "hi": ["अपनी पेस्लिप की नियमित रूप से अपने वास्तविक घंटों और सहमत वेतन से तुलना करें — छोटी, बार-बार होने वाली कमियों को जल्दी ठीक करना आसान होता है।",
                 "अगर ऐसी कटौतियाँ दिखें जिनसे आप सहमत नहीं थे, तो इसे ग़लती मान लेने से पहले अपने नियोक्ता से लिखित स्पष्टीकरण माँगें।",
                 "बक़ाया या देर से वेतन मिलना उन सबसे आम कारणों में से एक है जिनके लिए श्रमिक TADM के पास जाते हैं — अगर आपके साथ ऐसा हो तो “आप जिस मदद तक पहुँच सकते हैं” कार्ड देखें।"],
          "ta": ["உங்கள் ஊதியச் சீட்டை உங்கள் உண்மையான வேலை நேரங்கள் மற்றும் ஒப்புக்கொள்ளப்பட்ட சம்பளத்துடன் தொடர்ந்து ஒப்பிடுங்கள் — சிறிய, மீண்டும் மீண்டும் நிகழும் குறைபாடுகளை முன்கூட்டியே சரிசெய்வது எளிது.",
                 "நீங்கள் ஒப்புக்கொள்ளாத கழிவுகள் தோன்றினால், அது ஒரு தவறு என்று கருதுவதற்கு முன் உங்கள் முதலாளியிடம் எழுத்துப்பூர்வ விளக்கம் கேளுங்கள்.",
                 "செலுத்தப்படாத அல்லது தாமதமான சம்பளம் தொழிலாளர்கள் TADM-ஐ அணுகுவதற்கான மிகவும் பொதுவான காரணங்களில் ஒன்று — இது உங்களுக்கு நடந்தால் “நீங்கள் அடையக்கூடிய உதவி” கார்டைப் பார்க்கவும்."],
          "te": ["మీ పేస్లిప్‌ను మీ వాస్తవ పని గంటలు మరియు అంగీకరించిన జీతంతో క్రమం తప్పకుండా పోల్చండి — చిన్న, పునరావృత లోటులను ముందుగానే సరిదిద్దడం సులభం.",
                 "మీరు అంగీకరించని తగ్గింపులు కనిపిస్తే, అది పొరపాటు అని అనుకునే ముందు మీ యజమాని నుండి వ్రాతపూర్వక వివరణ కోరండి.",
                 "చెల్లించని లేదా ఆలస్యమైన జీతం కార్మికులు TADMని సంప్రదించడానికి అత్యంత సాధారణ కారణాలలో ఒకటి — ఇది మీకు జరిగితే “మీరు చేరుకోగల సహాయం” కార్డును చూడండి."],
          "ml": ["നിങ്ങളുടെ പേസ്ലിപ്പ് നിങ്ങളുടെ യഥാർത്ഥ ജോലി സമയങ്ങളും അംഗീകരിച്ച ശമ്പളവുമായി പതിവായി താരതമ്യം ചെയ്യുക — ചെറിയ, ആവർത്തിച്ചുള്ള കുറവുകൾ നേരത്തെ പരിഹരിക്കാൻ എളുപ്പമാണ്.",
                 "നിങ്ങൾ അംഗീകരിക്കാത്ത കിഴിവുകൾ പ്രത്യക്ഷപ്പെട്ടാൽ, അത് ഒരു തെറ്റാണെന്ന് കരുതുന്നതിന് മുമ്പ് നിങ്ങളുടെ തൊഴിലുടമയോട് രേഖാമൂലമുള്ള വിശദീകരണം ചോദിക്കുക.",
                 "അടയ്ക്കാത്തതോ വൈകിയതോ ആയ ശമ്പളം തൊഴിലാളികൾ TADM നെ സമീപിക്കുന്നതിനുള്ള ഏറ്റവും സാധാരണമായ കാരണങ്ങളിലൊന്നാണ് — ഇത് നിങ്ങൾക്ക് സംഭവിച്ചാൽ “നിങ്ങൾക്ക് എത്തിച്ചേരാവുന്ന സഹായം” കാർഡ് കാണുക."]},
    note={"en": "If your employer isn't issuing payslips at all, that is itself a breach you can raise — don't wait until salary actually stops to ask questions.",
          "hi": "अगर आपका नियोक्ता पेस्लिप बिल्कुल जारी ही नहीं कर रहा है, तो यह ख़ुद एक उल्लंघन है जिसे आप उठा सकते हैं — वेतन रुकने का इंतज़ार करने के बजाय सवाल पूछें।",
          "ta": "உங்கள் முதலாளி ஊதியச் சீட்டுகளை வழங்கவே இல்லை என்றால், அதுவே நீங்கள் எழுப்பக்கூடிய ஒரு மீறல் — சம்பளம் நிற்கும் வரை காத்திருக்காமல் கேள்விகள் கேளுங்கள்.",
          "te": "మీ యజమాని పేస్లిప్‌లను అస్సలు జారీ చేయకపోతే, అది స్వయంగా మీరు లేవనెత్తగల ఉల్లంఘన — జీతం నిజంగా ఆగిపోయే వరకు వేచి ఉండకుండా ప్రశ్నలు అడగండి.",
          "ml": "നിങ്ങളുടെ തൊഴിലുടമ പേസ്ലിപ്പുകൾ ഒട്ടും നൽകുന്നില്ലെങ്കിൽ, അത് തന്നെ നിങ്ങൾക്ക് ഉന്നയിക്കാവുന്ന ഒരു ലംഘനമാണ് — ശമ്പളം യഥാർത്ഥത്തിൽ നിലയ്ക്കുന്നതുവരെ കാത്തിരിക്കാതെ ചോദ്യങ്ങൾ ചോദിക്കുക."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.mom.gov.sg/employment-practices/salary", "label": {"en": "↗ MOM — salary and payslip rules", "hi": "↗ MOM — वेतन और पेस्लिप नियम", "ta": "↗ MOM — சம்பளம் மற்றும் ஊதியச் சீட்டு விதிகள்", "te": "↗ MOM — జీతం మరియు పేస్లిప్ నియమాలు", "ml": "↗ MOM — ശമ്പളവും പേസ്ലിപ്പ് നിയമങ്ങളും"}},
    ],
)

entry(
    category="sg_workpermit", country="singapore", badge_official=True,
    search_en="singapore work permit help TADM migrant workers centre HOME salary dispute helpline",
    title={"en": "If something goes wrong: help you can actually reach", "hi": "अगर कुछ ग़लत हो जाए: वह मदद जो आप वाक़ई पा सकते हैं", "ta": "ஏதேனும் தவறாக நடந்தால்: நீங்கள் உண்மையில் அடையக்கூடிய உதவி",
           "te": "ఏదైనా తప్పు జరిగితే: మీరు నిజంగా చేరుకోగల సహాయం", "ml": "എന്തെങ്കിലും തെറ്റായാൽ: നിങ്ങൾക്ക് ശരിക്കും എത്തിച്ചേരാവുന്ന സഹായം"},
    desc={"en": "If you're not being paid correctly, your housing is unsafe, or your employer is pressuring you unfairly, there are real organisations set up to help — most of them free, and not dependent on your employer's cooperation.",
          "hi": "अगर आपको सही वेतन नहीं मिल रहा, आपका आवास असुरक्षित है, या आपका नियोक्ता आप पर अनुचित दबाव डाल रहा है, तो मदद के लिए वास्तविक संस्थाएँ मौजूद हैं — इनमें से ज़्यादातर मुफ़्त हैं, और आपके नियोक्ता के सहयोग पर निर्भर नहीं हैं।",
          "ta": "உங்களுக்கு சரியாக ஊதியம் வழங்கப்படவில்லை என்றால், உங்கள் வீட்டுவசதி பாதுகாப்பற்றது என்றால், அல்லது உங்கள் முதலாளி உங்களை நியாயமற்ற முறையில் அழுத்துகிறார் என்றால், உதவுவதற்கு உண்மையான அமைப்புகள் உள்ளன — இவற்றில் பெரும்பாலானவை இலவசம், மேலும் உங்கள் முதலாளியின் ஒத்துழைப்பைச் சார்ந்தவை அல்ல.",
          "te": "మీకు సరిగ్గా చెల్లింపు జరగకపోతే, మీ నివాసం అసురక్షితంగా ఉంటే, లేదా మీ యజమాని మిమ్మల్ని అన్యాయంగా ఒత్తిడి చేస్తుంటే, సహాయం చేయడానికి నిజమైన సంస్థలు ఉన్నాయి — వీటిలో చాలా వరకు ఉచితం, మరియు మీ యజమాని సహకారంపై ఆధారపడవు.",
          "ml": "നിങ്ങൾക്ക് ശരിയായി ശമ്പളം ലഭിക്കുന്നില്ലെങ്കിൽ, നിങ്ങളുടെ താമസം അരക്ഷിതമാണെങ്കിൽ, അല്ലെങ്കിൽ നിങ്ങളുടെ തൊഴിലുടമ നിങ്ങളെ അന്യായമായി സമ്മർദ്ദപ്പെടുത്തുകയാണെങ്കിൽ, സഹായിക്കാൻ യഥാർത്ഥ സംഘടനകൾ ഉണ്ട് — ഇവയിൽ മിക്കതും സൗജന്യമാണ്, കൂടാതെ നിങ്ങളുടെ തൊഴിലുടമയുടെ സഹകരണത്തെ ആശ്രയിക്കുന്നില്ല."},
    handles={"en": "TADM · Migrant Workers' Centre · HOME", "hi": "TADM · Migrant Workers' Centre · HOME", "ta": "TADM · Migrant Workers' Centre · HOME",
             "te": "TADM · Migrant Workers' Centre · HOME", "ml": "TADM · Migrant Workers' Centre · HOME"},
    steps={"en": ["TADM (Tripartite Alliance for Dispute Management) is the government's free mediation service for salary and employment disputes — for most salary-related claims, you're required to go through TADM before a case can go to the Employment Claims Tribunals.",
                  "TADM has two service centres and no public phone line for enquiries — mediation is done in person or online by appointment; check TADM's website for current locations and hours before you go.",
                  "The Migrant Workers' Centre (MWC) runs a 24-hour helpline at 6536 2692, with support available in around 10 languages — useful for urgent issues outside office hours.",
                  "HOME (Humanitarian Organisation for Migration Economics) runs a helpline you can call, SMS, or WhatsApp at +65 6341 5535, and a walk-in help desk at 720 Geylang Road #02-01, Singapore 389631, open Monday to Friday, 10am–5pm."],
           "hi": ["TADM (Tripartite Alliance for Dispute Management) वेतन और रोज़गार विवादों के लिए सरकार की मुफ़्त मध्यस्थता सेवा है — ज़्यादातर वेतन-संबंधी दावों के लिए, मामले के Employment Claims Tribunals में जाने से पहले आपको TADM से गुज़रना ज़रूरी है।",
                  "TADM के दो सेवा केंद्र हैं और पूछताछ के लिए कोई सार्वजनिक फ़ोन लाइन नहीं है — मध्यस्थता व्यक्तिगत रूप से या ऑनलाइन अपॉइंटमेंट से की जाती है; जाने से पहले वर्तमान स्थान और समय के लिए TADM की वेबसाइट देखें।",
                  "Migrant Workers' Centre (MWC) 6536 2692 पर 24-घंटे की हेल्पलाइन चलाता है, जिसमें लगभग 10 भाषाओं में सहायता उपलब्ध है — कार्यालय समय के बाहर तत्काल समस्याओं के लिए उपयोगी।",
                  "HOME (Humanitarian Organisation for Migration Economics) +65 6341 5535 पर कॉल, SMS, या WhatsApp के लिए हेल्पलाइन चलाता है, और 720 Geylang Road #02-01, Singapore 389631 पर एक वॉक-इन हेल्प डेस्क, जो सोमवार से शुक्रवार, सुबह 10 बजे से शाम 5 बजे तक खुला रहता है।"],
           "ta": ["TADM (Tripartite Alliance for Dispute Management) என்பது சம்பளம் மற்றும் வேலைவாய்ப்பு தகராறுகளுக்கான அரசாங்கத்தின் இலவச மத்தியஸ்த சேவை — பெரும்பாலான சம்பளம் தொடர்பான உரிமைகோரல்களுக்கு, வழக்கு Employment Claims Tribunals-க்குச் செல்வதற்கு முன் நீங்கள் TADM வழியாகச் செல்ல வேண்டும்.",
                  "TADM-க்கு இரண்டு சேவை மையங்கள் உள்ளன, விசாரணைகளுக்கு பொது தொலைபேசி வரி இல்லை — மத்தியஸ்தம் நேரடியாக அல்லது ஆன்லைனில் நேரம் ஒதுக்கீட்டின் மூலம் செய்யப்படுகிறது; செல்வதற்கு முன் தற்போதைய இடங்கள் மற்றும் நேரங்களுக்கு TADM இன் இணையதளத்தைப் பார்க்கவும்.",
                  "Migrant Workers' Centre (MWC) 6536 2692 இல் 24-மணி நேர உதவி எண்ணை இயக்குகிறது, சுமார் 10 மொழிகளில் ஆதரவு கிடைக்கிறது — அலுவலக நேரத்திற்கு வெளியே அவசர பிரச்சினைகளுக்கு பயனுள்ளது.",
                  "HOME (Humanitarian Organisation for Migration Economics) +65 6341 5535 இல் அழைப்பு, SMS, அல்லது WhatsApp-க்கான உதவி எண்ணை இயக்குகிறது, மேலும் 720 Geylang Road #02-01, Singapore 389631 இல் ஒரு நேரடி வருகை உதவி மேசை, திங்கள் முதல் வெள்ளி வரை, காலை 10 மணி முதல் மாலை 5 மணி வரை திறந்திருக்கும்."],
           "te": ["TADM (Tripartite Alliance for Dispute Management) జీతం మరియు ఉద్యోగ వివాదాల కోసం ప్రభుత్వ ఉచిత మధ్యవర్తిత్వ సేవ — చాలా జీతం సంబంధిత దావాలకు, కేసు Employment Claims Tribunals కి వెళ్లే ముందు మీరు TADM ద్వారా వెళ్లాల్సి ఉంటుంది.",
                  "TADM కి రెండు సేవా కేంద్రాలు ఉన్నాయి మరియు విచారణల కోసం ప్రజా ఫోన్ లైన్ లేదు — మధ్యవర్తిత్వం వ్యక్తిగతంగా లేదా ఆన్‌లైన్‌లో అపాయింట్‌మెంట్ ద్వారా జరుగుతుంది; వెళ్లే ముందు ప్రస్తుత స్థానాలు మరియు సమయాల కోసం TADM వెబ్‌సైట్‌ను తనిఖీ చేయండి.",
                  "Migrant Workers' Centre (MWC) 6536 2692 వద్ద 24-గంటల హెల్ప్‌లైన్‌ను నిర్వహిస్తుంది, సుమారు 10 భాషల్లో మద్దతు అందుబాటులో ఉంటుంది — కార్యాలయ సమయాల వెలుపల అత్యవసర సమస్యలకు ఉపయోగకరం.",
                  "HOME (Humanitarian Organisation for Migration Economics) +65 6341 5535 వద్ద కాల్, SMS, లేదా WhatsApp కోసం హెల్ప్‌లైన్‌ను నిర్వహిస్తుంది, మరియు 720 Geylang Road #02-01, Singapore 389631 వద్ద వాక్-ఇన్ హెల్ప్ డెస్క్, సోమవారం నుండి శుక్రవారం వరకు, ఉదయం 10 నుండి సాయంత్రం 5 వరకు తెరిచి ఉంటుంది."],
           "ml": ["TADM (Tripartite Alliance for Dispute Management) ശമ്പളവും തൊഴിൽ തർക്കങ്ങൾക്കുമുള്ള സർക്കാരിന്റെ സൗജന്യ മധ്യസ്ഥ സേവനമാണ് — മിക്ക ശമ്പള സംബന്ധമായ അവകാശവാദങ്ങൾക്കും, കേസ് Employment Claims Tribunals ലേക്ക് പോകുന്നതിന് മുമ്പ് നിങ്ങൾ TADM വഴി പോകേണ്ടതുണ്ട്.",
                  "TADM ന് രണ്ട് സേവന കേന്ദ്രങ്ങളുണ്ട്, അന്വേഷണങ്ങൾക്കായി പൊതു ഫോൺ ലൈൻ ഇല്ല — മധ്യസ്ഥത നേരിട്ടോ ഓൺലൈനിലോ അപ്പോയിന്റ്മെന്റ് വഴി നടത്തുന്നു; പോകുന്നതിന് മുമ്പ് നിലവിലെ സ്ഥലങ്ങളും സമയങ്ങളും TADM ന്റെ വെബ്‌സൈറ്റിൽ പരിശോധിക്കുക.",
                  "Migrant Workers' Centre (MWC) 6536 2692 ൽ 24-മണിക്കൂർ ഹെൽപ്‌ലൈൻ പ്രവർത്തിപ്പിക്കുന്നു, ഏകദേശം 10 ഭാഷകളിൽ പിന്തുണ ലഭ്യമാണ് — ഓഫീസ് സമയത്തിന് പുറത്തുള്ള അടിയന്തര പ്രശ്നങ്ങൾക്ക് ഉപയോഗപ്രദമാണ്.",
                  "HOME (Humanitarian Organisation for Migration Economics) +65 6341 5535 ൽ വിളിക്കാനോ SMS അയക്കാനോ WhatsApp ചെയ്യാനോ കഴിയുന്ന ഹെൽപ്‌ലൈൻ പ്രവർത്തിപ്പിക്കുന്നു, കൂടാതെ 720 Geylang Road #02-01, Singapore 389631 ൽ ഒരു വാക്ക്-ഇൻ ഹെൽപ്പ് ഡെസ്ക്, തിങ്കൾ മുതൽ വെള്ളി വരെ, രാവിലെ 10 മുതൽ വൈകിട്ട് 5 വരെ തുറന്നിരിക്കും."]},
    docs={"en": ["Salary not paid, paid late, or paid less than agreed: start with TADM.",
                 "Unsafe or unhygienic housing, harassment, or general distress: MWC's 24-hour helpline (6536 2692) or HOME's helpline (+65 6341 5535) can point you to the right support.",
                 "None of these organisations require your employer's permission or cooperation for you to contact them."],
          "hi": ["वेतन न मिला, देर से मिला, या सहमति से कम मिला: TADM से शुरुआत करें।",
                 "असुरक्षित या अस्वच्छ आवास, उत्पीड़न, या सामान्य परेशानी: MWC की 24-घंटे हेल्पलाइन (6536 2692) या HOME की हेल्पलाइन (+65 6341 5535) आपको सही सहायता की ओर इशारा कर सकती है।",
                 "इनमें से किसी भी संस्था से संपर्क करने के लिए आपके नियोक्ता की अनुमति या सहयोग की ज़रूरत नहीं है।"],
          "ta": ["சம்பளம் வழங்கப்படவில்லை, தாமதமாக வழங்கப்பட்டது, அல்லது ஒப்புக்கொள்ளப்பட்டதை விட குறைவாக வழங்கப்பட்டது: TADM உடன் தொடங்குங்கள்.",
                 "பாதுகாப்பற்ற அல்லது சுகாதாரமற்ற வீட்டுவசதி, துன்புறுத்தல், அல்லது பொதுவான துயரம்: MWC இன் 24-மணி நேர உதவி எண் (6536 2692) அல்லது HOME இன் உதவி எண் (+65 6341 5535) உங்களை சரியான ஆதரவை நோக்கி வழிநடத்த முடியும்.",
                 "இந்த அமைப்புகளில் எதுவும் உங்களைத் தொடர்பு கொள்ள உங்கள் முதலாளியின் அனுமதி அல்லது ஒத்துழைப்பைத் தேவைப்படுத்தாது."],
          "te": ["జీతం చెల్లించలేదు, ఆలస్యంగా చెల్లించారు, లేదా అంగీకరించిన దానికంటే తక్కువ చెల్లించారు: TADM తో ప్రారంభించండి.",
                 "అసురక్షిత లేదా అపరిశుభ్ర నివాసం, వేధింపులు, లేదా సాధారణ బాధ: MWC యొక్క 24-గంటల హెల్ప్‌లైన్ (6536 2692) లేదా HOME యొక్క హెల్ప్‌లైన్ (+65 6341 5535) మిమ్మల్ని సరైన మద్దతు వైపు నడిపించగలవు.",
                 "ఈ సంస్థలలో దేనినీ సంప్రదించడానికి మీ యజమాని అనుమతి లేదా సహకారం అవసరం లేదు."],
          "ml": ["ശമ്പളം നൽകിയില്ല, വൈകി നൽകി, അല്ലെങ്കിൽ അംഗീകരിച്ചതിലും കുറവ് നൽകി: TADM മായി ആരംഭിക്കുക.",
                 "അരക്ഷിതമോ ശുചിത്വമില്ലാത്തതോ ആയ താമസം, പീഡനം, അല്ലെങ്കിൽ പൊതുവായ ദുരിതം: MWC ന്റെ 24-മണിക്കൂർ ഹെൽപ്‌ലൈൻ (6536 2692) അല്ലെങ്കിൽ HOME ന്റെ ഹെൽപ്‌ലൈൻ (+65 6341 5535) നിങ്ങളെ ശരിയായ പിന്തുണയിലേക്ക് നയിക്കാൻ കഴിയും.",
                 "ഈ സംഘടനകളിൽ ഏതെങ്കിലും ബന്ധപ്പെടാൻ നിങ്ങളുടെ തൊഴിലുടമയുടെ അനുമതിയോ സഹകരണമോ ആവശ്യമില്ല."]},
    note={"en": "Save these numbers in your phone now, before you need them — in a genuine emergency (violence, immediate danger), call the police at 999 first.",
          "hi": "इन नंबरों को अभी अपने फ़ोन में सेव करें, ज़रूरत पड़ने से पहले — किसी वास्तविक आपातकाल (हिंसा, तत्काल ख़तरा) में, पहले 999 पर पुलिस को कॉल करें।",
          "ta": "இந்த எண்களை உங்களுக்கு தேவைப்படுவதற்கு முன்பே இப்போதே உங்கள் தொலைபேசியில் சேமித்து வையுங்கள் — உண்மையான அவசரநிலையில் (வன்முறை, உடனடி ஆபத்து), முதலில் 999 இல் காவல்துறையை அழைக்கவும்.",
          "te": "మీకు అవసరమయ్యే ముందే ఈ నంబర్లను ఇప్పుడే మీ ఫోన్‌లో సేవ్ చేసుకోండి — నిజమైన అత్యవసర పరిస్థితిలో (హింస, తక్షణ ప్రమాదం), ముందుగా 999 వద్ద పోలీసులకు కాల్ చేయండి.",
          "ml": "നിങ്ങൾക്ക് ആവശ്യമായി വരുന്നതിന് മുമ്പ് ഈ നമ്പറുകൾ ഇപ്പോൾ തന്നെ നിങ്ങളുടെ ഫോണിൽ സേവ് ചെയ്യുക — യഥാർത്ഥ അടിയന്തരാവസ്ഥയിൽ (അക്രമം, ഉടനടി അപകടം), ആദ്യം 999 ൽ പോലീസിനെ വിളിക്കുക."},
    location=None, phone=None, email=None,
    links=[
        {"href": "https://www.tal.sg/tadm/mediation-guide-3", "label": {"en": "↗ TADM — mediation guide for salary claims", "hi": "↗ TADM — वेतन दावों के लिए मध्यस्थता गाइड", "ta": "↗ TADM — சம்பள உரிமைகோரல்களுக்கான மத்தியஸ்த வழிகாட்டி", "te": "↗ TADM — జీతం దావాల కోసం మధ్యవర్తిత్వ గైడ్", "ml": "↗ TADM — ശമ്പള അവകാശവാദങ്ങൾക്കുള്ള മധ്യസ്ഥ ഗൈഡ്"}},
        {"href": "https://www.mwc.org.sg/", "label": {"en": "↗ Migrant Workers' Centre", "hi": "↗ Migrant Workers' Centre", "ta": "↗ Migrant Workers' Centre", "te": "↗ Migrant Workers' Centre", "ml": "↗ Migrant Workers' Centre"}},
        {"href": "https://www.home.org.sg/", "label": {"en": "↗ HOME", "hi": "↗ HOME", "ta": "↗ HOME", "te": "↗ HOME", "ml": "↗ HOME"}},
    ],
)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    html_out = render_shell()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote index.html: %d bytes, %d entries" % (len(html_out), len(ENTRIES)))

    for lang in LANGS:
        if lang == "en":
            continue  # English is baked directly into index.html; no separate file needed
        payload = build_lang_payload(lang)
        out_name = "lang-%s.json" % lang
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        print("Wrote %s: %d bytes, %d keys" % (out_name, os.path.getsize(out_name), len(payload)))
