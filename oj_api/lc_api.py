import json
import pprint
import time
from lxml import etree
from web_operation.operation import *
from oj_api.contest import Contest


class LC(Contest):
    async def update_local_contest(self):
        url_data = "https://leetcode-cn.com/graphql"
        payload = {
            "operationName": "null",
            "query": "{\n  contestUpcomingContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    isLightCardFontColor\n    company {\n      watermark\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {}
        }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip,deflate,br",
            "accept-language": "zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
            "cache-control": "no-cache",
            # "content-length": "329",
            "content-type": "application/json",
            # "cookie": response.cookies,
            "origin": "https://leetcode-cn.com",
            "pragma": "no-cache",
            "referer": "https://leetcode-cn.com/contest/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            # 'x-csrftoken': response.cookies
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url_data, data=json.dumps(payload), headers=headers)

            url_text = response.content.decode()
            json_data = json.loads(url_text)
            with open("./oj_json/lc_contest.json", "w", encoding='utf-8') as f:
                json.dump(json_data, f)
            return True
        except:
            return False

    async def get_contest(self):
        await LC.update_local_contest(self)
        res = []
        with open("./oj_json/lc_contest.json", "r", encoding='utf-8') as f:
            json_data = json.load(f)
        contest_info = json_data['data']['contestUpcomingContests']
        for contest in contest_info:
            # try:
            #     html = etree.HTML(contest['description'])
            #     company = html.xpath("/html/body/div/div/div/p[1]/text()")[0]
            # except:
            #     return []
            info = "比赛名称：{}\n" \
                   "开始时间：{}\n" \
                   "持续时间：{}\n" \
                   "比赛地址：{}".format(
                       "LeetCode " + contest['title'],
                       time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(contest['startTime'])),
                       "{}小时{:02d}分钟".format(
                           contest['duration'] // 3600, contest['duration'] % 3600 // 60),
                       "https://leetcode-cn.com/contest/" + contest['titleSlug'])

            res.append([info, contest['startTime'], contest['duration']])
        res.sort(key=lambda x: x[1], reverse=False)
        return res

    async def get_next_contest(self):
        res = await self.get_contest()
        if res:
            return res[0][0], res[0][1], res[0][2]
        else:
            return "最近没有比赛~", 32536700000, 0

    async def get_contest_info(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return "最近没有比赛~"
        if len(contest_list_lately) > 3:
            find_contest = 3
        else:
            find_contest = len(contest_list_lately)
        res = "找到最近的 {} 场 LeetCode 比赛为：\n".format(find_contest)
        for contest in contest_list_lately[:find_contest]:
            res += contest[0] + '\n'
        return res.rstrip('\n')

    async def get_recent_info(self):
        recent, _, _ = await self.get_next_contest()
        return "LeetCode比赛还有15分钟就开始啦，没有报名的尽快报名~\n" + recent

    async def update_local_rating(self):
        json_data = await get_json(
            "https://raw.iqiq.io/chiehmin/leetcode-ranking-search/master/public/data/global-ranking.json")
        if json_data == -1:
            return False
        with open('./oj_json/lc_rating.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
            return True

    async def get_rating(self, name):
        with open('./oj_json/lc_rating.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for user in json_data:
            if user["realName"] == name:
                return '"{}"rating为: {}，全球ranking为: {}'.format(name, user["rating"].split(".")[0], user["globalRanking"])


if __name__ == '__main__':
    name = "guke"
