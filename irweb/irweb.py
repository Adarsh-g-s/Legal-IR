from flask import Flask, render_template,json ,request
import os
from systemone import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ir/sysone/home')
def showsystemonehome():

     return render_template('index.html')

@app.route('/ir/sysone/home',methods=['POST'])
def systemonehome():
    _query = request.form['query']
    search = Search()
    response = search.passingQuery(_query)

    outputs = [];

    for found in response:
        summary = found.highlights('contents')
        # summary = summary.decode('utf-8')
        result = {
            'relevantScore': found.score,
            'title': found['title'],
            'path': found['path'],
            'summary': summary
        }

        outputs.append(result)

    return render_template('index.html', results=outputs)

@app.route('/ir/systemtwo/home')
def showsystemtwohome():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
