import yaml, requests
from yaml.parser import ParserError
from rich import print
from pathlib import Path

from Exceptions.InvalidCredentialsException import InvalidCredentialsException


class Config:
    """
    A class that loads and stores the configuration
    """

    REMOTE_BEST_STREAMS_URL = "https://raw.githubusercontent.com/LeagueOfPoro/CapsuleFarmerEvolved/master/config/bestStreams.txt"
    RIOT_API_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"

    def __init__(self, configPath: str) -> None:
        """
        Loads the configuration file into the Config object

        :param configPath: string, path to the configuration file
        """
        
        self.accounts = {}
        try:
            configPath = self.__findConfig(configPath)
            with open(configPath, "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
                accs = config.get("accounts")
                onlyDefaultUsername = True
                for account in accs:
                    self.accounts[account] = {
                        #Orig data
                        "username": accs[account]["username"],
                        "password": accs[account]["password"],
                        
                        #IMAP data
                        "imapUsername": accs[account].get("imapUsername", ""),
                        "imapPassword": accs[account].get("imapPassword", ""),
                        "imapServer": accs[account].get("imapServer", ""),
                    }
                    if "username" != accs[account]["username"]:
                        onlyDefaultUsername = False
                if onlyDefaultUsername:
                    raise InvalidCredentialsException                    
                self.debug = config.get("debug", False)
                self.connectorDrops = config.get("connectorDropsUrl", "")
                self.showHistoricalDrops = config.get("showHistoricalDrops", True)
        except FileNotFoundError as ex:
            print(f"[red]CRITICAL ERROR: 配置文件在這個 {configPath}找不到\n")
            print("Press any key to exit...")
            input()
            raise ex
        except (ParserError, KeyError) as ex:
            print(f"[red]CRITICAL ERROR: 配置文件格式錯誤")
            print("Press any key to exit...")
            input()
            raise ex
        except InvalidCredentialsException as ex:
            print(f"[red]CRITICAL ERROR: 配置文件還為初始值.請輸入賬號信息")
            print("Press any key to exit...")
            input()
            raise ex
        try:
            remoteBestStreamsFile = requests.get(self.REMOTE_BEST_STREAMS_URL)
            if remoteBestStreamsFile.status_code == 200:
                self.bestStreams = remoteBestStreamsFile.text.split()
        except Exception as ex:
            print(f"[red]CRITICAL ERROR: 去挂梯,如果已經挂了那就是挂的姿勢不對或者梯子不行")
            print("Press any key to exit...")
            input()
            raise ex

    def getAccount(self, account: str) -> dict:
        """
        Get account information

        :param account: string, name of the account
        :return: dictionary, account information
        """
        return self.accounts[account]
    
    def __findConfig(self, configPath):
        """
        Try to find configuartion file in alternative locations.

        :param configPath: user suplied configuartion file path
        :return: pathlib.Path, path to the configuration file
        """
        configPath = Path(configPath)
        if configPath.exists():
            return configPath
        if Path("../config/config.yaml").exists():
            return Path("../config/config.yaml")
        if Path("config/config.yaml").exists():
            return Path("config/config.yaml")
        
        return configPath
