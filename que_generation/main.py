import json
import google.generativeai as genai # type: ignore
from json_decoder import parse_json_string
from scraping_engine import scrape_website
import subprocess
from urllib.parse import urlparse
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('API_KEY')

def process_website(url):
    print("Scraping website...")
    scraped_data, relevent_links = scrape_website(url)
    if scraped_data and relevent_links:
        print("Website scraping completed...✅ ✅")
    else:
        print("Error encountered while scraping...❌❌")
        return
    print("Generating Questions... Please wait...🕒🕒🕒")
    with open('././outputs/scraped_data/scraped_data.json', 'w') as f:
        json.dump(scraped_data, f, indent=4)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    query_template = "from the following content generate 2 general questions, with length striclty less than 70 characters. (return a json array): "

    questions = []
    rl = []
    main_content = []

    cnt = 0
    ind = 0
    for(content) in scraped_data:
        ind = ind + 1
        query = query_template + content["text"]
        response = model.generate_content(query)
        q = parse_json_string(response.text)
        if q:
            cnt = cnt + len(q)
            questions = questions + q
            rl.append(relevent_links[ind-1])
            main_content.append(content["text"])
        if cnt >= 10:
            break

    outputdata = [
        {
            "url": url,
            "questions": questions,
            "relevant_links": rl,
            "main_content": main_content
        }
    ]

    with open('././outputs/tem_outputs/output.json', 'w') as f:
        json.dump(outputdata, f, indent=4)

    print("Output Received ✅✅")

    print("Running tests...🕒🕒")
    result = subprocess.run(['pytest', '-p', 'no:warnings', 'testing_engine/test_.py', '-v'], capture_output=True, text=True)

    if result.stdout:
        print("Pytest Output:")
        print(result.stdout)
        outputdata = [
        {
            "url": url,
            "questions": questions,
            "relevant_links": rl,
        }
    ]
        with open('././outputs/output.json', 'w') as f:
            json.dump(outputdata, f, indent=4)
        

    if result.stderr:
        print("Pytest Errors:")
        print(result.stderr)


    if result.returncode == 0:
        print("Tests passed successfully✅✅")
    else:
        print("Some test failed!")

website_url = input("Enter URL : ") 

# ************ Uncomment below code and comment above line if You want to use Docker with env ***********

# website_url = os.getenv('WEBSITE_URL')
# if not website_url:
#     raise ValueError("No URL provided. Set the WEBSITE_URL environment variable.")

process_website(website_url)
print("Process Completed, Check the Output Folder ✅✅")