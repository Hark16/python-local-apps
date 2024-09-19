import os
import wx
import moviepy.editor as mp
import datetime

class VideoCutter(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 250))
        
        self.panel = wx.Panel(self)
        
        self.video_file_label = wx.StaticText(self.panel, label="Video File:")
        self.video_file_text = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.browse_button = wx.Button(self.panel, label="Browse")
        self.start_time_label = wx.StaticText(self.panel, label="Start Time (seconds):")
        self.start_time_text = wx.TextCtrl(self.panel)
        self.end_time_label = wx.StaticText(self.panel, label="End Time (seconds):")
        self.end_time_text = wx.TextCtrl(self.panel)
        self.cut_button = wx.Button(self.panel, label="Cut Video")
        
        self.Bind(wx.EVT_BUTTON, self.on_browse, self.browse_button)
        self.Bind(wx.EVT_BUTTON, self.on_cut, self.cut_button)
        
        self.setup_layout()
        
    def setup_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(self.video_file_label, 1, wx.EXPAND)
        file_sizer.Add(self.video_file_text, 5, wx.EXPAND)
        file_sizer.Add(self.browse_button, 1, wx.EXPAND)
        
        start_end_sizer = wx.BoxSizer(wx.HORIZONTAL)
        start_end_sizer.Add(self.start_time_label, 1, wx.EXPAND)
        start_end_sizer.Add(self.start_time_text, 2, wx.EXPAND)
        start_end_sizer.Add(self.end_time_label, 1, wx.EXPAND)
        start_end_sizer.Add(self.end_time_text, 2, wx.EXPAND)
        
        sizer.Add(file_sizer, 1, wx.EXPAND)
        sizer.Add(start_end_sizer, 1, wx.EXPAND)
        sizer.Add(self.cut_button, 1, wx.EXPAND)
        
        self.panel.SetSizerAndFit(sizer)
        
    def on_browse(self, event):
        file_dialog = wx.FileDialog(self, "Choose a video file", "", "", "Video Files (*.mp4)|*.mp4", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if file_dialog.ShowModal() == wx.ID_OK:
            video_path = file_dialog.GetPath()
            self.video_file_text.SetValue(video_path)
            video = mp.VideoFileClip(video_path)
            full_duration = video.duration
            wx.MessageBox(f"Video duration: {full_duration:.2f} seconds", "Video Information", wx.OK | wx.ICON_INFORMATION)
        file_dialog.Destroy()
        
    def on_cut(self, event):
        video_path = self.video_file_text.GetValue()
        start_time = float(self.start_time_text.GetValue())
        end_time = float(self.end_time_text.GetValue())
        
        if not video_path:
            wx.MessageBox("Please select a video file.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            try:
                video = mp.VideoFileClip(video_path)
                cut_video = video.subclip(start_time, end_time)
                
                # Extract the original video file's name without the extension
                video_filename = os.path.splitext(os.path.basename(video_path))[0]

                # Create the output folder in the Documents directory if it doesn't exist
                output_folder = os.path.expanduser('~/Documents/output_videoclip')
                os.makedirs(output_folder, exist_ok=True)

                # Construct the output filename with "clip" added
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%d-%m-%Y-%H-%M-%S")
                date_time_string = formatted_datetime
                output_filename = video_filename + date_time_string + '.mp4'
                output_path = os.path.join(output_folder, output_filename)

                cut_video.write_videofile(output_path, codec="libx264")
                wx.MessageBox(f"Video cut successfully. Output saved as '{output_filename}'", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = VideoCutter(None, -1, 'Video Cutter')
    frame.Show()
    app.MainLoop()
