from flask import Flask, render_template, request, Response
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

def lisaa_uusi_halukas():
    global halukkaat
    timestamp = time.time()
    poista_vanhat_halukkaat()
    if len(halukkaat) >= HALUKKAATMAX:
        halukkaat.pop(0)
    halukkaat.append(timestamp)

#========= main =========

def halukkaatstr():
    halukkaatstr = "Halukkaat"
    halukkaatlkm = len(halukkaat)
    if   (halukkaatlkm == 3):  halukkaatstr = halukkaatstr + f" :{halukkaatlkm}"
    elif (halukkaatlkm >= HALUKKAATMAX): halukkaatstr = halukkaatstr + f": {halukkaatlkm} (max)"
    else:                      halukkaatstr = halukkaatstr + f": {halukkaatlkm}"
    return halukkaatstr

@app.route('/kahvi',  methods=['POST'])
def home():
    if len(halukkaat) >= HALUKKAATMAX:
        halukkaats = halukkaatstr() 
        return render_template('index.html', halukkaat=halukkaats), 418

    lisaa_uusi_halukas()
    x = render_template('redirect.html')
    resp = Response(x)
    resp.headers.add('Location', 'https://kattila.cafe')
    return resp

@app.route('/', methods=['GET'])
def kissa():
    poista_vanhat_halukkaat()
    halukkaats = halukkaatstr() 
    return render_template('index.html', halukkaat=halukkaats)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/display')
def toinen_kissa():
    poista_vanhat_halukkaat()
    halukkaats = halukkaatstr() 
    return render_template('display.html', halukkaat=halukkaats, halukkaatlkm=str(len(halukkaat))+"%")

def main():
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()

