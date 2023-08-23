from playwright.sync_api import  sync_playwright
import datetime
from configs.logs import logger
from configs.untill import get_express_initial

class CaiNiao():
    def __init__(self, username, password, print_name, express):
        """
        username: 菜鸟账号
        password: 菜鸟密码
        """
        self.username = username
        self.password = password
        self.print_name = print_name
        self.express = express
        self.express_initial = get_express_initial(self.express)

    def get_browser_context(self, playwright, headless=False):
        
        browser = playwright.chromium.launch(headless=headless,
                                                args=['--start-maximized'], timeout=6030000)
        # 时区待设置
        context = browser.new_context(storage_state="./auth/cainiao_state.json", no_viewport=True)
        # 等待时间设置为2分钟30秒 ，防止网络不好时，抛出超时错误
        return context

    # windows7 菜鸟登陆
    def __win7_login(self, cainiao_win7_page):
        cainiao_win7_page.goto("https://auth.wms.cainiao.com/console/login?redirectURL=https://wms.cainiao.com/portal")
        cainiao_win7_page.frame(name="alibaba-login-box").click("[placeholder=\"账号名/手机号/邮箱\"]")
        cainiao_win7_page.frame(name="alibaba-login-box").fill("[placeholder=\"账号名/手机号/邮箱\"]", self.username)
        cainiao_win7_page.frame(name="alibaba-login-box").click("[placeholder=\"请输入登录密码\"]")
        cainiao_win7_page.frame(name="alibaba-login-box").fill("[placeholder=\"请输入登录密码\"]", self.password)
        cainiao_win7_page.frame(name="alibaba-login-box").click("button:has-text(\"登录\")")
        cainiao_win7_page.wait_for_timeout(120000)
        

    # 汇单
    def __wave_list(self, page, over_time, start_num, over_num, wave_type):
        page.goto("https://cwoutprod.cainiao.com/waveanalysis")
        logger.info("开始汇今天"+over_time +"的" + self.express + wave_type + str(start_num) +" - " + str(over_num) + " 单子")
        # 设置汇单时间
        self.__set_wave_time(page, over_time)
        # 设置单子的数量
        self.__set_wave_num(page, start_num, over_num)
        # 设置快递
        self.__select_express(page)
        # 设置汇单方式
        self.__set_wave_type(page, wave_type)
        logger.info("今天"+over_time +"的" + self.express + wave_type + str(start_num) +" - " + str(over_num) + "汇单完成")

    # 打印单子
    def __print_list(self, page, pick_list=False):
        page.goto("https://cwoutprod.cainiao.com/pickbill")
        # 打印面单
        self.__express_sheet_print(page)
        # 打印拣选单
        if pick_list:
            self.__print_pick_list(page)
        # 完成制单
        self.__prepared_success(page)

    def __set_wave_time(self, page, over_time):
        """
        设置汇单时间
        over_time: 汇单时设置的截止时间
        """
        nowday = datetime.datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        page.click("[placeholder=\"起始日期\"]")
        page.fill("[placeholder=\"YYYY-MM-DD\"]", yesterday)
        page.press("[placeholder=\"YYYY-MM-DD\"]", "Enter")
        # 起始时间
        page.click("[placeholder=\"HH:mm:ss\"]")
        page.fill("[placeholder=\"HH:mm:ss\"]", "18:00:00")
        # 结束时间
        page.click(":nth-match([placeholder=\"YYYY-MM-DD\"], 2)")
        page.fill(":nth-match([placeholder=\"YYYY-MM-DD\"], 2)", nowday)
        page.press(":nth-match([placeholder=\"YYYY-MM-DD\"], 2)", "Enter")
        page.fill(":nth-match([placeholder=\"HH:mm:ss\"], 2)", str(over_time))
        page.click("button:has-text(\"确定\")")

    def __set_wave_num(self, page, start_num, over_num):
        """
        设置要汇单的单子的数量
        start_num: 要汇单的单子的最小数量,start_num=1 >= 1
        over_num: 要汇单的单子的最大数量,over_num 用于将小批量和大批量分离开。over_num >= start_num
        """
        page.click("[placeholder=\"请输入\"]")
        page.fill("[placeholder=\"请输入\"]", str(start_num))
        page.click("input[name=\"maxOrderNum\"]")
        page.fill("input[name=\"maxOrderNum\"]", str(over_num))
        # 点击查询
        page.click("button:has-text(\"查询\")")

    def __set_express(self, page):
        """
        设置要汇单的快递
        express: 要汇单的快递名称
        注：要写快递的全名，如：东莞圆通
        """
        page.click("div[role=\"checkbox\"]:has-text(" + '"' + str(self.express) + '"' + ")")
        page.wait_for_timeout(7000)

    def __set_wave_type(self, page, wave_type):
        """
        设置汇单方式
        wave_type: 汇单方式 有两种：大秒杀、散单-前置
        """
        # 全部选中要汇单的单子
        page.check("input[type=\"checkbox\"]")
        # 点击汇单
        page.click("button:has-text(\"汇单\")")

        # 判断汇单类型
        if wave_type == "大秒杀":
            # 在弹出的汇单框中的汇单策略选择 大秒杀
            page.click("text=汇单策略请选择 >> i")
            page.click(":nth-match(div:has-text( " + '"' + str(wave_type) + '"' + "), 3)")
        elif wave_type == "散单-前置":
            # 在弹出的汇单框中的汇单策略选择 散单前置
            page.click("text=汇单策略请选择 >> i")
            page.click(":nth-match(div:has-text( " + '"' + wave_type + '"' + "), 3)")
            # 选中汇总汇单
            page.check("input[name=\"tailWave\"]")
            # 选中合并
            page.check("input[name=\"merge\"]")
        else:
            logger.info("汇单方式输入错误o(╥﹏╥)o...")

        # 点击确定
        page.click("button:has-text(\"确定\")")
        page.wait_for_timeout(30000)

    
    def __select_express(self,page):
        """
        在汇单页面中选择汇单的快递
        
        """
        page.click("text=快递公司请选择 >> i")

        page.click("[placeholder=\"请输入查询\"]")

        page.fill("[placeholder=\"请输入查询\"]", self.express)
        
        page.check("text="+ self.express_initial[0] + self.express +" >> input[type=\"checkbox\"]")
        
        page.click("button:has-text(\"查询\")")
        page.wait_for_timeout(7000)



    def __express_sheet_print(self, page):
        """
        将拣选制单中的面单全部打印出来
        """

        # 等待10秒防止有些汇的单子没有到拣选制单页面
        logger.info("开始打印面单...")
        page.wait_for_timeout(10000)

        self.__select_express(page)
        # 选中要打的单子
        page.check("input[type=\"checkbox\"]")
        # 打印出面单
        page.click("button:has-text(\"面单打印\")")
        # 选择打印机
        page.click("text=请选择打印机：请选择 >> i")
        page.click(":nth-match(div:has-text("+ '"' + self.print_name + '"' +"), 3)")
        # 点击确定
        page.click("button:has-text(\"确定\")")
        page.wait_for_timeout(7000)
        logger.info("面单打印完成")

    def __print_pick_list(self, page):
        """
        将大批量需要打印拣选单的单子打印出来 
        全部打出，所以需要在汇单子时，进行分类汇单
        """
        logger.info("开始打印拣选单...")

        page.click("button:has-text(\"查询\")")

        page.wait_for_timeout(5000)
        page.check("input[type=\"checkbox\"]")

        # 打印出拣选单  
        page.locator('xpath=//*[@id="root"]/div[2]/div/div[3]/div[1]/button[4]/span').click()
        page.click("text=请选择打印机：请选择 >> i")
        page.click(":nth-match(div:has-text("+ '"' + self.print_name + '"' +"), 3)")
        # 点击确定
        page.click("button:has-text(\"确定\")")
        page.wait_for_timeout(15000)
        logger.info("拣选单打印完成")

    def __prepared_success(self, page):
        """
        制单完成
        """
        page.click("button:has-text(\"查询\")")
        page.wait_for_timeout(5000)
        page.check("input[type=\"checkbox\"]")
        # 完成制单
        logger.info("完成制单")
        page.locator('xpath=//*[@id="root"]/div[2]/div/div[3]/div[1]/button[6]/span').click()
        page.wait_for_timeout(15000)

    # 登陆
    def cainiao_login(self):
        with sync_playwright() as playwright:
            logger.info("开始进行登陆...")
            context = self.get_browser_context(playwright, headless=False)
            page = context.new_page()
            self.__win7_login(page)
            context.storage_state(path="./auth/cainiao_state.json")
            logger.info("登陆完成！")

    # 批量启动函数
    def start(self, over_time: str, start_num: int, over_num: int, wave_type: str) -> None:
        """
        开始执行函数，外部调用函数
        :param over_time: 结束汇单的时间 如： “10:00:00”
        :param start_num: 汇单的最小数量，必须大于等于1 如：1
        :param over_num: 汇单的最大数量 ，必须大于等于1 如: 2
        :param wave_type: 汇单方式 如： "大秒杀"、 “散单-前置”
        :return: 空值
        """
        with sync_playwright() as playwright:
            cainiao_win7_context = self.get_browser_context(playwright, headless=False)

            # 汇单
            wave_page = cainiao_win7_context.new_page()
            self.__wave_list(wave_page, over_time, start_num, over_num, wave_type)

            # 打印面单
            
            print_page = cainiao_win7_context.new_page()
            if int(start_num) >= 10:
                self.__print_list(print_page, pick_list=True)
            else:
                self.__print_list(print_page, pick_list=False)