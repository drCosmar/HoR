import requests, json, pathlib
import json

CURRENT_CONGRESS = 118
API = 

class pths:
    root = pathlib.Path(__file__).parent.absolute()
    data = root / "data"
    downloads = root / "downloads"
    enviroment = root / ".env"

class pycongress:
    def __init__(self, api, congress=None):
        self.api = api
        self.congress = congress
        self.rootURL = "https://api.congress.gov/v3/"

    def writeJson(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def readJson(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data

    def setUrl(self, dir:str):
        url = self.rootURL + dir + f"?apikey={self.api}"
        return url


