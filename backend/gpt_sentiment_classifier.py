import openai
import ast
class GptSentimentClassifier():
    
    def __init__(self,message_history:str) -> None:
        openai.api_key = open("key.txt","r").read().strip("\n")
        self.message_history=message_history
        
    def get_message_history(self):
        return self.message_history
    
    def chat(self):
        is_continue=True
        while is_continue:
            input_s=input(">")
            self.message_history.append({"role":"user","content":input_s})
        
            completion=openai.ChatCompletion.create(
                
                model="gpt-3.5-turbo",
                messages=self.message_history
            )
            reply_content=completion.choices[0].message.content
            print(reply_content)
            self.message_history.append({"role":"assistant","content":reply_content})
            yes_or_no=input("Would you like to continue to chat?(Yes:y, No:n)")
            if yes_or_no =="n":
                is_continue=False
            
        return self.message_history
    
    def classify_sentence(self,sentence:str):
        self.message_history.append({"role":"user","content":sentence})
        
        completion=openai.ChatCompletion.create(
            
            model="gpt-4",
            messages=self.message_history
        )
        sentiment_result=completion.choices[0].message.content
        self.message_history.append({"role":"assistant","content":sentiment_result})
        return sentiment_result
        
if __name__ == '__main__':
     message_history=open('message_history.txt',"r",encoding="utf-8").read()
     message_history=ast.literal_eval(message_history)
     gpt_classifier= GptSentimentClassifier(message_history)
    
     gpt_classifier.classify_sentence("Küresel piyasalarda ABD'den gelen veriler geçen haftanın öne çıkan gündem maddeleri olurken, Türkiye'de TCMB'nin attığı adımlar ve açıklanan veriler izlendi.")
     