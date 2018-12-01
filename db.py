import pymysql.cursors
import genpass

class Database(object):
    def __init__(self):
        self.host = "localhost"
        self.usrnme = "root"
        self.pswrd = ""
        self.dbnme = "geo_loc"
        self.connection = pymysql.connect(host=self.host,
                             user=self.usrnme,
                             password=self.pswrd,
                             db=self.dbnme,
                             cursorclass=pymysql.cursors.DictCursor)

    def con_auth(self, mobile, user_pass):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM users WHERE mobile='"+mobile+"'"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
        try:
            userpass = check["password"]
            if genpass.check_password_hash(userpass, user_pass):
                return check

        except:
            return None

    def register_user(self, mobile, user_pass):
        with self.connection.cursor() as cursor:
            hash_pass = genpass.User(mobile, user_pass)
            hash_pass = hash_pass.pw_hash
            com = "INSERT INTO users VALUES ('"+mobile+"', '"+hash_pass+"', 'user')"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()

    def register_admin(self, adminID, adminPass):
        with self.connection.cursor() as cursor:
            hash_pass = genpass.User(adminID, adminPass)
            hash_pass = hash_pass.pw_hash
            com = "INSERT INTO users VALUES ('"+adminID+"', '"+hash_pass+"', 'admin')"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
