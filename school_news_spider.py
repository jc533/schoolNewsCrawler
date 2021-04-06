import requests,pandas,os
from pyquery import PyQuery as pq
import webbrowser
from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

CHANNEL_ACCESS_TOKEN = 'i76IuvwpBRgV3j2jkLcQ73fy0InOTA3fExe0u0hX4LSd74KWbV1Nt8Rik+vTIhkzIZuo8ksuhBSXMk3eiYzV418EcuRkYc0o+1jOsR79pTExl6VmbkfTOdUAn3DToeE+o7EUkicZsh2uOu4IZXSAxAdB04t89/1O/w1cDnyilFU='
to = "U5387d7168fd38f08da16ec6c70871cca"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=12)
def main():
    r = requests.get("http://web.ck.tp.edu.tw/web2007/index.php")
    r.encoding = 'utf-8'

    html = pq(r.text)

    table = []
    tmp = []
    
    for i in html("table #ann tr").items():
        if i(".office").text():
            tmp.append(i(".office").text())
        if i(".time").text():
            tmp.append(i(".time").text())
        if i("a").attr("href"):
            tmp.append(i("a").text())
            tmp.append(i("a").attr("href"))
        if len(tmp) == 4:
            table.append(tmp)
            tmp = []

    print(table)
    # dfs = pandas.read_csv("result.csv")
    # dfs = dfs.ix[:,1:]
    # print(dfs)

    # df = pandas.DataFrame(table, columns=["office", "time","text","url"])
    # ne = df.equals(dfs)
    # # print(df.ix[:,2] == dfs.ix[:,2])
    # old = list(dfs.ix[:, 2])
    # new = list(df.ix[:, 2])
    # if not ne or not old == new:
    #     df.to_csv("result.csv")
        # line_bot_api.push_message(to, TextSendMessage(text='校網有新訊息'))
    # line_bot_api.push_message(to, TextSendMessage(text='test'))

# @sched.scheduled_job('interval',minutes=10)
# def p():
#     print("p\n")


# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=12, minute=20)
# def test():
#     print("testing")
#     line_bot_api.push_message(to, TextSendMessage(text='testing'))



if __name__ == '__main__':
    # sched.start()
    main()
# print(compare_two_dfs(df,dfs))
