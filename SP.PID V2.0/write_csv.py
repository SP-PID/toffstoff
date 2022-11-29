import csv
import random
import shutil
from datetime import datetime

def WriteData():

    filename = 'SP.PID-' +str(datetime.now().strftime("%Y-%m-%d-%H-%M"))+'.csv'
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


def StoreData():
    pass
    #original = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\'+filename
    #target = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\' + filename
    #shutil.move(original, target)


WriteData()

