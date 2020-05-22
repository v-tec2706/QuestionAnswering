import argparse
import json


def merge_results(questions_path, answers_path, result):
    merged = []
    with open(questions_path, ) as questions, open(answers_path) as answers:
        questions_json = json.load(questions)
        answers_json = json.load(answers)
        for _, question in questions_json.items():
            question_number = int(question["question_number"].replace(".", ""))
            question["question_number"] = question_number
            answer = answers_json[question_number - 1]
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
    merge_results(questions, answers, output)
