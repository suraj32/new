from flask import Flask, render_template, redirect, request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import flash
from requests import get

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'delta'

class Shorten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortname = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer)
    countries = db.Column(db.String)

    def __init__(self, shortname, url, count):
        self.shortname = shortname
        self.url = url
        self.count = count

@app.route('/', methods = ['GET','POST'])
def hello_world():
    #print(get('https://ipapi.co/country/').text)
    if request.method == 'POST':
        shortName = request.form['name']
        Url = request.form['url']
        if shortName and Url :
            shorten = Shorten(shortname = shortName , url = Url,count =0)
            db.session.add(shorten)
            db.session.commit()
            flash('Successfully stored')
            return redirect('/')
        else:
            flash("Both are mandatory fields")
    return render_template('index.html')

@app.route('/shortUrl/<ShortName>')
def shorten(ShortName):
    shorten = Shorten.query.filter_by(shortname = ShortName).first()
    country = get('https://ipapi.co/country/').text + ", "
    if shorten:
        shorten.count+=1
        if not shorten.countries:
            shorten.countries = country
        else:
            shorten.countries = shorten.countries + country
        db.session.add(shorten)
        db.session.commit()
        return redirect(shorten.url)
    else:
        flash('Oops! Short Url was not found in Records')
        return render_template('wrongName.html')

if __name__ == "__main__":
    app.run(debug=True)