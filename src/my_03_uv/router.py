from crewai.flow.flow import Flow,start,listen,router
from pydantic import BaseModel
import random

class State(BaseModel):
    is_true : bool = False


class Router(Flow[State]):

    @start()
    def method_1(self) :
        print("Method 1.....")
        random_boolean = random.choice([True,False]) 
        print(random_boolean)
        self.state.is_true = random_boolean

    @router(method_1)
    def method_2(self):
        print("Method 2.....")
        if self.state.is_true:
            return "SUCCESS"
        else:
            return "FAILURE"

    @listen("SUCCESS")
    def method_3(self):
        print("Method 3 With SUCCESS")

    @listen("FAILURE")
    def method_4(self) :
        print("Method 4 With FAILURE")


def kickoff_2():
    obj = Router()
    obj.kickoff()                           