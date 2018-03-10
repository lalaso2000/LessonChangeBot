"""つぶやく
"""

import tweepy
import lessonData
import pandas as pd


class TweetBot:
    """botのためのクラス
    """

    def __init__(self, key_file_path='keys.txt'):
        """キーの初期化

        Arguments:
            key_file_path {string} -- キーが書かれたテキストファイルのパス
        """

        # 鍵は辞書形式で保存
        self.__KEY_DICT__ = {}
        DICT_KEYS = ['CK', 'CS', 'AT', 'AS']
        i = 0
        with open(key_file_path) as f:
            for line in f:
                line = line.rstrip('\r\n')
                self.__KEY_DICT__[DICT_KEYS[i]] = line
                i += 1

        # Twitterオブジェクトを保持
        auth = tweepy.OAuthHandler(self.__KEY_DICT__['CK'],
                                   self.__KEY_DICT__['CS'])
        auth.set_access_token(self.__KEY_DICT__['AT'], self.__KEY_DICT__['AS'])

        # APIインスタンス
        self.api = tweepy.API(auth)


def main():
    # 明日の授業変更を取得
    data = pd.read_csv('tomorrow.csv', parse_dates=['date'])

    # メッセージを作る
    msg = []
    for index, d in data.iterrows():
        print(d)
        msg.append(lessonData.create_tweet(d))
    print(msg)

    # twitterのbotを呼び出す
    tbot = TweetBot()
    for m in msg:
        tbot.api.update_status(status=m)
        print('tweet')


if __name__ == '__main__':
    main()
