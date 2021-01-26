from training_content.generate_content.generate_quiz.Pickle_File import dumpPickle, loadPickle, pickleExists
import spacy
from sense2vec import Sense2Vec
nlp = spacy.load("en_core_web_sm")

# Load the generated vector
modelName = './model_glove.pkl'
if (pickleExists(modelName)):
    model_glove = loadPickle('model_glove.pkl')
else:
    from gensim.models import KeyedVectors
    glove_file = './Out_Source/glove_6B/glove.6B.300d.txt'
    tmp_file = './Out_Source/glove_6B/word2vec-glove.6B.300d.txt'
    from gensim.scripts.glove2word2vec import glove2word2vec
    glove2word2vec(glove_file, tmp_file)
    model_glove = KeyedVectors.load_word2vec_format(tmp_file)
    dumpPickle('model_glove.pkl', model_glove)

# generate choice
def generateOtherChoice(answer, count):
    # make all word lowercase
    answer = str.lower(answer)
    closestWords = []

    try:

        doc1 = nlp((answer))

        # if answer count ==1, use glove2word2vec
        if (len(doc1) == 1):
            closestWords = model_glove.most_similar(positive=[doc1.text], topn=count)

        # if answer count >1, use Sense2Vec
        else:
            temp = doc1.text.replace(' ', '_') + '|NOUN'

            s2v = Sense2Vec().from_disk("./Out_Source/s2v_old")
            most_similar = s2v.most_similar(temp, n=count)

            for each_choice in most_similar:
                del_ = each_choice[0].replace('_', ' ')
                choice, sep, suffix = del_.partition('|')
                closestWords.append((choice, each_choice[1]))

    except:
        return []

    other_choice = list(map(lambda x: x[0], closestWords))[0:count]

    # Remove words that are the same as the answer
    temp = other_choice[:]
    for i in temp:
        choice = nlp(i)
        for token in choice:
            if (token.lemma_ in answer) or (answer in token.lemma_):
                other_choice.remove(i)
                break

    # Remove the cognate words in the options
    other_choice_ = []
    for j in other_choice:
        choice = nlp(j)
        if (len(choice) == 1):
            for token in choice:
                other_choice_.append(token.lemma_)
        else:
            tempword = ''
            for token in choice:
                tempword = tempword + token.lemma_ + ' '
            other_choice_.append(tempword.rstrip(' '))


    return list(set(other_choice_))

def addChoice(qaPairs, count):
    for qaPair in qaPairs:
        answer = qaPair['answer']
        distractors = generateOtherChoice(qaPair['answer'], count)
        if ((len(distractors) != 0) and (len(distractors) < 4)):
            for i in range(len(distractors)):
                second_choice_ = generateOtherChoice((distractors[i]), 2)
                if (second_choice_ != []):
                    for each_second in second_choice_:
                        distractors.append(each_second)

        # delete repeat choice
        temp = distractors[:]
        for i in temp:
            choice = nlp(i)
            for token in choice:
                if (token.lemma_ in answer) or (answer in token.lemma_):
                    distractors.remove(i)
                    break

        # Remove the cognate words in the options
        other_choice_ = []
        for j in distractors:
            choice = nlp(j)
            if (len(choice) == 1):
                for token in choice:
                    other_choice_.append(token.lemma_)
            else:
                tempword = ''
                for token in choice:
                    tempword = tempword + token.lemma_ + ' '
                other_choice_.append(tempword.rstrip(' '))

        qaPair['other_choice'] = distractors

    return qaPairs
