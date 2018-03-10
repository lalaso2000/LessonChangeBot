"""5Eの授業変更をチェックし、つぶやく
"""

import tweepy
import classData


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
    # 授業変更をチェックする
    update = classData.updateCheck(
        url='https://www.dropbox.com/s/p6hlhjp5f5v3y50/keijiyou.pdf?dl=1',
        file_path='test.pdf')
    if update:
        cd = classData.get_data(
            False, pdf_path='test.pdf', csv_path='test.csv')
    else:
        cd = classData.get_data(True)

    # 5Eの授業変更を取り出す
    data_5e = cd[(cd['grade'] == 5)
                 & (cd['department'].map(lambda s: s[0]) == 'E')]
    print(data_5e)

    # メッセージを作る
    msg = classData.create_tweet(data_5e.iloc[2])

    # twitterのbotを呼び出す
    tbot = TweetBot()
    tbot.api.update_status(status=msg)


if __name__ == '__main__':
    main()
