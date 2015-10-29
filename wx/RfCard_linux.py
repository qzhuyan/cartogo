from ctypes import *
from time import time

import unittest
import struct
import sys
debug = True
#Mute = False
Mute = True
#= Notes =
#secret control block FF 07 80 69


#global vars
Error = -1
mode = c_ubyte(0) #read/write mode

class RfCardReader():
    def getSerNum(self):
        return "abcde"
   
    def readhex(self,pwd,start,num):
        return "headhex"

    def readp(self,pwd,start,num):
        return "readp"

    def write(self,pwd,start,num,data):
        return 0

    def beep(self,freq=1, duration=3):
        return True;

#data on card:
## [unsigned int carid, unsigned int clientid,
##        float timeborrow, float timereturn]
class CarToGoRF(RfCardReader):
    dataformat='IIdd'
    def __init__(self,pwd='\xff\xff\xff\xff\xff\xff',carid=0,clientid=0):
        self.pwd = pwd #todo pwd length check
        self.carid = int(carid)
        self.clientid = int(clientid)
        self.borrowtag = float(0)
        self.returntag = float(0)

    def set_carid(self, carid):
        self.carid = carid

    def get_carid(self):
        return self.carid

    def update(self):
        ret = self.write(self.pwd,20,2,self.encode())
        return ret

    def get(self):
        res = self.readp(self.pwd, 20, 2)
        (errno, BDres) = res
        if errno != Error:
            self.cardid = errno
            res = (errno, self.decode(BDres))
        #todo throw exception here
        return res

    ## encode/decode, they shall be updated as a pair.
    def encode(self):
        return struct.pack(self.dataformat,self.carid,self.clientid,self.borrowtag,self.returntag)
        
    def decode(self,Data):
        (self.carid,self.clientid,self.borrowtag,self.returntag) = struct.unpack_from(self.dataformat,Data)
        return self

    def reset(self):
        if debug: print "in reset.."
        (res,old) = CarToGoRF().get()
        if res == -1:
            raise Exception(('reset_fail', old))
        new = CarToGoRF()
        new.carid = old.get_carid()
        res = new.update()
        if 0 != res:
            raise Exception(('reset_fail_update', res))
        return 0

#======
#tests
#======
# class RfCardReaderTest(unittest.TestCase):
#     defpwd = '\xff\xff\xff\xff\xff\xff' 
#     def test_getSerNum(self):
#         t=RfCardReader()
#         self.assertEqual(t.getSerNum(),"aabbaabbaabbaacc")

#     def test_readhex(self):
#         t=RfCardReader()
#         self.assertEqual(t.readhex(self.defpwd,4,1),("bd714e67","ffffff00000000000000000000000000"))

#     def test_write(self):
#         t=RfCardReader()
#         blk = 16
#         self.assertEqual(0, t.write(self.defpwd,blk,1,"abcef"))
#         pwd='\xff\xff\xff\xff\xff\xff' 
#         self.assertEqual(t.readhex(pwd,blk,1),("bd714e67","61626365660000000000000000000000"))   


# class CarToGORFTest(unittest.TestCase):
#     def test_init(self):
#         T= CarToGoRF("123456",100,99)
#         self.assertEqual(T.pwd, "123456")
#         self.assertEqual(T.carid, 100)
#         self.assertEqual(T.clientid, 99)

#     def test_encode(self):
#         T= CarToGoRF("123456",100,99)
#         self.assertEqual(T.encode(),'d\x00\x00\x00c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
#     def test_update(self):
#         T = CarToGoRF("\xff\xff\xff\xff\xff\xff",100,99)
#         T.borrowtag = 345.23753
#         self.assertEqual(T.update(), 0)
#         (Errno,BD) = T.get()
#         self.assertNotEqual(Errno, Error)
#         self.assertEqual(BD.carid, 100)
#         self.assertEqual(BD.clientid, 99)
#         self.assertEqual(BD.returntag, 0)
#         self.assertEqual(BD.borrowtag, 345.23753)

#     def test_get(self):
#         T = CarToGoRF("\xff\xff\xff\xff\xff\xff",100,99)
#         self.assertEqual(T.update(), 0)
#         (Errno,BD) = T.get()
#         self.assertNotEqual(Errno, Error)
#         self.assertEqual(BD.carid, 100)
#         self.assertEqual(BD.clientid, 99)
#         self.assertEqual(BD.returntag, 0)
#         self.assertEqual(BD.borrowtag, 0)

#     def test_update(self):
#         T = CarToGoRF("\xff\xff\xff\xff\xff\xff",100,99)
#         T.borrowtag = 345.23753
#         self.assertEqual(T.update(), 0)
#         (Errno,BD) = T.get()
#         self.assertNotEqual(Errno, Error)
#         self.assertEqual(BD.carid, 100)
#         self.assertEqual(BD.clientid, 99)
#         self.assertEqual(BD.returntag, 0)
#         self.assertEqual(BD.borrowtag, 345.23753)

        

#     def test_reset(self):
#          T = CarToGoRF("\xff\xff\xff\xff\xff\xff",2000,99)
#          upres = T.update()
#          rstres = T.reset()
         
#          T2 = CarToGoRF()
#          (res,new) = T2.get()

#          self.assertEqual(upres, 0)
#          self.assertEqual(rstres, 0)
#          self.assertEqual(res, 'bd714e67')
#          self.assertEqual(new.carid, 2000)
#          self.assertEqual(new.clientid, 0)
#          self.assertEqual(new.returntag, 0)
#          self.assertEqual(new.borrowtag, 0)

#     def test_beep(self):
#         T = CarToGoRF("\xff\xff\xff\xff\xff\xff",2000,99)
#         T.beep(10,1)

        
if __name__ == '__main__':
    #if sys.argv[1] == "test":
    unittest.main()

