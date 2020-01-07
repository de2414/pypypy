from tkinter import *
import sqlite3

myConn = sqlite3.connect("student.db")
from sqldb import *
db =myDB("D:\\上課資料\\10801基礎程式設計\\student.db")

def getAllData():
    sqlstr = "SELECT Record.Std_Id,Student.Std_Name,Record.Course_Id, Record.Rcd"
    sqlstr += "  FROM Record"
    sqlstr += "  INNER JOIN Student"
    sqlstr += "  on Student.Std_Id = Record.Std_Id"
    
    #myset = list()
    myset = db.getSQLresult(sqlstr)

    datalist.delete(0,END)
    for idx, item in enumerate(myset, 0):
        datalist.insert(END,"{0} {1} {2} {3}".format(item[0],item[1],item[2],item[3]))

def getitem(evt):
    selecteditem = datalist.get(datalist.curselection()[0])
    selectedlist = selecteditem.split(' ')
    #=== dep_id ===
    dep_id = selectedlist[0]
    #  判斷Option Mennu停在哪喇
    for idx, item in enumerate( depset,0):
        if dep_id == (item.split(':'))[0]:
            depvar.set(item)
            break
    #=== std_id ===
    std = selectedlist[1]
    for idx, item in enumerate( stuset,0):
        if std == (item.split(':'))[0]:
            stuvar.set(item)
            break
   
    #=== cou_id ===
    cou = selectedlist[2]
    for idx, item in enumerate( couset,0):
        if cou == (item.split(':'))[0]:
            couvar.set(item)
            break
   
    #=== rec ===
    rec = selectedlist[3]
    erec.delete(0,END)
    erec.insert(0,rec)
    
    
   


def Qo(instr):
    return "'" + instr + "'"    

def insertData():
    sqlstr = "insert into Record(Record.Rcd)values("
    sqlstr += Qo(stuvar.get().split(':')[0]) + ","
    sqlstr += Qo(depvar.get().split(':')[0]) + ","
    sqlstr += Qo(couvar.get().split(':')[0]) + ","
    sqlstr += Qo(erec.get()) + ")"
    
    db.execSQLcommand(sqlstr)
    
    getAllData()
             
def deleteData():
    sqlstr = "delete from  Course "
    sqlstr += " where Course_Id = " + Qo(ecou_id.get())
    db.execSQLcommand(sqlstr)
    getAllData()
    
def updateData():
    sqlstr = "update Course set Course_Id = " + db.Qo(ecou_id.get())
    sqlstr += " where Course_Name = " + db.Qo(ecou_name.get())

  
    db.execSQLcommand(sqlstr)
    getAllData()
def preparedepList():
    sqlstr =  'select dep_id, Dep_Name'
    sqlstr += ' from department '
    temp = db.getSQLresult(sqlstr)
    for idx , itemdep in enumerate(temp,0):
        depset.append("{0} {1}".format(itemdep[0], itemdep[1]))
def preparestdList():
    sqlstr =  'SELECT DISTINCT Record.Std_Id,Student.Std_Name'
    sqlstr += ' FROM Record '
    sqlstr += ' INNER JOIN Student '
    sqlstr += ' on Record.Std_Id = Student.Std_Id '
    temp = db.getSQLresult(sqlstr)
    for idx , itemstd in enumerate(temp,0):
        stuset.append("{0} {1}".format(itemstd[0], itemstd[1]))
def preparecouList():
    sqlstr =  'SELECT DISTINCT Record.Course_Id, Course.Course_Name'
    sqlstr += ' FROM Record '
    sqlstr += ' INNER JOIN Course '
    sqlstr += ' on Course.Course_Id = Record.Course_Id '
    temp = db.getSQLresult(sqlstr)
    for idx , itemcou in enumerate(temp,0):
        couset.append("{0} {1}".format(itemcou[0], itemcou[1]))
win = Tk()
win.title("成績資料維護")
win.geometry("600x520")
win.config(background="lightyellow")
#-------
   
        
queryStd = Button(win)
queryStd.config(text="全部資料", bg="gray", fg="white", width=10, height=2, font="標楷體14", command=getAllData)
queryStd.grid(row=0, column=0, stick=W)
#--------
datalist = Listbox(win)
datalist.bind('<<ListboxSelect>>', getitem)
datalist.config(width=80, height=15)
datalist.grid(row=1, column=0, columnspan=4)

#------
myScrollbar = Scrollbar(win)
myScrollbar.grid(row=1, column=4, stick=N+S)
myScrollbar.config(command=datalist.yview)
#====================================================
#學系--------------------------
ldepartment = Label(win, text="學系")
ldepartment.grid(row=2, column=0)
depset = list()
preparedepList()
depvar = StringVar() #準備 反映點選項目
depvar.set(depset[0]) #預設depList停駐的index

depList  = OptionMenu(win, depvar, *depset)
depList.grid(row=2, column=1, stick=W+E)
#學號+學生名字---------------------------------
lstudent = Label(win, text="學生")
lstudent.grid(row=3, column=0)
stuset = list()
preparestdList()
stuvar = StringVar() #準備 反映點選項目
stuvar.set(stuset[0]) #預設depList停駐的index

stuList  = OptionMenu(win, stuvar, *stuset)
stuList.grid(row=3, column=1, stick=W+E)
#課程名+課程ID----------------------------
lcou_name = Label(win, text="課程")
lcou_name.grid(row=3, column=2)
couset = list()
preparecouList()
couvar = StringVar() #準備 反映點選項目
couvar.set(couset[0]) #預設depList停駐的index

couList  = OptionMenu(win, couvar, *couset)
couList.grid(row=3, column=3, stick=W+E)

#成績---------------------------------------
lrec = Label(win, text="成績")
lrec.grid(row=4, column=2)
erec = Entry(win)
erec.grid(row=4, column=3, stick=W+E)







#=====================
opFrame = Frame(win)
opFrame.grid(row=6, column=0, columnspan=4, stick=W+E)
#
opInsert = Button(opFrame)
opInsert.config(text="新增", bg="gray", fg="blue", width=10, height=2, font="標楷體14", command=insertData)
opInsert.grid(row=0, column=0, stick=W+E)
#
opUpdate = Button(opFrame, command=updateData)
opUpdate.config(text="修改", bg="gray", fg="blue", width=10, height=2, font="標楷體14")
opUpdate.grid(row=0, column=1, stick=W+E)
#
opDelete = Button(opFrame)
opDelete.config(text="刪除", bg="gray", fg="blue", width=10, height=2, font="標楷體14", command=deleteData)
opDelete.grid(row=0, column=2, stick=W+E)



win.mainloop()
