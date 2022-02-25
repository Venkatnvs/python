from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
import pandas as pd

root = Tk()
root.title(" IP Project  ")
 
width = 1300
height = 768
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()

URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZIOetUvDjWOmtfB4YSBvQh8szCK7SIBQq7w&usqp=CAU" 
u = urlopen(URL)
raw_data = u.read() 
u.close()

im = Image.open(BytesIO(raw_data)) 
ia=im.resize((130,80),Image.ANTIALIAS) 
photo8 = ImageTk.PhotoImage(ia)

def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, \npassword TEXT, \nfirstname TEXT, \nlastname TEXT)")


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


def LoginForm():
    clear()
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=94)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 30), bd=18, bg='cadet blue', fg="cornsilk")
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", image=photo8, compound=LEFT, font=('arial', 30), bd=18, bg='dark green', fg="cornsilk")
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 23))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 30), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 30), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18,'bold'), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", fg="blue", font=('arial', 12,'bold'))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)

def RegisterForm():
    clear()
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 30), bd=18, bg='cadet blue', fg="cornsilk")
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 30), bd=18, bg='dark green', fg="cornsilk")
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 30), bd=18, bg='cadet blue', fg="cornsilk")
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 30), bd=18, bg='dark green', fg="cornsilk")
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 30), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 30), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 30), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 30), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18,'bold'), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12,'bold'))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", (str(USERNAME.get( )), str(PASSWORD.get( )), str(FIRSTNAME.get( )), str(LASTNAME.get( ))))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()
        
def clear():

    USERNAME.set("")

    PASSWORD.set("")

    FIRSTNAME.set("")

    LASTNAME.set("")        
        
def mainscr():
    login_sucess()
 	        
 
def de():
    f = open('output.csv', 'w') 
    # Create a connection and get a cursor 
    connection = sqlite3.connect('db_member.db') 
    cursor = connection.cursor() 
    # Execute the query 
    cursor.execute('select * from member') 
    # Get data in batches 
    while True:
        # Read the data 
        df = pd.DataFrame(cursor.fetchmany(1000))
        # We are done if there are no data 
        if len(df) == 0:
           break 
       # Let's write to the file 
        else:
           df.to_csv(f, header=False) 
    # Clean up 
    f.close() 
    cursor.close() 
    connection.close()
    



def login_sucess():

    global login_success_screen

    login_success_screen = Tk()

    login_success_screen.title("Success")

    login_success_screen.geometry("250x150")

    Label(login_success_screen, fg='green', bg='lime', width='29', text="Login Success", font=("calibri", 18)).pack()

    Label(login_success_screen, text="").pack()

    Button(login_success_screen, text="OK", fg='turquoise', bg='black', font=("bold"), command=delete_login_success).pack()

    Label(login_success_screen, text="").pack()	                        
def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            import time
            time.sleep(3)
        #    root.destroy()
            print('Hi....')
            print('Thanks for regiatration ')
            de()
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
LoginForm()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

if __name__ == '__main__':
    root.mainloop()
   

