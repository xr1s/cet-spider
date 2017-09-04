"""
Wrap query function for websites offering grades query service.
"""

import aiohttp
import asyncio

__all__ = ['chsi']


class QueryError(Exception):
    """
    Main Exception for cetdb
    """
    def __init__(self, who, what):
        super().__init__(who + ' ' + what)
