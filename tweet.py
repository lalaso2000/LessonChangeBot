"""授業変更を確認し、つぶやく
"""

import lessonData
import tweetBot
import csv
import logging.config
import pandas as pd
import annualData as ad
import pandas.tseries.offsets as offsets
import db

# 明日の授業変更を持ってくる
data_5e_tomorrow = pd.read_csv('tomorrow.csv')

# ロガー設定
logging.config.fileConfig('logging.conf')
# logger = logging.getLogger()

# 年間行事予定を取得する
annual_data = ad.get_data()

# 明日の日付を取得
tomorrow = (pd.datetime.today() + offsets.Day()).normalize()

# 明日の行事予定を取得する
annual_tomorrow = ad.search_for_date(annual_data, tomorrow)

# メッセージを作る
msgs = []
for index, d in data_5e_tomorrow.iterrows():
    msgs.append(lessonData.create_tweet(d))
# print(msgs)

for index, d in annual_tomorrow.iterrows():
    msgs.append(ad.create_tweet(d))

# twitterのbotを呼び出す
tbot = tweetBot.TweetBot()
ids = []
# つぶやく
for m in msgs:
    result = tbot.tweet(m)
    if result is not None:
        # つぶやけたらidを記憶する。
        ids.append(result.id)
# idをcsvに保存
with open('ids.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(ids)

# csvをdropboxに保存
dbx = db.DB()
dbx.upload('./ids.csv', '/ids.csv')
