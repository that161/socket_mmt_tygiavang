import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import datetime
import socket
from PIL import Image,ImageTk
import threading
import requests
from bs4 import BeautifulSoup
import pyodbc
response = requests.get("https://www.24h.com.vn/gia-vang-hom-nay-c425.html")

HOSTNAME="DESKTOP-C1VSI5K"
HOST = "127.0.0.1"
PORT = 65432
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"

#define sever name and database name
SEVER_NAME=HOSTNAME+'\SQLEXPRESS'
DATABASE_NAME='Socket'

#option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"
LIST = "listall"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def ConnectToDB():
    server = SEVER_NAME
    database = DATABASE_NAME
    username = 'ttt' 
    password = '12345' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor


def check_day(day):
    cursor=ConnectToDB()
    cursor.execute("select Ngay from GiaVang")
    for row in cursor:
        if row==day:
          return True          
    return True
def data():
    soup = BeautifulSoup(response.content, "html.parser")
    div4 = soup.findAll('span','fixW')
    div1 = soup.findAll('h2')
    div2 = soup.findAll('td')
    dem=0
    list_name = []
    list_purchase_price = []
    list_price = []
    day=""
    month=""
    year=""
    dem = 0
    for item in div2:
        if (dem < 2):
          day=item.text[9:11]
          month= item.text[12:14]
          year = item.text[15:19]
        dem+=1
        if(dem==2):
            break
    for item in div4:
        if (dem %2==0):
            list_purchase_price.append(item.text)
        else:
            list_price.append(item.text)
        dem+=1
    dem=0
    for item in div1:

        if (dem>2 and dem<13):
            list_name.append(item.text)
        dem+=1
    date = str(day+"-"+month+"-"+year)
    cursor = ConnectToDB()
    if check_day(date): 
        cursor.execute( "delete from GiaVang where Ngay=(?)",(date)) 
    for i in range(len(list_name)):
        cursor.execute( "insert into GiaVang(TenVang,GiaMua,GiaBan,Ngay) values(?,?,?,?);",
        (list_name[i],list_purchase_price[i],list_price[i],date ))
        cursor.commit()

def Insert_New_Account(user,password):
    cursor=ConnectToDB()
    cursor.execute( "insert into TaiKhoan(TenDangNhap,MatKhau) values(?,?);",(user,password))
    cursor.commit()



def check_clientSignUp(username):
    cursor=ConnectToDB()
    cursor.execute("select TenDangNhap from TaiKhoan")
    for row in cursor:
        parse=str(row)
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        if parse_check == username:
            return False
    return True

Live_Account=[]
ID=[]
Ad=[]

def Check_LiveAccount(username):
    for row in Live_Account:
        parse= row.find("-")
        parse_check= row[(parse+1):]
        if parse_check== username:
            return False
    return True

def Remove_LiveAccount(conn,addr):
    for row in Live_Account:
        parse= row.find("-")
        parse_check=row[:parse]
        if parse_check== str(addr):
            parse= row.find("-")
            Ad.remove(parse_check)
            username= row[(parse+1):]
            ID.remove(username)
            Live_Account.remove(row)
            conn.sendall("True".encode(FORMAT))

       
def check_clientLogIn(username, password):
    
    cursor=ConnectToDB()
    cursor.execute("select T.TenDangNhap from TaiKhoan T")
    
    if Check_LiveAccount(username)== False:
        return 0
    
    for row in cursor:
        parse=str(row)
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        if parse_check == username:
            cursor.execute("select T.MatKhau from TaiKhoan T where T.TenDangNhap=(?)",(username))
            parse= str(cursor.fetchone())
            parse_check =parse[2:]
            parse= parse_check.find("'")
            parse_check= parse_check[:parse]
            if password== parse_check:
                return 1
    return 2


def clientSignUp(sck, addr):

    user = sck.recv(1024).decode(FORMAT)
    print("username:--" + user +"--")

    sck.sendall(user.encode(FORMAT))

    pswd = sck.recv(1024).decode(FORMAT)
    print("password:--" + pswd +"--")


    #a = input("accepting...")
    accepted = check_clientSignUp(user)
    print("accept:", accepted)
    sck.sendall(str(accepted).encode(FORMAT))

    if accepted:
        Insert_New_Account(user, pswd)

        # add client sign up address to live account
        Ad.append(str(addr))
        ID.append(user)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)

    print("end-logIn()")
    print("")

def clientLogIn(sck):

    user = sck.recv(1024).decode(FORMAT)
    print("username:--" + user +"--")

    sck.sendall(user.encode(FORMAT))
    
    pswd = sck.recv(1024).decode(FORMAT)
    print("password:--" + pswd +"--")
    
    accepted = check_clientLogIn(user, pswd)
    if accepted == 1:
        ID.append(user)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)
    
    print("accept:", accepted)
    sck.sendall(str(accepted).encode(FORMAT))
    print("end-logIn()")
    print("")


def getGold():
    cursor=ConnectToDB()
    cursor.execute("select * from GiaVang")
    res=[]
    for row in cursor:
        res.append(row)
    return res


def clientListGold(sck):
    gold_list = getGold()
    
    for gold in gold_list:
        msg = "next"
        sck.sendall(msg.encode(FORMAT))
        sck.recv(1024)

        for data in gold:
            data = str(data)
            sck.sendall(data.encode(FORMAT))
            sck.recv(1024)

    
    msg = "end"
    sck.sendall(msg.encode(FORMAT))
    sck.recv(1024)

def clientSearch(sck):

    id = sck.recv(1024).decode(FORMAT)

    check_id = ""
    check_date= ""
    count = 0
    for i in range(len(id)):
        if id[i] != '+':
            check_id += id[i]
            count += 1
        else: break
    
    for i in range(len(id)):
        if i > count:
            check_date += id[i]
       
    gold_list = getGold()
    if (check_date != "" and check_id != "All"):
        check = False
        for gold in gold_list:
            if gold[0] == check_id:
                goldcheck = str(gold[3])
                if goldcheck == check_date:
                    check = True
        if check == False:
            msg = "noid"
            sck.sendall(msg.encode(FORMAT))
            return
        else:
            msg = "ok"
            sck.sendall(msg.encode(FORMAT))
            for gold in gold_list:
                if gold[0] == check_id:
                    goldcheck = str(gold[3])
                    if goldcheck == check_date:
                        msg = "next"
                        sck.sendall(msg.encode(FORMAT))
                        sck.recv(1024)
                        for data in gold:
                            data = str(data)
                            sck.sendall(data.encode(FORMAT))
                            sck.recv(1024)    
            msg = "end"
            sck.sendall(msg.encode(FORMAT))
    elif (check_id == "All"):
        check = False
        for gold in gold_list:
            if gold[3] == check_date:
                check = True
        if check == False:
            msg = "noid"
            sck.sendall(msg.encode(FORMAT))
            return
        else:
            msg = "ok"
            sck.sendall(msg.encode(FORMAT))
            for gold in gold_list:
                if gold[3] == check_date:
                    msg = "next"
                    sck.sendall(msg.encode(FORMAT))
                    sck.recv(1024)
                    for data in gold:
                        data = str(data)
                        sck.sendall(data.encode(FORMAT))
                        sck.recv(1024)    
            msg = "end"
            sck.sendall(msg.encode(FORMAT))

    else:
        check = False
        for gold in gold_list:
            if gold[0] == check_id:
                    check = True
        if check == False:
            msg = "noid"
            sck.sendall(msg.encode(FORMAT))
            return
        else:
            msg = "ok"
            sck.sendall(msg.encode(FORMAT))
            for gold in gold_list:
                if gold[0] == check_id:
                    msg = "next"
                    sck.sendall(msg.encode(FORMAT))
                    sck.recv(1024)
                    for data in gold:
                        data = str(data)
                        sck.sendall(data.encode(FORMAT))
                        sck.recv(1024)    
            msg = "end"
            sck.sendall(msg.encode(FORMAT))


def handle_client(conn, addr):
   
    while True:

        option = conn.recv(1024).decode(FORMAT)


        if option == LOGIN:
            Ad.append(str(addr))
            clientLogIn(conn)
        
        elif option == SIGNUP:
            clientSignUp(conn, addr)


        elif option == LIST:
            clientListGold(conn)
        
        elif option == SEARCH:
            clientSearch(conn)

        elif option == LOGOUT:
            Remove_LiveAccount(conn,addr)


def runServer():
    
    try:
        data()

        print(HOST)
        print("Waiting for Client")
        while True:
            print("enter while loop")
            conn, addr = s.accept()


            clientThread = threading.Thread(target=handle_client, args=(conn,addr))
            clientThread.daemon = True 
            clientThread.start()
            
            
            #handle_client(conn, addr)
            print("end main-loop")

        
    except KeyboardInterrupt:
        print("error")
        s.close()
    finally:
        s.close()
        print("end")
 

# defind GUI-app class
class SearchGold_Admin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #self.iconbitmap('soccer-ball.ico')
        self.title("Sever")
        self.geometry("600x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)


    def showFrame(self, container):
        
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("500x300")
        else:
            self.geometry("600x300")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn muốn thoát chương trình?"):
            self.destroy()

    def logIn(self,curFrame):

        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if pswd == "":
            curFrame.label_notice["text"] = "Mật khẩu không được để trống"
            return 

        if user == "admin" and pswd == "server":
            self.showFrame(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "Tên đăng nhập hoặc mật khẩu không đúng"


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#DCDCDC")
        
        label_school = tk.Label(self, text="\nĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TPHCM", font=("verdana", 16,"bold"),fg='black',bg="#DCDCDC")
        label_title = tk.Label(self, text="ĐĂNG NHẬP VÀO SERVER", font=("verdana", 14,"bold"),fg='#20639b',bg="#DCDCDC")

        label_user = tk.Label(self, text="\nTên đăng nhập",fg='red',bg="#DCDCDC",font='verdana 10 bold')
        label_pswd = tk.Label(self, text="\nMật khẩu",fg='red',bg="#DCDCDC",font='verdana 10 bold')

        self.label_notice = tk.Label(self,text="",bg="#DCDCDC",fg='red')
        self.entry_user = tk.Entry(self,width=25,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=25,bg='light yellow')

        label_space = tk.Label(self, text="\n\n",fg='black',bg="#DCDCDC")
        button_log = tk.Button(self,text="LOG IN",font=("verdana", 12,"bold"), bg="#20639b",fg='black',command=lambda: controller.logIn(self))

        label_school.pack()
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        label_space.pack()
        button_log.pack()
        
        self.style = Style()
        logo=Image.open("C:\\Users\\Admin\\Desktop\\1_20120370_20120376_20120439\\Source\\flower.png")

        barde = ImageTk.PhotoImage(logo)   
        label1 = Label(self, image=barde) 

        label1.image = barde
        label1.place(x=1,y=110)
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1) 
        
        logo2=Image.open("C:\\Users\\Admin\\Desktop\\1_20120370_20120376_20120439\\Source\\flower.png")
        
        barde = ImageTk.PhotoImage(logo2)   
        label1 = Label(self, image=barde) 

        label1.image = barde
        label1.place(x=360,y=110)
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)   

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg="#DCDCDC")
       
        label_title = tk.Label(self, text="\nTÀI KHOẢN HOẠT ĐỘNG\n", font=("verdana", 17,"bold"),fg='black',bg="#DCDCDC").pack()
        
        self.conent =tk.Frame(self)
        self.data = tk.Listbox(self.conent, height = 10, 
                  width = 40, 
                  bg='floral white',
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg='#20639b')
        
        button_log = tk.Button(self,text="Làm mới",bg="#20639b",fg='floral white',command=self.Update_Client)
        button_back = tk.Button(self, text="Đăng xuất",bg="#20639b",fg='floral white' ,command=lambda: controller.showFrame(StartPage))
        button_log.pack(side= BOTTOM)
        button_log.configure(width=10)
        button_back.pack(side=BOTTOM)
        button_back.configure(width=10)
        
        self.conent.pack_configure()
        self.scroll= tk.Scrollbar(self.conent)
        self.scroll.pack(side = RIGHT, fill= BOTH)
        self.data.config(yscrollcommand = self.scroll.set)
        
        self.scroll.config(command = self.data.yview)
        self.data.pack()
      
        # self.style.theme_use("default")
        # self.pack(fill=BOTH, expand=1) 
        
    def Update_Client(self):
        self.data.delete(0,len(Live_Account))
        for i in range(len(Live_Account)):
            self.data.insert(i,Live_Account[i])

sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()

        
app = SearchGold_Admin()
app.mainloop()


sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()

        
app = SearchGold_Admin()
app.mainloop()



