import re
import nltk
from html.parser import HTMLParser
from nltk.corpus import stopwords
import string
html_parser = HTMLParser()
import pyPdf

from pyPdf import PdfFileWriter, PdfFileReader

resume = PdfFileReader(open("/home/hachi/Downloads/10.pdf", "rb"))

for page in resume.pages:
    text_file = page.extractText()


from nltk.stem.wordnet import WordNetLemmatizer
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    final = ''.join([i for i in normalized if not i.isdigit()])
    return final

text_file1 = clean(text_file)

Res = nltk.tokenize.word_tokenize(text_file1)

cv = []
for i in range(0, len(Res), 10):
    cv+= [' '.join(Res[i:i+10])]
    

JP_skills = 'PHP, MySQL, MVC framework, open source testing tools, Git'
JP_designation = 'Software Engineer'
JP1 = JP_skills + JP_designation
exclude = set(string.punctuation)
JP2 = ''.join(ch for ch in JP1 if ch not in exclude)
JP = JP2.split()


import gensim
from gensim import corpora

clean_cv = [clean(doc).split() for doc in cv]
cleanwin = " ".join([clean(doc) for doc in cv])
dictionary = corpora.Dictionary(clean_cv)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_cv]

Lda = gensim.models.ldamodel.LdaModel

ldamodel = Lda(doc_term_matrix, num_topics = 15, id2word = dictionary, passes = 50)
topics1 = ldamodel.print_topics(num_topics = 15, num_words = 1)

topi = [x[1] for x in topics1]
topi_ = [topi[x][7:-1] for x in range(len(topi))]
topics = " ".join(topi_)

def levenshtein(s1,s2): 

    if len(s1) > len(s2):

        s1,s2 = s2,s1 

    distances = range(len(s1) + 1) 

    for index2,char2 in enumerate(s2):

        newDistances = [index2+1]

        for index1,char1 in enumerate(s1):

            if char1 == char2:

                newDistances.append(distances[index1]) 

            else:

                 newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1]))) 

        distances = newDistances 

    return distances[-1]

JP_ = " ".join(JP)

lev = levenshtein(topics, JP_)

score = ((1 - (lev/((len(cleanwin)*len(JP_))**0.5)))-0.55)/(0.9-0.55)
print(lev)
print(score)


