import google.generativeai as genai
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)  # Replace with your actual API key

model = genai.GenerativeModel('gemini-1.5-flash') 

def evaluate_question_quality(questions, content_summary):
    prompt = (
        f"Evaluate the quality of these questions based on their clarity, relevance, and conciseness. "
        f"Each question should be clear, relevant to the content summary, and concise (under 80 characters).\n\n"
        f"Questions: {questions}\n\nContent Summary: {content_summary}"
    )
    
    try:
        response = model.generate_content(prompt)
        result = response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        result = "Error in evaluation"
    
    return result

def evaluate_relevance(relevant_links, content_summary):
    prompt = (
        f"Evaluate the relevance of these links based on their connection to the content summary.\n\n"
        f"Links: {relevant_links}\n\nContent Summary: {content_summary}"
    )
    
    try:
        response = model.generate_content(prompt)
        result = response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        result = "Error in evaluation"
    
    return result
