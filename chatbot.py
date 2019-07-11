#Building a chatbot with movie conversation dataset

#import Libraries
import numpy as np
import tensorflow as tf #for tensorflow 
import re #for regular expression
import time # meansure training time

#========================= PART 1 - DATA PREPROCESSING =========================

#import the dataset
lines = open('movie_lines.txt',encoding = 'utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt',encoding = 'utf-8', errors='ignore').read().split('\n')

#Create a dictionary that maps each line and its ID
id2line = {}
for line in lines:
    #Extract ID and response text
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
#create a list of all the conversations
conversations_ids = []
for conversation in conversations[:-1]:
    #take the last element only
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","") #replace '' with nothing and remove space from input 
    #create a list of list, each list in this list is a conversation 
    conversations_ids.append(_conversation.split(','))
#Get questions and answers seperately
questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        #using the key ID to pull out conversation
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
        
#Do a first cleaning of texts
def clean_text(text):
    text = text.lower()
    #Remove apostrophe
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,'$*!&]", "", text)
    return text

#Cleaning the questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
#Cleaning the questions
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    
#Create a dictionary that maps each word to its number of occurences
word2count = {}
#count words in questions
for question in clean_questions:
    for word in question.split():
    #if the word is not on the list, count as the first time
        if word not in word2count:
            word2count[word] = 1
    #if the word is already in the list, increment occurence by 1
        else:
            word2count[word] +=1
#count words in answers
for answer in clean_answers:
    for word in answer.split():
    #if the word is not on the list, count as the first time
        if word not in word2count:
            word2count[word] = 1
    #if the word is already in the list, increment occurence by 1
        else:
            word2count[word] +=1
#Tokinization and remove least frequent words
#Create two dictionaries that map the question words and the answers words to a unique integer
threshold = 20
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1
answerswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1
        
# Add the last tokens to these two dictionaries
tokens = ['<PAD>','<EOS>', '<OUT>','<SOS>']
for token in tokens:
    #choose an integer that is not in the list
    questionswords2int[token] = len(questionswords2int) + 1
for token in tokens:
    #choose an integer that is not in the list
    answerswords2int[token] = len(answerswords2int) + 1
#Create an inverse dictionary of answerswords2int dictionary
answersints2word = {w_i: w for w, w_i in answerswords2int.items()}

#Adding the End of String token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS> ' 

#Translate all questions and answers into integers
#and Replaceing all the words filtered by <OUT>
questions_into_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_into_int.append(ints)
answers_into_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)

#Sorting questions and answers by the length of questions
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25 + 1):
    for i in enumerate(questions_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_into_int[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])
    




        
    