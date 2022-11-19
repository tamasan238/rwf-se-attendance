# rwf-se-attendance

Felicaリーダーを用いた非接触式活動者記録システム．   
日々の登録を行う Raspberry Pi 1台で動きますが，いつでもデータをダウンロードできるようにするためには24時間365日稼働のサーバが必要です．

## 注記

本システムは2021年度電波祭の開催にあたり，陽性者との接触確認のために設計・構築・運用されたものです．

公開用にプログラムの各所を改変しております．
そのままでは動作しませんので，ご了承ください．

# 動作概要

本システムは，以下の構成で動きます．

## Raspberry Pi 3B+
カード情報の登録，記録，ログデータのサーバへの転送を担う端末です．  
Felicaリーダ(SC-S320)，HDMIモニタ・マウスの接続が必須です．  
knct:publicが入らない環境では，別途インターネットへの接続設定のためキーボードを接続してください．  

本機の役割は，

1. 名簿データへの各カードのIDm情報の記録([pi/registration.py](pi/registration.py))
2. 日常的な活動記録，ログの出力([pi/record.py](pi/record.py))
3. Linuxサーバに定期的に rsync することでログを転送，名簿のバックアップをとる．

です．

起動 → knct:publicのログイン画面提示 → 待機 → 学内NTPサーバによる時刻同期 → record.py の起動 が自動で行われるようにしています．([pi/daily.sh](pi/daily.sh))

## Linuxサーバ
基本的に常時起動していれば，何の端末でも問題ありません．   
2021-07現在では，スタジオのMacPro(mid 2010)にUbuntu 20.04LTSを入れて使用しています．  
ただ，教員にはここから scp してもらうため，固定プライベートIPアドレスが割り当てられている必要があります．  

本機の役割は，

1. Raspberry Piから送られてきたログデータを蓄積し
2. 名簿データと突き合わせて読みやすいExcelデータに変換 ([server/convert.py](server/convert.py), [server/auto_convert.sh](server/auto_convert.sh))
3. 学内ネットからscpで取り出せるようにする (sshd)

です．

## データ取得用WindowsPC
各教員のPCです．  
学内ネットワークに接続していれば(上記LinuxサーバにSSHできれば)どのPCでも(複数あっても)よいです．  

こいつの役割は，

1. 初回接続時のFingerprintチェックを行い ([teacher/setupForOnlyOneTime.bat](teacher/getExcelData.bat))
2. scpによりデータを手元に持ってくる ([teacher/getExcelData.bat](teacher/getExcelData.bat))

です．

認証用に，ECDSA-521bitの秘密鍵 ([teacher/id_ecdsa](teacher/id_ecdsa)) を同梱しています．

# インストール

## Raspberry Pi 3B+
TBA

## Linuxサーバ
TBA

## データ取得用WindowsPC
以下に記載しています．(rwf-se@g.のマイドライブ内にあります．)  
[活動状況自動記録システム - データ記録マニュアル](https://docs.google.com/document/d/1uaFswARNEpSZ9VL0kqNYm7CbMXfOL_SBTvSo54YUP3A/edit?usp=sharing)

簡潔に示すと，以下の通りです．
1. [setupForOnlyOneTime.bat](teacher/getExcelData.bat)を実行
2. [getExcelData.bat](teacher/getExcelData.bat)を実行し，動作確認

# 日常的な使い方

## Raspberry Pi 3B+

### カードの登録
1. Raspberry Piに以下のものを接続します．
    - マウス
    - felicaリーダ(SONY SC-S320)
    - HDMIモニタ
    - MicroUSBケーブル(5V2.5A以上がとれる電源)
    - キーボード
2. 電源を接続すると自動で起動し，ブラウザでknct:publicの認証画面を表示しようとします．  
が，認証する必要がないので閉じます．(ログインしても問題はありません．)  
3. そして，30秒以内に `Please wait ...` と書かれたターミナルの画面も閉じてください．
4. 改めてターミナルを開き，以下のコマンドを入力してください．  
なお， `python3 se-attendance/registration.py` としたくなりますが，プログラム内で使用するファイルのパスを相対参照で指定しているためエラーとなります．  
必ず以下の方法に則って実行してください．
    ```
    cd se-attendance
    python3 registration.py
    ```
    
5. カード情報登録プログラムが起動します．  
プログラムの指示に従って登録してください．

### 活動状況の記録
#### knct:publicが拾える会場の場合
1. Raspberry Piに以下のものを接続します．
    - マウス
    - felicaリーダ(SONY SC-S320)
    - HDMIモニタ
    - MicroUSBケーブル(5V2.5A以上がとれる電源)
2. 電源を接続すると自動で起動し，ブラウザでknct:publicの認証画面が表示されます．  
ログインが完了したら，ブラウザを閉じてください．
3. 時刻同期のための待機，時刻同期，記録プログラムの起動が自動で進みます．  
あとは放置で問題ありません．

#### knct:publicが拾えない会場の場合
1. Raspberry Piに以下のものを接続します．
    - マウス
    - felicaリーダ(SONY SC-S320)
    - HDMIモニタ
    - MicroUSBケーブル(5V2.5A以上がとれる電源)
    - キーボード
2. 電源を接続すると自動で起動し，ブラウザでknct:publicの認証画面を表示しようとします．  
が，表示できないので閉じます．  
3. そして，30秒以内に `Please wait ...` と書かれたターミナルの画面も閉じてください．
4. 改めてターミナルを開き，以下のようなコマンドを入力してください．  
ダブルクオーテーションの中身は，コマンド投入時の日時にするのを忘れないでね．

    ```
    sudo date -s "07/30 13:00 2021"
    cd se-attendance
    python3 record.py
    ```

5. 記録プログラムが自動で起動します．  
あとは放置で問題ありません．

### 手動での活動記録の作成/追記/編集
1. Raspberry Piに以下のものを接続します．
    - マウス
    - felicaリーダ(SONY SC-S320)
    - HDMIモニタ
    - MicroUSBケーブル(5V2.5A以上がとれる電源)
    - キーボード
2. 電源を接続すると自動で起動し，ブラウザでknct:publicの認証画面を表示しようとします．  
が，認証する必要がないので閉じます．(ログインしても問題はありません．)  
3. そして，30秒以内に `Please wait ...` と書かれたターミナルの画面も閉じてください．
4. 改めてターミナルを開き，以下のコマンドを入力してください．  
    ```
    cd se-attendance/log
    ```
5.  `ls` すると，活動ログが並んでいます． `vi` などで編集/作成されてください．  
細かい表記は，過去のログを `cat` して確認してください．  
その際，ファイル名の日付，時刻は活動時のものを入力し，細かい桁の部分は0で構いません．  
ログ内の表記について，時刻は先頭の記録とすべて同一で構いません．  
ただし，カードのIDm(16桁の英数字)の部分は，0を16桁入力するようにお願いします．

## Linuxサーバ
何もする必要はありません．停電などでシャットダウンしていたら，起こしてあげてください．  
起動後，自動で処理を再開します．

## データ取得用WindowsPC
以下に記載しています．(rwf-se@g.のマイドライブ内にあります．)  
[活動状況自動記録システム - データ記録マニュアル](https://docs.google.com/document/d/1uaFswARNEpSZ9VL0kqNYm7CbMXfOL_SBTvSo54YUP3A/edit?usp=sharing)

簡潔に示すと，以下の通りです．
1. [getExcelData.bat](teacher/getExcelData.bat)を実行

# 作者
* 岩井 正輝
* 人間情報システム工学科 2017年度入学生
* 2021年度電波祭ステージイベント部門 感染症対策チーム技術主任
* メール : [hi17iwai@gmail.com](<mailto:hi17iwai@gmail.com>)
* Twitter : [@tamasan238](https://twitter.com/tamasan238)