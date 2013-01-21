# -*- coding: utf-8 -*-
import wx
from douban_client import DoubanClient
import httplib2
from urllib import urlencode
import json

save_path = "image"
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
    #查询图书，返回书籍列表
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
        #查询书籍信息
        book = self.search_book(self.book_name.GetValue(),0,0)
        if len(book) == 0:
            self.show.SetLabel(u"\n暂无结果╮(╯▽╰)╭")
        else:
            #wx.MessageBox('Result:'+book[0]["title"],'wxPython',wx.OK)
            str1 = ''
            for i in range(len(book)):
                str1 += ("\n" + str(i+1) +
                         u": 标题： " + book[i]["title"] +
                         u"\n作者： " + book[i]["author"][0] +
                         u"\n作者简介： "+ book[i]["author_intro"] +
                         u"\n简介： " + book[i]["summary"])
                #=========================
                self.get_image(book[i]["images"]["small"],save_path)
                #str1 = str1 + "\n" + (str(i+1) + u" 标题: " + str(book[i]["title"]))# + 
                    
   #                "\n作者" + str(book[0]["author"]) +
   #                 "\n\n作者简介: "+ str(book[i]["author_intro"]) +
    #                "\n\n简介: " + str(book[i]["summary"]))
            #str2 = unicode(str1, "utf-8")
            self.show.SetLabel(str1)
            #self.show.SetLabel(self.book_name.GetValue())
            #self.buttonOk.SetLabel('123')
    #下载图片
    def get_image(self,fileurl, save_path):
        img = urllib2.urlopen(fileurl).read()
        filename = save_path+"\\img.jpg"
        if os.path.exists(filename):
            output = open(filename,'wb+')
            output.write(img)
            output.close()
        else:
            output = open(filename, "wb")
            output.write(img)
            output.close()
        imgdata = wx.Image(filename, wx_BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(imgdata))
        fgs = wx.FlexGridSizer(cols=2,hgap=10,vgap=10)
        fgs.Add(sb)
        self.panel.SetSizerAndFit(fgs)
        self.frame.Fit()
    
app = MyApp()
app.MainLoop()
