import json
import time
from web_operation.operation import *
from oj_api.contest import Contest


class CF(Contest):
    async def get_rating(self, name):
        def pd_color(rating):
            if rating < 1200:
                return "灰名隐藏大佬"
            if rating < 1400:
                return '绿名Pupil'
            if rating < 1600:
                return '青名Specialist'
            if rating < 1900:
                return '蓝名Expert'
            if rating < 2100:
                return '紫名Candidate master'
            if rating < 2300:
                return '橙名International Master'
            if rating < 2400:
                return '橙名Master'
            if rating < 2600:
                return '红名Grandmaster'
            if rating < 3000:
                return '红名巨巨'
            else:
                return '黑红名神犇'

        with open('./oj_json/cf_rating.json', 'r', encoding='utf-8') as f:
            all_rating = json.load(f)
            rating = all_rating["all_rating"]
            if name in rating:
                rating_info = rating[name]
                if rating_info[0] == 0:
                    return '"{}"还未进行过比赛\n'.format(name)
                return '"{}"是{}，当前rating为：{}'.format(name, pd_color(rating_info[0]), rating_info[0])
        url = "https://codeforces.com/api/user.rating?handle=" + name
        json_data = await get_json(url)
        if json_data == -1:
            return "查询失败！"
        json_data = dict(json_data)
        if json_data['status'] == "OK":
            json_data = json_data['result']
            if len(json_data) == 0:
                return '"{}"还未进行过比赛\n'.format(name)
            final_contest = json_data[-1]
            return '"{}"是{}，当前rating为：{}'.format(name, pd_color(int(final_contest['newRating'])),
                                                 final_contest['newRating'])
        else:
            return "该用户不存在！"

    # 查询cf最近一次结束的比赛，筛除Kotlin比赛及Div .1难度
    async def get_final_contest(self):
        url = "https://codeforces.com/api/contest.list?gym=false"
        json_data = await get_json(url)
        if json_data == -1:
            return ''
        json_data = dict(json_data)
        if json_data['status'] == "OK":
            contest_list_all = list(json_data['result'])
            for contest in contest_list_all:
                if contest['relativeTimeSeconds'] > 0:
                    if 'Kotlin' not in contest['name']:
                        if 'Unrated' not in contest['name']:
                            if 'Div. 2' in contest['name'] or 'Div. 3' in contest['name'] or 'Div. 4' in contest[
                                    'name'] or 'Codeforces Global Round' in contest['name']:
                                final_contest = contest
                                return final_contest

    # 查询用户的rating总信息
    async def query_user_rating(self, uname, final_contest):
        url = "https://codeforces.com/api/user.rating?handle=" + uname
        json_data = await get_json(url)
        if json_data == -1:
            return []
        json_data = dict(json_data)
        if json_data['status'] == "OK":
            json_data = json_data['result']
            if len(json_data) == 0:
                return [0, 0]
            final_rating = json_data[-1]
            if final_rating['contestId'] != final_contest['id']:
                differ = 'X'
            else:
                differ = int(final_rating['newRating']) - \
                    int(final_rating['oldRating'])
                if differ > 0:
                    differ = '+' + str(differ)
                else:
                    differ = str(differ)
            return [final_rating['newRating'], differ]
        else:
            return []

    # 更新本地存储用户的rating信息
    async def update_rating(self):
        res = ''
        rating = {}
        final_contest = await self.get_final_contest()
        if not final_contest:
            return ''
        f = open('./oj_json/cf_rating.json', 'r+', encoding='utf-8')
        all_rating = json.load(f)
        local_rating = all_rating["all_rating"]
        for uname in local_rating:
            print(uname)
            rating_info = await self.query_user_rating(uname, final_contest)
            if not rating_info:
                return ''
            rating[uname] = rating_info
        rating = dict(
            sorted(rating.items(), key=lambda x: x[1][0], reverse=True))
        all_rating["all_rating"] = rating
        f.seek(0)
        f.truncate()
        json.dump(all_rating, f, indent=4)
        f.close()
        for uname in rating:
            res += await self.format_rating_res(uname, rating[uname])
        return res.rstrip('\n')

    async def auto_update(self):
        final_contest = await self.get_final_contest()
        up = final_contest['startTimeSeconds'] + \
            final_contest['durationSeconds']
        if final_contest['type'] == 'ICPC':
            up += 25 * 60 * 60
        else:
            up += 6 * 60 * 60
        return up

    # 获取本地存储所有用户rating信息
    async def get_cf_rating(self, group_id):
        res = ''
        with open('./oj_json/cf_rating.json', 'r', encoding='utf-8') as f:
            all_rating = json.load(f)
            if group_id not in all_rating:
                return "本群暂未添加任何cf用户"
            unames = all_rating[group_id]
            rating = all_rating["all_rating"]
            for uname in rating:
                if uname in unames:
                    res += await self.format_rating_res(uname, rating[uname])
            return res.rstrip('\n')

    # 为本地添加新用户及rating信息
    async def add_cf_user(self, uname, group_id):
        with open('./oj_json/cf_rating.json', 'r+', encoding='utf-8') as f:
            all_rating = json.load(f)
            rating = all_rating["all_rating"]
            if group_id not in all_rating:
                all_rating[group_id] = []
            if uname in all_rating[group_id]:
                return True
            else:
                if uname in rating:
                    all_rating[group_id].append(uname)
                    f.seek(0)
                    f.truncate()
                    json.dump(all_rating, f, indent=4)
                    return True
                final_contest = await self.get_final_contest()
                if not final_contest:
                    return False
                rating_info = await self.query_user_rating(uname, final_contest)
                all_rating[group_id].append(uname)
                if rating_info:
                    rating[uname] = rating_info
                    rating = dict(
                        sorted(rating.items(), key=lambda x: x[1][0], reverse=True))
                    all_rating["all_rating"] = rating
                    f.seek(0)
                    f.truncate()
                    json.dump(all_rating, f, indent=4)
                    return True
                else:
                    return False

    # 删除本地存储用户
    async def del_cf_user(self, uname, group_id):
        with open('./oj_json/cf_rating.json', 'r+', encoding='utf-8') as f:
            all_rating = json.load(f)
            rating = all_rating["all_rating"]
            if uname not in rating or uname == "wentaotao":
                return False
            for k in all_rating:
                if k != "all_rating" and k != group_id:
                    if uname in all_rating[k]:
                        break
            else:
                del rating[uname]
            all_rating[group_id].remove(uname)
            f.seek(0)
            f.truncate()
            json.dump(all_rating, f, indent=4)
            return True

    # 格式化查询cf rating输出
    async def format_rating_res(self, uname, rating_info):
        if rating_info[0] == 0:
            return '"{}"还未进行过比赛\n'.format(uname)
        return '"{}"：{}，{}\n'.format(uname, rating_info[0], rating_info[1])

    async def update_local_contest(self):
        url = "https://codeforces.com/api/contest.list?gym=false"
        json_data = await get_json(url)
        if json_data == -1:
            return False
        json_data = dict(json_data)
        if json_data['status'] == "OK":
            with open('./oj_json/cf_contest.json', 'w') as f:
                json.dump(json_data, f)
        return True

    async def get_contest(self):
        with open('./oj_json/cf_contest.json', 'r') as f:
            json_data = json.load(f)
            contest_list_all = list(json_data['result'])
            contest_list_lately = []

            for contest in contest_list_all:
                if contest['relativeTimeSeconds'] < 0:
                    if contest['name'][:6] != 'Kotlin':
                        if 'Unrated' not in contest['name']:
                            contest_list_lately.append(contest)
                else:
                    break
        if contest_list_lately:
            contest_list_lately.sort(key=lambda x: (
                x['relativeTimeSeconds'], x['name']), reverse=True)
        return contest_list_lately

    async def get_next_contest(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return "最近没有比赛~", 32536700000, 0
        else:
            for contest in contest_list_lately:
                res = await self.format_cf_contest(contest)
                return res, int(contest['startTimeSeconds']), int(contest['durationSeconds'])

    async def get_contest_info(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return "最近没有比赛~"
        if len(contest_list_lately) > 3:
            find_contest = 3
        else:
            find_contest = len(contest_list_lately)
        res = "找到最近的 {} 场 cf 比赛为：\n".format(find_contest)
        for contest in contest_list_lately[:find_contest]:
            res += await self.format_cf_contest(contest) + '\n'
        return res.rstrip('\n')

    async def get_recent_info(self):
        recent, _, _ = await self.get_next_contest()
        return "cf比赛还有15分钟就开始啦，没有报名的尽快报名~\n" + recent

    async def format_cf_contest(self, contest):
        contest_url = "https://codeforces.com/contest/"
        return "比赛名称：{}\n开始时间：{}\n持续时间：{}\n比赛地址：{}".format(
            contest['name'],
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(int(contest['startTimeSeconds']))),
            "{}小时{:02d}分钟".format(
                contest['durationSeconds'] // 3600, contest['durationSeconds'] % 3600 // 60),
            contest_url + str(contest['id'])
        )


if __name__ == '__main__':
    # name = input()
    name = "guke"

    # asyncio.run(get_usr_rating(name))
    # while True:
    #     name = input()
    #     print(asyncio.run(get_usr_rating(name)))
    # pprint.pprint(asyncio.run(get_hgnu_rating()))
    # asyncio.run(update_cf_contest())
    # pprint.pprint(asyncio.run(get_contest_info()))
    # pprint.pprint(asyncio.run(get_next_contest()))
    # pprint.pprint(asyncio.run(get_contest()))
