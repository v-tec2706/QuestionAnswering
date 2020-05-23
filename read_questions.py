import io
import re
import json
import os
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from argparse import ArgumentParser

# First if needed, you have to remove the front page with command
# pdftk in.pdf cat 2-end output out.pdf

different_footer_filenames = ['2007_adw', '2007_not', '2007_rad', '2012_kom', '2017_kom']

even_footer_pattern = '\s*\d+\s*EGZAMIN WSTĘPNY DLA KANDYDATÓW .+?(?=\d)'
odd_footer_pattern = '\s*EGZAMIN WSTĘPNY DLA KANDYDATÓW .+?(?=\d)\d+\s*'
different_even_footer_pattern = '\s*\d+\s*EGZAMIN KONKURSOWY DLA KANDYDATÓW .+?(?=\d)'
different_odd_footer_pattern = '\s*EGZAMIN KONKURSOWY DLA KANDYDATÓW .+?(?=\d)\d+\s*'
only_question_pattern = '\d+. (.+?(?=A))'
first_answer_pattern = 'A[.].+?(?=B)'
second_answer_pattern = 'B[.].+?(?=C)'
third_answer_pattern = 'C[.].+?(?=$)'


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text


def parse_questions_to_json(path_to_file, output_directory, output_filename):
    filename_without_extension = output_filename.replace(".json", "")

    parsed_text = extract_text_from_pdf(path_to_file)
    if filename_without_extension in different_footer_filenames:
        parsed_text = re.sub(different_even_footer_pattern, '', parsed_text)
        parsed_text = re.sub(different_odd_footer_pattern, '', parsed_text)
    else:
        parsed_text = re.sub(even_footer_pattern, '', parsed_text)
        parsed_text = re.sub(odd_footer_pattern, '', parsed_text)

    parsed_json = []

    current_number = 1
    next_number = 2
    is_not_finished = True

    while is_not_finished:
        question_pattern = f"{current_number}\. (.+?(?={next_number}\.|$))"
        full_question_match = re.search(question_pattern, parsed_text)
        if full_question_match is None:
            is_not_finished = False
        else:
            full_question = full_question_match.group()
            only_question = re.search(only_question_pattern, full_question).group(1)
            first_answer = re.search(first_answer_pattern, full_question).group()
            first_answer = re.sub("A. ", '', first_answer)
            second_answer = re.search(second_answer_pattern, full_question).group()
            second_answer = re.sub("B. ", '', second_answer)
            third_answer = re.search(third_answer_pattern, full_question).group()
            third_answer = re.sub("C. ", '', third_answer)

            answers = {'A': first_answer, 'B': second_answer, 'C': third_answer}
            question = {'question': only_question, 'answers': answers}

            parsed_json.append(question)

            current_number = next_number
            next_number += 1

    with open(os.path.abspath(os.path.join(output_directory, output_filename)), 'w+', encoding='utf-8') as file:
        json.dump(parsed_json, file, ensure_ascii=False, indent=4)


parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input", help="Input folder")
parser.add_argument("-o", "--output", dest="output", help="Output folder")

if __name__ == '__main__':
    args = parser.parse_args()

    for directory_path, _, filenames in os.walk(args.input):
        for filename in filenames:
            parse_questions_to_json(os.path.abspath(os.path.join(directory_path, filename)), args.output,
                                    filename.replace("pdf", "json"))
