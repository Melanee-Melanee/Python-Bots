import schedule, requests, time 
text= ''' سلام من ربات مِلانی ام. اگه پست های این چنل رو دوست دارید لطفا برای بقیه فوروارد کنید.
@melaneepython
'''

# LINK_1_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/getUpdates
#https://core.telegram.org/bots/api
# LINK_2_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text="ENTER YOUR TEXT"

# LINK_2_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text="ENTER YOUR TEXT"

def bot():
    requests.get(f""" https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text={text}"""")


schedule.every(1).day.at("19:30").do(bot)
while True:
    schedule.run_pending()
    time.sleep(1)
