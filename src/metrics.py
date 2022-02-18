from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

doc_ids = list(range(0, 310))

gold = [[200, 207, 203, 201, 196, 202, 183, 82, 174],
        [27, 28, 82, 26, 86, 306, 152, 220, 1, 222, 259],
        [28, 26, 27, 49, 86, 224, 85, 152, 25, 3, 5],
        [41, 91, 42, 126, 229, 83, 236, 5, 159, 240, 62, 6, 1],
        [196, 198, 238, 200, 117, 97, 116, 199, 53, 301, 205],
        [247, 249, 307, 208, 246, 128],
        [260, 253, 267],
        [264, 262, 263, 256, 275, 281, 257, 287, 288, 280, 56],
        [254, 263, 266, 296, 271, 295, 131, 239, 253, 155, 275],
        [263, 260, 138, 0, 90, 2, 128, 295, 105, 25],
        ]

def to_vector(doc_ids, doc_set):
    return [1 if doc in doc_set else 0 for doc in doc_ids]


def find_precision(question_idx, result):
    #print("Метрики за въпрос %s" % (question_idx))
    #print(result)

    #1 in the vector of gold annotations means that the document at this position is relevant to the query
    gold_v = to_vector(doc_ids, gold[question_idx - 1])
    #1 in the vector of results means that the algorithm considers the document at this position as relevant
    actual_result_v = to_vector(doc_ids, result)

    #print("Верен извлечен     | Неверен извлечен")
    #print("Невярно неизвлечен | Вярно неизвлечен")
    #print(confusion_matrix(gold_v, actual_result_v))

    #частта на получените документи, които са уместни - уместно извлечени документи/извлечени документи
    precision = precision_score(gold_v,actual_result_v)
    print("Прецизност:", precision)
    #частта от уместните документи, които са получени - извлечени документи/уместни документи
    recall = recall_score(gold_v, actual_result_v)
    print("Връщане:", recall)
    #точност = (tp + tn) / (tp + fp + fn + pn)
    accuracy = accuracy_score(gold_v,actual_result_v)
    print("Точност:", accuracy)

    print("-------------------------------------------------")
    return (precision, recall, accuracy)
