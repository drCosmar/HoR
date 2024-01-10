from openai import OpenAI
from utils import LMURL, loadingIndicator

# Class used to access the LM Studio server on your device, and leverage the AI LLM within the project.
class client:
    def __init__(self, sysprompt:str):
        self.sysprompt = sysprompt
        self.openai = OpenAI(base_url=LMURL, api_key="not_needed")
        self.history = [
                {"role": "system", "content": self.sysprompt},
            ]
        self.history_length = 0

    def updateHisLen(self):
        self.history_length = len(self.history)

    def appendHistoryUser(self, message):
        self.history.append( {"role": "user", "content": message})
        self.updateHisLen()

    def appendHsitoryAssistant(self, message):
        self.history.append( {"role": "assistant", "content": message})
        self.updateHisLen()
    @loadingIndicator
    def completion(self, message, stream=False):
        self.appendHistoryUser(message)
        comp = self.openai.chat.completions.create(
            model="local-model", # this field is currently unused
            messages=self.history,
            temperature=0.7,
            stream=True
            )

        newMessage = ""
        
        for chunk in comp:
            if chunk.choices[0].delta.content:
                if stream:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                newMessage += chunk.choices[0].delta.content

        self.appendHsitoryAssistant(newMessage)
    
        # Uncomment to see chat history
        # import json
        # gray_color = "\033[90m"
        # reset_color = "\033[0m"
        # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        # print(json.dumps(history, indent=2))
        # print(f"\n{'-'*55}\n{reset_color}")
        return newMessage

    def chat(self):
        while True:
            uIn = input("> ")
            if uIn.lower() == "exit":
                break
            self.completion(uIn, True)
    
    def main(self, message):
        response = self.completion(message)
        return response
