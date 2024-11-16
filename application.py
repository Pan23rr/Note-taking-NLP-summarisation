import tkinter as tk
import re
from tkinter import ttk
import sqlite3 as sql
from tkinter import font
import databaseManage as db
import hashlib
from tkinter import messagebox
import TFIDF
import textRank

appdb=sql.connect('applicationDB.db')
CurrentUser=None


appdb.execute('''CREATE TABLE IF NOT EXISTS USERS(
  USERID INTEGER PRIMARY KEY AUTOINCREMENT,
  NAME VARCHAR(100),
  EMAIL VARCHAR(100) UNIQUE,
  PASSWORD VARCHAR(100) NOT NULL
);
''')


appdb.execute('''CREATE TABLE IF NOT EXISTS NOTES(
  UID INT,
  NOTESID INTEGER PRIMARY KEY AUTOINCREMENT,
  CONTENT VARCHAR(1000),
  TITLE VARCHAR(1000),
  FOREIGN KEY (UID) REFERENCES USERS(USERID)
);
''')



def hash_pass(password):
  hashed_pass=hashlib.sha256(b'f{password}').hexdigest()
  return hashed_pass



class app(tk.Tk):
    def __init__(self,title,shape):
        super().__init__()
        self.title(title)
        self.geometry(f'{shape[0]}x{shape[1]}')

def onfocus(_,defaultText,entryWi:ttk.Entry):
  if entryWi.get()==defaultText:
    entryWi.delete(0,"end")
    entryWi.insert(0,"")
    entryWi.config(background='gray')
    
def focusOut(_,defaultText,entryWi:ttk.Entry):
  if entryWi.get()=="":
    entryWi.insert(0,defaultText)
    entryWi.config(background='white')




def noteLoad(content,title,Window:tk.Frame,noteID):
    
    def saveNote(content,title):
       notei=db.getNoteID(CurrentUser,title,appdb)
       if len(notei)>0:
          db.updateNote(CurrentUser,notei[0][0],content,appdb)
       else:
          db.addNote(CurrentUser,content,title,appdb)
    def summarize(content,windo,summaryArea:tk.Text):
       if len(content)<60:
          messagebox.showwarning('Need more content',message="Please give more content for summarization")
          return
       prompt=""
       response=textRank.mainSummary(content)
       summaryArea.config(state='normal')
       summaryArea.delete('1.0',tk.END)
       summaryArea.insert("1.0",response)
       summaryArea.config(state='disabled')


    titleL = ttk.Entry(Window, width=50)
    if len(title) > 0:
        titleL.insert(0, title)
    titleL.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    contenttext=tk.StringVar()
    contentWin = tk.Text(Window, width=60, height=20)
    if content is not None:
        contentWin.insert("1.0", content) 
    contentWin.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    
    saveBut = ttk.Button(Window, text="Save Note",command=lambda : saveNote(contentWin.get("1.0", "end-1c"),titleL.get()))
    saveBut.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    
    Summarize = ttk.Button(Window, text="Summarize Note",command=lambda : summarize(contentWin.get("1.0",'end-1c'),Window,summaryArea))
    Summarize.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    summaryArea=tk.Text(Window)
    summaryArea.grid(row=3,column=0,columnspan=2)
    summaryArea.config(state='disabled')

    
    Window.place()








def registration():
    def checkEmail(email):
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email) is not None
    def register(userName,userEmail,userPassword):
        rightFormat=checkEmail(userEmail)
        hash_password=hash_pass(userPassword)
        success=db.newUser(userName,userEmail,hash_password,appdb)
        if success:
            messagebox.showinfo(title="User Registered",message="You can login into you account using the email and password")
            registrationWindow.destroy()
        else:
            messagebox.showerror(title="User cant be registered",message="Email was used before")
  


    registrationWindow=app('New User Registration', (400,400))
    userEmail=tk.StringVar(value='Enter your email')
    userPassword=tk.StringVar(value='Enter your password')
    userName=tk.StringVar(value="Enter your name")
    informationFrame=ttk.Frame(registrationWindow)
    nameEntry=ttk.Entry(informationFrame,textvariable=userName)
    nameEntry.insert(0,"Enter your name")
    nameEntry.pack()
    nameEntry.bind('<FocusIn>',lambda event: onfocus(event,'Enter your name',nameEntry))
    nameEntry.bind('<FocusOut>',lambda event: focusOut(event,'Enter your name',nameEntry))
    emailEntry=ttk.Entry(informationFrame,textvariable=userEmail)
    emailEntry.insert(0,"Enter your email")
    emailEntry.pack()
    emailEntry.bind('<FocusIn>',lambda event: onfocus(event,'Enter your email',emailEntry))
    emailEntry.bind('<FocusOut>',lambda event: focusOut(event,'Enter your email',emailEntry))
    passwordEntry=ttk.Entry(informationFrame,textvariable=userPassword)
    passwordEntry.insert(0,"Enter your password")
    passwordEntry.pack()
    passwordEntry.bind('<FocusIn>',lambda event: onfocus(event,'Enter your password',passwordEntry))
    passwordEntry.bind('<FocusOut>',lambda event: focusOut(event,'Enter your password',passwordEntry))
    confirmationbtn=ttk.Button(informationFrame,text="Register!",command= lambda: register(nameEntry.get(),emailEntry.get(),passwordEntry.get()))
    confirmationbtn.pack()
    informationFrame.place(relx=0.4,rely=0.5)
    registrationWindow.mainloop()


def loginWindow():
  def checkLogin(email,password):
    global CurrentUser
    hash_password=hash_pass(password)
    valid,ID=db.validUser(email,hash_password,appdb)
    if valid :
      messagebox.showinfo("Successfully logged in",message="User logged in successfully")
      loginWindow.destroy()
      CurrentUser=ID
    else:
      messagebox.showerror("Invalid Credentials",message="Please enter a valid email or password")
      return

  loginWindow=app('Login to your account', (600,500))
  credentialFrame=ttk.Frame(loginWindow)
  credentialFrame.place(relx=0.4,rely=0.5)
  email=tk.StringVar(value="Registered Email")
  password=tk.StringVar(value="Password")
  emailentry=ttk.Entry(credentialFrame,textvariable=email)
  passwordentry=ttk.Entry(credentialFrame,textvariable=password)
  credentialFrame.columnconfigure((0,1),weight=1)
  credentialFrame.rowconfigure((0,1,2,3),weight=1)
  emailentry.grid(row=0,column=0,columnspan=2)
  passwordentry.grid(row=1,column=0,columnspan=2)
  loginButton=ttk.Button(credentialFrame,text="Login",command=lambda : checkLogin(email.get(),password.get()))
  registrationButton=ttk.Button(credentialFrame,text="New User Registration",command= registration)
  loginButton.grid(row=2,column=0,columnspan=2)
  registrationButton.grid(row=3,column=0,columnspan=2)

  emailentry.bind('<FocusIn>',lambda event: onfocus(event,'Registered Email',emailentry))
  emailentry.bind('<FocusOut>',lambda event: focusOut(event,'Registered Email',emailentry))

  passwordentry.bind('<FocusIn>',lambda event: onfocus(event,'Password',passwordentry))
  passwordentry.bind('<FocusOut>',lambda event: focusOut(event,'Password',passwordentry))

  loginWindow.mainloop()

loginWindow()

if CurrentUser is None:
   exit()

MainWindow=app("NOTION",(800,800))

notesList=ttk.Frame(MainWindow)
notesList.place(x=0,y=0,relwidth=0.3,relheight=1)

notesOption=ttk.Frame(MainWindow)
notesOption.place(relx=0.4,relwidth=0.7,relheight=1)
notes=db.getallNotes(CurrentUser,appdb)
newNote=ttk.Button(notesList,text="New Note",command= lambda: noteLoad("","",notesOption,''))
Allnotes=ttk.Treeview(notesList,columns=('NoteID','title'),show='headings')
for i in notes:
   Allnotes.insert('',0,values=(i[0],i[1]))
Allnotes.place(relx=0,rely=0,relheight=0.8)
newNote.place(relx=0.1,rely=0.9)


def loadSelected(_):
  noteID=0
  title=''
  for i in Allnotes.selection():
     items=Allnotes.item(i)['values']
     noteID=items[0]
     title=str(items[1])
  content=db.getNote(CurrentUser,noteID,appdb)[0][0]
  noteLoad(content,title,notesOption,noteID)


Allnotes.bind('<<TreeviewSelect>>',loadSelected)



MainWindow.mainloop()