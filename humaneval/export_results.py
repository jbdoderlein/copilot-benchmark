import os
import json

results_path = 'results'

output = {}

open_gen = ['algorithm', 'complexity', 'ltsbs']

for temperature in os.listdir(os.path.join(results_path)):
    output[temperature] = {}
    for model in os.listdir(os.path.join(results_path, temperature)):
        output[temperature][model] = {}
        for variation in os.listdir(os.path.join(results_path, temperature, model)):
            if variation.endswith('.json'):
                with open(os.path.join(results_path, temperature, model, variation), 'r') as f:
                    if sum([g in variation for g in open_gen])>0 and model=='copilot':
                        if 'cpfd' in variation:
                            output[temperature][model][variation.replace('_cpfd', '').replace('cpfd','')] = json.load(f)
                        else:
                            pass
                    else:
                        output[temperature][model][variation] = json.load(f)

with open('results.json', 'w') as f:
    json.dump(output, f)
