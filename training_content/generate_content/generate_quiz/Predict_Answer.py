
def predict(clf, w_Df, wordsDf, NCnumber, Allnumber):
    # predict label
    pre_data = clf.predict(w_Df)
    # predict probability
    y_pred = clf.predict_proba(w_Df)

    labeledAnswers = []
    for i in range(len(pre_data)):
        labeledAnswers.append({'word': wordsDf.iloc[i]['Words'], 'pre_label': pre_data[i], 'prob': y_pred[i][0]})


    NClabeled = []
    Wlabeled = []

    for i in range(NCnumber):
        NClabeled.append(labeledAnswers[i])

    for i in range(NCnumber, Allnumber):
        Wlabeled.append(labeledAnswers[i])

    for i in range(Allnumber - NCnumber):
        if (Wlabeled[i]['pre_label'] == True):
            for j in range(NCnumber):
                if (Wlabeled[i]['word'] in NClabeled[j]['word']):
                    Wlabeled.append({'word': NClabeled[j]['word'], 'pre_label': True,
                                     'prob': max(Wlabeled[i]['prob'], NClabeled[j]['prob'])})


    # Sort
    paixu = sorted(Wlabeled, key=lambda labeledAnswers: labeledAnswers['prob'], reverse=True)


    # Deduplication
    dic = {}
    duplicate = []
    for word in paixu:
        if (word['pre_label'] == True):
            if word['word'] not in dic.keys():
                dic[word['word']] = word
            elif dic[word['word']]['prob'] < word['prob']:
                dic[word['word']] = word
    for value in dic.values():
        duplicate.append(value)

    # If the predicted probability is more than 0.5, generate a problem
    final = []
    for i in duplicate:
        if (i['prob'] >= 0.5):
            final.append(i)
    return final








