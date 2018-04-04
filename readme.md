NIT-Gifu Lesson-Change Support Tool
====

岐阜高専における授業変更を扱いやすくするためのpythonのモジュール群です。
例えばpdfをcsv形式に変換したり、LINEやTwitterで通知したりできます。
あとオマケで年間行事予定も通知できます。(ゴリ押し)


## できること

* pdfをcsvに変換
* 変更を毎日チェック
* つぶやく
* クラスラインに通知
* ~~電子黒板に掲示~~
* 年間行事予定の通知


## 使い方

* 詳しい導入方法はwikiにて
* `check.py`を実行すると、授業変更のpdfの更新を確認し、csvに出力します。
* `tweet.py`、`line.py`を実行すると、それぞれの媒体で通知します。
* `tweet.py`を実行した後に`retweet.py`を実行すると`tweet.py`でつぶいたものをリツイートします。



## Requirement

* PythonとJavaの環境が必要です。
    * Python 3
    * Java 7 or 8
* Pythonでの必要なライブラリは主に次の通りです。(詳細は`requirements.txt`を確認してください。)
    * tabula-py
    * tweepy
    * dropbox
* サーバーはherokuを想定しています。


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[lalaso2000](https://github.com/lalaso2000)
