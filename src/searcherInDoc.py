import re
from nltk.tokenize import word_tokenize
from posTagger import get_words_from_tuples
from posTagger import sort_by_weight
from posTagger import transform_sentenc_to_POS
from posTagger import get_weight
from posTagger import get_word

fileName = "../resources/doc.txt"
#read file
def getFileContent(fileName):
    file = open(fileName, "r", encoding="utf-8")
    return file.read()

#split the text by "."
def splitText(text):
    sentences = text.split('.')
    return sentences
 
#get sentences weight 
#[(1:indexed sentence, 8:weight)]
#sorted_tuples [(),(),(alg,noun,3)]
def getSentencesWeight(sentences, sorted_tuples) :
    sentencesWeight = []
    wordsFromTuples = get_words_from_tuples(sorted_tuples)
        
    for sentence in sentences :
        sum_weight = 0
        words = sentence.split(" ")
        for word in words :
            if (word in wordsFromTuples) :
                for tuple in sorted_tuples :
                    if(word == get_word(tuple)) :
                        sum_weight = sum_weight + get_weight(tuple)
        
        
        sentence_index = sentences.index(sentence)
        created_tuple = (sentence_index, sum_weight)
        sentencesWeight.append(created_tuple)
    
    return sentencesWeight

print(getSentencesWeight(splitText(getFileContent(fileName)), transform_sentenc_to_POS('В кое училище е записан Алън Тюринг')))

#get weight 
#[(1:indexed sentence, 8:weight)]  -> 8
def getWeightFromSentencesList(element) :
    return element[1]

#sort a list based on the weight parameter in the tuple     
def sort_by(elements):
    elements.sort(key=getWeightFromSentencesList, reverse = True)
    return elements  

#(0,8)->0
def get_sentence_index(sentence_pair):
    return sentence_pair[0]
    
#return the right answer
def returnRightAnswer(answers, fileName, pos_tagged_sentences) :
    sorted_tuples = sort_by_weight(pos_tagged_sentences)
    #wordsFromTuples = getWordsFromTuples(sorted_tuples)
    wordsFromTuples = get_words_from_tuples(sorted_tuples)
    fileContent = getFileContent(fileName)
    sentences = splitText(fileContent)
    sentencesWeight = getSentencesWeight(sentences, sorted_tuples)
    sorted_sentences = sort_by(sentencesWeight)
    #sentencesWeight.sort(key=getWeightFromSentencesList)
    #sorted_sentences = [(0, 8), (1, 0), (2, 2), (3, 0), (4, 0)]
    for sentence_pair in sorted_sentences :
        sentence_index = get_sentence_index(sentence_pair)
        sentence = sentences[sentence_index]
        for answer in answers :
            if(answer in sentence) :
                return answer
    

answers = ['Сейнт Майкълс', 'бляв', 'вад']
print(returnRightAnswer(answers, fileName, transform_sentenc_to_POS('В кое училище е записан Алън Тюринг')))

#generate n-gramms
#def defineNGrammsFromQuestion(question):     
    
#def generate_ngrams(fileName, WordsToCombine):
#     fileContent = getFileContent(fileName)
#     sentances = splitText(fileContent)
#     nGramms = defineNGrammsFromQuestions(question); 
#     for i in range(len(words)- WordsToCombine+1):
#         sentances.append(words[i:i+WordsToCombine])
#     print(sentances)
#     return sentances

 
#generate_ngrams("../resources/doc.txt", WordsToCombine=3)
