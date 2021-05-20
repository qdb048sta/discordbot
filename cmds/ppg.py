import discord, json, time, datetime, asyncio, math
import pandas as pd
from discord.ext import commands
from core.classes import Cog_Extension
from selenium import webdriver
from selenium.webdriver.common.by import By

with open('json\\bestdori.json', 'r', encoding='utf8') as a:
    bestdori = json.load(a)

#設置Webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

class Ppg(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

    #群組point
    @commands.group()
    async def point(self, ctx):
        pass

    #開始追蹤
    @point.command()
    async def runTW(self, ctx):
        await ctx.send("---Start track TW's pts/game---")
        print("---Start track TW's pts/game---")

        async def run():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                Event = [0] * 4
                Id = [0] * 10
                Name = [0] * 10
                Pts = [0] * 10
                Record_pts = [0] * 10
                Cps = [0] * 10
                Record_cps = [0] * 10
                Speed_rank = [0] * 10
                Time = [0] * 1
                Msg = [0] * 1

                data("TW", Event, Id, Name, Pts, Record_pts, Cps, Record_cps, Speed_rank)
                print("data done")

                output(Name, Pts, Record_pts, Cps, Record_cps, Speed_rank, "TW", Time, Event, Msg)
                print("output done")

                await ctx.send(Msg[0])
                print(f"pts/game TW：{Time[0]} Done\n")

                await asyncio.sleep(95)

        self.tw = self.bot.loop.create_task(run())

    @point.command()
    async def runJP(self, ctx):
        await ctx.send("---Start track JP's pts/game---")
        print("---Start track JP's pts/game---")

        async def run():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                Event = [0] * 4
                Id = [0] * 10
                Name = [0] * 10
                Pts = [0] * 10
                Record_pts = [0] * 10
                Cps = [0] * 10
                Record_cps = [0] * 10
                Speed_rank = [0] * 10
                Time = [0] * 1
                Msg = [0] * 1

                data("JP", Event, Id, Name, Pts, Record_pts, Cps, Record_cps, Speed_rank)
                print("data done")

                output(Name, Pts, Record_pts, Cps, Record_cps, Speed_rank, "JP", Time, Event, Msg)
                print("output done")

                await ctx.send(Msg[0])
                print(f"pts/game JP：{Time[0]} Done\n")

                await asyncio.sleep(95)

        self.jp = self.bot.loop.create_task(run())

    #停止追蹤
    @point.command()
    async def stopTW(self, ctx):
        self.tw.cancel()

        await ctx.send("---Stop track TW's pts/game---")
        print("---Stop track TW's pts/game---")

    @point.command()
    async def stopJP(self, ctx):
        self.jp.cancel()

        await ctx.send("---Stop track JP's pts/game---")
        print("---Stop track JP's pts/game---")

    #重置JSON資料庫
    @point.command()
    async def cleanTW(self, ctx):
        with open("json\\pts_per_gameTW.json", "w", encoding = "utf8") as a:
            update = {}

            json.dump(update, a)

        a.close()
        print("---ppgTW.JSON cleaned---")
        await ctx.send("---ppgTW.JSON cleaned---")

    @point.command()
    async def cleanJP(self, ctx):
        with open("json\\pts_per_gameJP.json", "w", encoding = "utf8") as a:
            update = {}

            json.dump(update, a)

        a.close()
        print("---ppgJP.JSON cleaned---")
        await ctx.send("---ppgJP.JSON cleaned---")

#抓Bestdori資料
def data(server, event, id, name, pts, record_pts, cps, record_cps, speed_rank):
    #連結bestdori網站
    Bestdori = webdriver.Chrome(options=options)
    Bestdori.get(bestdori[f"Url {server}"])

    time.sleep(5)
    button_server = Bestdori.find_element_by_xpath(bestdori[f"Button {server}"])
    button_close = Bestdori.find_element_by_xpath(bestdori["Button close"])
    button_interval = Bestdori.find_element_by_xpath(bestdori["Button interval"])

    button_server.click()
    button_close.click()
    time.sleep(2)
    button_interval.click()
    time.sleep(6)
    print("連結bestdori網站 done")

    #抓資料
    event[0] = Bestdori.find_element_by_xpath(bestdori["Event title"]).text
    event[1] = Bestdori.find_element_by_xpath(bestdori["Event url"]).get_attribute('href')
    event[2] = Bestdori.find_element_by_xpath(bestdori["Event type"]).text
    event[3] = Bestdori.find_element_by_xpath(bestdori["Event banner"]).get_attribute('src')

    for i in range(10):
        #UID
        id[i] = Bestdori.find_element_by_xpath(bestdori["Id"][i]).text

        #名字、避免有人取空白
        try:
            name[i] = Bestdori.find_element_by_xpath(bestdori["Name"][i]).text
        except:
            name[i] = ""

        #PT
        pts[i] = Bestdori.find_element_by_xpath(bestdori["Pts"][i]).text
        pts[i] = int(pts[i][:pts[i].find(" Pts")])

    Bestdori.close()
    print("抓資料 done")

    #時速、CP計算
    with open(f"json\\pts_per_game{server}.json", "r", encoding = "utf8") as b:
        r = json.load(b)
        speed = [0] * 10

        for i in range(10):
            #原先就在10位中則計算時速，剛刺進來則不計算
            if id[i] in r:
                record_pts[i] = pts[i] - int(r[id[i]])
            else:
                record_pts[i] = "---"

            #CP計算
            if record_pts[i] != "---" and record_pts[i] < 15000:
                record_cps[i] = math.ceil(record_pts[i] / 20)
            elif record_pts[i] != "---" and record_pts[i] > 40000:
                record_cps[i] = -1600
            elif record_pts[i] != "---" and record_pts[i] > 15000:
                record_cps[i] = -800
            else:
                pass

            #將時速加上千分符
            if isinstance(record_pts[i], int):
                speed[i] = record_pts[i]
                record_pts[i] = format(record_pts[i], ",")
            else:
                speed[i] = 0

    b.close()
    print("時速、CP計算 done")

    #時速排名
    Record_speed = pd.Series([speed[0], speed[1], speed[2], speed[3], speed[4], speed[5], speed[6], speed[7], speed[8], speed[9]])
    Rank_speed = (Record_speed.rank(ascending = False, method = "max")).values

    for i in range(10):
        speed_rank[i] = Rank_speed[i]
    print("時速排名 done")

    #T10分數更新
    with open(f"json\\pts_per_game{server}.json", "w", encoding = "utf8") as c:
        update = {id[0] : pts[0], 
        id[1] : pts[1], 
        id[2] : pts[2], 
        id[3] : pts[3], 
        id[4] : pts[4], 
        id[5] : pts[5], 
        id[6] : pts[6], 
        id[7] : pts[7], 
        id[8] : pts[8], 
        id[9] : pts[9],}

        json.dump(update, c)

    c.close()
    print("T10分數更新 done")

    #CP計算2
    with open(f"json\\cps_per_game{server}.json", "r", encoding = "utf8") as d:
        r = json.load(d)

        for i in range(10):
            #原先就在10位中則計算CP，剛刺進來則不計算
            if id[i] in r:
                cps[i] = int(r[id[i]]) + record_cps[i]
            else:
                cps[i] = 0

    d.close()
    print("CP計算2 done")

    #CP更新
    with open(f"json\\cps_per_game{server}.json", "w", encoding = "utf8") as e:
        update = {id[0] : cps[0], 
        id[1] : cps[1], 
        id[2] : cps[2], 
        id[3] : cps[3], 
        id[4] : cps[4], 
        id[5] : cps[5], 
        id[6] : cps[6], 
        id[7] : cps[7], 
        id[8] : cps[8], 
        id[9] : cps[9],}

        json.dump(update, e)

    e.close()
    print("CP更新 done")

#文字排版後輸出
def output(name, pts, record_pts, cps, record_cps, speed_rank, server, time, event, msg):
    msg_title = [0] * 7
    msg_title[1] = '%3s' % "#"
    msg_title[2] = '%13s' % "Pts"
    msg_title[3] = '%10s' % "Pts/game"
    msg_title[4] = '%3s' % "#"
    msg_title[5] = '%11s' % "Cps"
    msg_title[6] = '%9s' % "Cps/game"

    if event[2] == "Challenge Live":
        msg_title[0] = f"{msg_title[1]}　{msg_title[2]}   {msg_title[3]}  {msg_title[4]}   {msg_title[5]}  {msg_title[6]}    Player"
    else:
        msg_title[0] = f"{msg_title[1]}　{msg_title[2]}   {msg_title[3]}  {msg_title[4]}    Player"    

    msg_rank = [0] * 10
    msg_pts = [0] * 10
    msg_record_pt = [0] * 10
    msg_speed = [0] * 10
    msg_cp = [0] * 10
    msg_record_cp = [0] * 10
    msg_content = [0] * 10
    for i in range(10):
        j = i + 1

        msg_rank[i] = '%3s' % j
        msg_pts[i] = '%13s' % format(pts[i], ',') #將pt加上千分符
        msg_record_pt[i] = '%10s' % record_pts[i]
        msg_speed[i] = '%3s' % int(speed_rank[i])
        msg_cp[i] = '%11s' % format(cps[i], ',') #將cp加上千分符
        msg_record_cp[i] = '%9s' % record_cps[i]

        if event[2] == "Challenge Live":
            msg_content[i] = f"{msg_rank[i]}位{msg_pts[i]}  |{msg_record_pt[i]}  {msg_speed[i]}  |{msg_cp[i]}  {msg_record_cp[i]}  | {name[i]}"
        else:
            msg_content[i] = f"{msg_rank[i]}位{msg_pts[i]}  |{msg_record_pt[i]}  {msg_speed[i]}  | {name[i]}"

    if server == "TW":
        time[0] = "{:%Y-%m-%d %H:%M:%S} - {}".format(datetime.datetime.now() + datetime.timedelta(hours = 0), "UTC+8")
    elif server == "JP":
        time[0] = "{:%Y-%m-%d %H:%M:%S} - {}".format(datetime.datetime.now() + datetime.timedelta(hours = 1), "UTC+9")

    msg[0] = f"```　Server: {server} \n　Time: {time[0]} \n　Event: {event[0]} \n　Type: {event[2]} \n\n{msg_title[0]}\n{msg_content[0]}\n{msg_content[1]}\n{msg_content[2]}\n{msg_content[3]}\n{msg_content[4]}\n{msg_content[5]}\n{msg_content[6]}\n{msg_content[7]}\n{msg_content[8]}\n{msg_content[9]}```"

def setup(bot):
    bot.add_cog(Ppg(bot))