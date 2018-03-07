"""授業変更の一覧のデータを扱うためのモジュール
"""

import tabula
import pandas as pd
import re
import datetime
import os


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
        if df.ix[i, 'date'] == u'月日':
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
    ptn = re.compile(u'([1-9]|10|11|12)月([1-3]?[0-9])日')
    text = list(df['date'])
    print(text)
    _ = list(map(lambda s: re.search(ptn, s), text))
    m_list = list(map(lambda m: int(m.group(1)), _))
    d_list = list(map(lambda m: int(m.group(2)), _))
    # pdfファイルの製作日時を取得(表に年が載ってない)
    _ = os.stat(input_path).st_mtime
    pdf_day = datetime.datetime.fromtimestamp(_)
    # 年度に変換(製作日時が1〜2月なら年-1)(3月は授業がないので次年度扱い)
    _ = pdf_day.year
    print(pdf_day)
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

    # 列の位置を調整
    df2 = df.ix[:, [
        'date', 'day', 'period', 'grade', 'department', 'before_subject',
        'before_teacher', 'after_subject', 'after_teacher', 'note'
    ]]

    # csv書き出し
    df2.to_csv(output_path, encoding='utf-8')


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
    print('===== element =====')
    # .ix[行, 列]で指定
    # 0番目のデータの日付を表示
    print(cd.ix[0, 'date'])
    # 曜日を表示
    print(cd.ix[0, 'day'])
    # 日付から曜日取得もできる(0が月〜6が日)
    print(cd.ix[0, 'date'].weekday())
    # 時限
    print(cd.ix[0, 'period'])
    # 学年
    print(cd.ix[0, 'grade'])
    # 学科
    print(cd.ix[0, 'department'])
    # 変更前教科
    print(cd.ix[0, 'before_subject'])
    # 変更前教師
    print(cd.ix[0, 'before_teacher'])
    # 変更後教科
    print(cd.ix[0, 'after_subject'])
    # 変更後教科
    print(cd.ix[0, 'after_teacher'])
    # 備考
    print(cd.ix[0, 'note'])

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
