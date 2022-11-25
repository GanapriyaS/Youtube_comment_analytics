from googleapiclient.discovery import build
from bs4 import BeautifulSoup
# Arguments that need to passed to the build function
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# creating Youtube Resource Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
										developerKey = DEVELOPER_KEY)


def youtube_search_keyword(query, max_results):
	
# 	# calling the search.list method to
# 	# retrieve youtube search results
	search_keyword = youtube_object.search().list(q = query, part = "id, snippet", maxResults = max_results).execute()
	
	# extracting the results from search response
	results = search_keyword.get("items", [])


	# empty list to store video,
	# channel, playlist metadata
	videos = []
	playlists = []
	channels = []
	
	# extracting required info from each result object
	for result in results:
		# video result object
		if result['id']['kind'] == "youtube#video":
			videos.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],result["id"]["videoId"], result['snippet']['description'],result['snippet']['thumbnails']['default']['url']))
			video_comments(result["id"]["videoId"])
			print("==========================")
            
            
            
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
		
	print("Videos:\n", "\n\n\n".join(videos), "\n")
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

	# iterate video response
	while video_response:
		# print(video_response)
		# extracting required info
		# from each result object
		print(len(video_response['items']))
		for item in video_response['items']:
			# Extracting comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			updated_at= item['snippet']['topLevelComment']['snippet']['updatedAt']
			
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
					# print(reply)

			soup = BeautifulSoup(comment,features="html.parser")
            
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

if __name__ == "__main__":
	youtube_search_keyword('BE Computer Science', max_results = 7)
	# video_request=youtube_object.videos().list(
	# part='snippet,statistics',
	# id="iSQdbXcAd20"
	# )
	# video_response = video_request.execute()
	# print("\n\n\n",video_response)
	
