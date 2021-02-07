
    # -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:05:12 2020

@author: Mohammad Azimi
https://www.youtube.com/azimypc
"""

import requests,json
import array as arr
from tkinter import *
import tkinter as tk
from tkinter import ttk
import textwrap
from tkinter.ttk import Combobox



#get Requst

ip = '192.168.12.20'
host = 'http://' + ip + '/api/v2.0.0/'

# Format headers

headers = {}
headers['Content-Type'] = 'application/json'
headers['Authorization'] = 'Basic YWRtaW46NWM4YTk0NjdiNzQ0MDYxN2IyMzFmNDMwNDk0OTYzYjExZWRiNzdlY2JiYTAxMDZlY2NiYzBiOTVkYjMxYTRhZg=='


win = tk.Tk()
win.title("Mir:R-1119")
win.geometry("700x400" ) 
win.configure(bg = 'orange')   
       
listbox = Listbox(win , height=100 , width=50 , selectbackground="red")
listbox.pack()
listbox.place(x=130 ,y =23)

listbox1 = Listbox(win )
listbox1.pack()
listbox1.place( x = 3 , y= 23)


#Battery Information Akku
BatteryLabel = Label(win ,text = '' , font=("Helvetica" , 20))
BatteryLabel.pack(side=BOTTOM , fill='x')
BatteryLabel.place()

labelName = Label(win , text = '' , bg="black" , fg= 'beige' , font=("Helvetica" , 12))
labelName.pack(side=BOTTOM , fill='x')
labelName.place()


LBMission = Label(win , text='---Mission List---' , bg='orange')
LBMission.pack()
LBMission.place(x = 230 , y=0)

LBMission_G = Label(win , text='--- List Groups---' , bg='orange')
LBMission_G.pack()
LBMission_G.place(x = 10 , y=0)


#Rede info abute Battery
get_missions = requests.get(host + 'status' , headers = headers)
Battery=get_missions.text.splitlines() # alternative: a_missions_temp=obj_get_missions.content.splitlines()
GetBatteryrocent = ""

BatteryInfo = '"battery_percentage"'
ListBattery = len(Battery) 
for i in range(ListBattery):
    temp_str = str(Battery[i]) 
    if str('"battery_percentage"') in temp_str:
       if BatteryInfo in temp_str:
           
            GetBatteryrocent = Battery[i].split(':')[1].split('.')[0]
    
            BatteryLabel.config(text= 'Akku:' +GetBatteryrocent + '%' )
            BattryValueInt = int(GetBatteryrocent)
            
            
            
obj_get_missions = requests.get(host + 'missions' , headers = headers)

a_missions_temp=obj_get_missions.text.splitlines() 
  
 

#-------------------for Show List of Mission_Groups-------------Start------
get_missions_groups = requests.get(host + 'mission_groups' ,  headers = headers)

mission_Sort=get_missions_groups.text.splitlines() 

Result_Serch = ""

Sort_Name = '"name"'


mission_list_Group = len(mission_Sort) 

for g in range(mission_list_Group):
    temp_str_groups = str(mission_Sort[g])
         
    if str('"name"') in temp_str_groups:
        if Sort_Name in temp_str_groups:
            
            Result_Serch = mission_Sort[g].split(',')[0].split(':')[1].split('"')[1]
            
            for Res in range(1):
               
                listbox1.insert(Res , Result_Serch)
#-------------------for Show List of Mission---------------End-----            
           
def SendData():
    getsubject_uid_temp = ""
    subject_name_temp = listbox.get(ANCHOR)
    mission_list_length = len(a_missions_temp) 

    for i in range(mission_list_length):
        temp_str = str(a_missions_temp[i])
        if str('"name"') in temp_str:
           if subject_name_temp in temp_str:
              getsubject_uid_temp = a_missions_temp[i-1].split(',')[0].split(':')[1].split('"')[1]
              mission_id = {"mission_id":getsubject_uid_temp}  
              post_mission = requests.post(host + 'mission_queue' , json = mission_id , headers = headers)  
              labelName.config(text=listbox.get(ANCHOR) + ': ' + getsubject_uid_temp)
              
           
             
def GroupSort():
    listbox.delete(0,END)
    getsubject_uid_group = ""
    subject_name__group_Name = listbox1.get(ANCHOR)#'Azimi-Gruppe' #fromListBox input
    mission_list_lengths = len(mission_Sort) 
    for i in range(mission_list_lengths):
        temp_strs = str(mission_Sort[i])
        if str('"name"') in temp_strs:
           if subject_name__group_Name in temp_strs:
              getsubject_uid_group = mission_Sort[i-1].split(',')[0].split(':')[1].split('"')[1]
              print(getsubject_uid_group)
              getListMission = requests.get(host+ '/mission_groups/'+getsubject_uid_group+'/missions' , headers = headers)
              print("---------------------")
              print(getListMission.text)
              a_missions_temp_Id=getListMission.text.splitlines() 
              getsubject_uid_temp = ""
              subject_name_temp = '"name"'
              ListNameMission = ""
              mission_list_length = len(a_missions_temp_Id) 
    for i in range(mission_list_length):
        temp_str = str(a_missions_temp_Id[i])
        if str('"name"') in temp_str:
           if subject_name_temp in temp_str:
              ListNameMission =  a_missions_temp_Id[i].split(',')[0].split(':')[1].split('"')[1]
              print(ListNameMission) # Output in List
              for Rows in range(1):
                listbox.insert(Rows , ListNameMission)
         
    
      

def Delete():
    post_mission = requests.delete(host + 'mission_queue' ,  headers = headers) 
    
    

#--------------------------Pause and Rady Srart------------------  



def RadyPause():
    obj_get_states = requests.get(host+ 'status' ,   headers = headers)
    #print(obj_get_states.text)
    a_states_temp = obj_get_states.text.splitlines()
    
    set_status = dict(Ready=3,Pause=4,ManualControl=11)
    set_status_list=list(set_status)
    set_status_keys=list(set_status.keys())
    set_status_values=list(set_status.values())
    ListStatus = len(a_states_temp)
    for i in range(ListStatus):
        temp_str = str(a_states_temp[i])
        if str('"state_id"') in temp_str:
            ListStates =  a_states_temp[i].split(',')[0].split(':')[1].split('"')[0]
            if str(set_status_values[0]) in ListStates:
                set_value ={"state_id":4}
                requests.put(host+ 'status' , json = set_value,  headers = headers)
                print(ListStates)
            elif str(set_status_values[1]) in ListStates:
                set_value ={"state_id":3}
                requests.put(host + 'status' , json = set_value,  headers = headers)
                print(ListStates)
             
#-------------------- pause and Rady-------------------------- END  
b=StringVar()

def com():
    c=b.get()
    
    
    getsubject_uid_temp = ""
    subject_name_temp = c
    mission_list_length = len(a_missions_temp) 

    for i in range(mission_list_length):
        temp_str = str(a_missions_temp[i])
        if str('"name"') in temp_str:
           if subject_name_temp in temp_str:
              getsubject_uid_temp = a_missions_temp[i-1].split(',')[0].split(':')[1].split('"')[1]
              mission_id = {"mission_id":getsubject_uid_temp}  
              post_mission = requests.post(host + 'mission_queue' , json = mission_id , headers = headers)  
              text.delete(0 , END)
              return





    
btnx = Button(text='Execute Barcode' , command=com)
btnx.place(x=500 , y=50) 
  
text = Entry(textvariable=b)
text.place(x=500 ,y= 25)




btnsm = Button(win , text="-----Select-----" , command=GroupSort)
btnsm.pack()        
btnsm.place(x=3 ,y= 200)

btns = Button(win , text="-----Play/Pause-----" , command=RadyPause)
btns.pack()        
btns.place(x=3 ,y= 230)  

         
btn = Button(win , text="-----Send Data-----" , command=SendData)
btn.pack()        
btn.place(x=3 ,y= 260)  

btnDelete = Button(win , text= "----Delete----" , command=Delete)
btnDelete.pack()
btnDelete.place(x = 3 , y=290 )           
win.mainloop() 

