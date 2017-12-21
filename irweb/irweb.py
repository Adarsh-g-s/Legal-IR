from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ir/sysone/home')
def showsystemonehome():
    return render_template('index.html')

@app.route('/ir/systemtwo/home')
def showsystemtwohome():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
