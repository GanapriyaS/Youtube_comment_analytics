from flask import Flask,render_template,request,Response
from google_trans import translate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
app = Flask(__name__)

import nltk
import re
# from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


wl = WordNetLemmatizer()
ps = PorterStemmer()

import numpy as np

# from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.models import load_model
from apiclient.discovery import build
from bs4 import BeautifulSoup
# Arguments that need to passed to the build function
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# creating Youtube Resource Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
										developerKey = DEVELOPER_KEY)


final_range={1:[],2:[],3:[]}
def youtube_search_keyword(query, max_results):
	
# 	# calling the search.list method to
# 	# retrieve youtube search results
	search_keyword = youtube_object.search().list(q = query, part = "id, snippet", maxResults = max_results).execute()
	
	# extracting the results from search response
	results = search_keyword.get("items", [])


	# empty list to store video,
	# channel, playlist metadata
	videos = []
	# playlists = []
	# channels = []
	
	# extracting required info from each result object
	i=0
	final_return=[]
	for result in results:
		# video result object
		print(result)
		
		if result['id']['kind'] == "youtube#video":
			print("asflkdsjfa")
			videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],result["id"]["videoId"], result['snippet']['description'],result['snippet']['thumbnails']['default']['url']))
			video_data=video_comments(result["id"]["videoId"])
			print(video_data,len(video_data))
			video_embedded=word_embedding(video_data)
			print(video_embedded,len(video_embedded))
			counts=model_predict(video_embedded)
			total=np.sum(counts)
			counts=counts/total
			print(counts)
			i=i+1
			final_range[i]=counts
			counts=counts*100
			result={"counts":counts,"description":result['snippet']['description'],"title":result["snippet"]["title"],"url":result["id"]["videoId"]}
			final_return.append(result)

			
# 		# playlist result object
# 		elif result['id']['kind'] == "youtube# playlist":
# 			playlists.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
# 								result["id"]["playlistId"],
# 								result['snippet']['description'],
# 								result['snippet']['thumbnails']['default']['url']))

# 		# channel result object
# 		elif result['id']['kind'] == "youtube# channel":
# 			channels.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
# 								result["id"]["channelId"],
# 								result['snippet']['description'],
# 								result['snippet']['thumbnails']['default']['url']))
		
	print("Videos:\n", "\n".join(videos), "\n")
	
	return final_return
# 	print("Channels:\n", "\n".join(channels), "\n")
# 	print("Playlists:\n", "\n".join(playlists), "\n")


def video_comments(video_id):
	# empty list for storing reply
	replies = []

	# retrieve youtube video results
	video_response=youtube_object.commentThreads().list(
	part='snippet,replies',
	videoId=video_id
	).execute()
	
	final=[]

	# iterate video response
	while video_response:
		
		# extracting required info
		# from each result object
		for item in video_response['items']:
			
			# Extracting comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			
			
			# counting number of reply of comment
			replycount = item['snippet']['totalReplyCount']

			# if reply is there
			if replycount>0:
				
				# iterate through all reply
				for reply in item['replies']['comments']:
					
					# Extract reply
					reply = reply['snippet']['textDisplay']
					
					# Store reply is list
					replies.append(reply)
					

			soup = BeautifulSoup(comment,features="html.parser")
			
			# print(soup.get_text('\n'), ",",replies, end = '\n\n')

			final.append(translate(soup.get_text('\n')))
			for reply in replies:
				soup = BeautifulSoup(reply,features="html.parser")
				print("=====================================")
				
				final.append(translate(soup.get_text('\n')))
			
			# empty reply list
			replies = []

		if(len(final)>20):
			break
		# Again repeat
		if 'nextPageToken' in video_response:
			video_response = youtube_object.commentThreads().list(
					part = 'snippet,replies',
					videoId = video_id,
					pageToken = video_response['nextPageToken']
				).execute()
		else:
			break
	
	return final

def get_maxlen(corpus):
	maxlen = 0
	for sent in corpus:
		maxlen = max(maxlen, len(sent))
	return maxlen

def word_embedding(texts):
	MAX_NB_WORDS = 40000
	stopwords=['a',
	'about',
	'again',
	'against',
	'ain',
	'all',
	'am',
	'an',
	'and',
	'any',
	'are',
	'aren',
	"aren't",
	'as',
	'at',
	'be',
	'been',
	'being',
	'between',
	'both',
	'but',
	'by',
	'can',
	'couldn',
	"couldn't",
	'd',
	'did',
	'didn',
	"didn't",
	'do',
	'does',
	'doesn',
	"doesn't",
	'doing',
	'don',
	"don't",
	'for',
	'from',
	'further',
	'had',
	'hadn',
	"hadn't",
	'has',
	'hasn',
	"hasn't",
	'have',
	'haven',
	"haven't",
	'having',
	'he',
	'her',
	'here',
	'hers',
	'herself',
	'him',
	'himself',
	'his',
	'how',
	'i',
	'if',
	'in',
	'into',
	'is',
	'isn',
	"isn't",
	'it',
	"it's",
	'its',
	'itself',
	'just',
	'll',
	'm',
	'ma',
	'me',
	'mightn',
	"mightn't",
	'more',
	'most',
	'mustn',
	"mustn't",
	'my',
	'myself',
	'needn',
	"needn't",
	'nor',
	'o',
	'of',
	'on',
	'once',
	'only',
	'or',
	'other',
	'our',
	'ours',
	'ourselves',
	'out',
	'over',
	'own',
	're',
	's',
	'shan',
	"shan't",
	'she',
	"she's",
	'should',
	"should've",
	'shouldn',
	"shouldn't",
	'so',
	'some',
	'such',
	't',
	'than',
	'that',
	"that'll",
	'the',
	'their',
	'theirs',
	'them',
	'themselves',
	'then',
	'there',
	'these',
	'they',
	'this',
	'those',
	'through',
	'to',
	'too',
	'under',
	'until',
	'up',
	've',
	'very',
	'was',
	'wasn',
	"wasn't",
	'we',
	'were',
	'weren',
	"weren't",
	'what',
	'when',
	'where',
	'which',
	'while',
	'who',
	'whom',
	'why',
	'will',
	'with',
	'won',
	"won't",
	'wouldn',
	"wouldn't",
	'y',
	'you',
	"you'd",
	"you'll",
	"you're",
	"you've",
	'your',
	'yours',
	'yourself',
	'yourselves']
	nltk.download('stopwords')
	nltk.download('punkt')
	nltk.download('wordnet')
	nltk.download('omw-1.4')

	corpus = []
	for i in range(0, len(texts)):
		print(i)
		review = texts[i].split()
		review= [word for word in review if not word.startswith('@') ]
		review = ' '.join(review)
		
		review = re.sub('[^a-zA-Z]', ' ',review)
		review = review.lower()
		
		review= str(TextBlob(review).correct())
		
		review = word_tokenize(review)
		final=[]
		for word in review:
			if word.endswith("'t"):
				word='not'
			if word not in stopwords:
				final.append(wl.lemmatize(word,pos='v'))
		
		final = ' '.join(final)
		print(texts[i])
		print(final)
		corpus.append(final)
	onehot_repr=[one_hot(words,MAX_NB_WORDS)for words in corpus] 
	maxlen=get_maxlen(corpus)
	embedded_docs=pad_sequences(onehot_repr,padding='pre',maxlen=127)
	data=np.array(embedded_docs)
	return data


def model_predict(data):
	model = load_model("sentiment_analysis_model.h5")
	y_pred = model.predict(data)
	y_pred_class = np.argmax(y_pred,axis=1)
	unique = np.array(np.unique(y_pred_class,return_counts=True)).T
	uniques, counts = np.unique(y_pred_class, return_counts=True)
	print(counts)
	print(y_pred_class)
	return counts


@app.route('/plot1.png')
def plot1_png():
	fig = create_figure(list(final_range[1]))
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot2.png')
def plot2_png():
	fig = create_figure(list(final_range[2]))
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot3.png')
def plot3_png():
	fig = create_figure(list(final_range[3]))
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

def create_figure(value):
	value=list(value)
	fig = Figure(figsize=(6,3.5))
	axis = fig.add_subplot(1, 1, 1)
	category=['Extremely happy','happy','neutral','sad','Angry']
	
	axis.barh(category,value)
	for s in ['top', 'bottom', 'left', 'right']:
		axis.spines[s].set_visible(False)
    
	axis.set_title("Sentiment Analytics")

	# Remove x, y Ticks
	axis.xaxis.set_ticks_position('none')
	axis.yaxis.set_ticks_position('none')
	
	# Add padding between axes and labels
	axis.xaxis.set_tick_params(pad = 5)
	axis.yaxis.set_tick_params(pad = 0)
	
	# Add x, y gridlines
	axis.grid(visible = True, color ='grey',
			linestyle ='-.', linewidth = 0.5,
			alpha = 0.2)
	
	# Show top values
	axis.invert_yaxis()
	
	# Add annotation to bars
	for i in axis.patches:
		plt.text(i.get_width()+0.2, i.get_y()+0.5,
				str(round((i.get_width()), 2)),
				fontsize = 10, fontweight ='bold',
				color ='grey')
	

	# Adding the labels
	axis.set_ylabel("Category")
	axis.set_xlabel("Range")
	axis.set_xlim([0,1])
	fig.tight_layout()
	return fig


	# import pandas as pd
	# from matplotlib import pyplot as plt
	
		
	# # Figure Size
	# fig, ax = plt.subplots(figsize =(16, 9))
	
	# # Horizontal Bar Plot
	# ax.barh(name, price)
	
	# # Remove axes splines
	# for s in ['top', 'bottom', 'left', 'right']:
	# 	ax.spines[s].set_visible(False)
	
	# # Remove x, y Ticks
	# ax.xaxis.set_ticks_position('none')
	# ax.yaxis.set_ticks_position('none')
	
	# # Add padding between axes and labels
	# ax.xaxis.set_tick_params(pad = 5)
	# ax.yaxis.set_tick_params(pad = 10)
	
	# # Add x, y gridlines
	# ax.grid(b = True, color ='grey',
	# 		linestyle ='-.', linewidth = 0.5,
	# 		alpha = 0.2)
	
	# # Show top values
	# ax.invert_yaxis()
	
	# # Add annotation to bars
	# for i in ax.patches:
	# 	plt.text(i.get_width()+0.2, i.get_y()+0.5,
	# 			str(round((i.get_width()), 2)),
	# 			fontsize = 10, fontweight ='bold',
	# 			color ='grey')
	
	# # Add Plot Title
	# ax.set_title('Sports car and their price in crore',
	# 			loc ='left', )
	
	# # Show Plot
	# plt.show()

@app.route('/', methods=["POST","GET"])
def search_results():
	if request.method=="POST":
		query=request.form['query'] 
		result = youtube_search_keyword(query, max_results = 1)
		return render_template('index.html',result=result)
	if request.method=="GET":

		result=youtube_search_keyword('BE education', max_results = 3)
		print(result)
		return render_template('index.html',result=result)

if __name__=='__main__':
	app.run(debug=True)