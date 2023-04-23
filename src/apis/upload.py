from flask import Blueprint, jsonify, request
import yaml
import openai
import logging

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    """
    POST request json:
    {
        "document": "the document text"
    }
    """
    # Check if the request has JSON data
    if request.is_json:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if the "text" field is present in the JSON data
        if 'document' in data:
            text = data['document']
            useGPT4 = data['useGPT4']
            response = generate_questions_and_answers(text, useGPT4=useGPT4)
            return jsonify(response), 200
        else:
            return jsonify({'error': 'The "text" field is missing from the JSON data.'}), 400
    else:
        return jsonify({'error': 'No JSON data provided.'}), 400


def generate_questions_and_answers(doc_text, useGPT4=False):
    """
    Response as a JSON:
    {
    "questions": [
        {
        "question_text": "What is the capital of Italy?",
        "choices": {
            "a": "Venice",
            "b": "Florence",
            "c": "Rome",
            "d": "Milan"
        },
        "correct_answer": "c"
        },
        {
        "question_text": "Which ancient country is Rome also associated with?",
        "choices": {
            "a": "Greece",
            "b": "Egypt",
            "c": "Persia",
            "d": "Rome"
        },
        "correct_answer": "d"
        }
    ]
    }
    """
    
    system_prompt = """You are an AI tutor that tries to assess gaps in understanding. An ideal quiz captures understanding of concepts, asks students to translate their understanding to unknown settings/contexts, and pushes students to move beyond mere definitions. Your goal is to create four quiz questions that test conceptual understanding and mastery. Multiple choice questions only.
Return in a YAML array with the following fields question text, choices, and correct answer. For the correct fields, return a-d, not the question text. Take it step by step."""
    
    question_prompt = f"""
Document to quiz on:
{doc_text}

Example of one question:
- question_text: "Question"
  choices:
    a: "Choice 1"
    b: "Choice 2"
    c: "Choice 3"
    d: "Choice 4"
  correct_answer: c

YAML of questions:
"""

    model = "gpt-4" if useGPT4 else "gpt-3.5-turbo"

    print("Starting chat completion with", model)
    
    result = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt,
            "role": "user", "content": question_prompt}
        ]
    )
    
    print("Chat completion finished")
    
    question_yaml = result["choices"][0]["message"]["content"]    
    dct = yaml.load(question_yaml, Loader=yaml.FullLoader)
    
    return {
        "questions": dct
    }