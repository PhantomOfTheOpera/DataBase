import json



def check_response(json_data):
    if json_data['status'] != 'ok' or json_data["totalResults"] < 1:
        return False
    return True


def check_present_content(value):
    if value is None:
        value = 0
    return value


def article_categorizer(entry):
    time = check_present_content(entry['publishedAt'])
    source = check_present_content(entry['source']['name'])
    title = check_present_content(entry['title'])
    url = check_present_content(entry['url'])
    content = check_present_content(entry['content'])
    return time, source, title, url, content


