from flask import Flask, jsonify, request 
from flask_cors import CORS 
import pizza #pizza is a config file for the piazza api wrapper. DM if you want access.
import db #db is a config file that inits mongodb. DM if you want access.
#import dis #dis is a config file that holds the api keys for discord. DM if you want access.
from piazza_api import Piazza
from piazza_api import network as net
import re
#shhhhhhhhh
import requests
app = Flask(__name__)

def sendPayload(postObj):
  # print(postObj['history'][0]['subject'])
  # print("https://piazza.com/class/keke5ooeun21ot?cid="  + str(postObj['nr']))
  # print(re.sub('<[^<]+?>', '', str(postObj['history'][0]['content'])) + "...")
  # print(postObj['unique_views'])
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
  result = requests.post(pizza.url, json=data, headers={"Content-Type": "application/json"})

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("succ {}.".format(result.status_code))


@app.route("/test")
def test():
  existingPosts = []
  query = db.table.find() 
  output = {} 
  i = 0
  for x in query: 
    output[i] = x 
    output[i].pop('_id') 
    existingPosts.append(output[i]['ID'] ) 
    i += 1
  #print(existingPosts)
  p = Piazza()
  p.user_login(pizza.email, pizza.password)
  ds = p.network(pizza.net)
  #print("ds", ds.iter_all_posts())
  posts = ds.iter_all_posts()
  for post in posts:
    print("post", post)
    if post['history'][0]['subject']  in existingPosts:
      sendPayload(post)
      queryObject = { 
        'ID': post['history'][0]['subject'],
      }
      #query = db.table.insert_one(queryObject) 
  # ds_posts = ds.get_filtered_feed(net.UnreadFilter())
  # if len(ds_posts['feed']) > 0:
  #   print("length", len(ds_posts['feed']))
  #   for x in range(0, len(ds_posts['feed'])):
  #     print(ds_posts['feed'][x]['subject'])

  return "Connected to the data base!"


@app.route('/')
def rootAcc():
    return 'h̸̨̨̧̳̯̻͕̩̙̟̯̐́̒͂̂͝ē̸̢̡̧̡̡̡̧̛̛̠̲̥̫̘͈̦̭̺͚̠̹̲̟̭͈͎̫̱̤͙̘̙̘͎̼̱͓͍͈̯̻̞̹͍̻̦͖̤̪̞̗̠͕̖͎̠̙̖̲͉͓͕̖͓̭̦̙̝̟̣̖̭͈͚̱̯̜̲̥͈̯̙̻͒̀̏̄̋͌͊̇̋̈́͑͆̌̈́̋̽̃̍͌́͑̓̋̀̊̈́̒̃̇̾̒͆̈́̓̋̇̇͂͆̒̏̿̓̑̀̽̂͐̌̕̕̚͘̕ͅl̸̢̡̛̩͇̦̠͇̤͖̬̝͙̰̟̱̺̯͓̪̤͖̩̞̩͚̠̫͓̠̥̎̾̔̐̌͗̋̀͛̊̆̓̀̽͊̈́͗͌̄͋̀́̈͌͐̆̈͛͑̽̃̊̆̓̅̍̃́́̿́̾͂̿́̀̀͆̾̓̏͛͘͘̕͝͠͝͝͠l̴̨̨̨̨̧̡̢̢̢̨̧̛̗̥̙̮̫͎̼̮̤͕̠̹̙͇̜͕̰̰̲͇̤̗̙̜͔̻͇̖̦͉̻̪̝̬̭̯̲̻̹̱̤̼̪̲̻̩͇͚͕̭̼͊̌̃͂͑́̚͜͜͜ͅͅͅơ̶̧̢̨̧̡̘͓̤̼̫͎̣̞͕̯͇͕̹̬͉̝͚̮͖͍̖̖̪̣͙̱̰̾̽̏͛̐̒͆̄̿̆͒͊̋̃̆̏̆̈́̈́̈̀̏̈́̾͌͑̉͐̍͋̅̈́̐͐̈́͗͗̓̀̈͊͋̈́̎̄͗̕̚͝͝͝͝͝͝͝͠'



if __name__ == '__main__':
    app.run(port=8000, debug=True)



