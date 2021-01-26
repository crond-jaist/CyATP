from training_content.generate_content.generate_quiz.Pickle_File import dumpPickle, loadPickle, pickleExists
import pandas as pd
from training_content.generate_content.generate_learning_content_data import getContent
from training_content.generate_content.generate_quiz.Future_Engineering import newAddNCForParagrapgh, newAddWordForParagrapgh, oneHotEncoding, asTrainingTable
from training_content.generate_content.generate_quiz.Predict_Answer import predict
from training_content.generate_content.generate_quiz.Generate_Question import addQuestions
from training_content.generate_content.generate_quiz.Generate_Choice import addChoice
import json
import spacy
import os.path
nlp = spacy.load("en_core_web_sm")

# load glove pre-trained word vectors
modelName = './model_glove.pkl'
if (pickleExists(modelName) == False):
    from gensim.models import KeyedVectors
    glove_file = './Out_Source/glove_6B/glove.6B.300d.txt'
    tmp_file = './Out_Source/glove_6B/word2vec-glove.6B.300d.txt'
    from gensim.scripts.glove2word2vec import glove2word2vec
    glove2word2vec(glove_file, tmp_file)
    model_glove = KeyedVectors.load_word2vec_format(tmp_file)
    dumpPickle('model_glove.pkl', model_glove)
else:
    model_glove = loadPickle('model_glove.pkl')

# redefine the stop word in spacy
from spacy.lang.en.stop_words import STOP_WORDS
for word in STOP_WORDS:
    for w in (word, word[0].capitalize(), word.upper()):
        lex = nlp.vocab[w]
        lex.is_stop = True


# 1 load content text
# 2 feature engineering
# 3 training and processing
# 4 generate question and answer
# 5 constructe data

if __name__ =='__main__':
    text0_3 = []
    keyword = 'Computer_security'

    # load trained model
    clf = loadPickle('./Trained_Models/M_BernoulliNB+isotonic_smote.pkl')
    # load content text file
    try:
        with open('./Data_3_KLT.json', 'r', encoding='utf8') as fp:
            text_data = json.load(fp)
    except FileNotFoundError:
        getContent(keyword)

    # extract all keywords' text
    for index in range(len(text_data)):
        # extract a certain level of text, here is the 3 level of text
        if text_data[index]['Level'] == 3:
        # if text_data[index]['Level'] < 3:
            try:
                each_text = text_data[index]['Text']
                # delete the content in brackets and '\n'
                # text = re.sub(u"\\(.*?\\)", "", each_text).replace('\n', '')
                # remove the content is empty
                if each_text != '':
                    text0_3.append([index, each_text])
            except:
                print(text_data[index]['Keyword'], 'has not text.')
                continue

    print('\nload text0-3 finished')
    print('All text number:', len(text0_3),'\n')

    for whole_number in range(len(text0_3)):
        text = text0_3[whole_number][1]
        print('Number ', text0_3[whole_number][0], 'text is processing.')
        print('Keyword is ', text_data[text0_3[whole_number][0]]['Keyword'])
        ##################################
        #######Text Feature Engineering###
        ##################################
        words = []
        # Feature engineering for noun chunk in the text
        words = newAddNCForParagrapgh(words, text)
        NCnumber = len(words)
        # Feature engineering for word in the text
        words = newAddWordForParagrapgh(words, text)
        Allnumber = len(words)

        # Define feature engineering headers and tables(wordsDf)
        wordColums = ['Words', 'InSentencePosition', 'Word_Count', 'NER', 'POS', 'TAG', 'DEP', 'Is_Alpha', 'Is_Stop']
        wordsDf = pd.DataFrame(words, columns=wordColums)

        # wordsDf-onehotencoding
        wordsDf = oneHotEncoding(wordsDf)

        # Correspond to the feature table items of the training set
        w_Df, Finished_fe_table = asTrainingTable(wordsDf)
        #print('Feature engineer table', Finished_fe_table)

        ##################################
        ####### Predicted Answer #########
        ##################################
        # predict answer
        predict_answer = predict(clf, w_Df, wordsDf, NCnumber, Allnumber)
        print('predict answer: ', predict_answer)
        ##################################
        ####### Generate Question ########
        ##################################
        # generate question
        question_sets = addQuestions(predict_answer, text)
        #print(question_sets)
        #print(len(question_sets))

        ##################################
        ####### Generate other choice ####
        ##################################
        # generate other choice
        Allsets = addChoice(question_sets[:len(question_sets)], 4)

        completed_set = []
        for i in range(len(question_sets)):
            if (Allsets[i]['other_choice'] != [] and len(Allsets[i]['other_choice']) > 2):
                completed_set.append(Allsets[i])

        print(completed_set)
        print(len(completed_set) , ' questions is generated.')
        # words_questionsets = {'Question': completed_set}

        text_data[text0_3[whole_number][0]].update({'Questions': completed_set})
        print(text_data[text0_3[whole_number][0]])
        print('number', text0_3[whole_number][0], 'question is added.\n')

    #print(text_data)

    # output the final quiz data
    filename = 'Data_level3_KLTQ.json'
    with open(filename, 'w') as file_obj:
        json.dump(text_data, file_obj)
