"""

This file shouldn't be called directly, I only call it for development purposes. You should be running assignment.py instead.

"""

import os
import re
from string import punctuation

stopwords = {
  "a": True, "a's": True, "able": True, "about": True, "above": True, "according": True, "accordingly": True, "across": True, "actually": True, "after": True, "afterwards": True, "again": True, "against": True, "ain't": True, "all": True, "allow": True, "allows": True, "almost": True, "alone": True, "along": True, "already": True, "also": True, "although": True, "always": True, "am": True, "among": True, "amongst": True, "an": True, "and": True, "another": True, "any": True, "anybody": True, "anyhow": True, "anyone": True, "anything": True, "anyway": True, "anyways": True, "anywhere": True, "apart": True, "appear": True, "appreciate": True, "appropriate": True, "are": True, "aren't": True, "around": True, "as": True, "aside": True, "ask": True, "asking": True, "associated": True, "at": True, "available": True, "away": True, "awfully": True, "b": True, "be": True, "became": True, "because": True, "become": True, "becomes": True, "becoming": True, "been": True, "before": True, "beforehand": True, "behind": True, "being": True, "believe": True, "below": True, "beside": True, "besides": True, "best": True, "better": True, "between": True, "beyond": True, "both": True, "brief": True, "but": True, "by": True, "c": True, "c'mon": True, "c's": True, "came": True, "can": True, "can't": True, "cannot": True, "cant": True, "cause": True, "causes": True, "certain": True, "certainly": True, "changes": True, "clearly": True, "co": True, "com": True, "come": True, "comes": True, "concerning": True, "consequently": True, "consider": True, "considering": True, "contain": True, "containing": True, "contains": True, "corresponding": True, "could": True, "couldn't": True, "course": True, "currently": True, "d": True, "definitely": True, "described": True, "despite": True, "did": True, "didn't": True, "different": True, "do": True, "does": True, "doesn't": True, "doing": True, "don't": True, "done": True, "down": True, "downwards": True, "during": True, "e": True, "each": True, "edu": True, "eg": True, "eight": True, "either": True, "else": True, "elsewhere": True, "enough": True, "entirely": True, "especially": True, "et": True, "etc": True, "even": True, "ever": True, "every": True, "everybody": True, "everyone": True, "everything": True, "everywhere": True, "ex": True, "exactly": True, "example": True, "except": True, "f": True, "far": True, "few": True, "fifth": True, "first": True, "five": True, "followed": True, "following": True, "follows": True, "for": True, "former": True, "formerly": True, "forth": True, "four": True, "from": True, "further": True, "furthermore": True, "g": True, "get": True, "gets": True, "getting": True, "given": True, "gives": True, "go": True, "goes": True, "going": True, "gone": True, "got": True, "gotten": True, "greetings": True, "h": True, "had": True, "hadn't": True, "happens": True, "hardly": True, "has": True, "hasn't": True, "have": True, "haven't": True, "having": True, "he": True, "he's": True, "hello": True, "help": True, "hence": True, "her": True, "here": True, "here's": True, "hereafter": True, "hereby": True, "herein": True, "hereupon": True, "hers": True, "herself": True, "hi": True, "him": True, "himself": True, "his": True, "hither": True, "hopefully": True, "how": True, "howbeit": True, "however": True, "i": True, "i'd": True, "i'll": True, "i'm": True, "i've": True, "ie": True, "if": True, "ignored": True, "immediate": True, "in": True, "inasmuch": True, "inc": True, "indeed": True, "indicate": True, "indicated": True, "indicates": True, "inner": True, "insofar": True, "instead": True, "into": True, "inward": True, "is": True, "isn't": True, "it": True, "it'd": True, "it'll": True, "it's": True, "its": True, "itself": True, "j": True, "just": True, "k": True, "keep": True, "keeps": True, "kept": True, "know": True, "known": True, "knows": True, "l": True, "last": True, "lately": True, "later": True, "latter": True, "latterly": True, "least": True, "less": True, "lest": True, "let": True, "let's": True, "like": True, "liked": True, "likely": True, "little": True, "look": True, "looking": True, "looks": True, "ltd": True, "m": True, "mainly": True, "many": True, "may": True, "maybe": True, "me": True, "mean": True, "meanwhile": True, "merely": True, "might": True, "more": True, "moreover": True, "most": True, "mostly": True, "much": True, "must": True, "my": True, "myself": True, "n": True, "name": True, "namely": True, "nd": True, "near": True, "nearly": True, "necessary": True, "need": True, "needs": True, "neither": True, "never": True, "nevertheless": True, "new": True, "next": True, "nine": True, "no": True, "nobody": True, "non": True, "none": True, "noone": True, "nor": True, "normally": True, "not": True, "nothing": True, "novel": True, "now": True, "nowhere": True, "o": True, "obviously": True, "of": True, "off": True, "often": True, "oh": True, "ok": True, "okay": True, "old": True, "on": True, "once": True, "one": True, "ones": True, "only": True, "onto": True, "or": True, "other": True, "others": True, "otherwise": True, "ought": True, "our": True, "ours": True, "ourselves": True, "out": True, "outside": True, "over": True, "overall": True, "own": True, "p": True, "particular": True, "particularly": True, "per": True, "perhaps": True, "placed": True, "please": True, "plus": True, "possible": True, "presumably": True, "probably": True, "provides": True, "q": True, "que": True, "quite": True, "qv": True, "r": True, "rather": True, "rd": True, "re": True, "really": True, "reasonably": True, "regarding": True, "regardless": True, "regards": True, "relatively": True, "respectively": True, "right": True, "s": True, "said": True, "same": True, "saw": True, "say": True, "saying": True, "says": True, "second": True, "secondly": True, "see": True, "seeing": True, "seem": True, "seemed": True, "seeming": True, "seems": True, "seen": True, "self": True, "selves": True, "sensible": True, "sent": True, "serious": True, "seriously": True, "seven": True, "several": True, "shall": True, "she": True, "should": True, "shouldn't": True, "since": True, "six": True, "so": True, "some": True, "somebody": True, "somehow": True, "someone": True, "something": True, "sometime": True, "sometimes": True, "somewhat": True, "somewhere": True, "soon": True, "sorry": True, "specified": True, "specify": True, "specifying": True, "still": True, "sub": True, "such": True, "sup": True, "sure": True, "t": True, "t's": True, "take": True, "taken": True, "tell": True, "tends": True, "th": True, "than": True, "thank": True, "thanks": True, "thanx": True, "that": True, "that's": True, "thats": True, "the": True, "their": True, "theirs": True, "them": True, "themselves": True, "then": True, "thence": True, "there": True, "there's": True, "thereafter": True, "thereby": True, "therefore": True, "therein": True, "theres": True, "thereupon": True, "these": True, "they": True, "they'd": True, "they'll": True, "they're": True, "they've": True, "think": True, "third": True, "this": True, "thorough": True, "thoroughly": True, "those": True, "though": True, "three": True, "through": True, "throughout": True, "thru": True, "thus": True, "to": True, "together": True, "too": True, "took": True, "toward": True, "towards": True, "tried": True, "tries": True, "truly": True, "try": True, "trying": True, "twice": True, "two": True, "u": True, "un": True, "under": True, "unfortunately": True, "unless": True, "unlikely": True, "until": True, "unto": True, "up": True, "upon": True, "us": True, "use": True, "used": True, "useful": True, "uses": True, "using": True, "usually": True, "uucp": True, "v": True, "value": True, "various": True, "very": True, "via": True, "viz": True, "vs": True, "w": True, "want": True, "wants": True, "was": True, "wasn't": True, "way": True, "we": True, "we'd": True, "we'll": True, "we're": True, "we've": True, "welcome": True, "well": True, "went": True, "were": True, "weren't": True, "what": True, "what's": True, "whatever": True, "when": True, "whence": True, "whenever": True, "where": True, "where's": True, "whereafter": True, "whereas": True, "whereby": True, "wherein": True, "whereupon": True, "wherever": True, "whether": True, "which": True, "while": True, "whither": True, "who": True, "who's": True, "whoever": True, "whole": True, "whom": True, "whose": True, "why": True, "will": True, "willing": True, "wish": True, "with": True, "within": True, "without": True, "won't": True, "wonder": True, "would": True, "wouldn't": True, "x": True, "y": True, "yes": True, "yet": True, "you": True, "you'd": True, "you'll": True, "you're": True, "you've": True, "your": True, "yours": True, "yourself": True, "yourselves": True, "z": True, "zero": True,  " ": True}

def splitBySentence(text):
  return re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

def clean(x):
  # lowercase
  x = x.lower()
  # separate by sentence to remove period cruft and join back.
  x = " ".join(splitBySentence(x))
  #remove line breaks
  x = x.split('\n')[0]
  # remove duplicate quotes
  x.replace('""', '"')
  x.replace('"', ' ')
  # remove apostrophies
  x = re.sub("'", " ", x)
  # remove punctuation
  x = ''.join(c for c in x if c not in punctuation)
  return x

def removeStopwords(x):
  # split words prior to submission
  x = x.split(" ")
  # remove empty strings
  x = list(filter(None, x))
  # remove stopwords
  x = [word.rstrip('.') for word in x if word not in stopwords.keys()]
  return x

def sanitise(text):
  for i in range(len(text)):
    text[i] = clean(text[i])
  # split string into a list of words
  cleaned = removeStopwords("".join(text))
  return cleaned

def processDocuments(documents):
  for i in documents:
    documents[i]['cleaned'] = sanitise(documents[i]['raw'].copy())
  return documents

def openFolderContents(folderPath="Test Files"):
  documents = {}
  for file in os.listdir(folderPath):
      if file.endswith(".txt"):
          filename = os.path.join(folderPath+"/", file)
          text_file = open(filename, "r")
          lines = text_file.readlines()
          documents[filename] = {
            "raw" : lines
          }
  return documents

if __name__ == "__main__":
  print("Loading articles in folder.. ",end="")
  documents = openFolderContents()
  documents = processDocuments(documents)
  print("Done.")