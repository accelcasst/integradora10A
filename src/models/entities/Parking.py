
class Parking():
    def __init__(self,db,id,parking_name,location,phone_number,space):
        self.db = db
        self.id = id
        self.parkings = parking_name
        self.location = location
        self.phone_number = phone_number
        self.space = space
