"""授業変更を確認し、つぶやく
"""

import lessonData
import tweetBot
import csv
import logging.config
import pandas as pd


def main():
    # 明日の授業変更を持ってくる
    data_5e_tomorrow = pd.read_csv('tomorrow.csv')

    # ロガー設定
    logging.config.fileConfig('logging.conf')
    # logger = logging.getLogger()

    # メッセージを作る
    msgs = []
    for index, d in data_5e_tomorrow.iterrows():
        msgs.append(lessonData.create_tweet(d))
    # print(msgs)

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


if __name__ == '__main__':
    main()
