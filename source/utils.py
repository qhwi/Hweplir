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

def help(command: str):
  title = ''
  desc = ''
  note = ''
  parameter = ''

  if command == 'info_find':
    title = '🔎 /ct-info_find (*search-key*)'
    desc = 'Tra cứu thông tin một giải CTF bất kì trên CTFTime'
    parameter = '**- `search-key`** (str): CTFtime ID hoặc tên của một CTF chưa diễn ra cần tìm'
  elif command == 'info_ongo':
    title = '🔎 /ct-info_ongo'
    desc = 'Xem tóm tắt thông tin các giải CTF **đang** diễn ra trên CTFTime'
  elif command == 'info_ongo':
    title = '🔎 /ct-info_upco (*page = 1*, *step = 3*)'
    desc = 'Xem tóm tắt thông tin các giải CTF **sắp** diễn ra trên CTFTime'
    note = ''
    parameter = '**- `page`** (Optional[int]): Chuyển số trang\n**- `step`** (Optional[int]): Tuỳ chỉnh số kết quả hiện trên mỗi trang'
  elif command == 'reg':
    title = '🚩 /ct-reg (*ctftime-id*)'
    desc = 'Tạo category thảo luận cho một giải CTF mới trên CTFTime'
    note = 'Category thảo luận sẽ bị ẩn sau 2 tuần từ khi kết thúc CTF'
    parameter = '**- `ctftime-id`** (int): ID giải CTF trên CTFTime\nVD: `https://ctftime.org/event/1000` -> `ctftime-id = 1000`'
  elif command == 'regacc':
    title = '🚩 /ct-regacc (*username*, *password*, *cate_id*)'
    desc = 'Update thông tin tài khoản CTF đã tạo, để chia sẻ account cho mọi người cùng tham gia'
    parameter = '**- `username`** (str): Tên đăng nhập của account đã tạo\n**- `password`** (str): Mật khẩu của account đã tạo\n**- `cate_id`** (Optional[int]): ID của Category thảo luận của giải CTF tương ứng trong Server [Hoặc bỏ qua nếu đang gọi command trong đúng Category đó]'
  elif command == 'list':
    title = '📃 /c-list (*order = "Mới nhất"*, *page = 1*, *step = 5*)'
    desc = 'List tất cả các giải CTF đã tạo trong Server'
    parameter = '**- `order`**: Thứ tự xếp list - "Mới nhất" (default) hoặc "Cũ nhất\n**- `page`** (Optional[int]): Chuyển số trang\n**- `step`** (Optional[int]): Tuỳ chỉnh số kết quả hiện trên mỗi trang'
  elif command == 'view':
    title = '👁 /c-view (*ctf-name*)'
    desc = 'Toggle ẩn/hiện Category thảo luận của một giải CTF trong Server'
    note = 'Để xem danh sách các giải trong Server, hãy dùng `/c-list`'
    parameter = '**- `ctf-name`** (discord.Role): Chọn role CTF cần thêm (VD: "<BKCTF 2023>")'
  elif command == 'admin-reg_special':
    title = '🚩 /admin-reg_special (*name*, *hide_after*)'
    desc = 'Tạo Category thảo luận thủ công cho một giải CTF (không trên CTFTime)'
    note = 'Category thảo luận sẽ bị ẩn `hide_after` ngày từ khi tạo.\n🔒 ADMIN ONLY'
    parameter = '**- `name`** (str): Tên của giải CTF muốn tạo\n**- `hide_after`** (int): Số ngày trước khi auto ẩn category'
  elif command == 'admin-delete':
    title = '❌ /admin-delete (*search_id*)'
    desc = 'Xoá một giải CTF đã tạo trong server'
    note = 'Có thể xoá tất cả dữ liệu, hoặc chỉ xoá Role và dữ liệu trong `ctf.json` nhưng giữ lại Category thảo luận.'
    parameter = '**- `search_id`** (str): CTFTime ID hoặc ID của Category thảo luận'
    note = '🔒 ADMIN ONLY'
  elif command == 'admin-add':
    title = '➕ /admin-add (*cate_id*)'
    desc = 'Thêm vào List `ctf.json` (và tạo Role xem) cho category thảo luận của một giải CTF bất kì'
    parameter = '**- `cate_id`** (Optional[int]): ID của Category thảo luận của giải CTF tương ứng trong Server [Hoặc bỏ qua nếu đang gọi command trong đúng Category đó]'
    note = '🔒 ADMIN ONLY'
  elif command == 'admin-hide':
    title = '👁 /admin-hide'
    desc = 'Ẩn Category thảo luận của các CTF cũ ngay lập tức [*autorun cùng `/reg`*]'
    note = '🔒 ADMIN ONLY'
  else:
    title = False

  if title:
    fields=[]
    values=[]
    if parameter != '':
      fields.append("Parameter(s)")
      values.append(parameter)
    embedVar = create_embed(title=title, description=desc, fields=fields, values=values, footer='❗'+note)
  else:
    embedVar = create_embed(title='Error', description='Không thấy j hết...', color = 0x000000)

  return embedVar
