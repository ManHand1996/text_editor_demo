import wx
import re
import base64

global old_pos, new_pos, old_key
new_pos, old_pos ,old_key= 0, 0, ""

class OptionFrame(wx.Frame):
    def __init__(self, parent, id, title, text_content):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title)

        # 组件
        self.text_content = text_content
        self.panel = wx.Panel(self, -1)
        self.query_rb = wx.RadioButton(self.panel, label="查找", style=wx.RB_GROUP)
        self.replace_rb = wx.RadioButton(self.panel, label="替换")
        self.Bind(wx.EVT_RADIOBUTTON, self.onCheck)
        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.fsizer = wx.FlexGridSizer(1, 4, 5, 5)
        # self.text_fsizer = wx.FlexGridSizer(2, 2, 5, 5)
        self.label_count = wx.StaticText(self.panel, id=-1, label="已找到:")
        self.label_target = wx.StaticText(self.panel, id=-1, label="目标字符串：")
        self.label_replace = wx.StaticText(self.panel, id=-1, label="替换字符串：")
        self.query_text = wx.TextCtrl(self.panel, id=-1)
        self.replace_text = wx.TextCtrl(self.panel, id=-1)
        self.query_btn = wx.Button(self.panel, id=-1, label="搜索")
        self.next_btn = wx.Button(self.panel, id=-1, label="下一个")
        self.replace_btn = wx.Button(self.panel, id=-1, label="替换所有")
        self.replace_single_btn = wx.Button(self.panel, id=-1, label="替换")


        # 事件绑定
        self.replace_btn.Bind(wx.EVT_BUTTON, self.replace_all)
        self.replace_single_btn.Bind(wx.EVT_BUTTON, self.replace_single)
        self.query_btn.Bind(wx.EVT_BUTTON, self.query)
        self.next_btn.Bind(wx.EVT_BUTTON, self.query_next)
        self.Bind(wx.EVT_CLOSE, self.close_window)

        self.SetSize(300, 160)
        self.diable_replace_ctr()
        self.layout_query()
        self.Centre()

    def highlightText(self, pos, size):
        self.text_content.SetInsertionPoint(pos)
        self.text_content.SetStyle(pos, size, wx.TextAttr("black", "yellow"))

    def query(self, evt):
        self.next_btn.Enable()
        content = self.text_content.GetValue()
        key = self.query_text.GetValue()
        if not key:
            wx.MessageDialog(parent=self,message="输入查找字符串").ShowModal()
            return
        if not content:
            wx.MessageDialog(parent=self,message="请先打开文件").ShowModal()
            return

        self.text_content.SetStyle(0, len(content), wx.TextAttr("black", "white"))
        count = 0
        for i in range(self.text_content.GetNumberOfLines()):
            old_pos, new_pos = 0, 0
            while new_pos != -1:
                new_pos = self.text_content.GetLineText(i).find(key, old_pos)
                if new_pos == -1:
                    break
                old_pos = new_pos + len(key)
                count += 1

        self.label_count.SetLabel("已找到："+ str(count) + "个")

    def query_next(self, evt):
        global old_pos, new_pos, old_key

        key = self.query_text.GetValue()
        old_key = key
        new_pos = self.text_content.GetValue().find(key, old_pos)
        if new_pos != -1:
            old_pos = new_pos + len(key)
        else:
            old_pos, new_pos = 0, 0
            messagebox = wx.MessageDialog(parent=self,message="已查找完毕")
            messagebox.ShowModal()
            self.text_content.SetStyle(0, len(self.text_content.GetValue()), wx.TextAttr("black", "white"))
            self.text_content.SetInsertionPoint(0)
            return

        self.text_content.SetFocus()
        self.text_content.Bind(wx.EVT_SET_FOCUS, self.highlightText(new_pos, old_pos))
        self.SetFocus()

    def replace_all(self, evt):
        # replace all or alone

        key = self.query_text.GetValue()
        replace_str = self.replace_text.GetValue()
        content = self.text_content.GetValue()
        if not key:
            wx.MessageDialog(parent=self,message="输入查找字符串").ShowModal()
            return
        if not content:
            wx.MessageDialog(parent=self,message="请先打开文件").ShowModal()
            return
        
        self.text_content.SetValue(content.replace(key, replace_str, -1))
        index = self.text_content.GetValue().find(replace_str, 0)
        self.text_content.SetFocus()
        self.text_content.Bind(wx.EVT_SET_FOCUS, self.highlightText(index, index + len(replace_str)))
        self.SetFocus()

        message = wx.MessageDialog(self, message="全部替换完成")
        message.ShowModal()

    def replace_single(self, evt):
 
        global old_key, old_pos, new_pos
        self.text_content.SetFocus()

        pos = self.text_content.GetInsertionPoint()
        key = self.query_text.GetValue()
        cursor = self.text_content.GetValue().find(key, pos)
        replace_str = self.replace_text.GetValue()
        
        if not key:
            wx.MessageDialog(parent=self,message="输入查找字符串").ShowModal()
            return
        if not self.text_content.GetValue():
            wx.MessageDialog(parent=self,message="请先打开文件").ShowModal()
            return
        if key != old_key:
             old_pos, new_pos =0, 0
             self.text_content.SetInsertionPoint(0)
        if cursor == -1:
            wx.MessageDialog(parent=self,message="替换完成：已到文章末尾").ShowModal()
            self.text_content.SetInsertionPoint(0)
            return
        self.text_content.Replace(cursor, cursor + len(key), replace_str)
        self.SetFocus()

    def onCheck(self, evt):
        obj = evt.GetEventObject()
        label = obj.GetLabel()
        if label == "查找":
            self.diable_replace_ctr()
            self.layout_query()
        else:
            self.diable_query_ctr()
            self.layout_replace()

    def diable_replace_ctr(self):

        self.label_replace.Show(False)
        self.replace_text.Show(False)
        self.next_btn.Disable()
        self.replace_btn.Show(False)
        self.replace_single_btn.Show(False)

    def diable_query_ctr(self):
        self.label_count.Show(False)
        self.query_btn.Show(False)

    def layout_replace(self):
        global old_pos, new_pos
        old_pos, new_pos = 0, 0
        self.label_replace.Show(True)
        self.replace_text.Show(True)
        self.next_btn.Enable()
        self.replace_btn.Show(True)
        self.replace_single_btn.Show(True)
        self.replace_text.SetValue("")
        self.query_text.SetValue("")
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fsizer_btn = wx.FlexGridSizer(1, 3, 1, 1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(2, 2, 1, 1)
        hbox.AddMany([self.query_rb, self.replace_rb])
        fsizer.Add(self.label_target, 0, wx.EXPAND | wx.ALL, 2)
        fsizer.Add(self.query_text, 1, wx.EXPAND | wx.ALL, 2)
        fsizer.Add(self.label_replace, 0, wx.EXPAND | wx.ALL, 2)
        fsizer.Add(self.replace_text, 1, wx.EXPAND | wx.ALL, 2)
        fsizer.AddGrowableCol(1, 1)
        fsizer_btn.Add(self.replace_btn, 1, wx.EXPAND | wx.ALL, 2)
        fsizer_btn.Add(self.replace_single_btn, 1, wx.EXPAND | wx.ALL, 2)
        fsizer_btn.Add(self.next_btn, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 1,  wx.EXPAND | wx.ALL, 2)
        vbox.Add(fsizer, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(fsizer_btn, 1, wx.EXPAND | wx.ALL, 2)
        self.panel.SetSizer(vbox)
        self.panel.Layout()

    def layout_query(self):
        global old_pos, new_pos
        old_pos, new_pos = 0, 0
        self.label_count.Show(True)
        self.query_text.SetValue("")
        self.query_btn.Show(True)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fsizer_btn = wx.FlexGridSizer(1, 2, 1, 1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(1, 2, 1, 1)
        hbox.AddMany([self.query_rb, self.replace_rb])
        fsizer.Add(self.label_target, 0, wx.EXPAND | wx.ALL, 2)
        fsizer.Add(self.query_text, 1, wx.EXPAND | wx.ALL, 2)
        fsizer.AddGrowableCol(1, 1)
        fsizer_btn.Add(self.query_btn, 1, wx.EXPAND | wx.ALL, 2)
        fsizer_btn.Add(self.next_btn, 1, wx.EXPAND | wx.ALL, 2)

        vbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(self.label_count, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(fsizer, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(fsizer_btn, 1, wx.EXPAND | wx.ALL, 2)
        self.panel.SetSizer(vbox)
        self.panel.Layout()

    def close_window(self, evt):
        self.text_content.SetStyle(0, len(self.text_content.GetValue()),
                                   wx.TextAttr("black", "white"))
        self.Destroy()


class MainFrame(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent=parent, id=id, title=title)
        w, h = wx.GetDisplaySize()
        self.SetSize(w/3, h/3)
        self.menu_bar = wx.MenuBar()
        self.OPEN_FILE_ID = 311
        self.SAVE_FILE_ID = 312

        self.STATISTICS_INFO_ID = 411
        self.SPEC_INFO_ID = 412

        self.COPY_ID = 511
        self.PASTE_ID = 512
        self.CUT_ID = 513
        self.DEL_ID = 514
        self.QUERY_ID = 515
        self.REPLACE_ID = 516

        self.ENCRYPT_ID = 611
        self.DECRYPT_ID = 612

        self.init_menu()
        self.SetMenuBar(self.menu_bar)

        self.panel = wx.Panel(self, -1)

        self.main_text = wx.TextCtrl(self.panel, id=-1, style=wx.TE_MULTILINE | wx.TE_RICH)
        # self.main_text.SetFocus()
        self.sizer = wx.FlexGridSizer(1,1,0,0)
        self.sizer.Add(self.main_text, 1, wx.ALL | wx.EXPAND | wx.CENTER, 0)
        self.sizer.AddGrowableRow(0,1)
        self.sizer.AddGrowableCol(0, 1)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Centre()
        self.panel.Show()

    def init_menu(self):
        # file menu
        file_menu = wx.Menu()
        open_item = wx.MenuItem(file_menu, id=self.OPEN_FILE_ID, text="打开", kind=wx.ITEM_NORMAL)
        file_menu.Append(open_item)
        file_menu.AppendSeparator()

        save_item = wx.MenuItem(file_menu, id=self.SAVE_FILE_ID, text="保存", kind=wx.ITEM_NORMAL)
        file_menu.Append(save_item)
        file_menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.open_file, open_item)
        self.Bind(wx.EVT_MENU, self.save_file, save_item)
        self.menu_bar.Append(file_menu, "文件")

        # base option menu
        base_option_menu = wx.Menu()
        query_replace_item = wx.MenuItem(base_option_menu, id=self.QUERY_ID, text="查找与替换", kind=wx.ITEM_NORMAL)
        base_option_menu.Append(query_replace_item)
        base_option_menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.query_replace, query_replace_item)
        self.menu_bar.Append(base_option_menu, "操作")

        # statistics menu
        statistics_menu = wx.Menu()
        statistics_item = wx.MenuItem(statistics_menu, id=self.STATISTICS_INFO_ID,
                                      text="字符统计信息", kind=wx.ITEM_NORMAL)
        statistics_menu.Append(statistics_item)
        statistics_menu.AppendSeparator()

        spec_item = wx.MenuItem(statistics_menu, id=self.SPEC_INFO_ID,
                                text="指定字符统计", kind=wx.ITEM_NORMAL)
        statistics_menu.Append(spec_item)
        statistics_menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.statistics_all, statistics_item)
        self.Bind(wx.EVT_MENU, self.statistics_spec, spec_item)
        self.menu_bar.Append(statistics_menu, "统计")

        # encrypt and decrypt
        encrypt_decrypt_menu = wx.Menu()
        encrypt_item = wx.MenuItem(encrypt_decrypt_menu, id=self.ENCRYPT_ID, text="文件加密", kind=wx.ITEM_NORMAL)
        encrypt_decrypt_menu.Append(encrypt_item)
        encrypt_decrypt_menu.AppendSeparator()

        decrypt_item = wx.MenuItem(encrypt_decrypt_menu, id=self.DECRYPT_ID, text="文件解密", kind=wx.ITEM_NORMAL)
        encrypt_decrypt_menu.Append(decrypt_item)
        encrypt_decrypt_menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.encrypt_file, encrypt_item)
        self.Bind(wx.EVT_MENU, self.decrypt_file, decrypt_item)
        self.menu_bar.Append(encrypt_decrypt_menu, "加密和解密")

    def open_file(self,evt):
        file_filter = "Txt (*.txt)|*.txt|" "All files (*.*)|*.*"
        file_dialog = wx.FileDialog(self, message="选择单个文件", wildcard=file_filter, style=wx.FD_OPEN)
        r = file_dialog.ShowModal()
        if r != wx.ID_OK:
            return
        path = file_dialog.GetPath()
        with open(path, 'r') as f:
            self.main_text.SetValue(f.read())


    def save_file(self, evt):
        global main_text
        file_filter = "Txt (*.txt)|*.txt|" "All file(*.*)|*.*"
        file_dialog = wx.FileDialog(self, message="保存为", wildcard=file_filter, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        r = file_dialog.ShowModal()
        if r == wx.ID_OK:
            with open(file_dialog.GetPath(), 'w') as f:
                f.write(self.main_text.GetValue())

    def query_replace(self, evt):
        qf = OptionFrame(self, id=-1, title="查找与替换",text_content=self.main_text)
        qf.Show()

    def statistics_all(self, evt):
        content = self.main_text.GetValue()
        statistics_info = {'letters':0, 'spaces':0, 'chinese_chars':0,
                            'interpunction':0, 'other':0, 'total':len(content)
            }
        regex_letters = re.compile(r'[a-zA-Z]')
        regex_spaces = re.compile(r' ')
        # [\u4E00-\u9FA5]
        regex_chinese_chars = re.compile(r'[\u2E80-\u9FFF]')
        regex_interpunction = re.compile(r'[。，、；：？！“”……——《》（）\[\]\.,]')
        statistics_info['letters'] = len(regex_letters.findall(content))
        statistics_info['spaces'] = len(regex_spaces.findall(content))
        statistics_info['chinese_chars'] = len(regex_chinese_chars.findall(content))
        statistics_info['interpunction'] = len(regex_interpunction.findall(content))
        statistics_info['other'] = statistics_info['total'] - statistics_info['letters']\
                                  - statistics_info['spaces'] - statistics_info['chinese_chars']\
                                  - statistics_info['interpunction']
        infos_str = ""
        for key, value in statistics_info.items():
            infos_str += key + ":  " + str(value) + " 个\n"
        infos_dialog = wx.MessageDialog(self, message=infos_str,caption="字符统计信息")
        infos_dialog.ShowModal()


    def statistics_spec(self, evt):
        text_dialog = wx.TextEntryDialog(self, message="输入字符串", caption="统计特等字符串数目")
        r = text_dialog.ShowModal()
        text_input = text_dialog.GetValue()
        if r == wx.ID_OK:
            message = "请输入字符串"
            if text_input:
                count = 0
                for i in range(self.main_text.GetNumberOfLines()):
                    old_pos, new_pos = 0, 0
                    while new_pos != -1:
                        new_pos = self.main_text.GetLineText(i).find(text_input, old_pos)
                        if new_pos == -1:
                            break
                        old_pos = new_pos + len(text_input)
                        count += 1
                message = '字符串 "' + text_input + ' ":  ' + str(count) + "个"
            message_box = wx.MessageDialog(text_dialog, message,caption="统计结果")
            message_box.ShowModal()
            text_dialog.ShowModal()
    
    def encrypt_file(self, evt):
        content = self.main_text.GetValue()
        encry_content = base64.b64encode(content.encode())
        self.main_text.SetValue(encry_content.decode())
        wx.MessageDialog(self,"加密完成，请保存。").ShowModal()


    def decrypt_file(self, evt):
        content = self.main_text.GetValue()
        decry_content = base64.b64decode(content)
        self.main_text.SetValue(decry_content)
        wx.MessageDialog(self, "解密完成，请保存。").ShowModal()


if __name__ == "__main__":
    app = wx.App()
    f = MainFrame(None, -1, "文本编辑器")
    f.Show()
    app.MainLoop()

