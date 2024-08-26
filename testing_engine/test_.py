# test_validation.py
import json
from validation import validate_json, validate_questions, validate_relevant_links
from gemini import evaluate_question_quality, evaluate_relevance  # Import your functions

filepath = 'outputs/tem_outputs/output.json'

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def test_json_validation():
    data = load_data(filepath)
    assert all(validate_json(entry) for entry in data)

def test_question_length():
    data = load_data(filepath)
    assert all(validate_questions(entry['questions']) for entry in data)

def test_relevant_links():
    data = load_data(filepath)
    assert all(validate_relevant_links(entry['relevant_links']) for entry in data)

def test_question_quality():
    data = load_data(filepath)
    for entry in data:
        questions = entry['questions']
        main_content = entry['main_content']
        
        for i, question in enumerate(questions):
            content_index = i // 2
            
            if content_index < len(main_content):
                content_summary = main_content[content_index]
            else:
                content_summary = main_content[-1]  # Fallback to last content if index exceeds
            
            result = evaluate_question_quality([question], content_summary)
            
            assert result 


def test_relevance():
    data = load_data(filepath)
    for entry in data:
        relevant_links = entry['relevant_links']
        main_content = entry['main_content']
        for i, link in enumerate(relevant_links):
            content_index = i // 2
            
            if content_index < len(main_content):
                content_summary = main_content[content_index]
            else:
                content_summary = main_content[-1]
            result = evaluate_relevance([link], content_summary)
            assert result  
