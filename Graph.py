import numpy as np
import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@coder007',
    port='3306',
    database='Drill_Hole'
)
mycursor = mydb.cursor()

mycursor.execute("Select * from Analysis")
result = mycursor.fetchall()

Defects = []
Dates = set()

for i in result:
    Dates.add(i[1])

for i in Dates:
    c = 0
    for j in result:
        if(j[1] == i and j[5]== 1):
            c+=1
    Defects.append(c)

Dates = list(Dates)
Defects = list(Defects)
# Visualizing Data using Matplotlib
plt.bar(Dates, Defects , 0.7)
#plt.ylim(0, 5)
plt.xlabel("Days")
plt.ylabel("No. of Defects")
plt.title("Analysis")
plt.show()