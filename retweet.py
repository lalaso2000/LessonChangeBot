"""授業変更をリツイートする
"""

import tweetBot
import csv
import logging.config
import db

# ロガー設定
logging.config.fileConfig('logging.conf')

# bot起動
tbot = tweetBot.TweetBot()
# リツイートするidリストを読み込む
dbx = db.DB()
dbx.download('./ids.csv', '/ids.csv')
with open('ids.csv', 'r') as f:
    reader = csv.reader(f)
    _ = [e for e in reader]
    ids = _[0]
print(ids)
# リツートする
for i in ids:
    tbot.retweet(i)
    # print(result)
