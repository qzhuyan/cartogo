import couchdb
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

class RentDoc(Document):
    CardId = TextField() 
    Client = TextField() 
    Rent   = TextField() 
    Return = TextField()

class CustomerDoc(Document):
    name = TextField()

class CardDoc(Document):
    CarId = TextField()
    time = TextField()

class server(couchdb.Server):
    def save(self,db,Data):
        return self.server[db].save(Data)

    def get(self, db, uid):
        try:
            return self.server[db][uid]
        except couchdb.http.ResourceNotFound as err:
            if err == (u'not_found', u'missing'):
                return None

    def query(self, db, fun):
        return self.server[db].query(fun)

    

    

