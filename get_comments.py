from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def snippet_to_dict(comment_id, snippet, parent_comment_id=False):
    t = {
        'comment_id': comment_id,
        'parent_id': parent_comment_id,
        'author': snippet['authorDisplayName'],
        'text': snippet['textOriginal']
    }
    return t


def get_replies(comment_id, service):
    replies = service.comments().list(part='snippet', parentId=comment_id, maxResults=100).execute()
    replies_list = []
    for reply in replies['items']:
        reply_comment_id = reply['id']
        reply_snippet = reply['snippet']
        replies_list.append(snippet_to_dict(reply_comment_id, reply_snippet, parent_comment_id=comment_id))
        replies_list += get_replies(reply_comment_id, service)
    return replies_list


def get_comments(video_id, service):
    comments = []
    max_pages = 100  # You can adjust this as needed

    args = {
        'videoUrl': f"https://www.youtube.com/watch?v={video_id}",
        'part': 'id,snippet',
        'maxResults': 100
    }

    try:
        r = service.commentThreads().list(videoId=video_id, part=args['part'], maxResults=args['maxResults']).execute()
    except HttpError as e:
        if e.resp.status == 403 and 'commentsDisabled' in str(e):
            print(f"Comments are disabled for video: {video_id}")
            return comments
        else:
            # Handle other errors
            print(f"An error occurred: {e}")
            return comments

    print(f"0/9000 = {r['pageInfo']['totalResults']}")

    for page in range(1, max_pages + 1):
        for top_level in r.get('items', []):
            comment_id = top_level['snippet']['topLevelComment']['id']
            snippet = top_level['snippet']['topLevelComment']['snippet']
            comment_text = snippet['textOriginal']
            comment_text = comment_text.replace('\n\n', '\n').replace('\n', ' ')
            comments.append(snippet_to_dict(comment_id, snippet))
            replies = get_replies(comment_id, service)
            comments += replies

        next_page_token = r.get('nextPageToken')
        if not next_page_token:
            break

        print(f"{page}/{max_pages} = {r['pageInfo']['totalResults']}")

        try:
            r = service.commentThreads().list(
                videoId=video_id,
                part=args['part'],
                maxResults=args['maxResults'],
                pageToken=next_page_token
            ).execute()
        except HttpError as e:
            if e.resp.status == 403 and 'commentsDisabled' in str(e):
                print(f"Comments are disabled for video: {video_id}")
                return comments
            else:
                # Handle other errors
                print(f"An error occurred: {e}")
                return comments

    return comments
