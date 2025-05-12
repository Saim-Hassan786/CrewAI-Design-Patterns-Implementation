from crewai.flow.flow import Flow ,start, listen , or_, router
from litellm import completion
from pydantic import BaseModel

class Translation(BaseModel):
    user_input : str = ""
    language : str = ""

class Parallel(Flow[Translation]):
    model = "gemini/gemini-2.0-flash-exp"
    API_KEY = "Place Your API Key Here"

    @start()
    def method_1(self):
        user_input = input("Enter your input here to translate : ")
        language = input("Enter the language you want to get your text translated into : ")
        print(user_input)
        print(language)
        self.state.user_input = user_input
        self.state.language = language    

    @listen(method_1)
    def method_2(self):
        response = completion(
            model = self.model,
            api_key= self.API_KEY,
            messages=[{
                "role":"user",
                "content": f"Translate the following text into {self.state.language}:\n\n'{self.state.user_input}'\n\nProvide only the translated text in the response."
            }]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print(result)
        return result
    
  
    @listen(method_2)
    def method_3(self, result):
        response=completion(
            model = self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":f"Write a 10 words reply to {result} in the following language only {self.state.language}"
            }]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print(result)


        
def run_it_3():
    obj = Parallel()
    obj.kickoff()