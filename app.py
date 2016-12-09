from flask import Flask, render_template,request,url_for
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("main.html")

@app.route('/home')
def homeP():
	return render_template("home.html")

@app.route('/SentimentAnalysis',methods=['post','get'])
def SentimentAnalysis():
	if(request.method=='POST'):
		txtQuery= request.form['textQuery']
		print("requested a post ",txtQuery)
		if txtQuery!="":
			textblobBaiyes = TextBlob(txtQuery,analyzer=NaiveBayesAnalyzer())
			textblobPattern = TextBlob(txtQuery)
			sentiments ={}
			sentiments["textblobBaiyes 0 neg 1 pos"] = [textblobBaiyes.sentiment.p_pos,'-']
			sentiments['textbloPattern -1 to 1'] = [textblobPattern.sentiment.polarity,textblobPattern.subjectivity]
			return render_template("SentimentProcessed.html",posts=sentiments,txt=txtQuery)
	"""
	if(request.method=='POST'):
		txtQuery= request.form['txtQuery']
		if txtQuery =="":
			return render_template("SentimentAnalysis.html")
		else:
			print("query is ", txtQuery)
		"""
	print("entered a post request")
	return render_template("SentimentAnalysis.html")
@app.route('/SentimentAnalysis2',methods=['post','get'])
def s1():
	return render_template("SentimentProcessed.html")
	  