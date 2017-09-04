#!/usr/bin/env python3

from cetdb import asyncio, aiohttp, QueryError
from bs4 import BeautifulSoup
from random import randint
from urllib.parse import urlencode

__author__ = 'Xris'


url = 'http://www.chsi.com.cn/cet/query'


async def _query(name, ticket):
    """
    A single operation for async http request
    :param name: Student's name
    :param ticket: Student's ticket for CET
    :return: A single tuple containing result
    :raises: Will raise QueryError if need captcha or ticket error.
    """
    # Generate random XFF to bypass captcha
    fake_ip = '.'.join(str(randint(0, 255)) for _ in range(4))
    headers = {
        'Referer': '.chsi.com.cn',
        'X-Forwarded-For': fake_ip,
    }
    data = urlencode({
        'xm': name,
        'zkzh': ticket,
    })
    # Create new session every time to prevent being banned
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url + '?' + data, headers=headers) as resp:
            bs = BeautifulSoup(await resp.text(), 'html.parser')
            error = bs.select_one('.error')
            if error:
                raise QueryError(name, error.text.strip())
            result = [node.text.strip() for node in bs.select('.cetTable td')]
            return tuple(filter(lambda st: bool(st), result))


def query(students):
    """
    Query students' CET grades.
    :param students: a list of tuples like (name, ticket)
    :return: a tuple of CET grades like (name, university, level, ticket,
    total score, listening score, comprehension score, writing score,
    oral ticket, oral grade).
    """
    loop = asyncio.get_event_loop()
    task = (_query(st[0], st[1]) for st in students)
    task = asyncio.gather(*task, return_exceptions=True)
    return loop.run_until_complete(task)
