from db_util import *
from string_matching import *
import re as regex
from KMP_algorithm import *
from BM_algorithm import *

global flag_deadline
global flag_antara
global flag_hari_ini
global flag_hari
global flag_minggu
global flag_mata_kuliah
global flag_undur
global flag_selesai
global flag_tambah_task
global flag_tugas

def process_string(string):
    global flag_deadline
    global flag_antara
    global flag_hari_ini
    global flag_hari
    global flag_minggu
    global flag_mata_kuliah
    global flag_undur
    global flag_selesai
    global flag_tambah_task
    global flag_tugas

    # Flag deadline akan aktif apabila terdapat kata "deadline" di string
    if (kmpMatch(string,"Deadline",True) != -1):
        flag_deadline = True
    # words = regex.split("\s", string)
    # for each_word in words:
    #     if(each_word.capitalize() == "Deadline"):
    #         flag_deadline = True

    # flag antara akan aktif apabila terdapat dua date di string 
    all_date = Date.find_all_dates_in(string)
    if(len(all_date) == 2):
        flag_antara = True
    else:
        flag_antara = False

    # flag hari ini akan aktif apabila ada kata "hari ini"(not case sensitive) di string
    hari_ini = regex.findall("[Hh][Aa][Rr][Ii] [Ii][Nn][Ii]", string)
    if(hari_ini == []):
        flag_hari_ini = False
    else:
        flag_hari_ini = True
    
    if(not flag_hari_ini):
        # flag hari akan aktif apabila ada kata "hari"(not case sensitive) di string
        flag_hari = regex.findall("[Hh][Aa][Rr][Ii]", string)
        if(flag_hari == []):
            flag_hari = False
        else:
            flag_hari = True
    
    # flag minggu akan aktif apabila ada kata "minggu"(not case sensitive) di string
    minggu = regex.findall("[Mm][Ii][Nn][Gg][Gg][Uu]", string)
    if(minggu == []):
        flag_minggu = False
    else:
        flag_minggu = True

    # flag mata_kuliah akan aktif apabila ada mata kuliah di string
    mata_kuliah = regex.findall(COURSE_REGEX, string)
    if(mata_kuliah == []):
        flag_mata_kuliah = False
    else:
        flag_mata_kuliah = True

    # flag_undur
    # flag_selesai

    # flag task akan aktif apabila objek task bisa di generate dari string
    task = Task.convert(string)
    if(task == None):
        flag_tambah_task = False
    else:
        flag_tambah_task = True

    # Cek flag tugas
    if (len((kmpMatch_getAllMatchPattern(string,TUGAS,True)))) == 1:
        flag_tugas = True
    else :
        flag_tugas = False
    
        
while(True):
    flag_deadline = False
    flag_antara = False
    flag_hari_ini = False
    flag_hari = False
    flag_minggu = False
    flag_mata_kuliah = False
    flag_undur = False
    flag_selesai = False
    flag_tambah_task = False
    flag_tugas = False

    user_chat = input()
    add_new_chat(user_chat)
    process_string(user_chat)
    listOfFlag = [flag_deadline,flag_antara,flag_hari_ini,flag_hari,flag_minggu,flag_mata_kuliah,flag_undur,flag_selesai,flag_tambah_task,flag_tugas]
    numOfActiveFlag = listOfFlag.count(True)

    print(flag_deadline,flag_mata_kuliah,flag_tugas)
    if(user_chat=="showTask"):
        print(get_all_task())
    elif(user_chat=="resetTask"):
        dell_all_task()
    elif(user_chat=="resetChat"):
        dell_all_chat()
        
    # tambah task baru
    elif(flag_tambah_task):
        t = Task.convert(user_chat)
        add_new_task(t)

    # tampilkan deadline antara 2 tanggal
    elif(flag_deadline and flag_antara):
        dates = Date.find_all_dates_in(user_chat)
        if(dates[1].is_after(dates[0])):
            date1 = dates[0]
            date2 = dates[1]
        else:
            date1 = dates[1]
            date2 = dates[0]

        kata = None
        if (len(kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING))==1):
            kata = kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING)[0]
        
        # for words in regex.split("\s", user_chat):
        #     if(words in KATA_PENTING):
        #         kata = words
        #         break

        tasks = get_task_between_date(date1, date2, include_completed=False, kata_penting=kata)
        print(tasks)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline N minggu ke depan
    elif(flag_deadline and flag_minggu):
        kata = None
        # cari kata penting
        if (len(kmpMatch_getAllMatchPattern(KATA_PENTING,user_chat))==1):
            kata = kmpMatch_getAllMatchPattern(KATA_PENTING,user_chat)[0] 
        # cari jumlah hari
        words = regex.split("\s", user_chat)
        for i in range(len(words)-1):
            if(words[i + 1].capitalize() == 'Minggu'):
                tasks = get_task_nextNWeeks(int(words[i]), include_completed=False, kata_penting=kata)
                print(tasks)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline N hari ke depan
    elif(flag_deadline and flag_hari):
        kata = None
        # cari kata penting
        if (len(kmpMatch_getAllMatchPattern(KATA_PENTING,user_chat))==1):
            kata = kmpMatch_getAllMatchPattern(KATA_PENTING,user_chat)[0] 
        # cari jumlah hari
        words = regex.split("\s", user_chat)
        for i in range(len(words)-1):
            if(words[i + 1].capitalize() == 'Hari'):
                tasks = get_task_nextNDays(int(words[i]), include_completed=False, kata_penting=kata)
                print(tasks)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline hari ini
    elif(flag_deadline and flag_hari_ini):
        tasks = get_task_thisday(include_completed=True, kata_penting=None)
        print(tasks)
        ''' tampilkan tasks di sini '''

    # Tampilkan deadline suatu tugas
    elif(flag_deadline and flag_tugas and flag_mata_kuliah and numOfActiveFlag == 3):
        mata_kuliah = regex.findall(COURSE_REGEX,user_chat)[0]
        jenis_tugas = kmpMatch_getAllMatchPattern(user_chat,TUGAS,True)[0].capitalize()
        deadline = get_deadline(mata_kuliah,jenis_tugas)
        print(deadline)
        ''' tampilkan tasks di sini '''

    # tampilkan semua deadline
    elif(flag_deadline and numOfActiveFlag == 1):
        tasks = get_all_task(include_completed=False)
        print(tasks)
        # tampilkan tasks di sini
    else:
        print("Command Tidak dikenali")

