# CET Spider

Query CET 4, CET 6, and similar college language tests from those websites who provide query service. 

chsi is still available but 99sushe does not provides in 2017, so deleted.

This project is asynchronous now.

## Prerequisite

The `async` and `await` key words needs CPython 3.5 support.

This project uses `aiohttp` to send and recv HTTP requests, `bs4` parse html.

Neccessary if you need read XLS or XLSX file, please install xlrd first.

## Single query

```python
from cetdb import chsi

information = ('Your name', 'Your ticket')
print(chsi.query([information]))
```

## Group of query

see `demo.py`.
