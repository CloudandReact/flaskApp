# flaskApp

Comp 490 Project on Sentiment Analysis

Link to research paper https://drive.google.com/drive/folders/0B6MFLleQhxNlaHlxWkdoUkpubkE

To Run the web app
1.	Install python 3.5

2.	Download anaconda by Continuum analytics

3.	 All these libraries below require python 3,5 with a relatively new version of the library dated January 2017

4.	flask (for the web app)

5.	nltk( natural language processing)

6.	pandas (data analysis)

7.	sicit-learn( data analysis)

8.	Textblob(sentiment analysis)

9.	matplotlib( graphing) 

10.	VaderSentiment (sentiment analysis)

These software from 3-10 which can easily be installed by downloading anaconda by Continuum analytics which either prepackages these software or can be installed by the command conda install packageName . 
Then to create the  directory

 Run conda create –n name of environment required packages python version
Sample example

conda create –n py35 flask Textblob pandas python=3.5

Then flask specific commands to run the project are in the command line

Set FLASK_APP =app.py

Set FLASK_DEBUG=1 

flask  run

Run on http://localhost:5000/home

Note please have the cache cleared when running the webapp in the browser as without this you may see some inconsistencies in the matplotlib graphs.
