import json

def parse_json_string(json_string):
    try:
        # Trim the string to get the JSON part between the first '[' and the last ']'
        start_index = json_string.find('[')
        end_index = json_string.rfind(']') + 1
        trimmed_json_string = json_string[start_index:end_index].strip()

        # Check if the trimmed string is empty
        if not trimmed_json_string:
            raise ValueError("No valid JSON data found in the string.")

        # Parse the JSON string
        parsed_json = json.loads(trimmed_json_string)
        return parsed_json
    
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
