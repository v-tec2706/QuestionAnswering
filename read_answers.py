import argparse
import json
import os

import camelot


def filter_description(description):
    return description.replace("\n", "") \
        .replace("<s>", "(") \
        .replace("</s>", ")")


def add_keys(element):
    return {"question_number": element[0].replace(".", ""),
            "answer": element[1],
            "answer_explanation": filter_description(element[2])}


def parseTable(input_data, output):
    tables = camelot.read_pdf(input_data, flag_size=True, pages='all')

    extracted_data = [element for table in tables for element in table.data]

    extracted_data_iter = iter(extracted_data)
    next(extracted_data_iter)

    extracted_data_as_dict = [add_keys(element) for element in extracted_data_iter]
    with open(output, 'w') as output_file:
        json.dump(extracted_data_as_dict, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()
    input = args.input
    output = args.output

    for directory_path, _, filenames in os.walk(args.input):
        for filename in filenames:
            parseTable(input + filename, output + filename.replace("pdf", "json"))
