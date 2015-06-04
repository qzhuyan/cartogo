import couchdb

class server(couchdb.Server):
    def __init__(self,url):
        self.server = couchdb.Server(url)
        self.db = self.server['car2go']
       
    def save(self,db,Data):
        self.server[db].save(Data)

    

