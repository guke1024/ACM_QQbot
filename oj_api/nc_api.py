import json
from web_operation.operation import *
import time
from lxml import etree
import requests
from oj_api.contest import Contest


class NC(Contest):
    async def request_rating(self, name):
        url = "https://ac.nowcoder.com/acm/contest/rating-index?searchUserName=" + name
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        try:
            resp = requests.get(url=url, headers=headers)
            text = resp.text
            zm = text.encode(resp.encoding).decode('utf-8')
            xx = etree.fromstring(zm, parser=etree.HTMLParser())
            return xx.xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr[*]')
        except:
            return False

    async def update_all_nc_rating(self):
        school_name = "黄冈师范学院"
        items = await self.request_rating(school_name)
        if items:
            all_rating = {}
            for item in items:
                username = item.xpath('./td[2]/a/span/text()')[0]
                rating = item.xpath('./td[5]/span/text()')[0]
                all_rating[username] = rating
            with open("./oj_json/nc_rating.json", 'w', encoding='utf-8') as f:
                json.dump(all_rating, f)
            return True
        else:
            return False

    async def get_rating(self, uname):
        with open("./oj_json/nc_rating.json", 'r', encoding='utf-8') as f:
            all_rating = json.load(f)
        if uname in all_rating:
            return "“{}”当前牛客rating为：{}".format(uname, all_rating[uname])
        else:
            items = await self.request_rating(uname)
            if items:
                for item in items:
                    username = item.xpath('./td[2]/a/span/text()')[0]
                    rating = item.xpath('./td[5]/span/text()')[0]
                    if username == uname:
                        return "“{}”当前牛客rating为：{}".format(uname, rating)
            else:
                return False

    async def update_local_contest(self):
        url = "https://contests.sdutacm.cn/contests.json"
        json_data = await get_json(url)
        if json_data == -1:
            return False
        with open('./oj_json/contests.json', 'w') as f:
            json.dump(json_data, f, indent=4)
        return True

    async def get_contest(self):
        with open('./oj_json/contests.json', 'r', encoding='utf-8') as f:
            contest_data = json.load(f)
        contest_list = []
        if contest_data != []:
            for contest in contest_data:
                if contest['source'] == '牛客竞赛' and "专题" not in contest['name']:
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

    async def format_nc_contest(self, next_contest, durationSeconds):
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

    async def get_next_contest(self):
        contest_list = await self.get_contest()
        if not contest_list:
            return "最近没有比赛~", 32536700000, 0
        next_contest, durationSeconds = contest_list[0][0], contest_list[0][1]
        res = await self.format_nc_contest(next_contest, durationSeconds)
        return res.rstrip('\n'), next_contest['startTime'], durationSeconds

    async def get_recent_info(self):
        recent, _, _ = await self.get_next_contest()
        return "牛客比赛还有15分钟就开始啦，没有报名的尽快报名~\n" + recent

    async def get_contest_info(self):
        contest_list = await self.get_contest()
        contest_len = len(contest_list)
        if contest_len == 0:
            return False
        if contest_len > 3:
            contest_len = 3
        res = '找到最近的 {} 场牛客比赛为：\n'.format(contest_len)
        for i in range(contest_len):
            next_contest, durationSeconds = contest_list[i][0], contest_list[i][1]
            res += await self.format_nc_contest(next_contest, durationSeconds)
        return res.rstrip('\n')


if __name__ == '__main__':
    # pprint.pprint(asyncio.run(update_all_nc_rating()))
    # asyncio.run(update_all_nc_contest())
    name = "guke"
