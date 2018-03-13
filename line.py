"""授業変更を確認し、LINE Notify経由で通知する
"""

import lessonData
import logging.config
import pandas as pd
import lineNotify

# ロガー設定
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 明日の授業変更を持ってくる
data_5e_tomorrow = pd.read_csv('tomorrow.csv')

# メッセージを作る
msgs = []
for index, d in data_5e_tomorrow.iterrows():
    msgs.append(lessonData.create_tweet(d))
# print(msgs)

# line Notifyにポスト
ln = lineNotify.LineNotify()
ln.multi_post(msgs)
