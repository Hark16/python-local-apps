import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        text = wx.StaticText(panel, label="Hello, wxPython!", pos=(10, 10))
        button = wx.Button(panel, label="Click Me!", pos=(10, 40))

        self.Bind(wx.EVT_BUTTON, self.on_button_click, button)

        self.Show(True)

    def on_button_click(self, event):
        wx.MessageBox("Button Clicked!")

app = wx.App()
frame = MyFrame(None, "My wxPython App")
app.MainLoop()
