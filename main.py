
from bigbaby.cainiao import CaiNiao
from bigbaby.timing import cainiao_start

from configs.config import global_config

from configs.logs import logger


def run():
    logger.info("程序启动...")
    username = global_config.get("info","username")
    password = global_config.get("info","password")
    express = global_config.get("info","express")
    print_name = global_config.get("info","print_name")
    cainiao_obj = CaiNiao(str(username), str(password), str(print_name),str(express))
    cainiao_start(cainiao_obj)
    logger.info("退出程序...")

if __name__ == "__main__":
    run()   
 