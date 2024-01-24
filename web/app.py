from flask import Flask, render_template, request, Response
import random
import time

app = Flask(__name__)
halukkaat = []

#========= tietokanta =========

def poista_vanhat_halukkaat():
    global halukkaat
    timestamp = time.time()
    temp = []
    for h in halukkaat:
        if (timestamp - h < 15*60):
            temp.append(h)
    halukkaat = temp

def lisaa_uusi_halukas():
    global halukkaat
    timestamp = time.time()
    poista_vanhat_halukkaat()
    if len(halukkaat) >= 100:
        halukkaat.pop(0)
    halukkaat.append(timestamp)

#========= main =========

@app.route('/kahvi',  methods=['POST'])
def home():
    lisaa_uusi_halukas()
    x = render_template('redirect.html')
    resp = Response(x)
    resp.headers.add('Location', 'https://kattila.cafe')
    return resp

@app.route('/', methods=['GET'])
def kissa():
    poista_vanhat_halukkaat()
    halukkaatstr = "Halukkaiden lkm"
    # Siitäs sait kun nimesit aliohjelman kissaksi
    if ( len(halukkaat) == 3): halukkaatstr = halukkaatstr + f" :{len(halukkaat)}"
    else: halukkaatstr = halukkaatstr + f": {len(halukkaat)}"
    return render_template('index.html', halukkaat=halukkaatstr)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

def main():
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()