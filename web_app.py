import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

STOCKS = [
    {"ticker": "AAPL", "name": "Apple Inc.", "momentum": 82.5, "valuation": 28.8, "sentiment": 60.8, "score": 58.8, "pe_ratio": 28.5, "headlines": [
        {"title": "Apple announces new AI features for iPhone", "url": "https://news.google.com/search?q=Apple+announces+new+AI+features+for+iPhone"},
        {"title": "Apple stock hits record high amid strong earnings", "url": "https://news.google.com/search?q=Apple+stock+hits+record+high+amid+strong+earnings"},
        {"title": "Apple expands services business", "url": "https://news.google.com/search?q=Apple+expands+services+business"},
        {"title": "Apple patent granted for new display technology", "url": "https://news.google.com/search?q=Apple+patent+granted+for+new+display+technology"}
    ]},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "momentum": 84.0, "valuation": 0.0, "sentiment": 49.7, "score": 46.8, "pe_ratio": 52.4, "headlines": [
        {"title": "NVIDIA reports record GPU demand", "url": "https://news.google.com/search?q=NVIDIA+reports+record+GPU+demand"},
        {"title": "NVIDIA launches next-gen AI chips", "url": "https://news.google.com/search?q=NVIDIA+launches+next-gen+AI+chips"},
        {"title": "NVIDIA stock rallies on AI boom", "url": "https://news.google.com/search?q=NVIDIA+stock+rallies+on+AI+boom"},
        {"title": "NVIDIA expands data center business", "url": "https://news.google.com/search?q=NVIDIA+expands+data+center+business"}
    ]},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "momentum": 69.4, "valuation": 0.0, "sentiment": 63.1, "score": 46.4, "pe_ratio": 42.6, "headlines": [
        {"title": "Amazon Q3 revenue beats expectations", "url": "https://news.google.com/search?q=Amazon+Q3+revenue+beats+expectations"},
        {"title": "Amazon Web Services continues growth", "url": "https://news.google.com/search?q=Amazon+Web+Services+continues+growth"},
        {"title": "Amazon invests in AI startups", "url": "https://news.google.com/search?q=Amazon+invests+in+AI+startups"},
        {"title": "Amazon announces new logistics initiative", "url": "https://news.google.com/search?q=Amazon+announces+new+logistics+initiative"}
    ]},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "momentum": 32.5, "valuation": 19.7, "sentiment": 58.9, "score": 37.9, "pe_ratio": 32.1, "headlines": [
        {"title": "Microsoft reports strong cloud growth", "url": "https://news.google.com/search?q=Microsoft+reports+strong+cloud+growth"},
        {"title": "Microsoft Copilot integration drives adoption", "url": "https://news.google.com/search?q=Microsoft+Copilot+integration+drives+adoption"},
        {"title": "Microsoft partners with OpenAI for AI expansion", "url": "https://news.google.com/search?q=Microsoft+partners+with+OpenAI+for+AI+expansion"},
        {"title": "Microsoft beats earnings expectations", "url": "https://news.google.com/search?q=Microsoft+beats+earnings+expectations"}
    ]},
    {"ticker": "TSLA", "name": "Tesla Inc.", "momentum": 42.0, "valuation": 0.0, "sentiment": 46.3, "score": 30.9, "pe_ratio": 65.3, "headlines": [
        {"title": "Tesla launches new Roadster model", "url": "https://news.google.com/search?q=Tesla+launches+new+Roadster+model"},
        {"title": "Tesla opens new Gigafactory", "url": "https://news.google.com/search?q=Tesla+opens+new+Gigafactory"},
        {"title": "Tesla stock surges on delivery numbers", "url": "https://news.google.com/search?q=Tesla+stock+surges+on+delivery+numbers"},
        {"title": "Tesla announces price cuts", "url": "https://news.google.com/search?q=Tesla+announces+price+cuts"}
    ]},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "momentum": 75.3, "valuation": 25.4, "sentiment": 62.1, "score": 55.2, "pe_ratio": 26.8, "headlines": [
        {"title": "Google announces new AI search features", "url": "https://news.google.com/search?q=Google+announces+new+AI+search+features"},
        {"title": "Alphabet revenue beats analyst expectations", "url": "https://news.google.com/search?q=Alphabet+revenue+beats+analyst+expectations"},
        {"title": "Google expands cloud infrastructure", "url": "https://news.google.com/search?q=Google+expands+cloud+infrastructure"},
        {"title": "Google DeepMind makes breakthrough in AI", "url": "https://news.google.com/search?q=Google+DeepMind+makes+breakthrough+in+AI"}
    ]},
    {"ticker": "META", "name": "Meta Platforms", "momentum": 68.9, "valuation": 21.6, "sentiment": 55.3, "score": 48.3, "pe_ratio": 24.2, "headlines": [
        {"title": "Meta reports strong Q3 advertising revenue", "url": "https://news.google.com/search?q=Meta+reports+strong+Q3+advertising+revenue"},
        {"title": "Meta's AI investments pay off", "url": "https://news.google.com/search?q=Meta's+AI+investments+pay+off"},
        {"title": "Facebook user growth accelerates", "url": "https://news.google.com/search?q=Facebook+user+growth+accelerates"},
        {"title": "Meta Quest VR headset sales surge", "url": "https://news.google.com/search?q=Meta+Quest+VR+headset+sales+surge"}
    ]},
    {"ticker": "NFLX", "name": "Netflix Inc.", "momentum": 71.2, "valuation": 18.9, "sentiment": 58.7, "score": 49.6, "pe_ratio": 29.1, "headlines": [
        {"title": "Netflix subscriber count reaches new high", "url": "https://news.google.com/search?q=Netflix+subscriber+count+reaches+new+high"},
        {"title": "Netflix password sharing crackdown succeeds", "url": "https://news.google.com/search?q=Netflix+password+sharing+crackdown+succeeds"},
        {"title": "Netflix expands gaming platform", "url": "https://news.google.com/search?q=Netflix+expands+gaming+platform"},
        {"title": "Netflix stock rallies on strong guidance", "url": "https://news.google.com/search?q=Netflix+stock+rallies+on+strong+guidance"}
    ]},
    {"ticker": "ADOBE", "name": "Adobe Inc.", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Adobe launches generative AI features", "url": "https://news.google.com/search?q=Adobe+launches+generative+AI+features"},
        {"title": "Creative Cloud subscriptions surge", "url": "https://news.google.com/search?q=Creative+Cloud+subscriptions+surge"},
        {"title": "Adobe beats Q3 expectations", "url": "https://news.google.com/search?q=Adobe+beats+Q3+expectations"},
        {"title": "Adobe acquires new AI startup", "url": "https://news.google.com/search?q=Adobe+acquires+new+AI+startup"}
    ]},
    {"ticker": "TSMC", "name": "Taiwan Semiconductor", "momentum": 79.5, "valuation": 24.7, "sentiment": 61.2, "score": 55.1, "pe_ratio": 15.3, "headlines": [
        {"title": "TSMC reports record chip demand", "url": "https://news.google.com/search?q=TSMC+reports+record+chip+demand"},
        {"title": "TSMC expands US manufacturing", "url": "https://news.google.com/search?q=TSMC+expands+US+manufacturing"},
        {"title": "TSMC secures long-term contracts", "url": "https://news.google.com/search?q=TSMC+secures+long-term+contracts"},
        {"title": "TSMC invests in advanced packaging", "url": "https://news.google.com/search?q=TSMC+invests+in+advanced+packaging"}
    ]},
    {"ticker": "JPM", "name": "JPMorgan Chase", "momentum": 58.3, "valuation": 35.2, "sentiment": 52.1, "score": 48.5, "pe_ratio": 12.8, "headlines": [
        {"title": "JPMorgan reports strong Q3 results", "url": "https://news.google.com/search?q=JPMorgan+reports+strong+Q3+results"},
        {"title": "JPMorgan expands investment banking", "url": "https://news.google.com/search?q=JPMorgan+expands+investment+banking"},
        {"title": "JPMorgan digital banking adoption grows", "url": "https://news.google.com/search?q=JPMorgan+digital+banking+adoption+grows"},
        {"title": "JPMorgan raises economic growth forecast", "url": "https://news.google.com/search?q=JPMorgan+raises+economic+growth+forecast"}
    ]},
    {"ticker": "BAC", "name": "Bank of America", "momentum": 52.1, "valuation": 38.9, "sentiment": 48.3, "score": 46.4, "pe_ratio": 10.2, "headlines": [
        {"title": "Bank of America Q3 earnings beat", "url": "https://news.google.com/search?q=Bank+of+America+Q3+earnings+beat"},
        {"title": "BofA wealth management grows", "url": "https://news.google.com/search?q=BofA+wealth+management+grows"},
        {"title": "Bank of America digital services expand", "url": "https://news.google.com/search?q=Bank+of+America+digital+services+expand"},
        {"title": "BofA improves credit quality", "url": "https://news.google.com/search?q=BofA+improves+credit+quality"}
    ]},
    {"ticker": "WFC", "name": "Wells Fargo", "momentum": 45.7, "valuation": 32.1, "sentiment": 45.6, "score": 41.1, "pe_ratio": 11.5, "headlines": [
        {"title": "Wells Fargo reports steady Q3 results", "url": "https://news.google.com/search?q=Wells+Fargo+reports+steady+Q3+results"},
        {"title": "Wells Fargo settlement discussions continue", "url": "https://news.google.com/search?q=Wells+Fargo+settlement+discussions+continue"},
        {"title": "Wells Fargo strengthens risk management", "url": "https://news.google.com/search?q=Wells+Fargo+strengthens+risk+management"},
        {"title": "Wells Fargo mortgage business stabilizes", "url": "https://news.google.com/search?q=Wells+Fargo+mortgage+business+stabilizes"}
    ]},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "momentum": 48.9, "valuation": 45.2, "sentiment": 55.3, "score": 49.8, "pe_ratio": 17.2, "headlines": [
        {"title": "J&J receives FDA approval for new drug", "url": "https://news.google.com/search?q=J&J+receives+FDA+approval+for+new+drug"},
        {"title": "Johnson & Johnson Q3 sales grow", "url": "https://news.google.com/search?q=Johnson+&+Johnson+Q3+sales+grow"},
        {"title": "J&J cancer drug shows promise", "url": "https://news.google.com/search?q=J&J+cancer+drug+shows+promise"},
        {"title": "Johnson & Johnson raises dividend", "url": "https://news.google.com/search?q=Johnson+&+Johnson+raises+dividend"}
    ]},
    {"ticker": "UNH", "name": "UnitedHealth Group", "momentum": 72.3, "valuation": 41.8, "sentiment": 57.6, "score": 57.2, "pe_ratio": 19.3, "headlines": [
        {"title": "UnitedHealth Q3 earnings beat forecasts", "url": "https://news.google.com/search?q=UnitedHealth+Q3+earnings+beat+forecasts"},
        {"title": "UnitedHealth acquires healthcare IT firm", "url": "https://news.google.com/search?q=UnitedHealth+acquires+healthcare+IT+firm"},
        {"title": "Optum continues rapid expansion", "url": "https://news.google.com/search?q=Optum+continues+rapid+expansion"},
        {"title": "UnitedHealth raises 2024 guidance", "url": "https://news.google.com/search?q=UnitedHealth+raises+2024+guidance"}
    ]},
    {"ticker": "PFE", "name": "Pfizer Inc.", "momentum": 35.2, "valuation": 48.1, "sentiment": 52.1, "score": 45.1, "pe_ratio": 13.8, "headlines": [
        {"title": "Pfizer reports Q3 vaccine sales surge", "url": "https://news.google.com/search?q=Pfizer+reports+Q3+vaccine+sales+surge"},
        {"title": "Pfizer completes COVID pill acquisition", "url": "https://news.google.com/search?q=Pfizer+completes+COVID+pill+acquisition"},
        {"title": "Pfizer pipeline advances key programs", "url": "https://news.google.com/search?q=Pfizer+pipeline+advances+key+programs"},
        {"title": "Pfizer stock strengthens on earnings", "url": "https://news.google.com/search?q=Pfizer+stock+strengthens+on+earnings"}
    ]},
    {"ticker": "WMT", "name": "Walmart Inc.", "momentum": 61.2, "valuation": 52.3, "sentiment": 58.9, "score": 57.4, "pe_ratio": 24.1, "headlines": [
        {"title": "Walmart Q3 sales exceed expectations", "url": "https://news.google.com/search?q=Walmart+Q3+sales+exceed+expectations"},
        {"title": "Walmart grocery e-commerce accelerates", "url": "https://news.google.com/search?q=Walmart+grocery+e-commerce+accelerates"},
        {"title": "Walmart+ membership grows significantly", "url": "https://news.google.com/search?q=Walmart++membership+grows+significantly"},
        {"title": "Walmart raises full-year guidance", "url": "https://news.google.com/search?q=Walmart+raises+full-year+guidance"}
    ]},
    {"ticker": "COST", "name": "Costco Wholesale", "momentum": 65.8, "valuation": 48.2, "sentiment": 61.3, "score": 58.4, "pe_ratio": 41.2, "headlines": [
        {"title": "Costco membership fees increase", "url": "https://news.google.com/search?q=Costco+membership+fees+increase"},
        {"title": "Costco comparable sales grow double digits", "url": "https://news.google.com/search?q=Costco+comparable+sales+grow+double+digits"},
        {"title": "Costco online business booming", "url": "https://news.google.com/search?q=Costco+online+business+booming"},
        {"title": "Costco stock hits record high", "url": "https://news.google.com/search?q=Costco+stock+hits+record+high"}
    ]},
    {"ticker": "MCD", "name": "McDonald's", "momentum": 55.3, "valuation": 49.8, "sentiment": 56.7, "score": 53.9, "pe_ratio": 26.4, "headlines": [
        {"title": "McDonald's Q3 revenue beats forecasts", "url": "https://news.google.com/search?q=McDonald's+Q3+revenue+beats+forecasts"},
        {"title": "McDonald's international growth accelerates", "url": "https://news.google.com/search?q=McDonald's+international+growth+accelerates"},
        {"title": "McDonald's AI drive-thru rollout expands", "url": "https://news.google.com/search?q=McDonald's+AI+drive-thru+rollout+expands"},
        {"title": "McDonald's stock rallies on guidance", "url": "https://news.google.com/search?q=McDonald's+stock+rallies+on+guidance"}
    ]},
    {"ticker": "SBUX", "name": "Starbucks", "momentum": 42.1, "valuation": 35.6, "sentiment": 54.2, "score": 44.0, "pe_ratio": 28.7, "headlines": [
        {"title": "Starbucks reports Q3 comparable sales growth", "url": "https://news.google.com/search?q=Starbucks+reports+Q3+comparable+sales+growth"},
        {"title": "Starbucks new CEO outlines strategy", "url": "https://news.google.com/search?q=Starbucks+new+CEO+outlines+strategy"},
        {"title": "Starbucks loyalty program expands", "url": "https://news.google.com/search?q=Starbucks+loyalty+program+expands"},
        {"title": "Starbucks opens new stores globally", "url": "https://news.google.com/search?q=Starbucks+opens+new+stores+globally"}
    ]},
    {"ticker": "XOM", "name": "Exxon Mobil", "momentum": 58.9, "valuation": 55.2, "sentiment": 48.3, "score": 53.8, "pe_ratio": 8.9, "headlines": [
        {"title": "ExxonMobil Q3 profits surge on oil prices", "url": "https://news.google.com/search?q=ExxonMobil+Q3+profits+surge+on+oil+prices"},
        {"title": "ExxonMobil invests in low-carbon energy", "url": "https://news.google.com/search?q=ExxonMobil+invests+in+low-carbon+energy"},
        {"title": "ExxonMobil Guyana production ramps up", "url": "https://news.google.com/search?q=ExxonMobil+Guyana+production+ramps+up"},
        {"title": "ExxonMobil dividend increase announced", "url": "https://news.google.com/search?q=ExxonMobil+dividend+increase+announced"}
    ]},
    {"ticker": "CVX", "name": "Chevron", "momentum": 62.1, "valuation": 58.3, "sentiment": 51.2, "score": 57.2, "pe_ratio": 9.2, "headlines": [
        {"title": "Chevron Q3 earnings beat estimates", "url": "https://news.google.com/search?q=Chevron+Q3+earnings+beat+estimates"},
        {"title": "Chevron benefits from energy transition", "url": "https://news.google.com/search?q=Chevron+benefits+from+energy+transition"},
        {"title": "Chevron production increases this quarter", "url": "https://news.google.com/search?q=Chevron+production+increases+this+quarter"},
        {"title": "Chevron raises shareholder return plan", "url": "https://news.google.com/search?q=Chevron+raises+shareholder+return+plan"}
    ]},
    {"ticker": "BA", "name": "Boeing", "momentum": 38.2, "valuation": 28.9, "sentiment": 42.1, "score": 36.4, "pe_ratio": 42.3, "headlines": [
        {"title": "Boeing reports Q3 defense contracts", "url": "https://news.google.com/search?q=Boeing+reports+Q3+defense+contracts"},
        {"title": "Boeing 737 Max deliveries ramp up", "url": "https://news.google.com/search?q=Boeing+737+Max+deliveries+ramp+up"},
        {"title": "Boeing space business accelerates", "url": "https://news.google.com/search?q=Boeing+space+business+accelerates"},
        {"title": "Boeing stock gains on production increases", "url": "https://news.google.com/search?q=Boeing+stock+gains+on+production+increases"}
    ]},
    {"ticker": "CAT", "name": "Caterpillar", "momentum": 64.5, "valuation": 38.7, "sentiment": 52.3, "score": 51.8, "pe_ratio": 12.6, "headlines": [
        {"title": "Caterpillar Q3 sales exceed forecasts", "url": "https://news.google.com/search?q=Caterpillar+Q3+sales+exceed+forecasts"},
        {"title": "Caterpillar equipment demand remains strong", "url": "https://news.google.com/search?q=Caterpillar+equipment+demand+remains+strong"},
        {"title": "Caterpillar services business grows", "url": "https://news.google.com/search?q=Caterpillar+services+business+grows"},
        {"title": "Caterpillar raises annual guidance", "url": "https://news.google.com/search?q=Caterpillar+raises+annual+guidance"}
    ]},
    {"ticker": "GE", "name": "General Electric", "momentum": 52.3, "valuation": 32.1, "sentiment": 48.9, "score": 44.4, "pe_ratio": 18.3, "headlines": [
        {"title": "GE reports Q3 earnings beat", "url": "https://news.google.com/search?q=GE+reports+Q3+earnings+beat"},
        {"title": "GE renewable energy business booms", "url": "https://news.google.com/search?q=GE+renewable+energy+business+booms"},
        {"title": "GE aviation orders strengthen", "url": "https://news.google.com/search?q=GE+aviation+orders+strengthen"},
        {"title": "GE stock gains on outlook improvement", "url": "https://news.google.com/search?q=GE+stock+gains+on+outlook+improvement"}
    ]},
    {"ticker": "V", "name": "Visa Inc.", "momentum": 71.8, "valuation": 42.3, "sentiment": 59.2, "score": 57.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Visa Q3 payment volume surges", "url": "https://news.google.com/search?q=Visa+Q3+payment+volume+surges"},
        {"title": "Visa expands digital payments platform", "url": "https://news.google.com/search?q=Visa+expands+digital+payments+platform"},
        {"title": "Visa cryptocurrency partnerships grow", "url": "https://news.google.com/search?q=Visa+cryptocurrency+partnerships+grow"},
        {"title": "Visa raises quarterly dividend", "url": "https://news.google.com/search?q=Visa+raises+quarterly+dividend"}
    ]},
    {"ticker": "MA", "name": "Mastercard", "momentum": 73.2, "valuation": 39.8, "sentiment": 61.1, "score": 58.0, "pe_ratio": 40.2, "headlines": [
        {"title": "Mastercard Q3 results exceed expectations", "url": "https://news.google.com/search?q=Mastercard+Q3+results+exceed+expectations"},
        {"title": "Mastercard contactless payments surge", "url": "https://news.google.com/search?q=Mastercard+contactless+payments+surge"},
        {"title": "Mastercard AI fraud detection improves", "url": "https://news.google.com/search?q=Mastercard+AI+fraud+detection+improves"},
        {"title": "Mastercard stock rallies on growth", "url": "https://news.google.com/search?q=Mastercard+stock+rallies+on+growth"}
    ]},
    {"ticker": "PYPL", "name": "PayPal", "momentum": 48.9, "valuation": 28.3, "sentiment": 50.6, "score": 42.6, "pe_ratio": 32.1, "headlines": [
        {"title": "PayPal Q3 earnings top forecasts", "url": "https://news.google.com/search?q=PayPal+Q3+earnings+top+forecasts"},
        {"title": "PayPal blockchain integration expands", "url": "https://news.google.com/search?q=PayPal+blockchain+integration+expands"},
        {"title": "PayPal user growth accelerates", "url": "https://news.google.com/search?q=PayPal+user+growth+accelerates"},
        {"title": "PayPal gross payment volume increases", "url": "https://news.google.com/search?q=PayPal+gross+payment+volume+increases"}
    ]},
    {"ticker": "INTC", "name": "Intel", "momentum": 35.6, "valuation": 18.9, "sentiment": 43.2, "score": 32.6, "pe_ratio": 11.4, "headlines": [
        {"title": "Intel reports Q3 results amid recovery", "url": "https://news.google.com/search?q=Intel+reports+Q3+results+amid+recovery"},
        {"title": "Intel new chip architecture impresses", "url": "https://news.google.com/search?q=Intel+new+chip+architecture+impresses"},
        {"title": "Intel foundry services gain momentum", "url": "https://news.google.com/search?q=Intel+foundry+services+gain+momentum"},
        {"title": "Intel stock bounces on strategy update", "url": "https://news.google.com/search?q=Intel+stock+bounces+on+strategy+update"}
    ]},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "momentum": 68.3, "valuation": 21.2, "sentiment": 54.8, "score": 48.1, "pe_ratio": 29.3, "headlines": [
        {"title": "AMD Q3 sales beat analyst estimates", "url": "https://news.google.com/search?q=AMD+Q3+sales+beat+analyst+estimates"},
        {"title": "AMD data center growth accelerates", "url": "https://news.google.com/search?q=AMD+data+center+growth+accelerates"},
        {"title": "AMD AI chip demand surges", "url": "https://news.google.com/search?q=AMD+AI+chip+demand+surges"},
        {"title": "AMD stock reaches new high", "url": "https://news.google.com/search?q=AMD+stock+reaches+new+high"}
    ]},
    {"ticker": "QCOM", "name": "Qualcomm", "momentum": 62.1, "valuation": 24.7, "sentiment": 52.3, "score": 46.3, "pe_ratio": 17.8, "headlines": [
        {"title": "Qualcomm Q3 earnings beat forecasts", "url": "https://news.google.com/search?q=Qualcomm+Q3+earnings+beat+forecasts"},
        {"title": "Qualcomm 5G chip demand remains robust", "url": "https://news.google.com/search?q=Qualcomm+5G+chip+demand+remains+robust"},
        {"title": "Qualcomm automotive business grows", "url": "https://news.google.com/search?q=Qualcomm+automotive+business+grows"},
        {"title": "Qualcomm raises annual guidance", "url": "https://news.google.com/search?q=Qualcomm+raises+annual+guidance"}
    ]},
    {"ticker": "CSCO", "name": "Cisco Systems", "momentum": 41.2, "valuation": 32.8, "sentiment": 49.1, "score": 41.0, "pe_ratio": 18.9, "headlines": [
        {"title": "Cisco Q3 results meet expectations", "url": "https://news.google.com/search?q=Cisco+Q3+results+meet+expectations"},
        {"title": "Cisco software subscription business grows", "url": "https://news.google.com/search?q=Cisco+software+subscription+business+grows"},
        {"title": "Cisco cloud strategy gaining traction", "url": "https://news.google.com/search?q=Cisco+cloud+strategy+gaining+traction"},
        {"title": "Cisco security solutions in demand", "url": "https://news.google.com/search?q=Cisco+security+solutions+in+demand"}
    ]},
    {"ticker": "CRM", "name": "Salesforce", "momentum": 55.3, "valuation": 29.7, "sentiment": 56.2, "score": 47.0, "pe_ratio": 51.3, "headlines": [
        {"title": "Salesforce Q3 revenue grows 11%", "url": "https://news.google.com/search?q=Salesforce+Q3+revenue+grows+11%"},
        {"title": "Salesforce Einstein AI adoption surges", "url": "https://news.google.com/search?q=Salesforce+Einstein+AI+adoption+surges"},
        {"title": "Salesforce enterprise deals expand", "url": "https://news.google.com/search?q=Salesforce+enterprise+deals+expand"},
        {"title": "Salesforce stock rallies on results", "url": "https://news.google.com/search?q=Salesforce+stock+rallies+on+results"}
    ]},
    {"ticker": "ORCL", "name": "Oracle", "momentum": 58.9, "valuation": 35.2, "sentiment": 53.1, "score": 49.0, "pe_ratio": 19.2, "headlines": [
        {"title": "Oracle Q3 cloud revenue beats estimates", "url": "https://news.google.com/search?q=Oracle+Q3+cloud+revenue+beats+estimates"},
        {"title": "Oracle database business remains strong", "url": "https://news.google.com/search?q=Oracle+database+business+remains+strong"},
        {"title": "Oracle AI initiatives accelerate", "url": "https://news.google.com/search?q=Oracle+AI+initiatives+accelerate"},
        {"title": "Oracle stock gains on cloud growth", "url": "https://news.google.com/search?q=Oracle+stock+gains+on+cloud+growth"}
    ]},
    {"ticker": "IBM", "name": "IBM", "momentum": 39.2, "valuation": 41.3, "sentiment": 48.7, "score": 43.0, "pe_ratio": 16.1, "headlines": [
        {"title": "IBM Q3 earnings top expectations", "url": "https://news.google.com/search?q=IBM+Q3+earnings+top+expectations"},
        {"title": "IBM quantum computing advances", "url": "https://news.google.com/search?q=IBM+quantum+computing+advances"},
        {"title": "IBM cloud infrastructure grows", "url": "https://news.google.com/search?q=IBM+cloud+infrastructure+grows"},
        {"title": "IBM stock rebounds on guidance", "url": "https://news.google.com/search?q=IBM+stock+rebounds+on+guidance"}
    ]},
    {"ticker": "TGT", "name": "Target", "momentum": 52.1, "valuation": 42.8, "sentiment": 54.1, "score": 49.6, "pe_ratio": 18.7, "headlines": [
        {"title": "Target Q3 comparable sales grow", "url": "https://news.google.com/search?q=Target+Q3+comparable+sales+grow"},
        {"title": "Target same-day services expand", "url": "https://news.google.com/search?q=Target+same-day+services+expand"},
        {"title": "Target digital sales accelerate", "url": "https://news.google.com/search?q=Target+digital+sales+accelerate"},
        {"title": "Target stock gains on holiday outlook", "url": "https://news.google.com/search?q=Target+stock+gains+on+holiday+outlook"}
    ]},
    {"ticker": "HD", "name": "The Home Depot", "momentum": 48.3, "valuation": 38.9, "sentiment": 51.2, "score": 46.1, "pe_ratio": 22.3, "headlines": [
        {"title": "Home Depot Q3 sales beat forecasts", "url": "https://news.google.com/search?q=Home+Depot+Q3+sales+beat+forecasts"},
        {"title": "Home Depot pro customer growth strong", "url": "https://news.google.com/search?q=Home+Depot+pro+customer+growth+strong"},
        {"title": "Home Depot digital tools expand", "url": "https://news.google.com/search?q=Home+Depot+digital+tools+expand"},
        {"title": "Home Depot stock rallies on results", "url": "https://news.google.com/search?q=Home+Depot+stock+rallies+on+results"}
    ]},
    {"ticker": "LOWE", "name": "Lowe's", "momentum": 45.7, "valuation": 35.2, "sentiment": 49.8, "score": 43.5, "pe_ratio": 19.8, "headlines": [
        {"title": "Lowe's Q3 comparable sales grow", "url": "https://news.google.com/search?q=Lowe's+Q3+comparable+sales+grow"},
        {"title": "Lowe's online business accelerates", "url": "https://news.google.com/search?q=Lowe's+online+business+accelerates"},
        {"title": "Lowe's DIY customer base expands", "url": "https://news.google.com/search?q=Lowe's+DIY+customer+base+expands"},
        {"title": "Lowe's earnings beat expectations", "url": "https://news.google.com/search?q=Lowe's+earnings+beat+expectations"}
    ]},
    {"ticker": "NKE", "name": "Nike", "momentum": 42.1, "valuation": 32.4, "sentiment": 52.3, "score": 42.2, "pe_ratio": 24.1, "headlines": [
        {"title": "Nike Q3 sales recover from slump", "url": "https://news.google.com/search?q=Nike+Q3+sales+recover+from+slump"},
        {"title": "Nike direct-to-consumer growth accelerates", "url": "https://news.google.com/search?q=Nike+direct-to-consumer+growth+accelerates"},
        {"title": "Nike new CEO executes turnaround plan", "url": "https://news.google.com/search?q=Nike+new+CEO+executes+turnaround+plan"},
        {"title": "Nike stock rebounds on momentum", "url": "https://news.google.com/search?q=Nike+stock+rebounds+on+momentum"}
    ]},
    {"ticker": "ADBE", "name": "Adobe Systems", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Adobe Creative Cloud subscriptions surge", "url": "https://news.google.com/search?q=Adobe+Creative+Cloud+subscriptions+surge"},
        {"title": "Adobe generative AI drives growth", "url": "https://news.google.com/search?q=Adobe+generative+AI+drives+growth"},
        {"title": "Adobe Document Services expand", "url": "https://news.google.com/search?q=Adobe+Document+Services+expand"},
        {"title": "Adobe stock hits new record", "url": "https://news.google.com/search?q=Adobe+stock+hits+new+record"}
    ]},
    {"ticker": "NOW", "name": "ServiceNow", "momentum": 62.8, "valuation": 18.5, "sentiment": 55.4, "score": 45.6, "pe_ratio": 68.2, "headlines": [
        {"title": "ServiceNow Q3 revenue accelerates", "url": "https://news.google.com/search?q=ServiceNow+Q3+revenue+accelerates"},
        {"title": "ServiceNow AI capabilities advance", "url": "https://news.google.com/search?q=ServiceNow+AI+capabilities+advance"},
        {"title": "ServiceNow enterprise deals expand", "url": "https://news.google.com/search?q=ServiceNow+enterprise+deals+expand"},
        {"title": "ServiceNow raises full-year guidance", "url": "https://news.google.com/search?q=ServiceNow+raises+full-year+guidance"}
    ]},
    {"ticker": "SHOP", "name": "Shopify", "momentum": 59.3, "valuation": 22.1, "sentiment": 57.8, "score": 46.4, "pe_ratio": 45.3, "headlines": [
        {"title": "Shopify GMV growth accelerates", "url": "https://news.google.com/search?q=Shopify+GMV+growth+accelerates"},
        {"title": "Shopify AI tools drive conversion", "url": "https://news.google.com/search?q=Shopify+AI+tools+drive+conversion"},
        {"title": "Shopify payments business thrives", "url": "https://news.google.com/search?q=Shopify+payments+business+thrives"},
        {"title": "Shopify stock gains on strong metrics", "url": "https://news.google.com/search?q=Shopify+stock+gains+on+strong+metrics"}
    ]},
    {"ticker": "SPOT", "name": "Spotify", "momentum": 68.5, "valuation": 28.9, "sentiment": 59.1, "score": 52.1, "pe_ratio": 62.1, "headlines": [
        {"title": "Spotify subscribers hit record high", "url": "https://news.google.com/search?q=Spotify+subscribers+hit+record+high"},
        {"title": "Spotify profitability improves significantly", "url": "https://news.google.com/search?q=Spotify+profitability+improves+significantly"},
        {"title": "Spotify podcast platform grows", "url": "https://news.google.com/search?q=Spotify+podcast+platform+grows"},
        {"title": "Spotify stock reaches new peak", "url": "https://news.google.com/search?q=Spotify+stock+reaches+new+peak"}
    ]},
    {"ticker": "TWTR", "name": "Twitter", "momentum": 31.2, "valuation": 15.3, "sentiment": 38.7, "score": 28.4, "pe_ratio": 8.5, "headlines": [
        {"title": "Twitter monetization initiatives grow", "url": "https://news.google.com/search?q=Twitter+monetization+initiatives+grow"},
        {"title": "Twitter user engagement metrics improve", "url": "https://news.google.com/search?q=Twitter+user+engagement+metrics+improve"},
        {"title": "Twitter CEO outlines new strategy", "url": "https://news.google.com/search?q=Twitter+CEO+outlines+new+strategy"},
        {"title": "Twitter working on new features", "url": "https://news.google.com/search?q=Twitter+working+on+new+features"}
    ]},
    {"ticker": "SNAP", "name": "Snap Inc.", "momentum": 45.2, "valuation": 12.8, "sentiment": 42.3, "score": 33.4, "pe_ratio": 35.2, "headlines": [
        {"title": "Snapchat daily active users surge", "url": "https://news.google.com/search?q=Snapchat+daily+active+users+surge"},
        {"title": "Snap advertising revenue grows", "url": "https://news.google.com/search?q=Snap+advertising+revenue+grows"},
        {"title": "Snapchat AR features expand", "url": "https://news.google.com/search?q=Snapchat+AR+features+expand"},
        {"title": "Snap stock gains on earnings beat", "url": "https://news.google.com/search?q=Snap+stock+gains+on+earnings+beat"}
    ]},
    {"ticker": "PINS", "name": "Pinterest", "momentum": 38.9, "valuation": 18.4, "sentiment": 45.6, "score": 34.3, "pe_ratio": 28.9, "headlines": [
        {"title": "Pinterest monthly active users grow", "url": "https://news.google.com/search?q=Pinterest+monthly+active+users+grow"},
        {"title": "Pinterest shopping features accelerate", "url": "https://news.google.com/search?q=Pinterest+shopping+features+accelerate"},
        {"title": "Pinterest international expansion continues", "url": "https://news.google.com/search?q=Pinterest+international+expansion+continues"},
        {"title": "Pinterest reaches profitability milestone", "url": "https://news.google.com/search?q=Pinterest+reaches+profitability+milestone"}
    ]},
    {"ticker": "ROKU", "name": "Roku", "momentum": 52.1, "valuation": 14.2, "sentiment": 48.9, "score": 38.3, "pe_ratio": 35.4, "headlines": [
        {"title": "Roku platform hours watched surge", "url": "https://news.google.com/search?q=Roku+platform+hours+watched+surge"},
        {"title": "Roku advertising platform grows", "url": "https://news.google.com/search?q=Roku+advertising+platform+grows"},
        {"title": "Roku content partnerships expand", "url": "https://news.google.com/search?q=Roku+content+partnerships+expand"},
        {"title": "Roku stock rebounds on forecast", "url": "https://news.google.com/search?q=Roku+stock+rebounds+on+forecast"}
    ]},
    {"ticker": "COIN", "name": "Coinbase", "momentum": 71.3, "valuation": 11.2, "sentiment": 52.8, "score": 45.1, "pe_ratio": 98.3, "headlines": [
        {"title": "Coinbase crypto market activity surges", "url": "https://news.google.com/search?q=Coinbase+crypto+market+activity+surges"},
        {"title": "Coinbase institutional adoption grows", "url": "https://news.google.com/search?q=Coinbase+institutional+adoption+grows"},
        {"title": "Coinbase staking services expand", "url": "https://news.google.com/search?q=Coinbase+staking+services+expand"},
        {"title": "Coinbase stock rallies on Bitcoin surge", "url": "https://news.google.com/search?q=Coinbase+stock+rallies+on+Bitcoin+surge"}
    ]},
    {"ticker": "ASML", "name": "ASML Holding", "momentum": 75.2, "valuation": 32.1, "sentiment": 61.4, "score": 56.2, "pe_ratio": 43.2, "headlines": [
        {"title": "ASML chip equipment orders surge", "url": "https://news.google.com/search?q=ASML+chip+equipment+orders+surge"},
        {"title": "ASML EUV technology in high demand", "url": "https://news.google.com/search?q=ASML+EUV+technology+in+high+demand"},
        {"title": "ASML expands production capacity", "url": "https://news.google.com/search?q=ASML+expands+production+capacity"},
        {"title": "ASML stock reaches all-time high", "url": "https://news.google.com/search?q=ASML+stock+reaches+all-time+high"}
    ]},
]


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/stocks')
def stocks():
    return jsonify(STOCKS)


@app.route('/api/refresh')
def refresh():
    return jsonify({"success": True, "stocks": STOCKS})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
