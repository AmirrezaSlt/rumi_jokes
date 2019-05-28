from pymongo import MongoClient
from termcolor import colored
import requests

mongo_client = MongoClient("127.0.0.1:27018")
db = mongo_client.dbms
mycol = db['Joke']
# Making request
req_obj = requests.get('http://api.icndb.com/jokes/')
r = req_obj.json()
status = r["type"]
print("api call status : " + status)
for i in range(30):
    categories = r["value"][i]["categories"]
    if "explicit" in categories:
        continue
    if i % 2 == 0:
        user_id = 1
    elif i % 2 == 1:
        user_id = 2
    # else:
    #     user_id = 3
    #  if active mod by 3
    joke = r["value"][i]["joke"]
    joke = joke.replace("&quot;", '\"')
    mydict = {'content': joke, 'views': 0, 'score': 0, 'author': user_id}
    mycol.insert_one(mydict)
    # post_str = "http://www.rumi.com/api/userFeedbackJokeSubmit?cn_user_id=4f67936a91d408bf2a000002&joke_text="
    # post_final = post_str + joke
    # requests.post(post_final)


mongo_client.close()
print(colored("Success!", 'green'))
