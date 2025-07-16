import datetime
from recorder import capture
# Setting alarm vairable

alarmHour = 14 #int(input("Enter Hour: ")) 
alarmMin =  15 #int(input("Enter the min: ")) 
# alarmAm = (input("am / pm: "))

# if alarmAm == "pm":
#     alarmHour += 12 

while True:
    if alarmHour == 14 : #alarmHour == datetime.datetime.now().hour and alarmMin == datetime.datetime.now().minute: 
        print("Sytem survillience is on")
        capture()
        break


