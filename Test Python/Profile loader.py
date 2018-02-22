import csv
import numpy as np

file = open('profile.csv','r',newline='')
reader = csv.reader(file, delimiter=',')

temperatures = []
timeStamps = []
lastTime = 0;

for i, row in enumerate(reader):
    if '#' in row[0]:
        continue
    if int(row[1]) < lastTime:
        print ("Sorry your csv cannot go back in time")
    lastTime = int(row[1])
    temperatures.append(int(row[0]))
    timeStamps.append(int(row[1]))

interval = 0.25
setTemps = []
subTimeStamps = []

for i, t in enumerate(temperatures):
    if i == len(temperatures)-1:
        break
    times = np.arange(timeStamps[i], timeStamps[i+1], interval)
    temps = np.linspace(t, temperatures[i+1], len(times))
    if i != len(temperatures)-2:
        setTemps = np.append(setTemps, temps[:-1])
        subTimeStamps = np.append(subTimeStamps, times[:-1])
    else:
        setTemps = np.append(setTemps, temps)
        subTimeStamps = np.append(subTimeStamps, times)

print(setTemps)
print(subTimeStamps)
file.close()
