import discord
import json, datetime
from math import ceil
import utils

def getCTF(ctftime_id, creating = False, username = None, password = None):
  data = utils.getjson("https://ctftime.org/api/v1/events/" + str(ctftime_id) + '/')
  if data == 404:
    if creating:
      return False, False, False
    else:
      return False
    
  start = int(datetime.datetime(int(data['start'][0:4]), int(data['start'][5:7]), int(data['start'][8:10]), int(data['start'][11:13]), int(data['start'][14:16]), int(data['start'][17:19])).timestamp())
  end = start + (data['duration']['hours'] + 24*data['duration']['days']) *3600
  ctf_fields = ['Time','Rating weight']
  ctf_fieldsinfo = ['Start: <t:{0}:t> <t:{0}:d>\nEnd: <t:{1}:t> <t:{1}:d>'.format(str(start),str(end)), data['weight']]

  if creating:
    ctf_fields.insert(0,'Login')
    if username != None:
      ctf_fieldsinfo.insert(0,'Username: '+username+'\nPassword: '+password)
    else:
      ctf_fieldsinfo.insert(0, "Đang đợi ai đó /regacc...")
  
  fmat = data['format']
  if fmat == 'Attack-Defense':
      fmat += ' ⚔'
  elif fmat == 'Hack quest':
      fmat += ' 🌄'
  if data['onsite'] == True:
    fmat += '\nOn-site: ' + data['location']
  if data['restrictions'] != "Open":
    fmat += '\nRestricted (' + data['restrictions'] + ')'
  if fmat == 'Jeopardy':
      fmat = None
  else:
    ctf_fields.append('Format')
    ctf_fieldsinfo.append(fmat)
  
  discord_link = None
  if 'discord.gg' in data['description']:
      discord_link = "https://"
      i = data['description'].find('discord.gg')
      c = data['description'][i]
      for j in range(25):
          if c not in '\r\n \t%*^$#@?=':
              discord_link += c
          i += 1
          if i == len(data['description']):
            break
          c = data['description'][i]
      ctf_fields.append('Discord')
      ctf_fieldsinfo.append(discord_link)

  logo = data['logo']
  if len(logo) < 5:
    logo = None

  embedVar = utils.create_embed(title=data['title'], description=data['url'], fields=ctf_fields, values=ctf_fieldsinfo, footer=data['ctftime_url'], thumbnail = logo, color = 0xd50000)
  if creating:
    return data['title'], end+1209600, embedVar #archive after 2 weeks
  else:
    return embedVar


def findCTF(searchkey):
  data = utils.getjson('https://ctftime.org/api/v1/events/?limit=1000')
  if data == 404:
    return 0

  found_id = 0
  for ctf in data:
    if "".join(searchkey.split()).lower() in "".join(ctf['title'].split()).lower():
      found_id = ctf['id']
      return found_id
  return 0  
      

def getUpcoCTF(page, step):
  data = utils.getjson('https://ctftime.org/api/v1/events/?limit=1000')
  if data == 404 or step<1 or page<0:
    return False, 0

  ctf_fields = []
  ctf_fieldsinfo = []
  warned_footer = ''
  
  npage = ceil(len(data)/step)

  if page >= npage:
    return False, 0
  elif page == npage-1:
    newstep = len(data) - page*step
  else:
    newstep = step

  for i in range(newstep):
    ctf = data[step*page+i]
    start = int(datetime.datetime(int(ctf['start'][0:4]), int(ctf['start'][5:7]), int(ctf['start'][8:10]), int(ctf['start'][11:13]), int(ctf['start'][14:16]), int(ctf['start'][17:19])).timestamp())
    end = start + (ctf['duration']['hours'] + 24*ctf['duration']['days']) *3600
    if (end - start) > 432000: #5 days
      warning = '⏰'
      warned_footer = '⏰: Event(s) dài > 5 ngày'
    else:
      warning = ''
    name = ""
    if ctf['format'] == 'Attack-Defense':
      name += '⚔ '
    elif ctf['format'] == 'Hack quest':
      name += '🌄 '
    ctf_fields.append(name + ctf['title'])
    ctf_fieldsinfo.append(ctf['ctftime_url']+'\nStart: <t:{0}:t> <t:{0}:d>\nEnd: <t:{1}:t> <t:{1}:d>'.format(str(start),str(end))+warning)

  warned_footer += '\nPage {}/{}'.format(page+1,npage)
  embedVar = utils.create_embed(title='Upcoming CTFs', fields=ctf_fields, values=ctf_fieldsinfo, footer = warned_footer, color = 0xd50000)
  return embedVar, npage


def getOngoCTF(limit_EventDuration=True):
  now = int(datetime.datetime.now().timestamp())
  data = utils.getjson('https://ctftime.org/api/v1/events/?limit=1000&start={}&finish={}/'.format(now-1000000,now+1000000))

  if data == 404:
    return False

  ctf_fields = []
  ctf_fieldsinfo = []
  warned_footer = None

  for ctf in data:
    start = int(datetime.datetime(int(ctf['start'][0:4]), int(ctf['start'][5:7]), int(ctf['start'][8:10]), int(ctf['start'][11:13]), int(ctf['start'][14:16]), int(ctf['start'][17:19])).timestamp())
    end = start + (ctf['duration']['hours'] + 24*ctf['duration']['days']) *3600
    if start < now and now < end:
      if (end - start) > 432000: #5 days
        if limit_EventDuration:
          continue
        else:
          warning = '⏰'
          warned_footer = '⏰: Event(s) dài > 5 ngày không được tính rating trên Ctftime'
      else:
        warning = ''
      name = ""
      if ctf['format'] == 'Attack-Defense':
        name += '⚔ '
      elif ctf['format'] == 'Hack quest':
        name += '🌄 '
      ctf_fields.append(name + ctf['title'])
      ctf_fieldsinfo.append(ctf['ctftime_url']+'\nStart: <t:{0}:t> <t:{0}:d>\nEnd: <t:{1}:t> <t:{1}:d>'.format(str(start),str(end))+warning)

  if ctf_fields == []:
    title = 'No results found.'
  else:
    title = 'Ongoing CTFs'
  embedVar = utils.create_embed(title=title, fields=ctf_fields, values=ctf_fieldsinfo, footer = warned_footer, color = 0xd50000)
  return embedVar



def getListCTF(order, page, step):
  try:
    with open('ctf.json', 'r') as db:
      data = json.load(db)
    data.pop("0")
    index = sorted(map(int,data.keys()))
    if order == 'Mới nhất':
      index = index[::-1]
    if step<1 or page<0 or len(data)<1:
      raise Exception("No data")
  except:
    return False, 0

  ctf_fields = []
  ctf_fieldsinfo = []
  
  npage = ceil(len(data)/step)

  if page >= npage:
    return False, 0
  elif page == npage-1:
    newstep = len(data) - page*step
  else:
    newstep = step

  for i in range(newstep):
    ctf = data[str(index[step*page+i])]
    if ctf['ctftimeid'] > 0:
      ctf_fieldsinfo.append("`CTFTime ID: " + str(ctf['ctftimeid']) +'`')
      emoji = '🚩 '
    else:
      ctf_fieldsinfo.append("`Cate ID: " + str(ctf['cate']) +'`')
      emoji = '⭐ '
    ctf_fields.append(emoji + ctf['name'])

  footer = 'Page {}/{}'.format(page+1,npage)
  embedVar = utils.create_embed(title='CTF List', fields=ctf_fields, values=ctf_fieldsinfo, footer=footer, color = 0xd50000)
  return embedVar, npage