NIT-Gifu Lesson-Change-PDF Support Tool
====

岐阜高専における授業変更pdfの表を扱いやすくするためのpythonのモジュール群です。
例えばpdfをcsv形式に変換したり出来ます。


## できること
* pdfをcsvに変換
* 変更を毎日チェック
* つぶやく
* クラスラインに通知
* ~~電子黒板に掲示~~


## 使い方
1. ラズパイか何かをサーバーにする
1. 毎日`check.py`を定期実行。`tomorrow.csv`に明日の授業変更が書き込まれます。
1. ツイートするなら`tweet.py`を、ラインに送るなら`line.py`を実行。
1. リツイートしたいタイミングで`retweet.py`を定期実行。
    - Twitterを使う場合は[TwitterApps](https://apps.twitter.com/)から各種キーを発行し、次のようなテキストファイルを`tweetBot.py`と同じ場所においてください。
    
    [keys.txt]
    ```
    YOUR_API_KEY
    YOUR_API_SECRET
    YOUR_ACCESS_TOKEN
    YOUR_ACCESS_TOKEN_SECRET
    ```
    
    - LINE Notifyを使う場合は、[LINE Notify](https://notify-bot.line.me/ja/)からトークンを発行し、次のようなテキストファイルを`lineNotify.py`と同じ場所に置いてください。
    
    [line_token.txt]
    ```
    # #から始まる行はコメントアウト
    SOMEONE_TOKEN_1
    SOMEONE_TOKEN_2
    ...
    ```
    


## Requirement
* [tabula-py](https://github.com/chezou/tabula-py) … pdfの表をpandasのデータ型に変換してくれる
    * Java 7か8
        * tabula-pyに必要
* pandas
* tweepy


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[lalaso2000](https://github.com/lalaso2000)
