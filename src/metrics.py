from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

doc_ids = list(range(0, 310))

gold = [[200, 207, 197],
        [27, 28, 82],
        [28, 26, 27],
        [41, 92, 42],
        [196, 198, 238],
        [247, 249, 359],
        [260, 253, 266],
        [264, 305, 263],
        [254, 263, 266],
        [263, 261, 139]]

def to_vector(doc_ids, doc_set):
    return [1 if doc in doc_set else 0 for doc in doc_ids]


def find_precision(question_idx, result):
    print("Метрики за въпрос %s" % (question_idx))
    print(result)

    #1 in the vector of gold annotations means that the document at this position is relevant to the query
    gold_v = to_vector(doc_ids, gold[question_idx - 1])
    #1 in the vector of results means that the algorithm considers the document at this position as relevant
    actual_result_v = to_vector(doc_ids, result)

    #print("Верен извлечен     | Неверен извлечен")
    #print("Невярно неизвлечен | Вярно неизвлечен")
    #print(confusion_matrix(gold_v, actual_result_v))

    #частта на получените документи, които са уместни - уместно извлечени документи/извлечени документи
    print("Прецизност: ", precision_score(gold_v,actual_result_v))
    #частта от уместните документи, които са получени - извлечени документи/уместни документи
    print("Връщане: ", recall_score(gold_v, actual_result_v))
    #точност = (tp + tn) / (tp + fp + fn + pn)
    print("Точност: ", accuracy_score(gold_v,actual_result_v))

    print("-------------------------------------------------")
