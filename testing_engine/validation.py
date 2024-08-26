# validation.py
import json
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "questions": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 10,
            "maxItems": 10
        },
        "relevant_links": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "link": {"type": "string"},
                    "title": {"type": "string"}
                },
                "required": ["link", "title"]
            },
            "minItems": 5,
            "maxItems": 5
        }
    },
    "required": ["url", "questions", "relevant_links"]
}

def validate_json(data):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False

def validate_questions(questions):
    return all(len(q) <= 80 for q in questions)

def validate_relevant_links(links):
    return len(links) == 5
