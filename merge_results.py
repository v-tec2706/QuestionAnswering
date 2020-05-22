import json

merged = []
with open('questions/adw_radc.json', ) as questions, open('answers/adw_radc.json') as answers:
    questions_json = json.load(questions)
    answers_json = json.load(answers)
    for _, question in questions_json.items():
        question_number = int(question["question_number"].replace(".", ""))
        question["question_number"] = question_number
        answer = answers_json[question_number - 1]
        question["correct_answer"] = {"answer": answer["answer"], "answer_explanation": answer["answer_explanation"]}
        merged.append(question)

with open("output/output.json", 'w') as output_file:
    json.dump(merged, output_file)
