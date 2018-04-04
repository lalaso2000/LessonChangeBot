"""Line Notifyのクラス
"""

import requests
import time
from logging import getLogger
import os

# ロガー設定
logger = getLogger()


class LineNotify:
    """Line Notifyのクラス
    """

    def __init__(self):
        """初期化(トークン取得)

        Keyword Arguments:
            token_file_path {str} -- トークンを書いたテキストファイルの場所 (default: {'line_token.txt'})
        """

        # トークン取得
        self.tokens = []
        # 環境変数からトークンを探す
        # LINE Notifyのトークンは'L_'から始まる
        for k, v in os.environ.items():
            if k[0:2] == 'L_':
                self.tokens.append(v)

    def _single_post(self, token, msg):
        """シングルポスト

        Arguments:
            token {str} -- 送り先トークン
            msg {str} -- メッセージ本文

        Returns:
            str -- レスポンスのメッセージ(失敗時はNone)
        """

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
                logger.log(20, 'LINE Notify \n {}'.format(msg))
                return response
        logger.log(40, 'ポストに失敗しました。')
        return None

    def multi_post(self, msgs):
        """複数メッセージポスト

        Arguments:
            msg {str[]} -- メッセージのリスト

        Returns:
            str[] -- 結果のリスト(失敗したものはNone)
        """

        results = []
        for m in msgs:
            for t in self.tokens:
                r = self._single_post(t, m)
                results.append(r)
        return results


def main():
    """テスト用
    """
    ln = LineNotify()
    msgs = ['hello', 'world']
    ln.multi_post(msgs)


if __name__ == '__main__':
    main()
