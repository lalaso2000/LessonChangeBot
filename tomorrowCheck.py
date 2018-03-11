"""授業変更を確認する
"""

import lessonData
import datetime


def main():
    # 授業変更をチェックする
    update = lessonData.updateCheck(
        url='https://www.dropbox.com/s/p6hlhjp5f5v3y50/keijiyou.pdf?dl=1',
        file_path='test.pdf')
    if update:
        cd = lessonData.get_data(
            False, pdf_path='test.pdf', csv_path='test.csv')
    else:
        cd = lessonData.get_data(True)
    # print(cd)

    # 5Eの授業変更を取り出す
    data_5e = lessonData.search_for_class(cd, grade=5, department='E')
    # print(data_5e)

    # 明日の授業変更を探す
    # today = datetime.date.today()
    today = datetime.date(2018, 1, 28)  # デバック用
    td = datetime.timedelta(days=1)
    tomorrow = today + td
    # print(tomorrow)
    data_5e_tomorrow = lessonData.search_for_date(data_5e, tomorrow)
    print(data_5e_tomorrow)

    # csv出力しておく
    data_5e_tomorrow.to_csv('tomorrow.csv', encoding='utf-8')


if __name__ == '__main__':
    main()
