"""twitter botのクラス
"""

import tweepy
import time
from logging import getLogger
import os
import datetime

# ロガー設定
logger = getLogger()


class TweetBot:
    """botのためのクラス
    """

    def __init__(self):
        """キーの初期化等

        Arguments:
            key_file_path {string} -- キーが書かれたテキストファイルのパス
        """

        # キー設定
        CK = os.environ['TW_CONSUMER_KEY']
        CS = os.environ['TW_CONSUMER_SECRET']
        AT = os.environ['TW_ACCESS_TOKEN_KEY']
        AS = os.environ['TW_ACCESS_TOKEN_SECRET']

        # 認証
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)

        # APIインスタンス
        self.api = tweepy.API(auth)

    def tweet(self, msg):
        """渡されたメッセージをつぶやく

        Arguments:
            msg {str} -- つぶやく内容

        Returns:
            status -- ツイートの情報(失敗時はNone)
        """

        for i in range(1, 4):
            try:
                result = self.api.update_status(status=msg)
            except Exception as e:
                # print('ERROR : ツイートに失敗しました。リトライしています。({}/3)'.format(i))
                logger.log(30, 'ツイートに失敗しました。リトライします。({}/3)'.format(i))
                time.sleep(i * 5)
            else:
                logger.log(20, 'ツイート \n {}'.format(result.text))
                return result
        # print('ERROR : ツイートに失敗しました。このツイートは破棄されます。')
        logger.log(40, 'ツイートに失敗しました。このツイートは破棄されます。')
        return None

    def retweet(self, id):
        """リツイート(すでにしていた場合は一回取り消してもう一度リツイート)

        Arguments:
            id {str} -- リツイートしたいツイートのid

        Returns:
            status -- リツイートの情報(失敗時はNone)
        """

        # リツイートする
        for i in range(1, 4):
            try:
                # 自分がリツイートしてるかどうかチェック
                status = self.api.get_status(id, include_my_retweet=1)
                if status.retweeted is True:
                    # リツイートしてたら解除
                    self.api.destroy_status(status.current_user_retweet['id'])
                result = self.api.retweet(id)
            except Exception as e:
                # print('ERROR : リツイートに失敗しました。リトライしています。({}/3)'.format(i))
                logger.log(30, 'リツイートに失敗しました。リトライします。({}/3)'.format(i))
                time.sleep(i * 5)
            else:
                logger.log(20, 'リツイート \n {}'.format(result.text))
                return result
        # print('ERROR : リツイートに失敗しました。')
        logger.log(40, 'リツイートに失敗しました。')
        return None


def main():
    t = TweetBot()

    # テストツイート(乱打すると規制かかるので注意)
    msg = 'This is test.\n'
    msg += '{}'.format(datetime.datetime.now())

    t.api.update_status(msg)


if __name__ == '__main__':
    main()
