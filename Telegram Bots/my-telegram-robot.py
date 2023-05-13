import schedule, requests, time 
text= ''' .من ربات مِلانی ام و تقریبا هر روز در گیت هابم پروژه های مفیدی میزارم
https://github.com/Melanee-Melanee?tab=repositories
'''



# LINK_1_FORMAT => https://api.telegram.org/bot6111278708:AAFObxPfCkCQ7DXUdgI1Qj43weN_cP6Z1uc/getUpdates


#chat_id= '-1001643606984'
#https://core.telegram.org/bots/api

 # LINK_2_FORMAT => https://api.telegram.org/bot6111278708:AAFObxPfCkCQ7DXUdgI1Qj43weN_cP6Z1uc/sendMessage?chat_id=-1001643606984&text="ENTER YOUR TEXT"

API ='6111278708:AAFObxPfCkCQ7DXUdgI1Qj43weN_cP6Z1uc'



def bot():
    requests.get(f"""https://api.telegram.org/bot6111278708:AAFObxPfCkCQ7DXUdgI1Qj43weN_cP6Z1uc/sendMessage?chat_id=-1001643606984&text={text}""")


schedule.every(5).seconds.do(bot)
while 1:
    time.sleep(1)
    schedule.run_pending( )
    