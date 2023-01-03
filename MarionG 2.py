import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import mysql.connector
import sys
from tkcalendar import DateEntry
from sqlalchemy import create_engine

def clear_text():
    e0.config(state="normal")
    e0.delete(0, END)
    e1.config(state="normal")
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e5.delete(0, END)
    e0.config(state="readonly")
    e1.config(state="readonly")
    e6.config(state="normal")
    e6.delete(0, END)
    e6.set('Process')
    e6.config(state="readonly")
    
def addTable():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="fruitas")
    mycursor = mysqldb.cursor()
    try:
        mycursor.execute("CREATE TABLE IF NOT EXISTS stocks (fruit VARCHAR(20) NOT NULL UNIQUE, quantity INT NOT NULL)")
        mycursor.execute("CREATE TABLE IF NOT EXISTS deliver (delID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, delFruit VARCHAR(20) NOT NULL, delStore VARCHAR(100) NOT NULL, delLoc VARCHAR(100) NOT NULL, delDate DATE NOT NULL, delQuant INT NOT NULL, remarks VARCHAR(20))")
        mycursor.execute("INSERT INTO stocks (fruit, quantity) VALUES ('Apple', 0), ('Cherry', 0), ('Dalandan', 0), ('Grapes', 0), ('Guyabano', 0), ('Kiwi', 0), ('Lanzones', 0), ('Lemon', 0), ('Mango', 0)")
        mysqldb.commit()
    except:
        mysqldb.rollback()
        mysqldb.close()

def GetValue(event):

    delID = e0.get()
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
    mycursor=mysqldb.cursor()
    e0.config(state="normal")
    e0.delete(0, END)
    e1.config(state="normal")
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.config(state="normal")
    e6.delete(0, END)
    row_id = listBox1.selection()[0]
    select = listBox1.set(row_id)
    e0.insert(0,select['delID'])
    e0.config(state="readonly")
    e1.insert(0,select['delFruit'])
    e1.config(state="readonly")
    e2.insert(0,select['delStore'])
    e3.insert(0,select['delLoc'])
    e4.insert(0,select['delDate'])
    e5.insert(0,select['delQuant'])
    e6.insert(0,select['remarks'])
    e6.config(state="readonly")
    mysqldb.rollback()
    mysqldb.close()
    refresh()

def refresh():
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
    mycursor=mysqldb.cursor()
    try:
        mycursor.execute("SELECT fruit, quantity FROM stocks")
        data=mycursor.fetchall()
        for i in listBox.get_children():
            listBox.delete(i)
        for i, (fruit, quantity) in enumerate(data, start=1):
            listBox.insert("", "end", values=(fruit, quantity))
        
        mycursor.execute("SELECT delID, delFruit, delStore, delLoc, delDate, delQuant, remarks FROM deliver")
        data2=mycursor.fetchall()
        for i in listBox1.get_children():
            listBox1.delete(i)
        for i, (delID, delFruit, delStore, delLoc, delDate, delQuant, remarks) in enumerate(data2, start=1):
            listBox1.insert("", "end", values=(delID, delFruit, delStore, delLoc, delDate, delQuant, remarks))
    except Exception as e:
       print(e)
       mysqldb.rollback()
       mysqldb.close()
    e6.config(state="normal")
    e6.delete(0, END)
    e6.set('Process')
    e6.config(state="readonly")
    
def AddSched():
    data1 = e1.get()
    data2 = e2.get()
    data3 = e3.get()
    data4 = e4.get()
    data5 = int(e5.get())
    data6 = e6.get()
    import functools
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
    mycursor=mysqldb.cursor()
    if len(data1) == 0 or len(data2) == 0 or len(data3) == 0 or len(data4) == 0:
        messagebox.showerror("Error", "Fields should not be empty")

    else:
        try:
            sql = "SELECT quantity FROM stocks WHERE fruit = %s"
            val = (data1,)
            mycursor.execute(sql, val)
            stock=mycursor.fetchall()
            for i in stock:
                a = sum(list(map(sum, list(stock))))
                
            if data5 < a:
                sql = "INSERT INTO deliver (delFruit, delStore, delLoc, delDate, delQuant, remarks) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (data1, data2, data3, data4, data5, data6)
                mycursor.execute(sql, val)
                
                sql2 = "UPDATE stocks SET quantity = quantity - %s WHERE fruit = %s"
                val2 = (data5, data1)
                mycursor.execute(sql2, val2)
                
                mysqldb.commit()
                lastid = mycursor.lastrowid
                messagebox.showinfo("Information", "Delivery Scheduled")
                e1.delete(0, END)
                e2.delete(0, END)
                e3.delete(0, END)
                e4.delete(0, END)
                e5.delete(0, END)
                e1.focus_set()
            else:
                messagebox.showerror("Error", "Kulang Stocks")
                clear_text()
                refresh()
            
        except Exception as e:
            print(e)
            mysqldb.rollback()
            mysqldb.close()
    refresh()

def delete():
    data0 = e0.get()
    data1 = e1.get()
    data5 = int(e5.get())
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
    mycursor=mysqldb.cursor()

    if len(data0) == 0:
        messagebox.showerror("Error", "Error in the Delivery ID")
    else:
        try:
            sql = "DELETE FROM deliver WHERE delID= %s"
            val = (data0,)
            mycursor.execute(sql, val)

            sql2 = "UPDATE stocks SET quantity = quantity + %s WHERE fruit = %s"
            val2 = (data5, data1)
            mycursor.execute(sql2, val2)
            mysqldb.commit()
            lastid = mycursor.lastrowid
            messagebox.showinfo("information", "Record Deleted successfully...")

        except Exception as e:
           print(e)
           mysqldb.rollback()
           mysqldb.close()
    clear_text()
    refresh()

def update():
    data0 = e0.get()
    data1 = e1.get()
    data2 = e2.get()
    data3 = e3.get()
    data4 = e4.get()
    data5 = int(e5.get())
    data6 = e6.get()
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
    mycursor=mysqldb.cursor()

    if len(data0) == 0 or len(data1) == 0 or len(data2) == 0 or len(data3) == 0 or len(data4) == 0:
        messagebox.showerror("Error", "Fields should not be empty")

    else:
        try:
           sql = "UPDATE deliver SET delDate= %s, delQuant= %s, remarks= %s WHERE delID= %s"
           val = (data4,data5,data6,data0)
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("information", "Record Updated successfully...")

        except Exception as e:
           print(e)
           mysqldb.rollback()
           mysqldb.close()
    clear_text()
    refresh()

def RecDel():
    win1 = Toplevel()
    win1.geometry("250x200")
    win1.minsize(250, 200)
    win1.maxsize(250, 200)
    win1.title("About")
    win1.config(bg='#b541a9')

    l=Label(win1,text="Recieve Delivery", font='Helvetica 9 bold', bg='#b541a9')
    l.grid(row=0, columnspan=3, sticky=W+E)
    
    l1=Label(win1,text="Fruit:", font='Helvetica 9 bold', bg='#b541a9')
    l1.grid(row=1, column=1, sticky=W)
    l2=Label(win1,text="Quantity:", font='Helvetica 9 bold', bg='#b541a9')
    l2.grid(row=2, column=1, sticky=W)

    my_conn = create_engine("mysql+mysqldb://root:@localhost/fruitas")
    query="SELECT fruit FROM stocks"
    my_data=my_conn.execute(query)
    my_list=[r for r, in my_data]
    e7=ttk.Combobox(win1, width=27, state="readonly", values=my_list)
    e7.grid(row=1, column=2)
    e7.current()
    e8=Entry(win1, width=30)
    e8.grid(row=2, column=2)
    
    def RecDel2():
        data1 = e7.get()
        data2 = e8.get()
        
        mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="fruitas")
        mycursor=mysqldb.cursor()
        if len(data1) == 0 or len(data2) == 0:
            messagebox.showerror("Error", "Fields should not be empty")

        else:
            try:
                sql = "UPDATE stocks SET quantity = quantity + %s WHERE fruit = %s"
                val = (data2, data1)
                mycursor.execute(sql, val)
                    
                mysqldb.commit()
                lastid = mycursor.lastrowid
                messagebox.showinfo("Information", "Products added to inventory")
                
            except Exception as e:
                print(e)
                mysqldb.rollback()
                mysqldb.close()
        refresh()
        
    b7=Button(win1, text="Receive Delivery", command=RecDel2, width=23)
    b7.grid(row=3, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)
    
    b8=Button(win1, text="Cancel", command=win1.destroy, width=23)
    b8.grid(row=4, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)

def AboutUs():
    win4 = Toplevel()
    win4.geometry("330x280")
    win4.minsize(330, 280)
    win4.maxsize(330, 280)
    win4.title("About")
    win4.config(bg='#b541a9')

    label1=Label(win4,text="About Us", font='Helvetica 11 bold', bg='#b541a9')
    label1.grid(row=0, columnspan=2, sticky=W+E)

    label2=Label(win4,text="Ribano's Fruit Distribution", font='Helvetica 9', bg='#b541a9')
    label2.grid(row=1, column=0, columnspan=2, sticky=W+E)
    label3=Label(win4,text="Database Management System", font='Helvetica 9', bg='#b541a9')
    label3.grid(row=2, column=0, columnspan=2, sticky=W+E)


    #Group Members
    frame3 = LabelFrame(win4, font=("Komika Axis", 10), text="Group Members", bd=5, relief="sunken", bg='#b541a9')
    frame3.grid(column=0, columnspan=2, row=11, rowspan=7, padx=5,pady=5,ipadx=2,ipady=2)
    m1=Label(frame3, font=("Verdana", 12), text="Table, Caleb Kyle", bg='#b541a9', width=30)
    m1.grid(column=0, row=11, sticky=W)
    m2=Label(frame3, font=("Verdana", 12), text="Ribano, Marion", bg='#b541a9', width=30)
    m2.grid(column=0, row=12, sticky=W)
    m3=Label(frame3, font=("Verdana", 12), text="Gabriel, Karryle Joy", bg='#b541a9', width=30)
    m3.grid(column=0, row=13, sticky=W)
    m4=Label(frame3, font=("Verdana", 12), text="Barundia, Dale Justin", bg='#b541a9', width=30)
    m4.grid(column=0, row=14, sticky=W)
    m5=Label(frame3, font=("Verdana", 12), text="Torres, John Paul", bg='#b541a9', width=30)
    m5.grid(column=0, row=15, sticky=W)
    m6=Label(frame3, font=("Verdana", 12), text="Torres, Lance Julian", bg='#b541a9', width=30)
    m6.grid(column=0, row=16, sticky=W)
    m7=Label(frame3, font=("Verdana", 12), text="Ramos, Eldrin Dave", bg='#b541a9', width=30)
    m7.grid(column=0, row=17, sticky=W)
    
def Exit():
    app.destroy()

app=Tk()
app.geometry("1170x550")
app.minsize(1170, 550)
app.maxsize(1170, 550)

global e0
global e1
global e2
global e3
global e4
global e5
global e6

app.title("RIBANO'S FRUIT DISTRIBUTION")
app.config(bg='#48f79a')
#bg = PhotoImage(file = "Ribano_Fruit_Distribution.png")
#bg1 = Label(app, image=bg)
#bg1.place(x=0, y=0, relwidth=1, relheight=1)

addTable()

style=ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#b541a9", fieldbackground="#6a2d7f")

img=PhotoImage(file="Header.png")
p1=Label(image = img, bg='#2d1336')
p1.grid(row=0, columnspan=7, sticky=W+E)


#Change select color:
style.map("Treeview", background=[('selected', '#274472')])
#Listbox of Stocks
listBox = ttk.Treeview(app, selectmode="extended", columns=("fruit", "quantity"), height=14)
listBox.heading("#0", text="-")
listBox.column("#0", anchor=CENTER, stretch=NO, width=0)
listBox.heading("#1", text="Fruit")
listBox.column("#1", anchor=CENTER, stretch=NO, width=100)
listBox.heading("#2", text="Quantity")
listBox.column("#2", anchor=CENTER, stretch=NO, width=80)            
listBox.grid(row=1, rowspan=8,column=1)
sb = Scrollbar(app,orient=VERTICAL)
listBox.config(yscrollcommand=sb.set)
sb.grid(row=1, rowspan=8, column=2, sticky=NS)
sb.config(command=listBox.yview)


#Inputs
frame = LabelFrame(app, font=("Berlin Sans FB Demi", 11), text="Inputs", bd=5, relief="groove", bg='#b541a9')
frame.grid(column=3, columnspan=2, row=1, rowspan=11, padx=5,pady=5,ipadx=2,ipady=2)
                       
l0=Label(frame,text="Deliver ID:", font='Helvetica 9 bold', bg='#b541a9')
l0.grid(row=1, column=3, sticky=W)
l1=Label(frame,text="Fruit:", font='Helvetica 9 bold', bg='#b541a9')
l1.grid(row=2, column=3, sticky=W)
l2=Label(frame,text="Store:", font='Helvetica 9 bold', bg='#b541a9')
l2.grid(row=3, column=3, sticky=W)
l3=Label(frame,text="Location:", font='Helvetica 9 bold', bg='#b541a9')
l3.grid(row=4, column=3, sticky=W)
l4=Label(frame,text="Date:", font='Helvetica 9 bold', bg='#b541a9')
l4.grid(row=5, column=3, sticky=W)
l5=Label(frame,text="Quantity:", font='Helvetica 9 bold', bg='#b541a9')
l5.grid(row=6, column=3, sticky=W)
l6=Label(frame,text="Remarks:", font='Helvetica 9 bold', bg='#b541a9')
l6.grid(row=7, column=3, sticky=W)

e0=Entry(frame, width=30, state="readonly")
e0.grid(row=1, column=4)

my_conn = create_engine("mysql+mysqldb://root:@localhost/fruitas")
query="SELECT fruit FROM stocks"
my_data=my_conn.execute(query)
my_list=[r for r, in my_data]

e1=ttk.Combobox(frame, width=27, state="readonly", values=my_list)
e1.grid(row=2, column=4)
e1.current()

e2=Entry(frame, width=30)
e2.grid(row=3, column=4)
e3=Entry(frame, width=30)
e3.grid(row=4, column=4)
e4=DateEntry(frame, selectmode='day', date_pattern='yyyy-mm-dd', width=27)
e4.grid(row=5, column=4)
e5=Entry(frame, width=30)
e5.grid(row=6, column=4)
value = StringVar(value='Process')
e6=ttk.Combobox(frame, width=27, state="disabled", textvariable=value)
e6['values'] = (' Process',
                ' Delivered',
                )
e6.grid(row=7, column=4)
e6.current()


b0=Button(frame, text="CLEAR / RESET", command=clear_text, borderwidth=2, relief="solid", fg="#ffa47e", font='Helvetica 9 bold', width=39)
b0.grid(row=8, column=3, columnspan=2, padx=1,pady=1,ipadx=1,ipady=1)
b1=Button(frame, text="Schedule Deliver", command=AddSched,width=39)
b1.grid(row=9, column=3, columnspan=2, padx=1,pady=1,ipadx=1,ipady=1)
b2=Button(frame, text="Cancel Deliver", command=delete,width=39)
b2.grid(row=10, column=3, columnspan=2, padx=1,pady=1,ipadx=1,ipady=1)
b3=Button(frame, text="Update Deliver", command=update,width=39)
b3.grid(row=11, column=3, columnspan=2, padx=1,pady=1,ipadx=1,ipady=1)

img2=PhotoImage(file="2.png")
p2=Label(image = img2)
p2.grid(row=12, rowspan=4, column=1, columnspan=2, sticky=W+E)

frame4 = LabelFrame(app, font=("Berlin Sans FB Demi", 11), text="Other Functions", bd=5, relief="groove", bg='#b541a9')
frame4.grid(column=3, columnspan=2, row=12, padx=5, pady=5,ipadx=2, ipady=2)
b4=Button(frame4, text="Refresh Tables", command=refresh, width=33)
b4.grid(row=12, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)
b5=Button(frame4, text="Receive Delivery", command=RecDel, width=33)
b5.grid(row=13, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)
b6=Button(frame4, text="About", command=AboutUs, width=33)
b6.grid(row=14, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)
b7=Button(frame4, text="Exit Program", command=Exit, width=42)
b7.grid(row=15, column=1, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky=W+E)


#Listbox of Deliver
listBox1 = ttk.Treeview(app, selectmode="extended", columns=("delID", "delFruit", "delStore", "delLoc", "delDate", "delQuant", "remarks"), height=24)
listBox1.heading("#0", text="-")
listBox1.column("#0", anchor=CENTER, stretch=NO, width=0)
listBox1.heading("#1", text="Deliver Code")
listBox1.column("#1", anchor=CENTER, stretch=NO, width=80)
listBox1.heading("#2", text="Fruit")
listBox1.column("#2", anchor=W, stretch=NO, width=80) 
listBox1.heading("#3", text="Store")
listBox1.column("#3", anchor=W, stretch=NO, width=110)
listBox1.heading("#4", text="Location")
listBox1.column("#4", anchor=W, stretch=NO, width=110)
listBox1.heading("#5", text="Date")
listBox1.column("#5", anchor=CENTER, stretch=NO, width=80)
listBox1.heading("#6", text="Quantity")
listBox1.column("#6", anchor=CENTER, stretch=NO, width=80)
listBox1.heading("#7", text="Remarks")
listBox1.column("#7", anchor=CENTER, stretch=NO, width=80)
listBox1.grid(row=1, rowspan=15,column=5)
sb1 = Scrollbar(app,orient=VERTICAL)
listBox1.config(yscrollcommand=sb1.set)
sb1.grid(row=1, rowspan=15, column=6, sticky=NS)
sb1.config(command=listBox1.yview)

refresh()

listBox1.bind('<Double-Button-1>',GetValue)

my_menu = Menu(app)
app.config(menu=my_menu)

app.iconphoto(False, tk.PhotoImage(file="1.png"))
app.mainloop()
