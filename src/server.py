from flask import Flask, render_template

app = Flask(__name__)

count = 0

@app.route('/')
def hello():
    global count
    count = count + 1
    return render_template('index.html', name="Glooty", count=count)

@app.route('/terry')
def terry():
    return render_template('index.html', name="Terry", count="Over 9000")

app.run()
