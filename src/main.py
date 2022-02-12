import re, json, glob, io

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from tfidf import get_closest_document

def get_stop_words():
	stop_words_file = open("../resources/bulgarianST.txt", "r", encoding="utf-8")
	stop_words_txt = stop_words_file.read()
	stop_words_file.close()
	stop_words = stop_words_txt.split("\n")
	return stop_words

def clean_question(question):
	return re.sub(r'[^\w\s\-]', '', question)

# def get_cleaned_questions(questions):
# 	cleaned_questions = []
# 	for question in questions:
# 		cleaned_question = re.sub(r'[^\w\s\-]', '', question)
# 		cleaned_questions.append(cleaned_question)
# 	return cleaned_questions

# def get_filtered_questions(questions):
# 	filtered_questions = []
# 	stop_words = get_stop_words()
# 	for question in questions:
# 		tokens = word_tokenize(question)
# 		filtered_question = []
# 		for token in tokens:
# 			if token.lower() not in stop_words:
# 				filtered_question.append(token)
# 		filtered_questions.append(filtered_question)
# 	return filtered_questions

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

if __name__ == "__main__":
	f = io.open("IR_lecture_notes.txt", mode="r", encoding="utf-8")
	s = f.read()

	l = re.split(r'\b[0-9][0-9]?\s[а-яА-Я\s,]+\n', s)

	# file_paths = glob.glob("../resources/files/text*.txt")
	# documents = []
	# for path in file_paths:
	# 	file = open(path, "r", encoding="utf-8")
	# 	file_txt = file.read()
	# 	documents.append(file_txt)

	json_file = open("../resources/questions.json", "r", encoding="utf-8")
	data = json.load(json_file)
	json_file.close()

	questions = []
	stop_words = get_stop_words()
	# answers = []
	c = 1
	for obj in data:
		answers = data[obj]
		print_question_with_answers(obj, answers, c)
		cleaned_question = clean_question(obj)
		filtered_question_words = filter_question_words(cleaned_question, stop_words)

		# print(filtered_question_words)
		# print(" ".join(filtered_question_words))
		closest_document = get_closest_document(l, " ".join(filtered_question_words))
		# closest_document_words = filter_question_words(closest_document, stop_words)
		closest_document = closest_document.replace('.', '')
		closest_document_words = closest_document.split(" ")
		if c == 5:
			print(closest_document)
		answers_found = []
		for answer in answers:
			if check_if_answer_appears_in_document_words(answer, closest_document):
				answers_found.append(answer)

		if answers_found:
			if len(answers_found) > 1:
				answers_found_as_whole_words = []
				for answer_found in answers_found:
					if check_if_answer_appears_in_document_words(answer_found, closest_document_words):
						answers_found_as_whole_words.append(answer_found)
				if answers_found_as_whole_words:
					if len(answers_found_as_whole_words) > 1:
						print("More than one answers found")
					else:
						print(answers_found_as_whole_words[0])
			else:
				print(answers_found[0])
		else:
			
			print("No answer found!")
		print("\n\n")
		c += 1

