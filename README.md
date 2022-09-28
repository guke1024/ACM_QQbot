本项目是一个在群里可以通知打codeforces、牛客、AtCoder、LeetCode的qq机器人项目，基于<a href="https://github.com/INGg/ACM_Contest_QQbot" target="__blank">
ACM_Contest_QQbot</a>修改（膜拜<a href="https://github.com/INGg" target="__blank">INGg巨巨</a>
![worship.gif](https://s2.loli.net/2022/02/27/VexPg9Nb5AT8cD3.gif) ）。

## 本项目与原项目的区别

1. 将 codeforces 、牛客、atc、LeetCode的比赛以json形式保存在本地；
2. ~~把本校ACM实验室成员的 codeforces rating 数据以json的形式保存在本地；~~ 将添加的cf用户rating数据以json形式保存到本地，同时将不同群添加的cf用户进行分离，每个群在进行cf总查询时仅显示本群所有cf用户信息
3. 把本校所有牛客用户的牛客 rating 数据以 json 形式保存在本地。
4. 将所有定时任务放入一个函数统一处理
5. 拥有今日人品功能
6. 添加图片时可判断该图片是否已在图库中存在
7. 可查询LeetCode分数
8. **不拥有**随机cf
9. 其他类似功能部分有所出入

提供定时/手动更新本地数据功能，仅在更新时与cf、牛客、atc、LeetCode进行交互，加速用户使用机器人时的查询速度并降低了被反爬虫的概率。

## 功能介绍  
- next -> 查询最近一场比赛
- today -> 查询今天比赛
- cf(不区分大小写)/牛客/atc(不区分大小写)/lc(不区分大小写) -> 查询最近三场cf/牛客/atc/lc比赛
- 查询cf/牛客/atc分数id -> 查询对应id的cf/牛客/atc分数(已解决牛客模糊查询导致结果不准确的问题)
- 更新cf/牛客分数 -> 更新本地所有用户的cf/牛客分数
- 添加cf用户id -> 添加对应id的cf用户及其相关信息到本地json文件中
- 删除cf用户id -> 删除本地json文件中的cf用户
- 随机蕊神/来只蕊神 -> 随机蕊神语录
- 来只清楚 -> 随机qcjj/固定群聊其他人的语录
- 添加蕊神/添加清楚 -> 使用该命令回复图片即可添加到本地图库中(已做权限处理)
- setu/涩图 -> 涩图
- 每天定时发送当天比赛
- cf、牛客、atc、LeetCode比赛前十五分钟提醒报名参加
- cf的rating分群管理，不同群之间cf总查询的结果只会是当前群曾添加的cf用户
- 订阅cf/牛客/lc/atc -> 在这些比赛开始前15分钟发送报名定时提醒，cf和牛客还有准时的上号提醒
- 订阅每日提醒 -> 每天早上8点发送当日比赛
- 取消订阅cf/牛客/lc/atc/每日提醒 -> 取消这些订阅

## 部署方法
1. 请直接参考原项目部署方法进行部署
2. 部署成功后，将yirimirai部署教程中的net.mamoe.mirai-api-http文件夹下的setting.yml里的端口号改成7275
3. 创建oj_json文件夹，在里面创建**cf_contest.json**、**cf_rating.json**、**lc_contest.json**、**nc_rating.json**、**contests.json**、**subscribe.json**等文件
4. 在cf_rating.json文件中添加以下内容
```json
{
    "all_rating": {}
}
```
5. 在subscribe.json文件中添加以下内容
```json
{
    "cf": {},
    "\u725b\u5ba2": {},
    "lc": {},
    "atc": {},
    "today": {}
}
```
6. 在cf_contest.json、lc_contest.json文件中添加以下内容
```json
{}
```
7. 在contests.json文件中添加以下内容
```json
[]
```

## 一点建议
强烈建议使用本项目的朋友 clone 项目到本地后，使用 cloudflare 分别做 codeforces 和 atcoder 的镜像站，然后将 `cf_api.py` 和 `atc_api.py` 中的用户 rating 查询函数的链接替换为你自己的镜像站链接。

该操作将在一定程度上起到反爬虫、加速访问 codeforces 和 atcoder 以及避免这两个网站在访问峰值时访问过慢导致查询失败的作用。

**cloudflare 可以使用免费版，每天有 10 万次请求额度，需要注意的是，workers.dev 域名被污染，在国内已经无法访问，需要使用自己的域名作为 worker 的路由，如果没有域名或者买不起域名，可以使用 freenom 申请免费域名。**

**作者并不解答 cloudflare 制作镜像站以及 freenom 申请免费域名这两个操作中遇到的问题，如果需要使用该方案或者遇到问题请自行 google。**