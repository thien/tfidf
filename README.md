---
title: "Web Technologies Assignment"
author: cmkv68
geometry: "left=1.5cm,right=1.5cm,top=1.5cm,bottom=1.5cm"
output: pdf_document
---

<!--  
• Report - 35%
  – Background - 5%
  – Implementation description and comparison of techniques - 10%
  – Presentation and analysis of results - 10%
  – Conclusion - 5%
  – Writing style, structure, grammar and presentation - 5%
-->

# Background Information
<!-- Some background information on the problem area -->
There is a copious amount of information on the internet. This is a double edged sword where the cons involve the incapability to comprehend most of the information around. There are attempts to solve the issue, with the introduction of text summarisation techniques. This depends on two relatively simple calculations, one of which involves calculating a histogram of words in an article (known as term frequency), and another refers to calculating the uniqueness of a given word in an article, called (Term Frequency - Inverse Document Frequency). In this report I will attempt to evalulate their effectiveness in a summariser program that determines sentences to choose based on the weights of their words. The summariser program takes in various articles (all of which have some relevancy with each other), and attempts to condense them into a single concise paragraph.

## Data Sanitisation

As the data itself is relatively clean, sanitisation was not necessarily thorough. It consisted of converting the articles to lowercase, removing line breaks, duplicate quotes and apostrophies, and other punctuation. A dataset of stopwords was produced in the form of a hash table, implemented in the form of a python dictionary with each stopword having a key. This improved the performance due as identifying whether a word is a given stopword can be performed in $O(1)$ time. Each article also has their stopwords removed. This allowed each document to have a sanitised model of their article, consisting of a list of sanitised words in the order they are mentioned in the article.

## Term Frequency

Note: _both `assignment.py` and `helpers.py` contains comments that may assist in the understanding of the code._

For each document, A new object, called `words` is created within the `document` object. The words in the document's cleaned structure is iterated through. For each word, it is checked whether it exists in the `words` object as a key. If it isn't, it is created with an initial value of 1. Otherwise it is incremented.

Each term is stored in the form of a dictionary, with the word as the key, and its frequency as the value pair. Like the stopwords, this is used to improve the read performance, allowing lookup to perform in $O(1)$ time.

## Term Frequency - Inverse Document Frequency

This depends on the term frequency program being executed prior. A new object called `df` is created at the root of the dataset object. `df` represents the words that appear in each document. Each document is iterated through its `tf` keys (which represent unique words in the document). The keys are added to the `df` object in the same vein as the articles words are added to `tf` in _Term Frequency_. This ensures that there are no duplicate admissions in the process. 

The intution behind this is that words with a high document frequency are common words. This makes them less valulable for distinguishing words that are unique to an article.

Once the document frequency has been counted, Each word in a document is iterated to calculate their  `tfidf` value with the simple formula $tfidf=tf*(1/df)$. They can be created as their own object, stored in the document object. 

## Simple Summarisation
A document's sentences are split via the expression `(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s`, and are index based on their position in the document. For each sentence, a sanitised model was constructed in the same vein as what the articles were originally scrutinised against in Data Sanitisation. Stop words are also removed from the sanitised model of a given sentence. Both sentences are stored in a dictionary.

Each sanitised sentence is now ranked based on the words it consisted of. There are two options in terms of ranking, `"tf"`, and `"tfidf"`. The ranking options can be configured in the parameters of the function `summarise()`. For the document it accumulates the weight of the article by summing up the score of the words based on their ranking. 

The sentences are then sorted based on their score, acummulated in the previous section. This allows the most significant sentences to appear before their weaker counterparts. At this stage, a summarisation string containing the sentences is constructed. A loop iterates through the sentences (starting with the highest weighted). For each sentence, its length in terms of words $l_{s}$ is counted, and compared against the current word length of the summary string $l_{x}$. If the sum of the two counters are less than the word limit then the sentence is concatenated to the summary string. If they are greater, than they are ignored. Once the `for` loop has finished, we return the summarised string, containing a summary of the article.

## Advanced Summarisation
The advanced summarisation works similarly to the simple advanced summarisation, but includes additional tweaks:

- Once a sentence is chosen, the weights of the sentences are recalibrated by recalculating the term frequencies of the remaining sentences, and a new sentence is chosen from the remaining options in a loop. This applies to both TF and TF-IDF.
- Structural approaches are considered in the weight of the sentences by calculating the ratio $\alpha$ of the number of words in the summary against the word limit For instance, i.e. if there are 60 words in the summary already, against a word limit of 150, then the ratio is $\alpha=60/150$. The remaining sentences are then given a index score $\beta$ based on their position in the article. For instance, For an article with 9 sentences, sentence 1 would have a score of 1/9, and sentence 7 will have a score of $\beta = 7/9$. Each sentence is then scored using the formula $(\alpha - \beta)^{-1}$. Scores closer to each other will be weighed higher than those who are not. 
- Sentence similarity scores are calculated for each remaining sentence, such that sentences containing similar words to what is currently present in the article are scored lower than sentences that do not. This is calculated by summiung the number of matching words in the sentence and returning the inverse value of the sum.

The advanced method is used as the base to create a multi-document summarisation. Similar methods apply, but we instead choose from a list of all the sentences from all of the documents, when it comes to summarisation. Scores for each sentences in terms of structural approaches are calculated relative to the document the sentence appears in. Sentence similarity scores compare the sentence of a document against the present sentences in the summary.

# Comparison of Different Techniques

  100 Words:

    tf (Adv) Results: 
    Two times now, SpaceX has sent a Dragon cargo capsule to space and back two times. Falcon Heavy's 
    successful launch opened a new chapter for SpaceX. FALCON Heavy, the highly anticipated SpaceX 
    rocket, blasted into orbit on Tuesday as Elon Musk rewrote the history books with the incredible 
    feat. Gwynne Shotwell, president and COO of SpaceX, told Ashlee Vance, author of Elon Musk: How
    The Billionaire CEO of SpaceX and Tesla is Shaping Our Future: “Our Falcon Heavy will not take a 
    busload of people to Mars. So, there’s something after Heavy.  

    tfidf (Adv) Results: 
    Two times now, SpaceX has sent a Dragon cargo capsule to space and back two times. Falcon Heavy's
    successful launch opened a new chapter for SpaceX. Elon Musk's Boring Company has presented plans
    to build a tunnel under Culver City, California for a Hyperloop-like transport system. FALCON 
    Heavy, the highly anticipated SpaceX rocket, blasted into orbit on Tuesday as Elon Musk rewrote 
    the history books with the incredible feat. "It seems surreal to me," said Elon Musk, proprietor 
    of SpaceX, and for once he was understating things. There's no Dragon capsule that's been used 
    three times - yet.  

  200 Words:

    tf Results: 
    "It seems surreal to me," said Elon Musk, proprietor of SpaceX, and for once he was understating 
    things. Two times now, SpaceX has sent a Dragon cargo capsule to space and back two times. Falcon 
    Heavy's successful launch opened a new chapter for SpaceX. FALCON Heavy, the highly anticipated 
    SpaceX rocket, blasted into orbit on Tuesday as Elon Musk rewrote the history books with the 
    incredible feat. Elon Musk's personal Tesla might have gotten all the headlines during SpaceX's 
    historic rocket launch last week, but the Falcon Heavy also carried a second, secret payload 
    almost nobody knew about. and we’re aspiring to fly crew to orbit at the end of this year.”  Elon 
    Musk himself said that he'd consider Tuesday's launch a "win" if the Falcon Heavy rocket makes it 
    "far enough away from the pad that it doesn't cause pad damage."  And after the successful launch 
    he said: “It seems surreal to me." He added: “I had this image of a giant explosion on the pad, a 
    wheel bouncing down the road and a Tesla logo landing somewhere. So, there’s something after 
    Heavy.  Here are six key facts you need to know about Falcon Heavy.  

    tfidf Results: 
    "It seems surreal to me," said Elon Musk, proprietor of SpaceX, and for once he was understating 
    things. Two times now, SpaceX has sent a Dragon cargo capsule to space and back two times. Donald 
    Trump's administration could announce in their proposed budget that they intend to cease funding 
    for operations to the ISS by 2025. Given the events of the past few weeks, says The Weekly 
    Standard's Ethan Epstein, the games that open Friday "should be re-christened the Pyongyang 
    Olympics." Because "what should have been a celebration of South Korea's titanic cultural, 
    economic and political achievements is degenerating into an event that will instead normalize the 
    barbarous North Korean regime that wants to destroy the South." Now comes word that Kim Jong-un's 
    sister, who has been sanctioned by the US for human-rights abuses, will attend the opening 
    ceremonies, the first-ever visit to South Korea by a member of the ruling family. Elon Musk's 
    Boring Company has presented plans to build a tunnel under Culver City, California for a 
    Hyperloop-like transport system. There's no Dragon capsule that's been used three times - yet.  
    Surreal, yes.  The reusability didn't stop with the Dragon capsule for this mission.  

<!-- Analyse the results of applying your programs to the documents on duo. -->
<!-- Think about whether the summaries produced seem accurate and read coherently for different lengths of summary -->
There are cases that both TF and TFIDF produce similar results. Both produce relatively coherent paragraph given a short word limit constraint. This is less of a case however in some scenarios, such as the original sentences being very long or that sentences are not separated precisely. This is more of the fault of the sanitisation process. It seems to produce worse results given a larger word limit, as there is the chance for some significant sentences to embed themselves even though they are largely unrelated to the rest of the content of the summary. This is more pronounced in TF-IDF. There exists some redundancies in the 200 words tf, where the same quote is provided twice ("It seems surreal to me").

The data itself can be shown by running the program `assignment.py` in a python3 interpreter. The folder called "Test Data" is to be created, which contains the text files that will be used in our program. More instructions are shown in `assignment.py` itself.

# Conclusion

In the event that the assignment can be continued, various considerations would take place to improve the performance of the summariser:

- Incorporating structural/location information of a word in a given sentence.
- Improved word filtering when it comes to article sanitisation for stop words. This may include improved regular expressions, known acronym substitutions and so on.
- Looking at the grammatical cases for a given word, i.e apostrophes to be broken off as they do not provide significant information in terms of word frequency.
- Looking at word tense and substitutions, i.e convert sentences to present tense.
- Presently, regular expression breaks quotes with multiple sentences in them, which should not be the case.
- Restructuring the summarised sentences to further condense the information, which would lead to less words utilised, whilst conveying the same semantics.
- During sentence scoring, sentences that are longer tend to have more weighting since there is more words available for scoring. This can be solved with breaking down the sentences into separate constituent sentences.