import socket
import tkinter as tk 
from tkinter import Tk, messagebox
from tkinter import ttk 

import threading
from tkinter.constants import BOTH
from PIL import Image,ImageTk
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"



#option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"
LIST = "listall"

#GUI intialize
class GoldRate(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("600x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("800x600")
        else:
            self.geometry("500x300")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn muốn thoát chương trình?"):
            self.destroy()
            try:
                option = LOGOUT
                client.sendall(option.encode(FORMAT))
            except:
                pass

    def logIn(self,curFrame,sck):
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if user == "" or pswd == "":
                curFrame.label_notice = "Vui lòng nhập tên đăng nhập và mật khẩu"
                return 
       
            #notice server for starting log in
            option = LOGIN
            sck.sendall(option.encode(FORMAT))

            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input:", user)

            sck.recv(1024)
            print("s responded")

            
            sck.sendall(pswd.encode(FORMAT))
            print("input:", pswd)


            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)

            if accepted == "1":
                self.showFrame(HomePage)
                
                curFrame.label_notice["text"] = ""
            elif accepted == "2":
                curFrame.label_notice["text"] = "Sai tên đăng nhập hoặc mật khẩu"
            elif  accepted == "0":
                curFrame.label_notice["text"] = "Người dùng đã đăng nhập"

        except:
            curFrame.label_notice["text"] = "Lỗi: Server đang tạm dừng"
            print("Lỗi: Server đang tạm dừng ")

    def signUp(self,curFrame, sck):
        
        try:
        
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if pswd == "":
                curFrame.label_notice["text"] = "Mật khẩu không đúng"
                return 

            #notice server for starting log in
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))
            
            
            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input:", user)

            sck.recv(1024)
            print("s responded")

            sck.sendall(pswd.encode(FORMAT))
            print("input:", pswd)


            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)

            if accepted == "True":
                self.showFrame(HomePage)
                curFrame.label_notice["text"] = ""
            else:
                curFrame.label_notice["text"] = "Tên đăng nhập đã tồn tại"

        except:
            curFrame.label_notice["text"] = "Lỗi 404: Server đang tạm dừng"
            print("404")

    def logout(self,curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            accepted = sck.recv(1024).decode(FORMAT)
            if accepted == "True":
                self.showFrame(StartPage)
        except:
            curFrame.label_notice["text"] = "Lỗi: Server is not responding"





class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#DCDCDC")
        
        
        label_title = tk.Label(self, text="ĐĂNG NHẬP", font=("verdana", 17,"bold"),fg='black',bg="#DCDCDC")
        label_user = tk.Label(self, text="Tên đăng nhập",fg='#20639b',bg="#DCDCDC",font='verdana 12 ')
        label_pswd = tk.Label(self, text="Mật khẩu ",fg='#20639b',bg="#DCDCDC",font='verdana 12 ')
       
        self.label_notice = tk.Label(self,text="",bg="#DCDCDC")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="Đăng nhập", bg="#bdb76b",fg="#008000",command=lambda: controller.logIn(self, client)) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="Đăng ký",bg="#bdb76b",fg="#008000", command=lambda: controller.signUp(self, client)) 
        button_sign.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()

        button_log.pack()
        button_sign.pack()
   

# gold : ID	Ten	Gia Mua	Gia Ban	Tinh	Ngay

class HomePage(tk.Frame):
    def __init__(self, parent, controller):     
        tk.Frame.__init__(self, parent)
        
        self.configure(bg="#FAF0E6")
        
        logo=Image.open("C:\\Users\\Admin\\Desktop\\1_20120370_20120376_20120439\\Source\\computer.PNG")


        barde = ImageTk.PhotoImage(logo)   
        label1 = ttk.Label(self, image=barde) 
        
        label1.image = barde
        label1.place(x=289,y=190)
        logo=Image.open("C:\\Users\\Admin\\Desktop\\1_20120370_20120376_20120439\\Source\\gold.PNG")

        barde = ImageTk.PhotoImage(logo)   
        label1 = ttk.Label(self, image=barde) 
        
        label1.image = barde
        label1.place(x=1,y=200) 
        
        label_title = tk.Label(self, text="TRA CỨU TỶ GIÁ VÀNG VIỆT NAM", font=("verdana", 20,"bold"),fg='red',bg="#FAF0E6")
        lable_notification = tk.Label(self, text="Nhập ID và Ngày: ID+Ngày (SJC+12-12-2021)", font=("verdana", 10),fg='black',bg="#FAF0E6")
        button_back = tk.Button(self, text="Đăng xuất",bg="#bdb76b",fg='red', command=lambda: controller.logout(self,client))
        button_list = tk.Button(self, text="Danh sách toàn bộ", bg="#f0e68c",fg='#32cd32',command=self.listAll)

        self.entry_search = tk.Entry(self, width=45)

        button_search = tk.Button(self, text="Tìm kiếm",bg="#f0e68c",fg='#32cd32', command=self.searchID)

        label_title.pack(pady=10)
        lable_notification.pack(pady=10)
        button_search.configure(width=20)
        button_list.configure(width=20)
        button_back.configure(width=20)

        self.entry_search.pack()
        self.label_notice = tk.Label(self, text="", bg="#DCDCDC" )
        self.label_notice.pack(pady=4)

        button_search.pack(pady=2)
        button_list.pack(pady=2) 
        button_back.pack(pady=2)

        self.frame_detail = tk.Frame(self, bg="steelblue1")
        
        self.label_gold = tk.Label(self.frame_detail,bg="steelblue1", text="", font=("verdana", 13,"bold"))
        self.label_time = tk.Label(self.frame_detail,bg="steelblue1", text="", font=("verdana", 13,"bold"))
        self.label_status = tk.Label(self.frame_detail,bg="steelblue1", text="", font=("verdana", 13,"bold"))


      #self.style = Style()
        
    
        

        self.label_gold.pack(pady=10)
        self.label_time.pack(pady=10)
        self.label_status.pack(pady=10)       


        self.frame_list = tk.Frame(self, bg="red")
        
        self.tree = ttk.Treeview(self.frame_list)

        
        self.tree["column"] = ("Tên Vàng", "Giá Mua", "Giá Bán", "Ngày")
         
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Tên Vàng", anchor='c', width=140)
        self.tree.column("Giá Mua", anchor='c', width=100)
        self.tree.column("Giá Bán", anchor='c', width=100)
        self.tree.column("Ngày", anchor='c', width=100)


        self.tree.heading("0", text="", anchor='c')
        self.tree.heading("Tên Vàng", text="Tên Vàng", anchor='c')
        self.tree.heading("Giá Mua", text="Giá Mua", anchor='c')
        self.tree.heading("Giá Bán", text="Giá Bán", anchor='c')
        self.tree.heading("Ngày", text="Ngày", anchor='c')

        
        self.tree.pack(pady=10)
        
    
    def recievegoldrate(self):
        gold = []
    
        gold_list = []
        data = ''
        while True:
            data = client.recv(1024).decode(FORMAT)
            client.sendall(data.encode(FORMAT))
            if data == "end":
                break
            
            # gold : [Ten]	[Gia Mua]	[Gia Ban]	[Ngay]
            for i in range(4):
                data = client.recv(1024).decode(FORMAT)
                client.sendall(data.encode(FORMAT))
                gold.append(data) 

            
            gold_list.append(gold)
            gold = []
        return gold_list

    def listAll(self):
        try:
            self.frame_detail.pack_forget()

            option = LIST
            client.sendall(option.encode(FORMAT))
            
            gold_list = self.recievegoldrate()
            
            x = self.tree.get_children()
            
            for item in x:
                self.tree.delete(item)

            i = 0
            for m in gold_list:
                self.tree.insert(parent="", index="end", iid=i, 
                        values=( m[0], m[1], m[2], m[3]))
                
                i += 1

            self.frame_list.pack(pady=10)
        except:
            self.label_notice["text"] = "Lỗi"
            
    def Recieve_ListGold_ID(self):   
        gold = []
        gold_list = []
        data = ''
        while True:
            data = client.recv(1024).decode(FORMAT)
            client.sendall(data.encode(FORMAT))

            if data == "end":
                break
            for i in range(4):
                data = client.recv(1024).decode(FORMAT)
                client.sendall(data.encode(FORMAT))
                gold.append(data) 
                
            gold_list.append(gold)
            
            gold = []
        return gold_list
    
    def searchID(self):
        try:
            self.label_notice["text"] = ""
            id = self.entry_search.get()    
            if (id == ""):
                self.label_notice["text"] = "Vui lòng nhập tên vàng để tra cứu"
                return

            option = SEARCH
            client.sendall(option.encode(FORMAT))

            self.frame_list.pack_forget()

            client.sendall(id.encode(FORMAT))
            
            msg = client.recv(1024).decode(FORMAT)
                
            if (msg == "noid"):
                print("no id")
                self.label_notice["text"] = "Tên vàng không tồn tại"
                return
                
            elif (msg == "ok"):
                print("ok")
                res = self.Recieve_ListGold_ID()

                x = self.tree.get_children()
                
                for item in x:
                    self.tree.delete(item)

                i = 0
                for m in res:
                    self.tree.insert(parent="", index="end", iid=i, 
                        values=( m[0], m[1], m[2], m[3]))
                    
                    i += 1
            self.frame_list.pack(pady=10)
                           
        except:
            self.label_notice["text"] = "Lỗi"


    


#GLOBAL socket initialize
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
client.connect(server_address)


app = GoldRate()



#main
try:
    app.mainloop()
except:
    print("Lỗi 404: Server đang tạm dừng")
    client.close()

finally:
    client.close()
