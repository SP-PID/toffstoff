import csv
import random
import shutil
from datetime import datetime
import os

def WriteData():
    filename= "sppid.csv"
    #filename = "SP.PID-" +str(datetime.now().strftime("%Y-%m-%d %H.%M"))+".csv"
    with open(filename, mode= 'w', newline= '') as csvfile:
        fieldnames = ['SP', 'DC', 'Time']
        writer = csv.DictWriter(csvfile, fieldnames= fieldnames)
        writer.writeheader()
        for i in range (10):
            SetPoint = random.randint(0,100)
            DC_Val = random.randint(0,100)
            Time_value = random.randint(0,100)
            writer.writerow({'SP': SetPoint, 'DC': DC_Val, 'Time': Time_value})    
            i +=1            
    
    original = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\sppid.csv'
    target = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\sppid.csv'
    shutil.move(original, target)
    timestamp = datetime.now().strftime("%Y-%m-%d %H.%M")
    old_name = r"C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\sppid.csv"
    new_name = r"C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\sppid " + timestamp + ".csv"
    os.rename(old_name,new_name)


WriteData()

