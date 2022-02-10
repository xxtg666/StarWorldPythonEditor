import tkinter as tk
import tkinter.messagebox
import traceback

import resources
import sys
import PySimpleGUI as sg
import tkinter.filedialog

#代码高亮
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator



class __main__:
    window = tk.Tk()
    def __init__(self):
        window = self.window
        window.title("Python 编辑器")
        window.geometry('600x500')
        window.resizable(0,0)
        window.iconphoto(False,resources.base64_tkinter(resources.ice_cube))
        self.layout_setup()
        window.mainloop()
    def layout_setup(self):
        window = self.window
        # Menubar
        menu1 = tk.Menu(window)
        helpmenu = tk.Menu(window,tearoff=False)
        helpmenu.add_command(label="关于",command=lambda: commands.about(window))
        
        fm1 = tk.Menu(window,tearoff=False)
        fm1.add_command(label="新建",command=lambda: commands.file_operation.new(window,highlight_text))
        fm1.add_command(label="打开",command=lambda: commands.file_operation.open(highlight_text,window))
        fm1.add_command(label="保存",command=lambda: commands.file_operation.save(highlight_text.get("1.0","end"),window))
        fm1.add_command(label="另存为",command=lambda: commands.file_operation.save_as(window,highlight_text.get("1.0","end")))
        fm1.add_command(label="退出",command=exit)
        
        dm1 = tk.Menu(window,tearoff=False)
        dm1.add_command(label="启动调试",command=lambda: commands.run(highlight_text.get("1.0","end")))

        menu1.add_cascade(label="文件",menu=fm1)
        menu1.add_cascade(label="调试",menu=dm1)
        menu1.add_cascade(label="帮助",menu=helpmenu)
        
        window.config(menu=menu1)
        # Scrollbar
        scrollbar1 = tk.Scrollbar(window)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        # TextEdit
        highlight_text = tk.Text(window,yscrollcommand=scrollbar1.set,font=("Consolas",13))
        scrollbar1.config(command=highlight_text.yview)
        highlight_text.place(height=480,width=585)
        Percolator(highlight_text).insertfilter(ColorDelegator())


class commands:
    def about(window):
        tkinter.messagebox.showinfo(
            title=
            "关于 Python 编辑器",
            message=
"""
贡献名单：
    |- 功能
    |   |- StarWorld (https://www.starworldstudio.tk/)
    |- 布局
    |   |- 这里是小邓 (https://www.thisisxd.tk/)
    |- 应用测试
    |   |- 熊熊糖果
许可证：
    Copyright © 2022 StarWorld, 这里是小邓 & 熊熊糖果

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
        )
    def run(code):
        sg.theme("Default1")
        layout = [[sg.Output(key="输出",size=(50,10))],[sg.Button("运行")]]
        window = sg.Window("代码调试内容",layout=layout,icon=resources.ice_cube)
        while True:
            events,values = window.read()
            if events in (None,"Cancel","Exit"):
                break
            if events == "运行":
                window.Element("输出").update("")
                sys.stdin = commands.stdin
                try:
                    exec(code)
                except:
                    window.Element("输出").Update(traceback.format_exc())
        window.close()
    class stdin:
        def readline():
            text = sg.popup_get_text("请输入内容","运行调试",icon=resources.ice_cube,okb="确定",cancelb="取消")
            if text and text!="":
                sys.stdout.write(text+"\n\n")
            else:
                text="\n"
            return str(text)
    class file_operation:
        file = None
        file_e = 'utf-8'
        def save_as(window,content):
            try:
                self = commands.file_operation
                file = open(sg.popup_get_file("另存为","请选择文件",okb="确定",cancelb="取消",browseb="浏览",save_as=True),"w")
                if file != None:
                    self.file = file.name
                    self.file_e = file.encoding
                    window.title(f"{self.file} —— Python 编辑器")
                else:
                    return 0
                file.write(content)
                file.close()
            except BaseException as e:
                tkinter.messagebox.showerror("保存文件失败",f"异常信息\n{e}")
        def save(content,window):
            try:
                self = commands.file_operation
                if self.file == None:
                    self.save_as(window,content)
                    return 0
                else:
                    with open(self.file,"w",encoding=self.file_e) as file:
                        file.write(content)
            except BaseException as e:
                tkinter.messagebox.showerror("保存文件失败",f"异常信息\n{e}")
        def open(textedit:tk.Text,window:tk.Tk):
            try:
                self = commands.file_operation
                file = open(sg.popup_get_file("打开文件","请选择文件",okb="确定",cancelb="取消",browseb="浏览"
                ),"r",encoding="utf-8")
                textedit.replace("1.0","end",file.read())
                self.file = file.name
                self.file_e = "utf-8"
                window.title(f"{self.file} —— Python 编辑器")
            except BaseException as e:
                tkinter.messagebox.showerror("打开文件失败",f"异常信息\n{e}")
        def new(window:tk.Tk,textedit:tk.Text):
            try:
                self = commands.file_operation
                textedit.replace("1.0","end","")
                window.title("Python 编辑器")
                self.file = None
            except BaseException as e:
                tkinter.messagebox.showerror("新建文件失败",f"异常信息\n{e}")
if __name__ == "__main__":
    __main__()