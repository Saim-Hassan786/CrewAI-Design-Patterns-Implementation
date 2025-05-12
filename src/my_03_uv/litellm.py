from crewai.flow.flow import Flow, start, listen
from litellm import completion

API_KEY = "Place Your API Key Here"

class CityFunFact(Flow):
    
    @start()
    def generate_random_city(self):
        result = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=API_KEY,
            messages=[
                {"role":"user","content":"Return the name of a City name from Pakistan"}
            ]
        )
        city_name = result["choices"][0]["message"]["content"]
        print(city_name)
        self.state["city"] = city_name
        return city_name
    
    @listen(generate_random_city)
    def generate_fun_fact(self,city_name):
        result = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=API_KEY,
            messages=[
                {"role":"user","content":f"Generate some Fun Facts about the {city_name}"}
            ]
        )
        funfact = result["choices"][0]["message"]["content"]
        print(funfact)
        self.state["funfact"]=funfact
        return funfact

    @listen(generate_fun_fact)
    def save_fun_fact(self,funfact):
        with open("fun_fact.md","w") as f:
            f.write(funfact)



def kickoff_1():
    obj = CityFunFact()
    obj.kickoff()        
