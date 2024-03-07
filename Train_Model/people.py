class People:
    # constants
    mass_per_person = 81.65  # in kg

    def __init__(self, ppl=1):
        self.people_number = int()
        self.set_people(ppl)

    def set_people(self, ppl):
        if ppl <= 1:
            self.people_number = 1
        else:
            self.people_number = ppl

    def mass_of_people(self):
        return self.mass_per_person * self.people_number
