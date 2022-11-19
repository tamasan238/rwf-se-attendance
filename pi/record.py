# -*- coding: utf-8 -*-
 
from __future__ import print_function
from time import sleep
from ctypes import *
import numpy as np # for CSV
import datetime

# libpafe.hの77行目で定義
FELICA_POLLING_ANY = 0xffff

old_data=""

libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")
libpafe.pasori_open.restype = c_void_p
pasori = libpafe.pasori_open()
libpafe.pasori_init(pasori)
libpafe.felica_polling.restype = c_void_p

print("\n\n  Radio Wave Festival\n\n      Attendance Check System\n\n")

init_date = datetime.datetime.now().isoformat()
f = open("log/"+init_date+".txt", "a")
f.write("# "+init_date+"\n")
f.close()

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
            csv = np.loadtxt("se-meibo.csv", delimiter=",", 
                    usecols=(0,1,2,3,4,5,6,7), dtype="U16")
            dt_now = datetime.datetime.now()
            data = dt_now.strftime("%m/%d %H:%M:%S")
            try:
                where_is_you = np.where(csv == idm_No)[0][0]
            except IndexError:
                print("\n  Error: 名簿データに存在しません\n")

                f = open("log/"+init_date+".txt", "a")
                f.write(data+" UnRegisteredUser "+idm_No+"\n")
                f.close()
            else:
                temp = csv[where_is_you]
                print("\n"+data+" "+temp[1]+"班 "+temp[5]+"さんの参加を記録しました\n")

                f = open("log/"+init_date+".txt", "a")
                f.write(data+" "+temp[0]+" "+temp[7]+"\n")
                f.close()

                old_data=idm_No
        sleep(1)

except KeyboardInterrupt:
    print('finished')
    libpafe.free(felica)
    libpafe.pasori_close(pasori)
