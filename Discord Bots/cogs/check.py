import disnake
from disnake.ext import commands
import asyncio
import sqlite3

# # create form 
class MyModal(disnake.ui.Modal):
    def __init__(self) -> None:
        self.add_role = 997142096836304896
        self.remove_role = 997143448484315247
        self.error_channel = 997858250106089632
        self.lobby_channel = 997144260501569599
        components = [
            disnake.ui.TextInput(
                label="شماره تلفن خود به انگلیسی",
                placeholder = "مثال (09111111111)",
                custom_id="phone",
                style=disnake.TextInputStyle.short,
                max_length=11,
            ),

        ]
        super().__init__(title="CS50 Discord Authentication", custom_id="create_tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        number_input = inter.text_values.get("phone")
        
        data = sqlite3_check(number_input)
        #print(data)
        Check = False

        try :
            # check the phone number in the database
            if "phone_number" in data:
                # check phone number in database equal to the phone number in the form 
                if data["phone_number"] == number_input :
                    if data["Login"] == None and data["Discord_id_name"] == None and data["Discord_id"] == None:
                        # success message
                        embed=disnake.Embed(color=0x14db4c)
                        embed.title = "اطلاعات شما تایید شد"
                        embed.description = f"""سلام , {data['First']} {data['Last']}
                        اطلاعات شما برسی و تایید شد و تا چند ثانیه دیگر سرور برای شما باز خواهد شد
                        """
                        await inter.response.send_message(embed = embed, ephemeral=True)
                        # add and remove roles
                        #  set your personal role id for add and remove 
                        Add_Role_id = inter.guild.get_role(self.add_role)
                        Remove_role_id = inter.guild.get_role(self.remove_role)
                        await asyncio.sleep(3)
                        await inter.author.add_roles(Add_Role_id)
                        await inter.author.remove_roles(Remove_role_id)
                        # connect to database
                        connect = sqlite3.connect("CS50.db")
                        db = connect.cursor()
                        db.execute(f"UPDATE account_user SET Login = 'YES', Discord_id_name = '{inter.author}', Discord_id = '{inter.author.id}' WHERE phone_number = '{number_input}'")
                        connect.commit()
                        connect.close()
                        Check = True

                    else:
                        #if if phone number is already signed up in server this message will sent for user
                        Check = True
                        embed=disnake.Embed(color=0xe00909)
                        embed.title = " از شماره مورد نظر شمااستفاده شده در صورت نیاز به پشتیبانی اطلاع دهید"
                        await inter.response.send_message(embed = embed, ephemeral=True)
            # if phone number dose not exist in database this message will be sent for user
            if not Check:
                embed=disnake.Embed(color=0xe00909)
                embed.title = "متاسفانه مشخصات شما در لیست موجود نمیباشد لطفا به پشتیبانی اطلاع دهید"
                await inter.response.send_message(embed = embed, ephemeral=True)
        except Exception as e:
            #error Log
            # set your personal channel for errors 
            channel = inter.guild.get_channel(self.error_channel)
            await channel.send(e)
    # if there is a problem in Discord api or no response from discord this message will be shown
    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message("مشکلی پیش امده لطفا بعدا تلاش کنید", ephemeral=True)

class button(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Authenticate", style=disnake.ButtonStyle.success)
    async def authenticate(self, button:disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(MyModal())


class check(commands.Cog, MyModal):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        MyModal.__init__(self)
        
    @commands.Cog.listener()
    async def on_ready(self):
        # lobby channel 
        # set your personal channel 
        channel = self.bot.get_channel(self.lobby_channel)
        # delete last 10 message from channel 
        await channel.purge(limit = 10)
        embed=disnake.Embed(color=0x14db4c)
        embed.title = "احراز هویت شرکت کنندگان"
        embed.description = "لطفا برای دسترسی به محتوای سرور روی دکمه زیر کلیک کنید"
        await channel.send(embed = embed, view=button())

def sqlite3_check(number_input):
    connect = sqlite3.connect("CS50.db")
    db = connect.cursor()
    db.execute(f"SELECT * FROM account_user WHERE phone_number = '{number_input}';")
    data = db.fetchall()
    row = {}
    for x in data:
        row = {
            "First":None, "Last":None, "phone_number":None, "Login":None, "Discord_id_name":None, "Discord_id":None,
        }
        row["First"] = x[0]
        row["Last"] = x[1]
        row["phone_number"] = x[2]
        row["Login"] = x[3]
        row["Discord_id_name"] = x[4]
        row["Discord_id"] = x[5]
    connect.close()
    return row
    
def setup(bot:commands.Bot):
    bot.add_cog(check(bot))
