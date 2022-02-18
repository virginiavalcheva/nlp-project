import io
import json
import re

from nltk.tokenize import word_tokenize
from tfidf import get_closest_documents_indexes
from pos_tagger import transform_sentence_to_POS
from searcher_in_doc import return_right_answer
from constants import RESOURCE_FILENAME, QESTIONS_PATH_TO_FILE,\
                      NUMBER_OF_GOOGLE_WEBPAGES_TO_BE_SEARCHED
from bulstem import stem_word
from metrics import find_precision
from crawler import get_first_n_google_webpages_for_searched_string,\
                    get_responce_text_paragraphs
from termcolor import colored

def get_stop_words():
    stop_words_file = open("../resources/bulgarianST.txt", "r", encoding="utf-8")
    stop_words_txt = stop_words_file.read()
    stop_words_file.close()
    stop_words = stop_words_txt.split("\n")
    return stop_words

def clean_question(question):
    return re.sub(r'[^\w\s\-]', '', question)

def filter_question_words(question, stop_words):
    tokens = word_tokenize(question)
    filtered_question_words = []
    for token in tokens:
        if token.lower() not in stop_words:
            filtered_question_words.append(token)
    return filtered_question_words

def print_question_with_answers(question, answers, question_number):
    print("Въпрос %s: %s" % (question_number, question))
    print("A) %s" % answers[0])
    print("B) %s" % answers[1])
    print("C) %s" % answers[2])
    print("D) %s" % answers[3])
    print("-------------------------------------------------")

def check_if_answer_appears_in_document_words(answer, document):
    return answer in document

def find_answer_using_tfidf(documents, closest_documents_indexes, question, answers):
    answer_to_return = None
    for closest_document_index in closest_documents_indexes:
        closest_document = documents[closest_document_index]
        pos_tagged_sentence = transform_sentence_to_POS(question)
        answer = return_right_answer(answers, closest_document, pos_tagged_sentence)
        if answer:
            return answer
    return answer_to_return    

def read_resource_from_file(resource_name):
    resource_as_file = io.open(resource_name, mode="r", encoding="utf-8")
    resource_as_string = resource_as_file.read()
    return resource_as_string

def split_resource_in_documents_by_headings(resource):
    documents = re.split(r'\b[0-9][0-9]?\s[а-яА-Я\s,]+\n', resource)
    return documents

def read_questions_from_json():
    json_file = open(QESTIONS_PATH_TO_FILE, "r", encoding = "utf-8")
    data = json.load(json_file)
    json_file.close()
    return data

def main():
    resource_as_string = read_resource_from_file(RESOURCE_FILENAME)
    questions_data = read_questions_from_json()
    stop_words = get_stop_words()

    precision_sum = 0
    recall_sum = 0
    accuracy_sum = 0
    question_counter = 1
    for question in questions_data:
        documents = split_resource_in_documents_by_headings(resource_as_string)
        answers = questions_data[question]
        print_question_with_answers(question, answers, question_counter)
        cleaned_question = clean_question(question)
        filtered_question_words = filter_question_words(cleaned_question, stop_words)
        question_words_stemmed = [stem_word(i) for i in filtered_question_words]
        filtered_question_string = " ".join(question_words_stemmed)

        closest_documents_indexes = get_closest_documents_indexes(documents, filtered_question_string)

        #find precision of tf-idf algorithm
        if question_counter <= 10: 
            metrics = find_precision(question_counter, closest_documents_indexes)
            precision_sum += metrics[0]
            recall_sum += metrics[1]
            accuracy_sum += metrics[2]

        # tfidf usage
        answer = find_answer_using_tfidf(documents, closest_documents_indexes, filtered_question_string, answers)
        if answer:
            print(colored(answer, 'green'))
        else:
            print(colored("No answer found in the resource %s !" % RESOURCE_FILENAME, 'red'))
            print("Let's crawl the web for answer!")
            urls = get_first_n_google_webpages_for_searched_string(filtered_question_string)
            is_answer_found_on_the_web = False
            for url in urls:
                documents = get_responce_text_paragraphs(url)
                try:
                    closest_documents_indexes = get_closest_documents_indexes(documents, filtered_question_string)
                except ValueError:
                    pass
                else:
                    # tfidf usage
                    answer = find_answer_using_tfidf(documents, closest_documents_indexes, filtered_question_string,
                                                     answers)
                    if answer:
                        print(colored(answer, 'green'))
                        is_answer_found_on_the_web = True
                        break
            if not is_answer_found_on_the_web:
                print(colored("No answer found in the first %s webpages on the Internet!" % NUMBER_OF_GOOGLE_WEBPAGES_TO_BE_SEARCHED, 'red'))
        print("\n")
        question_counter += 1

        print("Средна прецизност:", precision_sum / 10)
        print("Средно връщане:", recall_sum / 10)
        print("Средна точност:", accuracy_sum / 10)

if __name__ == "__main__":
    main()





