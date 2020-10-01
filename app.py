from flask import Flask
import pizzapizzasecret #pizzapizzasecret has all the secrets
from piazza_api import Piazza
from piazza_api import network as net
import re
import pymongo
import time
import requests
app = Flask(__name__)

def sendPayload(postObj):
    data = {}
    data["content"] = "New post: " + postObj['created']
    data["username"] = "CMSC PIAZZA BOT"
    data["embeds"] = []
    embed = {}
    embed["description"] = re.sub('<[^<]+?>', '', str(postObj['history'][0]['content']))
    embed["title"] = postObj['history'][0]['subject']
    embed["url"] = "https://piazza.com/class/keke5ooeun21ot?cid="  + str(postObj['nr'])
    embed["color"] = 0XA5E0FE
    data["embeds"].append(embed)
    result = requests.post(pizzapizzasecret.url, json=data, headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
        time.sleep(5)
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("succ {}.".format(result.status_code))


@app.route("/check")
def test():
    client = pymongo.MongoClient(pizzapizzasecret.dbsecret)
    db = client.get_database('piazza-posts')
    table = db.posts
    existingPosts = []
    query = table.find()
    print(query)
    output = {}
    i = 0
    for x in query:
        output[i] = x
        output[i].pop('_id')
        existingPosts.append(output[i]['ID'] )
        i += 1
    print(existingPosts)
    p = Piazza()
    p.user_login(pizzapizzasecret.email, pizzapizzasecret.password)
    ds = p.network(pizzapizzasecret.net)
    #print("ds", ds.iter_all_posts())
    posts = ds.iter_all_posts()
    for post in posts:
        #print("post", post)
        if post['history'][0]['subject'] not in existingPosts:
            payload = post['history'][0]['subject']
            print(payload)
            queryObject = {
                'ID': payload,
            }
            queryMongo = table.insert_one(queryObject)
            sendPayload(post)

        else:
            print("piazza channel up to date")
    return "success"


@app.route('/')
def rootAcc():
    return 'h̸̨̨̧̳̯̻͕̩̙̟̯̐́̒͂̂͝ē̸̢̡̧̡̡̡̧̛̛̠̲̥̫̘͈̦̭̺͚̠̹̲̟̭͈͎̫̱̤͙̘̙̘͎̼̱͓͍͈̯̻̞̹͍̻̦͖̤̪̞̗̠͕̖͎̠̙̖̲͉͓͕̖͓̭̦̙̝̟̣̖̭͈͚̱̯̜̲̥͈̯̙̻͒̀̏̄̋͌͊̇̋̈́͑͆̌̈́̋̽̃̍͌́͑̓̋̀̊̈́̒̃̇̾̒͆̈́̓̋̇̇͂͆̒̏̿̓̑̀̽̂͐̌̕̕̚͘̕ͅl̸̢̡̛̩͇̦̠͇̤͖̬̝͙̰̟̱̺̯͓̪̤͖̩̞̩͚̠̫͓̠̥̎̾̔̐̌͗̋̀͛̊̆̓̀̽͊̈́͗͌̄͋̀́̈͌͐̆̈͛͑̽̃̊̆̓̅̍̃́́̿́̾͂̿́̀̀͆̾̓̏͛͘͘̕͝͠͝͝͠l̴̨̨̨̨̧̡̢̢̢̨̧̛̗̥̙̮̫͎̼̮̤͕̠̹̙͇̜͕̰̰̲͇̤̗̙̜͔̻͇̖̦͉̻̪̝̬̭̯̲̻̹̱̤̼̪̲̻̩͇͚͕̭̼͊̌̃͂͑́̚͜͜͜ͅͅͅơ̶̧̢̨̧̡̘͓̤̼̫͎̣̞͕̯͇͕̹̬͉̝͚̮͖͍̖̖̪̣͙̱̰̾̽̏͛̐̒͆̄̿̆͒͊̋̃̆̏̆̈́̈́̈̀̏̈́̾͌͑̉͐̍͋̅̈́̐͐̈́͗͗̓̀̈͊͋̈́̎̄͗̕̚͝͝͝͝͝͝͝͠ yes, cmsc is misspelled '



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)



