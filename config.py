import os

class AIProviderConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key")
    # Add more providers here

    MODELS = {
        "openai_gpt3.5": {
            "provider": "openai",
            "name": "gpt-3.5-turbo",
            "cost_per_token_input": 0.0000015, # Example cost
            "cost_per_token_output": 0.000002,
        },
        "anthropic_claude_opus": {
            "provider": "anthropic",
            "name": "claude-3-opus-20240229",
            "cost_per_token_input": 0.000015,
            "cost_per_token_output": 0.000075,
        },
        # Add more models
    }

    EVALUATION_DATA = [
        {"prompt": "What is the capital of France?", "expected_answer": "Paris"},
        {"prompt": "2 + 2 = ?", "expected_answer": "4"},
    ]
