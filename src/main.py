import re
from nltk.tokenize import word_tokenize

sentences = ["Каква е сложността на алгоритъма ЙАК?", "От къде започва тъсенето на термин в дърво за търсене?"]

cleaned_sentences = []
for sentence in sentences :
	cleaned_sentence = re.sub(r'[^\w\s\-]', '', sentence)
	cleaned_sentences.append(cleaned_sentence)

#read stop words from file
file = open("../resources/bulgarianST.txt", "r", encoding="utf-8")
file_txt = file.read()
stop_words = file_txt.split("\n")
file.close()

#extract stop words from question
for cleaned_sentence in cleaned_sentences : 
	tokens = word_tokenize(cleaned_sentence)

	filtered_sentence = []
	for token in tokens: 
		if token.lower() not in stop_words:
			filtered_sentence.append(token)
	print(filtered_sentence)

