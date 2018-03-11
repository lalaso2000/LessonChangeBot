"""授業変更を確認し、つぶやく
"""

import lessonData
import logging.config
import pandas as pd
import requests
import time

# ロガー設定
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def get_token(token_file_path='line_token.txt'):
    """トークンを取得

    Keyword Arguments:
        token_file_path {str} -- トークンが書かれたtxtファイル (default: {'line_token.txt'})

    Returns:
        list -- トークンの配列
    """

    tokens = []
    with open(token_file_path) as f:
        for line in f:
            line = line.rstrip('\r\n')
            tokens.append(line)
    return tokens


def post(token, msg):
    for i in range(1, 4):
        try:
            # ポスト
            headers = {
                'Authorization': 'Bearer {}'.format(token),
            }
            files = {
                'message': (None, msg),
            }
            response = requests.post(
                'https://notify-api.line.me/api/notify',
                headers=headers,
                files=files)
        except Exception as e:
            logger.log(30, 'ポストに失敗しました。リトライします。({}/3)'.format(i))
            time.sleep(i * 5)
        else:
            logger.log(20, 'response={}'.format(response))
            return response
    logger.log(40, 'ポストに失敗しました。')
    return None


def main():
    # 明日の授業変更を持ってくる
    data_5e_tomorrow = pd.read_csv('tomorrow.csv')

    # メッセージを作る
    msgs = []
    for index, d in data_5e_tomorrow.iterrows():
        msgs.append(lessonData.create_tweet(d))
    # print(msgs)

    # line Notifyにポスト
    tokens = get_token()
    for m in msgs:
        for t in tokens:
            post(t, m)


if __name__ == '__main__':
    main()
