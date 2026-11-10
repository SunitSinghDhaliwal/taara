"""Every line the app speaks is written here by hand, or typed by a parent. The AI never writes what a child hears.

Taara (a star) is a friendly coach. She never pretends to be family, except in the clearly
announced pretend call, and always points the child back to their real grandparent.
"""

CONTENT = {
    "hi-IN": {
        "buddy": "तारा",
        "buddy_roman": "Taara",
        "elder": "दादी",
        "elder_roman": "Dadi",
        "language_name": "Hindi",
        "ask_frame": "जब दादी पूछें, “{ask}” तो क्या बोलना है?",
        "model_prefix": "मेरे साथ बोलो: ",
        "shared": {
            "streak": "तीन सही, लगातार! तुम तो स्टार हो!",
            "fix": "लगभग सही! बस यह शब्द ठीक करो:",
            "tryagain": "फिर से कोशिश करो!",
            "hindi_please": "चलो, अब हिंदी में बात करते हैं!",
            "nevermind": "कोई बात नहीं।",
            "english": "हिंदी में ऐसे बोलते हैं। अब तुम बोलो।",
            "ring": "चलो एक खेल खेलें! मैं दादी बनती हूँ, तुम जवाब दो।",
            "ready": "शाबाश! अब असली दादी को फ़ोन करो!",
        },
        "praise": [
            "शाबाश! दादी बहुत खुश {G}!",
            "वाह! बिल्कुल सही!",
            "बहुत बढ़िया! तुम तो कमाल हो!",
            "एकदम सही! ऐसे ही बोलते रहो!",
            "अरे वाह! दादी को यह सुनकर बहुत अच्छा लगेगा!",
        ],
        "encourage": [
            "अच्छी कोशिश! अगली बार और भी अच्छा!",
            "बहुत अच्छे! थोड़ा थोड़ा करके आ जाएगा।",
            "वाह! बहुत बढ़िया कोशिश!",
        ],
        "lessons": [
            {"id": "hello", "emoji": "👋", "title": "Say hello",
             "ask": "नमस्ते बेटा!", "ask_roman": "Namaste beta!", "ask_en": "Hello, child!",
             "target": "नमस्ते दादी जी", "target_roman": "Namaste Dadi ji", "target_en": "Hello, Dadi ji"},
            {"id": "haal", "emoji": "😊", "title": "How are you?",
             "ask": "कैसे हो मेरे बच्चे?", "ask_roman": "Kaise ho mere bachche?", "ask_en": "How are you, my child?",
             "target": "मैं ठीक हूँ दादी जी", "target_roman": "Main theek hoon Dadi ji", "target_en": "I'm fine, Dadi ji"},
            {"id": "roti", "emoji": "🍽️", "title": "Have you eaten?",
             "ask": "बेटा, खाना खा लिया?", "ask_roman": "Beta, khaana kha liya?", "ask_en": "Have you eaten, child?",
             "target": "हाँ जी, मैंने खाना खा लिया", "target_roman": "Haan ji, maine khaana kha liya", "target_en": "Yes, I've eaten"},
            {"id": "family", "emoji": "👨‍👩‍👧", "title": "Mummy and Papa",
             "ask": "मम्मी पापा कैसे हैं?", "ask_roman": "Mummy Papa kaise hain?", "ask_en": "How are Mummy and Papa?",
             "target": "मम्मी पापा ठीक हैं", "target_roman": "Mummy Papa theek hain", "target_en": "Mummy and Papa are fine"},
            {"id": "school", "emoji": "🎒", "title": "School",
             "ask": "स्कूल कैसा चल रहा है?", "ask_roman": "School kaisa chal raha hai?", "ask_en": "How's school going?",
             "target": "स्कूल अच्छा है दादी जी", "target_roman": "School achha hai Dadi ji", "target_en": "School is good, Dadi ji"},
            {"id": "weather", "emoji": "❄️", "title": "Weather there",
             "ask": "वहाँ ठंड है?", "ask_roman": "Wahaan thand hai?", "ask_en": "Is it cold there?",
             "target": "हाँ जी, बहुत ठंड है", "target_roman": "Haan ji, bahut thand hai", "target_en": "Yes, it's very cold"},
            {"id": "visit", "emoji": "✈️", "title": "Coming to India",
             "ask": "भारत कब आओगे?", "ask_roman": "Bharat kab aaoge?", "ask_en": "When will you come to India?",
             "target": "गर्मियों में आएँगे", "target_roman": "Garmiyon mein aayenge", "target_en": "We'll come in the summer"},
            {"id": "bye", "emoji": "💛", "title": "Saying bye",
             "ask": "अच्छा बेटा, फ़ोन रखूँ?", "ask_roman": "Achha beta, phone rakhoon?", "ask_en": "Okay child, shall I hang up?",
             "target": "आपकी याद आती है दादी जी", "target_roman": "Aapki yaad aati hai Dadi ji", "target_en": "I miss you, Dadi ji"},
        ],
    },
    "pa-IN": {
        "buddy": "ਤਾਰਾ",
        "buddy_roman": "Taara",
        "elder": "ਬੇਬੇ",
        "elder_roman": "Bebe",
        "language_name": "Punjabi",
        "ask_frame": "ਜਦੋਂ ਬੇਬੇ ਪੁੱਛੇ, “{ask}” ਤਾਂ ਕੀ ਕਹਿਣਾ ਹੈ?",
        "model_prefix": "ਮੇਰੇ ਨਾਲ ਬੋਲੋ: ",
        "shared": {
            "streak": "ਤਿੰਨ ਸਹੀ, ਲਗਾਤਾਰ! ਤੁਸੀਂ ਤਾਂ ਸਟਾਰ ਹੋ!",
            "fix": "ਲਗਭਗ ਸਹੀ! ਬੱਸ ਇਹ ਸ਼ਬਦ ਠੀਕ ਕਰੋ:",
            "tryagain": "ਫੇਰ ਕੋਸ਼ਿਸ਼ ਕਰੋ!",
            "hindi_please": "ਚਲੋ, ਹੁਣ ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰੀਏ!",
            "nevermind": "ਕੋਈ ਗੱਲ ਨਹੀਂ।",
            "english": "ਪੰਜਾਬੀ ਵਿੱਚ ਇੰਝ ਕਹਿੰਦੇ ਹਨ। ਹੁਣ ਤੁਸੀਂ ਬੋਲੋ।",
            "ring": "ਚਲੋ ਇੱਕ ਖੇਡ ਖੇਡੀਏ! ਮੈਂ ਬੇਬੇ ਬਣਦੀ ਹਾਂ, ਤੁਸੀਂ ਜਵਾਬ ਦਿਓ।",
            "ready": "ਸ਼ਾਬਾਸ਼! ਹੁਣ ਅਸਲੀ ਬੇਬੇ ਨੂੰ ਫ਼ੋਨ ਕਰੋ!",
        },
        "praise": [
            "ਸ਼ਾਬਾਸ਼! ਬੇਬੇ ਬਹੁਤ ਖ਼ੁਸ਼ {G}!",
            "ਵਾਹ! ਬਿਲਕੁਲ ਠੀਕ!",
            "ਬਹੁਤ ਵਧੀਆ! ਤੁਸੀਂ ਤਾਂ ਕਮਾਲ ਕਰ ਦਿੱਤਾ!",
            "ਇੱਕਦਮ ਸਹੀ! ਇੰਜ ਹੀ ਬੋਲਦੇ ਰਹੋ!",
            "ਅਰੇ ਵਾਹ! ਬੇਬੇ ਨੂੰ ਇਹ ਸੁਣ ਕੇ ਬਹੁਤ ਚੰਗਾ ਲੱਗੇਗਾ!",
        ],
        "encourage": [
            "ਵਧੀਆ ਕੋਸ਼ਿਸ਼! ਅਗਲੀ ਵਾਰ ਹੋਰ ਵੀ ਵਧੀਆ!",
            "ਸ਼ਾਬਾਸ਼! ਹੌਲੀ ਹੌਲੀ ਆ ਜਾਵੇਗਾ।",
            "ਵਾਹ! ਬਹੁਤ ਵਧੀਆ ਕੋਸ਼ਿਸ਼!",
        ],
        "lessons": [
            {"id": "hello", "emoji": "👋", "title": "Say hello",
             "ask": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪੁੱਤ!", "ask_roman": "Sat Sri Akal putt!", "ask_en": "Hello, my child!",
             "target": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਬੇਬੇ ਜੀ", "target_roman": "Sat Sri Akal Bebe ji", "target_en": "Hello, Bebe ji"},
            {"id": "haal", "emoji": "😊", "title": "How are you?",
             "ask": "ਕੀ ਹਾਲ ਹੈ ਮੇਰੇ ਪੁੱਤ ਦਾ?", "ask_roman": "Ki haal hai mere putt da?", "ask_en": "How is my child?",
             "target": "ਮੈਂ ਠੀਕ ਹਾਂ ਬੇਬੇ ਜੀ", "target_roman": "Main theek haan Bebe ji", "target_en": "I'm fine, Bebe ji"},
            {"id": "roti", "emoji": "🍽️", "title": "Have you eaten?",
             "ask": "ਪੁੱਤ, ਰੋਟੀ ਖਾ ਲਈ?", "ask_roman": "Putt, roti kha lai?", "ask_en": "Have you eaten, child?",
             "target": "ਹਾਂ ਜੀ, ਮੈਂ ਰੋਟੀ ਖਾ ਲਈ", "target_roman": "Haan ji, main roti kha lai", "target_en": "Yes, I've eaten"},
            {"id": "family", "emoji": "👨‍👩‍👧", "title": "Mummy and Papa",
             "ask": "ਮੰਮੀ ਪਾਪਾ ਕਿਵੇਂ ਨੇ?", "ask_roman": "Mummy Papa kiven ne?", "ask_en": "How are Mummy and Papa?",
             "target": "ਮੰਮੀ ਪਾਪਾ ਠੀਕ ਨੇ", "target_roman": "Mummy Papa theek ne", "target_en": "Mummy and Papa are fine"},
            {"id": "school", "emoji": "🎒", "title": "School",
             "ask": "ਸਕੂਲ ਕਿਵੇਂ ਚੱਲ ਰਿਹਾ?", "ask_roman": "School kiven chall reha?", "ask_en": "How's school going?",
             "target": "ਸਕੂਲ ਵਧੀਆ ਹੈ ਬੇਬੇ ਜੀ", "target_roman": "School vadhiya hai Bebe ji", "target_en": "School is great, Bebe ji"},
            {"id": "weather", "emoji": "❄️", "title": "Weather there",
             "ask": "ਉੱਥੇ ਠੰਢ ਹੈ?", "ask_roman": "Uthe thandh hai?", "ask_en": "Is it cold there?",
             "target": "ਹਾਂ ਜੀ, ਬਹੁਤ ਠੰਢ ਹੈ", "target_roman": "Haan ji, bahut thandh hai", "target_en": "Yes, it's very cold"},
            {"id": "visit", "emoji": "✈️", "title": "Coming to Punjab",
             "ask": "ਪੰਜਾਬ ਕਦੋਂ ਆਓਗੇ?", "ask_roman": "Punjab kadon aaoge?", "ask_en": "When will you come to Punjab?",
             "target": "ਗਰਮੀਆਂ ਵਿੱਚ ਆਵਾਂਗੇ", "target_roman": "Garmiyan vich aavange", "target_en": "We'll come in the summer"},
            {"id": "bye", "emoji": "💛", "title": "Saying bye",
             "ask": "ਚੰਗਾ ਪੁੱਤ, ਫ਼ੋਨ ਰੱਖਾਂ?", "ask_roman": "Changa putt, phone rakhaan?", "ask_en": "Okay child, shall I hang up?",
             "target": "ਤੁਹਾਡੀ ਯਾਦ ਆਉਂਦੀ ਹੈ ਬੇਬੇ ਜੀ", "target_roman": "Tuhadi yaad aundi hai Bebe ji", "target_en": "I miss you, Bebe ji"},
        ],
    },
}


import re

# First words for little ones: Taara says the English word, then the family-language word.
WORD_FRAME = {
    "hi-IN": "{en} को हिंदी में कहते हैं, {target}। बोलो, {target}!",
    "pa-IN": "{en} ਨੂੰ ਪੰਜਾਬੀ ਵਿੱਚ ਕਹਿੰਦੇ ਨੇ, {target}। ਬੋਲੋ, {target}!",
}
WORDS = {
    "hi-IN": [
        ("family", "Family", [("दादी", "Dadi", "Papa's mummy"), ("दादा", "Dada", "Papa's papa"), ("नानी", "Nani", "Mummy's mummy"),
                              ("नाना", "Nana", "Mummy's papa"), ("भाई", "Bhai", "Brother"), ("बहन", "Behen", "Sister")]),
        ("food", "Food", [("पानी", "Paani", "Water"), ("दूध", "Doodh", "Milk"), ("खाना", "Khaana", "Food"),
                          ("फल", "Phal", "Fruit"), ("आम", "Aam", "Mango")]),
        ("numbers", "Numbers 1 to 5", [("एक", "Ek", "One"), ("दो", "Do", "Two"), ("तीन", "Teen", "Three"),
                                       ("चार", "Chaar", "Four"), ("पाँच", "Paanch", "Five")]),
        ("numbers2", "Numbers 6 to 10", [("छह", "Chheh", "Six"), ("सात", "Saat", "Seven"), ("आठ", "Aath", "Eight"),
                                         ("नौ", "Nau", "Nine"), ("दस", "Das", "Ten")]),
        ("colours", "Colours", [("लाल", "Laal", "Red"), ("नीला", "Neela", "Blue"), ("पीला", "Peela", "Yellow"), ("हरा", "Hara", "Green")]),
        ("animals", "Animals", [("कुत्ता", "Kutta", "Dog"), ("बिल्ली", "Billi", "Cat"), ("गाय", "Gaay", "Cow"),
                                ("हाथी", "Haathi", "Elephant"), ("शेर", "Sher", "Lion"), ("चिड़िया", "Chidiya", "Bird")]),
        ("body", "My body", [("आँख", "Aankh", "Eye"), ("नाक", "Naak", "Nose"), ("कान", "Kaan", "Ear"),
                             ("मुँह", "Munh", "Mouth"), ("हाथ", "Haath", "Hand"), ("पैर", "Pair", "Foot")]),
        ("feelings", "Feelings", [("खुश", "Khush", "Happy"), ("उदास", "Udaas", "Sad"), ("भूख", "Bhookh", "Hunger"),
                                  ("प्यास", "Pyaas", "Thirst"), ("नींद", "Neend", "Sleep")]),
        ("manners", "Kind words", [("धन्यवाद", "Dhanyavaad", "Thank you"), ("माफ़ करना", "Maaf karna", "Sorry"),
                                   ("नमस्ते", "Namaste", "Hello"), ("शुभ रात्रि", "Shubh raatri", "Good night"), ("जी हाँ", "Ji haan", "Yes please")]),
    ],
    "pa-IN": [
        ("family", "Family", [("ਦਾਦੀ", "Dadi", "Papa's mummy"), ("ਦਾਦਾ", "Dada", "Papa's papa"), ("ਨਾਨੀ", "Nani", "Mummy's mummy"),
                              ("ਨਾਨਾ", "Nana", "Mummy's papa"), ("ਭਰਾ", "Bhra", "Brother"), ("ਭੈਣ", "Bhain", "Sister")]),
        ("food", "Food", [("ਪਾਣੀ", "Paani", "Water"), ("ਦੁੱਧ", "Duddh", "Milk"), ("ਖਾਣਾ", "Khaana", "Food"),
                          ("ਫਲ", "Phal", "Fruit"), ("ਅੰਬ", "Amb", "Mango")]),
        ("numbers", "Numbers 1 to 5", [("ਇੱਕ", "Ikk", "One"), ("ਦੋ", "Do", "Two"), ("ਤਿੰਨ", "Tinn", "Three"),
                                       ("ਚਾਰ", "Chaar", "Four"), ("ਪੰਜ", "Panj", "Five")]),
        ("numbers2", "Numbers 6 to 10", [("ਛੇ", "Chhe", "Six"), ("ਸੱਤ", "Satt", "Seven"), ("ਅੱਠ", "Atth", "Eight"),
                                         ("ਨੌਂ", "Naun", "Nine"), ("ਦਸ", "Das", "Ten")]),
        ("colours", "Colours", [("ਲਾਲ", "Laal", "Red"), ("ਨੀਲਾ", "Neela", "Blue"), ("ਪੀਲਾ", "Peela", "Yellow"), ("ਹਰਾ", "Hara", "Green")]),
        ("animals", "Animals", [("ਕੁੱਤਾ", "Kutta", "Dog"), ("ਬਿੱਲੀ", "Billi", "Cat"), ("ਗਾਂ", "Gaan", "Cow"),
                                ("ਹਾਥੀ", "Haathi", "Elephant"), ("ਸ਼ੇਰ", "Sher", "Lion"), ("ਚਿੜੀ", "Chiri", "Bird")]),
        ("body", "My body", [("ਅੱਖ", "Akh", "Eye"), ("ਨੱਕ", "Nakk", "Nose"), ("ਕੰਨ", "Kann", "Ear"),
                             ("ਮੂੰਹ", "Moonh", "Mouth"), ("ਹੱਥ", "Hath", "Hand"), ("ਪੈਰ", "Pair", "Foot")]),
        ("feelings", "Feelings", [("ਖ਼ੁਸ਼", "Khush", "Happy"), ("ਉਦਾਸ", "Udaas", "Sad"), ("ਭੁੱਖ", "Bhukh", "Hunger"),
                                  ("ਪਿਆਸ", "Pyaas", "Thirst"), ("ਨੀਂਦ", "Neend", "Sleep")]),
        ("manners", "Kind words", [("ਧੰਨਵਾਦ", "Dhanvaad", "Thank you"), ("ਮਾਫ਼ ਕਰਨਾ", "Maaf karna", "Sorry"),
                                   ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "Sat Sri Akal", "Hello"), ("ਸ਼ੁਭ ਰਾਤ", "Shubh raat", "Good night"), ("ਹਾਂ ਜੀ", "Haan ji", "Yes please")]),
    ],
}


# Questions only used in the pretend call, so the call is different each time.
CALL_EXTRAS = {
    "hi-IN": [
        {"id": "c-aaj", "title": "What did you eat today?",
         "ask": "आज खाने में क्या खाया?", "ask_roman": "Aaj khaane mein kya khaaya?", "ask_en": "What did you eat today?",
         "target": "आज मैंने दाल चावल खाए", "target_roman": "Aaj maine daal chawal khaaye", "target_en": "I ate dal and rice today"},
        {"id": "c-padhai", "title": "Studies",
         "ask": "पढ़ाई कैसी चल रही है?", "ask_roman": "Padhai kaisi chal rahi hai?", "ask_en": "How are your studies going?",
         "target": "पढ़ाई अच्छी चल रही है", "target_roman": "Padhai achhi chal rahi hai", "target_en": "Studies are going well"},
        {"id": "c-neend", "title": "Sleep",
         "ask": "रात को अच्छी नींद आई?", "ask_roman": "Raat ko achhi neend aayi?", "ask_en": "Did you sleep well last night?",
         "target": "हाँ जी, अच्छी नींद आई", "target_roman": "Haan ji, achhi neend aayi", "target_en": "Yes, I slept well"},
        {"id": "c-dost", "title": "Friends",
         "ask": "स्कूल में दोस्त हैं?", "ask_roman": "School mein dost hain?", "ask_en": "Do you have friends at school?",
         "target": "हाँ जी, बहुत दोस्त हैं", "target_roman": "Haan ji, bahut dost hain", "target_en": "Yes, lots of friends"},
    ],
    "pa-IN": [
        {"id": "c-aaj", "title": "What did you eat today?",
         "ask": "ਅੱਜ ਕੀ ਖਾਧਾ?", "ask_roman": "Ajj ki khaadha?", "ask_en": "What did you eat today?",
         "target": "ਅੱਜ ਮੈਂ ਦਾਲ ਚੌਲ ਖਾਧੇ", "target_roman": "Ajj main daal chaul khaadhe", "target_en": "I ate dal and rice today"},
        {"id": "c-padhai", "title": "Studies",
         "ask": "ਪੜ੍ਹਾਈ ਕਿਵੇਂ ਚੱਲ ਰਹੀ ਹੈ?", "ask_roman": "Padhai kiven chall rahi hai?", "ask_en": "How are your studies going?",
         "target": "ਪੜ੍ਹਾਈ ਵਧੀਆ ਚੱਲ ਰਹੀ ਹੈ", "target_roman": "Padhai vadhiya chall rahi hai", "target_en": "Studies are going well"},
        {"id": "c-neend", "title": "Sleep",
         "ask": "ਰਾਤ ਨੂੰ ਨੀਂਦ ਚੰਗੀ ਆਈ?", "ask_roman": "Raat nu neend changi aayi?", "ask_en": "Did you sleep well last night?",
         "target": "ਹਾਂ ਜੀ, ਨੀਂਦ ਚੰਗੀ ਆਈ", "target_roman": "Haan ji, neend changi aayi", "target_en": "Yes, I slept well"},
        {"id": "c-dost", "title": "Friends",
         "ask": "ਸਕੂਲ ਵਿੱਚ ਦੋਸਤ ਨੇ?", "ask_roman": "School vich dost ne?", "ask_en": "Do you have friends at school?",
         "target": "ਹਾਂ ਜੀ, ਬਹੁਤ ਦੋਸਤ ਨੇ", "target_roman": "Haan ji, bahut dost ne", "target_en": "Yes, lots of friends"},
    ],
}


# Who the child is practising for. Every line adapts, with the right grammar for him or her.
RELATIVES = {
    "hi-IN": [
        {"id": "dadi", "native": "दादी", "roman": "Dadi", "gender": "f", "en": "Papa's mummy"},
        {"id": "dada", "native": "दादा", "roman": "Dada", "gender": "m", "en": "Papa's papa"},
        {"id": "nani", "native": "नानी", "roman": "Nani", "gender": "f", "en": "Mummy's mummy"},
        {"id": "nana", "native": "नाना", "roman": "Nana", "gender": "m", "en": "Mummy's papa"},
        {"id": "bua", "native": "बुआ", "roman": "Bua", "gender": "f", "en": "Papa's sister"},
        {"id": "chacha", "native": "चाचा", "roman": "Chacha", "gender": "m", "en": "Papa's brother"},
        {"id": "mausi", "native": "मौसी", "roman": "Mausi", "gender": "f", "en": "Mummy's sister"},
        {"id": "mama", "native": "मामा", "roman": "Mama", "gender": "m", "en": "Mummy's brother"},
    ],
    "pa-IN": [
        {"id": "bebe", "native": "ਬੇਬੇ", "roman": "Bebe", "gender": "f", "en": "Grandma"},
        {"id": "dada", "native": "ਦਾਦਾ", "roman": "Dada", "gender": "m", "en": "Papa's papa"},
        {"id": "nani", "native": "ਨਾਨੀ", "roman": "Nani", "gender": "f", "en": "Mummy's mummy"},
        {"id": "nana", "native": "ਨਾਨਾ", "roman": "Nana", "gender": "m", "en": "Mummy's papa"},
        {"id": "bhua", "native": "ਭੂਆ", "roman": "Bhua", "gender": "f", "en": "Papa's sister"},
        {"id": "chacha", "native": "ਚਾਚਾ", "roman": "Chacha", "gender": "m", "en": "Papa's brother"},
        {"id": "masi", "native": "ਮਾਸੀ", "roman": "Masi", "gender": "f", "en": "Mummy's sister"},
        {"id": "mama", "native": "ਮਾਮਾ", "roman": "Mama", "gender": "m", "en": "Mummy's brother"},
    ],
}
GENDER_WORD = {"hi-IN": {"f": "होंगी", "m": "होंगे"}, "pa-IN": {"f": "ਹੋਵੇਗੀ", "m": "ਹੋਵੇਗਾ"}}
FIND_FRAME = {"hi-IN": "{word} कहाँ है? छूकर दिखाओ!", "pa-IN": "{word} ਕਿੱਥੇ ਹੈ? ਛੂਹ ਕੇ ਦਿਖਾਓ!"}
GREET_FRAME = {"hi-IN": "नमस्ते {name}! चलो सीखते हैं।", "pa-IN": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ {name}! ਚਲੋ ਸਿੱਖੀਏ।"}


# Each relative has their own favourite questions, added to the path and every pretend call.
RELATIVE_EXTRAS = {
    "hi-IN": {
        "dadi": [
            {"id": "r-dadi-1", "special": True, "title": "Favourite food", "ask": "बेटा, तुम्हें क्या खाना पसंद है?", "ask_roman": "Beta, tumhe kya khaana pasand hai?", "ask_en": "What food do you like?", "target": "मुझे आलू के पराठे पसंद हैं", "target_roman": "Mujhe aloo ke parathe pasand hain", "target_en": "I like aloo parathas"},
            {"id": "r-dadi-2", "special": True, "title": "Diwali", "ask": "दिवाली पर क्या किया?", "ask_roman": "Diwali par kya kiya?", "ask_en": "What did you do on Diwali?", "target": "हमने दिए जलाए", "target_roman": "Humne diye jalaaye", "target_en": "We lit diyas"},
        ],
        "dada": [
            {"id": "r-dada-1", "special": True, "title": "Cricket", "ask": "कल क्रिकेट मैच देखा?", "ask_roman": "Kal cricket match dekha?", "ask_en": "Did you watch the cricket match yesterday?", "target": "हाँ जी, मैंने मैच देखा", "target_roman": "Haan ji, maine match dekha", "target_en": "Yes, I watched the match"},
            {"id": "r-dada-2", "special": True, "title": "In the park", "ask": "पार्क में क्या खेला?", "ask_roman": "Park mein kya khela?", "ask_en": "What did you play in the park?", "target": "मैंने फुटबॉल खेला", "target_roman": "Maine football khela", "target_en": "I played football"},
        ],
        "nani": [
            {"id": "r-nani-1", "special": True, "title": "Nani's halwa", "ask": "नानी के हाथ का हलवा याद है?", "ask_roman": "Nani ke haath ka halwa yaad hai?", "ask_en": "Do you remember Nani's halwa?", "target": "हाँ जी, बहुत याद है", "target_roman": "Haan ji, bahut yaad hai", "target_en": "Yes, I remember it well"},
            {"id": "r-nani-2", "special": True, "title": "Mummy's cooking", "ask": "आज मम्मी ने क्या बनाया?", "ask_roman": "Aaj Mummy ne kya banaaya?", "ask_en": "What did Mummy cook today?", "target": "मम्मी ने राजमा चावल बनाए", "target_roman": "Mummy ne rajma chawal banaaye", "target_en": "Mummy made rajma rice"},
        ],
        "nana": [
            {"id": "r-nana-1", "special": True, "title": "Stories", "ask": "तुम्हें कौन सी कहानी पसंद है?", "ask_roman": "Tumhe kaun si kahaani pasand hai?", "ask_en": "Which story do you like?", "target": "मुझे परियों की कहानियाँ पसंद हैं", "target_roman": "Mujhe pariyon ki kahaaniyan pasand hain", "target_en": "I like fairy stories"},
            {"id": "r-nana-2", "special": True, "title": "Today's weather", "ask": "आज मौसम कैसा है?", "ask_roman": "Aaj mausam kaisa hai?", "ask_en": "How's the weather today?", "target": "आज धूप निकली है", "target_roman": "Aaj dhoop nikli hai", "target_en": "It's sunny today"},
        ],
        "bua": [
            {"id": "r-bua-1", "special": True, "title": "Your drawing", "ask": "ड्रॉइंग में क्या बनाया?", "ask_roman": "Drawing mein kya banaaya?", "ask_en": "What did you draw?", "target": "मैंने एक घर बनाया", "target_roman": "Maine ek ghar banaaya", "target_en": "I drew a house"},
            {"id": "r-bua-2", "special": True, "title": "Best friend", "ask": "तुम्हारा सबसे अच्छा दोस्त कौन है?", "ask_roman": "Tumhaara sabse achha dost kaun hai?", "ask_en": "Who is your best friend?", "target": "मेरा सबसे अच्छा दोस्त सैम है", "target_roman": "Mera sabse achha dost Sam hai", "target_en": "My best friend is Sam"},
        ],
        "chacha": [
            {"id": "r-chacha-1", "special": True, "title": "Sports", "ask": "कौन सा खेल पसंद है?", "ask_roman": "Kaun sa khel pasand hai?", "ask_en": "Which sport do you like?", "target": "मुझे फुटबॉल पसंद है", "target_roman": "Mujhe football pasand hai", "target_en": "I like football"},
            {"id": "r-chacha-2", "special": True, "title": "Marks", "ask": "स्कूल में कितने नंबर आए?", "ask_roman": "School mein kitne number aaye?", "ask_en": "What marks did you get at school?", "target": "मेरे अच्छे नंबर आए", "target_roman": "Mere achhe number aaye", "target_en": "I got good marks"},
        ],
        "mausi": [
            {"id": "r-mausi-1", "special": True, "title": "A card", "ask": "मौसी के लिए क्या बनाया?", "ask_roman": "Mausi ke liye kya banaaya?", "ask_en": "What did you make for Mausi?", "target": "मैंने एक कार्ड बनाया", "target_roman": "Maine ek card banaaya", "target_en": "I made a card"},
            {"id": "r-mausi-2", "special": True, "title": "Holidays", "ask": "छुट्टियों में कहाँ घूमने गए?", "ask_roman": "Chhuttiyon mein kahaan ghoomne gaye?", "ask_en": "Where did you go on holiday?", "target": "हम समुद्र किनारे गए", "target_roman": "Hum samudra kinaare gaye", "target_en": "We went to the beach"},
        ],
        "mama": [
            {"id": "r-mama-1", "special": True, "title": "Visiting Mama", "ask": "मामा के घर कब आना है?", "ask_roman": "Mama ke ghar kab aana hai?", "ask_en": "When are you coming to Mama's house?", "target": "गर्मियों में आना है", "target_roman": "Garmiyon mein aana hai", "target_en": "In the summer"},
            {"id": "r-mama-2", "special": True, "title": "A gift", "ask": "मामा से क्या गिफ़्ट चाहिए?", "ask_roman": "Mama se kya gift chahiye?", "ask_en": "What gift do you want from Mama?", "target": "मुझे एक साइकिल चाहिए", "target_roman": "Mujhe ek cycle chahiye", "target_en": "I want a bicycle"},
        ],
    },
    "pa-IN": {
        "bebe": [
            {"id": "r-bebe-1", "special": True, "title": "Favourite food", "ask": "ਪੁੱਤ, ਤੈਨੂੰ ਕੀ ਖਾਣਾ ਪਸੰਦ ਹੈ?", "ask_roman": "Putt, tainu ki khaana pasand hai?", "ask_en": "What food do you like?", "target": "ਮੈਨੂੰ ਆਲੂ ਦੇ ਪਰਾਂਠੇ ਪਸੰਦ ਨੇ", "target_roman": "Mainu aloo de paranthe pasand ne", "target_en": "I like aloo parathas"},
            {"id": "r-bebe-2", "special": True, "title": "Diwali", "ask": "ਦੀਵਾਲੀ ਤੇ ਕੀ ਕੀਤਾ?", "ask_roman": "Diwali te ki keeta?", "ask_en": "What did you do on Diwali?", "target": "ਅਸੀਂ ਦੀਵੇ ਜਗਾਏ", "target_roman": "Asin deeve jagaaye", "target_en": "We lit diyas"},
        ],
        "dada": [
            {"id": "r-dada-1", "special": True, "title": "Cricket", "ask": "ਕੱਲ੍ਹ ਕ੍ਰਿਕਟ ਮੈਚ ਦੇਖਿਆ?", "ask_roman": "Kall cricket match dekhya?", "ask_en": "Did you watch the cricket match yesterday?", "target": "ਹਾਂ ਜੀ, ਮੈਂ ਮੈਚ ਦੇਖਿਆ", "target_roman": "Haan ji, main match dekhya", "target_en": "Yes, I watched the match"},
            {"id": "r-dada-2", "special": True, "title": "In the park", "ask": "ਪਾਰਕ ਵਿੱਚ ਕੀ ਖੇਡਿਆ?", "ask_roman": "Park vich ki khedya?", "ask_en": "What did you play in the park?", "target": "ਮੈਂ ਫੁੱਟਬਾਲ ਖੇਡਿਆ", "target_roman": "Main football khedya", "target_en": "I played football"},
        ],
        "nani": [
            {"id": "r-nani-1", "special": True, "title": "Nani's kheer", "ask": "ਨਾਨੀ ਦੇ ਹੱਥ ਦੀ ਖੀਰ ਯਾਦ ਹੈ?", "ask_roman": "Nani de hath di kheer yaad hai?", "ask_en": "Do you remember Nani's kheer?", "target": "ਹਾਂ ਜੀ, ਬਹੁਤ ਯਾਦ ਹੈ", "target_roman": "Haan ji, bahut yaad hai", "target_en": "Yes, I remember it well"},
            {"id": "r-nani-2", "special": True, "title": "Mummy's cooking", "ask": "ਅੱਜ ਮੰਮੀ ਨੇ ਕੀ ਬਣਾਇਆ?", "ask_roman": "Ajj Mummy ne ki banaaya?", "ask_en": "What did Mummy cook today?", "target": "ਮੰਮੀ ਨੇ ਰਾਜਮਾਹ ਚੌਲ ਬਣਾਏ", "target_roman": "Mummy ne rajmah chaul banaaye", "target_en": "Mummy made rajma rice"},
        ],
        "nana": [
            {"id": "r-nana-1", "special": True, "title": "Stories", "ask": "ਤੈਨੂੰ ਕਿਹੜੀ ਕਹਾਣੀ ਪਸੰਦ ਹੈ?", "ask_roman": "Tainu kehri kahaani pasand hai?", "ask_en": "Which story do you like?", "target": "ਮੈਨੂੰ ਪਰੀਆਂ ਦੀਆਂ ਕਹਾਣੀਆਂ ਪਸੰਦ ਨੇ", "target_roman": "Mainu pariyan diyan kahaaniyan pasand ne", "target_en": "I like fairy stories"},
            {"id": "r-nana-2", "special": True, "title": "Today's weather", "ask": "ਅੱਜ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਹੈ?", "ask_roman": "Ajj mausam kiho jiha hai?", "ask_en": "How's the weather today?", "target": "ਅੱਜ ਧੁੱਪ ਨਿਕਲੀ ਹੈ", "target_roman": "Ajj dhupp nikli hai", "target_en": "It's sunny today"},
        ],
        "bhua": [
            {"id": "r-bhua-1", "special": True, "title": "Your drawing", "ask": "ਡਰਾਇੰਗ ਵਿੱਚ ਕੀ ਬਣਾਇਆ?", "ask_roman": "Drawing vich ki banaaya?", "ask_en": "What did you draw?", "target": "ਮੈਂ ਇੱਕ ਘਰ ਬਣਾਇਆ", "target_roman": "Main ikk ghar banaaya", "target_en": "I drew a house"},
            {"id": "r-bhua-2", "special": True, "title": "Best friend", "ask": "ਤੇਰਾ ਸਭ ਤੋਂ ਵਧੀਆ ਦੋਸਤ ਕੌਣ ਹੈ?", "ask_roman": "Tera sabh ton vadhiya dost kaun hai?", "ask_en": "Who is your best friend?", "target": "ਮੇਰਾ ਸਭ ਤੋਂ ਵਧੀਆ ਦੋਸਤ ਸੈਮ ਹੈ", "target_roman": "Mera sabh ton vadhiya dost Sam hai", "target_en": "My best friend is Sam"},
        ],
        "chacha": [
            {"id": "r-chacha-1", "special": True, "title": "Sports", "ask": "ਕਿਹੜੀ ਖੇਡ ਪਸੰਦ ਹੈ?", "ask_roman": "Kehri khed pasand hai?", "ask_en": "Which sport do you like?", "target": "ਮੈਨੂੰ ਫੁੱਟਬਾਲ ਪਸੰਦ ਹੈ", "target_roman": "Mainu football pasand hai", "target_en": "I like football"},
            {"id": "r-chacha-2", "special": True, "title": "Marks", "ask": "ਸਕੂਲ ਵਿੱਚ ਕਿੰਨੇ ਨੰਬਰ ਆਏ?", "ask_roman": "School vich kinne number aaye?", "ask_en": "What marks did you get at school?", "target": "ਮੇਰੇ ਚੰਗੇ ਨੰਬਰ ਆਏ", "target_roman": "Mere change number aaye", "target_en": "I got good marks"},
        ],
        "masi": [
            {"id": "r-masi-1", "special": True, "title": "A card", "ask": "ਮਾਸੀ ਲਈ ਕੀ ਬਣਾਇਆ?", "ask_roman": "Masi layi ki banaaya?", "ask_en": "What did you make for Masi?", "target": "ਮੈਂ ਇੱਕ ਕਾਰਡ ਬਣਾਇਆ", "target_roman": "Main ikk card banaaya", "target_en": "I made a card"},
            {"id": "r-masi-2", "special": True, "title": "Holidays", "ask": "ਛੁੱਟੀਆਂ ਵਿੱਚ ਕਿੱਥੇ ਘੁੰਮਣ ਗਏ?", "ask_roman": "Chhuttiyan vich kithe ghumman gaye?", "ask_en": "Where did you go on holiday?", "target": "ਅਸੀਂ ਸਮੁੰਦਰ ਕੰਢੇ ਗਏ", "target_roman": "Asin samundar kandhe gaye", "target_en": "We went to the beach"},
        ],
        "mama": [
            {"id": "r-mama-1", "special": True, "title": "Visiting Mama", "ask": "ਮਾਮੇ ਦੇ ਘਰ ਕਦੋਂ ਆਉਣਾ ਹੈ?", "ask_roman": "Mame de ghar kadon aauna hai?", "ask_en": "When are you coming to Mama's house?", "target": "ਗਰਮੀਆਂ ਵਿੱਚ ਆਉਣਾ ਹੈ", "target_roman": "Garmiyan vich aauna hai", "target_en": "In the summer"},
            {"id": "r-mama-2", "special": True, "title": "A gift", "ask": "ਮਾਮੇ ਤੋਂ ਕੀ ਤੋਹਫ਼ਾ ਚਾਹੀਦਾ ਹੈ?", "ask_roman": "Mame ton ki tohfa chahida hai?", "ask_en": "What gift do you want from Mama?", "target": "ਮੈਨੂੰ ਇੱਕ ਸਾਈਕਲ ਚਾਹੀਦਾ ਹੈ", "target_roman": "Mainu ikk cycle chahida hai", "target_en": "I want a bicycle"},
        ],
    },
}


def relative(lang: str, rel_id=None) -> dict:
    options = RELATIVES[lang]
    return next((r for r in options if r["id"] == rel_id), options[0])


def localize(lang: str, rel_id=None) -> dict:
    """The language's content with the chosen relative's name and grammar filled in."""
    rel = relative(lang, rel_id)
    src_native, src_roman = CONTENT[lang]["elder"], CONTENT[lang]["elder_roman"]
    word = GENDER_WORD[lang][rel["gender"]]

    def walk(x):
        if isinstance(x, str):
            return x.replace("{G}", word).replace(src_native, rel["native"]).replace(src_roman, rel["roman"])
        if isinstance(x, list):
            return [walk(i) for i in x]
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        return x

    out = walk({**CONTENT[lang], "call_extras": CALL_EXTRAS[lang]})
    out["lessons"] = out["lessons"] + RELATIVE_EXTRAS[lang].get(rel["id"], [])
    out["relative"] = rel
    out["relatives"] = RELATIVES[lang]
    return out


def tracks(lang: str) -> list:
    out = []
    for track_id, title, items in WORDS[lang]:
        out.append({"id": track_id, "title": title, "items": [
            {"id": f"w-{track_id}-{i}", "kind": "word", "title": en,
             "ask": WORD_FRAME[lang].format(en=en, target=word), "ask_roman": "", "ask_en": "",
             "target": word, "target_roman": roman, "target_en": en}
            for i, (word, roman, en) in enumerate(items)
        ]})
    return out


def word_items(lang: str) -> list:
    return [item for track in tracks(lang) for item in track["items"]]


def target_words(text: str) -> list:
    return re.sub(r"[,।?!.]", " ", text).split()


def line_text(lang: str, key: str, lessons=None, rel_id=None) -> str:
    """Resolve a line key to its fixed text. Unknown keys fail.

    shared:x, praise:n, encourage:n, ask:id (coach framing), q:id (pretend call), model:id,
    slow:id, word:id:n (one word, slowly), find:id (toddler game), en:id (English help).
    """
    content = localize(lang, rel_id)
    lessons = lessons if lessons is not None else content["lessons"] + content["call_extras"]
    kind, _, name = key.partition(":")
    if kind == "shared":
        return content["shared"][name]
    if kind in ("praise", "encourage"):
        return content[kind][int(name)]
    if kind == "word":
        lesson_id, _, index = name.rpartition(":")
        lesson = next(item for item in lessons if item["id"] == lesson_id)
        return "<slow> " + target_words(lesson["target"])[int(index)]
    lesson = next(item for item in lessons if item["id"] == name)
    if kind == "ask":
        if lesson.get("kind") == "word":
            return lesson["ask"]
        return content["ask_frame"].replace("{ask}", lesson["ask"])
    if kind == "q":
        return lesson["ask"]
    if kind == "model":
        return content["model_prefix"] + lesson["target"]
    if kind == "slow":
        return "<slow> " + lesson["target"]
    if kind == "find":
        return FIND_FRAME[lang].format(word=lesson["target"])
    if kind == "en":
        return lesson.get("ask_en") or lesson.get("target_en") or ""
    raise KeyError(key)


def all_keys(lang: str, lessons=None, rel_id=None) -> list:
    """Lines made ahead of time. Word, slow, find and English lines are made only when needed."""
    content = localize(lang, rel_id)
    lessons = lessons if lessons is not None else content["lessons"]
    keys = [f"shared:{name}" for name in content["shared"]]
    keys += [f"praise:{i}" for i in range(len(content["praise"]))]
    keys += [f"encourage:{i}" for i in range(len(content["encourage"]))]
    for lesson in lessons:
        keys += [f"ask:{lesson['id']}", f"q:{lesson['id']}", f"model:{lesson['id']}"]
    for extra in content["call_extras"]:
        keys += [f"q:{extra['id']}", f"model:{extra['id']}"]
    return keys
