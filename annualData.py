"""年間行事予定を扱う
"""

import pandas as pd


def get_data(csv_path='annual.csv'):
    """年間行事予定のデータを取得

    Keyword Arguments:
        csv_path {str} -- 年間行事予定のcsvファイルのパス (default: {'annual.csv'})

    Returns:
        pandas.DataFrame -- 年間行事予定のデータ
    """

    return pd.read_csv(csv_path, delimiter=',', parse_dates=['date'])


def search_for_date(annual_datas, date):
    """日付で行事を取得

    Arguments:
        annual_datas {pandas.DataFrame} -- 年間行事予定のデータ

    Keyword Arguments:
        today {any} -- 検索する日付 (default: {datetime.date.today()})

    Returns:
        pandas.DataFrame -- 検索結果
    """

    df = annual_datas
    t = pd.to_datetime(date)
    return df.ix[df['date'] == t]


def create_tweet(data):
    msg = '【'
    msg += '行事予定'
    msg += '】\n'
    date = pd.to_datetime(data['date'])
    msg += '{0:%-m月%-d日}  '.format(date)
    if data['time'] == data['time']:
        # NanとNanを比較するとfalseが返ってくるのを利用してNanチェック
        msg += data['time']
    msg += '\n'
    msg += data['event']
    if data['class_change'] is True:
        msg += '\n'
        msg += '※授業変更あり'
    return msg


def main():
    """テスト用
    """
    # データ読み込み
    df = get_data()
    # 日付で検索
    t_data = search_for_date(df, '2018/4/6')
    print(t_data)
    # つぶやき作成＆チェック
    for index, row in t_data.iterrows():
        msg = create_tweet(row)
        print(msg)


if __name__ == '__main__':
    main()
