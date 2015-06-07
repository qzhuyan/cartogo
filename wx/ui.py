#!/usr/bin/python
# coding=utf-8

import wx

from RfCard import *
from time import sleep
from time import time
from datetime import datetime
import threading
from wx.lib.newevent import NewEvent
import ctypes

import car2goDB
from car2goDB import RentDoc, CustomerDoc, CardDoc

niceface=""

debug=True

wxCardInsert, EVT_CARD_INSERT= NewEvent()

ALLOWSTATES="IDLE CARDIN DIALOGIFREG PASSWORDOK".split()

TIMEFMT = '%Y-%m-%d %H:%M:%S'

DEF_PWD = '\xff\xff\xff\xff\xff\xff'

beepf = 10 #beep fequency
beepd = 2  #beep duration

ROWS = 5
COLS = 4

BORDER = 20

##DB
DBServerUrl = 'http://wtwo.no-ip.org:5984/'
CardDB = 'car2go_card'
CustomerDB = 'car2go_customer'
RentDB = 'car2go_rent'


class StateError(Exception):
    def __init__(self,State):
        self.value=State
    def __str__(self):
        repr(self.value)

class MainFrame(wx.Frame):
    def __init__(self,size):
        no_caption = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CLIP_CHILDREN
        on_top =  wx.STAY_ON_TOP
        frameStyle = no_caption
        frameStyle = wx.DEFAULT_FRAME_STYLE | on_top | no_caption
        
        wx.Frame.__init__(self, None, -1, title="CarToGo",
                          size=(1024,768), style = frameStyle )

        panel = wx.Panel(self)

        TopLB = wx.StaticText(panel, -1, u"租借登记系统",size = (-1,100), style = wx.ALIGN_CENTRE)
        TopLB.SetFont(wx.Font( 50 , wx.SWISS, wx.NORMAL, wx.BOLD))
        TopLB.SetBackgroundColour(wx.Colour(58,87,149))
        TopLB.SetForegroundColour('white')

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(TopLB,0,wx.ALL|wx.EXPAND, border = 0)
        mainsizer.Add(wx.StaticLine(panel,size = (-1,3)),0,wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)

        sizer = wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        CustomerS = wx.StaticText(panel, -1, label=u"客户名称" )
        CustomerC = wx.StaticText(panel, -1, label=u"")
        CustomerNumS = wx.StaticText(panel, -1, label=u"客户编号")
        CustomerNumC = wx.TextCtrl(panel, -1, "", )
        Dummy = wx.StaticText(panel, -1, label=u"")
        Dummy2 = wx.StaticText(panel, -1, label=u"")

        
        CarNumS = wx.StaticText(panel, -1, u"车号",  style = wx.ALIGN_CENTRE)
        CarNumC = wx.TextCtrl(panel, -1, "", )

        # * ROW FOUR *
 
        TimeRentS = wx.StaticText(panel, -1, u"租车时间")
        TimeRentC = wx.TextCtrl(panel, -1, "")
        TimeReturnS = wx.StaticText(panel, -1, u"还车时间")
        TimeReturnC = wx.TextCtrl(panel, -1, "")

         # * ROW FIVE *

        CardNumS = wx.StaticText(panel, -1, u"卡号")
        CardNumC = wx.StaticText(panel, -1, "")
        CardNumC.SetForegroundColour('red')


        CompanyNameS = wx.StaticText(panel, -1, "Designed by W2 in Solna",
                                    style =  wx.LEFT)
        

        sizer.Add(CustomerS, 0, wx.ALL | wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(CustomerC, 0, wx.ALL | wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(Dummy, 0, wx.ALL, border = BORDER )
        sizer.Add(Dummy2, 0, wx.ALL, border = BORDER )

        sizer.Add(CustomerNumS, 0, wx.ALL | wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(CustomerNumC, 0, wx.ALL  | wx.EXPAND | wx.ALIGN_CENTER, border = 45 )


        sizer.Add(CarNumS, 0, wx.ALL | wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(CarNumC, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, border = 45  )
        
        sizer.Add(TimeRentS, 0, wx.ALL| wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(TimeRentC, 0, wx.ALL  | wx.EXPAND | wx.ALIGN_CENTER, border = 45  )

        sizer.Add(TimeReturnS, 0, wx.ALL| wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(TimeReturnC, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, border = 45  )

        sizer.Add(CardNumS, 0, wx.ALL| wx.ALIGN_CENTER, border = BORDER )
        sizer.Add(CardNumC, 0, wx.ALL  | wx.EXPAND | wx.ALIGN_CENTER, border = 45  )

        sizer.Add(CompanyNameS, 0, wx.ALL| wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, border = BORDER )

        mainsizer.Add(sizer,4, wx.ALL| wx.ALIGN_CENTER, 0)

        panel.SetSizer(mainsizer)

        panel.Fit()

        self.Center()

        self.DisplayObjs = [CustomerS,CustomerNumS,CarNumS,TimeRentS,
                            CustomerC,TimeReturnS, CardNumS]
                            
        for m in self.DisplayObjs:
            m.SetFont(wx.Font(45, wx.SWISS, wx.NORMAL, wx.BOLD))
            m.SetBackgroundColour(wx.Colour(246,247,248))
            m.SetForegroundColour(wx.Colour(76,103,161))

            
        self.MOs={'cuid' : CustomerNumC,
                  'carid': CarNumC,
                  'rent': TimeRentC,
                  'return' : TimeReturnC,
                  'cardid': CardNumC,
                  'cutext':CustomerC
                  }

        for (k,v) in self.MOs.items():
            if not v == CustomerC:
                
                v.SetFont(wx.Font(45, wx.SWISS, wx.NORMAL, wx.BOLD))

            


        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        dbserver = car2goDB.server(DBServerUrl)
        self.dbtab_card = dbserver[CardDB]
        self.dbtab_customer = dbserver[CustomerDB]
        self.dbtab_rent = dbserver[RentDB]
        self.MOs['cuid'].Bind(wx.EVT_CHAR_HOOK, self.OnCustomerIdInput)

        CustomerC.SetFocus()
        self.shutdown = False

        self.Layout()
        self.Bind(EVT_CARD_INSERT, self.OnCardInsert)
        self.stateinit() 


    def onKey(self,event):
        key = event.GetKeyCode()
        event.Skip()
        if key == wx.WXK_ESCAPE:
            self.close_me()

        if key == 315: #simulate a card inseart
            print "keycode 315"
            self.sevent("cardin")            
        else:
            print "when %s" %(self.GetState())
            self.sevent(key)
            event.Skip()


    def OnCustomerIdInput(self,event):
        if debug: print "OnCustomerIdInput"
        key = event.GetKeyCode()

        if (key == wx.WXK_RETURN or key == wx.WXK_NUMPAD_ENTER
            or key == 370):
            print key
            self.sevent('CustomerId_Return')
        else:
            event.Skip()

    def onDialogKey(self,event):
        if debug: print "In onDialogKey"
        key = event.GetKeyCode()

        if (key == wx.WXK_NUMPAD_ADD or key == wx.WXK_INSERT):
            self.dialog.EndModal(wx.ID_CANCEL)
        elif (key == wx.WXK_RETURN or key == wx.WXK_NUMPAD_ENTER):#13: enter
            self.dialog.EndModal(wx.ID_OK)    
        else: #todo: shall handle the other key press??
            self.dialog.EndModal(wx.ID_CANCEL)    

    #### Following are about state machine
    def stateinit(self):#init state machine
        self.rf_reader_online = None
        self.bg_wait_for_card()
        for (k,o) in self.MOs.items():
            if k != 'cardid' and k != 'cutext':
                o.SetEditable(False)
                o.SetValue("")
        self.SetState("IDLE")
        self.MOs['cardid'].SetLabel(u"无卡")
        self.MOs['cutext'].SetLabel(u"")

       
    def SetState(self,State):
        if State in ALLOWSTATES: #Ensure states are under control
            self.__state = State
        else:
            raise StateError(State)

    def GetState(self):
        return self.__state

    def OnCardInsert(self,evt):
        if debug: print "OnCardInsert"
        self.sevent('cardin')

    def get_carddata(self):
        self.rf = CarToGoRF('\xff\xff\xff\xff\xff\xff')
        reader = self.rf
        CardId = -1
    
        while (CardId == -1 or CardId == "00000000") and not self.shutdown:
            sleep(0.1)
            (CardId, Data) = reader.readhex('\xff\xff\xff\xff\xff\xff',4,1)
            print CardId,Data
            if CardId == -1 and Data == "00" and self.rf_reader_online != False:
                self.MOs['cardid'].SetLabel(u"读卡器未连接")
                self.rf_reader_online = False
            else:
                self.rf_reader_online = True
                if CardId == -1 and Data == "83":
                    self.MOs['cardid'].SetLabel(u"无卡")
            
                
        self.MOs['cardid'].SetLabel(CardId)
        evt = wxCardInsert()
        wx.PostEvent(self, evt)
        self.CurrentCard = CardId
        return Data

    def bg_wait_for_card(self):
        thread = threading.Thread(target=self.get_carddata)
        thread.setDaemon(True)
        thread.start()
        self.bg = thread

    def show_info_dialog(self,Msg):
        #just popup a info window do not check user selection
        self.dialog = wx.MessageDialog(self, Msg, "cartogo", wx.OK)
        self.dialog.ShowModal()
        self.dialog.Destroy()

    def close_me(self):
        self.shutdown = True
        self.bg.join()
        self.Close()
               
    ###-----------------------    
    ### State machine:
    ###
    def sevent(self,Evt):
##        try :
##            self.do_sevent(Evt)
##        except Exception as e:
##            print "Oops! Error found !!"
##            print   e.args
##            self.stateinit()
        self.do_sevent(Evt)
    def do_sevent(self,Evt): # Evt: rfreader event| keyboard event 
        State = self.GetState()
        if debug: print"sevent: state: -> %s,Evt -> %s " %  (State,Evt)
        if self.GetState() == "IDLE" and Evt == 'cardin': 
            if debug: print "SIM: card inserted"
            self.action_card_inserted()

            

        elif State == "CARDIN" and (Evt == wx.WXK_NUMPAD_ADD or Evt == wx.WXK_INSERT): 
            if debug: print "ask if reg"
            self.dialog = wx.TextEntryDialog(None,u"是否注册卡?", "reg?")
            self.dialog.Bind(wx.EVT_CHAR_HOOK, self.onDialogKey)
            result = self.dialog.ShowModal()
            self.dialog.Destroy()
            self.SetState("DIALOGIFREG")
            self.sevent(result)

        elif State == "CARDIN" and Evt == 'CustomerId_Return':
            if debug: print "Get&Display Customer name."
            id = self.MOs['cuid'].GetValue()
            if id == "":
                self.show_info_dialog(u"客户号不能为空")
                self.stateinit()
                return
            carid = self.MOs['carid'].GetValue()
            if carid == 0:
                self.show_info_dialog(u"空卡请先注册！")

            CUText = self.db_cid_to_cname(id)
            self.dialog = wx.TextEntryDialog(None,u"%s公司租车 ?" % (CUText), "rent car now?")
            self.dialog.Bind(wx.EVT_CHAR_HOOK, self.onDialogKey)

            Choice = self.dialog.ShowModal()
            self.dialog.Destroy()

            if wx.ID_OK == Choice :
                Rf = self.action_rent_car()
                
                self.show_info_dialog(u"%s公司于%s租车成功，请取卡！" % (CUText,format_datetime(Rf.borrowtag)))
                self.wait_for_remove_card(Rf.cardid)
            else:
                self.show_info_dialog(u"租车已取消！")         
            self.stateinit()

        elif State == "DIALOGIFREG" and Evt == wx.ID_CANCEL:
            if debug: print "user cancel reg"
            self.SetState("IDLE")
            self.stateinit()
            
        elif State == "DIALOGIFREG" and (Evt == wx.ID_OK):
            if debug: print "start password dialog "

            self.dialog = wx.PasswordEntryDialog(None,u"请输入注册卡密码", "cartogo: query pwd")
            self.dialog.ShowModal()
            result = self.dialog.GetValue()
            self.dialog.Destroy()
            if debug: print "password is %s" % (result)
            
            
            if verify_password_ok(result) :
                if debug: print "verify password success!"
                self.SetState("PASSWORDOK")
                self.MOs['carid'].SetValue("")
                self.MOs['carid'].SetEditable(True)
                self.MOs['carid'].SetFocus()
            else:
                self.SetState("IDLE")
                if debug: print "verify password fail!"
                self.show_info_dialog(u"密码错误")
                self.stateinit()

        elif State == "PASSWORDOK" and (Evt == wx.WXK_RETURN or Evt == wx.WXK_NUMPAD_ENTER):
            self.MOs['carid'].SetEditable(False)
            
            if self.reg_card_with_carnum():
                self.SetState("IDLE")

                self.dialog = wx.MessageDialog(self,u"卡注册成功", "cartogo", wx.OK)
                result = self.dialog.ShowModal()
                self.dialog.Destroy()
                

            else: #todo: handle erro when rfreader throw err or return error
                pass
            self.stateinit()
        else:
            if debug: print "Error: unsupported state /evt"
            pass
    
    ###-----------------------    
    ### State machine actions:
    ###    
    def action_card_inserted(self):
        (res,Rf) = self.rf.get()
        self.rf.beep(1,1)

        if res != -1:
            self.MOs['carid'].SetValue(str(Rf.carid))
            if Rf.borrowtag == 0:
                if debug: print "set focus of CustomerNumC"  
                self.MOs['cuid'].SetEditable(True)
                self.MOs['cuid'].SetFocus()
                self.SetState("CARDIN")

            else:
                if debug: print "borrowtag:"+str(Rf.borrowtag)
                renttime = datetime.fromtimestamp(Rf.borrowtag).strftime(TIMEFMT)
                self.MOs['rent'].SetValue(renttime)
                CUText = self.db_cid_to_cname(Rf.clientid)
                self.dialog = wx.TextEntryDialog(None,u"%s公司现在还车?" % (CUText) , "return car now?")
                self.dialog.Bind(wx.EVT_CHAR_HOOK, self.onDialogKey)
                select = self.dialog.ShowModal()
                self.dialog.Destroy()
                if wx.ID_OK == select:
                    #todo
                    self.action_return_car(Rf)
                
                self.stateinit()
        else:
             if debug: print "action_card_inserted get " + str(res)

    def action_rent_car(self):
        if debug: print "action_rent_car"
        RentTime = time()
        Client = int(self.MOs['cuid'].GetValue())        
        #todo
        (ret,rf) = CarToGoRF().get()
        if ret != -1:
            rf.clientid = Client
            rf.borrowtag = RentTime
            rf.update()
            self.db_rentcar(rf)
            self.rf.beep(beepf,beepd)
            return rf 
        else:
            raise Exception(('action_rent_car_fail',ret))

    def db_rentcar(self, rf):
        doc = RentDoc(id = key_rent(rf),
                     CardId = rf.cardid,
                     Client = self.db_cid_to_cname(rf.clientid),
                     Rent = format_datetime(rf.borrowtag))
        doc.store(self.dbtab_rent)

    def action_return_car(self,Rf):
        now = time()
        returntime = datetime.fromtimestamp(now).strftime(TIMEFMT)
        self.MOs['return'].SetValue(returntime)
        self.rf.beep(beepf,beepd)
        CUText = self.db_cid_to_cname(Rf.clientid)
        self.MOs['cutext'].SetLabel(CUText)

        self.db_return_car(Rf,now)

        if 0 != CarToGoRF().reset():
            raise Exception('action_return_car_fail')

        self.show_info_dialog(u"%s公司，客户号:%s 于 %s 还车成功，请取卡！" %(CUText,str(Rf.clientid),returntime))
        
        self.wait_for_remove_card(Rf.cardid)
        #todo
        #write_to_db

    def db_return_car(self,rf,time):
        #query doc with key
        doc = RentDoc.load(self.dbtab_rent, key_rent(rf))

        if doc:
            doc.Return = format_datetime(time)
            doc.store(self.dbtab_rent)
            return 0
        else:
            #todo handle case if we didn't get the rental record
            return -1

    def wait_for_remove_card(self,current):
        CardId = current
        while CardId == current:
            sleep(0.2)
            reader = CarToGoRF(DEF_PWD)        
            (CardId, Data) = reader.readhex(DEF_PWD,4,1)
        if debug: print "card %s removed" % (current)

    def reg_card_with_carnum(self):
        #cardnum = 
        #if debug: print "reg card num: %s car num: %s" % (cardnum,carnum)

        RfCardId = self.CurrentCard
        carnum = self.MOs['carid'].GetValue()
        doc = CardDoc.load(self.dbtab_card, str(RfCardId))
        if doc:
            doc.CarId = str(carnum)
        else:
            doc = CardDoc(id = RfCardId, CarId = str(carnum))
        doc.time =  format_datetime(time())
        doc.store(self.dbtab_card)

        rf = CarToGoRF(pwd=DEF_PWD,carid=self.MOs['carid'].GetValue())
        rf.beep(beepf,2) #todo: shall not beep in state machine
        rf.update()
        return True
    
    def db_cid_to_cname(self,id):
        #todo what if name is not found?
        r = CustomerDoc.load(self.dbtab_customer,str(id))
        if None == r:
            return ""
        else:
            return r['name']

def verify_password_ok(rawtext):
    if rawtext=="11":
        return True
    else:
        return False


class cartogoApp(wx.App):
    def __init__(self, redirect=False, filename=None,
                 useBestVisual=False,clearSigInt=True):
        wx.App.__init__(self,redirect,filename,useBestVisual,clearSigInt)
    
    def OnInit(self):
        return True

def get_screen_resolution():
    user32 = ctypes.windll.user32
    Res = (user32.GetSystemMetrics(0),user32.GetSystemMetrics(1))
    print "Screen: W:%d H:%d" % Res

def  pixel_to_pointer(pix):
    return pix * 0.75

def format_datetime(TimeTag):
    return datetime.fromtimestamp(TimeTag).strftime(TIMEFMT)

def key_rent(rf):
    print format_datetime(rf.borrowtag)
    res = rf.cardid + str(rf.borrowtag)
    if debug: print res
    return res
 


if __name__ == '__main__':
    print "Welcome to cartogoApp"
    Size = get_screen_resolution()
    app = cartogoApp()
    
    frame = MainFrame((1024,768))
    frame.Show(True)
    app.MainLoop()

    

