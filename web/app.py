from flask import Flask, render_template

app = Flask(__name__)
# source myenv/bin/activate
# nohup python3 app.py
# This route will serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
