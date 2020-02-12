import excel
from tkinter import *
import tkinter.filedialog

top =  Tk()

global _erpName
_erpName = './erp.xlsx'
def guiInit():
    def fchoose():
        global _erpName
        filename = tkinter.filedialog.askopenfilename()
        if len(filename) != 0:
            s = filename
            lb.config(text='你选择的erp文件是:{}'.format(filename))
            _erpName = filename
    def okPress():
        global _erpName
        if oldName.get() and newName.get():
            OName = oldName.get()
            NName = newName.get()
            erp   = excel.handlerErp(_erpName)
            erp.findout(OName,NName)
            # newWindow = Tk()
            # newWindow.title('---------新旧模块对应关系-------')
            # newWindow.geometry('300x700+150+150')
            # msg_count = 0
            # for i in result1:
            #     msg = i +'---->' + result2[msg_count]
            #     Label(newWindow,text=msg)
            #     Label.pack()
            #     msg_count += 1
            lb.config(text='生成完毕')
        else:
            lb.config(text='请输入替换模块及被替换模块')
    top.title('EOL模块替换关系自动生成')
    top.geometry('450x180+150+150')

    fm1 = Frame()
    fm1.pack(side='left',padx=15,expand='YES')
    lb2 = Label(fm1,text='请输入旧模块名字')
    lb2.pack(side='top')
    oldName = Entry(fm1)
    oldName.pack()
    lb3 = Label(fm1,text='请输入新模块名字')
    lb3.pack(side='top')
    newName = Entry(fm1)
    newName.pack()
    lb = Label(fm1,text='')
    lb.pack()
    Button(fm1,text='erp文件(默认已配置好)',command = fchoose).pack(side='left',fill='y',expand='yes')
    Button(fm1,text='生成替代关系表',command=okPress).pack(side='left',padx=20,expand='yes')
    #Button(fm1,text='erp文件(默认已配置好)').pack(side='right',fill='y',expand='yes')
    
    
    top.mainloop()
    

if __name__ == '__main__':
    guiInit()
    

