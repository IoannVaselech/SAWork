from googleapiclient.discovery import build
from utils import snippet_to_dict, get_video_id

def get_live_chat_id(video_id, service):
    response = service.videos().list(part="liveStreamingDetails", id=video_id).execute()
    live_streaming_details = response.get('items', [])
    if live_streaming_details:
        live_streaming_details = live_streaming_details[0]['liveStreamingDetails']
        if 'activeLiveChatId' in live_streaming_details:
            return live_streaming_details['activeLiveChatId']

    return None


def get_live_chat_comments(live_chat_id, service):
    comments = []

    args = {
        'part': 'id,snippet',
        'maxResults': 100
    }

    r = service.liveChatMessages().list(liveChatId=live_chat_id, part=args['part'],
                                        maxResults=args['maxResults']).execute()

    for comment in r['items']:
        comment_id = comment['id']
        snippet = comment['snippet']
        comments.append(snippet_to_dict(comment_id, snippet))

    return comments
