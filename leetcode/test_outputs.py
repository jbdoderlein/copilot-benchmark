import os
import json
import argparse
from time import sleep
from pathlib import Path

import leetcode
import leetcode.auth

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send solution to Leetcode')
    parser.add_argument('directory', type=str,
                        help='Sample directory')
    parser.add_argument('-k', '--key', type=int,
        default=0, help='The key of session id in config.json')

    parser.add_argument('-e', '--engine', type=str, nargs='+',
                            default=['copilot', 'codex'])
    parser.add_argument('-t', '--temperature', type=float, nargs='+', default=[0.0,0.2,0.4,0.6,0.8,1.0])
    parser.add_argument('-l', '--lang', type=str, nargs='+', default=['python3', 'java', 'cpp', 'c', 'csharp', 'javascript'])

    parser.add_argument('-ns', '--skip', type=int,
        default=0, help='Number of problem to skip(for parallelisation)')

    parser.add_argument('-nt', '--stop', type=int,
        default=-1, help='Number of problem to stop(for parallelisation)')
    args = parser.parse_args()

    KEY = args.key
    SKIP = args.skip
    STOP = args.stop

    with open('config.json', 'r') as f:
        config = json.load(f)

    configuration = leetcode.Configuration()
    leetcode_session: str = config['LEETCODE_SESSIONS'][KEY]
    csrf_token: str = leetcode.auth.get_csrf_cookie(leetcode_session)
    configuration.api_key["x-csrftoken"] = csrf_token
    configuration.api_key["csrftoken"] = csrf_token
    configuration.api_key["LEETCODE_SESSION"] = leetcode_session
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    QUERY = """
            query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
            }
            }
        """

    LANG = ['python3', 'java', 'cpp', 'c', 'csharp', 'javascript']
    EXTENSION = {
        'python3': '.py',
        'java': '.java',
        'cpp': '.cpp',
        'c': '.c',
        'csharp': '.cs',
        'javascript': '.js'
    }

    TIME_SLEEP = 30


    lib_path = args.directory
    engines = args.engine
    temperatures = args.temperature
    langs = args.lang

    OUTPUT_PATH = "outputs"
    RESULT_PATH = "results"

    for temperature in temperatures:
        if os.path.exists(os.path.join(OUTPUT_PATH, str(temperature))):
            for engine in engines:
                if os.path.exists(os.path.join(OUTPUT_PATH,str(temperature),engine)):
                    for lang in langs:
                        if os.path.exists(os.path.join(OUTPUT_PATH,str(temperature),engine,lib_path,lang)):
                            output_path = os.path.join(OUTPUT_PATH, str(temperature), engine, lib_path, lang)
                            print(output_path)
                            gen = os.listdir(output_path)[SKIP:STOP]
                            for i,f in enumerate(gen):
                                problem = f.replace(EXTENSION[lang], '')
                                print(f"-{problem} ({i+1}/{len(gen)})", end="")
                                
                                result_path = os.path.join(RESULT_PATH, str(temperature), engine, lib_path, lang)

                                if not os.path.exists(os.path.join(result_path, problem+".json")):
                                    graphql_request = leetcode.GraphqlQuery(
                                    query=QUERY,
                                    variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=problem),
                                    operation_name="getQuestionDetail")

                                    output = api_instance.graphql_post(body=graphql_request)

                                    question_id: str = output.data.question.question_id
                                    print(f"({question_id})", end="", flush=True)
                                    with open(os.path.join(output_path, f), "r") as file:
                                        code = file.read()

                                    # Real submission
                                    submission = leetcode.Submission(
                                        judge_type="large", typed_code=code, question_id=question_id, test_mode=False, lang=lang
                                    )

                                    submission_id = api_instance.problems_problem_submit_post(
                                        problem=problem, body=submission
                                    )
                                    print("|Queued", end="", flush=True)

                                    sleep(TIME_SLEEP)

                                    submission_result = api_instance.submissions_detail_id_check_get(
                                        id=submission_id.submission_id
                                    )


                                    res = leetcode.SubmissionResult(**submission_result).to_dict()
                                    Path(
                                        os.path.join(result_path)
                                    ).mkdir(parents=True, exist_ok=True)
                                    with open(os.path.join(result_path, problem+".json"), "w") as f:
                                        json.dump(res, f)
                                    print("|Complete", end="", flush=True)
                                else:
                                    print("|Cache", end="", flush=True)
                                print("")