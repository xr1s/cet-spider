#!/usr/bin/env python3

import re
import queue
import requests

failed = queue.Queue(maxsize=15000)
grades = queue.Queue(maxsize=15000)

class sushe99:
    url = 'http://cet.99sushe.com/getscore'
    headers = {
        'Referer': 'http://cet.99sushe.com',
    }
    errorlist = (
        'Unknown Error',
        'Request header error',
        'Invalid Post key',
        'No such name or admission ticket'
    )

    def query(name, ticket, studentID=None, college=None):
        posts = {
            'id': ticket,
            'name': name[:2].encode('gbk'),
        }
        try:
            response = requests.post(
                url=sushe99.url,
                data=posts,
                headers=sushe99.headers
            ).text
        except Exception as err:
            print(name, 'network error {}'.format(err))
            failed.put(name)
            return None
        response = response.strip('\x00').split(',')
        if len(response) == 1:
            print(name, errorlist[int(response[0])])
            failed.put(name)
            return None
        listen, read, write, full = map(int, response[2:6])
        spoken_ticket, spoken = response[-2:]
        print(name, 'success')
        result = (
            name, ticket, studentID, college,
            listen, read, write, full,
            spoken_ticket, spoken
        )
        grades.put(result)
        return {
            '总分': full,
            '听力': listen,
            '阅读': read,
            '写作与翻译': write,
            '口语准考证': spoken_ticket,
            '口语成绩': spoken,
        }


class chsi:
    url = 'http://www.chsi.com.cn/cet/query?zkzh=%s&xm=%s'
    headers = {
        'Referer': '.chsi.com.cn',
        'X-Forwarded-For': '127.0.0.',
    }
    regex = re.compile(r'>\s*(\d{1,3}|--|[FS]\d{14}|[ABCD]\+?)\s*<')
    not_found = '无法找到对应的分数，请确认你输入的准考证号及姓名无误'
    invalid_data = '请输入15位笔试或口试准考证号'
    
    def query(name, ticket, studentID=None, college=None):
        header = chsi.headers
        header['X-Forwarded-For'] += str(ticket)
        try:
            response = requests.get(
                url=chsi.url % (str(ticket), name),
                headers=chsi.headers
            ).text
        except Exception as err:
            print(name, 'network error {}'.format(err))
            failed.put(name)
            return None
        scores = chsi.regex.findall(response)
        if not scores:
            if ~response.find(chsi.not_found): 
                print(name, 'No such name or admission ticket')
            elif ~response.find(chsi.invalid_data):
                print(name, 'Invalid admission ticket')
            failed.put(name)
            return None
        full, listen, read, write = map(int, scores[:4])
        spoken_ticket, spoken = scores[4:]
        print(name, 'success')
        result = (
            name, ticket, studentID, college,
            listen, read, write, full,
            spoken_ticket, spoken
        )
        grades.put(result)
        return {
            '总分': full,
            '听力': listen,
            '阅读': read,
            '写作与翻译': write,
            '口语准考证': spoken_ticket,
            '口语成绩': spoken,
        }

