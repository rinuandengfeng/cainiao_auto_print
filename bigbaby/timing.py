import schedule
import time



def cainiao_start(cainiao_obj):
    schedule.every(30).minutes.do(cainiao_obj.cainiao_login)

    schedule.every().day.at("09:45").do(cainiao_obj.start, "10:00:00", 10, 200, "大秒杀")
    schedule.every().day.at("09:50").do(cainiao_obj.start, "10:00:00", 3, 9, "大秒杀")
    schedule.every().day.at("10:00").do(cainiao_obj.start, "10:00:00", 1, 2, "散单-前置")


    schedule.every().day.at("17:50").do(cainiao_obj.start, "18:02:00", 10, 200, "大秒杀")
    schedule.every().day.at("17:55").do(cainiao_obj.start, "18:02:00", 3, 9, "大秒杀")
    schedule.every().day.at("18:00").do(cainiao_obj.start, "18:02:00", 1, 2, "散单-前置")

    while True:
        schedule.run_pending()
        time.sleep(10)


