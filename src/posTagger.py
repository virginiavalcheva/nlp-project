import spacy

#pos-tagging
nlp = spacy.load("ru_core_news_sm")
my_question = 'Каква e сложността на алгоритъма ЙАК?'
def transformSentenceToPOS(my_question):
    doc = nlp(my_question)
    result = []
    for token in doc:
        weight = 0
        if(token.pos_ == 'PROPN'):
            weight = 3
        elif(token.pos_ == 'NOUN' or token.pos_ == 'VERB'):
            weight = 2
        elif(token.pos_ == 'ADJ' or token.pos_ == 'ADV'):
            weight = 1
        tuple = (token.text, token.pos_, weight)
        result.append(tuple)
    print(result)
    return result
    
transformSentenceToPOS(my_question)

