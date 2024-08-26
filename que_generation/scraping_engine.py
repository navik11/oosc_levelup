import requests
from bs4 import BeautifulSoup # type: ignore
import json
# import numpy as np
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url):
    logging.info(f"Scraping website: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch the main URL: {e}")
        return []

    main_soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in main_soup.find_all('a') if link.get('href')]
    
    logging.debug(f"Found {len(links)} links on the main page")

    main_content = []
    unique_links = set()
    count = 0
    relevant_links = []

    for link in links:
        # Construct full link if necessary
        full_link = link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}"

        # Check if the link is unique and doesn't contain '#'
        if '#' not in full_link and full_link not in unique_links:
            unique_links.add(full_link)
            logging.debug(f"Processing link: {full_link}")

            try:
                link_response = requests.get(full_link, timeout=5)
                link_response.raise_for_status()  # Check for HTTP errors

                soup = BeautifulSoup(link_response.text, 'html.parser')

                title = soup.title.string.strip() if soup.title else "No Title Found"
                relevant_links.append({"link": full_link, "title": title})
                content = {"link": full_link}
                txt = ""

                # Iterate over all elements and add their text to the content list
                for element in soup.find_all(['h1', 'h2', 'p']):
                    txt += " " + element.get_text(strip=True)

                content["text"] = txt.strip() + '\n'  # Ensure each content ends with a newline
                main_content.append(content)
                
                count += 1
                if count == 12:  # Stop after processing exactly 5 unique links
                    break

            except requests.RequestException as e:
                logging.warning(f"Failed to scrape {full_link}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error when scraping {full_link}: {e}")
    
    return main_content, relevant_links
