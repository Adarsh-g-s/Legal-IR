from flask import Flask, flash, session, render_template, jsonify, request, redirect, url_for,send_from_directory
import sqlite3
import string
from random import *
import time

from systemone import *
from systemtwo import *

app = Flask(__name__, static_url_path='')
app.secret_key = 'dslfdsls3993jdshfsd'
# conn = sqlite3.connect("C:\Users\Oyewale\Desktop\IR Project\Legal-IR\irweb\data\mydatabase.db")
conn = sqlite3.connect(".\mydatabase.db")
# conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

@app.route('/files/<path:path>')
def send_js(path):
    return send_from_directory('../rawfiles', path)

@app.route('/', methods=['GET'])
@app.route('/ir/mercury/home', methods=['GET'])
def showsystemonehome():

    return render_template('index.html')

@app.route('/ir/mercury/query', methods=['GET'])
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
            'path': "/"+ntpath.basename(ntpath.dirname(found['path'])) +"/"+ ntpath.basename(found['path']), #found['path'].split("Legalfiles")[1],
            'summary': summary
        }

        outputs.append(result)


    finalout = {
        'data': outputs,
        'draw': draw,
        'recordsTotal': len(response),
        'recordsFiltered': len(response)
    }
    if draw == 1:
        time.sleep(30)

    return jsonify(finalout)


@app.route('/ir/pluto/home')
@app.route('/ir/venus/home')
def showsystemtwohome():
    return render_template('diverse.html')

@app.route('/ir/venus/query', methods=['GET'])
def systemtwohome():
    start = request.args.get('start', default=1, type=int)
    length = request.args.get('length', default=10, type=int)
    filter = request.args.get('filter', default="no", type=str)
    draw = request.args.get('draw', default=1, type=int)
    query = request.args.get('query', type=str)

    search = SearchTwo()
    response = search.passingQuery(query)

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

        # generate the order of the first two system using random number;
        cursor.execute("select presentvalue from usertracker")

        result_set = cursor.fetchall()
        for row in result_set:
            presentvalue = row[0]

        if session.get('userTracker') is None:

            session['userTracker'] = presentvalue + 1;



        presentvalue = session['userTracker']

        # update the user tracker value in the db
        cursor.execute('update usertracker set presentvalue = ?',(presentvalue,))

        orderChoice = session['userTracker'] % 4

        order = [];

        if orderChoice == 0 :
            order = ['mercury','venus','pluto']
        if orderChoice == 1:
            order = ['mercury','pluto','pluto']
        if orderChoice == 2:
            order = ['pluto','mercury','mercury']
        if orderChoice == 3:
            order = ['pluto','mercury','venus']

        session['firstSystemUsed'] = order[0]
        session['secondSystemUsed'] = order[1]
        session['thirdSystemUsed'] = order[2]


        allchar = string.ascii_lowercase + string.digits
        user_id = "".join(choice(allchar) for x in range(randint(5, 8)))
        session['session_id'] = user_id;
        session_id = session['session_id']

        biodata = [(session_id,occupation, age, sex, course, semester)]

        # check if an entry exist for the session
        cursor.execute("select * from biodata where sessionid = ?",(session_id,))
        result_set = cursor.fetchone()

        if result_set == None :

            cursor.executemany("INSERT INTO biodata VALUES (?,?,?,?,?,?)", biodata)

        else:
            cursor.execute('update biodata set occupation = ?, age = ?, sex = ?, course = ?, semester = ? where sessionid = ?',[occupation,age,sex,course, semester,session_id])

        conn.commit()

        return redirect(url_for('showuserstudyone'))



    return render_template('userstudybio.html')

@app.route('/ir/userstudy/1', methods=['POST', 'GET'])
def showuserstudyone():
    if request.method == 'POST':
        session_id = session['session_id']
        language = request.form.get('language')
        proficiency = request.form.get('proficiency')
        tool = request.form.getlist('tool')
        frequently_legal = request.form.get('frequently_legal')
        frequently = request.form.get('frequently')
        toolstr = ' '.join(str(e) for e in tool)

        skills = [(session_id, language, proficiency,frequently, toolstr, frequently_legal)]

        # check if an entry exist for the session
        cursor.execute("select * from skills where sessionid = ?", (session_id,))
        result_set = cursor.fetchone()

        if result_set == None:

            cursor.executemany("INSERT INTO skills VALUES (?,?,?,?,?,?)", skills)

        else:
            cursor.execute(
                'update skills set language = ?, proficiency = ?, frequently = ?, tool = ?, frequently_legal = ? where sessionid = ?',
                [language, proficiency, frequently, toolstr, frequently_legal, session_id])

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


        task_one = [(session_id, familiar_topic,familiar_context,'','','','','','','','','',)]

        # check if an entry exist for the session
        cursor.execute("select * from taskone where sessionid = ?", (session_id,))
        result_set = cursor.fetchone()

        if result_set == None:

            cursor.executemany("INSERT INTO taskone VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", task_one)

        else:
            cursor.execute(
                'update taskone set familiar_topic = ?, familiar_context = ? where sessionid = ?',
                [familiar_topic, familiar_context, session_id])

        conn.commit()

        return redirect(url_for('showuserstudythreetwo'))


    return render_template('userstudythird.html')

@app.route('/ir/userstudy/32', methods=['POST', 'GET'])
def showuserstudythreetwo():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        system_used = request.form.get('system_used')

        task_one = [(familiar_now,relevant,overview,
                     support,similar,reuse,system_rate,sufficient,system_used,session_id)]
        cursor.executemany("update taskone set familiar_now = ?, relevant = ?, overview = ?, support = ?, similar = ?, reuse = ?, system_rate = ?, sufficient = ?,system_used = ? where sessionid = ?", task_one)
        conn.commit()

        return redirect(url_for('showuserstudyfour'))


    return render_template('userstudythirdtwo.html')

@app.route('/ir/userstudy/4', methods=['POST', 'GET'])
def showuserstudyfour():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_topic = request.form.get('familiar_topic')
        familiar_context = request.form.get('familiar_context')

        task_two = [(session_id, familiar_topic, familiar_context, '','','','','','','','','')]


        # check if an entry exist for the session
        cursor.execute("select * from tasktwo where sessionid = ?", (session_id,))
        result_set = cursor.fetchone()

        if result_set == None:

            cursor.executemany("INSERT INTO tasktwo VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", task_two)

        else:
            cursor.execute(
                'update tasktwo set familiar_topic = ?, familiar_context = ? where sessionid = ?',
                [familiar_topic, familiar_context, session_id])

        conn.commit()

        return redirect(url_for('showuserstudyfourtwo'))

    return render_template('userstudyfourth.html')


@app.route('/ir/userstudy/42', methods=['POST', 'GET'])
def showuserstudyfourtwo():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        system_used = request.form.get('system_used')

        task_two = [(session_id, familiar_now, relevant, overview, support, similar,
                     reuse, system_rate, sufficient,system_used)]
        cursor.executemany("update tasktwo set familiar_now = ?, relevant = ?, overview = ?, support = ?, similar = ?, reuse = ?, system_rate = ?, sufficient = ?,system_used = ? where sessionid = ?",
            task_two)

        conn.commit()

        return redirect(url_for('showuserstudyfive'))

    return render_template('userstudyfourthtwo.html')

@app.route('/ir/userstudy/5', methods=['POST', 'GET'])
def showuserstudyfive():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_topic = request.form.get('familiar_topic')
        familiar_context = request.form.get('familiar_context')

        task_three = [(session_id, familiar_topic, familiar_context, '', '', '',
                       '', '', '', '', '','')]

        # check if an entry exist for the session
        cursor.execute("select * from taskthree where sessionid = ?", (session_id,))
        result_set = cursor.fetchone()

        if result_set == None:

            cursor.executemany("INSERT INTO taskthree VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", task_three)

        else:
            cursor.execute(
                'update taskthree set familiar_topic = ?, familiar_context = ? where sessionid = ?',
                [familiar_topic, familiar_context, session_id])

        conn.commit()

        return redirect(url_for('showuserstudyfivetwo'))

    return render_template('userstudyfifth.html')

@app.route('/ir/userstudy/52', methods=['POST', 'GET'])
def showuserstudyfivetwo():
    if request.method == 'POST':
        session_id = session['session_id']
        familiar_now = request.form.get('familiar_now')
        relevant = request.form.get('relevant')
        overview = request.form.get('overview')
        support = request.form.get('support')
        similar = request.form.get('similar')
        reuse = request.form.get('reuse')
        system_rate = request.form.get('system_rate')
        sufficient = request.form.get('sufficient')
        system_used = request.form.get('system_used')

        task_three = [(session_id, familiar_now, relevant, overview, support, similar,
                     reuse, system_rate, sufficient,system_used)]
        cursor.executemany(
            "update taskthree set familiar_now = ?, relevant = ?, overview = ?, support = ?, similar = ?, reuse = ?, system_rate = ?, sufficient = ?,system_used = ? where sessionid = ?",
            task_three)
        conn.commit()

        return redirect(url_for('showuserstudyfinal'))

    return render_template('userstudyfifthtwo.html')

@app.route('/ir/userstudy/final', methods=['POST', 'GET'])
def showuserstudyfinal():
    if request.method == 'POST':
        session_id = session['session_id']
        easiest = request.form.get('easiest')
        helps = request.form.get('helps')
        suggestion = request.form.get('suggestion')
        reuse = request.form.get('reuse')


        task_final = [(session_id, easiest, helps, reuse, suggestion)]

        # check if an entry exist for the session
        cursor.execute("select * from final where sessionid = ?", (session_id,))
        result_set = cursor.fetchone()

        if result_set == None:

            cursor.executemany("INSERT INTO final VALUES (?,?,?,?,?)", task_final)

        else:
            cursor.execute(
                'update final set easiest = ?, helps = ?, reuse = ?, suggestion = ? where sessionid = ?',
                [easiest, helps,reuse, suggestion, session_id])

        conn.commit()
        session.pop('session_id', None)
        session.pop('userTracker', None)

        # session['final_remark'] = 'You are done with the tasks, thanks for your time';

        flash('You are done with the tasks, thanks for your time')

        return redirect(url_for('showuserstudy'))

    return render_template('userstudyfinal.html')

if __name__ == '__main__':
    # app.run(host='192.168.137.1')
    # app.run(debug=True)
     app.run()