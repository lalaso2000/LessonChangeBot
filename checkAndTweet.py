"""授業変更を確認し、つぶやく
"""

import lessonData
import datetime
import tweetBot
import csv


def main():
    # 授業変更をチェックする
    # update = lessonData.updateCheck()
    update = lessonData.updateCheck(
        url='https://www.dropbox.com/s/p6hlhjp5f5v3y50/keijiyou.pdf?dl=1',
        file_path='test.pdf')  # デバック用
    if update:
        # cd = lessonData.get_data(False)
        cd = lessonData.get_data(
            False, pdf_path='test.pdf', csv_path='test.csv')  # デバック用
    else:
        # cd = lessonData.get_data(True)
        cd = lessonData.get_data(True, csv_path='test.csv')  # デバック用
    # print(cd)

    # 5Eの授業変更を取り出す
    data_5e = lessonData.search_for_class(cd, grade=5, department='E')
    # print(data_5e)

    # 明日の授業変更を探す
    today = datetime.date.today()
    # today = datetime.date(2018, 3, 13)  # デバック用
    td = datetime.timedelta(days=1)
    tomorrow = today + td
    # print(tomorrow)
    data_5e_tomorrow = lessonData.search_for_date(data_5e, tomorrow)
    print(data_5e_tomorrow)

    # メッセージを作る
    msgs = []
    for index, d in data_5e_tomorrow.iterrows():
        print(d)
        msgs.append(lessonData.create_tweet(d))
    print(msgs)

    # twitterのbotを呼び出す
    tbot = tweetBot.TweetBot()
    ids = []
    # つぶやく
    for m in msgs:
        result = tbot.tweet(m)
        if result is not None:
            # つぶやけたらidを記憶する。
            ids.append(result.id)
    # idをcsvに保存
    print(ids)
    with open('ids.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(ids)


if __name__ == '__main__':
    main()
