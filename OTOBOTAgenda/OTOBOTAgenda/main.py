from db_util import *
from string_matching import *
import re as regex

global flag_deadline
global flag_antara
global flag_hari_ini
global flag_hari
global flag_minggu
global flag_mata_kuliah
global flag_undur
global flag_selesai
global flag_tambah_task

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

    words = regex.split("\s", string)
    
    for each_word in words:
        if(each_word.capitalize() == "Deadline"):
            flag_deadline = True

    flag_antara = regex.findall(DATE_REGEX, string)
    if(len(flag_antara) == 2):
        flag_antara = True
    else:
        flag_antara = False

    flag_hari_ini = regex.findall("[Hh][Aa][Rr][Ii] [Ii][Nn][Ii]", string)
    if(flag_hari_ini == []):
        flag_hari_ini = False
    else:
        flag_hari_ini = True

    if(not flag_hari_ini):
        flag_hari = regex.findall("[Hh][Aa][Rr][Ii]", string)
        if(flag_hari == []):
            flag_hari = False
        else:
            flag_hari = True

    flag_minggu = regex.findall("[Mm][Ii][Nn][Gg][Gg][Uu]", string)
    if(flag_minggu == []):
        flag_minggu = False
    else:
        flag_minggu = True

    flag_mata_kuliah = regex.findall(COURSE_REGEX, string)
    if(flag_mata_kuliah == []):
        flag_mata_kuliah = False
    else:
        flag_mata_kuliah = True

    # flag_undur
    # flag_selesai

    flag_tambah_task = Task.convert(string)
    if(flag_tambah_task == None):
        flag_tambah_task = False
    else:
        flag_tambah_task = True

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

    user_chat = input()
    add_new_chat(user_chat)
    process_string(user_chat)

    print(flag_tambah_task)
    print(get_all_task())

    # tambah task baru
    if(flag_tambah_task):
        t = Task.convert(user_chat)
        add_new_task(t)

    # tampilkan deadline antara 2 tanggal
    elif(flag_deadline and flag_antara):
        dates = regex.findall(DATE_REGEX, user_chat)
        if(dates[0] < dates[1]):
            date1 = dates[0]
            date2 = dates[1]
        else:
            date1 = dates[1]
            date2 = dates[0]

        kata = None
        for words in regex.split("\s", user_chat):
            if(words in KATA_PENTING):
                kata = words
                break
        tasks = get_task_between_date(date1, date2, include_completed=False, kata_penting=kata)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline N minggu ke depan
    elif(flag_deadline and flag_minggu):
        kata = None
        words = regex.split("\s", user_chat)
        # cari kata penting
        for word in words:
            if(word in KATA_PENTING):
                kata = word
                break
        # cari jumlah hari
        for i in range(len(words)):
            if(words[i + 1].capitalize() == 'Minggu'):
                tasks = get_task_nextNWeeks(int(words[i]), include_completed=False, kata_penting=kata)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline N hari ke depan
    elif(flag_deadline and flag_hari):
        kata = None
        words = regex.split("\s", user_chat)
        # cari kata penting
        for word in words:
            if(word in KATA_PENTING):
                kata = word
                break
        # cari jumlah hari
        for i in range(len(words)):
            if(words[i + 1].capitalize() == 'Hari'):
                tasks = get_task_nextNDays(int(words[i]), include_completed=False, kata_penting=kata)
        ''' tampilkan tasks di sini '''

    # tampilkan deadline hari ini
    elif(flag_deadline and flag_hari_ini):
        tasks = get_task_thisday(include_completed=True, kata_penting=None)
        ''' tampilkan tasks di sini '''

    # tampilkan semua deadline
    elif(flag_deadline):
        tasks = get_all_task(include_completed=False)
        # tampilkan tasks di sini

