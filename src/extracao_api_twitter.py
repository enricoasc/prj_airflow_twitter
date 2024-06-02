from datetime import datetime, timedelta
import requests
import json
import os 


# MONTANDO URL
TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.00Z'

end_time = (datetime.now() + timedelta( hours=3,seconds=-30) ).strftime(TIMESTAMP_FORMAT)
start_time = (datetime.now() + timedelta(days=-7, hours=3 )).strftime(TIMESTAMP_FORMAT)
query = 'data science'

tweet_fields = 'tweet.fields=author_id,conversation_id,creted_at,id,in_replay_to_user_id,public_metrics,lang,text'
user_fields = 'expansions=author_id&user.fields=id,name,username,creted_at'

url_raw = f"https://labdados.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

# MONTANDO HEADERS 
bearer_token = '5ADS4F5SA4F5A4SF54ASDF4AS544F' ##os.environ.get('BEARER_TOKEN')
headers = {'Authorizations':'Bearer {}'.format(bearer_token)}
response = requests.request('GET',url_raw, headers=headers)

json_response = response.json()
# print(bearer_token)

# IMPRIMANDO JSON
print(json.dumps(json_response,indent=4,sort_keys=True))

## PAGINATE
while 'next_token' in json_response.get('meta',{}):
    next_token = json_response['meta']['next_token']
    url = f"{url_raw}&next_tken={next_token}"
    response = requests.request('GET',url,headers=headers)
    json_response = response.json()
    print(json.dumps(json_response,indent=4,sort_keys=True))

