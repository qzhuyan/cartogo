from elasticsearch import Elasticsearch
from elasticsearch import TransportError
class Document(dict):
    def load(self, table, id):
        doc = Document()
        doc.id = id
        doc.tab = table
        return doc

    def store(self, table):
        table.server.save(table,self.id,self)

class TextField():
    pass

class RentDoc(Document):
    CardId = TextField()
    CarId = TextField()
    Client = TextField() 
    Rent   = TextField() 
    Return = TextField()

class CustomerDoc(Document):
    name = TextField()

class CardDoc(Document):
    CarId = TextField()
    time = TextField()

class server(Elasticsearch):
    def __init__(self,addr,db="testdb1"):
        self.db = db
        super(server, self).__init__([addr])

    def save(self, tab, id,Data):
        return self.index(self.db, doc_type=tab, id = id ,body=Data)

    def read(self, tab, uid):
        try:
            res = self.get(index=self.db, doc_type=tab, id=uid)
            return res['_source']
        except TransportError as e:
            if e.status_code == "404":
                return None

    def __getitem__(self,tabname):
        return table(tabname,self)

class table(server):
    def __init__(self, name, server):
        self.name = name
        self.server = server

    def __getitem__(self,id):
        self.server.read(self.name,id)

#===========
# TESTS
#===========
import unittest
class DocTest(unittest.TestCase):
    def test_init(self):
        doc = Document(a=1,b=2)
        self.assertEqual(doc["a"],1)
        self.assertEqual(doc["b"],2)
        
    def test_load(self):
        doc = Document().load("tab1", 1)
        self.assertEqual(doc.id,1)
        self.assertEqual(doc.tab,"tab1")
        doc["d"] = 4
        self.assertEqual(doc["d"],4)
        self.assertEqual(doc, {"d":4})
    
    def test_store(self):
        self.assertEqual("todo","do it ")

class server_test(unittest.TestCase):
    "to make case pass, make sure, elk is running locally"
    testdata = Document(a=1,b=2)
    testdata.id =1
    def test_init(self):
        server("http://127.0.0.1:34567")
    
    def test_save(self):
        s = server("http://127.0.0.1:34567")
        s.save("unittest", 1,{'a':1, 'b':2})

    def test_read(self):
        s = server("http://127.0.0.1:34567")
        s.save("unittest", self.testdata.id, self.testdata)
        res = s.read("unittest",self.testdata.id)
        self.assertEqual(res ,self.testdata)

    def test_read_notfound(self):
        s = server("http://127.0.0.1:34567")
        res = s.read("unittest","notfound")
        self.assertEqual(None , res)

if __name__ == '__main__':
    unittest.main()
