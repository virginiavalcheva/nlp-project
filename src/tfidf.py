from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_score(query, vectorizer, train_corpus_vectors, top_n=2):
    # compute similarity to all sentences in the training corpus
    similarities = cosine_similarity(vectorizer.transform([query]), train_corpus_vectors).flatten()
    # get indexes of top n closest sentences
    related_docs_indices = similarities.argsort()[:-top_n-1:-1]
    # return tuples of (similarity score, document id)
    return [(similarities[idx], idx)  for idx in related_docs_indices]

def get_closest_documents_indexes(documents, query):
	tfidf_vectorizer = TfidfVectorizer(min_df=2)

	#fit goes through the provided documents and collects the vocabulary
	#transform transforms documents in text representation to a vector representation according to the vocabulary
	tfidf_vectorizer.fit_transform(documents).toarray()
	tfidf_vectorizer.vocabulary_

	#vectorizer should be fit on the documents beforehand
	train_corpus_vectors = tfidf_vectorizer.transform(documents)

	closest_documents = get_similarity_score(query, tfidf_vectorizer, train_corpus_vectors)
	return [i[1] for i in closest_documents]
	# return documents[closest_documents[1][1]]