"""

To run this program, create a folder called "Test Files" which is in the same directory as this file, and add the test documents in that folder. The project directory should look like this:

  ./assignment.py
  ./helpers.py
  ./Test Files/Doc 1.txt
  ./Test Files/Doc 2.txt
  ./Test Files/Doc 3.txt
  ./Test Files/Doc 4.txt
  ./Test Files/Doc 5.txt
  ./Test Files/Doc 6.txt
  ./Test Files/Doc 7.txt
  ./Test Files/Doc 8.txt

Once that is done, simply run python3 assignment.py 
DO NOT USE PYTHON2 IT WILL NOT WORK. USE PYTHON3!

"""

import helpers

def tf(document, advanced=False):
  terms = {}
  for word in document['cleaned']:
    if word not in terms.keys():
      terms[word] = 1
    else:
      terms[word] += 1
  return terms

def tfOnAllDocuments(data):
  documents = data['documents']
  for doc in documents:
    document = documents[doc]
    document['tf'] = tf(document)
    documents[doc] = document
  data['documents'] = documents
  return data

def df(documents):
  documents = data['documents']
  df = {}
  for document in documents:
    for word in documents[document]['tf']:
      # look through the word and see if it exists in 
      if word not in df.keys():
        df[word] = 1
      else:
        df[word] += 1
  # allocate df at the end.
  data['df'] = df
  return data

def tfidf(data):
  documents = data['documents']
  for doc in documents:
    document = documents[doc]
    document['tfidf'] = {}

    for word in document['tf']:
      weight = document['tf'][word] / data['df'][word]
      document['tfidf'][word] = weight
    documents[doc] = document
  data['documents'] = documents
  return data

def summariseBasic(document, word_limit=100, freq="tfidf", debug=False):
  summary = ""
  raw_base = "".join(document['raw'].copy())
  sentences = {}
  counter = 0
  # split by periods and linebreaks
  raw_base = " ".join(raw_base.split("\n"))
  # split article into lists of sentences
  raw_base = helpers.splitBySentence(raw_base)

  # add them to the dictionary so we can analyse them
  for i in raw_base:
    # clean sentence of junk
    cleaned = helpers.clean(i)
    # remove stopwords
    cleaned = helpers.removeStopwords("".join(cleaned))
    # add to dictionary
    sentences[counter] = {
      "raw" : i,
      "clean" : cleaned,
      "worth" : 0
    }
    counter += 1
  
  # look for freq header and decide on ranking term
  if freq != "tfidf":
    freq = "tf"

  # now we rank each sentence based on the use of words
  rankings = {}
  for sen in sentences:
    for word in sentences[sen]['clean']:
      if word in document[freq]:
        sentences[sen]['worth'] += document[freq][word]
    rankings[sen] = sentences[sen]['worth']

  # now we sort the sentences based on how relevant they are.
  rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)

  if debug:
    for i in rankings:
      print(i[0],sentences[i[0]]['raw'])

  # now we add sentences based on their score.
  for i in rankings:
    if len(summary.split(" ") + sentences[i[0]]['raw'].split(" ")) < word_limit:
      summary += sentences[i[0]]['raw'] + " "
  return summary

def summariseAdvanced(document, data, word_limit=100, freq="tfidf", debug=False):
  summary = ""
  raw_base = "".join(document['raw'].copy())
  sentences = {}
  counter = 0
  # split by periods and linebreaks
  raw_base = " ".join(raw_base.split("\n"))
  # split article into lists of sentences
  raw_base = helpers.splitBySentence(raw_base)
  # add them to the dictionary so we can analyse them
  for i in raw_base:
    # clean sentence of junk
    cleaned = helpers.clean(i)
    # remove stopwords
    cleaned = helpers.removeStopwords("".join(cleaned))
    # add to dictionary
    sentences[counter] = {
      "raw" : i,
      "clean" : cleaned,
      "worth" : 0
    }
    counter += 1
  # keep track of the original number of sentences
  maxSentences = len(sentences)

  # look for freq header and decide on ranking term
  if freq != "tfidf":
    freq = "tf"

  # have a loop that breaks when we've reached the word limit
  # or we've gone through all the sentences.
  counter = 0
  used_words = []

  while (len(summary.split(" ")) < word_limit) and (counter < len(sentences)):
    # RANKING SYSTEM
    # rank each sentence based on the use of words
    rankings = {}
    max_word_score = 0

    # this loop counts the weights of the sentences using the weights
    # of the words.
    for sen in sentences:
      sentences[sen]['word_score'] = 0
      # tally up the word weights
      for word in sentences[sen]['clean']:
        if word in document[freq]:
          sentences[sen]['word_score'] += document[freq][word]
      # update the maximum word score to normalise the score values
      if sentences[sen]['word_score'] > max_word_score:
        max_word_score = sentences[sen]['word_score']
    
    # we use a separate loop to normalise the word weights
    for sen in sentences:
      similarity_score = 1
      word_score = sentences[sen]['word_score'] / max_word_score
      # check for sentence similarity (if there are words that are in this
      # sentence that are also used already, then its ranked lower)
      for used_word in used_words:
        if used_word in sentences[sen]['clean']:
          similarity_score += 1
      # invert the score so we have an idea of how unique the sentence is
      # in regards to the context of the original article.
      uniqueness_score = round(1/similarity_score,3)

      # look at where the sentence is and compare it to how far in the
      # summary we're in.
      position_ratio = sen/maxSentences
      present_summary_fill_fraction = len(summary.split(" ")+sentences[sen]['clean'])/word_limit
      relative_position_score = 1/(present_summary_fill_fraction-position_ratio)

      # calculate overall score
      overall_score = round(1/4*(relative_position_score * uniqueness_score)+ (3/4*word_score), 2)

      # allocate score to sentence
      sentences[sen]['worth'] = overall_score
      rankings[sen] = sentences[sen]['worth']
    

    # now we sort the sentences based on how relevant they are.
    rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    # get the ID of the best ranked sentence, and the sentence itself.
    best_ID = rankings[0]
    best_sentence = sentences[best_ID[0]]['raw']
    best_cleaned = sentences[best_ID[0]]['clean']

    # now that we've found our sentence, we need to see whether it can fit.
    # otherwise we ignore the sentence and move on.
    if len((summary + best_sentence).split(" ")) <= word_limit:
      # add the raw sentence to our summary
      summary += best_sentence
      used_words = used_words + best_cleaned

    # Now that we've found the best sentence, we'll need to 
    # update the word weights so we can get the next best sentence.

    # delete the added sentence from the cleaned set.
    sentences.pop(best_ID[0], None) # remove from our list of sentences
    document['cleaned'] = " ".join(document['cleaned']).replace(" ".join(best_cleaned),"").split(" ")
    # update word weights by recalculating tf
    document['tf'] = tf(document)

    if freq == "tfidf":
      # we'll need to recalculate the tf-idf too (if we're using it.)
      data = df(data)
      data = tfidf(data)
      # find the current document in the whole dataset and store the new tfidf
      for doc in data['documents']:
        if data['documents'][doc]['raw'] == document['raw']:
          document['tfidf'] = data['documents'][doc]['tfidf']
          break

    # reset counter on current sentences that we're still considering
    for i in sentences: sentences[i]['worth'] = 0
    # update counter so we know that we've iterated through the sentences.
    counter += 1
  return summary

def multiDocumentSummary(documents, data, word_limit=100, freq="tfidf", debug=False):
  # get a dictionary of sentences to work with
  sentences = {}
  # get a list of the length of each article
  documentLength = {}

  for docID in documents:
    document = documents[docID]
    summary = ""
    raw_base = "".join(document['raw'].copy())
    counter = 0
    # split by periods and linebreaks
    raw_base = " ".join(raw_base.split("\n"))
    # split article into lists of sentences
    raw_base = helpers.splitBySentence(raw_base)
    # add them to the dictionary so we can analyse them
    for i in raw_base:
      # clean sentence of junk
      cleaned = helpers.clean(i)
      # remove stopwords
      cleaned = helpers.removeStopwords("".join(cleaned))
      # add to dictionary
      sentences[(docID,counter)] = {
        "raw" : i,
        "clean" : cleaned,
        "worth" : 0
      }
      # update sentence counter
      counter += 1
    # keep track of the original number of sentences
    documentLength[docID] = counter

  # look for freq header and decide on ranking term
  if freq != "tfidf":
    freq = "tf"

  # have a loop that breaks when we've reached the word limit
  # or we've gone through all the sentences.
  counter = 0
  used_words = []

  while (len(summary.split(" ")) < word_limit) and (counter < len(sentences)):
    # RANKING SYSTEM
    # rank each sentence based on the use of words
    rankings = {}
    max_word_score = 0

    # this loop counts the weights of the sentences using the weights
    # of the words.
    for sen in sentences:
      sentences[sen]['word_score'] = 0
      # tally up the word weights
      for word in sentences[sen]['clean']:
        document = documents[sen[0]]
        if word in document[freq]:
          sentences[sen]['word_score'] += document[freq][word]
      # update the maximum word score to normalise the score values
      if sentences[sen]['word_score'] > max_word_score:
        max_word_score = sentences[sen]['word_score']
    
    # we use a separate loop to normalise the word weights
    for sen in sentences:
      similarity_score = 1
      word_score = sentences[sen]['word_score'] / max_word_score
      # check for sentence similarity (if there are words that are in this
      # sentence that are also used already, then its ranked lower)
      for used_word in used_words:
        if used_word in sentences[sen]['clean']:
          similarity_score += 1
      # invert the score so we have an idea of how unique the sentence is
      # in regards to the context of the original article.
      uniqueness_score = 0
      if similarity_score > 0 and len(sentences[sen]['clean']) > 0:
        uniqueness_score = similarity_score/len(sentences[sen]['clean'])

      # look at where the sentence is and compare it to how far in the
      # summary we're in.
      position_ratio = sen[1]+1/documentLength[sen[0]]
      present_summary_fill_fraction = len(summary.split(" ")+sentences[sen]['clean'])/word_limit
      relative_position_score = 1/(present_summary_fill_fraction-position_ratio)

      # calculate overall score
      overall_score = round(1/8*(relative_position_score) + ((1/4)*uniqueness_score)+ (1/2*word_score), 2)

      # allocate score to sentence
      sentences[sen]['worth'] = overall_score
      rankings[sen] = sentences[sen]['worth']
    

    # now we sort the sentences based on how relevant they are.
    rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)


    # get the ID of the best ranked sentence, and the sentence itself.
    best_ID = rankings[0]
    best_sentence = sentences[best_ID[0]]['raw']
    best_cleaned = sentences[best_ID[0]]['clean']

    # now that we've found our sentence, we need to see whether it can fit.
    # otherwise we ignore the sentence and move on.
    if len((summary + best_sentence).split(" ")) <= word_limit:
      # add the raw sentence to our summary
      summary += best_sentence + " "
      used_words = used_words + best_cleaned

    # Now that we've found the best sentence, we'll need to 
    # update the word weights so we can get the next best sentence.

    # delete the added sentence from the cleaned set.
    sentences.pop(best_ID[0], None) # remove from our list of sentences
    document['cleaned'] = " ".join(document['cleaned']).replace(" ".join(best_cleaned),"").split(" ")
    # update word weights by recalculating tf
    document['tf'] = tf(document)

    if freq == "tfidf":
      # we'll need to recalculate the tf-idf too (if we're using it.)
      data = df(data)
      data = tfidf(data)
      # find the current document in the whole dataset and store the new tfidf
      for doc in data['documents']:
        if data['documents'][doc]['raw'] == document['raw']:
          document['tfidf'] = data['documents'][doc]['tfidf']
          break

    # reset counter on current sentences that we're still considering
    for i in sentences: sentences[i]['worth'] = 0
    # update counter so we know that we've iterated through the sentences.
    counter += 1
  return summary


def summariseIndividualReports(data, word_limit=100):
  # In the event that you wish to read a summary of 
  # individual documents, then it is possible by calling this function.

  for documentID in data['documents']:
    # clear screen
    print(chr(27) + "[2J")
    # show document ID
    print(documentID, "\n") 
    # create report summaries
    document = data['documents'][documentID]
    summary = summariseBasic(document, word_limit, freq="tf")
    print("TF (Sim) Results:")
    print(summary,"\n")
    summary = summariseBasic(document, word_limit, freq="tfidf")
    print("TFIDF (Sim) Results:")
    print(summary,"\n")
    summary = summariseAdvanced(document, data, word_limit, freq="tf")
    print("TF (Adv) Results:")
    print(summary,"\n")
    summary = summariseAdvanced(document, data, word_limit, freq="tfidf")
    print("TFIDf (Adv) Results:")
    print(summary,"\n")
    input("Press enter to show the next article:")

if __name__ == "__main__":
  word_limit = 200
  # load documents and preprocess them
  documents = helpers.openFolderContents()
  documents = helpers.processDocuments(documents)
  # initialise data set which will allow us to process df
  data = {
    'documents' : documents,
    'df' : {}
  }
  # run term frequency (Words!)
  data = tfOnAllDocuments(data)
  # run document frequency
  data = df(data)
  # run tf-idf
  data = tfidf(data)
  # summarise individual reports
  # summariseIndividualReports(data, word_limit)

  summary = multiDocumentSummary(data['documents'], data, word_limit, freq="tf")
  print("tf Results: \n", summary, "\n")

  summary = multiDocumentSummary(data['documents'], data, word_limit, freq="tfidf")
  print("tfidf Results: \n", summary, "\n")