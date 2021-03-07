import PyConBehavior
#import tkinter

from tkinter import *
from tkinter import messagebox


my_connection = PyConBehavior.PyConFunction()
#register your name
my_connection.register_name('john')
receiver_name = ['david']
rec_msg=''
i = 0.05
def start_chat():
    while True:
        str_message = my_connection.get_server_message()
        if str_message != []:
            print(str(str_message))
            str_message = []
        my_connection.sleeptime(3)
        root.after(10000,start_chat)

def rec_mess():
    global i
    text_rec= Label(text = rec_msg,background='green', width = 8, height = 1).place(relx=0.05, rely=i)
    i+=0.06






def send_msg():    
    #send message using connection
    global i
    my_connection.tell_others_msg(receiver_name, message.get())
    text_send= Label(text = message.get(),background='blue', width = 8, height = 1).place(relx=0.8, rely=i)
    i += 0.05
    


root = Tk()
root.title('Test window')
root.geometry('350x350')

message = StringVar()
msg_entry = Entry(textvariable = message,width = 40).place(relx=0.05, rely=0.8)

btn = Button(root,text = 'Send', command =start_chat).place(relx=0.8, rely=0.8)
#btn = Button(root,text = 'Send', command =start_chat).place(relx=0.5, rely=0.8)
root.after(10000,start_chat)





#del my_connection



    

