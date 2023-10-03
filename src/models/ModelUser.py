from .entities.User import User


class ModelUser(): 

    @classmethod
    def login(self, db, user):
        try:
            print(user)
            parking = db.connection.cursor()
            sql = """SELECT id, username, password, fullname, rol FROM users
                    WHERE username = '{}'""".format(user.username)
            parking.execute(sql)
            row = parking.fetchone()
            if row != None:
                print(row)
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            parking = db.connection.cursor()
            sql = "SELECT id, username,fullname, rol FROM users WHERE id = {}".format(id)
            parking.execute(sql)
            row = parking.fetchone()
            if row != None:
                logged_user = User(row[0], row[1],None,row[2], row[3])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def get_full_users(self, db):
        try:
            parking = db.connection.cursor()
            sql = "SELECT * FROM users"
            parking.execute(sql)
            data = parking.fetchall()
            return data
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_list_users(self, db):
        try:
            parking = db.connection.cursor()
            sql = "SELECT * FROM users WHERE rol = 'USER'"
            parking.execute(sql)
            data = parking.fetchall()
            return data
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_user(self, db,fullname,email,username,password):
        try:
            parking = db.connection.cursor()
            parking.execute('INSERT INTO users (fullname,email, username, password, rol) VALUES (%s,%s,%s,%s,%s)',(fullname,email,username,password, 'USER'))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_user(self, db, id):
        try:
            parking = db.connection.cursor()
            parking.execute('SELECT * FROM users WHERE id = %s', (id))
            data = parking.fetchone()
            return data
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_user(self, db,fullname,email,username,password,id):
        try:
            parking = db.connection.cursor()
            parking.execute("""
                    UPDATE users
                    SET fullname = %s,
                        email = %s,
                        username = %s,
                        password = %s
                    WHERE id = %s 
                        """, (fullname, email, username, password, id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_user(self, db,id):
        try:
            parking = db.connection.cursor()
            parking.execute('DELETE FROM users WHERE id = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        

