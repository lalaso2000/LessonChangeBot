"""授業変更をリツイートする
"""

import tweetBot
import csv
import logging.config


def main():
    # ロガー設定
    logging.config.fileConfig('logging.conf')

    # bot起動
    tbot = tweetBot.TweetBot()
    # リツイートするidリストを読み込む
    with open('ids.csv', 'r') as f:
        reader = csv.reader(f)
        _ = [e for e in reader]
        ids = _[0]
    print(ids)
    # リツートする
    for i in ids:
        tbot.retweet(i)
        # print(result)


if __name__ == '__main__':
    main()
