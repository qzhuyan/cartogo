#!/usr/bin/python
# coding=utf-8

import wx
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="Car To Go",size=(800,600))
        
        panel=wx.Panel(self)

        TopLB = wx.StaticText(panel, -1, "Car to Go")        
        TopLB.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # #left top: customer
        CustomerS = wx.StaticText(panel, -1, "Customer")
        CustomerC = wx.TextCtrl(panel, -1, "",size=(200,-1))

        CustomerNumS = wx.StaticText(panel, -1, "Customer number")
        CustomerNumC = wx.TextCtrl(panel, -1, "",size=(150,-1))

        CarNumS = wx.StaticText(panel, -1, "Car number")
        CarNumC = wx.TextCtrl(panel, -1, "",size=(150,-1))

        TimeRentS = wx.StaticText(panel, -1, "Rent: ")
        TimeRentC = wx.TextCtrl(panel, -1, "",size=(150,-1))
        TimeReturnS = wx.StaticText(panel, -1, "Return: ")
        TimeReturnC = wx.TextCtrl(panel, -1, "",size=(150,-1))

        # Main Sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)        
        mainsizer.Add(TopLB,0,wx.ALL,5)
        mainsizer.Add(wx.StaticLine(panel),0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)


        ParmSizer = wx.BoxSizer(wx.VERTICAL)

        ParmL1 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL1.Add(CustomerS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL1.AddSpacer((75,10))
        ParmL1.Add(CustomerC, 0,wx.EXPAND|wx.ALIGN_RIGHT)

        ParmL2 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL2.Add(CustomerNumS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL2.AddSpacer(20)
        ParmL2.Add(CustomerNumC,wx.EXPAND)
        ParmL2.AddSpacer(20)
        ParmL2.Add(CarNumS, 0,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL2.AddSpacer(20)
        ParmL2.Add(CarNumC,wx.EXPAND)

        ParmL3 = wx.BoxSizer(wx.HORIZONTAL)
        ParmL3.Add(TimeRentS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer(20)
        ParmL3.Add(TimeRentC, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer(20)
        ParmL3.Add(TimeReturnS, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmL3.AddSpacer(20)
        ParmL3.Add(TimeReturnC, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL,border=10)

        ParmSizer.Add(ParmL1, 0,wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmSizer.AddSpacer(20)
        ParmSizer.Add(ParmL2, 0,wx.ALIGN_CENTER_VERTICAL,border=10)
        ParmSizer.AddSpacer(20)
        ParmSizer.Add(ParmL3, 0,wx.ALIGN_CENTER_VERTICAL,border=10)

        mainsizer.Add(ParmSizer, 0, wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(mainsizer)

        self.Center()
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)

        
        

class cartogoApp(wx.App):
    def __init__(self, redirect=False, filename=None,
                 useBestVisual=False,clearSigInt=True):
        wx.App.__init__(self,redirect,filename,useBestVisual,clearSigInt)
    
    def OnInit(self):
        return True

if __name__ == '__main__':
    app = cartogoApp()
    frame = MainFrame()
    frame.Show(True)
    app.MainLoop()

                 

