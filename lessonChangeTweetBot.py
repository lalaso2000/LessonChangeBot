"""5Eの授業変更をチェックし、つぶやく
"""

import tweepy
import lessonData


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
    update = lessonData.updateCheck(
        url='https://www.dropbox.com/s/p6hlhjp5f5v3y50/keijiyou.pdf?dl=1',
        file_path='test.pdf')
    print('update:{}'.format(update))
    if update:
        cd = lessonData.get_data(
            False, pdf_path='test.pdf', csv_path='test.csv')
    else:
        cd = lessonData.get_data(True)
    print(cd)

    # 4Eの授業変更を取り出す
    data_3e = lessonData.search_for_class(cd, grade=3, department='E')
    print(data_3e)

    # 3Eの2/22の授業変更を検索
    data_3e_2_22 = lessonData.search_for_date(data_3e, date='2018/2/22')
    print(data_3e_2_22)

    # メッセージを作る
    msg = lessonData.create_tweet(data_3e_2_22.iloc[0])
    print(msg)

    # twitterのbotを呼び出す
    tbot = TweetBot()
    tbot.api.update_status(status=msg)
    print('tweet')


if __name__ == '__main__':
    main()
