import re
import json
import time

from web_operation.operation import *
from oj_api.contest import Contest


class PTYZOJ(Contest):
    async def get_contest(self):
        with open('./oj_json/ptyzoj_contests.json', 'r', encoding='utf-8') as f:
            contest_data = json.load(f)
        contest_list = []
        if contest_data != []:
            for contest in contest_data:
                if contest['source'] == 'PTYZOJ':
                    contest['contestName'] = contest['name']
                    start_time = int(time.mktime(time.strptime(
                        contest['start_time'], "%Y-%m-%dT%H:%M:%S+00:00"))) + 8 * 3600
                    contest['startTime'] = start_time
                    end_time = int(time.mktime(time.strptime(
                        contest['end_time'], "%Y-%m-%dT%H:%M:%S+00:00"))) + 8 * 3600
                    contest['endTime'] = end_time
                    durationSeconds = contest['endTime'] - contest['startTime']
                    if durationSeconds <= 18000 and contest['startTime'] >= int(time.time()):
                        contest_list.append([contest, durationSeconds])
        return contest_list

    async def get_contest_info(self):
        contest_list = await self.get_contest()
        contest_len = len(contest_list)
        if contest_len == 0:
            return "最近没有比赛~"
        if contest_len > 3:
            contest_len = 3
        res = '找到最近的 {} 场 PTYZOJ 比赛为：\n'.format(contest_len)
        for i in range(contest_len):
            next_contest, durationSeconds = contest_list[i][0], contest_list[i][1]
            res += await self.format_ptyzoj_contest(next_contest, durationSeconds)
        return res.rstrip('\n')

    async def get_next_contest(self):
        contest_list = await self.get_contest()
        if not contest_list:
            return "最近没有比赛~", 32536700000, 0
        next_contest, durationSeconds = contest_list[0][0], contest_list[0][1]
        res = await self.format_ptyzoj_contest(next_contest, durationSeconds)
        return res.rstrip('\n'), int(next_contest['startTime']), durationSeconds

    async def get_recent_info(self):
        recent, _, _ = await self.get_next_contest()
        return "PTYZOJ比赛还有15分钟就开始啦，没有报名的尽快报名~\n" + recent

    async def format_ptyzoj_contest(self, next_contest, durationSeconds):
        res = "比赛名称：{}\n" \
              "开始时间：{}\n" \
              "持续时间：{}\n" \
              "比赛地址：{}\n".format(
                  next_contest['contestName'],
                  time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(int(next_contest['startTime']))),
                  "{}小时{:02d}分钟".format(
                      durationSeconds // 3600, durationSeconds % 3600 // 60),
                  next_contest['link']
              )
        return res


    async def update_local_contest(self):
        return True

if __name__ == '__main__':
    name = "guke"
