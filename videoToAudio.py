import os
import wx
from moviepy.editor import VideoFileClip

class Mp4ToMp3Converter(wx.Frame):
    def __init__(self, parent, title):
        super(Mp4ToMp3Converter, self).__init__(parent, title=title, size=(400, 200))

        panel = wx.Panel(self)
        self.selected_file = ""
        
        # File Selection Button
        select_file_button = wx.Button(panel, label="Select MP4 File")
        select_file_button.Bind(wx.EVT_BUTTON, self.on_select_file)

        # Selected File Label
        self.selected_file_label = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.selected_file_label.Hide()

        # Convert Button
        convert_button = wx.Button(panel, label="Convert to MP3")
        convert_button.Bind(wx.EVT_BUTTON, self.on_convert)

        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(select_file_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.selected_file_label, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(convert_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.Center()

    def on_select_file(self, event):
        dlg = wx.FileDialog(self, "Select MP4 File", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.selected_file = dlg.GetPath()
            self.selected_file_label.SetLabel(f"Selected File: {os.path.basename(self.selected_file)}")
            self.selected_file_label.Show()
        dlg.Destroy()

    def on_convert(self, event):
        if not self.selected_file:
            wx.MessageBox("Please select an MP4 file.", "Error", wx.OK | wx.ICON_ERROR)
            return

        output_folder = os.path.expanduser("~/Documents/MP3Output")  # Output folder in Documents
        os.makedirs(output_folder, exist_ok=True)

        mp4_file = VideoFileClip(self.selected_file)
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(self.selected_file))[0] + ".mp3")

        mp4_file.audio.write_audiofile(output_path)
        wx.MessageBox(f"MP4 file converted to MP3 and saved at: {output_path}", "Conversion Complete", wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    frame = Mp4ToMp3Converter(None, "MP4 to MP3 Converter")
    frame.Show()
    app.MainLoop()
