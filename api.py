
import requests
from datetime import datetime, timezone

NOTION_TOKEN = "secret_gWbHCCekHyWzV5jSXG47e3PGkzZeyePhtOplgUTVnLM"
DATABASE_ID = "5d6b43874ab04bb09e02bd6e0e79e88d"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_pages(num_pages=None):
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # ce code juste pour creer le fichier json 
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

pages = get_pages()

for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)
    print(url, title, published)
    
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res

URL = " URL"
Title = "Test TITLE new  "
published_date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "URL": {"title": [{"text": {"content": URL}}]}, 
    "Title": {"rich_text": [{"text": {"content": Title}}]},
    "Published": {"date": {"start": published_date, "end": None}}
}

create_page(data)

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res

page_id = "d1d49b61748e4f7d8d9196812647732d"

new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()

title = "updated title"
update_data = {"Title": {"rich_text":[{"text": {"content": title}}] } ,"Published": {"date": {"start": new_date, "end": None}} }

update_page(page_id, update_data)

def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    return res

new_page_id = "3cef6f2dbf1b460f9eaee77e74347e83"
delete_page(new_page_id)