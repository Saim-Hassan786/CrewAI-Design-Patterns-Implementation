from crewai.flow.flow import Flow , start, listen
from litellm import completion
from pydantic import BaseModel

class Structure(BaseModel):
    user_input : str = ""
    words : int = 0
    essay : str = ""

class Essay_writer(Flow[Structure]):
    model = "gemini/gemini-2.0-flash-exp"
    API_KEY = "Place Your API Key Here"

    @start()
    def Step_1(self) :
       user_input = input("Write Down The Topic On Which You Want the Essay To Be Written : ")
       words =  input("Write Down The Number Of Words You Want Your Essay To Comprise Of : ") 
       print(user_input)
       print(words)
       self.state.user_input = user_input
       self.state.words = words

    @listen(Step_1)
    def Step_2(self):
        response = completion(
            model = self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":f"""You are an Adept Essay Writer that has All the capabilities of 
                writing a very wonderful Essay so keeping above in context perform the following tasks:-
                1. Generate A Good Heading of the Essay
                2. Write A Precise And Concise <Essay> on the following topic comprising of exactly the prescribed <words> given below(Not more not less exact the same words) with Generated Heading in first step
                <topic> : <Words>
                <{self.state.user_input}> : <{self.state.words}>
                3.Just give the output at the End like only Heading and Essay not any other thing like format below
                <Heading>

                <Essay>
                """
            }]
        )  
        result= response["choices"][0]["message"]["content"].strip()
        print(result)
        self.state.essay = result

    
    @listen(Step_2)
    def Step_3(self):
        response = completion(
            model = self.model,
            api_key=self.API_KEY,
            messages=[{
                "role":"user",
                "content":f"For the Essay generated ahead rate it out of 10 after thoroughly evaluating it {self.state.essay} and tell in 10 words whether you liked it or not"
            }]
        )
        result= response["choices"][0]["message"]["content"].strip()
        print(result)

def write_essay():
    obj = Essay_writer()
    obj.kickoff()         