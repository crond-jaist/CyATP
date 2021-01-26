import spacy
nlp = spacy.load("en_core_web_sm")


def blankAnswer(firstTokenIndex, lastTokenIndex, sentStart, sentEnd, doc):
    try:
        leftPartStart = doc[sentStart].idx
        leftPartEnd = doc[firstTokenIndex].idx
        rightPartStart = doc[lastTokenIndex].idx + len(doc[lastTokenIndex])
        rightPartEnd = doc[sentEnd - 1].idx + len(doc[sentEnd - 1])
        question = doc.text[leftPartStart:leftPartEnd] + '_____' + doc.text[rightPartStart:rightPartEnd]
        return question
    except IndexError:
        print('IndexError')
        pass
    except Exception as e:
        print(e)



# One answer should only generate one question
def addQuestions(answers, text):
    doc = nlp(text)
    currAnswerIndex = 0
    qaPair = []

    while (currAnswerIndex < len(answers)):
        answerDoc = nlp(answers[currAnswerIndex]['word'])
        # print(answerDoc)
        # answerIsFound = True

        for sent in doc.sents:
            for token in sent:
                answerIsFound = True

                # when answer count == 1
                if (len(answerDoc) == 1):
                    if token.i >= len(doc) or doc[token.i].text.lower() != answerDoc[0].text.lower():
                        answerIsFound = False

                    if answerIsFound:
                        question = blankAnswer(token.i, token.i + len(answerDoc) - 1, sent.start, sent.end, doc)
                        #print(question)
                        qaPair.append({'question': question, 'answer': answers[currAnswerIndex]['word']})

                # when answer count == 2
                elif(len(answerDoc)==2):
                    if (token.i >= len(doc) or doc[token.i].text.lower() != answerDoc[0].text.lower()):
                        answerIsFound = False

                    if (token.i + 1 >= len(doc) or doc[token.i + 1].text.lower() != answerDoc[1].text.lower()):
                        answerIsFound = False

                    if answerIsFound:
                        question = blankAnswer(token.i, token.i + len(answerDoc) - 1, sent.start, sent.end, doc)
                        #print(question)
                        qaPair.append({'question': question, 'answer': answers[currAnswerIndex]['word']})

                # when answer count > 2
                else:
                    if (token.i >= len(doc) or doc[token.i].text.lower() != answerDoc[0].text.lower()):
                        answerIsFound = False

                    if (token.i + 2 >= len(doc) or doc[token.i + 2].text.lower() != answerDoc[2].text.lower()):
                        answerIsFound = False

                    if answerIsFound:
                        question = blankAnswer(token.i, token.i + len(answerDoc) - 1, sent.start, sent.end, doc)
                        #print(question)
                        qaPair.append({'question': question, 'answer': answers[currAnswerIndex]['word']})

        currAnswerIndex += 1

    return qaPair


