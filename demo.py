# use natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

#this download required only once
nltk.download('punkt')
# word stemmer
stemmer = LancasterStemmer()

# 3 classes of training data
training_data = []

#Name intention
training_data.append({"class":"q1", "sentence":"What is your name"})
training_data.append({"class":"q1", "sentence":"Hi, What's your name"})
training_data.append({"class":"q1", "sentence":"Hey, What is your name"})
training_data.append({"class":"q1", "sentence":"By the way, What is your name"})
training_data.append({"class":"q1", "sentence":"Can I know your name"})
training_data.append({"class":"q1", "sentence":"May I know your name"})
training_data.append({"class":"q1", "sentence":"Your name please"})
training_data.append({"class":"q1", "sentence":"Could you tell me your name"})
training_data.append({"class":"q1", "sentence":"can you say your name"})
training_data.append({"class":"q1", "sentence":"By what name I can call you"})

#How Doing Intention
training_data.append({"class":"q2", "sentence":"How are you"})
training_data.append({"class":"q2", "sentence":"hey how you doing"})
training_data.append({"class":"q2", "sentence":"Are you ok"})
training_data.append({"class":"q2", "sentence":"Hope you are doing good"})
training_data.append({"class":"q2", "sentence":"is everything ok"})

#Experience Intention
training_data.append({"class":"q3", "sentence":"What's your experience"})
training_data.append({"class":"q3", "sentence":"How many years of experience you have"})
training_data.append({"class":"q3", "sentence":"Experience"})
training_data.append({"class":"q3", "sentence":"Can I know your experience"})
training_data.append({"class":"q3", "sentence":"May I know your experience"})

#Certificate Intention
training_data.append({"class":"q4", "sentence":"What's your location"})
training_data.append({"class":"q4", "sentence":"Where do you stay"})
training_data.append({"class":"q4", "sentence":"you are from"})
training_data.append({"class":"q4", "sentence":"coming from"})
training_data.append({"class":"q4", "sentence":"may I know where do you stay"})

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}

# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    class_words[c] = []

for data in training_data:
    for word in nltk.word_tokenize(data['sentence']):
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1
            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score

# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score
    # print(high_class)
    # print(high_score)
    if high_class == 'q1':
    	print('your intention is to know the name');
    elif high_class == 'q2':
    	print( 'Your intention is to check how am I doing')
    elif high_class == 'q3':
        print( 'Your intention is to know the Experience')
    elif high_class == 'q4':
        print( 'Your intention is to know the Location')
    else:
    	print( 'Sorry not found your intention')

question = input("What is your question? \n")
classify(question)