#
import time
from time import sleep
from datetime import datetime
import logging
import pyodbc
import yaml

yaml_path= "C:\Zoll_5368_FinalAOI\setup.yaml"
print(yaml_path)
with open(yaml_path, 'r') as file:
      machineDetail = yaml.safe_load(file)

def SCADA_update_sql(StationName,Status,Model,CycleTime,Count,OEE,YIELD,RunTime,DownTime,IdleTime):
    sqlServer= machineDetail['sqlServer']
    sqlDriver= machineDetail['sqlDriver']
    sqlUsername = machineDetail['sqlUsername']
    sqlPassword = machineDetail['sqlPassword']
    sqlDatabase=  machineDetail['sqlDatabase']
    cnxn = pyodbc.connect('Driver='+sqlDriver+
                          ';Server='+sqlServer+
                          ';Database='+sqlDatabase+
                          ';UID='+sqlUsername+
                          ';PWD='+sqlPassword+';')
    cursor = cnxn.cursor()
    logging.warning("Connect to SQL")
    print("Connect to SQL")
    logging.warning("Update " )
    # current date and time
    now_sql = datetime.now()
    timestamp_sql = datetime.fromtimestamp(datetime.timestamp(now_sql))
    timestamp_s = datetime.fromtimestamp(datetime.timestamp(now_sql))    
    timestamp_sql = timestamp_sql.strftime("%Y-%m-%d %H:%M:%S")
    SerialKey = timestamp_s.strftime("%Y%m%d%H%M%S")
    StationName = StationName
    Status= Status
    Model= Model
    CycleTime= CycleTime
    Count=Count
    OEE=OEE
    YIELD=YIELD
    RunTime=RunTime
    DownTime=DownTime
    IdleTime=IdleTime
    count = cursor.execute("""INSERT INTO KETL_AE24_M_01_AOI_MONITOR_V1 (SerialKey,StationName,Status,Model,CycleTime,Count,OEE,YIELD,RunTime,DownTime,IdleTime,Timestamp) values(?,?,?,?,?,?,?,?,?,?,?,?)"""
                           , (str(SerialKey)+str(StationName)),StationName,Status,Model,CycleTime,Count,OEE,YIELD,RunTime,DownTime,IdleTime, timestamp_sql).rowcount
    cnxn.commit()
    logging.warning('SQL save complete')
    logging.warning('Rows inserted: ' + str(count))
    print('Rows inserted: ' + str(count))
    time.sleep(1)
