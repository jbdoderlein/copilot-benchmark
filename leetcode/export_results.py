import os
import json

results_path = 'results'

output = {}

for temperature in os.listdir(os.path.join(results_path)):
    output[temperature] = {}
    for model in os.listdir(os.path.join(results_path, temperature)):
        output[temperature][model] = {}
        for variation in os.listdir(os.path.join(results_path, temperature, model)):
            output[temperature][model][variation] = {}
            for lang in os.listdir(os.path.join(results_path, temperature, model, variation)):
                output[temperature][model][variation][lang] = {}
                for file in os.listdir(os.path.join(results_path, temperature, model, variation, lang)):
                    if file.endswith('.json'):
                        with open(os.path.join(results_path, temperature, model, variation, lang, file)) as f:
                            data = json.load(f)
                            output[temperature][model][variation][lang][file] = {
                                'status_msg': data['status_msg'],
                                'total_testcases': data['total_testcases'],
                                'total_correct': data['total_correct'],
                            }

with open('results.json', 'w') as f:
    json.dump(output, f)
