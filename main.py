from cryptography.fernet import Fernet
from datetime import datetime
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import re
import shutil
import glob
from time import sleep
from datetime import datetime
import logging
import pyodbc
import pymcprotocol
from decimal import Decimal
import numpy as np
import struct
import threading
import serial as Serial
# importing the binascii module
import binascii
import clr 
import sys
import os
import socket
import random
import requests
import os.path
from pathlib import Path
import csv

import yaml
import os
import os.path
from pathlib import Path
print(Path.cwd())
yaml_path= str(Path.cwd())+"\\"+"setup.yaml"
print(yaml_path)

with open(yaml_path, 'r') as file:
      machineDetail = yaml.safe_load(file)

print(machineDetail['STATION_NAME'])
print(machineDetail['HOST_COGNEX_INSIGHT'])
print(machineDetail['PORT_COGNEX_INSIGHT'])
print(machineDetail['PORTRead_COGNEX_INSIGHT'])
print(machineDetail['HOST_IV3_1'])
print(machineDetail['PORT_IV3_1'])
print(machineDetail['HOST_IV3_2'])
print(machineDetail['PORT_IV3_2'])
print(machineDetail['HOST_IV2'])
print(machineDetail['PORT_IV2'])
print(machineDetail['COMPORT_BARCODE'])
print(machineDetail['COMPORT_SCANNER'])
print(machineDetail['COMPORT_SCANNER_BIT'])
print(machineDetail['DRIVE_LOG_FILE'])
print(machineDetail['MAIN_FOLDER_LOG_FILE'])
print(machineDetail['SUB_FOLDER_RESULT_FILE'])
print(machineDetail['MQTT_BROKER'])
print(machineDetail['MQTT_PORT'])
print(machineDetail['MQTT_TOPIC'])

#---------------------------------------------------------------------------------------
#HOST1 = "192.168.3.30"  # Standard loopback interface address (localhost) #IV3 #LCD
HOST1 = str(machineDetail['HOST_IV3_1'])
PORT1 = int(machineDetail['PORT_IV3_1'])
#PORT1 = 8500  # Port to listen on (non-privileged ports are > 1023)


#HOST3 = "192.168.3.23"  # Standard loopback interface address (localhost) #IV3 #PIN 
HOST3 = str(machineDetail['HOST_IV3_2'])
PORT3 = int(machineDetail['PORT_IV3_2'])
#PORT3 = 8500  # Port to listen on (non-privileged ports are > 1023)


#HOST6 = "192.168.3.26"  #Standard loopback interface address (localhost)  #IV2 #Switch
HOST6 = str(machineDetail['HOST_IV2'])
PORT6 = int(machineDetail['PORT_IV2'])
#PORT6 = 8500  # Port to listen on (non-privileged ports are > 1023)
#------------------------------------------------------------------------------------------

HOST7 = str(machineDetail['HOST_COGNEX_INSIGHT'])
PORT7 = int(machineDetail['PORT_COGNEX_INSIGHT'])
PORT8 = int(machineDetail['PORTRead_COGNEX_INSIGHT'])
#HOST7 = "192.168.3.50"  #Standard loopback interface address (localhost)  #COGNEX 
#PORT7 = 23  # Port to listen on (non-privileged ports are > 1023)
#PORT8 = 3000  # Port to listen on (non-privileged ports are > 1023)


#------------------------------------------------------------------------------------------
now = datetime.now()
timestamp = datetime.fromtimestamp(datetime.timestamp(now))
timestamp = timestamp.strftime("%Y-%m-%d-%H%M%S")
print(timestamp)
log_file_path = machineDetail['DRIVE_LOG_FILE']+ "\\" +machineDetail['SUB_FOLDER_LOGT_FILE']+"\\"+timestamp +'.log'
#log_file_path = 'C:\ZOLL_5368_FinalAOI\datalog\\'+timestamp+'.log'


ser = Serial.Serial(machineDetail['COMPORT_SCANNER'],machineDetail['COMPORT_SCANNER_BIT'],timeout=10)


#logging.basicConfig(filename = timestamp +'.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.basicConfig(
    level=logging.INFO, # Set the logging level (e.g., INFO, DEBUG, WARNING, ERROR)
    #filename = timestamp +'.log',
    #filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # FileHandler for writing logs to a file
        logging.StreamHandler()  # StreamHandler for displaying logs in the console
    ]
)
#------------------------------------------------------------------------------------------

os.getcwd()
print("Path is ",Path.cwd())
logging.info("Path is " + str(Path.cwd()))

os.chdir('C:\AOI_result')
print("New Path is ",Path.cwd())
logging.info("Path is " + str(Path.cwd()))
# current date and time

logging.info('This will get logged to a file')

client = mqtt.Client()
# current date and time
print("start")
logging.info("Start")

#------------------------------------------------------------------------------------------
broker = machineDetail['MQTT_BROKER']
port = machineDetail['MQTT_PORT']
topic = machineDetail['MQTT_TOPIC']
Scan=0
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
Tool_number = 0
LenghtResult = 0
Count = 0
Tool=[]
Capture_press = False
Tool_name =""
Start_time = ""
End_time = ""
SerialKey=""
StationID = "Final Inspection"
trace_sta_name ="ZOLL_KETL_FINAL_AOI_02"
FinalStatus =0
ModelBarcode = 0
t = 0
BC_Trac=""
client = mqtt.Client()
SorceCognexPath = ""
DestinationCognexPath=""
NoderedPath=""
SorceCognexfile =""
source_pathIV2= ""
SorceIV2file= ""
SorceIV3_01file= ""
SorceIV3_02file= ""
ResponseIV2 =0
ResponseIV3_01 =0
ResponseIV3_02 =0
ResponseCognex =0
Barcode =""              #
Result =""               #
topics_name = ""         #  
#-----------COGNEX
A6J1=0 #1
A6J2=0#2
R109=0#3
R110=0#4
D100=0#5
R101=0#6
R102=0#7
R103=0#8
R207=0#9
R240=0#10
T100=0#11
T101=0#12
T102=0#13
C132=0#14
C126=0#15
A3J7=0#16
Q101=0#17
Q103=0#18
Q104=0#19
A10J5=0#20
A9J3=0#21
RY100=0#22
L101=0#23
T103=0#24
T105=0#25
R105=0#26
R106=0#27
R107=0#28
R108=0#29
PCB=0#30
RTV_C126=0#31
RTV_C132=0#32
RTV_Q103=0#33

#-----------IV
SW500=0#34
A9J9=0#35
A9J10=0#36
U509=0#37
U523=0#38
PIN =0

#------------------------------------------------------------------------------------------------------
import ScadaMonitor 
from datetime import datetime

def scada_monitor():
    while True:
        try:    
            StationName = "ZOLL5368FinalAOI"
            Status= "RUN"
            Model= "A054G527"
            CycleTime= "10"
            Count="15"
            OEE="70"
            YIELD="90"
            RunTime="00:06:30"
            DownTime="00:00:00"
            IdleTime="00:01:20"
            Chktime = datetime.now()
            if(Chktime.second == 10):
                ScadaMonitor.SCADA_update_sql(StationName,Status,Model,CycleTime,Count,OEE,YIELD,RunTime,DownTime,IdleTime)
                print("SCADA_Update_SQL")
            sleep(1)
        except Exception as e:
            print(f'An error occurred : {e}')

def Treacibility_backcheck_data(barcodeR): #Define function backcheck after barcode have to check

    #try:

        print("Treacibility_backcheck_data ")
        logging.info('Treacibility_backcheck_data')
        directory = os.getcwd()
        print("directory",directory)
        logging.info('directory'+directory)
        sys.path.append(directory)
        print("assembly_path "+ str (directory))
        logging.info('assembly_path'+ str (directory))
        clr.AddReference("KETL_DLL_AOI_Backend")
        print("AddReference")
        logging.info('AddReference')
        from KETL_DLL_AOI_Backend import Main_Function
        bc = Main_Function()

        print("Treacibility_read_data OK1")
        logging.info('Treacibility_read_data OK')
        print("Treacibility_read_data OK barcodeR")
        rt_insert = bc.Backcheck_Data(str(barcodeR),trace_sta_name)


        print("Read =", str(rt_insert))
        logging.info('Read ='+ str(rt_insert))
        if rt_insert != "NODATA":
            print("Treacibility_backcheck_data Read complete=",str(rt_insert))
            logging.info("Backcheck completed ")  

        else:
            print("Treacibility_backcheck_data Read not complete!!")
            logging.error("Backcheck not completed ")  

        return rt_insert

#------------------------------------------------------------------------------------------------------
def pTRC_Insert_Process_Data(Barcode,Timestamp_start,Timestamp_end,Result): #Define function for insert data in DB
    #try:
       
        print("Treacibility_read_data ")
        logging.info("Treacibility_read_data")
        directory = os.getcwd()
        print("directory",directory)
        logging.info('directory'+directory)
        sys.path.append(directory)
        print("assembly_path ", str (directory))
        logging.info('assembly_path'+ str (directory))
        clr.AddReference("KETL_DLL_AOI_Backend")
        print("AddReference")
        logging.info('AddReference')
        from KETL_DLL_AOI_Backend import Main_Function

        bc = Main_Function()
        print("Type of ModelBarcode => ", type(Barcode))

        
        

        print("Treacibility_backcheck_data OK")
        logging.info("Treacibility_backcheck_data OK")
        rt_insert = bc.pTRC_Insert_Process_Data(Barcode,trace_sta_name,"Final Inspection AOI",Timestamp_start,Timestamp_end,Result)
        print ("Result ==",Result)

        print("Read =", str(rt_insert))
        logging.info("Read ="+ str(rt_insert))
        if rt_insert != "NODATA":
            print("pTRC_Insert_Process_Data Insert complete!!",str(rt_insert))
            logging.info("Insert data completed ")
            client.publish("Insert","Insert data completed ")

        else:
            print("pTRC_Insert_Process_Data not complete!!")
            logging.error("Insert data not completed ")  

        return rt_insert

#------------------------------------------------------------------------------------------------------
def Log_defect(Barcode,Type_Defect,componentList): #define function log defect for sending component and defect type to traceability

     #try:
     if Backchk == 1:
        print("Treacibility_log_defect => Start ")
        logging.info("Treacibility_log_defect => Start ")
        now = datetime.now()
        Timestamp = datetime.fromtimestamp(datetime.timestamp(now))
        Timestamp = Timestamp.strftime("%Y-%m-%d %H:%M:%S")
        directory = os.getcwd()
        print("directory",directory)
        logging.info("directory"+str(directory))
        sys.path.append(directory)
        print("assembly_path "+ str (directory))
        logging.info("assembly_path "+ str (directory))
        clr.AddReference("KETL_DLL_AOI_Backend")
        print("AddReference")
        logging.info("AddReference")
        from KETL_DLL_AOI_Backend import Main_Function
        bc = Main_Function()

        print("Treacibility_log_defect => OK")
        logging.info("Treacibility_log_defect => OK")
        rt_insert = bc.udp_AOITH_Log_Defect_By_Serial(Barcode,trace_sta_name,Type_Defect,componentList,1)   
        
        
        print("Read =", str(rt_insert))
        logging.info("Read ="+ str(rt_insert))
        if rt_insert != "NODATA":
            print("Log_defect Read complete=",str(rt_insert)) 
            logging.info("Log defect completed ")  

        else:
            print("Log_defect Read not complete!!")
            logging.error("Log defect not completed ") 

        return rt_insert        

#------------------------------------------------------------------------------------------------------
def Traceability_checkStatus():
   
   if Backchk == 1:
    print("Barcode is =>> ",Barcode)
    logging.info("Barcode is =>> " +str(Barcode))
    pTRC_Insert_Process_Data(Barcode.strip(),Start_time,End_time,Result)
    print("Open system_Traceability ")
    logging.info("Open system_Traceability ") 
    print("Backcheck_Param >>", Backchk) 
    logging.info("Backcheck_Param >>"+str( Backchk))
   
   if Backchk == 0:
    print("Close system_Traceability ")
    logging.info("Close system_Traceability ")
    print("Backcheck_Param >>", Backchk)   
    logging.info("Backcheck_Param >>"+str( Backchk))
#------------------------------------------------------------------------------------------------------

def InSightTrig(Host,Port,IV_Function):
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as IV_Function:
        IV_Function.connect((HOST7, PORT7))
        IV_Function.sendall(b"admin\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}")
        logging.info(f"Received {data!r}")
        IV_Function.sendall(b"\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}")
        logging.info(f"Received {data!r}")    
        IV_Function.sendall(b"MT\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}")
        logging.info(f"Received {data!r}")

        IV_Function.sendall(b"admin\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}")
        logging.info(f"Received {data!r}")
        IV_Function.sendall(b"\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}") 
        logging.info(f"Received {data!r}")   
        IV_Function.sendall(b"RB\r\n")
        print(f"Cognex")
        logging.info(f"Cognex")
        data = IV_Function.recv(1024)
        print(f"Received {data!r}")
        logging.info(f"Received {data!r}")
        IV_Function.close()

def InSightRead(Host,Port,IV_Function):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as IV_Function:
        IV_Function.connect((Host, Port)) 
        data = IV_Function.recv(1024)
        print(f"Received From Insight{data!r}")
        logging.info(f"Received From Insight{data!r}")
        IV_Function.close()
        return (data)
 

def IVTrig(Host,Port,IV_Function):
    Tool_name = IV_Function
    global SW500
    global PIN
    global U509 
    global U523
    global A9J3
    global A9J10
    global A9J9
    global SorceIV3_01file
    global SorceIV3_02file
    global SorceIV2file
    global ResponseIV2
    global ResponseIV3_01
    global ResponseIV3_02
    Tool_name = IV_Function
     
    print("-----------------------------------------------------------")
    print("Scan from IV = ",Scan)
    logging.info("Scan from IV = "+str(Scan))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as IV_Function:
            

            IV_Function.connect((Host,Port))
            IV_Function.sendall(b"T2\r\n")
            data = IV_Function.recv(1024)
            print(f"Received {data!r}")
            logging.info(f"Received {data!r}")
            print(type(data))
            logging.info(type(data))  
            Result = str(data).split(',')
            print(Result)
            logging.info(Result)  
            print(len(Result))
            logging.info(len(Result))
            LenghtResult = len(Result)
            print("Len of result = ",LenghtResult)
            Tool_number = (LenghtResult/3)-1
            print ("No of Tool is",int(Tool_number))
            logging.info("No of Tool is"+str(Tool_number))
            print("Tool name is",Tool_name)
            logging.info("Tool name is"+str(Tool_name))

            
            
    
            if (Tool_name == "SW500"):
                print("SW500 read...")
                logging.info("SW500 read...")
                #["b'RT", '00415', 'NG', '01', 'NG', '0000000', '02', 'NG', '0000020', '03', 'NG', '0000027', '04', 'NG', '0000014', '05', 'OK', "0000061\\r'"]

                #for Count in range (1,int(Tool_number)):
                  #if (Tool_number == 1 ):
                    #  Tool_RT=Result[2]
                    # Tool[Count]=Result((3*Count)+1)
                #print("Summary Result :" + Tool_RT )
                #print("Result :"+ Tool) 

                if (Tool_number == 2 ):
                    Tool_RT=Result[2]
                    Tool1=Result[4]
                    Tool2=Result[7]
                    print("Tool_RT" + Tool_RT )
                    logging.info("Tool_RT" + str(Tool_RT ))
                    print("SW500 result = " + Tool2)
                    logging.info("SW500 result = " + str(Tool2)) 
                    if (Tool_RT=="OK"):
                        SW500 = 1
                        client.publish("SW500",str(SW500))
                    else :
                        SW500 = 0
                        client.publish("SW500",str(SW500))
                        #Log_defect(ModelBarcode,"Part Not Placed (PNP)","SW500")

                    print ("SW500 =",SW500)
                    logging.info("SW500 ="+str(SW500))
                    ResponseIV2 =1
                else :
                    client.publish("ToolChanged","Tool SW500 ERROR,Please check !!")
                #ResponseIV2 =1

            if (Tool_name == "PIN"):
                print("PIN read...")
                logging.info("PIN read...")

                if (Tool_number == 3):
                    Tool_RT=Result[2] 
                    Tool1=Result[4] #A9J3
                    Tool2=Result[7] #A9J9_A9J10
                    Tool3=Result[10] #U523

                    print("Tool_RT1=",Tool_RT)
                    logging.info("Tool_RT1="+str(Tool_RT)) 
                    #------------------------------------A9J3
                    if (Tool1 == "OK")  :
                        A9J3 = 1
                    else :
                        A9J3 = 0
                       
                    print("A9J3 result = " , A9J3)
                    logging.info("A9J3 result = " +str(A9J3)) 
                    client.publish("A9J3",str(A9J3))
                    #------------------------------------A9J10
                    if (Tool2 == "OK"):
                        A9J10= 1
                    else :
                        A9J10= 0
                        
                    print("A9J10 result = " , A9J10)
                    logging.info("A9J10 result = " + str(A9J10))
                    client.publish("A9J10",str(A9J10))
                    #------------------------------------A9J9
                    if (Tool2 == "OK"):
                        A9J9= 1 
                    else :
                        A9J9= 0
                        
                    print("A9J9 result = ", A9J9) 
                    logging.info("A9J9 result = "+ str(A9J9)) 
                    client.publish("A9J9",str(A9J9))
                    #------------------------------------U509

                    if (Tool3 == "OK"):
                        U523= 1 
                    else :
                        U523= 0
                        
                    print("U523 result = ", U523) 
                    logging.info("U523 result = "+ str(U523))
                    client.publish("U523",str(U523))
                    #-----------------------------------------
                    if (Tool_RT == "OK"):
                            PIN = int(1)
                    else :
                            PIN = int(0)

                            #client.publish("A9J3","NG")TKA054Q
                            
                            #client.publish("A9J9","NG")
                            #client.publish("A9J10","NG")
                    print ("A9J9_A9J10_A9J3_U523 =",PIN)
                    logging.info ("A9J9_A9J10_A9J3_U523 ="+ str(PIN))
                    ResponseIV3_01 =1

                else :
                    client.publish("ToolChanged","Tool PIN ERROR,Please check !!")
                


            if (Tool_name == "U509"):
                print("U509 read...")
                logging.info("U509 read...")
                print("Tool_number =",str(Tool_number))
                if (Tool_number == 2 ):
                    Tool_RT=Result[7]
        
                    print("U509 result = ",str(U509))
                    logging.info("U509 result = "+ str(U509)) 
                    print("Tool_RT",Tool_RT)
                    logging.info("Tool_RT"+str(Tool_RT))
                    if (Tool_RT=="OK"):
                        U509 =1
                        client.publish("U509",str(U509))
                    else :
                        U509 =0
                        client.publish("U509",str(U509))
                        
                        
                    print ("U509 =",U509)
                    logging.info ("U509 ="+ str(U509))
                    ResponseIV3_02=1
                else :
                    client.publish("ToolChanged","Tool U509 ERROR,Please check !!")

            

def copy(src_path, dest_path ):
    # Copy the file
    print("src_path",src_path)
    print("dest_path",dest_path) 
    shutil.copy(src_path, dest_path)



def move_and_rename(SerialNo):
    global SorceCognexPath
    global DestinationCognexPath
    global NoderedPath
    global source_pathIV2 
    global SorceIV2file
    global SorceIV3_01file
    global SorceIV3_02file
    global new_file_name_cognex
    global new_file_name_path_Cognex
    global new_file_name_IV2
    global new_file_name_path_IV2
    global new_file_name_IV3_01
    global new_file_name_path_IV3_01
    global new_file_name_IV3_02
    global new_file_name_path_IV3_02

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    print ("Year = ",year)
    logging.info ("Year = "+str(year))
    print ("Month = ",month)
    logging.info ("Month = "+str(month))
    print ("Day = ",day)
    logging.info ("Day = "+str(day))
    #-------------------------------------------------------------------------------------------------------------
    list_of_files = glob.glob('C:\IV3_Capture\IV3_01\*.jpeg') # * means all if need specific format then *.csv
    SorceIV3_01file = max(list_of_files, key=os.path.getctime)
    print("SorceIV3_01file",SorceIV3_01file)
    list_of_files = glob.glob('C:\IV3_Capture\IV3_02\*.jpeg') # * means all if need specific format then *.csv
    SorceIV3_02file = max(list_of_files, key=os.path.getctime)
    print("SorceIV3_02file",SorceIV3_02file)
    list_of_files = glob.glob('C:\IV2_Capture\IV2\*.jpeg') # * means all if need specific format then *.csv
    SorceIV2file = max(list_of_files, key=os.path.getctime)
    print("SorceIV2file",SorceIV2file)
    #-------------------------------------------------------------------------------------------------------------
    n_timestamp = datetime.fromtimestamp(datetime.timestamp(now))
    n_timestamp = n_timestamp.strftime("%d%m%Y%H%M%S")
    DestinationCognexPath = '\\'+'\\'+machineDetail['NAS_IP']+'\\'+machineDetail['MAIN_FOLDER_AUTOMATE']+'\\'+machineDetail['MAIN_FOLDER_ZOLL']+'\\'+machineDetail['SUB_FOLDER_ZOLL']+'\\'+machineDetail['SUB_FOLDER_MAC']+'\\'+machineDetail['SUB_FOLDER_MAC_NAME']+'\\'+machineDetail['FOLDER_IMAGE']+'\\' + str(year)+'\\'+str(month)+'\\'+str(day)+'\\'+str(SerialNo)
 
    # check whether directory already exists
    if not os.path.exists(DestinationCognexPath):
        print("Don't have folder in Path!!")
        logging.info("Don't have folder in Path!!")
        os.makedirs(DestinationCognexPath)
        print("Created Folder !!")
        logging.info("Created Folder !!")
        

    else:
        print("Folder exist ")
        logging.info("Folder exist")   


        # check whether directory already exists
    if not os.path.exists(SorceCognexPath):
        print("Don't image file !!")
        #os.makedirs(DestinationCognexPath)
        logging.info("Copy image success !!")
    else:
        print("Image file exist")
        logging.info("Image file exist") 


  # Example usage
    #------------------------------------------------------------------------Cognex      
    source_path = 'C:\\COGNEX_Capture\\' 
    source_file = SorceCognexfile
    new_file_name_cognex = str(SerialNo)+"_"+str(n_timestamp)+"COGNEX_Capture"+".JPG"


    new_file_name_path_Cognex  =  DestinationCognexPath+ '\\' + new_file_name_cognex
    NoderedPath ='/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(SerialNo)+'/'+str(new_file_name_cognex)
    if not os.path.exists(new_file_name_path_Cognex):
        shutil.move(source_path+source_file, DestinationCognexPath)
        print("Successfully Created File_Cognex ")
        logging.info("Successfully File_Cognex ")
        os.rename(DestinationCognexPath+'\\'+source_file, new_file_name_path_Cognex)
        print("Successfully rename File ")
        logging.info("Successfully rename File ")
    else:
        print("Image file exist")
        logging.info("Image file exist") 
    #------------------------------------------------------------------------------IV2
    source_fileIV2 = SorceIV2file
    source_fileIV2_imageName = source_fileIV2.split("\\")
    print("source_fileIV2",source_fileIV2)
    print("source_fileIV2_imageName#1",source_fileIV2_imageName)
    print("source_fileIV2_imageName",source_fileIV2_imageName[3])

    new_file_name_IV2 = str(SerialNo)+"_"+str(n_timestamp)+"Capture_IV2"+".JPG"
    new_file_name_path_IV2  =  DestinationCognexPath+ '\\' + new_file_name_IV2

    if not os.path.exists(new_file_name_path_IV2):
        shutil.move(source_pathIV2+source_fileIV2, DestinationCognexPath)
        print("Successfully Created File_IV2 ")
        logging.info("Successfully File_IV2 ")
        os.rename(DestinationCognexPath+'\\'+source_fileIV2_imageName[3], new_file_name_path_IV2)
        client.publish("image_pathIV2",new_file_name_path_IV2) 
        print("Successfully rename File ")
        logging.info("Successfully rename File ")
    else:
        print("Image file exist")
        logging.info("Image file exist")     
  
    #---------------------------------------------------------------------------------IV3_1

    source_fileIV3_01 = SorceIV3_01file
    source_fileIV3_imageName = source_fileIV3_01.split("\\")
    print("source_fileIV3_01",source_fileIV3_01)
    print("source_fileIV3_imageName",source_fileIV3_imageName)
    new_file_name_IV3_01 = str(SerialNo)+"_"+str(n_timestamp)+"Capture_IV3_01"+".JPG"
    new_file_name_path_IV3_01  =  DestinationCognexPath+ '\\' + new_file_name_IV3_01

    if not os.path.exists(new_file_name_path_IV3_01):
        shutil.move(source_fileIV3_01, DestinationCognexPath)
        print("Successfully Created File_IV3_01 ")
        logging.info("Successfully File_IV3_01 ")
        os.rename(DestinationCognexPath+'\\'+source_fileIV3_imageName[3], new_file_name_path_IV3_01)
        client.publish("image_pathIV3_01",new_file_name_path_IV3_01) 
        print("Successfully rename File ")
        logging.info("Successfully rename File ")
    else:
        print("Image file exist")
        logging.info("Image file exist")     
    #------------------------------------------------------------------------------------IV3_02
    source_fileIV3_02 = SorceIV3_02file
    source_fileIV3_imageName2 = source_fileIV3_02.split("\\")
    print("source_fileIV3_02",source_fileIV3_02)
    print("source_fileIV3_imageName2",source_fileIV3_imageName2)
    new_file_name_IV3_02 = str(SerialNo)+"_"+str(n_timestamp)+"Capture_IV3_02"+".JPG"
    new_file_name_path_IV3_02  =  DestinationCognexPath+ '\\' + new_file_name_IV3_02

    if not os.path.exists(new_file_name_path_IV3_02):
        shutil.move(source_fileIV3_02, DestinationCognexPath)
        print("Successfully Created File_IV3_01 ")
        logging.info("Successfully File_IV3_01 ")
        os.rename(DestinationCognexPath+'\\'+source_fileIV3_imageName2[3], new_file_name_path_IV3_02)
        client.publish("image_pathIV3_02",new_file_name_path_IV3_02) 
        print("Successfully rename File ")
        logging.info("Successfully rename File ")
    else:
        print("Image file exist")
        logging.info("Image file exist")   

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            logging.info("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            logging.info("Failed to connect, return code %d\n", rc)

    client.on_message=on_message
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client



def on_message(client, userdata, msg):
        
    global t
    global Capture_press 
    global FinalStatus
    global Timestamp
    global End_time
    global Scan
    global SerialKey
    global ResponseIV2
    global ResponseIV3_01
    global ResponseIV3_02
    global ResponseCognex

            
    client.publish("Press_Capture","START")
    t = 1


    if (msg.topic == "imgshow"):
        print("imgshow")
        client.publish("IMG_Cognex",NoderedPath)


    if (msg.topic == "python/mqtt"):
        print("Press_Capture")
        serial_thread()
        print("serial_thread>> START")

        print("SCAN =",Scan)
        if (Scan == 1):
            IVTrig(HOST1,PORT1,"U509") #IV3 #LCD
            IVTrig(HOST3,PORT3,"PIN")  #IV3 #PIN
            IVTrig(HOST6,PORT6,"SW500") #IV2 #SW500
            InSightTrig(HOST7,PORT7,"Cognex")
            sleep(3)
            move_and_rename(ModelBarcode)
            
             
        else :
            print("Not complete scan",Scan)
            logging.info("Not complete scan "+str(Scan))
            client.publish("Status_backcheck","Not complete scan")

    if ((msg.topic == "ConfirmFinal")&(ResponseIV2 ==1)&(ResponseIV3_01==1)&(ResponseIV3_02==1)&(ResponseCognex==1)):
  #Check from Node-red Mqtt out after final status
        ConfirmFinal = str(msg.payload.decode("utf-8"))
        print("ConfirmFinal =",ConfirmFinal)
        print("ResponseIV2 =",str(ResponseIV2))
        print("ResponseIV3_01 =",str(ResponseIV3_01))
        print("ResponseIV3_02 =",str(ResponseIV3_02))
        print("ResponseCognex =",str(ResponseCognex))
        logging.info("ConfirmFinal="+ConfirmFinal)        
        logging.info("ResponseIV2="+str(ResponseIV2))
        logging.info("ResponseIV3_01="+str(ResponseIV3_01))
        logging.info("ResponseIV3_02="+str(ResponseIV3_02)) 
        logging.info("ResponseCognex="+str(ResponseCognex)) 


        #Test
        
        now = datetime.now()
        Timestamp = datetime.now()
        Timestamp = datetime.fromtimestamp(datetime.timestamp(now))
        Timestamp = Timestamp.strftime("%Y-%m-%d %H:%M:%S")
        SerialKey = datetime.fromtimestamp(datetime.timestamp(now))
        SerialKey = SerialKey.strftime("%Y%m%d%H%M%S")
        print("SerialKey...",SerialKey)
        End_time = Timestamp
        
        if ((ConfirmFinal=="Finish")&(Scan==1)):

            Timestamp = datetime.now()
            Timestamp = datetime.fromtimestamp(datetime.timestamp(now))
            Timestamp = Timestamp.strftime("%Y-%m-%d %H:%M:%S")
            End_time = Timestamp
            Serial_No = ModelBarcode
            
            
            Traceability_checkStatus()

            if (C126==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","C126")
                logging.info("C126 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","C126")
                logging.info("C126 defect is Wrong Polarity(WPO)!!")
            if (C132==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","C132")
                logging.info("C132 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","C132")
                logging.info("C132 defect is Wrong Polarity(WPO)!!")
            if (A6J1==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A6J1")
                logging.info("A6J1 defect is Part Not Placed(PNP)!!")
            if (A6J2==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A6J2")
                logging.info("A6J2 defect is Part Not Placed(PNP)!!")
            if (R109==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R109")
                logging.info("R109 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R109")
                logging.info("R109 defect is Wrong Polarity(WPO)!!")
            if (R110==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R110")
                logging.info("R110 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R110")
                logging.info("R110 defect is Wrong Polarity(WPO)!!")
            if (D100==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","D100")
                logging.info("D100 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","D100")
                logging.info("D100 defect is Wrong Polarity(WPO)!!")
            if (R101==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R101")
                logging.info("R101 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R101")
                logging.info("R101 defect is Wrong Polarity(WPO)!!")
            if (R102==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R102")
                logging.info("R102 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R102")
                logging.info("R102 defect is Wrong Polarity(WPO)!!")
            if (R103==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R103")
                logging.info("R103 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R103")
                logging.info("R103 defect is Wrong Polarity(WPO)!!")
            if (R207==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R207")
                logging.info("R207 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R207")
                logging.info("R207 defect is Wrong Polarity(WPO)!!")
            if (R240==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R240")
                logging.info("R240 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","R240")
                logging.info("R240 defect is Wrong Polarity(WPO)!!")
            if (T100==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","T100")
                logging.info("T100 defect is Part Not Placed(PNP)!!")
            if (T101==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","T101")
                logging.info("T101 defect is Part Not Placed(PNP)!!")
            if (T102==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","T102")
                logging.info("T102 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","T102")
                logging.info("T102 defect is Wrong Polarity(WPO)!!")
            if (A3J7==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A3J7")
                logging.info("A3J7 defect is Part Not Placed(PNP)!!")
            if (Q101==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","Q101")
                logging.info("Q101 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","Q101")
                logging.info("Q101 defect is Wrong Polarity(WPO)!!")
            if (Q103==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","Q103")
                logging.info("Q103 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","Q103")
                logging.info("Q103 defect is Wrong Polarity(WPO)!!")
            if (Q104==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","Q104")
                logging.info("Q104 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","Q104")
                logging.info("Q104 defect is Wrong Polarity(WPO)!!")
            if (A10J5==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A10J5")
                logging.info("A10J5 defect is Part Not Placed(PNP)!!")
            if (A9J3==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A9J3")
                logging.info("A9J3 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Bend Lead/Pin(AOI:BL/BP)","A9J3")
                logging.info("A9J3 defect is Bend Lead/Pin(BL/BP)!!")
            if (U509==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","U509")
                logging.info("U509 defect is Part Not Placed(PNP)!!")
            if (SW500==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","SW500")
                logging.info("SW500 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","SW500")
                logging.info("SW500 defect is Wrong Polarity(WPO)!!")
            if (RY100==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","RY100")
                logging.info("RY100 defect is Part Not Placed(PNP)!!")
            if (L101==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","L101")
                logging.info("L101 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Wrong Polarity(AOI:WPO)","L101")
                logging.info("L101 defect is Wrong Polarity(WPO)!!")
            if (T103==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","T103")
                logging.info("T103 defect is Part Not Placed(PNP)!!")
            if (T105==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","T105")
                logging.info("T105 defect is Part Not Placed(PNP)!!")
            if (R105==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R105")
                logging.info("R105 defect is Part Not Placed(PNP)!!")
            if (R106==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R106")
                logging.info("R106 defect is Part Not Placed(PNP)!!")
            if (R107==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R107")
                logging.info("R107 defect is Part Not Placed(PNP)!!")
            if (R108==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","R108")
                logging.info("R108 defect is Part Not Placed(PNP)!!")
            if (A9J9==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A9J9")
                logging.info("A9J9 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Bend Lead/Pin(AOI:BL/BP)","A9J9")
                logging.info("A9J9 defect is Bend Lead/Pin(BL/BP)!!")
            if (A9J10==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","A9J10")
                logging.info("A9J10 defect is Part Not Placed(PNP)!!")
                Log_defect(ModelBarcode,"AOI: Bend Lead/Pin(AOI:BL/BP)","A9J10")
                logging.info("A9J10 defect is Bend Lead/Pin(BL/BP)!!")
            if (RTV_C126==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","RTV_C126")
                logging.info("RTV_C126 defect is Part Not Placed(PNP)!!")
            if (RTV_C132==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","RTV_C132")
                logging.info("RTV_C132 defect is Part Not Placed(PNP)!!")
            if (RTV_Q103==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","RTV_Q103")
                logging.info("RTV_Q103 defect is Part Not Placed(PNP)!!")
            if (U523==0):
                Log_defect(ModelBarcode,"AOI: Part not place(AOI:PNP)","U523")
                logging.info("U523 defect is Part Not Placed(PNP)!!")
            
        file_update_sql(SerialKey,StationID,ModelBarcode,new_file_name_cognex,new_file_name_path_Cognex,new_file_name_IV2,new_file_name_path_IV2,new_file_name_IV3_01,new_file_name_path_IV3_01,new_file_name_IV3_02,new_file_name_path_IV3_02,FinalStatus,Timestamp)   
        file_update(StationID,Serial_No,FinalStatus,new_file_name_cognex,new_file_name_IV2,new_file_name_IV3_01,new_file_name_IV3_02,A6J1,A6J2,R109,R110,D100,R101,R102,R103,R207,R240, 
        T100,T102,C132,C126,A3J7,Q101,Q103,Q104,A10J5,A9J3,U509,U523,SW500,RY100,L101,T103,T105,T101,R105,R106,R107, 
        R108,A9J9,A9J10,PCB,RTV_C126,RTV_C132,RTV_Q103,timestamp)
        FinalStatus = " "
        ResponseIV2 =0
        ResponseIV3_01 =0
        ResponseIV3_02 =0
        ResponseCognex =0
        print("")
        sleep(1)
         
   
        #--------------------------------IV
        client.publish("Final_status","CLR")
        client.publish("ModelBarcode","CLR") 
        client.publish("Status_system","CLR")
        client.publish("Status_board","CLR")

        print("CLR Finished !!")
        logging.info("CLR Finished !!")
        Scan=0

    else:
        print("Not matching condition !!")


def on_connect(client,userdata, flags, rc):
    global Capture_press 
    global Result

    try:
        print("Connected with result code "+str(rc))
        logging.info("Connected with result code "+str(rc))
        client.subscribe("python/mqtt") 
        client.subscribe("ConfirmFinal") 
        client.subscribe("Final_status") 
        client.subscribe("Status_board") 
        client.subscribe("Status_system") 
        client.subscribe("imgshow") 
        client.subscribe("Insert") 
    except:
     print("Connected with result code ")
     logging.info("Connected with result code ")   

def chk_timestamp():
    global file_timestamp
    global path
    global Serial_No
    global timestamp
    # current date and time
    now = datetime.now()
    timestamp = datetime.fromtimestamp(datetime.timestamp(now))
    timestamp = timestamp.strftime("%d%m%Y%H%M%S")
    file_timestamp = datetime.fromtimestamp(datetime.timestamp(now))
    file_timestamp = file_timestamp.strftime("%d%m%Y%H%M")
    
    path_to_file = str(Path.cwd()) + file_timestamp + '.csv'
    path = Path(path_to_file)
    Serial_No = str(timestamp)

def file_update(StationID,ModelBarcode,final_status,CognexIMG,IV2IMG,IV3_01IMG,IV3_02IMG,A6J1,A6J2,R109,R110,D100,R101,R102,R103,R207,R240, 
            T100,T102,C132,C126,A3J7,Q101,Q103,Q104,A10J5,A9J3,U509,U523,SW500,RY100,L101,T103,T105,T101,R105,R106,R107, 
            R108,A9J9,A9J10,PCB,RTV_C126,RTV_C132,RTV_Q103,n_timestamp):
                
                
        
        global End_time
        End_time = Timestamp

        print("Create new .CSV file1")
        logging.info("Create new .CSV file1")
        
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        print ("Year = ",year)
        logging.info ("Year = "+str(year))
        print ("Month = ",month)
        logging.info ("Month = "+str(month))
        print ("Day = ",day)
        logging.info ("Day = "+str(day))

        #n_timestamp = datetime.fromtimestamp(datetime.timestamp(now))
        #n_timestamp = n_timestamp.strftime("%d%m%Y")
        path = '\\'+'\\'+machineDetail['NAS_IP']+'\\'+machineDetail['MAIN_FOLDER_AUTOMATE']+'\\'+machineDetail['MAIN_FOLDER_ZOLL']+'\\'+machineDetail['SUB_FOLDER_ZOLL']+'\\'+machineDetail['SUB_FOLDER_MAC']+'\\'+machineDetail['SUB_FOLDER_MAC_NAME']+'\\'+machineDetail['FOLDER_RESULT']+'\\' + str(year)+'\\'+str(month)+'\\'+str(day)+'\\'+str(ModelBarcode)+'\\'

        now = datetime.now()
        nfile_timestamp = datetime.fromtimestamp(datetime.timestamp(now))
        nfile_timestamp = nfile_timestamp.strftime("%d%m%Y%H%M%S")
        
        # check whether directory already exists
        if not os.path.exists(path):
         os.makedirs(path)
         print("Folder %s created!" + path)
         logging.info ("Folder %s created!" + path)
        else:
         print("Folder %s already exists" + path)
         logging.info("Folder %s already exists" + path)
        with open( path + str(ModelBarcode) + '_' +nfile_timestamp + '.csv', 'w') as csv_file:
            csv_file.write('Software,version KETL-AE24-M006-SW-001\n')
            csv_file.write('Program name,9301536801+05_NX1\n')
            csv_file.write('StationID,'+ str(StationID) +'\n')
            csv_file.write('SerialNo,' + str(ModelBarcode) +' \n')  
            csv_file.write('Image Name from Cognex,' + str(CognexIMG) +' \n')    
            csv_file.write('Image Name from IV2,' + str(IV2IMG) +' \n')    
            csv_file.write('Image Name from IV3_01,' + str(IV3_01IMG) +' \n')
            csv_file.write('Image Name from IV3_02,' + str(IV3_02IMG) +' \n')
            csv_file.write('final_status,   ' + str(final_status) +' \n')

            now = datetime.now()
            n_timestamp = datetime.fromtimestamp(datetime.timestamp(now))
            n_timestamp = n_timestamp.strftime("%d-%m-%Y,%H:%M:%S")

            csv_file.write('Timestamp,    '+ str(n_timestamp)+' \n')
            csv_file.write('No'+ ',Component'+',Result'+' \n')
            csv_file.write('1,A6J1,'+str(A6J1)+' \n')
            csv_file.write('2,A6J2,'+str(A6J2)+' \n')  
            csv_file.write('3,R109,'+str(R109)+' \n')
            csv_file.write('4,R110,'+str(R110)+' \n')  
            csv_file.write('5,D100,'+str(D100)+' \n')
            csv_file.write('6,R101,'+str(R101)+' \n')  
            csv_file.write('7,R102,'+str(R102)+' \n')  
            csv_file.write('8,R103,'+str(R103)+' \n')
            csv_file.write('9,R207,'+str(R207)+' \n')  
            csv_file.write('10,R240,'+str(R240)+' \n')
            csv_file.write('11,T100,'+str(T100)+' \n')  
            csv_file.write('12,T102,'+str(T102)+' \n')  
            csv_file.write('13,C132,'+str(C132)+' \n')  
            csv_file.write('14,C126,'+str(C126)+' \n')
            csv_file.write('15,A3J7,'+str(A3J7)+' \n')  
            csv_file.write('16,Q101,'+str(Q101)+' \n')  
            csv_file.write('17,Q103,'+str(Q103)+' \n')
            csv_file.write('18,Q104,'+str(Q104)+' \n')  
            csv_file.write('19,A10J5,'+str(A10J5)+' \n')
            csv_file.write('20,A9J3,'+str(A9J3)+' \n')  
            csv_file.write('21,U509,'+str(U509)+' \n')  
            csv_file.write('22,U523,'+str(U523)+' \n')  
            csv_file.write('23,SW500,'+str(SW500)+' \n')
            csv_file.write('24,RY100,'+str(RY100)+' \n')  
            csv_file.write('24,L101,'+str(L101)+' \n')  
            csv_file.write('26,T103,'+str(T103)+' \n')  
            csv_file.write('27,T105,'+str(T105)+' \n')
            csv_file.write('28,T101,'+str(T101)+' \n')  
            csv_file.write('29,R105,'+str(R105)+' \n')  
            csv_file.write('30,R106,'+str(R106)+' \n')  
            csv_file.write('31,R107,'+str(R107)+' \n')
            csv_file.write('32,R108,'+str(R108)+' \n')  
            csv_file.write('33,A9J9,'+str(A9J9)+' \n')  
            csv_file.write('34,A9J10,'+str(A9J10)+' \n')  
            csv_file.write('35,PCB,'+str(PCB)+' \n')
            csv_file.write('36,RTV_C126,'+str(RTV_C126)+' \n')  
            csv_file.write('37,RTV_C132,'+str(RTV_C132)+' \n')  
            csv_file.write('38,RTV_Q103,'+str(RTV_Q103)+' \n')  

def file_update_sql(SerialKey,StationID,ModelBarcode,Image_name_COGNEX,Image_Path_COGNEX,Image_name_IV2,Image_Path_IV2,Image_name_IV3_01,Image_Path_IV3_01,Image_name_IV3_02,Image_Path_IV3_02,Final_status,Timestamp):
    
    sqlServer= machineDetail['sqlServer']
    sqlDriver= machineDetail['sqlDriver']
    sqlUsername = machineDetail['sqlUsername']
    sqlPassword  = decrypt_message(machineDetail['Encrypted'], machineDetail['Key'])
    sqltable = machineDetail['sqltable']
    sqlDatabase=  machineDetail['sqlDatabase']
    cnxn = pyodbc.connect('Driver='+sqlDriver+
                                ';Server='+sqlServer+
                                ';Database='+sqlDatabase+
                                ';UID='+sqlUsername+
                                ';PWD='+sqlPassword+';')
    cursor = cnxn.cursor()
    print("Connect to SQL")
    
    count = cursor.execute("""INSERT INTO """+str(sqltable)+"""
      (SerialKey 
      ,StationID
      ,Serial_No
      ,Image_name_COGNEX
      ,Image_Path_COGNEX
      ,Image_name_IV2
      ,Image_Path_IV2
      ,Image_name_IV3_01
      ,Image_Path_IV3_01
      ,Image_name_IV3_02
      ,Image_Path_IV3_02
      ,Final_status
      ,Timestamp                                                             )
      VALUES 
      (?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?
      ,?                     
      )"""
      ,str(SerialKey)
      ,str(StationID)
      ,str(ModelBarcode)
      ,str(Image_name_COGNEX)
      ,str(Image_Path_COGNEX)
      ,str(Image_name_IV2)
      ,str(Image_Path_IV2)
      ,str(Image_name_IV3_01)
      ,str(Image_Path_IV3_01)
      ,str(Image_name_IV3_02)
      ,str(Image_Path_IV3_02)
      ,str(Final_status)
      ,str(Timestamp)
                           ).rowcount 
    
    cnxn.commit()
    print('Rows inserted: ' + str(count))     
    sleep(1)
    
    
# Generate a key
def generate_key():
    return Fernet.generate_key()

# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()    


def Cognex_thread():
   
    global A6J1#1
    global A6J2#2
    global R109#3
    global R110#4
    global D100#5
    global R101#6
    global R102#7
    global R103#8
    global R207#9
    global R240#10
    global T100#11
    global T101#12
    global T102#13
    global C132#14
    global C126#15
    global A3J7#16
    global Q101#17
    global Q103#18
    global Q104#19
    global A10J5#20
    global RY100#21
    global L101#22
    global T103#23
    global T105#24
    global R105#25
    global R106#26
    global R107#27
    global R108#28
    global PCB#29
    global RTV_C126#30
    global RTV_C132#31
    global RTV_Q103#32
    global t
    global FinalStatus
    global Result
    global SorceCognexPath
    global SorceCognexfile
    global ResponseCognex
    while True:
        print("Scan from COGNEX = ")
        logging.info("Scan from COGNEX = ")
        print("Cognex_thread")
        logging.info("Cognex_thread")
       
        t = 0 
        result = InSightRead(HOST7,PORT8,"s")
        print("result",type(result))
        logging.info("result"+str(type(result)))

        result = str(result, encoding='utf-8') 
        print("result", (result))
        logging.info("result"+ (result))
        result = re.split('.Pass|,| ', result)
        print("result split", (result))   
        logging.info("result split"+str (type (result)))
        nm = "A6J1"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),str(n),result[n+2])
            logging.info(str(nm)+str(n)+str(result[n+2]))
            A6J1 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
           
        nm = "A6J2"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            A6J2 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))
        else:
            client.publish( nm ,str(0))
                  

        nm = "R109"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R109 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))
        else:
            client.publish( nm ,str(0))
           

        nm = "R110"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R110 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))
        else:
            client.publish( nm ,str(0))
           

        nm = "D100"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm))  
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            D100 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))
        else:
            client.publish( nm ,str(0))
           

        nm = "R101"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R101 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "R102"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R102 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "R103"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R103 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "R207"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R207 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "R240"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R240 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "T100"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            T100 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "T102"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            T102 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
            

        nm = "C132"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            C132 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            
        nm = "C126"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            C126 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
            
        else:
            print('C126 = NG')
            logging.info('C126 = NG')
            client.publish( nm ,str(0))
            print('C126 = NG')
            logging.info('C126 = NG')
           

        nm = "A3J7"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm))  
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            A3J7 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "Q101"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),str (result[n+2]))
            logging.info(str(nm)+str(result[n+2]))
            Q101 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
           

        nm = "Q103"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm), (result[n+2]))
            logging.info(str(nm)+str(result[n+2]))
            Q103 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "Q104"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            Q104 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "A10J5"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            A10J5 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))     
        else:
            client.publish( nm ,str(0))
            

      
        nm = "RY100"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            RY100 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
           

        nm = "L101"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            L101 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            
        nm = "T103"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            T103 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
            

        nm = "T105"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            T105 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
           

        nm = "T101"    
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            T101 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
           

        nm = "R105"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R105 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))   
        else:
            client.publish( nm ,str(0))
           

        nm = "R106"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R106 = int(result[n+2])
            client.publish( nm ,str(result[n+2])) 
        else:
            client.publish( nm ,str(0))
           

        nm = "R107"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R107 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
            

        nm = "R108"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm))  
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            R108 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
            


        nm = "PCB"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            PCB = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))
            

        nm = "RTV_C126"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            RTV_C126 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))   
        else:
            client.publish( nm ,str(0))
           

        nm = "RTV_C132"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            RTV_C132 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))   
        else:
            client.publish( nm ,str(0))
            


        nm = "RTV_Q103"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm)) 
            print(str(nm),result[n+2])
            logging.info(str(nm)+str(result[n+2]))
            RTV_Q103 = int(result[n+2])
            client.publish( nm ,str(result[n+2]))  
        else:
            client.publish( nm ,str(0))


        nm = "Image"   
        if (result.index(str(nm)) >= 0):
            n = result.index(str(nm))
            print(str(nm),result[n+1])
            logging.info(str(nm)+str(result[n+1]))

        SorceCognexPath = 'C:\Capture_Cognex'+'\\'+str(result[n+1])+'.jpg'
        SorceCognexfile = str(result[n+1])+'.jpg'
        print("Image path =",SorceCognexPath)
        print("length =",len(SorceCognexPath))
        
        

            #---------------------------------------------------------------------------------------------------------------------------------------
        
        print ("A6J1 =",A6J1)
        logging.info("A6J1 ="+str(A6J1))
        print ("A6J2 =",A6J2)
        logging.info("A6J2 ="+str(A6J2))
        print ("R109 =",R109)
        logging.info("R109 ="+str(R109))
        print ("R110 =",R110)
        logging.info("R110 ="+str(R110))
        print ("D100 =",str(D100))
        logging.info("D100 ="+str(D100))
        print ("R101 =",str(R101))
        logging.info("R101 ="+str(R101))
        print ("R102 =",str(R102))
        logging.info("R102 ="+str(R102))
        print ("R103 =",R103)
        logging.info("R103 ="+str(R103))
        print ("R207 =",R207)
        logging.info("R207 ="+str(R207))
        print ("R240 =",R240)
        logging.info("R240 ="+str(R240))
        print ("T100 =",T100)
        logging.info("T100 ="+str(T100))
        print ("T102 =",T102)
        logging.info("T102 ="+str(T102))
        print ("C132 =",C132)
        logging.info("C132 ="+str(C132))
        print ("C126 =",C126)
        logging.info("C126 ="+str(C126))
        print ("A3J7 =",A3J7)
        logging.info("A3J7 ="+str(A3J7))
        print ("Q101 =",Q101)
        logging.info("Q101 ="+str(Q101))
        print ("Q103 ="+str(Q103))
        logging.info("Q103 ="+str(Q103))
        print ("Q104 ="+str(Q104))
        logging.info("Q104 ="+str(Q104))
        print ("A10J5 ="+str(A10J5))
        logging.info("A10J5 ="+str(A10J5))
        print ("RY100 =",RY100)
        logging.info("RY100 ="+str(RY100))
        print ("L101 =",L101)
        logging.info("L101 ="+str(L101))
        print ("T103 =",T103)
        logging.info("T103 ="+str(T103))
        print ("T105 =",T105)
        logging.info("T105 ="+str(T105))
        print ("T101 =",T101)
        logging.info("T101 ="+str(T101))
        print ("R105 =",R105)
        logging.info("R105 ="+str(R105))
        print ("R106 =",R106)
        logging.info("R106 ="+str(R106))
        print ("R107 =",R107)
        logging.info("R107 ="+str(R107))
        print ("R108 =",R108)
        logging.info("R108 ="+str(R108))
        print ("D100 =",PCB)
        logging.info("D100 ="+str(PCB))
        print ("R106 =",RTV_C126)
        logging.info("R106 ="+str(RTV_C126))
        print ("Q101 =",RTV_C132)
        logging.info("Q101 ="+str(RTV_C132))
        print ("R101 =",RTV_Q103)
        logging.info("R101 ="+str(RTV_Q103))
        ResponseCognex=1

        #---------------------------------------------------------------------------------------------------------------------------------------

        if ((A6J1 == 1)&(A6J2 == 1)&(R109 == 1)&(R110 == 1)&(D100 == 1)&(R101 == 1)&(R102 == 1)&(R103 == 1)&(R207 == 1)&(R240 == 1)
            &(T100 == 1)&(T102 == 1)&(C132 == 1)&(C126 == 1)&(A3J7 == 1)&(Q101 == 1)&(Q103 == 1)&(Q104 == 1)&(A10J5 == 1)&(A9J3 == 1)
            &(U509 == 1)&(U523 == 1)&(SW500 == 1)&(RY100 == 1)&(L101 == 1)&(T103 == 1)&(T105 == 1)&(T101 == 1)&(R105 == 1)&(R106 == 1)
            &(R107 == 1)&(R108 == 1)&(A9J9 == 1)&(A9J10 == 1)&(PCB == 1)&(RTV_C126 == 1)&(RTV_C132 == 1)&(RTV_Q103 == 1)):
            
            client.publish("Final_status",str(1))   
            FinalStatus = "OK"
            Result = 1
            print("Final_status",str(1))           
            logging.info("Update OK complete ")
            #sleep(5)
            #--------------------------------IV/COGNEX
            
        else:
            client.publish("Final_status",str(0))   
            print("Final_status",str(0)) 
            FinalStatus = "NG"
            Result = 0
            logging.info("Update NG complete ")

def mqtt_thread():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.loop_forever()

def serial_thread():

    global Barcode
    global Backchk
    global Start_time
    global End_time
    global Status_board
    global Capture_press
    global ModelBarcode
    global Timestamp 
    global StationID
    global Scan
    print("try")    

    try: 
        print("A ") 

    #Step8 
        if ser.isOpen():
            print("Serial_port com is opened")
            logging.info("Serial_port com is opened")
            
            print("Serial com is trig")
            logging.info("Serial com is trig")
            sleep(0.5)
            v_text = "LON\r\n"
            ser.write(v_text.encode())
            sleep(0.5)
            #print("Barcode : " + str(Barcode) + " Result : " + str(Result) + " SerialKey : " + str(SerialKey) + "topics_name : " + str(topics_name))
                
            if ser.inWaiting() > 0:
                Barcode = ser.read(ser.inWaiting()).decode("utf-8")
                print (">> " ,len(Barcode))
                logging.info (">> " +str(len(Barcode)))
                print ("Barcode>> " ,Barcode)
                logging.info ("Barcode>> " +str(Barcode))
                #ModelBarcode = BarcodeSplit[0].split("\r")[0]
            
                ModelBarcode = Barcode.strip()
                print (">> " ,len(ModelBarcode))    
                logging.info (">> " +str(len(ModelBarcode)))
                print ("ModelBarcode",ModelBarcode)
                logging.info ("ModelBarcode"+str(ModelBarcode))
                print("Type",(type(ModelBarcode)))
                logging.info ("Type"+str((type(ModelBarcode))))
                #ModelBarcode='TKA0049'
                #*****************Test
                Start_time = datetime.now()
                Start_time = datetime.fromtimestamp(datetime.timestamp(Start_time))
                Start_time = Start_time.strftime("%Y-%m-%d %H:%M:%S")
                print("Start time >> ", Start_time)
                logging.info("Start time >> "+ Start_time)

                client.publish("ModelBarcode",str(ModelBarcode)) 
                logging.info("ModelBarcode  = "+ str(ModelBarcode)) 
                print ("ModelBarcode",ModelBarcode)
                ser.flushOutput
                
                #---------------------------------------------------------------
                Status_board = Treacibility_backcheck_data(ModelBarcode)
                print ("Status_board =",Status_board)
                logging.info ("Status_board ="+Status_board)
                print ('Len barcode', len(ModelBarcode))
                #--------------------------------------------------------------

                if (len(ModelBarcode)==7):
                    print ("ModelBarcode",ModelBarcode) 
                    logging.info ("ModelBarcode"+str(ModelBarcode) )
                
                    if ((str(Status_board).find('Final')>0)|(ModelBarcode=='TKA001A')|(ModelBarcode=='TKA0049')):#|(ModelBarcode=='TKA0011')| (ModelBarcode=='TKA003T'):

                        if ((ModelBarcode=='TKA001A')|(ModelBarcode=='TKA0049')):#|(Barcode=='230802636'): #| (str(Status_board).find('Scrapped')>0):#232605881232605881
                            Backchk = 0
                            print("Backchk = ", Backchk)
                            logging.info("Backchk = "+str (Backchk))
                            client.publish("Status_system","Close system!!")

                        elif ((str(Status_board).find('Final')>0)): #|: 
                            Backchk = 1
                            print("Backchk = ", Backchk)
                            logging.info("Backchk = "+str( Backchk))
                            client.publish("Status_system","Open system")
                        else:
                            print("Backchk not Matching")

                        ser.flushInput()
                        Start_time = datetime.now()
                        Start_time = datetime.fromtimestamp(datetime.timestamp(Start_time))
                        Start_time = Start_time.strftime("%Y-%m-%d %H:%M:%S")
                        print("Start time >> ", Start_time)
                        logging.info("Start time >> "+ Start_time)
                        client.publish("Status_board",Status_board)
                        print (">>Status_board "+Status_board)
                        logging.info("Status_board  = "+ Status_board) 
                        
                        client.publish("ModelBarcode",str(ModelBarcode)) 
                        logging.info("ModelBarcode  = "+ str(ModelBarcode)) 
                        print ("ModelBarcode",ModelBarcode)
                        client.publish("Insert","CLR")
                        ser.flushOutput
                        Scan = 1
                        
                    else :
                        client.publish("Status_board","Process skipped !!"+ Status_board)
                        client.publish("Status_backcheck","Process skipped !!"+ Status_board)

                        print ("Status_backcheck >> Not complete")    
                        logging.warning("Process skipped !!") 
                        Scan = 0
                            
                else:
                    print("Not matching length!!")
            else:
                    print(">> sError to read barcode")        
                    
                    
                    
                    
    except  Serial.SerialException as error:
            print("Failed  {}".format(error))
             
chk_timestamp()
mqtt_thread = threading.Thread(target=mqtt_thread)
mqtt_thread.start()
Cognex_thread = threading.Thread(target=Cognex_thread) 
Cognex_thread.start()
scada_monitor = threading.Thread(target=scada_monitor)
scada_monitor.start()
sleep(3)

if __name__ == '__main__':
    
    print("Vision Start process...") 
    logging.info("Vision Start process...") 
    sleep(1)
    client.publish("Python","RUNNING")
    print("START1")
    