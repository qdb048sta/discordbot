import discord, json, time, datetime, asyncio
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

class Rank(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

    #群組rank
    @commands.group()
    async def rank(self, ctx):
        pass

    #開始追蹤
    @rank.command()
    async def runTW(self, ctx):
        await ctx.send("---Start track TW's pts/hr---")
        print("---Start track TW's pts/hr---")

        async def run():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                Time_min = datetime.datetime.now().strftime("%M")

                if Time_min == "00":
                    Event = [0] * 4
                    Id = [0] * 10
                    Name = [0] * 10
                    Pts = [0] * 10
                    Record = [0] * 10
                    Speed_rank = [0] * 10
                    Time = [0] * 1
                    Msg = [0] * 1

                    data("TW", Event, Id, Name, Pts, Record, Speed_rank)
                    print("data done")

                    output(Name, Pts, Record, Speed_rank, "TW", Time, Event, Msg)
                    print("output done")

                    await ctx.send(Msg[0])
                    print(f"pts/hr TW：{Time[0]} Done\n")

                    await asyncio.sleep(3540)

                else:
                    await asyncio.sleep(1)
                    pass

        self.tw = self.bot.loop.create_task(run())

    @rank.command()
    async def runJP(self, ctx):
        await ctx.send("---Start track JP's pts/hr---")
        print("---Start track JP's pts/hr---")

        async def run():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                Time_min = datetime.datetime.now().strftime("%M")

                if Time_min == "00":
                    Event = [0] * 4
                    Id = [0] * 10
                    Name = [0] * 10
                    Pts = [0] * 10
                    Record = [0] * 10
                    Speed_rank = [0] * 10
                    Time = [0] * 1
                    Msg = [0] * 1

                    data("JP", Event, Id, Name, Pts, Record, Speed_rank)
                    print("data done")

                    output(Name, Pts, Record, Speed_rank, "JP", Time, Event, Msg)
                    print("output done")

                    await ctx.send(Msg[0])
                    print(f"pts/hr JP：{Time[0]} Done\n")

                    await asyncio.sleep(3540)

                else:
                    await asyncio.sleep(1)
                    pass

        self.jp = self.bot.loop.create_task(run())

    #停止追蹤
    @rank.command()
    async def stopTW(self, ctx):
        self.tw.cancel()

        await ctx.send("---Stop track TW's pts/hr---")
        print("---Stop track TW's pts/hr---")

    @rank.command()
    async def stopJP(self, ctx):
        self.jp.cancel()

        await ctx.send("---Stop track JP's pts/hr---")
        print("---Stop track JP's pts/hr---")

    #重置JSON資料庫
    @rank.command()
    async def cleanTW(self, ctx):
        with open("json\\rankTW.json", "w", encoding = "utf8") as a:
            update = {}

            json.dump(update, a)

        a.close()
        print("---rankTW.JSON cleaned---")
        await ctx.send("---rankTW.JSON cleaned---")

    @rank.command()
    async def cleanJP(self, ctx):
        with open("json\\rankJP.json", "w", encoding = "utf8") as a:
            update = {}

            json.dump(update, a)

        a.close()
        print("---rankJP.JSON cleaned---")
        await ctx.send("---rankJP.JSON cleaned---")


#抓Bestdori資料
def data(server, event, id, name, pts, record, speed_rank):
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

    #時速計算
    with open(f"json\\rank{server}.json", "r", encoding = "utf8") as b:
        r = json.load(b)
        speed = [0] * 10

        for i in range(10):
            #原先就在10位中則計算時速，剛刺進來則不計算
            if id[i] in r:
                record[i] = pts[i] - int(r[id[i]])
            else:
                record[i] = "---"

            #將時速加上千分符
            if isinstance(record[i], int):
                speed[i] = record[i]
                record[i] = format(record[i], ",")
            else:
                speed[i] = 0

    b.close()
    print("時速計算 done")

    #時速排名
    Record_speed = pd.Series([speed[0], speed[1], speed[2], speed[3], speed[4], speed[5], speed[6], speed[7], speed[8], speed[9]])
    Rank_speed = (Record_speed.rank(ascending = False, method = "max")).values

    for i in range(10):
        speed_rank[i] = Rank_speed[i]
    print("時速排名 done")

    #T10分數更新
    with open(f"json\\rank{server}.json", "w", encoding = "utf8") as c:
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

#文字排版後輸出
def output(name, pts, record, speed_rank, server, time, event, msg):
    msg_title = [0] * 5
    msg_title[1] = '%3s' % "#"
    msg_title[2] = '%13s' % "Pts"
    msg_title[3] = '%10s' % "Pts/hr"
    msg_title[4] = '%3s' % "#"
    msg_title[0] = f"{msg_title[1]}　{msg_title[2]}   {msg_title[3]}  {msg_title[4]}    Player"

    msg_rank = [0] * 10
    msg_pts = [0] * 10
    msg_record = [0] * 10
    msg_speed = [0] * 10
    msg_content = [0] * 10
    for i in range(10):
        j = i + 1

        msg_rank[i] = '%3s' % j
        msg_pts[i] = '%13s' % format(pts[i], ',') #將pt加上千分符
        msg_record[i] = '%10s' % record[i]
        msg_speed[i] = '%3s' % int(speed_rank[i])
        msg_content[i] = f"{msg_rank[i]}位{msg_pts[i]}  |{msg_record[i]}  {msg_speed[i]}  | {name[i]}"

    if server == "TW":
        time[0] = "{:%Y-%m-%d %H:%M:%S} - {}".format(datetime.datetime.now() + datetime.timedelta(hours = 0), "UTC+8")
    elif server == "JP":
        time[0] = "{:%Y-%m-%d %H:%M:%S} - {}".format(datetime.datetime.now() + datetime.timedelta(hours = 1), "UTC+9")

    msg[0] = f"```　Server: {server} \n　Time: {time[0]} \n　Event: {event[0]} \n　Type: {event[2]} \n\n{msg_title[0]}\n{msg_content[0]}\n{msg_content[1]}\n{msg_content[2]}\n{msg_content[3]}\n{msg_content[4]}\n{msg_content[5]}\n{msg_content[6]}\n{msg_content[7]}\n{msg_content[8]}\n{msg_content[9]}```"

def setup(bot):
    bot.add_cog(Rank(bot))