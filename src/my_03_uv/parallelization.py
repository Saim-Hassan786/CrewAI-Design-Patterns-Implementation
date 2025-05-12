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
        self.state["cricket"] = result_a
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
        self.state["football"] = result_b
        return result_b
    
    @listen(or_(step_1a,step_1b))
    @router("router_result_of_all")
    def or_result(self,result_a=None,result_b=None):
        if result_a :
            print("First Result: ")
            if "cricket" in result_a.lower():
                return "cricket"
        elif result_b:
            print("Second Result: ")
            if "football" in result_b.lower():
                return "football"
        
    @listen("cricket")
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
    
    @listen("football")
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



def run_it():
    obj = Parallel()
    obj.kickoff()

