import time
import requests
from config import AIProviderConfig

def call_openai_api(model_name, prompt):
    headers = {
        "Authorization": f"Bearer {AIProviderConfig.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50
    }
    start_time = time.time()
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        end_time = time.time()
        response_json = response.json()
        return {
            "response": response_json["choices"][0]["message"]["content"],
            "latency": end_time - start_time,
            "input_tokens": response_json["usage"]["prompt_tokens"],
            "output_tokens": response_json["usage"]["completion_tokens"],
        }
    except requests.exceptions.RequestException as e:
        print(f"OpenAI API error: {e}")
        return {"response": None, "latency": -1, "input_tokens": 0, "output_tokens": 0}

def call_anthropic_api(model_name, prompt):
    headers = {
        "x-api-key": AIProviderConfig.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50
    }
    start_time = time.time()
    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        response.raise_for_status()
        end_time = time.time()
        response_json = response.json()
        return {
            "response": response_json["content"][0]["text"],
            "latency": end_time - start_time,
            "input_tokens": response_json["usage"]["input_tokens"],
            "output_tokens": response_json["usage"]["output_tokens"],
        }
    except requests.exceptions.RequestException as e:
        print(f"Anthropic API error: {e}")
        return {"response": None, "latency": -1, "input_tokens": 0, "output_tokens": 0}

def calculate_accuracy(response, expected_answer):
    return 1 if expected_answer.lower() in response.lower() else 0
