import json
from config import AIProviderConfig
from utils import call_openai_api, call_anthropic_api, calculate_accuracy

def run_evaluation():
    results = []

    for model_id, model_info in AIProviderConfig.MODELS.items():
        print(f"\nEvaluating model: {model_id}")
        total_accuracy = 0
        total_latency = 0
        total_cost = 0
        successful_evals = 0

        for item in AIProviderConfig.EVALUATION_DATA:
            prompt = item["prompt"]
            expected_answer = item["expected_answer"]
            api_response = None

            if model_info["provider"] == "openai":
                api_response = call_openai_api(model_info["name"], prompt)
            elif model_info["provider"] == "anthropic":
                api_response = call_anthropic_api(model_info["name"], prompt)
            else:
                print(f"Unknown provider: {model_info['provider']}")
                continue

            if api_response and api_response["response"] is not None:
                accuracy = calculate_accuracy(api_response["response"], expected_answer)
                cost = (api_response["input_tokens"] * model_info["cost_per_token_input"]) + \
                       (api_response["output_tokens"] * model_info["cost_per_token_output"])
                
                total_accuracy += accuracy
                total_latency += api_response["latency"]
                total_cost += cost
                successful_evals += 1

                print(f"  Prompt: '{prompt[:30]}...' -> Response: '{api_response['response'][:30]}...' - Accuracy: {accuracy}")

        avg_accuracy = (total_accuracy / successful_evals) if successful_evals > 0 else 0
        avg_latency = (total_latency / successful_evals) if successful_evals > 0 else 0
        
        results.append({
            "model_id": model_id,
            "provider": model_info["provider"],
            "avg_accuracy": avg_accuracy,
            "avg_latency_ms": avg_latency * 1000, # Convert to milliseconds
            "total_cost": total_cost, # Sum of costs for all prompts
            "num_evaluations": successful_evals
        })
    
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\n--- Evaluation Complete ---")
    print("Results saved to results.json")

if __name__ == "__main__":
    run_evaluation()
