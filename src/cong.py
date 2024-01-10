from utils import os, PATHS, CONAPI, DEFAULT, requests, re,\
timeStamp, stringToDatetime

# All research is limited by default to the current congress so they don't start restrictingtheir API.
# Please make sure you make API calls responsibly.
class congressProbe:
    def __init__(self):
        self.dataFp = PATHS.congressData
        self.rootURL = "https://api.congress.gov/v3"
        self.api = CONAPI
        print(self.api)

        self.conSess = self.getSessionNum() #Rtrieves the most current congress in session.

    def requestHandler(self, url:str):
        data = requests.get(url)
        if data.status_code == 200:
            return data.json()
        else:
            print(f"Error: {data.status_code}\n{data.json()}")

    def createURL(self, dir:str):
        if self.conSess == None:
            self.conSess = self.getSessionNum()
        self.url = self.rootURL + dir + f"?api_key={self.api}"
    
    def getSessionNum(self):
        self.url = self.rootURL + "/congress" + f"?api_key={self.api}"
        data = self.requestHandler(self.url)
        sessNum = int(re.search(r"(\d+)", data['congresses'][0]['name']).group(1))
        return sessNum

    def getMembers(self):
        self.createURL("/member")
        members = self.requestHandler(self.url)
        return members

    def getBills(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/bill")
        else:
            self.createURL(f"/bill/{self.conSess}")
        bills = self.requestHandler(self.url)
        return bills
    
    def getAmendments(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/amendment")
        else:
            self.createURL(f"/amendment/{self.conSess}")
        amendments = self.requestHandler(self.url)
        return amendments
    
    def getSummaries(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/summaries")
        else:
            self.createURL(f"/summaries/{self.conSess}")
        summaries = self.requestHandler(self.url)
        return summaries
    
    def getCommittees(self, allSess:bool=DEFAULT, chamber=None):
        if allSess == True and chamber == None:
            self.createURL("/committee")
        if allSess == False and chamber != None:
            self.createURL(f"/committee/{self.conSess}/{chamber}")
        if allSess == True and chamber != None:
            self.createURL(f"/committee/{chamber}")
        else:
            self.createURL(f"/committee/{self.conSess}")
        
        committees = self.requestHandler(self.url)
        return committees
    
    def getCommitteeReports(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/committee-report")
        else:
            self.createURL(f"/committee-report/{self.conSess}")
        committeeReports = self.requestHandler(self.url)
        return committeeReports
    
    def getCommitteePrints(self, allSess:bool=DEFAULT, chamber:str=None):
        if allSess == True and chamber == None:
            self.createURL("/committee-print")
        if allSess == False and chamber != None:
            self.createURL(f"/committee-print/{self.conSess}/{chamber}")
        if allSess == True and chamber != None:
            self.createURL(f"/committee-print/{chamber}")
        else:
            self.createURL(f"/committee-print/{self.conSess}")
        
        committeePrints = self.requestHandler(self.url)
        return committeePrints
    
    def getCommitteeMeetings(self, allSess:bool=DEFAULT, chamber:str=None):
        if allSess == True and chamber == None:
            self.createURL("/committee-meeting")
        if allSess == False and chamber != None:
            self.createURL(f"/committee-meeting/{self.conSess}/{chamber}")
        if allSess == True and chamber != None:
            self.createURL(f"/committee-meeting/{chamber}")
        else:
            self.createURL(f"/committee-meeting/{self.conSess}")
        
        committeeMeetings = self.requestHandler(self.url)
        return committeeMeetings
    
    def getHearings(self, allSess:bool=DEFAULT, chamber:str=None):
        if allSess == True and chamber == None:
            self.createURL("/hearing")
        if allSess == False and chamber != None:
            self.createURL(f"/hearing/{self.conSess}/{chamber}")
        if allSess == True and chamber != None:
            self.createURL(f"/hearing/{chamber}")
        else:
            self.createURL(f"/hearing/{self.conSess}")
        
        hearings = self.requestHandler(self.url)
        return hearings
    
    #WARNING: This enpoint is very sensitive. It's It is not recommended to use it unless you know what you are doing.
    # Default values are set to the prior day to today (your machine's date). It's intended use is for "lookup".
    # Fetching the same day data, will usually fetch you incomplete data until the next day or even longer in some cases.
    # Use dailyConggresionalRecord or boundCongressionalRecords to get the most up to date data on proceedings.
    def getCongressionalRecord(self, date:str=None):
        if date == None:
            today = timeStamp()
            self.createURL(f"/congressional-record/?y={today.year}&m={today.month}&d={today.day-1}")
        else:
            d = stringToDatetime(date)
            self.createURL(f"/congressional-record/?y={d.year}&m={d.month}&d={d.day}")
        
        congressionalRecord = self.requestHandler(self.url)
        return congressionalRecord

    def getDailyConggresionalRecord(self):
        self.createURL(f"/daily-congressional-record/{self.conSess}")
        dailyCongressionalRecord = self.requestHandler(self.url)
        return dailyCongressionalRecord
    
    def getBoundCongressionalRecord(self, year:int=None, month:int=None, day:int=None):
        if year != None and month == None and day == None:
            self.createURL(f"/bound-congressional-record/{year}")
        if year != None and month != None and day == None:
            self.createURL(f"/bound-congressional-record/{year}/{month}")
        if year != None and month != None and day != None:
            self.createURL(f"/bound-congressional-record/{year}/{month}/{day}")
        else:
            self.createURL(f"/bound-congressional-record")

        boundCongressionalRecords = self.requestHandler(self.url)
        return boundCongressionalRecords
    
    def getHouseCommunications(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/house-communication")
        else:
            self.createURL(f"/house-communication/{self.conSess}")
        houseCommunications = self.requestHandler(self.url)
        return houseCommunications

    def getHouseRequirements(self):
        self.createURL(f"/house-requirement")
        houseRequirement = self.requestHandler(self.url)
        return houseRequirement
    
    def getSenateCommunications(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/senate-communication")
        else:
            self.createURL(f"/senate-communication/{self.conSess}")
        senateCommunication = self.requestHandler(self.url)
        return senateCommunication

    def getNominations(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/nomination")
        else:
            self.createURL(f"/nomination/{self.conSess}")
        nominations = self.requestHandler(self.url)
        return nominations
    
    def getTreaties(self, allSess:bool=DEFAULT):
        if allSess:
            self.createURL("/treaty")
        else:
            self.createURL(f"/treaty/{self.conSess}")
        treaties = self.requestHandler(self.url)
        return treaties
