"""授業変更pdfが更新されたかをチェックするためのモジュール
"""

import urllib.request
import filecmp
import os


def updateCheck(url='http://www.gifu-nct.ac.jp/gakka/keijiyou/keijiyou.pdf',
                file_path='keijiyou.pdf'):
    """ファイルの更新があったかをチェック

    Keyword Arguments:
        url {str} -- 授業変更pdfのURL (default: {'http://www.gifu-nct.ac.jp/gakka/keijiyou/keijiyou.pdf'})
        file_path {str} -- ダウンロードしたpdfのパス(名前) (default: {'keijiyou.pdf'})

    Returns:
        bool -- 更新があったかどうか(あればTrue)
    """

    # まず落とす
    n_file_path = 'new.pdf'
    urllib.request.urlretrieve(url, n_file_path)
    # 前のやつがない
    if not os.path.exists(file_path):
        os.rename(n_file_path, file_path)
        return True
    # 前のやつと中身を比較
    if not filecmp.cmp(file_path, n_file_path):
        # 違う＝更新された
        # 古いのを消して、新しいのをリネーム
        os.remove(file_path)
        os.rename(n_file_path, file_path)
        return True
    else:
        # ダウンロードしたのを消す
        os.remove(n_file_path)
        return False


def main():
    """テスト用メイン関数
    """

    # 更新チェック
    print(updateCheck(file_path='test.pdf'))


if __name__ == '__main__':
    main()
