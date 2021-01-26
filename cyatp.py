from flask import Flask, request, jsonify, url_for, render_template
from neo_db.query_graph import query
from scripts.show_profile import get_keyword_profile
from scripts.get_5_data import get_all_question
from scripts.get_cross import get_crossword
from scripts.save_feedback import save, save_survey
import json
app = Flask(__name__)


# homepage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_page.html'), 404


# concept map page
@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html')

# learn page
@app.route('/learn', methods=['GET', 'POST'])
def learn():
    return render_template('learn.html')

# search keyword information for learn page
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    # print(json_data)
    return jsonify(json_data)

# get keyword's text for learn page
@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    name = request.args.get('name')
    json_data = get_keyword_profile(name)
    #print(json_data)
    #print(jsonify(json_data))
    return jsonify(json_data)

# quiz page
@app.route('/game/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('quiz.html')

# get questions for quiz page
@app.route('/get_question', methods=['GET', 'POST'])
def get_question():
    with app.app_context():
        All_question = get_all_question()
        return jsonify(All_question)

# quiz feedback
@app.route('/game/feedback', methods=['GET', 'POST'])
def game_feedback():
    temp_value = request.form.to_dict()
    final = []
    result = []
    for key in temp_value:
        if(key=='record'):
            temp_num = temp_value[key].split(',')
            for i in range(len(temp_num)):
                result.append(temp_num[i])
        else:
            temp_dic = {}
            temp_text = temp_value[key]
            temp_split = temp_text.split(',answer,')
            temp_dic.update({'Question': temp_split[0]})
            temp_dic.update({'Answer': temp_split[1]})
            final.append(temp_dic)

    for index, q_dic in enumerate(final):
        q_dic.update({'Record': result[index]})
    return render_template('quiz_feedback.html', data = final)

# crossword puzzle page
@app.route('/game/puzzle', methods=['GET', 'POST'])
def puzzle():
    return render_template('puzzle.html')

# get puzzle for crossword puzzle page
@app.route('/get_cross', methods=['GET', 'POST'])
def get_cross():
    puzzleData = get_crossword()
    return jsonify(puzzleData)

# survey page
survey_data = []
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'GET':
        return render_template('survey.html')
    if request.method == 'POST':
        survey_feedback = json.loads(request.get_data())
        # print(survey_feedback)
        # add feedback to survey_data, and save it
        survey_data.append(survey_feedback)
        save_survey(survey_data)
        return render_template('survey.html')

data_list = []
@app.route('/back', methods=['GET', 'POST'])
def back():
    if request.method == 'POST':
        # get feedback user information
        info_ip = request.remote_addr
        info_platform = request.user_agent.platform
        info_brower = request.user_agent.browser
        info_bv = request.user_agent.version
        info_all = info_ip + ' ' + info_platform + ' ' + info_brower + ' ' + info_bv

        data = json.loads(request.get_data())
        data.update({'info': info_all})
        data_list.append(data)
        statues_data = save(data_list)

        return render_template('back.html', data_ = data_list)

    if request.method == 'GET':
        return render_template('back.html', data_=data_list)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    # app.debug = True
    app.debug = False
    app.run(host='0.0.0.0')
