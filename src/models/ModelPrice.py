

class ModelPrice():
    @classmethod
    def add_price(self,db,time_min,time_max,tolerance_time,payment,parking_id):
        try:
            parking = db.connection.cursor()
            sql = """SELECT parking_id FROM prices WHERE parking_id = '{}'""".format(parking_id)
            parking.execute(sql)
            row = parking.fetchone()
            if row == None:
                print(row)
                parking.execute('INSERT INTO prices (time_min,time_max,tolerance_time,payment,parking_id) VALUES (%s,%s,%s,%s)',
                            (time_min,time_max,tolerance_time,payment,parking_id))
                db.connection.commit()
            else:
                return None                  
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)