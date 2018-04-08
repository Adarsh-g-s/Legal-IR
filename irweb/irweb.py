from flask import Flask, flash, session, render_template, jsonify, request, redirect, url_for
import sqlite3
import string
from random import *

from systemone import *
from systemtwo import *

app = Flask(__name__)
app.secret_key = 'dslfdsls3993jdshfsd'
# conn = sqlite3.connect("C:\Users\Oyewale\Desktop\IR Project\Legal-IR\irweb\data\mydatabase.db")
conn = sqlite3.connect("C:\\Users\\Oyewale\\Desktop\\mydatabase.db")
# conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


@app.route('/', methods=['GET'])
@app.route('/ir/systemone/home', methods=['GET'])
def showsystemonehome():

    return render_template('index.html')

@app.route('/ir/systemone/query', methods=['GET'])
def systemhome():
    start = request.args.get('start', default=1, type=int)
    length = request.args.get('length', default=10, type=int)
    filter = request.args.get('filter', default="no", type=str)
    draw = request.args.get('draw', default=1, type=int)
    query = request.args.get('query', type=str)

    if start == 10:
        start = 1;

    if start > 10:
        start = start // length

    start = start + 1;
    search = Search()
    response = search.passingQuery(query, start, length)

    outputs = [];

    for found in response:
        summary = found.highlights('contents')
        title = found['title']
        title = title[:100]
        # title = title.split(';', maxsplit=2) #should it be too longer than a line
        result = {
            'relevantScore': found.score,
            'title': title, #just pick the first element
            # 'path': pathlib.Path(found['path']).as_uri(),
            'path': found['path'].split("Legalfiles")[1],
            'summary': summary
        }

        outputs.append(result)

    finalout = {
        'data': outputs,
        'draw': draw,
        'recordsTotal': len(response),
        'recordsFiltered': len(response)
    }

    return jsonify(finalout)


@app.route('/ir/systemtwo/home')
def showsystemtwohome():
    return render_template('diverse.html')

@app.route('/ir/systemtwo/query', methods=['GET'])
def systemtwohome():
    start = request.args.get('start', default=1, type=int)
    length = request.args.get('length', default=10, type=int)
    filter = request.args.get('filter', default="no", type=str)
    draw = request.args.get('draw', default=1, type=int)
    query = request.args.get('query', type=str)
    # start = 1
    # length = 10


    if start == 10:
        start = 1;

    if start > 10:
        start = start // length

    start = start + 1;
    search = SearchTwo()
    response = search.passingQuery(query, start, length)

    finalout = {
        'data': response,
        'draw': draw,
        'recordsTotal': len(response),
        'recordsFiltered': len(response)
    }

    return jsonify(finalout)

@app.route('/ir/userstudy', methods=['POST', 'GET'])
def showuserstudy():

    if request.method == 'POST':
        occupation = request.form.get('occupation')
        age = request.form.get('age')
        sex = request.form.get('sex')
        course = request.form.get('course')
        semester = request.form.get('semester')
        firstSystemUsed = ''
        secondSystemUsed = ''
        # generate the order of the first two system using random number;
        system = randint(1,10)

        if system % 2 == 0:
            firstSystemUsed = 'systemOne'
            secondSystemUsed = 'systemTwo'
        else:
            firstSystemUsed = 'systemTwo'
            secondSystemUsed = 'systemOne'

        session['firstSystemUsed'] = firstSystemUsed
        session['secondSystemUsed'] = secondSystemUsed


        allchar = string.ascii_lowercase + string.digits
        user_id = "".join(choice(allchar) for x in range(randint(5, 8)))
        session['session_id'] = user_id;
        session_id = session['session_id']

        biodata = [(session_id,occupation, age, sex, course, semester)]
        cursor.executemany("INSERT INTO biodata VALUES (?,?,?,?,?,?)", biodata)
        conn.commit()

        return redirect(url_for('showuserstudyone'))



    return render_template('userstudybio.html')

@app.route('/ir/userstudy/1', methods=['POST', 'GET'])
def showuserstudyone():
    if request.method == 'POST':
        session_id = session['session_id']
        language = request.form.get('language')
        proficiency = request.form.get('proficiency')
        tool = request.form.get('tool')
        frequently_legal = request.form.get('frequently_legal')
        frequently = request.form.get('frequently')


        skills = [(session_id, language, proficiency,frequently, tool, frequently_legal)]
        cursor.executemany("INSERT INTO skills VALUES (?,?,?,?,?,?)", skills)
        conn.commit()

        return redirect(url_for('showuserstudytwo'))

    return render_template('userstudyfirst.html')

@app.route('/ir/userstudy/2')
def showuserstudytwo():

    return render_template('userstudysecond.html')

@app.route('/ir/userstudy/3', methods=['POST', 'GET'])
def showuserstudythree():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_topic = request.form.get('familiar_topic')
        familiar_context = request.form.get('familiar_context')
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        system_used = request.form.get('system_used')

        task_one = [(session_id, familiar_topic,familiar_context,familiar_now,relevant,overview,
                     support,similar,reuse,system_rate,sufficient,system_used)]
        cursor.executemany("INSERT INTO taskone VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", task_one)
        conn.commit()

        return redirect(url_for('showuserstudyfour'))


    return render_template('userstudythird.html')

@app.route('/ir/userstudy/4', methods=['POST', 'GET'])
def showuserstudyfour():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_topic = request.form.get('familiar_topic')
        familiar_context = request.form.get('familiar_context')
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        previous = request.form.get('previous')
        system_used = request.form.get('system_used')

        task_two = [(session_id, familiar_topic, familiar_context, familiar_now, relevant, overview, support, similar,
                     reuse, system_rate, sufficient, previous,system_used)]
        cursor.executemany("INSERT INTO tasktwo VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", task_two)
        conn.commit()

        return redirect(url_for('showuserstudyfive'))

    return render_template('userstudyfourth.html')

@app.route('/ir/userstudy/5', methods=['POST', 'GET'])
def showuserstudyfive():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_topic = request.form.get('familiar_topic')
        familiar_context = request.form.get('familiar_context')
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        previous = request.form.get('previous')
        suggestion = request.form.get('suggestion')
        system_used = request.form.get('system_used')

        task_three = [(session_id, familiar_topic, familiar_context, familiar_now, relevant, overview, support, similar,
                     reuse, system_rate, sufficient, previous, suggestion,system_used)]
        cursor.executemany("INSERT INTO taskthree VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", task_three)
        conn.commit()

        session.pop('session_id', None)

        # session['final_remark'] = 'You are done with the tasks, thanks for your time';

        flash('You are done with the tasks, thanks for your time')

        return redirect(url_for('showuserstudy'))

    return render_template('userstudyfifth.html')


if __name__ == '__main__':
    app.run()
