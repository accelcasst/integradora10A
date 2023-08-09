from .entities.Parking import Parking

class ModelParking():
    @classmethod
    def add_parking(self,db,id,parkings,space):
        self.id = id
        self.db = db
        self.parkings = parkings
        self.space = space
        