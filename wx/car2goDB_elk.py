from elasticsearch import Elasticsearch
from elasticsearch import TransportError
from datetime import datetime
from collections import defaultdict
class Document(dict):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @classmethod
    def load(self,table, id):
        return table.load(id)
    
    def store(self, table):
        if 'id' in self.__dict__:
            id = self.__dict__['id']
        else:
            id = None
        res = table.server.save(table, id, self)
        print "store data res: %s" % (res)


class TextField():
    ""

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

    def save(self, tab, id, Data):
        Data['timestamp'] = datetime.now()
        print "save data %s to table %s which id is %s" % (Data, tab, id)
        return self.index(self.db, doc_type=tab, id = id ,body=Data)

    def read(self, tab, uid):
        try:
            res = self.get(index=self.db, doc_type=str(tab), id=uid)
            data = res['_source']
            data['id'] = res['_id']
            print data
            return data
        except TransportError as e:
            if e.status_code == "404":
                return None

    def __getitem__(self,tabname):
        return table(tabname,self)

class table(server):
    def __init__(self, name, server):
        self.name = name
        self.server = server
    def __getitem__(self, id):
        self.server.read(self.name, id)

    def __str__(self):
        return self.name

    def load(self, id):
        d = self.server.read(self.name, id)
        if d:
            return Document(d)
        else:
            return None

#===========
# TESTS
#===========
import unittest
class car2goDB_elk_ut(unittest.TestCase):
    serverurl = "http://192.168.200.8:34567"
    
class DocTest(car2goDB_elk_ut):
    def test_init(self):
        doc = Document(a="1",b="2")
        self.assertEqual(doc["a"],"1")
        self.assertEqual(doc["b"],"2")

    # def test_set_get_attr(self):
    #     doc = Document(a="1",b="2")
    #     self.assertEqual(doc.a,"1")

    def test_store(self):
        ser = server(self.serverurl)
        doc1 = Document(a=1, b=2, id=100)
        tab = table("unittest", ser)
        doc1.store(tab)
        doc2 = Document().load(tab,100)
        self.assertEqual(1, doc2['a'])
        doc2.load(tab, 100)
        self.assertEqual(2, doc2['b'])

class server_test(car2goDB_elk_ut):
    "to make case pass, make sure, elk is running locally"
    testdata = Document(a=1, b=2)
    testdata.id =3
    def test_init(self):
        server(self.serverurl)
    
    def test_save(self):
        s = server(self.serverurl)
        s.save("unittest", 1,{'a':1, 'b':2})

    def test_read(self):
        s = server(self.serverurl)
        s.save("unittest", 1,{'a':1, 'b':2})
        res = s.read("unittest",1)
        self.assertEqual(res['a'] ,1)
        self.assertEqual(res['b'] ,2)

    def test_read_doc(self):
        s = server(self.serverurl)
        s.save("unittest", self.testdata.id, self.testdata)
        res = s.read("unittest",self.testdata.id)
        self.assertEqual(res['a'] ,1)
        self.assertEqual(res['b'] ,2)


    def test_read_notfound(self):
        s = server(self.serverurl)
        res = s.read("unittest","notfound")
        self.assertEqual(None , res)

if __name__ == '__main__':
    unittest.main()
