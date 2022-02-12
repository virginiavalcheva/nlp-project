import re
from nltk.tokenize import word_tokenize
from pos_tagger import get_words_from_tuples
from pos_tagger import sort_by_weight
from pos_tagger import transform_sentence_to_POS
from pos_tagger import get_weight
from pos_tagger import get_word

#read file
def get_file_content(file_name):
    file = open(file_name, "r", encoding="utf-8")
    return file.read()

#split the text by "."
def split_text(text):
    sentences = text.split('.')
    return sentences
 
#get sentences weight 
#[(1:indexed sentence, 8:weight)]
#sorted_tuples [(),(),(alg,noun,3)]
def get_sentences_weight(sentences, sorted_tuples) :
    sentences_weight = []
    words_from_tuples = get_words_from_tuples(sorted_tuples)       
    for sentence in sentences :
        sum_weight = 0
        words = sentence.split(" ")
        for word in words :
            if (word in words_from_tuples) :
                for tuple in sorted_tuples :
                    if(word == get_word(tuple)) :
                        sum_weight = sum_weight + get_weight(tuple)
        
        sentence_index = sentences.index(sentence)
        created_tuple = (sentence_index, sum_weight)
        sentences_weight.append(created_tuple)
    return sentences_weight

#[(1:indexed sentence, 8:weight)]  -> 8
def get_weight_from_indexed_sentences(element) :
    return element[1]

#sort a list based on the weight parameter in the tuple     
def sort_sentences_by_weight(elements):
    elements.sort(key=get_weight_from_indexed_sentences, reverse = True)
    return elements  

#(0,8)->0
def get_sentence_index(sentence_pair):
    return sentence_pair[0]
    
#return the right answer
def return_right_answer(answers, file_content, pos_tagged_sentence) :
    sorted_tuples = sort_by_weight(pos_tagged_sentence)
   # file_content = get_file_content(file_name)
    sentences = split_text(file_content)
    sentences_weight = get_sentences_weight(sentences, sorted_tuples)
    sorted_sentences = sort_sentences_by_weight(sentences_weight)
    for sentence_pair in sorted_sentences :
        sentence_index = get_sentence_index(sentence_pair)
        sentence = sentences[sentence_index]
        for answer in answers :
            if(answer in sentence) :
                return answer
    

