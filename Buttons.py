import discord
import ctftime, utils

class ShowOngoAll(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Xem tất cả",style=discord.ButtonStyle.gray,emoji='👁')
    async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(embed=ctftime.getOngoCTF(limit_EventDuration=False), view=HideOngo())

class HideOngo(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Ẩn CTF >5 ngày",style=discord.ButtonStyle.gray,emoji='❌')
    async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(embed=ctftime.getOngoCTF(limit_EventDuration=True), view=ShowOngoAll())

class ShowUpcoPages(discord.ui.View):
    current_page : int = 0
    step : int = 3
    npage : int = 1
    
    def __init__(self, *, step, page, npage, timeout=180):
        super().__init__(timeout=timeout)
        self.step = step
        self.current_page = page
        self.npage = npage
        self.update_buttons()

    def update_buttons(self):
        if self.current_page == 0:
            self.prev_button.disabled = True
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.prev_button.disabled = False
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == self.npage-1:
            self.next_button.disabled = True
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        embedVar, self.npage = ctftime.getUpcoCTF(self.current_page,step=self.step)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        embedVar, self.npage = ctftime.getUpcoCTF(self.current_page,step=self.step)
        await interaction.response.edit_message(embed=embedVar, view=self)

class Delete(discord.ui.View):
    def __init__(self, *,name='CTF', timeout=180):
        super().__init__(timeout=timeout)
        self.option =  'Cancel'
        self.name = name

    @discord.ui.button(label="Xoá tất cả", style=discord.ButtonStyle.primary)
    async def yes(self, interaction:discord.Interaction, button: discord.ui.Button):
        embedVar = utils.create_embed(title='Xong!', description='Toàn bộ dữ liệu của <***'+self.name+'***> đã bị xoá', color = 0xd50000)
        button.style=discord.ButtonStyle.red
        button.emoji='⛔'
        button.disabled=True
        self.cancel.disabled = True
        self.no.style=discord.ButtonStyle.gray
        self.no.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(embed=embedVar)
        self.option = True
        self.stop()

    @discord.ui.button(label="Giữ lại channel", style=discord.ButtonStyle.primary)
    async def no(self, interaction:discord.Interaction, button: discord.ui.Button):
        embedVar = utils.create_embed(title='Xong!', description='<***'+self.name+'***> đã bị bỏ khỏi list', color = 0xd50000)
        button.style=discord.ButtonStyle.red
        button.emoji='⭕'
        button.disabled=True
        self.cancel.disabled = True
        self.yes.style=discord.ButtonStyle.gray
        self.yes.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(embed=embedVar)
        self.option = False
        self.stop()

    @discord.ui.button(label="Huỷ", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction:discord.Interaction, button: discord.ui.Button):
        embedVar = utils.create_embed(title='Đã huỷ', color=0x000000)
        await interaction.response.edit_message(embed=embedVar, view=None)
        self.stop()

class ListPages(discord.ui.View):
    current_page : int = 0
    step : int = 3
    npage : int = 1
    order : str = 'Mới nhất'
    
    def __init__(self, *, order, step, page, npage, timeout=180):
        super().__init__(timeout=timeout)
        self.step = step
        self.current_page = page
        self.npage = npage
        self.order = order
        self.update_buttons()

    def update_buttons(self):
        if self.current_page == 0:
            self.prev_button.disabled = True
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.prev_button.disabled = False
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == self.npage-1:
            self.next_button.disabled = True
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        embedVar, self.npage = ctftime.getListCTF(order=self.order, page=self.current_page, step=self.step)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        embedVar, self.npage = ctftime.getListCTF(order=self.order, page=self.current_page, step=self.step)
        await interaction.response.edit_message(embed=embedVar, view=self)