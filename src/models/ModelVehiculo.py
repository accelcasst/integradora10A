from .entities.Vehiculo import Vehiculo

class ModelVehiculo():
    @classmethod
    def add_vehiculo(self,db,input_datetime,plate, parking_id):
        try:
            vehiculo_id = ""
            parking = db.connection.cursor()
            sql = "SELECT count(*) FROM vehiculos WHERE parking_id = {}".format(parking_id)
            parking.execute(sql)
            countCars = parking.fetchone()[0] + 1
            
            sql = "SELECT slots FROM parkings WHERE id = {}".format(parking_id)
            parking.execute(sql)
            countSlots = parking.fetchone()[0]

            #sql = "SELECT output_datetime FROM vehiculos WHERE plate = '{}' AND parking_id = {}".format(plate).format(parking_id)
            #print(sql)
            #parking.execute(sql)
            #output_datetime = parking.fetchone()[0]
            #print(output_datetime)

            valor=str(plate) + str(input_datetime)
            vehiculo_id = valor.upper()[1:9] 
            
            #if output_datetime != None:
            if countCars <= countSlots:
                parking.execute('INSERT INTO vehiculos (id,input_datetime,plate, parking_id) VALUES (%s,%s,%s,%s)',
                                (vehiculo_id,input_datetime,plate, parking_id))
                db.connection.commit()
                vehiculo = Vehiculo(vehiculo_id)
                return vehiculo
            else:
                vehiculo = Vehiculo('LLENO')
                return vehiculo
           # else:
            #    vehiculo = Vehiculo('ERROR')
             #   return vehiculo               
        except Exception as ex:
            db.connection.rollback()
            return None
        
    @classmethod
    def get_full_vehiculos(self,db):
        try:
            parking = db.connection.cursor()
            sql = "SELECT * FROM vehiculos"
            parking.execute(sql)
            data = parking.fetchall()
            return data
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def output_vehiculo(self,db,id,output):
        try:
            parking = db.connection.cursor()
            sql = "SELECT id FROM vehiculos WHERE id = {}".format(output)
            parking.execute(sql)
            data = parking.fetchall()
            return data
        except Exception as ex:
            raise Exception(ex)
