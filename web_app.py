import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

STOCKS = [
    {"ticker": "AAPL", "name": "Apple Inc.", "momentum": 82.5, "valuation": 28.8, "sentiment": 60.8, "score": 58.8, "pe_ratio": 28.5, "headlines": [
        {"title": "Apple announces new AI features for iPhone", "url": "https://finance.yahoo.com/news/apple-ai-features"},
        {"title": "Apple stock hits record high amid strong earnings", "url": "https://www.cnbc.com/apple-earnings"},
        {"title": "Apple expands services business", "url": "https://www.bloomberg.com/news/apple-services"},
        {"title": "Apple patent granted for new display technology", "url": "https://www.theverge.com/apple-patent"}
    ]},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "momentum": 84.0, "valuation": 0.0, "sentiment": 49.7, "score": 46.8, "pe_ratio": 52.4, "headlines": [
        {"title": "NVIDIA reports record GPU demand", "url": "https://finance.yahoo.com/news/nvidia-gpu-demand"},
        {"title": "NVIDIA launches next-gen AI chips", "url": "https://www.cnbc.com/nvidia-ai-chips"},
        {"title": "NVIDIA stock rallies on AI boom", "url": "https://www.bloomberg.com/news/nvidia-ai"},
        {"title": "NVIDIA expands data center business", "url": "https://www.theverge.com/nvidia-datacenter"}
    ]},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "momentum": 69.4, "valuation": 0.0, "sentiment": 63.1, "score": 46.4, "pe_ratio": 42.6, "headlines": [
        {"title": "Amazon Q3 revenue beats expectations", "url": "https://finance.yahoo.com/news/amazon-earnings"},
        {"title": "Amazon Web Services continues growth", "url": "https://www.cnbc.com/amazon-aws"},
        {"title": "Amazon invests in AI startups", "url": "https://www.bloomberg.com/news/amazon-ai"},
        {"title": "Amazon announces new logistics initiative", "url": "https://www.theverge.com/amazon-logistics"}
    ]},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "momentum": 32.5, "valuation": 19.7, "sentiment": 58.9, "score": 37.9, "pe_ratio": 32.1, "headlines": [
        {"title": "Microsoft reports strong cloud growth", "url": "https://finance.yahoo.com/news/microsoft-cloud"},
        {"title": "Microsoft Copilot integration drives adoption", "url": "https://www.cnbc.com/microsoft-copilot"},
        {"title": "Microsoft partners with OpenAI for AI expansion", "url": "https://www.bloomberg.com/news/microsoft-openai"},
        {"title": "Microsoft beats earnings expectations", "url": "https://www.theverge.com/microsoft-earnings"}
    ]},
    {"ticker": "TSLA", "name": "Tesla Inc.", "momentum": 42.0, "valuation": 0.0, "sentiment": 46.3, "score": 30.9, "pe_ratio": 65.3, "headlines": [
        {"title": "Tesla launches new Roadster model", "url": "https://finance.yahoo.com/news/tesla-roadster"},
        {"title": "Tesla opens new Gigafactory", "url": "https://www.cnbc.com/tesla-gigafactory"},
        {"title": "Tesla stock surges on delivery numbers", "url": "https://www.bloomberg.com/news/tesla-delivery"},
        {"title": "Tesla announces price cuts", "url": "https://www.theverge.com/tesla-prices"}
    ]},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "momentum": 75.3, "valuation": 25.4, "sentiment": 62.1, "score": 55.2, "pe_ratio": 26.8, "headlines": [
        {"title": "Google announces new AI search features", "url": "https://finance.yahoo.com/news/google-ai-search"},
        {"title": "Alphabet revenue beats analyst expectations", "url": "https://www.cnbc.com/alphabet-earnings"},
        {"title": "Google expands cloud infrastructure", "url": "https://www.bloomberg.com/news/google-cloud"},
        {"title": "Google DeepMind makes breakthrough in AI", "url": "https://www.theverge.com/google-deepmind"}
    ]},
    {"ticker": "META", "name": "Meta Platforms", "momentum": 68.9, "valuation": 21.6, "sentiment": 55.3, "score": 48.3, "pe_ratio": 24.2, "headlines": [
        {"title": "Meta reports strong Q3 advertising revenue", "url": "https://finance.yahoo.com/news/meta-earnings"},
        {"title": "Meta's AI investments pay off", "url": "https://www.cnbc.com/meta-ai"},
        {"title": "Facebook user growth accelerates", "url": "https://www.bloomberg.com/news/meta-users"},
        {"title": "Meta Quest VR headset sales surge", "url": "https://www.theverge.com/meta-quest"}
    ]},
    {"ticker": "NFLX", "name": "Netflix Inc.", "momentum": 71.2, "valuation": 18.9, "sentiment": 58.7, "score": 49.6, "pe_ratio": 29.1, "headlines": [
        {"title": "Netflix subscriber count reaches new high", "url": "https://finance.yahoo.com/news/netflix-subscribers"},
        {"title": "Netflix password sharing crackdown succeeds", "url": "https://www.cnbc.com/netflix-passwords"},
        {"title": "Netflix expands gaming platform", "url": "https://www.bloomberg.com/news/netflix-gaming"},
        {"title": "Netflix stock rallies on strong guidance", "url": "https://www.theverge.com/netflix-guidance"}
    ]},
    {"ticker": "ADOBE", "name": "Adobe Inc.", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Adobe launches generative AI features", "url": "https://finance.yahoo.com/news/adobe-ai"},
        {"title": "Creative Cloud subscriptions surge", "url": "https://www.cnbc.com/adobe-cloud"},
        {"title": "Adobe beats Q3 expectations", "url": "https://www.bloomberg.com/news/adobe-earnings"},
        {"title": "Adobe acquires new AI startup", "url": "https://www.theverge.com/adobe-acquisition"}
    ]},
    {"ticker": "TSMC", "name": "Taiwan Semiconductor", "momentum": 79.5, "valuation": 24.7, "sentiment": 61.2, "score": 55.1, "pe_ratio": 15.3, "headlines": [
        {"title": "TSMC reports record chip demand", "url": "https://finance.yahoo.com/news/tsmc-demand"},
        {"title": "TSMC expands US manufacturing", "url": "https://www.cnbc.com/tsmc-us"},
        {"title": "TSMC secures long-term contracts", "url": "https://www.bloomberg.com/news/tsmc-contracts"},
        {"title": "TSMC invests in advanced packaging", "url": "https://www.theverge.com/tsmc-packaging"}
    ]},
    {"ticker": "JPM", "name": "JPMorgan Chase", "momentum": 58.3, "valuation": 35.2, "sentiment": 52.1, "score": 48.5, "pe_ratio": 12.8, "headlines": [
        {"title": "JPMorgan reports strong Q3 results", "url": "https://finance.yahoo.com/news/jpm-earnings"},
        {"title": "JPMorgan expands investment banking", "url": "https://www.cnbc.com/jpm-banking"},
        {"title": "JPMorgan digital banking adoption grows", "url": "https://www.bloomberg.com/news/jpm-digital"},
        {"title": "JPMorgan raises economic growth forecast", "url": "https://www.theverge.com/jpm-forecast"}
    ]},
    {"ticker": "BAC", "name": "Bank of America", "momentum": 52.1, "valuation": 38.9, "sentiment": 48.3, "score": 46.4, "pe_ratio": 10.2, "headlines": [
        {"title": "Bank of America Q3 earnings beat", "url": "https://finance.yahoo.com/news/bac-earnings"},
        {"title": "BofA wealth management grows", "url": "https://www.cnbc.com/bac-wealth"},
        {"title": "Bank of America digital services expand", "url": "https://www.bloomberg.com/news/bac-digital"},
        {"title": "BofA improves credit quality", "url": "https://www.theverge.com/bac-credit"}
    ]},
    {"ticker": "WFC", "name": "Wells Fargo", "momentum": 45.7, "valuation": 32.1, "sentiment": 45.6, "score": 41.1, "pe_ratio": 11.5, "headlines": [
        {"title": "Wells Fargo reports steady Q3 results", "url": "https://finance.yahoo.com/news/wfc-earnings"},
        {"title": "Wells Fargo settlement discussions continue", "url": "https://www.cnbc.com/wfc-settlement"},
        {"title": "Wells Fargo strengthens risk management", "url": "https://www.bloomberg.com/news/wfc-risk"},
        {"title": "Wells Fargo mortgage business stabilizes", "url": "https://www.theverge.com/wfc-mortgage"}
    ]},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "momentum": 48.9, "valuation": 45.2, "sentiment": 55.3, "score": 49.8, "pe_ratio": 17.2, "headlines": [
        {"title": "J&J receives FDA approval for new drug", "url": "https://finance.yahoo.com/news/jnj-fda"},
        {"title": "Johnson & Johnson Q3 sales grow", "url": "https://www.cnbc.com/jnj-sales"},
        {"title": "J&J cancer drug shows promise", "url": "https://www.bloomberg.com/news/jnj-cancer"},
        {"title": "Johnson & Johnson raises dividend", "url": "https://www.theverge.com/jnj-dividend"}
    ]},
    {"ticker": "UNH", "name": "UnitedHealth Group", "momentum": 72.3, "valuation": 41.8, "sentiment": 57.6, "score": 57.2, "pe_ratio": 19.3, "headlines": [
        {"title": "UnitedHealth Q3 earnings beat forecasts", "url": "https://finance.yahoo.com/news/unh-earnings"},
        {"title": "UnitedHealth acquires healthcare IT firm", "url": "https://www.cnbc.com/unh-acquisition"},
        {"title": "Optum continues rapid expansion", "url": "https://www.bloomberg.com/news/unh-optum"},
        {"title": "UnitedHealth raises 2024 guidance", "url": "https://www.theverge.com/unh-guidance"}
    ]},
    {"ticker": "PFE", "name": "Pfizer Inc.", "momentum": 35.2, "valuation": 48.1, "sentiment": 52.1, "score": 45.1, "pe_ratio": 13.8, "headlines": [
        {"title": "Pfizer reports Q3 vaccine sales surge", "url": "https://finance.yahoo.com/news/pfe-vaccines"},
        {"title": "Pfizer completes COVID pill acquisition", "url": "https://www.cnbc.com/pfe-covid"},
        {"title": "Pfizer pipeline advances key programs", "url": "https://www.bloomberg.com/news/pfe-pipeline"},
        {"title": "Pfizer stock strengthens on earnings", "url": "https://www.theverge.com/pfe-earnings"}
    ]},
    {"ticker": "WMT", "name": "Walmart Inc.", "momentum": 61.2, "valuation": 52.3, "sentiment": 58.9, "score": 57.4, "pe_ratio": 24.1, "headlines": [
        {"title": "Walmart Q3 sales exceed expectations", "url": "https://finance.yahoo.com/news/wmt-sales"},
        {"title": "Walmart grocery e-commerce accelerates", "url": "https://www.cnbc.com/wmt-ecommerce"},
        {"title": "Walmart+ membership grows significantly", "url": "https://www.bloomberg.com/news/wmt-plus"},
        {"title": "Walmart raises full-year guidance", "url": "https://www.theverge.com/wmt-guidance"}
    ]},
    {"ticker": "COST", "name": "Costco Wholesale", "momentum": 65.8, "valuation": 48.2, "sentiment": 61.3, "score": 58.4, "pe_ratio": 41.2, "headlines": [
        {"title": "Costco membership fees increase", "url": "https://finance.yahoo.com/news/cost-membership"},
        {"title": "Costco comparable sales grow double digits", "url": "https://www.cnbc.com/cost-sales"},
        {"title": "Costco online business booming", "url": "https://www.bloomberg.com/news/cost-online"},
        {"title": "Costco stock hits record high", "url": "https://www.theverge.com/cost-record"}
    ]},
    {"ticker": "MCD", "name": "McDonald's", "momentum": 55.3, "valuation": 49.8, "sentiment": 56.7, "score": 53.9, "pe_ratio": 26.4, "headlines": [
        {"title": "McDonald's Q3 revenue beats forecasts", "url": "https://finance.yahoo.com/news/mcd-earnings"},
        {"title": "McDonald's international growth accelerates", "url": "https://www.cnbc.com/mcd-international"},
        {"title": "McDonald's AI drive-thru rollout expands", "url": "https://www.bloomberg.com/news/mcd-ai"},
        {"title": "McDonald's stock rallies on guidance", "url": "https://www.theverge.com/mcd-guidance"}
    ]},
    {"ticker": "SBUX", "name": "Starbucks", "momentum": 42.1, "valuation": 35.6, "sentiment": 54.2, "score": 44.0, "pe_ratio": 28.7, "headlines": [
        {"title": "Starbucks reports Q3 comparable sales growth", "url": "https://finance.yahoo.com/news/sbux-sales"},
        {"title": "Starbucks new CEO outlines strategy", "url": "https://www.cnbc.com/sbux-ceo"},
        {"title": "Starbucks loyalty program expands", "url": "https://www.bloomberg.com/news/sbux-loyalty"},
        {"title": "Starbucks opens new stores globally", "url": "https://www.theverge.com/sbux-expansion"}
    ]},
    {"ticker": "XOM", "name": "Exxon Mobil", "momentum": 58.9, "valuation": 55.2, "sentiment": 48.3, "score": 53.8, "pe_ratio": 8.9, "headlines": [
        {"title": "ExxonMobil Q3 profits surge on oil prices", "url": "https://finance.yahoo.com/news/xom-profits"},
        {"title": "ExxonMobil invests in low-carbon energy", "url": "https://www.cnbc.com/xom-carbon"},
        {"title": "ExxonMobil Guyana production ramps up", "url": "https://www.bloomberg.com/news/xom-guyana"},
        {"title": "ExxonMobil dividend increase announced", "url": "https://www.theverge.com/xom-dividend"}
    ]},
    {"ticker": "CVX", "name": "Chevron", "momentum": 62.1, "valuation": 58.3, "sentiment": 51.2, "score": 57.2, "pe_ratio": 9.2, "headlines": [
        {"title": "Chevron Q3 earnings beat estimates", "url": "https://finance.yahoo.com/news/cvx-earnings"},
        {"title": "Chevron benefits from energy transition", "url": "https://www.cnbc.com/cvx-transition"},
        {"title": "Chevron production increases this quarter", "url": "https://www.bloomberg.com/news/cvx-production"},
        {"title": "Chevron raises shareholder return plan", "url": "https://www.theverge.com/cvx-returns"}
    ]},
    {"ticker": "BA", "name": "Boeing", "momentum": 38.2, "valuation": 28.9, "sentiment": 42.1, "score": 36.4, "pe_ratio": 42.3, "headlines": [
        {"title": "Boeing reports Q3 defense contracts", "url": "https://finance.yahoo.com/news/ba-defense"},
        {"title": "Boeing 737 Max deliveries ramp up", "url": "https://www.cnbc.com/ba-737max"},
        {"title": "Boeing space business accelerates", "url": "https://www.bloomberg.com/news/ba-space"},
        {"title": "Boeing stock gains on production increases", "url": "https://www.theverge.com/ba-production"}
    ]},
    {"ticker": "CAT", "name": "Caterpillar", "momentum": 64.5, "valuation": 38.7, "sentiment": 52.3, "score": 51.8, "pe_ratio": 12.6, "headlines": [
        {"title": "Caterpillar Q3 sales exceed forecasts", "url": "https://finance.yahoo.com/news/cat-sales"},
        {"title": "Caterpillar equipment demand remains strong", "url": "https://www.cnbc.com/cat-demand"},
        {"title": "Caterpillar services business grows", "url": "https://www.bloomberg.com/news/cat-services"},
        {"title": "Caterpillar raises annual guidance", "url": "https://www.theverge.com/cat-guidance"}
    ]},
    {"ticker": "GE", "name": "General Electric", "momentum": 52.3, "valuation": 32.1, "sentiment": 48.9, "score": 44.4, "pe_ratio": 18.3, "headlines": [
        {"title": "GE reports Q3 earnings beat", "url": "https://finance.yahoo.com/news/ge-earnings"},
        {"title": "GE renewable energy business booms", "url": "https://www.cnbc.com/ge-renewable"},
        {"title": "GE aviation orders strengthen", "url": "https://www.bloomberg.com/news/ge-aviation"},
        {"title": "GE stock gains on outlook improvement", "url": "https://www.theverge.com/ge-outlook"}
    ]},
    {"ticker": "V", "name": "Visa Inc.", "momentum": 71.8, "valuation": 42.3, "sentiment": 59.2, "score": 57.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Visa Q3 payment volume surges", "url": "https://finance.yahoo.com/news/v-volume"},
        {"title": "Visa expands digital payments platform", "url": "https://www.cnbc.com/v-digital"},
        {"title": "Visa cryptocurrency partnerships grow", "url": "https://www.bloomberg.com/news/v-crypto"},
        {"title": "Visa raises quarterly dividend", "url": "https://www.theverge.com/v-dividend"}
    ]},
    {"ticker": "MA", "name": "Mastercard", "momentum": 73.2, "valuation": 39.8, "sentiment": 61.1, "score": 58.0, "pe_ratio": 40.2, "headlines": [
        {"title": "Mastercard Q3 results exceed expectations", "url": "https://finance.yahoo.com/news/ma-results"},
        {"title": "Mastercard contactless payments surge", "url": "https://www.cnbc.com/ma-contactless"},
        {"title": "Mastercard AI fraud detection improves", "url": "https://www.bloomberg.com/news/ma-fraud"},
        {"title": "Mastercard stock rallies on growth", "url": "https://www.theverge.com/ma-growth"}
    ]},
    {"ticker": "PYPL", "name": "PayPal", "momentum": 48.9, "valuation": 28.3, "sentiment": 50.6, "score": 42.6, "pe_ratio": 32.1, "headlines": [
        {"title": "PayPal Q3 earnings top forecasts", "url": "https://finance.yahoo.com/news/pypl-earnings"},
        {"title": "PayPal blockchain integration expands", "url": "https://www.cnbc.com/pypl-blockchain"},
        {"title": "PayPal user growth accelerates", "url": "https://www.bloomberg.com/news/pypl-users"},
        {"title": "PayPal gross payment volume increases", "url": "https://www.theverge.com/pypl-volume"}
    ]},
    {"ticker": "INTC", "name": "Intel", "momentum": 35.6, "valuation": 18.9, "sentiment": 43.2, "score": 32.6, "pe_ratio": 11.4, "headlines": [
        {"title": "Intel reports Q3 results amid recovery", "url": "https://finance.yahoo.com/news/intc-recovery"},
        {"title": "Intel new chip architecture impresses", "url": "https://www.cnbc.com/intc-architecture"},
        {"title": "Intel foundry services gain momentum", "url": "https://www.bloomberg.com/news/intc-foundry"},
        {"title": "Intel stock bounces on strategy update", "url": "https://www.theverge.com/intc-strategy"}
    ]},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "momentum": 68.3, "valuation": 21.2, "sentiment": 54.8, "score": 48.1, "pe_ratio": 29.3, "headlines": [
        {"title": "AMD Q3 sales beat analyst estimates", "url": "https://finance.yahoo.com/news/amd-sales"},
        {"title": "AMD data center growth accelerates", "url": "https://www.cnbc.com/amd-datacenter"},
        {"title": "AMD AI chip demand surges", "url": "https://www.bloomberg.com/news/amd-ai"},
        {"title": "AMD stock reaches new high", "url": "https://www.theverge.com/amd-high"}
    ]},
    {"ticker": "QCOM", "name": "Qualcomm", "momentum": 62.1, "valuation": 24.7, "sentiment": 52.3, "score": 46.3, "pe_ratio": 17.8, "headlines": [
        {"title": "Qualcomm Q3 earnings beat forecasts", "url": "https://finance.yahoo.com/news/qcom-earnings"},
        {"title": "Qualcomm 5G chip demand remains robust", "url": "https://www.cnbc.com/qcom-5g"},
        {"title": "Qualcomm automotive business grows", "url": "https://www.bloomberg.com/news/qcom-auto"},
        {"title": "Qualcomm raises annual guidance", "url": "https://www.theverge.com/qcom-guidance"}
    ]},
    {"ticker": "CSCO", "name": "Cisco Systems", "momentum": 41.2, "valuation": 32.8, "sentiment": 49.1, "score": 41.0, "pe_ratio": 18.9, "headlines": [
        {"title": "Cisco Q3 results meet expectations", "url": "https://finance.yahoo.com/news/csco-results"},
        {"title": "Cisco software subscription business grows", "url": "https://www.cnbc.com/csco-software"},
        {"title": "Cisco cloud strategy gaining traction", "url": "https://www.bloomberg.com/news/csco-cloud"},
        {"title": "Cisco security solutions in demand", "url": "https://www.theverge.com/csco-security"}
    ]},
    {"ticker": "CRM", "name": "Salesforce", "momentum": 55.3, "valuation": 29.7, "sentiment": 56.2, "score": 47.0, "pe_ratio": 51.3, "headlines": [
        {"title": "Salesforce Q3 revenue grows 11%", "url": "https://finance.yahoo.com/news/crm-growth"},
        {"title": "Salesforce Einstein AI adoption surges", "url": "https://www.cnbc.com/crm-einstein"},
        {"title": "Salesforce enterprise deals expand", "url": "https://www.bloomberg.com/news/crm-deals"},
        {"title": "Salesforce stock rallies on results", "url": "https://www.theverge.com/crm-results"}
    ]},
    {"ticker": "ORCL", "name": "Oracle", "momentum": 58.9, "valuation": 35.2, "sentiment": 53.1, "score": 49.0, "pe_ratio": 19.2, "headlines": [
        {"title": "Oracle Q3 cloud revenue beats estimates", "url": "https://finance.yahoo.com/news/orcl-cloud"},
        {"title": "Oracle database business remains strong", "url": "https://www.cnbc.com/orcl-database"},
        {"title": "Oracle AI initiatives accelerate", "url": "https://www.bloomberg.com/news/orcl-ai"},
        {"title": "Oracle stock gains on cloud growth", "url": "https://www.theverge.com/orcl-growth"}
    ]},
    {"ticker": "IBM", "name": "IBM", "momentum": 39.2, "valuation": 41.3, "sentiment": 48.7, "score": 43.0, "pe_ratio": 16.1, "headlines": [
        {"title": "IBM Q3 earnings top expectations", "url": "https://finance.yahoo.com/news/ibm-earnings"},
        {"title": "IBM quantum computing advances", "url": "https://www.cnbc.com/ibm-quantum"},
        {"title": "IBM cloud infrastructure grows", "url": "https://www.bloomberg.com/news/ibm-cloud"},
        {"title": "IBM stock rebounds on guidance", "url": "https://www.theverge.com/ibm-guidance"}
    ]},
    {"ticker": "TGT", "name": "Target", "momentum": 52.1, "valuation": 42.8, "sentiment": 54.1, "score": 49.6, "pe_ratio": 18.7, "headlines": [
        {"title": "Target Q3 comparable sales grow", "url": "https://finance.yahoo.com/news/tgt-sales"},
        {"title": "Target same-day services expand", "url": "https://www.cnbc.com/tgt-sameday"},
        {"title": "Target digital sales accelerate", "url": "https://www.bloomberg.com/news/tgt-digital"},
        {"title": "Target stock gains on holiday outlook", "url": "https://www.theverge.com/tgt-outlook"}
    ]},
    {"ticker": "HD", "name": "The Home Depot", "momentum": 48.3, "valuation": 38.9, "sentiment": 51.2, "score": 46.1, "pe_ratio": 22.3, "headlines": [
        {"title": "Home Depot Q3 sales beat forecasts", "url": "https://finance.yahoo.com/news/hd-sales"},
        {"title": "Home Depot pro customer growth strong", "url": "https://www.cnbc.com/hd-pro"},
        {"title": "Home Depot digital tools expand", "url": "https://www.bloomberg.com/news/hd-digital"},
        {"title": "Home Depot stock rallies on results", "url": "https://www.theverge.com/hd-results"}
    ]},
    {"ticker": "LOWE", "name": "Lowe's", "momentum": 45.7, "valuation": 35.2, "sentiment": 49.8, "score": 43.5, "pe_ratio": 19.8, "headlines": [
        {"title": "Lowe's Q3 comparable sales grow", "url": "https://finance.yahoo.com/news/lowe-sales"},
        {"title": "Lowe's online business accelerates", "url": "https://www.cnbc.com/lowe-online"},
        {"title": "Lowe's DIY customer base expands", "url": "https://www.bloomberg.com/news/lowe-diy"},
        {"title": "Lowe's earnings beat expectations", "url": "https://www.theverge.com/lowe-earnings"}
    ]},
    {"ticker": "NKE", "name": "Nike", "momentum": 42.1, "valuation": 32.4, "sentiment": 52.3, "score": 42.2, "pe_ratio": 24.1, "headlines": [
        {"title": "Nike Q3 sales recover from slump", "url": "https://finance.yahoo.com/news/nke-recovery"},
        {"title": "Nike direct-to-consumer growth accelerates", "url": "https://www.cnbc.com/nke-dtc"},
        {"title": "Nike new CEO executes turnaround plan", "url": "https://www.bloomberg.com/news/nke-ceo"},
        {"title": "Nike stock rebounds on momentum", "url": "https://www.theverge.com/nke-momentum"}
    ]},
    {"ticker": "ADBE", "name": "Adobe Systems", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5, "headlines": [
        {"title": "Adobe Creative Cloud subscriptions surge", "url": "https://finance.yahoo.com/news/adbe-cloud"},
        {"title": "Adobe generative AI drives growth", "url": "https://www.cnbc.com/adbe-genai"},
        {"title": "Adobe Document Services expand", "url": "https://www.bloomberg.com/news/adbe-docs"},
        {"title": "Adobe stock hits new record", "url": "https://www.theverge.com/adbe-record"}
    ]},
    {"ticker": "NOW", "name": "ServiceNow", "momentum": 62.8, "valuation": 18.5, "sentiment": 55.4, "score": 45.6, "pe_ratio": 68.2, "headlines": [
        {"title": "ServiceNow Q3 revenue accelerates", "url": "https://finance.yahoo.com/news/now-revenue"},
        {"title": "ServiceNow AI capabilities advance", "url": "https://www.cnbc.com/now-ai"},
        {"title": "ServiceNow enterprise deals expand", "url": "https://www.bloomberg.com/news/now-deals"},
        {"title": "ServiceNow raises full-year guidance", "url": "https://www.theverge.com/now-guidance"}
    ]},
    {"ticker": "SHOP", "name": "Shopify", "momentum": 59.3, "valuation": 22.1, "sentiment": 57.8, "score": 46.4, "pe_ratio": 45.3, "headlines": [
        {"title": "Shopify GMV growth accelerates", "url": "https://finance.yahoo.com/news/shop-gmv"},
        {"title": "Shopify AI tools drive conversion", "url": "https://www.cnbc.com/shop-ai"},
        {"title": "Shopify payments business thrives", "url": "https://www.bloomberg.com/news/shop-payments"},
        {"title": "Shopify stock gains on strong metrics", "url": "https://www.theverge.com/shop-metrics"}
    ]},
    {"ticker": "SPOT", "name": "Spotify", "momentum": 68.5, "valuation": 28.9, "sentiment": 59.1, "score": 52.1, "pe_ratio": 62.1, "headlines": [
        {"title": "Spotify subscribers hit record high", "url": "https://finance.yahoo.com/news/spot-subscribers"},
        {"title": "Spotify profitability improves significantly", "url": "https://www.cnbc.com/spot-profit"},
        {"title": "Spotify podcast platform grows", "url": "https://www.bloomberg.com/news/spot-podcast"},
        {"title": "Spotify stock reaches new peak", "url": "https://www.theverge.com/spot-peak"}
    ]},
    {"ticker": "TWTR", "name": "Twitter", "momentum": 31.2, "valuation": 15.3, "sentiment": 38.7, "score": 28.4, "pe_ratio": 8.5, "headlines": [
        {"title": "Twitter monetization initiatives grow", "url": "https://finance.yahoo.com/news/twtr-monetization"},
        {"title": "Twitter user engagement metrics improve", "url": "https://www.cnbc.com/twtr-engagement"},
        {"title": "Twitter CEO outlines new strategy", "url": "https://www.bloomberg.com/news/twtr-strategy"},
        {"title": "Twitter working on new features", "url": "https://www.theverge.com/twtr-features"}
    ]},
    {"ticker": "SNAP", "name": "Snap Inc.", "momentum": 45.2, "valuation": 12.8, "sentiment": 42.3, "score": 33.4, "pe_ratio": 35.2, "headlines": [
        {"title": "Snapchat daily active users surge", "url": "https://finance.yahoo.com/news/snap-users"},
        {"title": "Snap advertising revenue grows", "url": "https://www.cnbc.com/snap-ads"},
        {"title": "Snapchat AR features expand", "url": "https://www.bloomberg.com/news/snap-ar"},
        {"title": "Snap stock gains on earnings beat", "url": "https://www.theverge.com/snap-earnings"}
    ]},
    {"ticker": "PINS", "name": "Pinterest", "momentum": 38.9, "valuation": 18.4, "sentiment": 45.6, "score": 34.3, "pe_ratio": 28.9, "headlines": [
        {"title": "Pinterest monthly active users grow", "url": "https://finance.yahoo.com/news/pins-users"},
        {"title": "Pinterest shopping features accelerate", "url": "https://www.cnbc.com/pins-shopping"},
        {"title": "Pinterest international expansion continues", "url": "https://www.bloomberg.com/news/pins-intl"},
        {"title": "Pinterest reaches profitability milestone", "url": "https://www.theverge.com/pins-profit"}
    ]},
    {"ticker": "ROKU", "name": "Roku", "momentum": 52.1, "valuation": 14.2, "sentiment": 48.9, "score": 38.3, "pe_ratio": 35.4, "headlines": [
        {"title": "Roku platform hours watched surge", "url": "https://finance.yahoo.com/news/roku-hours"},
        {"title": "Roku advertising platform grows", "url": "https://www.cnbc.com/roku-ads"},
        {"title": "Roku content partnerships expand", "url": "https://www.bloomberg.com/news/roku-content"},
        {"title": "Roku stock rebounds on forecast", "url": "https://www.theverge.com/roku-forecast"}
    ]},
    {"ticker": "COIN", "name": "Coinbase", "momentum": 71.3, "valuation": 11.2, "sentiment": 52.8, "score": 45.1, "pe_ratio": 98.3, "headlines": [
        {"title": "Coinbase crypto market activity surges", "url": "https://finance.yahoo.com/news/coin-activity"},
        {"title": "Coinbase institutional adoption grows", "url": "https://www.cnbc.com/coin-institutional"},
        {"title": "Coinbase staking services expand", "url": "https://www.bloomberg.com/news/coin-staking"},
        {"title": "Coinbase stock rallies on Bitcoin surge", "url": "https://www.theverge.com/coin-bitcoin"}
    ]},
    {"ticker": "ASML", "name": "ASML Holding", "momentum": 75.2, "valuation": 32.1, "sentiment": 61.4, "score": 56.2, "pe_ratio": 43.2, "headlines": [
        {"title": "ASML chip equipment orders surge", "url": "https://finance.yahoo.com/news/asml-orders"},
        {"title": "ASML EUV technology in high demand", "url": "https://www.cnbc.com/asml-euv"},
        {"title": "ASML expands production capacity", "url": "https://www.bloomberg.com/news/asml-capacity"},
        {"title": "ASML stock reaches all-time high", "url": "https://www.theverge.com/asml-high"}
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
