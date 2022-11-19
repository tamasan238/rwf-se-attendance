# -*- coding: utf-8 -*-

# このプログラムを動かすためには，pandas(numpyも一緒に入ります), 
# openpyxl をpipでインストールしておく必要があります．コマンド例は以下の通り．
# pip install pandas openpyxl

import sys          # for read command line arguments
import numpy as np  # for load CSV
import pandas as pd # for export xlsx

log_file_name = ""
file_name = ""
try:
    log_file_name = sys.argv[1]
    file_name = log_file_name.split(".")[0] + "-" + log_file_name.split(".")[1]
    file_name = "export_xlsx/" + file_name.split("/")[1].replace("-", "_").replace(":", "-")
except IndexError:
    print("ログファイル名をコマンドライン引数として渡してください．")
    exit()

f = open(log_file_name, "r")
csv = np.loadtxt("se-meibo.csv", delimiter=",", 
        usecols=(0,1,2,3,4,5,6,7), dtype="U16")

output = list()

log=f.readline() #1行目を飛ばすための空打ち
while True:
    log = f.readline()
    if log == "":
        break
    log = log.split()
    try:
        where_is_you = np.where(csv == log[2])[0][0]
    except IndexError:
        output.append(["名簿データに存在しない値が入力されました"])

    user = csv[where_is_you]

    output.append([log[0], log[1], log[2], user[3], user[2], 
                    user[4], user[5], user[1], log[3]])
    
df = pd.DataFrame(output)
df.to_excel(file_name+'.xlsx', index = False, header = False)
