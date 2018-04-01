"""授業変更を確認し、LINE Notify経由で通知する
"""

import lessonData
import logging.config
import pandas as pd
import lineNotify
import annualData as ad
import pandas.tseries.offsets as offsets

# ロガー設定
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 明日の授業変更を持ってくる
data_5e_tomorrow = pd.read_csv('tomorrow.csv')

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

# line Notifyにポスト
ln = lineNotify.LineNotify()
ln.multi_post(msgs)
