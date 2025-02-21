import wx
import wx.stc as stc

class Notepad(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Notepad", size=(600, 400))
        
        self.panel = wx.Panel(self)
        self.text_area = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        
        self.create_menu_bar()
        self.create_dark_mode()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_area, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        self.Show()
    
    def create_menu_bar(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        edit_menu = wx.Menu()
        view_menu = wx.Menu()
        
        open_item = file_menu.Append(wx.ID_OPEN, "&Open", "Open a file")
        save_item = file_menu.Append(wx.ID_SAVE, "&Save", "Save the file")
        exit_item = file_menu.Append(wx.ID_EXIT, "&Exit", "Exit application")
        
        find_replace_item = edit_menu.Append(wx.ID_FIND, "&Find & Replace", "Find and replace text")
        dark_mode_item = view_menu.Append(wx.ID_ANY, "&Dark Mode", "Toggle Dark Mode")
        
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(edit_menu, "&Edit")
        menu_bar.Append(view_menu, "&View")
        self.SetMenuBar(menu_bar)
        
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_find_replace, find_replace_item)
        self.Bind(wx.EVT_MENU, self.toggle_dark_mode, dark_mode_item)
    
    def create_dark_mode(self):
        self.dark_mode = False
        self.update_theme()
    
    def toggle_dark_mode(self, event):
        self.dark_mode = not self.dark_mode
        self.update_theme()
    
    def update_theme(self):
        if self.dark_mode:
            self.panel.SetBackgroundColour(wx.Colour(30, 30, 30))
            self.text_area.SetBackgroundColour(wx.Colour(50, 50, 50))
            self.text_area.SetForegroundColour(wx.Colour(255, 255, 255))
        else:
            self.panel.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.text_area.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.text_area.SetForegroundColour(wx.Colour(0, 0, 0))
        self.panel.Refresh()
    
    def on_open(self, event):
        with wx.FileDialog(self, "Open file", wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*", 
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                file_path = dialog.GetPath()
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.SetValue(file.read())
    
    def on_save(self, event):
        with wx.FileDialog(self, "Save file", wildcard="Text files (*.txt)|*.txt", 
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                file_path = dialog.GetPath()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.GetValue())
    
    def on_exit(self, event):
        self.Close()
    
    def on_find_replace(self, event):
        find_replace_dialog = wx.TextEntryDialog(self, "Enter text to find and replace (format: find_text,replacement_text)", "Find & Replace")
        if find_replace_dialog.ShowModal() == wx.ID_OK:
            input_text = find_replace_dialog.GetValue()
            if "," in input_text:
                find_text, replace_text = input_text.split(",", 1)
                content = self.text_area.GetValue()
                updated_content = content.replace(find_text, replace_text)
                self.text_area.SetValue(updated_content)
        find_replace_dialog.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    Notepad()
    app.MainLoop()
