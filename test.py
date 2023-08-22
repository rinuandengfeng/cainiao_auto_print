from bigbaby.cainiao import CaiNiao
from configs.config import global_config

username = global_config.get("info","username")
password = global_config.get("info","password")
express = global_config.get("info","express")
print_name = global_config.get("info","print_name")
cn = CaiNiao(username,password,print_name,express)
# # # cn.start("18:00:00",1,2,"散单-前置")
cn.test()
# cn.cainiao_login()

# from playwright.sync_api import  sync_playwright
# import time

# with sync_playwright()  as playwright:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="./auth/cainiao_state.json")
#     page = context.new_page()
#     page.goto("https://cnlogin.cainiao.com/wmsLogin?isNewLogin=true&hideReg=true&hiddenMobile=true&showreg=false&noPwdReset=true&type=WMS&sec=PoLtb0bWFd15mk9n3otAI2q3HV3X5rBxHxsaw3fgpLmvWma2HLQvWacCkkFHHvjfSFdWJgMsTYV3t9e_FBZM5k6TpgZidc0TfFLDxo9B9POi4DwWS9psXbJ04BgMl2nty6oLYfRSYD3vX0G8YRncHQluoqi-LRmWOyQ85lQ3oQk&title=菜鸟WMS登录&hideForgetAccount=false&lang=zh_cn&redirect_url=https://auth.wms.cainiao.com/portal")
#     print("点击输入账号")
#     page.locator('[placeholder="账号名/手机号/邮箱"]').click()
#     print("输入账号")
#     page.locator('[placeholder="账号名/手机号/邮箱"]').fill("GXW7351")
#     print("点击输入密码")
#     page.locator("[placeholder=\"请输入登录密码\"]").click()
#     print("输入密码")
#     page.locator("[placeholder=\"请输入登录密码\"]").fill("GXW7351")
#     page.locator("button",name="登录").click()
#     time.sleep(10)


