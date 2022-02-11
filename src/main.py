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

def get_cleaned_questions(questions):
	cleaned_questions = []
	for question in questions:
		cleaned_question = re.sub(r'[^\w\s\-]', '', question)
		cleaned_questions.append(cleaned_question)
	return cleaned_questions

def get_filtered_questions(questions):
	filtered_questions = []
	stop_words = get_stop_words()
	for question in questions: 
		tokens = word_tokenize(question)
		filtered_question = []
		for token in tokens: 
			if token.lower() not in stop_words:
				filtered_question.append(token)
		filtered_questions.append(filtered_question)
	return filtered_questions

if __name__ == "__main__":
	f = io.open("IR_lecture_notes.txt", mode="r", encoding="utf-8")
	s = f.read()

	l = re.split(r'\b[0-9][0-9]?\s[а-яА-Я\s,]+\n', s)

	file_paths = glob.glob("../resources/files/text*.txt")
	documents = []
	for path in file_paths:
		file = open(path, "r", encoding="utf-8")
		file_txt = file.read()
		documents.append(file_txt)

	json_file = open("../resources/questions.json", "r", encoding="utf-8")
	data = json.load(json_file)
	json_file.close()

	questions = []
	answers = []
	for obj in data:
		questions.append(obj)
		answers.append(data[obj])
		
	cleaned_questions = get_cleaned_questions(questions)
	filtered_questions = get_filtered_questions(cleaned_questions)

	print(filtered_questions)
	print(" ".join(filtered_questions[3]))
	closest_document = get_closest_document(l, " ".join(filtered_questions[3]))
	print(closest_document)

