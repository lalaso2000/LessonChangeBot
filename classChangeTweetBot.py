"""5Eの授業変更をチェックし、つぶやく
"""

import tweepy
import updateChecker
import classData
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
    # 授業変更をチェックする
    update = updateChecker.updateCheck(
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

    # つぶやく本文を作る
    msg = '【'
    msg += '{0}{1}'.format(data_5e['grade'].values[0],
                           data_5e['department'].values[0])
    msg += '授業変更】\n'
    date = pd.to_datetime(data_5e['date'].values[0])
    msg += '{0:%m/%d}  '.format(date)
    msg += '{0}限'.format(int(data_5e['period'].values[0]))
    msg += '\n'
    msg += '{}'.format(data_5e['before_subject'].values[0])
    msg += '({})'.format(data_5e['before_teacher'].values[0])
    msg += '\n↓\n'
    msg += '{}'.format(data_5e['after_subject'].values[0])
    msg += '({})'.format(data_5e['after_teacher'].values[0])
    print(msg)
    # twitterのbotを呼び出す
    tbot = TweetBot()
    tbot.api.update_status(status=msg)


if __name__ == '__main__':
    main()
