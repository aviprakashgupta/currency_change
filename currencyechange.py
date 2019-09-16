from flask import Flask, render_template, request
import requests
import os
app = Flask('__name__')

bes = requests.get(f"http://data.fixer.io/api/latest?access_key={os.environ.get('fixer_key')}")
res = requests.get(f"http://data.fixer.io/api/2013-03-16?access_key={os.environ.get('fixer_key')}&symbols=USD,AUD,CAD,PLN,INR&format=1")
detail = requests.get(f"http://data.fixer.io/api/symbols?access_key={os.environ.get('fixer_key')}")
if res.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
if bes.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
if detail.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
details = detail.json()
data = res.json()
dat = bes.json()
cur = details['symbols'].items()
@app.route('/', methods=['POST', "GET"])
def index():
    if request.method =="GET":
        return render_template('currency.html',currency=cur)
    else:
        bas = request.form.get('base')
        othe = request.form.get('other')
        amt = float(request.form.get('amount'))
        base = bas[-4:-1]
        other = othe[-4:-1]
        val = dat['rates'][other] * 1 / dat['rates'][base]
        res = val*amt
        return render_template('currency.html',message=bas, other=othe, value=val, result=res,amt=amt)
