from datetime import datetime
from threading import Thread
from time import sleep
from Browser import Browser
import requests
import dingding_webhook.webhook as dingding_webhook

from SharedData import SharedData

class FarmThread(Thread):
    """
    A thread that creates a capsule farm for a given account
    """

    def __init__(self, log, config, account, stats, locks, sharedData: SharedData):
        """
        Initializes the FarmThread

        :param log: Logger object
        :param config: Config object
        :param account: str, account name
        :param stats: Stats, Stats object
        """
        super().__init__()
        self.log = log
        self.config = config
        self.account = account
        self.stats = stats
        self.browser = Browser(self.log, self.config, self.account, sharedData)
        self.locks = locks
        self.sharedData = sharedData

    def run(self):
        """
        Start watching every live match
        """
        try:
            self.stats.updateStatus(self.account, "[green]LOGIN")
            if self.browser.login(self.config.getAccount(self.account)["username"], self.config.getAccount(self.account)["password"], self.locks["refreshLock"]):
                self.stats.updateStatus(self.account, "[green]LIVE")
                self.stats.resetLoginFailed(self.account)
                while True:
                    self.browser.maintainSession()
                    watchFailed = self.browser.sendWatchToLive()
                    newDrops = []
                    if self.sharedData.getLiveMatches():
                        liveMatchesStatus = []
                        for m in self.sharedData.getLiveMatches().values():
                            if m.league in watchFailed:
                                leagueName = f"[red]{m.league}[/]"
                            else:
                                leagueName = str(m.league)
                            liveMatchesStatus.append(leagueName)
                        self.log.debug(f"Live matches: {', '.join(liveMatchesStatus)}")
                        liveMatchesMsg = f"{', '.join(liveMatchesStatus)}"
                        newDrops = self.browser.checkNewDrops(self.stats.getLastDropCheck(self.account))
                        self.stats.updateLastDropCheck(self.account, int(datetime.now().timestamp() * 1e3))
                    else:
                        liveMatchesMsg = self.sharedData.getTimeUntilNextMatch()
                    try:
                        if newDrops and getLeagueFromID(newDrops[-1]["leagueID"]):
                            self.stats.update(self.account, len(newDrops), liveMatchesMsg, getLeagueFromID(newDrops[-1]["leagueID"]))
                        else:
                            self.stats.update(self.account, 0, liveMatchesMsg)
                    except (IndexError, KeyError):
                        self.stats.update(self.account, len(newDrops), liveMatchesMsg)
                    if self.config.connectorDrops:
                        self.__notifyConnectorDrops(newDrops)
                    sleep(Browser.STREAM_WATCH_INTERVAL)
            else:
                self.log.error(f"Login for {self.account} FAILED!")
                self.stats.addLoginFailed(self.account)
                if self.stats.getFailedLogins(self.account) < 3:
                    self.stats.updateStatus(self.account, "[red]LOGIN FAILED - WILL RETRY SOON")
                else:
                    self.stats.updateStatus(self.account, "[red]LOGIN FAILED")
        except Exception:
            self.log.exception(f"Error in {self.account}. The program will try to recover.")

    def stop(self):
        """
        Try to stop gracefully
        """
        self.browser.stopMaintaininingSession()

    def __notifyConnectorDrops(self, newDrops: list):
        if newDrops:
            if self.config.accounts[0] in self.account:
                title1 = newDrops[0]["dropsetTitle"]
                title = f"[{self.account}] {title1}"
                rewardImage = newDrops[0]["inventory"][0]["localizedInventory"]["inventory"]["imageUrl"]
                msgUrl = "https://lolesports.com/rewards"
                post_url = self.config.connectorDrops
                leagueId = getLeagueFromID(newDrops[0]["leagueID"])
                text = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "Received a Capsule From " + leagueId;
                dingding_webhook.send_link(post_url, title, text, rewardImage, msgUrl)
            
            

def getLeagueFromID(leagueId):
    allLeagues = getLeagues()
    for league in allLeagues:
        if leagueId in league["id"]:
            return league["name"]
    return ""
def getLeagues():
    headers = {"Origin": "https://lolesports.com", "Referrer": "https://lolesports.com",
               "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
    res = requests.get(
        "https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-GB", headers=headers)
    leagues = res.json()["data"].get("leagues", [])
    res.close()
    return leagues
