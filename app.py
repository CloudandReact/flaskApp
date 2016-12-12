from flask import Flask, render_template,request,url_for,send_from_directory
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
import os
import sentimeAnalysis
import groupByHour
import topComments
import averageComments
import pandas as pd

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("main.html")

@app.route('/home')
def homeP():
	return render_template("home.html")
blobBaiyes =Blobber(analyzer=NaiveBayesAnalyzer())
blobPattern = Blobber()

@app.route('/SentimentAnalysis',methods=['post','get'])
def SentimentAnalysis():
	if(request.method=='POST'):
		txtQuery= request.form['textQuery']
		print("requested a post ",txtQuery)
		if txtQuery!="":
			textblobBaiyes = blobBaiyes(txtQuery)
			textblobPattern = blobPattern(txtQuery)
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
		option = request.form['graphSelection']
		f =request.files['fileUpload']
		
		if not f:
			print("not file entered")
		elif option!="Average likes for top commentators":
			file_contents = f.stream.read().decode("latin-1")
			print("before writing to the file")
			newFile= open("statsFile.csv","w+",encoding='latin-1')
			newFile.write(file_contents)
			newFile.close()
			print("wrote to file ")
			print(type(file_contents))
			if option=="Comments by hour of the day":
				print("in top comments of hour of the day")
				groupByHour.saveHourGraph("statsFile.csv")
				return render_template("graph.html",figName="commentsByHour.png",title="Comments per hour of the day")
			elif option=="Top Commentators":
				topComments.makeTopCommentsGraph("statsFile.csv")
				return render_template("graph.html",figName="topComments.png",title="top 100 commentators and the number of comments over a period of time")
			elif option=="General Statistics":
				dfComments = pd.read_csv("statsFile.csv", parse_dates=['comment_published'],encoding="latin-1")
				print("hello world statistics")
				return render_template("generalStats.html",dFrame=dfComments.describe(percentiles=[0.25,0.5,0.75,0.85,0.9,0.95,0.97,0.98,0.99]).to_html(classes="table table-striped"),title="General statistics on the file including mean ,standard deviation and percentiles of count of comment")
		elif option=="Average likes for top commentators":
			print("in average likes for top commentators need 2 files")
			postsFile = request.files['fileUploadLikes']
			if not f or not postsFile:
				print("need to enter both files")
			else:
				file_contents = f.stream.read().decode("latin-1")
				filePostsContents= postsFile.stream.read().decode("latin-1")
				print("before writing to the file")
				newFile= open("statsFile.csv","w+",encoding='latin-1')
				newFile.write(file_contents)
				newFile.close()
				newFile= open("postsFile.csv","w+",encoding='latin-1')
				newFile.write(filePostsContents)
				newFile.close()

				print("wrote to both files")
				averageComments.getAverageLikes("statsFile.csv","postsFile.csv")
				return render_template("graph.html",figName="averageComments.png",title="Average Comments for top 500 users")

		
		print(option)
		print("posted file ")
	return render_template("fileAnalysis.html")
@app.route("/fileSentiment",methods=['post','get'])
def fileSentiment():

	if request.method=="POST":
		dictFileMapping={"Somewhat Negative":"somewhatCons.csv","Very Negative":"veryCons.csv", "Somewhat Positive":"somewhatPros.csv","Very Positive":"veryPros.csv"}
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
		sentimeAnalysis.parseFile("newFile.csv",option)
		#fName = 
		return send_from_directory(os.getcwd(), dictFileMapping[option],as_attachment=True)
	return render_template("fileSentiment.html")

	  