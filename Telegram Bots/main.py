###############          ##########        #######   #######        #########      #######       #
#              #        #          #             #         #       #         #           #
#               #       #          #            #         #        #         #          #        #
#              #        #          #           #         #         #         #         #         #
###############         ############          #         #          ###########        #          #
#              #        #          #         #         #           #         #       #           #
#               #       #          #        #         #            #         #      #            #
#              #        #          #       #         #             #         #     #             #
###############         #          #      #######    #######       #         #    #######        #

# Developer: Mohammad Ali Bazzazi (me)

# MY YOUTUBE CHANNEL: https://youtube.com/c/MohammadAliBazzazi

########################### START ###########################

# WRITE "pip install schedule" IN TERMINAL AND THEN...
import schedule, requests, time

def bot():
    # 1) Create Telegram Group or Channel
    # 2) Create Telegram bot
    # 3) Add bot to Group or Channel
    # 4) Create Link 1
    # LINK_1_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/getUpdates
    # 5) Get chat id
    # 6) Create Link 2
    # LINK_2_FORMAT => https://api.telegram.org/bot<ENTER_BOT_TOKEN>/sendMessage?chat_id=<ENTER_CHAT_ID>&text="ENTER YOUR TEXT"
    
    requests.get("""ENTER LINK 2""")

schedule.every(5).seconds.do(bot)
while 1:
    time.sleep(1)
    schedule.run_pending()
    
########################### END ###########################
