# Querier for CET

懒得写英文了，写中文好了。

cetdb.py里有两个CET查询网站，已经搞好了这俩网站的API，直接查询即可。

使用方法：

## 只查询单个成绩

如果没有全校学生信息的，仅仅查询自己的成绩可以如此

```
from cetdb import *
chsi.query(your_name, admission_ticket)
```

返回一个dict，有各项信息。

## 批量查询成绩

如果有全校学生的xls或者xlsx，用了xlrd读取，文件名储存为student\_info.xlsx然后就可以了，必须有列名姓名和准考证，最好有学号和院系（虽然没有也可以），直接运行spider.py，输出到cet-grades.csv中。

