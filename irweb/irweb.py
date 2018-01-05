from flask import Flask, render_template, jsonify, request
import os
from systemone import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/ir/sysone/home', methods=['GET'])
def showsystemonehome():
    return render_template('index.html')


@app.route('/ir/sysone/query', methods=['GET'])
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
        title = title.split(';', maxsplit=2) #should it be too longer than a line
        result = {
            'relevantScore': found.score,
            'title': title[0], #just pick the first element
            'path': found['path'],
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
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
