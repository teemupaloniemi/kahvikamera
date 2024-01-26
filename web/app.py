from flask import Flask, render_template, request, Response
import random
import time

app = Flask(__name__)
halukkaat = []
HALUKKAATMAX = 10

#========= tietokanta =========

def poista_vanhat_halukkaat():
    global halukkaat
    timestamp = time.time()
    temp = []
    for h in halukkaat:
        if (timestamp - h < 15*60):
            temp.append(h)
    halukkaat = temp

#========= main =========

@app.route('/', methods=['GET'])
def kissa():
    #poista_vanhat_halukkaat()
    return render_template('index.html', halukkaat=str(len(halukkaat))+"%")

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

def main():
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()
