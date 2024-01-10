from openai import OpenAI
from bin.utils import LMURL, loadingIndicator

# Class used to access the LM Studio server on your device, and leverage the AI LLM within the project.
# There can only be one client class at a time.
class client:
    def __init__(self, sysprompt:str):
        self.sysprompt = sysprompt
        self.openai = OpenAI(base_url=LMURL, api_key="not_needed")
        self.history = [
                {"role": "system", "content": self.sysprompt},
            ]
        self.historyLength = 0
    # This function is used to update the history length variable.
    def updateHistoryLen(self):
        self.historyLength = len(self.history)
    # self explanatory
    def appendHistoryUser(self, message):
        self.history.append( {"role": "user", "content": message})
        self.updateHistoryLen()
    # Self explanatory
    def appendHsitoryAssistant(self, message):
        self.history.append( {"role": "assistant", "content": message})
        self.updateHistoryLen()   
    @loadingIndicator # This decorator is used to display a loading indicator while the completion is being processed.
    def completion(self, message, stream=False, doneEvent=None):
        self.appendHistoryUser(message)
        comp = self.openai.chat.completions.create(
            model="local-model", # this field is currently unused
            messages=self.history,
            temperature=0.7,
            stream=True # You cannot edit the parameters here. Leave streaming on.
            )
        if stream:
            doneEvent.set()
            print("\n")
        newMessage = "" # This variable is used to store the new message.
        for chunk in comp:
            if chunk.choices[0].delta.content:
                if stream:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                newMessage += chunk.choices[0].delta.content

        self.appendHsitoryAssistant(newMessage)
    
        ## Uncomment to see chat history
        ## This is useful for debugging and testing, so I left it in.
        # import json
        # gray_color = "\033[90m"
        # reset_color = "\033[0m"
        # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        # print(json.dumps(self.history, indent=2))
        # print(f"\n{'-'*55}\n{reset_color}")
        return newMessage
    # This chat function remains untested.
    def chat(self):
        while True:
            uIn = input("\n>>> ")
            if uIn.lower() == "exit":
                break
            self.completion(uIn, True)
    # This is the main function that is used to call the completion function within other parts of your program.    
    def main(self, message):
        response = self.completion(message)
        return response
