import discord
from discord.ext import commands
from discord import app_commands
import os, json, logging
from time import time
from typing import Literal, Optional

import utils, ctftime, Buttons

### Need .env with SERVER_ID and TOKEN
SERVER_ID = discord.Object(id=os.getenv("SERVER_ID"))
BOT_TOKEN = os.getenv("TOKEN")
VIEW_ALL_CTF_ROLEID = None ### Need A <<<VIEW_ALL_CTF>>> ROLE ID and ASSIGN that role to bot
LOG_CHANNELID = None ###Need LOG CHANNEL ID if want to enable logging

class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=SERVER_ID)
        await self.tree.sync(guild=SERVER_ID)

intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(intents=intents)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

Error_embed = utils.create_embed(title='Error', description='Không thấy j hết...', color = 0x000000)

### WHEN JOIN
@bot.event
async def on_ready():
    print("{0.user} is running!".format(bot))
    if LOG_CHANNELID: 
        log = bot.get_channel(LOG_CHANNELID)
        await log.send("BOT RESTARTED")


### SLASH commands tree
@bot.tree.command()
async def help(ctx: discord.Interaction):
    """Hiển thị list các command của mình"""
    embedVar = utils.create_embed(
        title="Commands List",
#        description="/help [tên command] để biết thêm chi tiết",
        fields=['🚩 CTFTime /ct', '✨ Chung /c', '🔒 Admin'],
        values=['`info_find` | `info_upco` | `info_ongo` | `reg` | `regacc`', '`list` | `view`', '`add` | `delete` | `hide` | `reg-special`'],
        footer='Suggest/Report lỗi liên hệ Hwi#9932')
    await ctx.response.send_message(embed=embedVar, ephemeral=True)

@bot.tree.command(name="ct-info_find")
@app_commands.rename(searchkey='search-key')
@app_commands.describe(
    searchkey='Nhập CTFtime ID / hoặc string tên CTF (chưa diễn ra) cần tìm kiếm')
async def find(ctx: discord.Interaction, searchkey: str):
    """[CTFTime] Tìm thông tin giải CTF"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
#CONVERT searchkey -> ctftime_id
    if searchkey.isnumeric():
        ctftime_id = int(searchkey)
    else:
        ctftime_id = ctftime.findCTF(searchkey)

#GET info
    embedVar = ctftime.getCTF(ctftime_id)
    if embedVar:
        await ctx.edit_original_response(embed=embedVar)
    else:
        await ctx.edit_original_response(embed=Error_embed)


@bot.tree.command(name="ct-info_ongo")
async def ongo(ctx: discord.Interaction):
    """[CTFTime] Xem các CTF đang diễn ra"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
    embedVar = ctftime.getOngoCTF(limit_EventDuration=True)
    if embedVar:
        await ctx.edit_original_response(embed=embedVar,view=Buttons.ShowOngoAll())
    else:
        await ctx.edit_original_response(embed=Error_embed)

@bot.tree.command(name="ct-info_upco")
@app_commands.describe(
    page='Số trang',
    step='Chỉnh số kết quả hiện trên 1 trang')
async def upco(ctx: discord.Interaction,page: int = 1, step: int = 3):
    """[CTFTime] Xem các CTF sắp diễn ra"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
    embedVar, npage = ctftime.getUpcoCTF(page=page-1,step=step)
    if embedVar:
        await ctx.edit_original_response(embed=embedVar,view=Buttons.ShowUpcoPages(page=page-1, step=step, npage=npage))
    else:
        await ctx.edit_original_response(embed=Error_embed)

@bot.tree.command(name="ct-reg")
@app_commands.describe(
    ctfid='ID giải CTF trên CTFtime')
@app_commands.rename(ctfid='ctftime-id')
async def reg(ctx: discord.Interaction, ctfid: int):
    """[CTFTime] Đăng kí giải CTF mới cho server"""
    with open('ctf.json', 'r') as db:
        ctf_data = json.load(db)

    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))

#CHECK if already registered/valid
    reg = True
    for ctf in ctf_data:
        if ctf != "0":
            if ctf_data[ctf]['ctftimeid'] == ctfid:
                await ctx.edit_original_response(embed=utils.create_embed(title='Oops...', description='CTF này đã được tạo.', color = 0xFEE12B))
                reg = False
                break

#CREATE
    if reg:
        name, endtime, embedVar = ctftime.getCTF(ctfid, creating=True)
        if embedVar != False:
            #Create role
            allctf_role = ctx.guild.get_role(VIEW_ALL_CTF_ROLEID)
            name = name.strip()
            role = await ctx.guild.create_role(name="<"+name+">", mentionable=True)
            await role.edit(position=1)

            #Create category + set perms
            cate = await ctx.guild.create_category(name=name)
            await cate.set_permissions(role, read_messages=True)
            await cate.set_permissions(allctf_role, read_messages=True)

            #Send information
            general = await cate.create_text_channel(name=name)
            try:
                msg = await general.send(embed=embedVar)
                await msg.pin()
            except discord.errors.Forbidden:
                await ctx.edit_original_response(embed=utils.create_embed(title='Oops...', description='Error: Please make sure I have view permission.', color = 0xFEE12B))

#WRITE data
            ctf_data['0']['infom'] += 1
            ctf_data[ctf_data['0']['infom']] = {'ctftimeid': ctfid, 'role': role.id, 'cate': cate.id, 'name': name, 'infom': msg.id, 'channel': general.id, 'endtime': endtime, 'archived': False}
            with open('ctf.json', 'w') as db:
                json.dump(ctf_data, db)

            #Create remaining channels
            await cate.create_text_channel(name="web")
            await cate.create_text_channel(name="crypto")
            await cate.create_text_channel(name="pwn-rev")

            await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='Đã tạo channel cho <***'+name+'***>', color = 0x03AC13))
            # LOG
            if LOG_CHANNELID: 
                log = bot.get_channel(LOG_CHANNELID)
                await log.send("{} has created <***{}***>".format(ctx.user.name + '#' + ctx.user.discriminator, name))
        else:
            await ctx.edit_original_response(embed=Error_embed)

#Auto HIDE old CTF
    update = False
    for ctf in ctf_data:
        if ctf_data[ctf]['archived'] == False:
            if ctf_data[ctf]['endtime'] < int(time()):
                cate = discord.utils.get(ctx.guild.categories, id=ctf_data[ctf]['cate'])
                await cate.set_permissions(ctx.guild.default_role, read_messages=False)
                ctf_data[ctf]['archived'] = True
                update = True
    if update:
        with open('ctf.json', 'w') as db:
            json.dump(ctf_data, db)
        # LOG
        if LOG_CHANNELID: 
            log = bot.get_channel(LOG_CHANNELID)
            await log.send("`reg` - Auto hiding some CTFs")


@bot.tree.command(name="ct-regacc")
@app_commands.describe(
    cate_id='Nhập Discord Category ID của giải CTF trong server [Hoặc chỉ cần chạy trong channel thuộc CTF đó]',
    username='Tên đăng nhập của account đã tạo',
    password='Mật khẩu của account đã tạo')
async def regacc(ctx: discord.Interaction, username: str, password: str, cate_id: str = "0"):
    """[CTFTime] Update thông tin tài khoản của CTF đã tạo"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
    
#GET category ID
    if cate_id == "0":
        cate_id = ctx.channel.category.id
    else:
        try:
            cate_id = int(cate_id)
        except:
            cate_id = -1

#GET CTF data
    try:
        with open('ctf.json', 'r') as db:
            ctf_data = json.load(db)
        target = None
        for ctf in ctf_data:
            if ctf_data[ctf]['ctftimeid'] != 0 and ctf_data[ctf]['cate'] == cate_id:
                target = ctf_data[ctf]
                break
        if target == None:
            raise Exception("Nothing found")

#RESEND info 
        name, endtime, embedVar = ctftime.getCTF(target['ctftimeid'], creating=True, username=username, password=password)
        if not embedVar:
            raise Exception("404")
        channel = bot.get_channel(target['channel'])
        msg = await channel.fetch_message(target['infom'])
        await msg.edit(embed=embedVar)
        await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='Login info của <***'+target['name']+'***> đã được update', color = 0x03AC13))
        # LOG
        if LOG_CHANNELID: 
            log = bot.get_channel(LOG_CHANNELID)
            await log.send("{} has updated login info for <***{}***>".format(ctx.user.name + '#' + ctx.user.discriminator, target['name']))
    except:
        await ctx.edit_original_response(embed=Error_embed)
            

@bot.tree.command(name="c-list")
@app_commands.describe(
    order='Thứ tự list',
    page='Số trang',
    step='Chỉnh số kết quả hiện trên 1 trang')
async def list(ctx: discord.Interaction, order: Literal['Cũ nhất', 'Mới nhất'] = 'Mới nhất', page: int = 1, step: int = 5):
    """List tất cả các giải CTF trong server"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
    embedVar, npage = ctftime.getListCTF(order=order, page=page-1, step=step)
    if embedVar:
        await ctx.edit_original_response(embed=embedVar,view=Buttons.ListPages(order=order, page=page-1, step=step, npage=npage))
    else:
        await ctx.edit_original_response(embed=Error_embed)


@bot.tree.command(name="c-view")
@app_commands.describe(
    role='Nhập role CTF cần thêm (có dạng "<Tên CTF>")')
@app_commands.rename(role='ctf-name')
async def toggle(ctx: discord.Interaction, role: discord.Role):
    """Toggle ẩn/hiện channel thảo luận của một giải CTF trong server"""
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B),ephemeral=True)
    if role.name.startswith("<"):
        if role in ctx.user.roles:
            await ctx.user.remove_roles(role)
            await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='Đã ẩn ***'+role.name+'*** cho bạn!', color = 0x03AC13))
        else:
            await ctx.user.add_roles(role)
            await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='Đã hiện ***'+role.name+'*** cho bạn!', color = 0x03AC13))
    else:
        await ctx.edit_original_response(embed=utils.create_embed(title='Oops...', description="Role không hợp lệ", color = 0xFEE12B))


@bot.tree.command(name="admin-hide")
async def hidectf(ctx: discord.Interaction):
    """Ẩn các CTF cũ ngay lập tức [autorun cùng /reg]"""
    await ctx.response.send_message(content="Hiding old CTF... Please wait", ephemeral=True)
    with open('ctf.json', 'r') as db:
        ctf_data = json.load(db)
    update = False
    for ctf in ctf_data:
        if ctf_data[ctf]['archived'] == False:
            if ctf_data[ctf]['endtime'] < int(time()):
                cate = discord.utils.get(ctx.guild.categories, id=ctf_data[ctf]['cate'])
                await cate.set_permissions(ctx.guild.default_role, read_messages=False)
                ctf_data[ctf]['archived'] = True
                update = True
    if update:
        with open('ctf.json', 'w') as db:
            json.dump(ctf_data, db)
        # LOG
        if LOG_CHANNELID: 
            log = bot.get_channel(LOG_CHANNELID)
            await log.send("{} has manually hide some CTFs".format(ctx.user.name + '#' + ctx.user.discriminator))
        

@bot.tree.command(name="admin-reg_special")
@app_commands.describe(
    name='Tên của giải CTF muốn tạo',
    day='Số ngày hiện kênh trước khi auto ẩn')
@app_commands.rename(day='hide_after')
async def regspecial(ctx: discord.Interaction, name: str, day: int):
    """Đăng kí giải CTF thủ công (không trên CTFTime) cho server"""
    with open('ctf.json', 'r') as db:
        ctf_data = json.load(db)
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))
    
#CREATE
    #Create role
    allctf_role = ctx.guild.get_role(VIEW_ALL_CTF_ROLEID)
    name = name.strip()
    role = await ctx.guild.create_role(name="<"+name+">", mentionable=True)
    await role.edit(position=1)
    #Create category
    cate = await ctx.guild.create_category(name=name)
    await cate.set_permissions(role, read_messages=True)
    await cate.set_permissions(allctf_role, read_messages=True)
#WRITE data
    ctf_data['0']['infom'] += 1
    ctf_data[ctf_data['0']['infom']] = {'ctftimeid': 0, 'role': role.id, 'cate': cate.id, 'name': name, 'infom': 0, 'channel': 0, 'endtime': int(time())+86400*day, 'archived': False}
    with open('ctf.json', 'w') as db:
        json.dump(ctf_data, db)
    #Create channels
    general = await cate.create_text_channel(name=name)
    await cate.create_text_channel(name="web")
    await cate.create_text_channel(name="crypto")
    await cate.create_text_channel(name="pwn-rev")

    await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='Đã tạo channel cho <***{}***>\nVui lòng tự cung cấp info giải CTF vào <#{}>'.format(name, general.id), color = 0x03AC13))
    # LOG
    if LOG_CHANNELID: 
        log = bot.get_channel(LOG_CHANNELID)
        await log.send("{} has manually created <***{}***>".format(ctx.user.name + '#' + ctx.user.discriminator, name))
    
#Auto HIDE old CTF
    update = False
    for ctf in ctf_data:
        if ctf_data[ctf]['archived'] == False:
            if ctf_data[ctf]['endtime'] < int(time()):
                cate = discord.utils.get(ctx.guild.categories, id=ctf_data[ctf]['cate'])
                await cate.set_permissions(ctx.guild.default_role, read_messages=False)
                ctf_data[ctf]['archived'] = True
                update = True
    if update:
        with open('ctf.json', 'w') as db:
            json.dump(ctf_data, db)
        # LOG
        if LOG_CHANNELID: 
            log = bot.get_channel(LOG_CHANNELID)
            await log.send("`reg-special` - Auto hiding some CTFs")


@bot.tree.command(name="admin-delete")
@app_commands.describe(
    search_id='Nhập CTFTime ID, hoặc Discord Category ID')
async def delete(ctx: discord.Interaction, search_id: str):
    """Xoá một giải CTF đã tạo trong server"""
    with open('ctf.json', 'r') as db:
        ctf_data = json.load(db)
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B),ephemeral=True)

#FIND CTF data
    target = None
    for ctf in ctf_data:
        if ctf != "0":
            if ctf_data[ctf]['ctftimeid'] == int(search_id) or str(ctf_data[ctf]['cate']) == search_id:
                target = ctf_data.pop(ctf)
                break
    if target == None:
        await ctx.edit_original_response(embed=Error_embed)
    else:
#CONFIRM
        view = Buttons.Delete(name=target['name'])
        await ctx.edit_original_response(embed=utils.create_embed(title='Xác nhận xoá', description='Bạn muốn xoá tất cả dữ liệu của <***'+target['name']+'***> hay vẫn giữ lại các kênh thảo luận?', color = 0xFEE12B), view=view)
        await view.wait()
        if view.option == 'Cancel':
            pass
        else:
#DELETE
            await ctx.guild.get_role(target['role']).delete()
            cate = discord.utils.get(ctx.guild.categories, id=target['cate'])
            await cate.set_permissions(ctx.guild.default_role, read_messages=True)
            if view.option == True:
                for channel in cate.channels:
                    try:
                        await channel.delete()
                    except AttributeError:
                        pass
                await cate.delete()
            # LOG
            if LOG_CHANNELID: 
                log = bot.get_channel(LOG_CHANNELID)
                await log.send("{} has deleted <***{}***>".format(ctx.user.name + '#' + ctx.user.discriminator, target['name']))
            else:
                await cate.edit(name="[UNLISTED] " + cate.name)
                # LOG
                if LOG_CHANNELID: 
                    log = bot.get_channel(LOG_CHANNELID)
                    await log.send("{} has unlinked <***{}***> from the database".format(ctx.user.name + '#' + ctx.user.discriminator, target['name']))
            with open('ctf.json', 'w') as db:
                json.dump(ctf_data, db)



@bot.tree.command(name="admin-add")
@app_commands.describe(
    cate_id='Nhập Discord Category ID của giải CTF trong server [Hoặc chỉ cần chạy trong channel thuộc CTF đó]')
async def addctf(ctx: discord.Interaction, cate_id: str = "0"):
    """Thêm vào List một giải CTF cũ"""
       
    with open('ctf.json', 'r') as db:
        ctf_data = json.load(db)
    await ctx.response.send_message(embed=utils.create_embed(title='Đợi chút...', color = 0xFEE12B))

#GET category ID
    if cate_id == "0":
        cate_id = ctx.channel.category.id
    else:
        try:
            cate_id = int(cate_id)
        except:
            cate_id = -1
#CHECK if existed
    reg = True
    for ctf in ctf_data:
        if ctf != "0":
            if ctf_data[ctf]['cate'] == cate_id:
                await ctx.edit_original_response(embed=utils.create_embed(title='Oops...', description='CTF này đã có trong list.', color = 0xFEE12B))
                reg = False
                break
    if reg:
        try:
#CREATE
            #Get category
            cate = discord.utils.get(ctx.guild.categories, id=cate_id)
            if cate.name.startswith("[UNLISTED]"):
                await cate.edit(name=cate.name.replace("[UNLISTED]",""))
            await cate.edit(name=cate.name.strip())
            #Create role
            allctf_role = ctx.guild.get_role(VIEW_ALL_CTF_ROLEID)
            role = await ctx.guild.create_role(name="<"+cate.name+">")
            await role.edit(position=1)
            #Set perms
            await cate.set_permissions(role, read_messages=True)
            await cate.set_permissions(allctf_role, read_messages=True)
            await cate.set_permissions(ctx.guild.default_role, read_messages=False)
            for channel in cate.channels:
                await channel.edit(sync_permissions=True)
        except:
            ctx.edit_original_response(embed=Error_embed)
        else:
            await ctx.edit_original_response(embed=utils.create_embed(title='Xong!', description='<***'+cate.name+'***> đã thêm vào list', color = 0x03AC13))

#WRITE data
        ctf_data['0']['infom'] += 1
        ctf_data[ctf_data['0']['infom']] = {'ctftimeid': 0, 'role': role.id, 'cate': cate_id, 'name': cate.name, 'infom': 0, 'channel': 0, 'endtime': 0, 'archived': True}
        with open('ctf.json', 'w') as db:
            json.dump(ctf_data, db)
        # LOG
        if LOG_CHANNELID: 
            log = bot.get_channel(LOG_CHANNELID)
            await log.send("{} has manually listed <***{}***>".format(ctx.user.name + '#' + ctx.user.discriminator, cate.name))



bot.run(BOT_TOKEN, log_handler=handler, log_level=logging.INFO)
