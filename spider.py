#!/usr/bin/env python3

import threading
import csv
try:
    import xlrd
except ImportError:
    exit('Needs modules requests and xlrd.')
from cetdb import *

# Read students' informations from excel
students = xlrd.open_workbook('student-info.xlsx').sheets()[0]
cols = students.row_values(0)
colID = dict()
for i in range(students.ncols):
    if cols[i] in '姓名准考证学号院系':
        colID[cols[i]] = i

# Output students' grades to csv file
csvfile = open('cet-grades.csv', 'w')
fieldname = (
    '姓名', '准考证', '学号', '院系',
    '听力', '阅读', '写作与翻译', '总分',
    '口语准考证', '口语等级',
)
csvwriter = csv.writer(csvfile)
csvwriter.writerow(fieldname)

pool = list()
for row in range(students.nrows - 1):
    student = students.row_values(row + 1)
    name = student[colID['姓名']]
    ticket = student[colID['准考证']]
    if '学号' in colID:
        studentID = student[colID['学号']]
    else: studentID = None
    if '院系' in colID:
        college = student[colID['院系']]
    else: college = None
    pool.append(threading.Thread(
        target=sushe99.query,
        args=(name, ticket, studentID, college)
    ))

for thread in pool: thread.start()
# wait until all were done
for thread in pool: thread.join()

while not grades.empty():
    csvwriter.writerow(grades.get())
csvfile.close()

# if not found
while not failed.empty():
    fail = failed.get()
    print('Something wrong with', fail)

