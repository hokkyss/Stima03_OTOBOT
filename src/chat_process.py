import re as regex
from util import *
from classes import *
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
global flag_one_date
global flag_invalid

def process_string(string):
    """Mengidentifikasi kata kunci yang ada pada string untuk diubah menjadi sebuah flag

    Args:
        string (String): Masukkan string yang akan diidentifikasi
    """
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
    global flag_one_date
    global flag_invalid

    # Flag deadline akan aktif apabila terdapat kata "deadline" di string
    if (kmpMatch(string, "Deadline", True) != -1):
        flag_deadline = True

    # flag antara akan aktif apabila terdapat dua date di string 
    all_date = Date.find_all_dates_in(string)
    if(len(all_date) == 2):
        flag_antara = True
    # flag_one_date akan aktif apabila ada satu tanggal di string
    elif (len(all_date) == 1):
        flag_one_date = True
    elif (len(all_date) >= 3):
        flag_invalid = True

    # flag hari ini akan aktif apabila ada kata "hari ini"(not case sensitive) di string
    hari_ini = regex.findall("[Hh]ari [Ii]ni", string)
    if(hari_ini == []):
        flag_hari_ini = False
    else:
        flag_hari_ini = True
    
    if(not flag_hari_ini):
        # flag hari akan aktif apabila ada kata "N hari"(not case sensitive) di string
        # flag_hari = regex.findall("[Hh][Aa][Rr][Ii]", string)
        flag_hari = regex.findall("\d+\s*[Hh]ari", string)
        if(flag_hari == []):
            flag_hari = False
        elif(len(flag_hari) == 1):
            flag_hari = True
        else:
            flag_invalid = True
    
    # flag minggu akan aktif apabila ada kata "N minggu"(not case sensitive) di string
    # minggu = regex.findall("[Mm][Ii][Nn][Gg][Gg][Uu]", string)
    minggu = regex.findall("\d+\s*[Mm]inggu", string)
    if(minggu == []):
        flag_minggu = False
    elif(len(minggu) == 1):
        flag_minggu = True
    else:
        flag_invalid = True

    # flag mata_kuliah akan aktif apabila ada satu mata kuliah di string 
    mata_kuliah = regex.findall(COURSE_REGEX, string)
    if(len(mata_kuliah) == 1):
        flag_mata_kuliah = True
    elif(len(mata_kuliah) > 1):
        flag_invalid = True

    # flag_ubah akan aktif jika ada kata kunci yang mengindikasikan perubahan deadline
    ubah = regex.findall("[Uu]ndur|[Tt]unda|[Mm]aju|[Uu]bah|[Gg]anti|[Uu]pdate", string)
    if ubah == []:
        flag_ubah = False
    else:
        flag_ubah = True
        
    # flag_task_id akan aktif jika ada "Task <ID>" pada string
    task_id = regex.findall("[Tt]ask[\s]*\d+", string)    # Biar diproses kalau ada task id
    if task_id == []:
        flag_task_id = False
    elif (len(task_id) == 1):
        flag_task_id = True
    else:
        flag_invalid = True
            
    # flag_selesai akan aktif apabila ada kata kunci yang mengindikasikan selesai mengerjakan
    selesai = regex.findall("[Ss]elesai|[Bb]eres|[Tt]amat|[Kk]elar", string)
    if selesai == []:
        flag_selesai = False
    else:
        flag_selesai = True
    
    # flag task akan aktif apabila objek task bisa di generate dari string
    flag_tambah_task = Task.convert(string)
    if(flag_tambah_task is None):
        flag_tambah_task = False
    else:
        flag_tambah_task = True
    
    # flag kata_penting akan aktif apabila ada kata penting di string
    if (len(kmpMatch_getAllMatchPattern(string, KATA_PENTING, True))) == 1:
        flag_kata_penting = True
        # flag tugas akan aktif apabila ada kata penting berjenis tugas ada di string
        if (len(kmpMatch_getAllMatchPattern(string, TUGAS, True))) == 1:
            flag_tugas = True
        elif (len(kmpMatch_getAllMatchPattern(string, TUGAS, True)) > 1):
            flag_invalid = True
    elif (len(kmpMatch_getAllMatchPattern(string, KATA_PENTING, True)) > 1):
        flag_invalid = True
    
    # waktu tidak kontradiksi
    if(flag_minggu and (flag_hari or flag_hari_ini or flag_antara)):
        flag_invalid = True
    if(flag_hari and (flag_hari_ini or flag_antara)):
        flag_invalid = True
    if(flag_hari_ini and flag_antara):
        flag_invalid = True

    # update dan selesaikan tidak fleksibel
    if(flag_ubah and flag_selesai):
        flag_invalid = True
    if((flag_ubah or flag_selesai) and (flag_antara or flag_hari_ini or flag_hari or flag_minggu)):
        flag_invalid = True
    if((flag_ubah or flag_selesai) and flag_tambah_task):
        flag_invalid = True
    if((flag_ubah or flag_selesai) and flag_kata_penting):
        flag_invalid = True
    if(flag_selesai and flag_one_date):
        flag_invalid = True

    # tambah task tidak fleksibel
    if(flag_tambah_task and (flag_antara or flag_hari_ini or flag_hari or flag_minggu or flag_ubah or flag_selesai or flag_task_id)):
        flag_invalid = True
    

def process_user_chat(user_chat):
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
    global flag_one_date
    global flag_invalid

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
    flag_one_date = False
    flag_invalid = False
    
    # Detektor typo
    kata_penting = [x.lower() for x in KATA_PENTING]
    nama_bulan = ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"]
    kata_keyword = ["deadline", "hari", "minggu", "task", "undur", "ganti", "update", "selesai", "kelar", "--showAllTask", "--resetTask","--resetChat","--help","--createTask","--createChat"]
    kamus_typo = kata_penting + kata_keyword + nama_bulan

    typo = typo_solver(user_chat, kamus_typo, True)
    if typo != "Tidak ada typo":
        return typo

    # Melakukan identifikasi flag
    process_string(user_chat)
    
    # Hitung berapa banyak flag yang aktif
    listOfFlag = [flag_deadline, flag_antara, flag_hari_ini,  flag_hari, flag_minggu, flag_mata_kuliah, flag_ubah, flag_selesai, flag_tambah_task, flag_tugas, flag_kata_penting, flag_task_id, flag_one_date]
    numOfActiveFlag = listOfFlag.count(True)

    if(flag_invalid):
        return "Perintah tidak dikenal, gunakan --help untuk <br> melihat command yang bisa dilakukan"

    # General command for application
    if(user_chat.lower() == "--showAllTask".lower()):
        print(get_all_task())
        return task_deadline_completeChatbuilder(get_all_task())
    elif(user_chat.lower() == "--resetTask".lower()):
        dell_all_task()
        return "Berhasil mereset semua task"
    elif(user_chat.lower() == "--resetChat".lower()):
        dell_all_chat()
        return ""
    elif (user_chat.lower() == "--createTask".lower()):
        create_tabel_task()
        return "tabel task berhasil dibuat"
    elif (user_chat.lower() == "--createChat".lower()):
        create_tabel_chat()
        return "tabel chat berhasil dibuat"
    elif (user_chat.lower() == "--help".lower()):
        return help_chatbuilder()

    # Menambah task baru
    elif(flag_tambah_task):
        t = Task.convert(user_chat)
        botMsg = add_new_task(t)
        return botMsg

    # Menampilkan deadline antara 2 tanggal
    elif(flag_antara):
        # Dapatkan hari yang ada pada user_chat
        dates = Date.find_all_dates_in(user_chat)
        if(dates[1].is_after(dates[0])):
            date1 = dates[0]
            date2 = dates[1]
        else:
            date1 = dates[1]
            date2 = dates[0]
        kata = None
        # Mengidentifikasi variasi dari jenis task
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
            # return ("Perintah tidak dikenal")
            return typo_solver(user_chat, kamus_typo)

    # Menampilkan deadline N minggu ke depan
    elif(flag_minggu):
        kata = None
        # Cari jumlah minggu
        N_minggu = regex.findall("\d+\s*[Mm]inggu", user_chat)
        Nweeks = int(regex.findall("\d+", " ".join(N_minggu))[0])
        # Mengidentifikasi variasi dari jenis task
        if(flag_deadline):
            # Cari tugas
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
            # return ("Perintah tidak dikenal")
            return typo_solver(user_chat,kamus_typo)
        
    # Menampilkan deadline N hari ke depan
    elif(flag_hari):
        kata = None
        # Cari jumlah hari
        N_hari = regex.findall("\d+\s*[Hh]ari", user_chat)
        Ndays = int(regex.findall("\d+", " ".join(N_hari))[0])
        # Mengidentifikasi variasi dari jenis task
        if(flag_deadline):
            # Cari tugas
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
            # return ("Perintah tidak dikenal")
            return typo_solver(user_chat,kamus_typo)
        
    # Menampilkan deadline hari ini
    elif(flag_hari_ini):
        kata = None
        if (flag_deadline):
            if (flag_kata_penting and not (flag_tugas)):
                return "Task yang bukan tugas tidak memiliki deadline"
            if (flag_tugas):
                kata = kmpMatch_getAllMatchPattern(user_chat,TUGAS)[0]
            tasks = get_task_thisday(include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        elif(flag_kata_penting):
            kata = kmpMatch_getAllMatchPattern(user_chat, KATA_PENTING)[0]
            tasks = get_task_thisday(include_completed=False, kata_penting=kata)
            print(tasks)
            return task_deadline_chatbuilder(tasks)
        else :
            # return ("Perintah tidak dikenal")
            return typo_solver(user_chat,kamus_typo)

    # Menampilkan semua deadline jenis tugas dari mata kuliah tertentu atau bisa juga deadline mata kuliah tanpa jenis tugas
    # Yang nyala flag_deadline, flag_tugas, flag_kata_penting dan flag_mata_kuliah
    elif(flag_deadline and flag_mata_kuliah):
        mata_kuliah = regex.findall(COURSE_REGEX, user_chat)[0]
        jenis_tugas = None
        if (flag_kata_penting):
            if (not flag_tugas):
                return "Task yang bukan tugas tidak mempunyai deadline"
            elif (flag_tugas and numOfActiveFlag == 4):
                jenis_tugas = kmpMatch_getAllMatchPattern(user_chat, TUGAS, True)[0].capitalize()
                deadline = get_deadline(mata_kuliah, jenis_tugas)
                print(deadline)
                return task_deadline_Shortchatbuilder(deadline)
            else :
                return typo_solver(user_chat, kamus_typo)
        elif (not(flag_kata_penting) and numOfActiveFlag==2):
            deadline = get_deadline(mata_kuliah, jenis_tugas)
            print(deadline)
            return task_deadline_Shortchatbuilder(deadline)
        else :
            return typo_solver(user_chat)

    
    # Menampilkan semua deadline dari suatu jenis tugas
    # Yang nyala flag_deadline, flag_tugas, flag_kata_penting
    elif(flag_deadline and flag_tugas and numOfActiveFlag == 3):
        jenis_tugas = kmpMatch_getAllMatchPattern(user_chat, TUGAS, True)[0].capitalize()
        task = get_all_task_by_jenis_tugas(jenis_tugas, False)
        print(task)
        return task_deadline_chatbuilder(task)
    
    # Menampilkan semua deadline
    elif(flag_deadline and numOfActiveFlag == 1):
        tasks = get_all_task(include_completed=False)
        print(tasks)
        return (task_deadline_chatbuilder(tasks))
    
    # Menangkap kesalahan command berupa deadline dari task yang bukan tugas
    elif(flag_kata_penting and flag_deadline and  numOfActiveFlag == 2):
        return "Task yang bukan tugas tidak memiliki deadline"
    
    # Menampilkan task dari suatu kata penting
    elif(flag_kata_penting and numOfActiveFlag == 1):
        jenis_tugas = kmpMatch_getAllMatchPattern(user_chat, KATA_PENTING, True)[0].capitalize()
        task = get_all_task_by_jenis_tugas(jenis_tugas, False)
        print(task)
        return task_deadline_chatbuilder(task)
    
    
    # Mengubah deadline suatu task
    elif(flag_ubah and flag_task_id and flag_one_date):
        dates = Date.find_all_dates_in(user_chat)
        date = dates[0]
        
        task = regex.findall("[Tt]ask[\s]*\d+", user_chat)    # Biar diproses kalau ada task id
        task_id = regex.findall("\d+", " ".join(task))[0]
        
        botMsg = update_deadline(task_id, date)   # Update database
        return botMsg
    
    # Menyelesaikan suatu task
    elif (flag_selesai and flag_task_id):
        task = regex.findall("[Tt]ask[\s]*\d+", user_chat)    # Biar diproses kalau ada task id
        task_id = regex.findall("\d+", " ".join(task))[0]
        
        botMsg  = finish_task(task_id) # Update database
        return botMsg

    else:
        print(listOfFlag)
        # return ("Perintah tidak dikenal")
        return typo_solver(user_chat, kamus_typo)
        
        
def typo_solver(user_chat, kamus, checker=False):
    """Melakukan pengubahan kata yang typo dengan Levenshtein distance
    Args:
        user_chat (String): chat yang dimasukkan user
        kamus (String): kamus kata yang akan diperiksa
        checker (Boolean): apakah suatu penjaga typo sebelum masuk check flag
    Returns:
        (String): chat yang sudah dibenerin typonya
    """
    
    # Ubah menjadi setiap kata
    user_words = regex.split("\s+", user_chat)
    found_typo = False
    for i in range(len(user_words)):
        for kata in kamus:
            if ((kata == "juni" and user_words[i].lower() == "juli") or (kata == "juli" and user_words[i].lower() == "juni")):
                continue
            ratio = levenshtein_ratio(user_words[i], kata)
            if (ratio > 0.725 and ratio < 1):
                user_words[i] = kata
                found_typo = True
    final_words = " ".join(user_words)
    
    if found_typo:
        return ("Mungkin maksud kamu:<br>" + final_words)
    else:
        if checker:
            return ("Tidak ada typo")
        else:
            return ("Perintah tidak dikenal, gunakan --help untuk <br> melihat command yang bisa dilakukan")
        
# MAIN PROGRAM
# while(True):
#     print("> ", end="")
#     user_chat = input()
#     res = process_user_chat(user_chat)
#     print(res)
