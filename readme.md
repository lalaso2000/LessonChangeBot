NIT-Gifu Lesson-Change-PDF Support Tool
====

岐阜高専における授業変更pdfの表を扱いやすくするためのpythonのモジュール群です。
例えばpdfをcsv形式に変換したり出来ます。


## できること
* pdfをcsvに変換
* 変更を毎日チェック
* つぶやく
* ~~電子黒板に掲示~~


## 使い方
### tweet bot
1. ラズパイか何かをサーバーにする
1. 毎日`checkAndTweet.py`を定期実行。明日授業変更があるならここでつぶやきます。
1. リツイートしたいタイミングで`retweet.py`を定期実行。次に`checkAndTweet.py`を実行するまでリツイートし続けます。


## Requirement
* [tabula-py](https://github.com/chezou/tabula-py) … pdfの表をpandasのデータ型に変換してくれる
    * Java
        * tabula-pyに必要
        * 7か8
* pandas


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[lalaso2000](https://github.com/lalaso2000)
