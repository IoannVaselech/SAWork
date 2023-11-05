from urllib.parse import urlparse, parse_qs


def snippet_to_dict(comment_id, snippet, parent_comment_id=False):
    t = {
        'comment_id': comment_id,

        'parent_id': parent_comment_id,
        'author': snippet['authorDisplayName'],
        'text': snippet['textOriginal']
    }
    return t


def get_video_id(video_url):
    parsed_url = urlparse(video_url)
    query = parsed_url.query
    if query:
        video_id = parse_qs(query).get('v', [''])[0]
        return video_id
    else:
        path = parsed_url.path.strip('/')
        if path.startswith('channel/'):
            channel_id = path.split('/')[1]
            return channel_id

    return None
