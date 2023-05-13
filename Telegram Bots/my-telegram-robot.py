import schedule, requests, time 
text= ''' .من ربات مِلانی ام و تقریبا هر روز در گیت هابم پروژه های مفیدی میزارم
https://github.com/Melanee-Melanee?tab=repositories
'''

# LINK_1_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/getUpdates
#https://core.telegram.org/bots/api
# LINK_2_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text="ENTER YOUR TEXT"

# LINK_2_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text="ENTER YOUR TEXT"

def bot():
    requests.get(f""" https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text={text}"""")


schedule.every(1).days.do(bot)
while 1:
    time.sleep(1)
    schedule.run_pending( )
    
