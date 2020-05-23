import argparse
import json
import os


def merge_results(questions_path, answers_path, result):
    merged = []
    with open(questions_path, ) as questions, open(answers_path) as answers:
        questions_json = json.load(questions)
        answers_json = json.load(answers)
        for index, question in enumerate(questions_json):
            answer = answers_json[index]
            question["correct_answer"] = {"answer": answer["answer"],
                                          "answer_explanation": answer["answer_explanation"]}
            merged.append(question)

    with open(result, 'w') as output_file:
        json.dump(merged, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions', type=str)
    parser.add_argument('--answers', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()
    questions = args.questions
    answers = args.answers
    output = args.output

    for directory_path, _, filenames in os.walk(args.questions):
        for filename in filenames:
            merge_results(questions + filename, answers + filename, output + filename)
