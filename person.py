class Person:
    def __init__(self, name, person_id, email):
        self.name = name
        self.person_id = person_id
        self.email = email

    def get_person_info(self):
        return f"Name: {self.name}, ID: {self.person_id}, Email: {self.email}"

