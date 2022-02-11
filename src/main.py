import re, json
from nltk.tokenize import word_tokenize

#parse json file
json_file = open("../resources/questions.json", "r", encoding="utf-8")
data = json.load(json_file)
json_file.close()

questions = []
answers = []
for obj in data:
	questions.append(obj)
	answers.append(data[obj])

cleaned_questions = []
for question in questions :
	cleaned_question = re.sub(r'[^\w\s\-]', '', question)
	cleaned_questions.append(cleaned_question)

#read stop words from file
file = open("../resources/bulgarianST.txt", "r", encoding="utf-8")
file_txt = file.read()
stop_words = file_txt.split("\n")
file.close()

#extract stop words from question
for cleaned_question in cleaned_questions : 
	tokens = word_tokenize(cleaned_question)

	filtered_question = []
	for token in tokens: 
		if token.lower() not in stop_words:
			filtered_question.append(token)
	print(filtered_question)

