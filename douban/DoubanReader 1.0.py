# -*- coding: utf-8 -*-
import wx
from douban_client import DoubanClient
import httplib2
from urllib import urlencode
import json

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent = None, title = 'Douban Reader', size=(480,600))
        
        panel = wx.Panel(frame, -1)
        top = wx.StaticText(panel, -1, 'Douban Reader',
                              style = wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL,
                              size = (480,50))
        top.SetForegroundColour('white')
        top.SetBackgroundColour('grey')
        
        self.book_name = wx.TextCtrl(panel, -1,u"请输入需要查询的书籍名", pos = (10,60), size = (350,20))
        self.buttonOk = wx.Button(panel, -1, 'search', pos = (370,60))
#        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOk)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOk)
        self.show = wx.StaticText(panel, -1, '====================================',
                                  style = wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL,
                                  size = (480,500),
                                  pos = (0,90))
        self.show = wx.StaticText(panel, -1, '',                                 
                                  size = (460,500),
                                  style = wx.TE_WORDWRAP,
                                  pos = (5,100))
        self.show.SetForegroundColour('grey')
        font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
        self.show.SetFont(font)
        frame.Show()
        return True
    #查询图书
    def search_book(self,book,start,count):
        #book = u"白夜行"
        h = httplib2.Http()
        start = "0"
        count = "5"
        url_search = "https://api.douban.com/v2/book/search"+"?q="+book+"&start="+start+"&count="+count
        resp, content = h.request(url_search,"GET")
        #print resp
        s = json.loads(content,encoding="utf-8")
        #print s['books']
        #wx.MessageBox('Books:'+str(len(s['books'])),'wxPython',wx.OK)
        return s['books']
    
    #查询按钮
    def OnButtonOK(self,event):
        #wx.MessageBox('You input:'+self.book_name.GetValue(),'wxPython',wx.OK)
        book = self.search_book(self.book_name.GetValue(),0,0)
        if len(book) == 0:
            self.show.SetLabel(u"暂无结果╮(╯▽╰)╭")
        else:
        #show = book["books"][0]["title"]
            str1 = ''
            for i in range(len(book)):               
                str1 = str1 + "\n" + (str(i+1) + u" 标题: " + str(book[i]["title"]))# + 
                    
   #                "\n作者" + str(book[0]["author"]) +
   #                 "\n\n作者简介: "+ str(book[i]["author_intro"]) +
    #                "\n\n简介: " + str(book[i]["summary"]))
            #str2 = unicode(str1, "utf-8")
            self.show.SetLabel(str1)
            #self.show.SetLabel(self.book_name.GetValue())
            #self.buttonOk.SetLabel('123')  
    
app = MyApp()
app.MainLoop()
