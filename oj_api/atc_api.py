import re
import json
import time
from web_operation.operation import *
from oj_api.contest import Contest


class ATC(Contest):
    async def get_contest(self):
        with open('./oj_json/nc_contest.json', 'r', encoding='utf-8') as f:
            contest_data = json.load(f)
        contest_list = []
        for contest in contest_data:
            if contest['ojName'] == 'AtCoder' and contest['startTime'] >= int(time.time()) * 1000:
                lately_contest = contest
                if lately_contest.__contains__('endTime') and lately_contest.__contains__('startTime'):
                    durationSeconds = (int(lately_contest['endTime']) - int(lately_contest['startTime'])) // 1000
                    contest_list.append([lately_contest, durationSeconds])
        return contest_list

    async def get_contest_info(self):
        contest_list = await self.get_contest()
        contest_len = len(contest_list)
        if contest_len == 0:
            return "最近没有比赛~"
        if contest_len > 3:
            contest_len = 3
        res = '找到最近的 {} 场Atc比赛为：\n'.format(contest_len)
        for i in range(contest_len):
            next_contest, durationSeconds = contest_list[i][0], contest_list[i][1]
            res += await self.format_atc_contest(next_contest, durationSeconds)
        return res.rstrip('\n')

    async def get_next_contest(self):
        contest_list = await self.get_contest()
        if not contest_list:
            return "最近没有比赛~", 32536700000, 0
        next_contest, durationSeconds = contest_list[0][0], contest_list[0][1]
        res = await self.format_atc_contest(next_contest, durationSeconds)
        return res.rstrip('\n'), int(next_contest['startTime'] // 1000), durationSeconds

    async def format_atc_contest(self, next_contest, durationSeconds):
        res = "比赛名称：{}\n" \
              "开始时间：{}\n" \
              "持续时间：{}\n" \
              "比赛地址：{}\n".format(
            next_contest['contestName'],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(next_contest['startTime']) // 1000)),
            "{}小时{:02d}分钟".format(durationSeconds // 3600, durationSeconds % 3600 // 60),
            next_contest['link']
        )
        return res

    async def get_rating(self, name):  # 返回一个列表，如果不存在用户则是空列表
        url = "https://atcoder.jp/users/" + name
        html = await get_html(url)
        r = r'<th class="no-break">Rating<\/th><td><span class=(.*?)>(.*?)<\/span>'
        results = re.findall(r, html, re.S)
        try:
            return results[0][1]
        except:
            return -1

    async def update_local_contest(self):
        return True


if __name__ == '__main__':
    name = "guke"
