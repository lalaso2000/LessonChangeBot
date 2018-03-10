"""授業変更の一覧のデータを扱うためのモジュール
"""

import tabula
import pandas as pd
import re
import datetime
import os
import urllib.request
import filecmp


def _pdf_to_csv(input_path, output_path):
    """pdfからcsvを生成する

    Arguments:
        input_path {String} -- pdfファイルのパス
        output_path {Stirng} -- csvファイルのパス
    """

    # pdfからデータを読み込む
    df = tabula.read_pdf(input_path, pages='all')

    # データを整形
    df.columns = \
        ['date',
            'day',
            'period',
            'department_and_grade',
            'before_subject',
            'before_teacher',
            'after_subject',
            'after_teacher',
            'note']

    for i in range(0, len(df.index)):
        # 各ページの先頭の見出し行を削除
        if df.ix[i, 'date'] == '月日':
            df.drop(i, inplace=True)
            if i != 0:
                df.drop(i - 1, inplace=True)
            continue
    # 番号振り直し
    df.reset_index(drop=True, inplace=True)

    for i in range(0, len(df.index)):
        # 日付が無いデータを消去
        # 備考が2行以上になってると起こるっぽい？
        if pd.isnull(df.ix[i, 'date']):
            df.drop(i, inplace=True)
    # 番号振り直し
    df.reset_index(drop=True, inplace=True)

    # 学年と学科を分割
    grad_list = list(df['department_and_grade'].map(lambda x: x[-1]))
    dprt_list = list(df['department_and_grade'].map(lambda x: x[:-2]))
    df['grade'] = grad_list
    df['department'] = dprt_list
    df.drop('department_and_grade', axis=1, inplace=True)

    # 正規表現で月と日を抽出
    ptn = re.compile('([1-9]|10|11|12)月([1-3]?[0-9])日')
    text = list(df['date'])
    # print(text)
    _ = list(map(lambda s: re.search(ptn, s), text))
    m_list = list(map(lambda m: int(m.group(1)), _))
    d_list = list(map(lambda m: int(m.group(2)), _))
    # pdfファイルの製作日時を取得(表に年が載ってない)
    _ = os.stat(input_path).st_mtime
    pdf_day = datetime.datetime.fromtimestamp(_)
    # 年度に変換(製作日時が1〜2月なら年-1)(3月は授業がないので次年度扱い)
    _ = pdf_day.year
    # print(pdf_day)
    if pdf_day.month < 3:
        _ -= 1
    # 日付のリスト
    date_list = []
    for i in range(0, len(d_list)):
        # 1~3月は年度+1年
        if m_list[i] < 4:
            date = datetime.date(_ + 1, m_list[i], d_list[i])
        else:
            date = datetime.date(_, m_list[i], d_list[i])
        date_list.append(date)
    df.drop('date', axis=1, inplace=True)
    df['date'] = date_list

    # 曜日を数値に変換
    day_list = list(df['date'].map(lambda d: d.weekday()))
    # print(day_list)
    df.drop('day', axis=1, inplace=True)
    df['day'] = day_list

    # 時限を数値に変換
    # 小数第一位が0 -> フル授業
    #             1 -> 前半
    #             2 -> 後半
    period_list = list(df['period'].map(lambda p: __convert_period__(p)))
    # print(period_list)
    df.drop('period', axis=1, inplace=True)
    df['period'] = period_list

    # 列の位置を調整
    df2 = df.ix[:, [
        'date', 'day', 'period', 'grade', 'department', 'before_subject',
        'before_teacher', 'after_subject', 'after_teacher', 'note'
    ]]

    # csv書き出し
    df2.to_csv(output_path, encoding='utf-8')


def __convert_period__(period_string):
    """時限を数値に変換
       小数第一位が0 -> フル授業
                   1 -> 前半
                   2 -> 後半

    Arguments:
        period_string {String} -- 時限の文字列

    Returns:
        float -- 時限の数値
    """
    # 一応1-8まで対応
    p_str = period_string
    p_num = 0
    if p_str[:2] == 'IV':
        p_num += 4
        p_str = p_str[2:]
    for c in p_str:
        if c == 'I':
            p_num += 1
        elif c == 'V':
            p_num += 5
        elif c == 'a':
            p_num += 0.1
        elif c == 'b':
            p_num += 0.2
    return p_num


def get_data(buf, pdf_path='keijiyou.pdf', csv_path='buf.csv'):
    """ 授業変更データの取得
        buf=Trueならバッファファイル(csv)から
        buf=Falseならpdfから(重い)
        pandasのDataFrame形式で返却

    Arguments:
        buf {Boolean} -- バッファデータ(csv)を読むかどうか
    """

    # バッファ更新
    if buf is False:
        _pdf_to_csv(pdf_path, csv_path)

    # データ読み込み
    return pd.read_csv(csv_path, parse_dates=['date'])


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
    elif not filecmp.cmp(file_path, n_file_path):
        # 違う＝更新された
        # 古いのを消して、新しいのをリネーム
        os.remove(file_path)
        os.rename(n_file_path, file_path)
        return True
    else:
        # ダウンロードしたのを消す
        os.remove(n_file_path)
        return False


def create_tweet(data):
    """つぶやき本文の作成

    Arguments:
        data {dataFrame} -- つぶやき対象の授業変更データ

    Returns:
        string -- つぶやく文字列
    """

    # つぶやく本文を作る
    msg = '【'
    msg += '{0}{1}'.format(data['grade'], data['department'])
    msg += '授業変更】\n'
    date = pd.to_datetime(data['date'])
    msg += '{0:%m月%d日}  '.format(date)
    msg += '{0}限'.format(int(data['period']))
    msg += '\n'
    msg += '{}'.format(data['before_subject'])
    msg += '({})'.format(data['before_teacher'])
    msg += '\n↓\n'
    msg += '{}'.format(data['after_subject'])
    msg += '({})'.format(data['after_teacher'])
    # print(msg)
    return msg


def main():
    """テスト用関数
    """
    # バッファ(csv)からデータ取得
    # cd = get_data(True)

    # pdfからデータ取得(重い)
    # pdfが更新された時以外はバッファから読む
    cd = get_data(False)

    # とりあえず出力
    print('===== all data =====')
    print(cd)

    # 各要素の名前
    print('===== first element =====')
    # .ix[行, 列]で指定
    # 0番目のデータの日付を表示
    print('date = {}'.format(cd.ix[0, 'date']))
    # 曜日を表示(数値で保存されている)(0が月曜日...6が日曜日)
    print('day = {}'.format(cd.ix[0, 'day']))
    # わかりやすく表示する
    yobi_list = ['月', '火', '水', '木', '金', '土', '日']
    yobi = yobi_list[cd.ix[0, 'day']]
    print('曜日 = {}'.format(yobi))
    # 時限
    print('period = {}'.format(cd.ix[0, 'period']))
    # 学年
    print('grade = {}'.format(cd.ix[0, 'grade']))
    # 学科
    print('department = {}'.format(cd.ix[0, 'department']))
    # 変更前教科
    print('before_subject = {}'.format(cd.ix[0, 'before_subject']))
    # 変更前教師
    print('before_teacher = {}'.format(cd.ix[0, 'before_teacher']))
    # 変更後教科
    print('after_subject = {}'.format(cd.ix[0, 'after_subject']))
    # 変更後教科
    print('after_teacher = {}'.format(cd.ix[0, 'after_teacher']))
    # 備考
    print('note = {}'.format(cd.ix[0, 'note']))

    # 5Eの授業変更を抽出
    # E(J)とE(E)は別学科扱いなので
    # mapを使ってそれぞれの要素の一文字目を取り出し、
    # それがEかどうかをチェック
    print('===== 5E data =====')
    e5_data = cd[(cd.grade == 5) & (cd.department.map(lambda s: s[0]) == 'E')]
    print(e5_data)
    # レコード長はlenで取得
    print(len(e5_data.index))


if __name__ == '__main__':
    main()