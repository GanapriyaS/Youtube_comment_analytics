from googletrans import Translator


# text = 'seekiram sollu'
# text = 'neenga sanda podum pothum nee alaga irukinga'
# text = 'video massunga epidi shot pannuringa'
# text = 'enga vitulayum same samayal tha'
# text='padal varigal nalla iruku'
text="I've good"
# text='naan tha unga first viewer'
# text='ella videos vida unga video nalla iruku'
# text="sir kabhi start hoga"
# text="ellarukum oru, seat mathi"
# text="ohaiyo"
# text="ஊட்டி  மற்ற எல்லா இடங்களையும்  விட romba chill பகுதியாகும்"
# text="बच्चे TV देख रहे हैं"
# Detecting the language

def translate(text):
    translator = Translator()
    print(translator.detect(text))
    result = translator.translate(text).text


    possesions = {
        "aren't" : "are not",
        "can't" : "cannot",
        "couldn't" : "could not",
        "didn't" : "did not",
        "doesn't" : "does not",
        "don't": "do not",
        "hadn't" : "had not",
        "hasn't" : "has not",
        "haven't" : "have not",
        "he'd" : "he would",
        "he'll" : "he will",
        "he's" : "he is",
        "i'd" : "I would",
        "i'll" : "I will",
        "i'm" : "I am",
        "isn't" : "is not",
        "it's" : "it is",
        "it'll":"it will",
        "i've" : "I have",
        "let's" : "let us",
        "mightn't" : "might not",
        "mustn't" : "must not",
        "shan't" : "shall not",
        "she'd" : "she would",
        "she'll" : "she will",
        "she's" : "she is",
        "shouldn't" : "should not",
        "should've" : "should have",
        "that's" : "that is",
        "there's" : "there is",
        "they'd" : "they would",
        "they'll" : "they will",
        "they're" : "they are",
        "they've" : "they have",
        "we'd" : "we would",
        "we're" : "we are",
        "weren't" : "were not",
        "we've" : "we have",
        "what'll" : "what will",
        "what're" : "what are",
        "what's" : "what is",
        "what've" : "what have",
        "where's" : "where is",
        "who'd" : "who would",
        "who'll" : "who will",
        "who're" : "who are",
        "who's" : "who is",
        "who've" : "who have",
        "I've":"I have",
        "won't" : "will not",
        "wouldn't" : "would not",
        "would've" : "would have",
        "you'd" : "you would",
        "you'll" : "you will",
        "you're" : "you are",
        "you've" : "you have",
        "'re": " are",
        "wasn't": "was not",
        "we'll":" will",
        "must've": "must have",
        "y'all": "you all",
        "it'd ": "it would",
        "ain't": "is not",
        "ROFL":"Rolling on the floor laughing",
        "STFU":"Shut the freak up",
        "LMK":"Let me know",
        "ILY":"I love you",
        "YOLO":"You only live once",
        "SMH":"Shaking my head",
        "LMFAO":"Laughing my freaking ass off",
       "NVM":"Never mind",
        "IKR":"I know, right",
        "OFC":"Of course",
        "LOL":"Laughing Out Loud",
        "BRB":"Be Right Back",
        "BBL":"Be Back Later",
        "ASAP":"As Soon As Possible",
        "B4":"Before",
        "B4N":"Bye For Now",
        "BTW":"By The Way",
        "B/C":"Because",
        "C U L8R":"See You Later",
        "Def":"Definitely",
        "tmrw":"Tomorrow",
        "ETA":"Estimated Time of Arrival",
        "F2F":"Face To Face",
        "GF":"Girlfriend",
        "BF":"Boyfriend",
        "BFF":"Best Friend Forever",
        "AML":"All My Love",
        "G2G":"Got To Go",
        "GTG":"Got To Go",
        "GR8":"Great",
        "IDK":"I Don’t Know",
        "IDC":"I Don’t Care",
        "JK":"Just Kidding",
        "K":"OK",
        "THX":"Thanks",
        "PLS":"Please",
        "TTYL":"Talk To You Later",
        "TMI":"Too Much Information",
        "CYE":"Check Your Email",
        "FYI":"For Your Information",
        "IMHO":"In My Honest Opinion",
        "BION":"Believe It Or Not",
        "BRT":"Be Right There",
        "Y":"Why?",
        "PCM":"Please Call Me",
        "IYKWIM":"If You Know What I Mean",
        "WYSIWYG":"What You See Is What You Get",
        "XOXO":"Hugs and Kisses",
        "4U":"I have a question for you",
        "<3":"Love/friendship",
        "121":"One to one",
        "2":"To",
        "2EZ":"Too easy",
        "2F4U":"Too fast for you",
        "2G2BT":"Too good to be true",
        "2M2H":"Too much to handle",
        "2NITE":"Tonight",
        "4":"For",
        "8L3W":"Eight letters, three words (I love you)",
        "ABT":"About",
        "ADDY":"Address",
        "ADMIN":"Administrator",
        "AKA":"Also known as",
        "ALOL":"Actually laughing out loud",
        "APP":"Application",
        "ASAP":"As soon as possible",
        "B2W":"Back to work",
        "B4":"Before",
        "BAE":"baby",
        "BAK":"Back at keyboard",
        "BAU":"Business as usual",
        "BBL":"Be back later",
        "BBS":"Be back soon",
        "BC":"Because",
        "BCNU":"Be seeing you",
        "BD":"Big deal",
        "BDAY":"Birthday",
        "BFF":"Best friends forever",
        "BFD":"Big freaking deal",
        "BFN":"Bye for now",
        "BIF":"Before I forget",
        "BLNT":"Better luck next time",
        "BOL":"Best of luck",
        "BR":"Best regards",
        "BRT":"Be right there",
        "BTDT":"Been there, done that",
        "BTW":"By the way",
        "BYOB":"Bring your own beer",
        "BYOC":"Bring your own computer",
        "BYOD":"Bring your own device",
        "BYTM":"Better you than me",
        "CHK":"Check",
        "CID":"Consider it done",
        "CLD":"Could",
        "CLK":"Click",
        "CMON":"Come on",
        "COB":"Close of business",
        "CRAY":"Crazy",
        "CRE8":"Create",
        "CU":"See you",
        "DBEYR":"Don’t believe everything you read",
       "DERP":"Meaning stupid or silly",
        "DGT":"Don’t go there",
        "DIY":"Do it yourself",
        "DKDC":"Don’t know, don’t care",
        "DL":"Download",
        "DM":"Direct message",
        "DQMOT":"Don’t quote me on this",
        "DUPE":"Duplicate",
        "EAK":"Eating at keyboard",
        "EOBD":"End of business day",
        "EOD":"End of day",
        "EOM":"End of message",
        "ETA":"Estimated time of arrival",
        "EZ":"Easy",
        "F2F":"Face to face",
        "FAQ":"Frequently asked questions",
        "FB":"Facebook",
        "FBM":"Fine by me",
        "FBOW":"For better or worse",
        "FF":"Follow Friday",
        "FIMH":"Forever in my heart",
        "FOAF":"Friend of a friend",
        "FOMO":"Fear of missing out",
        "FRT":"For real though",
        "FTBOMH":"From the bottom of my heart",
        F"TL":"For the loss",
        "FTW":"For the win",
        "FWB":"Friend with benefits",
        "FWIW":"For what it’s worth",
        "FWM":"Fine with me",
       " FYA":"For your amusement",
        "FYEO":"For your eyes only",
        "4YEO":"For your eyes only",
        "FYI":"For your information",
        "G2CU":"Good to see you",
        "GB":"Goodbye",
        "GB2W":"Get back to work",
        "GD":"Good",
        "GFI":"Go for it",
        "GL":"Good luck",
        "GOI":"Get over it",
        "GR8":"Great",
        "GRATZ":"Congratulations",
        "H8":"Hate",
        "143":"I love you",
        "n8":"night",
        "w8":"what",
        "msg":"message",
        "u":"you",
        "b/w":"between",
        "lyk":"like",
        "luv":"love",
        "bro":"brother",
        "sis":"sister",
        "nyc":"nice",
        "gm":"good morning",
        "gn":"good night",
        "sd":"sweet dreams",
        "tc":"take care",
        "4ever":"forever",
        "tq":"thank you",
        "wp":"whatsapp",
        "fb":"facebook",
        "wth":"what the hell",
        "wtf":"what the fuck",
        "Utube":"Youtube",
        "ig":"instagram",
        "info":"information",
        "govt":"government",
        "clg":"college",
        "scl":"school",
        "hbd":"happy birthday",
        "R":"are",
        "cum":"come",
        "bcoz":"because",
        "bc":"busy",
        "eve":"evening",
       "s":"yes",
        "2day":"today",
        "ss":"screenshot",
        "wat":"what",
        "whr":"where",
        "Yday":"Yesterday",
        "Ur":"your",
        "frnd":"friend",
        "loml":"love of my life",
       "ttys":"Talk To You soon",
        "tqsm":"thank you so much",
        "omg":"oh my god",
        "osm":"owesome",
        
    }
    result = " ".join(possesions.get(ele, ele) for ele in result.split())
    return result

