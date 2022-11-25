from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
import datetime
import dateutil.parser
import pytz

dotenv_path = '.env'
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# creating Youtube Resource Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
										developerKey = DEVELOPER_KEY)

video_ids=["iSQdbXcAd20","mTacjBVUDyg","BKvPkcfDE_4","FtvIZ_mLoMM","UPZ7fwGUcVw","CnGjePpCh94","oMrA0FhQD6g","3oMXsnXW5Sw","nOpUklDFjxY","qISBVpb7FMg","SgEHyoKyLA4","Y1Ui-NdE-zs","bNppB3ZT-Ws","hKrAoh5Ayhg","Z7btuaEWjOQ"]

def connect_to_db():
	conn = psycopg2.connect(
	   database=os.getenv('DB_MAIN'), user=os.getenv('USER_MAIN'), password=os.getenv('PASSWORD_MAIN'), host=os.getenv('HOST_MAIN'), port= '5432'
	)
	cur = conn.cursor()
	return cur, conn


def youtube_title_description(video_ids):
	for video_id in video_ids:
		video_request=youtube_object.videos().list(
			part='snippet,statistics',
			id=video_id
		)
		video_response = video_request.execute()
		title=video_response['items'][0]['snippet']['title']
		description=video_response['items'][0]['snippet']['description']
		cur,conn = connect_to_db()
		if(pd.read_sql(f'''SELECT * from public.videos where video_id='{video_id}' and title='{title.replace("'","")}' and description='{description.replace("'","")}' ''', con=conn).empty):
			if(pd.read_sql(f'''SELECT * from public.videos where video_id='{video_id}' ''', con=conn).empty):
				query = f"""INSERT INTO  public.videos (video_id,title,description) VALUES ('{video_id}','{title.replace("'","")}','{description.replace("'","")}')"""
				cur.execute(query)
				print("insert")
				conn.commit()
			else:
				query = f"""update public.videos set title='{title.replace("'","")}',description='{description.replace("'","")}' where video_id='{video_id}'"""
				cur.execute(query)
				conn.commit()
				print("update")
		else:
			print("Not")

		video_comments(video_id)


		cur.close()
		conn.close()

		


def video_comments(video_id):
	# empty list for storing reply
	replies = []

	# retrieve youtube video results
	video_response=youtube_object.commentThreads().list(
	part='snippet,replies',
	videoId=video_id
	).execute()

	# iterate video response
	while video_response:
		for item in video_response['items']:
			# Extracting comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay'].replace("'","")
			replies.append(comment)
			updated_at= item['snippet']['topLevelComment']['snippet']['updatedAt']
			# counting number of reply of comment
			replycount = item['snippet']['totalReplyCount']
			comment_id=item['id']

			insertion_date = dateutil.parser.parse(updated_at)
			diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - insertion_date

			cur,conn = connect_to_db()
			if(pd.read_sql(f'''SELECT * from public.comments where comment_id='{comment_id}' ''', con=conn).empty):
				query = f"""INSERT INTO  public.comments (video_id,comment_id,content) VALUES ('{video_id}','{comment_id}','{comment}')"""
				cur.execute(query)
				print("comment insert")
				conn.commit()
			elif(diffretiation.total_seconds()//60<60):
				query = f"""update public.comments set content='{comment}' where comment_id='{comment_id}'"""
				cur.execute(query)
				conn.commit()
				print("comment update")
			else:
				print("comment not")


			# if reply is there
			if replycount>0:
								
				# iterate through all reply
				for reply in item['replies']['comments']:
					
					reply_content = reply['snippet']['textDisplay'].replace("'","")
					# Store reply is list
					replies.append(reply)
					reply_updated_at= reply['snippet']['updatedAt']
					reply_id=reply['id']
					reply_insertion_date = dateutil.parser.parse(reply_updated_at)
					reply_diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - reply_insertion_date

					if(pd.read_sql(f'''SELECT * from public.replies where reply_id='{reply_id}' ''', con=conn).empty):
						query = f"""INSERT INTO  public.replies (video_id,reply_id,content) VALUES ('{video_id}','{reply_id}','{reply_content}')"""
						cur.execute(query)
						print("reply insert")
						conn.commit()
					elif(reply_diffretiation.total_seconds()//60<60):
						query = f"""update public.replies set content='{reply_content}' where comment_id='{reply_id}'"""
						cur.execute(query)
						conn.commit()
						print("reply update")
					else:
						print("reply not")

					

			# soup = BeautifulSoup(comment,features="html.parser")
			# print(soup.get_text('\n'), replies, end = '\n\n')
			# empty reply list
			replies = []

		# Again repeat
		if 'nextPageToken' in video_response:
			video_response = youtube_object.commentThreads().list(
					part = 'snippet,replies',
					videoId = video_id,
					pageToken = video_response['nextPageToken']
				).execute()
		else:
			break

		cur.close()
		conn.close()

if __name__ == "__main__":
	# youtube_search_keyword('BE Computer Science', max_results = 7)
	youtube_title_description(video_ids)
	# video_request=youtube_object.videos().list(
	# part='snippet,statistics',
	# id="iSQdbXcAd20"
	# )
	# video_response = video_request.execute()
	# print("\n\n\n",video_response)
	
