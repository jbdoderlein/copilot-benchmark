"""
"""
import argparse
import os
import json
from pathlib import Path
from time import sleep

import openai

import copilot

with open('config.json', 'r') as f:
    config = json.load(f)

if '__main__' in __name__:
    parser = argparse.ArgumentParser(description='Generate solution from copilot/codex and test')
    parser.add_argument('directory', type=str,
                        help='Sample directory')
    parser.add_argument('-k', '--key', type=int, help="Index of key", default=0)
    parser.add_argument('-e', '--engine', type=str, nargs='+',
                            default=['copilot', 'codex'])
    parser.add_argument('-t', '--temperature', type=float, nargs='+', default=[0.0,0.2,0.4,0.6,0.8,1.0])
    parser.add_argument('-l', '--lang', type=str, nargs='+', default=['python3', 'java', 'cpp', 'c', 'csharp', 'javascript'])
    parser.add_argument('-n', '--number', type=int, default=1, help="Number of samples to generate")

    args = parser.parse_args()
    lib_path = args.directory
    engines = args.engine
    temperatures = args.temperature
    langs = args.lang

    copilot_instance = copilot.Copilot(
        agent_path=os.path.join(os.path.dirname(copilot.__file__), 'dist','agent.js')
    )
    openai.api_key = config["OPENAI_API_KEYS"][args.key]

    PROMPT_PATH = "prompts"
    OUTPUT_PATH = "outputs"
    RESULT_PATH = "results"



    CODEX_SLEEP_COOLDOWN = 20

    input_path = os.path.join(PROMPT_PATH, lib_path)
    for temperature in temperatures:
        for engine in engines:
            for lang in langs:
                Path(
                    os.path.join(OUTPUT_PATH, str(temperature), engine,  lib_path, lang)
                ).mkdir(parents=True, exist_ok=True)

    for lang in langs:
        for i, f in enumerate(os.listdir(os.path.join(input_path, lang))):
            print(f"({i+1}/300) : {f}", flush=True)
            if os.path.isfile(os.path.join(input_path, lang, f)):
                for temperature in temperatures:
                    print(f"Temperature : {temperature}", flush=True)
                    for engine in engines:
                        final_path = os.path.join(OUTPUT_PATH, str(temperature), engine, lib_path, lang)
                        match engine:
                            case "copilot":
                                if temperature == 1.0 and (not os.path.isfile(os.path.join(final_path ,f))): # Define copilto as temp 1
                                    doc = copilot.Document(os.path.join(input_path, lang, f), lang)
                                    gen = copilot_instance.get_all_completion(doc)
                                    doc.save(os.path.join(final_path ,f))

                            case "codex":
                                if not os.path.isfile(os.path.join(final_path ,f)):
                                    with open(os.path.join(input_path, lang, f)) as file:
                                        content_prefix, content_suffix = file.read().split("$$$")

                                    api_pass = False

                                    while not api_pass:
                                        try:
                                            api_result = openai.Completion.create(
                                                model="code-davinci-002",
                                                prompt=content_prefix,
                                                suffix=content_suffix,
                                                max_tokens=256,
                                                temperature=temperature,
                                                n=args.number,
                                            )
                                            api_pass = True
                                        except openai.error.RateLimitError:
                                            print("API Sleep")
                                            sleep(CODEX_SLEEP_COOLDOWN)

                                    if len(api_result["choices"]) > 0:
                                        if args.number == 1:
                                            file_content = content_prefix+api_result["choices"][0]["text"]+content_suffix
                                            with open(os.path.join(final_path ,f), "w") as file:
                                                file.write(str(file_content))
                                        else:
                                            Path(os.path.join(final_path ,f)).mkdir(parents=True, exist_ok=True)
                                            for j, choice in enumerate(api_result["choices"]):
                                                file_content = content_prefix+choice["text"]+content_suffix
                                                with open(os.path.join(final_path ,f,f"{j+1}.{f.split('.')[-1]}"), "w") as file:
                                                    file.write(str(file_content))
