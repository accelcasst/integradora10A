from .entities.Parking import Parking

class ModelParking():
    @classmethod
    def add_parking(self,db,parking_name,location,phone_number,space):
        try:
            parking = db.connection.cursor()
            sql = """SELECT parking_name FROM parkings WHERE parking_name = '{}'""".format(parking_name)
            parking.execute(sql)
            row = parking.fetchone()
            if row == None:
                print(row)
                parking.execute('INSERT INTO parkings (parking_name,location,phone_number,slots) VALUES (%s,%s,%s,%s)',
                            (parking_name,location,phone_number,space))
                db.connection.commit()
            else:
                return None                  
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        
    @classmethod
    def get_parking(self, db, id):
        try:
            parking = db.connection.cursor()
            parking.execute('SELECT * FROM parkings WHERE id = %s', (id))
            data = parking.fetchone()
            return data
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_full_parking(self, db):
        try:
            parking = db.connection.cursor()
            sql = "SELECT * FROM parkings"
            parking.execute(sql)
            data = parking.fetchall()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_parking(self,db,parking_name,location,phone_number,space,id):
        try:
            parking = db.connection.cursor()
            parking.execute("""UPDATE parkings 
                            SET parking_name = %s,
                            location = %s,phone_number = %s,
                            slots = %s WHERE id = %s""",(parking_name,location,phone_number,space,id))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        
    @classmethod
    def delete_parking(self,db,id):
        try:
            parking = db.connection.cursor()
            parking.execute('DELETE FROM parkings WHERE id = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
        #Crear metodo para obtener el id y nombre de todos los estacionameintos