import re as regex
from db_util import *
from string_matching import *
from string_matching_algorithm import *

global flag_deadline
global flag_antara
global flag_hari_ini
global flag_hari
global flag_minggu
global flag_tugas
global flag_kata_penting
global flag_mata_kuliah
global flag_ubah
global flag_selesai
global flag_tambah_task
global flag_task_id
global flag_date

def process_string(string):
    global flag_deadline
    global flag_antara
    global flag_hari_ini
    global flag_hari
    global flag_minggu
    global flag_tugas
    global flag_kata_penting
    global flag_mata_kuliah
    global flag_ubah
    global flag_selesai
    global flag_tambah_task
    global flag_task_id
    global flag_date

    # Flag deadline akan aktif apabila terdapat kata "deadline" di string
    if (kmpMatch(string,"Deadline",True) != -1):
        flag_deadline = True

    # flag antara akan aktif apabila terdapat dua date di string 
    all_date = Date.find_all_dates_in(string)
    if(len(all_date) == 2):
        flag_antara = True

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

    # flag mata_kuliah akan aktif apabila ada satu mata kuliah di string 
    mata_kuliah = regex.findall(COURSE_REGEX, string)
    if(len(mata_kuliah) == 1):
        flag_mata_kuliah = True

    # flag_ubah
    ubah = regex.findall("[Uu]ndur|[Tt]unda|[Mm]aju|[Uu]bah|[Gg]anti|[Uu]pdate", string)
    if ubah == []:
        flag_ubah = False
    else:
        flag_ubah = True
        
    # flag_task_id
    task_id = regex.findall("[Tt]ask[\s]*\d+",string)    # Biar diproses kalau ada task id
    if task_id == []:
        flag_task_id = False
    else:
        flag_task_id = True
        
    # flag_date akan aktif apabila ada satu tanggal di string
    date = Date.find_all_dates_in(string) # Biar diproses kalau ada hari
    if (len(date) == 1):
        flag_date = True
    else:
        flag_date = False
    
    # flag_selesai
    selesai = regex.findall("[Ss]elesai|[Bb]eres|[Tt]amat|[Kk]elar",string)
    if selesai == []:
        flag_selesai = False
    else:
        flag_selesai = True
    
    # flag task akan aktif apabila objek task bisa di generate dari string
    task = Task.convert(string)
    if(task != None):
        flag_tambah_task = True
    
    # flag kata_penting akan aktif apabila ada kata penting di string
    if (len((kmpMatch_getAllMatchPattern(string,KATA_PENTING,True)))) == 1:
        flag_kata_penting = True
        # flag tugas akan aktif apabila ada kata penting berjenis tugas ada di string
        if (len((kmpMatch_getAllMatchPattern(string,TUGAS,True)))) == 1:
            flag_tugas = True
    

def process_user_chat(user_chat):
    global flag_deadline
    global flag_antara
    global flag_hari_ini
    global flag_hari
    global flag_minggu
    global flag_mata_kuliah
    global flag_ubah
    global flag_selesai
    global flag_tambah_task
    global flag_tugas
    global flag_kata_penting
    global flag_task_id
    global flag_date

    # Inisialisasi flag false
    flag_deadline = False
    flag_antara = False
    flag_hari_ini = False
    flag_hari = False
    flag_minggu = False
    flag_mata_kuliah = False
    flag_ubah = False
    flag_selesai = False
    flag_tambah_task = False
    flag_tugas = False
    flag_kata_penting = False
    flag_task_id = False
    flag_date = False

    process_string(user_chat)
    
    listOfFlag = [flag_deadline,flag_antara,flag_hari_ini,flag_hari,flag_minggu,flag_mata_kuliah,flag_ubah,flag_selesai,flag_tambah_task,flag_tugas, flag_task_id, flag_date]
    numOfActiveFlag = listOfFlag.count(True)

    # print(flag_deadline,flag_mata_kuliah,flag_tugas)
    if(user_chat=="--showAllTask"):
        print(get_all_task())
        return task_deadline_completeChatbuilder(get_all_task())
    elif(user_chat=="--resetTask"):
        dell_all_task()
        return "Berhasil mereset semua task"
    elif(user_chat=="--resetChat"):
        dell_all_chat()
        return ""

    # tambah task baru
    elif(flag_tambah_task):
        t = Task.convert(user_chat)
        botMsg = add_new_task(t)
        return botMsg

    # tampilkan deadline antara 2 tanggal
    elif(flag_antara):
        dates = Date.find_all_dates_in(user_chat)
        if(dates[1].is_after(dates[0])):
            date1 = dates[0]
            date2 = dates[1]
        else:
            date1 = dates[1]
            date2 = dates[0]
        kata = None
        if (flag_deadline):
            if (flag_kata_penting and not (flag_tugas)):
                return "Task yang bukan tugas tidak memiliki deadline"
            elif (flag_tugas):
                kata = kmpMatch_getAllMatchPattern(user_chat,TUGAS)[0]
            tasks = get_task_between_date(date1, date2, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        elif (flag_kata_penting):
            kata = kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING)[0]
            tasks = get_task_between_date(date1, date2, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        else:
            return ("Perintah tidak dikenal")

    # tampilkan deadline N minggu ke depan
    elif(flag_minggu):
        kata = None
        # cari jumlah hari
        Nweeks = None
        words = regex.split("\s", user_chat)
        for i in range(len(words)-1):
            if(words[i + 1].capitalize() == 'Minggu'):
                Nweeks = int(words[i])
                break
        if (Nweeks == None):
            return ("Perintah tidak dikenal")
        if(flag_deadline):
            # cari tugas
            if (flag_kata_penting and not (flag_tugas)):
                return "Task yang bukan tugas tidak memiliki deadline"
            if (flag_tugas):
                kata = kmpMatch_getAllMatchPattern(user_chat,TUGAS)[0]
            tasks = get_task_nextNWeeks(Nweeks, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        elif (flag_kata_penting):
            kata = kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING)[0]
            tasks = get_task_nextNWeeks(Nweeks, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        else:
            return ("Perintah tidak dikenal")
        
    # tampilkan deadline N hari ke depan
    elif(flag_hari):
        # cari jumlah hari
        Ndays = None
        words = regex.split("\s", user_chat)
        for i in range(len(words)-1):
            if(words[i + 1].capitalize() == 'Hari'):
                Ndays = int(words[i])
                break
        if (Ndays == None):
            return ("Perintah tidak diketahui")
        kata = None
        if(flag_deadline):
            # cari tugas
            if (flag_kata_penting and not (flag_tugas)):
                return "Task yang bukan tugas tidak memiliki deadline"
            if (flag_tugas):
                kata = kmpMatch_getAllMatchPattern(user_chat,TUGAS)[0]
            tasks = get_task_nextNDays(Ndays, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        elif (flag_kata_penting):
            kata = kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING)[0]
            tasks = get_task_nextNDays(Ndays, include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        else:
            return ("Perintah tidak dikenal")
        
    # tampilkan deadline hari ini
    elif(flag_hari_ini):
        kata = None
        if (flag_deadline):
            if (flag_kata_penting and not (flag_tugas)):
                return "Task yang bukan tugas tidak memiliki deadline"
            if (flag_tugas):
                kata = kmpMatch_getAllMatchPattern(user_chat,TUGAS)[0]
            tasks = get_task_thisday(include_completed=True, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        elif(flag_kata_penting):
            kata = kmpMatch_getAllMatchPattern(user_chat,KATA_PENTING)[0]
            tasks = get_task_thisday(include_completed=True, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        else :
            return ("Perintah tidak dikenal")

    # Tampilkan deadline suatu tugas
    elif(flag_deadline and flag_tugas and flag_mata_kuliah and numOfActiveFlag == 3):
        mata_kuliah = regex.findall(COURSE_REGEX,user_chat)[0]
        jenis_tugas = kmpMatch_getAllMatchPattern(user_chat,TUGAS,True)[0].capitalize()
        deadline = get_deadline(mata_kuliah,jenis_tugas)
        print(deadline)
        return task_deadline_Shortchatbuilder(deadline)

    # tampilkan semua deadline
    elif(flag_deadline and numOfActiveFlag == 1):
        tasks = get_all_task(include_completed=False)
        print(tasks)
        return (task_deadline_chatbuilder(tasks))
        
    elif(flag_ubah and flag_task_id and flag_date):
        dates = Date.find_all_dates_in(user_chat)
        date = dates[0] # Asumsikan selalu ambil date yang pertama muncul
        
        task = regex.findall("[Tt]ask[\s]*\d+",user_chat)    # Biar diproses kalau ada task id
        task_id = regex.findall("\d+",user_chat)[0]
        
        botMsg = update_deadline(task_id,date)   # Update database
        return botMsg
    
    elif (flag_selesai and flag_task_id):
        task = regex.findall("[Tt]ask[\s]*\d+",user_chat)    # Biar diproses kalau ada task id
        task_id = regex.findall("\d+",user_chat)[0]
        
        botMsg  = finish_task(task_id) # Update database
        return botMsg

    else:
        return ("Perintah tidak dikenal")
        
        
        
# MAIN PROGRAM
# while(True):
#     print("> ", end="")
#     user_chat = input()
#     res = process_user_chat(user_chat)
#     print(res)

    

