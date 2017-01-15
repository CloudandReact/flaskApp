from flask import Flask, render_template,request,url_for,send_from_directory
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import sentimeAnalysis
import groupByHour
import topComments
import averageComments
import finalClassifier
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
analyzer = SentimentIntensityAnalyzer()
@app.route('/createClassifier',methods=['post','get'])
def createClassifer():
	if (request.method=='POST'):
		print("post method createClassifier")
		f =request.files['fileUpload']
		negFile = request.files['fileUploadNegative']
		if not f and not negFile:
			print("not file entered")
		else:
			file_contentsPos = f.stream.read().decode("latin-1")
			file_contentsNeg= negFile.stream.read().decode("latin-1")
			print("before writing to the file")
			newFile= open("trainingSetPos.txt","w+",encoding='utf-8')
			newFile.write(file_contentsPos)
			newFile.close()
			newFile= open("trainingSetNeg.txt","w+",encoding='utf-8')
			newFile.write(file_contentsNeg)
			newFile.close()
			finalClassifier.makeClassifier(file_contentsPos,file_contentsNeg)
			finalClassifier.zipFiles()
			return send_from_directory(os.getcwd(), "classifiers.zip",as_attachment=True)
			

		


	return render_template("createClassifier.html")
@app.route('/SentimentAnalysis',methods=['post','get'])
def SentimentAnalysis():
	if(request.method=='POST'):
		txtQuery= request.form['textQuery']
		print("requested a post ",txtQuery)
		if txtQuery!="":
			textblobBaiyes = blobBaiyes(txtQuery)
			textblobPattern = blobPattern(txtQuery)
			vaderPolarity = analyzer.polarity_scores(txtQuery)  
			sentiments ={}
			sentiments["textblobBaiyes -1 to 1"] = [(textblobBaiyes.sentiment.p_pos-.5)*2,'-']
			sentiments['textbloPattern -1 to 1'] = [textblobPattern.sentiment.polarity,textblobPattern.subjectivity]
			sentiments['vaderSentiment -1  to 1']= [vaderPolarity['compound'],'-']
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
		fName = request.files['fileUpload'].filename
		fName = fName[:fName.find("_")]
		currentDir = os.getcwd()
		
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
				groupByHour.saveHourGraph("statsFile.csv",fName)
				return render_template("graph.html",figName=("commentsByHour.png"),title="Comments per hour of the day")
			elif option=="Top Commentators":
				topComments.makeTopCommentsGraph("statsFile.csv",fName)
				return render_template("graph.html",figName=("topCommentators.png"),title="top 100 commentators and the number of comments over a period of time")
			elif option=="General Statistics":
				dfComments = pd.read_csv("statsFile.csv", parse_dates=['comment_published'],encoding="latin-1")
				print("hello world statistics")
				return render_template("generalStats.html",dFrame=dfComments.describe(percentiles=[0.25,0.5,0.75,0.85,0.9,0.95,0.97,0.98,0.99]).to_html(classes="table table-striped"),title="General statistics on the file for " + fName + " including mean ,standard deviation and percentiles of count of comment")
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
				newFile= open("postsFile.csv","w+",encoding='utf-8')
				newFile.write(filePostsContents)
				newFile.close()

				print("wrote to both files")

				averageComments.getAverageLikes("statsFile.csv","postsFile.csv",fName)

				return render_template("graph.html",figName=("averageComments.png"),title="Average Comments for top 500 users")
				#return render_template("")

		
		print(option)
		print("posted file ")
	return render_template("fileAnalysis.html")
@app.route("/static/<figName>",methods=['post','get'])
def renderFigure(figName):
	fileLocation = os.getcwd()+"\\static\\"
	print("rendering image",figName)
	return send_from_directory(fileLocation, figName)
@app.route("/fileSentiment",methods=['post','get'])
def fileSentiment():

	if request.method=="POST":
		fName = request.files['fileUpload'].filename
		fName = fName[:fName.find("_")]
		dictFileMapping={"Somewhat Negative":("somewhatCons"+fName+"_.csv"),"Very Negative":("veryCons"+fName+"_.csv"), "Somewhat Positive":("somewhatPros"+fName+"_.csv"),"Very Positive":("veryPros"+fName+"_.csv")}
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
		sentimeAnalysis.parseFile("newFile.csv",option,dictFileMapping[option])
		#fName = 
		return send_from_directory(os.getcwd(), dictFileMapping[option],as_attachment=True)
	return render_template("fileSentiment.html")

	  