from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
import random
import string
import socket
import datetime
import webbrowser


# Functions
def update(rows):
    trv.delete(*trv.get_children())
    for row in rows:
        trv.insert('', 'end', values=row)
    username.set(get_YID())
    password.set(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8)))


def search():
    q = search_txt.get()
    cursor.execute(
        "SELECT * FROM users WHERE username LIKE '%" + q + "%' OR name LIKE '%" + q + "%' or email LIKE '%" + q + "%' or branch LIKE '%" + q + "%'")
    rows = cursor.fetchall()
    update(rows)


def clear():
    search_txt.set('')
    username.set(get_YID())
    password.set('')
    name.set('')
    branch.set('')
    email.set('')
    points.set(0)
    events.set(0)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    update(rows)


def getrow(event):
    item = trv.item(trv.focus())
    username.set(item['values'][0])
    password.set(item['values'][1])
    name.set(item['values'][2])
    email.set(item['values'][3])
    branch.set(item['values'][4])
    events.set(int(item['values'][5]))
    points.set(int(item['values'][6]))


def update_usr():
    if username.get() == '' or password.get() == '' or name.get() == '' or branch.get() == '' or email.get() == '':
        messagebox.showerror('Error', 'Student details are must')
    else:
        cursor.execute("Select * from users")
        cursor.execute(
            "UPDATE users SET username= %s,password= %s,name= %s,email= %s,branch= %s,events= %s,points= %s WHERE username = %s",
            (username.get(),
             password.get(),
             name.get(),
             email.get(),
             branch.get(),
             events.get(),
             points.get(),
             username.get()),
        )
        if messagebox.askyesno('Prompt', 'Do you want to commit this operation ?'):
            mydb.commit()
            messagebox.showinfo("Table Updated", f"Details for {username.get()} updated successfully")
            clear()


def del_usr():
    if messagebox.askyesno("Prompt", "THE DATA WILL BE DESTROYED.\n PROCEED ?"):
        cursor.execute("delete from users where username=%s", username.get())
        mydb.commit()
        clear()


def add_new():
    if name.get() == '' or branch.get() == '' or email.get() == '':
        messagebox.showerror('Error', 'User details are must')
    else:
        cursor.execute("Select * from users")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == username.get() or row[3] == email.get():
                messagebox.showerror('Error', 'Duplicate entry not allowed')
                return

        cursor.execute("Insert into users values(%s,%s,%s,%s,%s,%s,%s)",
                       (username.get(),
                        password.get(),
                        name.get(),
                        email.get(),
                        branch.get(),
                        events.get(),
                        points.get())
                       )
        mydb.commit()
        clear()


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))  # better to set timeout as well
        state = "ONLINE"
        colour = "#47E019"
    except OSError:
        state = "OFFLINE"
        colour = "#FF0000"
    light.config(text=state, font=('Calibri', 11, 'bold'), bg=colour, fg='white')
    root.after(1000, is_connected)  # do checking again one second later


def get_YID():
    cursor.execute("Select * from users")
    rows = cursor.fetchall()

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")[-2:]

    if year == rows[len(rows) - 1][0][1:3]:
        letter = rows[len(rows) - 1][0][3]
        index = string.ascii_uppercase.index(letter)
        if int(rows[len(rows) - 1][0][-4:]) == 9999:
            yID = 'Y' + year + string.ascii_uppercase[index + 1] + ''.join(str(1).zfill(4))
        else:
            count = int(rows[len(rows) - 1][0][-4:]) + 1
            yID = 'Y' + year + letter + ''.join(str(count).zfill(4))
    else:
        yID = 'Y' + year + 'A' + ''.join(str(1).zfill(4))

    return yID

def callback(url):
   webbrowser.open_new_tab(url)


# Variables and Connections
mydb = pymysql.connect(host='sql6.freemysqlhosting.net',
                   user='sql6468111',
                   password='qTZs7J6xij',
                   database='sql6468111')
cursor = mydb.cursor()
root = Tk()
search_txt = StringVar()
username = StringVar()
password = StringVar()
name = StringVar()
email = StringVar()
branch = StringVar()
events = IntVar()
points = IntVar()

# Mainframe Section
link = Label(root, text="https://yuvarset.herokuapp.com", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e:
callback("https://yuvarset.herokuapp.com"))

title = tk.Label(root, text='YUVA Member Management System', font=('Calibri', 20, 'bold'), bg='white', fg='black', bd=10, relief=FLAT)
title.pack(side=tk.TOP,fill=tk.X)

light = tk.Label(root, text='Checking ...', bg='white')
light.pack(side=tk.TOP, anchor=tk.NE, fill=tk.X)

wm = Label(root, text="v1.0 © Copyright 2022, danielkokkaravalel", font=('Calibri', 9))
wm.pack(side=tk.BOTTOM, padx=10)

wrapper1 = LabelFrame(root, text="Member List")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text="Member Data")

wrapper1.pack(fill="both", expand=1, padx=20, pady=10)
wrapper2.pack(fill="both", expand=1, padx=20, pady=10)
wrapper3.pack(fill="both", expand=1, padx=20, pady=10)

# Table Section
trv_scroll = Scrollbar(wrapper1)
trv_scroll.pack(side=RIGHT, fill=Y)

trv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=10, yscrollcommand=trv_scroll.set)
trv.pack()

trv_scroll.config(command=trv.yview)


trv.heading(1, text='Username')
trv.column(1, minwidth=0, width=80, stretch=NO)
trv.heading(2, text='Password')
trv.column(2, minwidth=0, width=80, stretch=NO)
trv.heading(3, text="Name")
trv.column(3, minwidth=0, width=200, stretch=NO)
trv.heading(4, text="Email")
trv.column(4, minwidth=0, width=200, stretch=NO)
trv.heading(5, text="Branch")
trv.column(5, minwidth=0, width=200, stretch=NO)
trv.heading(6, text="Events")
trv.column(6, minwidth=0, width=80, stretch=NO)
trv.heading(7, text="Points")
trv.column(7, minwidth=0, width=80, stretch=NO)

trv.bind('<Double 1>', getrow)

query = "SELECT * FROM users"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

# Search Section
lbl = Label(wrapper2, text="Enter :", font=('Calibri', 11))
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper2, textvariable=search_txt, width=30)
ent.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text="Search", cursor="hand2", command=search)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Clear", cursor="hand2", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)

# User Data Section
lbl1 = Label(wrapper3, text="Username", font=('Calibri', 11))
lbl1.grid(row=0, column=0, padx=5, pady=3)
en_username = Entry(wrapper3, textvariable=username, width=30)
en_username.grid(row=0, column=1, padx=5, pady=3)

lbl2 = Label(wrapper3, text="Password", font=('Calibri', 11))
lbl2.grid(row=0, column=2, padx=5, pady=3)
en_password = Entry(wrapper3, textvariable=password, width=30)
en_password.grid(row=0, column=3, padx=5, pady=3)

lbl3 = Label(wrapper3, text="Name", font=('Calibri', 11))
lbl3.grid(row=1, column=0, padx=5, pady=3)
en_name = Entry(wrapper3, textvariable=name, width=30)
en_name.grid(row=1, column=1, padx=5, pady=3)

lbl4 = Label(wrapper3, text="Email", font=('Calibri', 11))
lbl4.grid(row=1, column=2, padx=5, pady=3)
en_email = Entry(wrapper3, textvariable=email, width=30)
en_email.grid(row=1, column=3, padx=5, pady=3)

lbl5 = Label(wrapper3, text="Branch", font=('Calibri', 11))
lbl5.grid(row=1, column=4, padx=5, pady=3)
en_branch = ttk.Combobox(wrapper3, state='readonly', width=31, textvariable=branch)
en_branch['values'] = ('Mechanical',
                   'Computer Science',
                   'Electronics & Communication',
                   'Electronics & Electrical',
                   'Civil',
                   'Information Technology',
                   'Applied Electronics & Instrumentation',
                   'Computer Science & Business Systems',
                   'Artificial Intelligence & Data Science')
en_branch.grid(row=1, column=5, padx=5, pady=3, sticky='w')

lbl6 = Label(wrapper3, text="Events", font=('Calibri', 11))
lbl6.grid(row=2, column=0, padx=5, pady=3)
en_events = Entry(wrapper3, textvariable=events, width=30)
en_events.grid(row=2, column=1, padx=5, pady=3)

lbl7 = Label(wrapper3, text="Points", font=('Calibri', 11))
lbl7.grid(row=2, column=2, padx=5, pady=3)
en_points = Entry(wrapper3, textvariable=points, width=30)
en_points.grid(row=2, column=3, padx=5, pady=3)

# Buttons
add_btn = Button(wrapper3, text="ADD", font=('Calibri', 14, 'bold'), height=3, width=15, cursor="hand2", command=add_new)
add_btn.grid(row=7, column=0, padx=5, pady=3)
up_btn = Button(wrapper3, text="UPDATE", font=('Calibri', 14, 'bold'), height=3, width=15, cursor="hand2", command=update_usr)
up_btn.grid(row=7, column=2, padx=5, pady=3)
del_btn = Button(wrapper3, text="DELETE", font=('Calibri', 14, 'bold'), height=3, width=15, cursor="hand2", command=del_usr)
del_btn.grid(row=7, column=4, padx=5, pady=3)

root.geometry('1200x700')
root.title("YMMS")
#root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo.png'))

try:
    is_connected()# start the checking
    root.mainloop()

except:
    stem = tk.Tk()
    stem.overrideredirect(1)
    stem.withdraw()
    messagebox.showerror("Error", "Can't connect to MySQL server on 'sql6.freemysqlhosting.net'\nCheck Internet Connection")
    stem.destroy()
