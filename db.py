"""dropboxのクラス
"""

import dropbox
import time
from logging import getLogger
import os

# ロガー設定
logger = getLogger()


class DB:
    """dropboxのクラス
    """

    def __init__(self):
        """認証
        """

        token = os.environ['DB_ACCESS_TOKEN']
        self.dbx = dropbox.Dropbox(token)
        self.dbx.users_get_current_account()

    def download(self, local_path, path):
        for i in range(1, 4):
            try:
                result = self.dbx.files_download_to_file(local_path, path)
            except Exception as e:
                logger.log(30,
                           'dropboxのダウンロードに失敗しました。リトライします。({}/3)'.format(i))
                time.sleep(i * 5)
            else:
                logger.log(20, 'dropboxからダウンロード\n{}'.format(result))
                return result
        logger.log(40, 'dropboxとの通信に失敗しました。')
        return None

    def upload(self, local_path, path, mode='overwrite'):
        for i in range(1, 4):
            try:
                f = open(local_path, 'rb')
                result = self.dbx.files_upload(f.read(), path,
                                               dropbox.files.WriteMode(mode))
                f.close()
            except Exception as e:
                logger.log(30,
                           'dropboxのアップロードに失敗しました。リトライします。({}/3)'.format(i))
                logger.log(30, e)
                time.sleep(i * 5)
            else:
                logger.log(20, 'dropboxへアップロード\n{}'.format(result))
                return result
        logger.log(40, 'dropboxとの通信に失敗しました。')
        return None


def main():
    db = DB()
    db.upload('./buf.csv', '/buf.csv')
    db.upload('./annual.csv', '/annual.csv')
    db.upload('./keijiyou.pdf', '/keijiyou.pdf')
    db.upload('./ids.csv', '/ids.csv')
    db.upload('./tomorrow.csv', '/tomorrow.csv')
    db.upload('./lessonChangeBot.log', '/lessonChangeBot.log')

    for entry in db.dbx.files_list_folder('').entries:
        print(entry.name)


if __name__ == '__main__':
    main()
