import people
import random


class PassengerPeople(people.People):
    def __init__(self, ppl=0, max_ppl=222):
        super().__init__(ppl)
        self.set_people(ppl, max_ppl)

    def set_people(self, ppl, max_ppl=222):
        if ppl >= max_ppl:
            self.people_number = max_ppl
        elif ppl <= 0:
            self.people_number = 0
        else:
            self.people_number = ppl

    def update_at_station(self, incoming, max_ppl):
        disembarking = random.randint(0, self.people_number)
        self.set_people(self.people_number - disembarking + incoming, max_ppl)
        return disembarking
