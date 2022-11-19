@echo off
echo;
echo データの取得先正しいものであるかを確認します．
echo --
echo ECDSA key fingerprint is SHA256:(removed for publication). 
echo --
echo 以下に，上記と同じメッセージが表示されていれば， yes と入力してEnterを押してください．
echo 本プログラムは，初回に1度だけ実行すればあとは起動する必要はありません．
echo;
echo;
ssh -p (removed) -i id_ecdsa (removed)@(removed) -t exit