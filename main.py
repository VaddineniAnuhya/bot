import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words=['sad','depresses','angry','not happy','unhappy','depression','depressed']

encourage=['Cheer up','Hang in there','You are a great person / bot!']

if 'responding' not in db.keys():
  db['responding'] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+'-'+json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements']=encouragements
  else:
    db['encouragements'] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  #0 will be replaced by client i.e which api key we provide according to that,the username will be replaced 

#if the message is from author i.e ourselves (bot)the bot shouldnt do anything .if the msg is from bot itself then the bot shouldnt react
@client.event
async def on_message(message):
  if message.author==client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  msg=message.content
  if db['responding']:
    options = encourage
    if 'encouragements' in db.keys():
      options = options.extend(db['encouragements'])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(encourage))
  #now if user asks for updating the encouragements 
  if msg.startswith('$new'):
    #we should check whether it was starting with $new and take that encourging message which will be typed after $new
    encouraging_message = msg.split('$new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('New encouraging message added.')

    #now if user asks for updating the encouragements 
  if msg.startswith('$del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_encouragements(index)
      encouragements = db['encouragements']
      await message.channel.send(encouragements)
  
  if msg.startswith('$list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)


  if msg.startswith('$responding'):
    value = msg.split('$responding ',1)[1]

    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on')

    else:
      db['responding'] = False
      await message.channel.send('Responding is off')


my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)

#now we should run our client ie our bot for that we need token of our bot which we can get from #https://discord.com/developers/applications/858657675998265344/bot it should be private for that we using #environments variables
#getting the token by environ
  
