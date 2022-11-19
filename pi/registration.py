# -*- coding: utf-8 -*-
 
from __future__ import print_function
from time import sleep
from ctypes import *
import numpy as np # for CSV

# libpafe.hの77行目で定義
FELICA_POLLING_ANY = 0xffff
 
libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")
libpafe.pasori_open.restype = c_void_p
pasori = libpafe.pasori_open()
libpafe.pasori_init(pasori)
libpafe.felica_polling.restype = c_void_p

print("\n\n  Radio Wave Festival\n\n      Attendance Check System\n\n")
print(" ユーザーデータを登録します\n Felicaつきカード/デバイスが使用可能です\n")

old_data=""

try:
    while True:
        felica = libpafe.felica_polling(pasori, FELICA_POLLING_ANY, 0, 0)
        idm = c_ulonglong() 
        libpafe.felica_get_idm.restype = c_void_p
        libpafe.felica_get_idm(felica, byref(idm))
        idm_No = ("%016X" % idm.value)
        if idm_No == '0000000000000000' or idm_No == old_data:
            print('カードをタッチしてください')
        else:
            print("\n【読み取り成功】 カードを離してください")
            name = input("Input your ID(ex. hi17iwai): ")

            csv = np.loadtxt("se-meibo.csv", delimiter=",", 
                    usecols=(0,1,2,3,4,5,6,7), dtype="U16")
            try:
                where_is_you = np.where(csv == name)[0][0]
            except IndexError:
                print("\n  Error: 名簿データに存在しません\n")
            else:
                csv[where_is_you][7] = idm_No
                temp = csv[where_is_you]
                np.savetxt("se-meibo.csv", csv, delimiter=",", fmt="%s")
            
                print("\n"+temp[1]+"班 "+temp[3]+"科"+temp[2]+temp[4]+" "+
                        temp[5]+" さんの登録を受け付けました")
                print("    IDm: "+idm_No+"\n")
                if temp[6]!="":
                    print("    備考: "+temp[6]+"\n")

                old_data=idm_No
        sleep(1)

except KeyboardInterrupt:
    print('finished')
    libpafe.free(felica)
    libpafe.pasori_close(pasori)
