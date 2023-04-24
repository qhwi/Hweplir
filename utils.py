import discord
import urllib.request
import json

def create_embed(title=None, description=None, color=0xFCBA03, fields=[], values=[], inlines=[], footer=None, url=None, timestamp=None, thumbnail = None):
  embed = discord.Embed(title=title, description=description, color=color, url=url, timestamp=timestamp)
  n = len(fields)
  if n != len(values):
    print("Error - Unable to send embed: Mismatched field and value array")
    return None
  if n != len(inlines):
    inlines = [False for i in range(n)]
  if footer != None:
    embed.set_footer(text=footer)
  if thumbnail != None:
    embed.set_thumbnail(url=thumbnail)
  for i in range(n):
    embed.add_field(name=fields[i], value=values[i], inline=inlines[i])
  return embed

def getjson(url):
  try:
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    return json.loads(response.read())
  except urllib.error.HTTPError:
    return 404
