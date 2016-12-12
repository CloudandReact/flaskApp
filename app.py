from flask import Flask, render_template,request,url_for,send_from_directory
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
import os

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

@app.route("/fileAnalysis",methods=['post','get'])
def fileAnalysis():
	if request.method=="POST":
		f =request.files['fileUpload']
		if not f:
			print("not file entered")
		else:
			file_contents = f.stream.read().decode("latin-1")
			print("before writing to the file")
			newFile= open("statsFile.csv","w+",encoding='latin-1')
			newFile.write(file_contents)
			newFile.close()
			print("wrote to file ")
			print(type(file_contents))
		option = request.form['graphSelection']
		
		print(option)
		print("posted file ")
	return render_template("fileAnalysis.html")
@app.route("/fileSentiment",methods=['post','get'])
def fileSentiment():
	if request.method=="POST":
		print("made a post request yeah")
		option = request.form['graphSelection']
		#fName = request.form['fileUpload']
		print("made it this far before f")
		f =request.files['fileUpload']
		if not f:
			print("not file entered")
		else:
			print("decoding the file ")
			file_contents = f.stream.read().decode("latin-1")
			print("before writing to the file")
			newFile= open("newFile.csv","w+",encoding='latin-1')
			newFile.write(file_contents)
			newFile.close()
			print("wrote to file ")
			print(type(file_contents))
		print(option,f)
		print("posted file ")
		print(os.getcwd())
		return send_from_directory(os.getcwd(), "newFile.csv",as_attachment=True)
	return render_template("fileSentiment.html")

	  