import requests
from datetime import datetime
import sys

# Run the script by running recent_lessons <API Bearer Token>
headers = {"Authorization": "Bearer " + sys.argv[1]}

reviews = requests.get(url='https://api.wanikani.com/v2/review_statistics', headers=headers)
rev_list = list()
while reviews.json()['pages']['next_url']:
    next_url = reviews.json()['pages']['next_url']
    for x in reviews.json()['data']:
        rev_list.append(x)
    reviews = requests.get(url=next_url, headers=headers)
for x in reviews.json()['data']:
    rev_list.append(x)
rev_list = list(
    filter(lambda x: ((datetime.now() - datetime.strptime(x['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')).days < 7),
           rev_list))

subjects = list()
for x in rev_list:
    subjects.append(x['data']['subject_id'])

print(subjects)
