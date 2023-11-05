from googleapiclient.errors import HttpError
from helpers import snippet_to_dict, get_replies

def get_comments(video_id, service, progress_callback):
    comments = []

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
            # Обработка других ошибок
            print(f"An error occurred: {e}")
            return comments

    total_results = r['pageInfo']['totalResults']
    progress_callback(0, total_results)

    for index, top_level in enumerate(r.get('items', [])):
        comment_id = top_level['snippet']['topLevelComment']['id']
        snippet = top_level['snippet']['topLevelComment']['snippet']
        comment_text = snippet['textOriginal']
        comment_text = comment_text.replace('\n\n', '\n').replace('\n', ' ')
        comments.append(snippet_to_dict(comment_id, snippet))
        replies = get_replies(comment_id, service)
        comments += replies
        progress_callback(index + 1, total_results)

    next_page_token = r.get('nextPageToken')
    if not next_page_token:
        return comments

    for page in range(1, 5):
        try:

            r = service.commentThreads().list(videoId=video_id, part=args['part'], maxResults=args['maxResults'], pageToken=next_page_token).execute()
        except HttpError as e:
            if e.resp.status == 403 and 'commentsDisabled' in str(e):
                print(f"Comments are disabled for video: {video_id}")
                return comments
            else:
                # Обработка других ошибок
                print(f"An error occurred: {e}")
                return comments

        total_results = r['pageInfo']['totalResults']
        progress_callback(page * args['maxResults'], total_results)

        for index, top_level in enumerate(r.get('items', [])):
            comment_id = top_level['snippet']['topLevelComment']['id']
            snippet = top_level['snippet']['topLevelComment']['snippet']
            comment_text = snippet['textOriginal']
            comment_text = comment_text.replace('\n\n', '\n').replace('\n', ' ')
            comments.append(snippet_to_dict(comment_id, snippet))
            replies = get_replies(comment_id, service)
            comments += replies
            progress_callback(page * args['maxResults'] + index + 1, total_results)

        next_page_token = r.get('nextPageToken')
        if not next_page_token:
            break

    return comments
