import requests
import json
from tqdm import tqdm
import pandas as pd
import time

def construct_payload(nouns):
    payload = json.dumps({
      "input": [ {"source": noun} for noun in nouns],
      "config": {
        "modelId": 72,
        "language": {
          "sourceLanguage": "en", # ENGLISH
          "targetLanguage": "te"  # TELUGU
        }
      }
    })
    return payload

def generate_results(start_range, end_range, steps):
    results = []
    headers = {
        'Content-Type': 'application/json'
        }

    for i in tqdm(range(start_range, end_range, steps)):
        start = i
        end = i + steps
        # print(f"starting {start}-{end} / {len(nouns)}")
        response = requests.request("POST", url, headers=headers, data=construct_payload(nouns[start:end]))
        response_json = json.loads(response.text)
        results = results + response_json["output"]
        # print(f"{end}/{len(nouns)} done")
        time.sleep(1)
    
    results_df = pd.DataFrame(results)
    target_df = results_df.target

    results_df.to_csv('telugu_results.txt', header=False, index_label=False, index=False)
    target_df.to_csv('telugu_targets.txt', header=False, index_label=False, index=False)
 
    return results

if __name__ == '__main__':
    url = "https://users-auth.anuvaad.org/nmt-inference/v0/translate"
    nouns = open('testing_sample.txt').read().splitlines()

    translated_text = generate_results(0, 125, 125)