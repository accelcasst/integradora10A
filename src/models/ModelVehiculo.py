from .entities.Vehiculo import Vehiculo

class ModelVehiculo():
    @classmethod
    def add_vehiculo(self,db,input_datetime,plate, parking_id):
        try:
            vehiculo_id = ""
            parking = db.connection.cursor()
            parking.execute("SELECT output_datetime FROM vehiculos WHERE plate = %s AND parking_id = %s", (plate, parking_id))
            row = parking.fetchone()
            valor=str(plate) + str(input_datetime)

            vehiculo_id = valor.upper()[1:9] 
            
            if row != None:
                print(row)
                if row[0] != None:
                    #  UPDATE vehiculos SET plate = %s, parking_id = %s WHERE id = %s
                    parking.execute('INSERT INTO vehiculos (id,input_datetime,plate, parking_id) VALUES (%s,%s,%s,%s)',
                            (vehiculo_id,input_datetime,plate, parking_id))
                    
                    db.connection.commit()
                else:
                    return None
            else:
                parking.execute('INSERT INTO vehiculos (id,input_datetime,plate, parking_id) VALUES (%s,%s,%s,%s)',
                            (vehiculo_id,input_datetime,plate, parking_id))
                db.connection.commit()
                    
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            db.connection.close()