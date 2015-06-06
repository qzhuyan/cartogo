import couchdb

class server(couchdb.Server):
    def __init__(self,url):
        self.server = couchdb.Server(url)
       
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

    

    

S = server("http://192.168.0.28:5984/")
print S.get('car2go_rent',"3")
