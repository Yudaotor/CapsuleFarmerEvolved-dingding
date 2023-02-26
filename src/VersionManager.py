import requests as req

class VersionManager:

    @staticmethod
    def getLatestTag():
        try:
            latestTagResponse = req.get("https://github.com/Yudaotor/CapsuleFarmerEvolved-dingding/releases/latest")
            if 'application/json' in latestTagResponse.headers.get('Content-Type', ''):
                latestTagJson = latestTagResponse.json()
                if "tag_name" in latestTagJson:
                    return float(latestTagJson["tag_name"][1:])
            return 0.0
        except Exception:
            print("查找是否版本是否为最新时发生错误")
    @staticmethod
    def isLatestVersion(currentVersion):
        return currentVersion >= VersionManager.getLatestTag()