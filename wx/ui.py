#!/usr/bin/python
# coding=utf-8

import wx

from RfCard import *
from time import sleep
from time import time
from datetime import datetime
import threading
from wx.lib.newevent import NewEvent
 
debug=True

wxCardInsert, EVT_CARD_INSERT= NewEvent()

ALLOWSTATES="IDLE CARDIN DIALOGIFREG PASSWORDOK".split()

TIMEFMT = '%Y-%m-%d %H:%M:%S'

DEF_PWD = '\xff\xff\xff\xff\xff\xff'

beepf = 10
beepd = 2

class StateError(Exception):
    def __init__(self,State):
        self.value=State
    def __str__(self):
        repr(self.value)

class MainFrame(wx.Frame):
    def __init__(self,size):
        wx.Frame.__init__(self, None, id=-1, title="Car To Go",size=size,style=wx.STAY_ON_TOP)
        panel=wx.Panel(self)
        self.shutdown = False
        panel.SetBackgroundColour(wx.Colour(192, 222, 237))
        self.rf = CarToGoRF()
    
        TopLB = wx.StaticText(panel, -1, u"租借登记系统")        
        TopLB.SetFont(wx.Font(28, wx.SWISS, wx.NORMAL, wx.BOLD))
        

        # #left top: customer
        CustomerS = wx.StaticText(panel, -1, u"客户名称")

        #CustomerC = wx.TextCtrl(panel, -1, "",size=(200,-1))
        CustomerC = wx.StaticText(panel, -1, "")
        CustomerNumS = wx.StaticText(panel, -1, u"客户号")
     

        CustomerNumC = wx.TextCtrl(panel, -1, "",size=(150,-1))
        CustomerNumC.SetEditable(False)

        CarNumS = wx.StaticText(panel, -1, u"车号")
        CarNumC = wx.TextCtrl(panel, -1, "",size=(150,-1))

        TimeRentS = wx.StaticText(panel, -1, u"租车时间")
        TimeRentC = wx.TextCtrl(panel, -1, "",size=(150,-1))
        TimeReturnS = wx.StaticText(panel, -1, u"还车时间")
        TimeReturnC = wx.TextCtrl(panel, -1, "",size=(150,-1))

        CardNumS = wx.StaticText(panel, -1, u"卡号")
        CardNumC = wx.StaticText(panel, -1, "", size=(150,-1))
        CardNumC.SetForegroundColour('red')


        CompanyNameS = wx.StaticText(panel, -1, "Designed by W2 in Solna",style=wx.ALIGN_RIGHT)
        CompanyNameS.SetFont(wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        
        self.MOs={'cuid' : CustomerNumC,
                  'carid': CarNumC,
                  'rent': TimeRentC,
                  'return' : TimeReturnC,
                  'cardid': CardNumC
                  }

        self.DisplayObjs = [CustomerS,CustomerNumS,CarNumS,TimeRentS,
                            TimeReturnS, CardNumS 
                            ]
        
##        for (k,m) in self.MOs.items():
##            m.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL))
##            m.SetBackgroundColour('white')
##            m.SetForegroundColour('red')
##        for m in self.DisplayObjs:
##            m.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL))
##            m.SetBackgroundColour(wx.Colour(192, 222, 237))
##            m.SetForegroundColour('black')
        

        # Main Sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)        
        mainsizer.Add(TopLB,0,wx.ALL,5)
        mainsizer.Add(wx.StaticLine(panel),0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)

        ParmSizer = wx.BoxSizer(wx.VERTICAL)

        ParmL1 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL1.Add(CustomerS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL1.AddSpacer((100,10))
        ParmL1.Add(CustomerC, 0,wx.EXPAND|wx.ALIGN_RIGHT)

        ParmL2 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL2.Add(CustomerNumS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL2.AddSpacer((60,20))
        ParmL2.Add(CustomerNumC,wx.EXPAND)
        ParmL2.AddSpacer((50,10))
        ParmL2.Add(CarNumS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL2.AddSpacer((40,10))
        ParmL2.Add(CarNumC,wx.EXPAND)

        ParmL3 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL3.Add(TimeRentS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer((50,40))
        ParmL3.Add(TimeRentC, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer(20)
        ParmL3.Add(TimeReturnS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer(45)
        ParmL3.Add(TimeReturnC, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)

        ParmL4 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL4.Add(CardNumS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL4.AddSpacer(20)
        ParmL4.Add(CardNumC, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL4.AddSpacer((150,20))
        ParmL4.Add(CompanyNameS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL4.AddSpacer(20)

        ParmSizer.Add(ParmL1, 0,wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmSizer.AddSpacer(20)
        ParmSizer.Add(ParmL2, 0,wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmSizer.AddSpacer(20)
        ParmSizer.Add(ParmL3, 0,wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmSizer.AddSpacer(20)
        ParmSizer.Add(ParmL4, 0,wx.ALIGN_CENTER_VERTICAL,border=10)

        mainsizer.Add(ParmSizer, 0, wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(mainsizer)

        self.Center()

        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        self.MOs['cuid'].Bind(wx.EVT_CHAR_HOOK, self.OnCustomerIdInput)
        #self.ShowFullScreen(True)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)

        style = self.GetWindowStyle()
        # stay on top
        self.SetWindowStyle( style | wx.STAY_ON_TOP )
        # normal behaviour again
        self.SetWindowStyle( style )

        CustomerC.SetFocus()
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
        self.bg_wait_for_card()
        for (k,o) in self.MOs.items():
            if k != 'cardid':
                o.SetEditable(False)
                o.SetValue("")
        self.SetState("IDLE")
        self.MOs['cardid'].SetLabel(u"无卡")

       
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
    
        while CardId == -1 and not self.shutdown:
            sleep(0.1)
            (CardId, Data) = reader.readhex('\xff\xff\xff\xff\xff\xff',4,1)
            print Data
        self.MOs['cardid'].SetLabel(CardId)
        evt = wxCardInsert()
        wx.PostEvent(self, evt)
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
        try :
            self.do_sevent(Evt)
        except Exception as e:
            print "Oops! Error found !!"
            print   e.args
            self.stateinit()
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

            CUText = db_query_customer(id)
            self.dialog = wx.TextEntryDialog(None,u"是否现在租车给 %s ?" % (CUText), "rent car now?")
            self.dialog.Bind(wx.EVT_CHAR_HOOK, self.onDialogKey)
            if wx.ID_OK == self.dialog.ShowModal():
                Rf = self.action_rent_car()
            self.dialog.Destroy()
            self.show_info_dialog(u"租车成功，请取卡！")
            self.wait_for_remove_card(Rf.cardid)
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
            
            if self.reg_card_with_carnum(self.MOs['carid'].GetValue()):
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
                self.dialog = wx.TextEntryDialog(None,u"是否现在还车?" , "return car now?")
                self.dialog.Bind(wx.EVT_CHAR_HOOK, self.onDialogKey)
                select = self.dialog.ShowModal()
                self.dialog.Destroy()
                if wx.ID_OK == select:
                    #todo
                    self.action_return_car(Rf)
                
                self.stateinit()
        else:
             if debug: print "action_card_inserted get " + res

    def action_rent_car(self):
        if debug: print "action_rent_car"
        #todo
        (ret,rf) = CarToGoRF().get()
        if ret != -1:
            rf.borrowtag = time()
            rf.update()
            self.rf.beep(beepf,beepd)

            return rf 
        else:
            raise Exception(('action_rent_car_fail',ret))
        

    def action_return_car(self,Rf):
        self.MOs['return'].SetValue(datetime.fromtimestamp(time()).strftime(TIMEFMT))
        if 0 != CarToGoRF().reset():
            raise Exception('action_return_car_fail')
        self.rf.beep(beepf,beepd)
        self.show_info_dialog(u"还车成功，请取卡！")
        self.wait_for_remove_card(Rf.cardid)
        #todo
        #write_to_db

    def wait_for_remove_card(self,current):
        CardId = current
        while CardId == current:
            sleep(0.2)
            reader = CarToGoRF(DEF_PWD)        
            (CardId, Data) = reader.readhex(DEF_PWD,4,1)
        if debug: print "card %s removed" % (current)

    def reg_card_with_carnum(self, carnum):
        #cardnum = 
        #if debug: print "reg card num: %s car num: %s" % (cardnum,carnum)
        ##todo call rfreader class
        rf = CarToGoRF(pwd=DEF_PWD,carid=carnum)
        rf.beep(beepf,2) #todo: shall not beep in state machine

        rf.update()
        return True


   

def verify_password_ok(rawtext):
    if rawtext=="11":
        return True
    else:
        return False



def db_query_customer(id):
    #todo
    return "China Mobile"

class cartogoApp(wx.App):
    def __init__(self, redirect=False, filename=None,
                 useBestVisual=False,clearSigInt=True):
        wx.App.__init__(self,redirect,filename,useBestVisual,clearSigInt)
    
    def OnInit(self):
        return True

if __name__ == '__main__':
    print "Welcome to cartogoApp"
    app = cartogoApp()
    frame = MainFrame((800,600))
    frame.Show(True)
    app.MainLoop()

                 

