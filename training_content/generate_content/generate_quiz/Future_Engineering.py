from training_content.generate_content.generate_quiz.Pickle_File import loadPickle, dumpPickle
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.tokenize import word_tokenize

# extract the answer
def extractAnswers(qas, doc):
    answers = []
    senStart = 0
    senId = 0
    for sentence in doc.sents:
        senLen = len(sentence.text)
        for answer in qas:
            answerStart = answer['answers'][0]['answer_start']
            if (answerStart >= senStart and answerStart < (senStart + senLen)):
                answers.append({'sentenceId': senId, 'text': answer['answers'][0]['text']})
        senStart += senLen
        senId += 1

    return answers


# Determine if the current word is the answer
def tokenIsAnswer(token, sentenceId, answers):
    for i in range(len(answers)):
        if (answers[i]['sentenceId'] == sentenceId):
            if (answers[i]['text'] == token):
                return True
    return False

def getNEStartIndexs(doc):
    neStarts = {}
    for ne in doc.ents:
        print(ne.start)
        neStarts[ne.start] = ne
    return neStarts

# extract the start index of none chunk  in the text
def getNCStartIndexs(doc):
    neStarts = {}
    for ne in doc.noun_chunks:
        neStarts[ne.start] = ne
    return neStarts


# get sentence start index
def getSentenceStartIndexes(doc):
    senStarts = []  # sentence start position
    for sentence in doc.sents:  # doc.sents: divide the sentences of the text into sentence by sentence
        senStarts.append(sentence[0].i)  # add the each sentence start position to senStarts
    return senStarts


#  get each word in which sentence position
def getSentenceForWordPosition(wordPos, senStarts):  # words position/sentence start index position
    if (len(senStarts) == 1):
        return 0
    for i in range(1, len(senStarts)):
        if (wordPos < senStarts[i] or wordPos == 0):
            return i - 1
        if (wordPos > senStarts[len(senStarts) - 1]):
            return len(senStarts) - 1
        if (wordPos == senStarts[i]):
            return i


# KMP algorithm
def getNext(p, nexts):
    i = 0
    j = -1
    nexts[0] = -1
    while i < len(p):
        if j == -1 or list(p)[i] == list(p)[j]:
            i = i + 1
            j = j + 1
            nexts[i] = j
        else:
            j = nexts[j]
    return nexts


# KMP algorithm
def match(s, p, nexts):
    if s == None or p == None:
        return -1
    slen = len(s)
    plen = len(p)
    if slen < plen:
        return -1
    i = 0
    j = 0
    while i < slen and j < plen:
        # print("i="+str(i)+","+"j="+str(j))
        if j == -1 or list(s)[i] == list(p)[j]:
            i = i + 1
            j = j + 1
        else:
            j = nexts[j]
    if j >= plen:
        return i - plen
    return -1

######Training - Feature engineering#####
# extract the none chunk in answer
def addAnswersNC(df, newWords, titleId, paragraphId):
    text = df['data'][titleId]['paragraphs'][paragraphId]['context']
    qas = df['data'][titleId]['paragraphs'][paragraphId]['qas']

    doc = nlp(text)  # use nlp processing the text
    answers = extractAnswers(qas, doc)

    answers_noun_chunks = []
    answers_noun_chunks_sentenceId = []

    for j in range(len(answers)):
        temp = nlp(answers[j]['text']).noun_chunks
        for i in temp:
            answers_noun_chunks.append(i)
            answers_noun_chunks_sentenceId.append(answers[j]['sentenceId'])

    i = 0
    while (i < len(answers_noun_chunks)):

        word = answers_noun_chunks[i]
        wordLen = word.end - word.start
        shape = ''
        for wordIndex in range(word.start, word.end):
            shape += (' ' + doc[wordIndex].shape_)
        currentSentence = answers_noun_chunks_sentenceId[i]

        sentence = []
        for Sentence in list(doc.sents):
            sentence.append(Sentence)

        sentence_token = word_tokenize(str(sentence[currentSentence]))
        word_token = word_tokenize(str(word))

        lens = len(word_token)
        nexts = [0] * (lens + 1)
        nexts = getNext(word_token, nexts)
        InSentencePosition = match(sentence_token, word_token, nexts)
        # print(InSentencePosition)

        nlpword = nlp(str(word))

        if (len(nlpword) == 1):
            newWords.append([word.text,
                             True,
                             titleId,
                             paragraphId,
                             currentSentence,
                             InSentencePosition,
                             wordLen,
                             word.label_,
                             nlpword[0].pos_,
                             nlpword[0].tag_,
                             nlpword[0].dep_,
                             shape,
                             nlpword[0].is_alpha,
                             nlpword[0].is_stop])

        else:
            newWords.append([word.text,
                             True,
                             titleId,
                             paragraphId,
                             currentSentence,
                             InSentencePosition,
                             wordLen,
                             word.label_,
                             None,
                             None,
                             None,
                             shape,
                             False,
                             False])

        i = i + 1
    return newWords


######training - feature engineering#####
# extract the none chunk from text
def addWordsForParagrapgh(df, newWords, titleId, paragraphId):
    text = df['data'][titleId]['paragraphs'][paragraphId]['context']  # paragraph
    qas = df['data'][titleId]['paragraphs'][paragraphId]['qas']  # answer and question

    doc = nlp(text)
    answers = extractAnswers(qas, doc)

    doc_NC = getNCStartIndexs(doc)
    senStarts = getSentenceStartIndexes(doc)

    i = 0
    while (i < len(doc)):
        if (i in doc_NC):

            word = doc_NC[i]
            currentSentence = getSentenceForWordPosition(word.start, senStarts)
            wordLen = word.end - word.start
            shape = ''
            for wordIndex in range(word.start, word.end):
                shape += (' ' + doc[wordIndex].shape_)

            sentence = []
            for Sentence in list(doc.sents):
                sentence.append(Sentence)

            # print(sentence)
            sentence_token = word_tokenize(str(sentence[currentSentence]))
            # print(sentence_token)
            word_token = word_tokenize(str(word))
            # print(word_token)

            lens = len(word_token)
            nexts = [0] * (lens + 1)
            nexts = getNext(word_token, nexts)
            InSentencePosition = match(sentence_token, word_token, nexts)

            newWords.append([word.text,
                             tokenIsAnswer(word.text, currentSentence, answers),
                             titleId,
                             paragraphId,
                             currentSentence,
                             InSentencePosition,
                             wordLen,
                             word.label_,
                             None,
                             None,
                             None,
                             shape,
                             False,
                             False])
            i = doc_NC[i].end - 1

        if (doc[i].is_stop == False and doc[i].is_alpha == True):
            word = doc[i]
            currentSentence = getSentenceForWordPosition(i, senStarts)
            wordLen = 1
            sentence = []
            for Sentence in list(doc.sents):
                sentence.append(Sentence)

            # print(sentence)
            sentence_token = word_tokenize(str(sentence[currentSentence]))
            # print(sentence_token)
            if (str(word) in sentence_token):
                for t in range(len(sentence_token)):
                    if (str(word) == sentence_token[t]):
                        InSentencePosition = t
            else:
                InSentencePosition = -1

            newWords.append([word.text,
                             tokenIsAnswer(word.text, currentSentence, answers),
                             titleId,
                             paragraphId,
                             currentSentence,
                             InSentencePosition,
                             wordLen,
                             None,
                             word.pos_,
                             word.tag_,
                             word.dep_,
                             word.shape_,
                             True,
                             False])
        i = i + 1
    return newWords


######predict - feature engineering#####
# each none chunk's feature
def newAddNCForParagrapgh(newWords, text):
    doc = nlp(text)
    senStarts = getSentenceStartIndexes(doc)
    i = 0

    doc_NC = []
    for temp in doc.noun_chunks:
        doc_NC.append(temp)
    while (i < len(doc_NC)):

            word = doc_NC[i]
            currentSentence = getSentenceForWordPosition(word.start, senStarts)
            wordLen = word.end - word.start
            shape = ''
            for wordIndex in range(word.start, word.end):
                shape += (' ' + doc[wordIndex].shape_)

            sentence = []
            for Sentence in list(doc.sents):
                sentence.append(Sentence)

            # print(sentence)
            sentence_token = word_tokenize(str(sentence[currentSentence]))
            # print(sentence_token)
            word_token = word_tokenize(str(word))
            # print(word_token)

            lens = len(word_token)
            nexts = [0] * (lens + 1)
            nexts = getNext(word_token, nexts)
            InSentencePosition = match(sentence_token, word_token, nexts)

            newWords.append([word.text,
                             InSentencePosition,
                             wordLen,
                             word.label_,
                             None,
                             None,
                             None,
                             False,
                             False])
            i = i+1
            #print(i)

    return newWords

######predict - feature engineering#####
# each words feature
def newAddWordForParagrapgh(newWords, text):
    doc = nlp(text)
    senStarts = getSentenceStartIndexes(doc)
    j = 0
    while(j < len(doc)):
        if (doc[j].is_stop == False and doc[j].is_alpha == True):
            word = doc[j]

            currentSentence = getSentenceForWordPosition(j, senStarts)
            wordLen = 1

            sentence = []
            for Sentence in list(doc.sents):
                sentence.append(Sentence)

            # print(sentence)
            sentence_token = word_tokenize(str(sentence[currentSentence]))
            # print(sentence_token)

            if (str(word) in sentence_token):
                for t in range(len(sentence_token)):
                    if (str(word) == sentence_token[t]):
                        InSentencePosition = t
            else:
                InSentencePosition = -1

            newWords.append([word.text,
                             InSentencePosition,
                             wordLen,
                             None,
                             word.pos_,
                             word.tag_,
                             word.dep_,
                             True,
                             False])
        j += 1
    return newWords


def processWordsData(wordsDf):
    # 1 -  delete strange data
    df_1 = wordsDf[~wordsDf['InSentencePosition'].isin([-1])]
    df_1 = df_1.reset_index(drop=True)
    print(df_1['InSentencePosition'].describe())
    print(df_1.duplicated().value_counts())

    # 2 - delete repeat data
    cleandf = df_1.drop_duplicates(subset=['Words', 'Is_Answer'], keep='last')
    cleandf = cleandf.reset_index(drop=True)

    cleandf.to_csv('All_cleandf.csv', encoding='utf_8_sig')
    dumpPickle('All_cleandf.pkl', cleandf)

    con = len(cleandf[cleandf['Is_Answer'] == True]) / len(cleandf)
    print('After cleandf (words and Is_answer) Is_Answer percent:', con)

    # 3 - save feature matrix df
    columnsToDrop = ['Words', 'TitleId', 'ParagrapghId', 'SentenceId', 'Shape']
    FeDf = cleandf.drop(columnsToDrop, axis=1)

    FeDf.replace([True, False, None], [1, 0, 0], inplace=True)

    return FeDf


# one-hot-encoding
def oneHotEncoding(wordsDf):
    columnsToEncode = ['NER', 'POS', "TAG", 'DEP']
    for column in columnsToEncode:
        one_hot = pd.get_dummies(wordsDf[column])
        one_hot = one_hot.add_prefix(column + '_')

        wordsDf = wordsDf.drop(column, axis=1)
        wordsDf = wordsDf.join(one_hot)

    dumpPickle('All_featureDf.pkl', wordsDf)
    wordsDf.to_csv('All_featureDf.csv', encoding='utf_8_sig')

    return wordsDf

# Correspond to the feature table items of the training set
def asTrainingTable(wordsDf):
    df0 = loadPickle('./Trained_Models/All_featureDf.pkl')
    predictorColumns = list(df0.columns.values)
    predictorColumns.pop(0)
    w_Df = pd.DataFrame(columns=predictorColumns)
    for column in w_Df.columns:
        if (column in wordsDf.columns):
            w_Df[column] = wordsDf[column]
        else:
            w_Df[column] = 0
    Finished_fe_table = pd.DataFrame(w_Df)
    #print(Finished_fe_table)
    return w_Df, Finished_fe_table