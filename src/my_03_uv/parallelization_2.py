from crewai.flow.flow import Flow ,start, listen , or_, router
from litellm import completion

class Parallel(Flow):
    model = "gemini/gemini-2.0-flash-exp"
    API_KEY = "Place Your API Key Here"

    @start()
    def step_1a(self):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":"Generate a 7 words Sentence About Cricket with the fist word starting with cricket"
            }]
        )    
        result_a = response["choices"][0]["message"]["content"].strip()
        print("Step 1a Completed",result_a)
        return result_a

    @start()
    def step_1b(self):
        response = completion(
            model = self.model,
            api_key= self.API_KEY,
            messages=[{
                "role":"user",
                "content":"Generate a 7 words sentence about Football with the first word starting with football"
            }]
        )
        result_b = response["choices"][0]["message"]["content"].strip()
        print("Step 1b Completed", result_b)
        return result_b
    
  
    @listen(step_1a)
    def player_A(self,result_a):
        response=completion(
            model = self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":f"List me about the 5 Greatest Current Player in {result_a} only"
            }]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print("Greatest Player About Cricket")
        print(result)
        return result
    
    @listen(step_1b)
    def player_B(self,result_b):
        response=completion(
            model = self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":f"List me about the 5 Greatest Current Player in {result_b} only"
            }]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print("Greatest Player About Football")
        print(result)
        return result
    

def run_it_2():
    obj = Parallel()
    obj.kickoff()