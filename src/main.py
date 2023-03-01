from DataProviderThread import DataProviderThread
from Exceptions.CapsuleFarmerEvolvedException import CapsuleFarmerEvolvedException
from FarmThread import FarmThread
from GuiThread import GuiThread
from threading import Lock
from Config import Config
from Logger import Logger
import logging
import sys
import argparse
from rich import print
from pathlib import Path
from time import sleep, strftime, localtime
from Restarter import Restarter
from SharedData import SharedData
import requests
from Stats import Stats
from VersionManager import VersionManager

CURRENT_VERSION = 1.44


def init() -> tuple[logging.Logger, Config]:
    parser = argparse.ArgumentParser(description='Farm Esports Capsules by watching all matches on lolesports.com.')
    parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                        help='Path to a custom config file')
    args = parser.parse_args()

    print("**********************************************************************************************")
    print(
        f"*                         Thank you for using Capsule Farmer Evolved v{str(CURRENT_VERSION)}!                  *")
    print("*                        以下为本改版的github链接(非原版),供源码和下载方式.                  *")
    print("*                   https://github.com/Yudaotor/CapsuleFarmerEvolved-dingding                *")
    print("*                        如果不能正常使用的话,本软件需要梯子 (注意不是加速器)                *")
    print("*   如出现登陆失败的情况,1.检查账密是否正确 2.删除sessions文件夹后重试 3.网络问题(梯子问题)  *")
    print("*                     关于如何使用钉钉提醒(饭碗警告软件)功能请查看以下链接                   *")
    print("*     https://blog.csdn.net/qq_33884853/article/details/129104726?spm=1001.2014.3001.5502    *")
    print(
        f"*                                     Start Time: [green]{strftime('%b %d, %H:%M', localtime())}[/]                              *")
    print("**********************************************************************************************")
    print()

    Path("./logs/").mkdir(parents=True, exist_ok=True)
    Path("./sessions/").mkdir(parents=True, exist_ok=True)
    config = Config(args.configPath)
    log = Logger.createLogger(config.debug, CURRENT_VERSION)
    if not VersionManager.isLatestVersion(CURRENT_VERSION):
        log.warning(
            "!!! 新版本可用 !!! 从github这下载: https://github.com/Yudaotor/CapsuleFarmerEvolved-dingding/releases/latest")
        print(
            "[bold red]!!! 新版本可用 !!!\n从github这下载: https://github.com/Yudaotor/CapsuleFarmerEvolved-dingding/releases"
            "/latest\n")

    return log, config


def main(log: logging.Logger, config: Config):
    farmThreads = {}
    refreshLock = Lock()
    locks = {"refreshLock": refreshLock}

    sharedData = SharedData()
    stats = Stats()

    for account in config.accounts:
        stats.initNewAccount(account)

    restarter = Restarter(stats)

    log.info(f"Starting a GUI thread.")
    guiThread = GuiThread(log, config, stats, locks)
    guiThread.daemon = True
    guiThread.start()

    dataProviderThread = DataProviderThread(log, config, sharedData)
    dataProviderThread.daemon = True
    dataProviderThread.start()

    while True:
        for account in config.accounts:
            if account not in farmThreads and restarter.canRestart(account) and stats.getThreadStatus(account):
                log.info(f"Starting a thread for {account}.")
                thread = FarmThread(log, config, account, stats, locks, sharedData)
                thread.daemon = True
                thread.start()
                farmThreads[account] = thread
                log.info(f"Thread for {account} was created.")

            if account in farmThreads and not stats.getThreadStatus(account):
                del farmThreads[account]

        toDelete = []

        for account in farmThreads:
            if not farmThreads[account].is_alive():
                toDelete.append(account)
                log.warning(f"Thread {account} has finished.")
                restarter.setRestartDelay(account)
                stats.updateStatus(account,
                                   f"[red]错误:将在 {restarter.getNextStart(account).strftime('%H:%M:%S')}之后重启, 登陆失败次数: {stats.getFailedLogins(account)}")
                if stats.getFailedLogins(account) >= 5:
                    if config.notifyError:
                        params = {
                            "text": f"注意哦,账号:{account}掉线啦",
                        }
                        requests.post(config.connectorDrops,
                                      headers={"Content-type": "application/json"},
                                      json=params)
                    log.exception(f"Error in {account}. The program will try to recover.")
                log.warning(
                    f"Thread {account} has finished and will restart at {restarter.getNextStart(account).strftime('%H:%M:%S')}. Number of consecutively failed logins: {stats.getFailedLogins(account)}")

        for account in toDelete:
            del farmThreads[account]

        sleep(5)


if __name__ == '__main__':
    log = None
    try:
        log, config = init()
        main(log, config)
    except (KeyboardInterrupt, SystemExit):
        print('退出成功,欢迎使用本软件!')
        sys.exit()
    except CapsuleFarmerEvolvedException as e:
        if isinstance(log, logging.Logger):
            log.error(f"An error has occurred: {e}")
        else:
            print(f'[red]An error has occurred: {e}')
