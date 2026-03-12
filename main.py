import json
import pandas as pd
from evaluate import run_evaluation

def display_results():
    try:
        with open("results.json", "r") as f:
            results = json.load(f)

        if not results:
            print("No evaluation results found. Run `python evaluate.py` first.")
            return

        df = pd.DataFrame(results)
        df_sorted = df.sort_values(by='avg_accuracy', ascending=False)

        print("\n--- Model Evaluation Summary ---")
        print(df_sorted[['model_id', 'provider', 'avg_accuracy', 'avg_latency_ms', 'total_cost']])
        print("\nDetailed raw results stored in results.json")

    except FileNotFoundError:
        print("results.json not found. Please run `python evaluate.py` to generate results.")
    except Exception as e:
        print(f"An error occurred while displaying results: {e}")

if __name__ == "__main__":
    # Optionally uncomment to re-run evaluation every time main.py is executed
    # print("Running evaluations...")
    # run_evaluation()
    display_results()
