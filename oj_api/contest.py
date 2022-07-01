import abc
import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Contest(metaclass=abc.ABCMeta):

    def __init__(self):
        self.query_time = time.time()
        self.info, self.begin_time, self.during_time = asyncio.run(self.get_next_contest())
        self.note_time = self.begin_time - 15 * 60
        self.end_time = self.begin_time + self.during_time
        self.update_time = self.end_time + 10 * 60

    async def update_contest(self):
        self.query_time = time.time()
        if await self.update_local_contest():
            self.info, self.begin_time, self.during_time = await self.get_next_contest()
            self.note_time = self.begin_time - 15 * 60
            self.end_time = self.begin_time + self.during_time
            self.update_time = self.end_time + 10 * 60
            print('更新比赛成功！')
            return True
        else:
            print('更新比赛失败！')
            return False

    @abc.abstractmethod
    async def get_next_contest(self):
        pass

    @abc.abstractmethod
    async def get_rating(self, name):
        pass

    @abc.abstractmethod
    async def update_local_contest(self):
        pass

    @abc.abstractmethod
    async def get_contest_info(self):
        pass
