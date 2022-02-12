import spacy

#pos-tagging
nlp = spacy.load("ru_core_news_sm")
def transform_sentence_to_POS(my_question):
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
        
        if(weight != 0):
            tuple = (token.text, token.pos_, weight)
            result.append(tuple)
    return result

#get weight  
def get_weight(element):
    return element[2]

#get word  
def get_word(element):
    return element[0]

#get all words from tuples
#("Алгоритъм", Noun, 2) -> Алгоритъм
def get_words_from_tuples(elements):
    result = []
    for element in elements:
        result.append(get_word(element))
    return result
    
#sort a list based on the weight parameter in the tuple     
def sort_by_weight(elements):
    elements.sort(key=get_weight, reverse = True)
    return elements


