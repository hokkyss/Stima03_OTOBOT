import sqlite3
import datetime
from sqlite3.dbapi2 import DataError
from string_matching import *

def get_db():
    # Melakukan koneksi ke database
    # Apabila gagal print pesan kesalahan
    try:
        db = sqlite3.connect('Otobot.db')
        return db
    except sqlite3.Error as er:
        print(er)

def create_tabel_task():
    # Membuat tabel task
    # Apabila gagal print pesan kesalahan
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""CREATE TABLE task(
            ID INTEGER PRIMARY KEY,
            Jenis TEXT NOT NULL,
            Mata_Kuliah TEXT NOT NULL,
            Tanggal DATE NOT NULL,
            Topik   TEXT NOT NULL,
            Selesai INT DEFAULT 0
        )""")
        db.commit()
        print("Sukses membuat tabel task")
    except sqlite3.Error as er:
        print(er)

def add_new_task(task):
    # Menambahkan task baru
    # Task adalah objek kelas task
    # Return pesan sukses /gagal
    task.matakuliah = str(task.mata_kuliah).upper()
    new_task = (task.jenis, task.mata_kuliah , str(task.tanggal), task.topik)
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO task(Jenis, Mata_Kuliah, Tanggal, Topik) VALUES (?, ?, ?, ?)", new_task)
        print("Berhasil menambahkan task (ID " + str(cursor.lastrowid) + ") "+ task.jenis + " " + task.mata_kuliah + " " + task.topik)
        db.commit()
        return("[TASK BERHASIL DICATAT]<br>(ID: "+ str(cursor.lastrowid) +") "+ str(task.tanggal)+" - "+ task.mata_kuliah +" - "+ task.jenis+" - "+ task.topik)
    except sqlite3.Error as er:
        print(er)
        return ("Gagal menambahkan task")

def get_all_task(include_completed = True):
    # Mendapatkan semua task
    db = get_db()
    cursor = db.cursor()
    try:
        if (include_completed):
            cursor.execute("SELECT * FROM task")
        else:
            cursor.execute("SELECT * FROM task WHERE Selesai = 0")
        print("Berhasil mendapatkan semua task ")
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []

def get_all_task_by_mata_kuliah(mata_kuliah,include_completed = True):
    # Mendapatkan semua task
    db = get_db()
    cursor = db.cursor()
    mata_kuliah = str(mata_kuliah).upper()
    sql = "SELECT * FROM task WHERE Mata_Kuliah = '" + mata_kuliah + "'"
    try:
        if (include_completed):
            sql = sql + " AND Selesai = 1"
        cursor.execute(sql)
        print("Berhasil mendapatkan semua task dengan mata kuliah " + str(mata_kuliah))
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []
    
    
def get_all_task_by_jenis_tugas(jenis_tugas,include_completed = True):
    # Mendapatkan semua task
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM task WHERE Jenis = '" + jenis_tugas + "'"
    try:
        if (include_completed):
            sql = sql + " AND Selesai = 1"
        cursor.execute(sql)
        print("Berhasil mendapatkan semua task dengan mata kuliah " + jenis_tugas)
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []


def get_task_between_date(date1, date2, include_completed = True, kata_penting = None):
    # Mendapatkan task diantara dua hari
    # date 1 dan date 2 harus valid formatnya, date haruslah bentuk string dari kelas date
    date1 = str(date1)
    date2 = str(date2)
    db = get_db()
    date_range = (date1, date2)
    cursor = db.cursor()
    try:
        sql = "SELECT * FROM task WHERE tanggal BETWEEN ? AND ?"
        if (not include_completed):
            sql = sql + " AND (Selesai = 0)"
        if (kata_penting != None):
            sql = sql + " AND (Jenis = '" + kata_penting + "')"
        cursor.execute(sql, date_range)
        print("Berhasil mendapatkan " + ("task" if kata_penting == None else kata_penting) + " " + ("belum selesai" if (not include_completed) else "") + " diantara tanggal " + str(date1) + " dan " + str(date2))
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []

def get_task_nextNDays(NDays, include_completed = True, kata_penting = None):
    # Mendapatkan task dalam "N" hari selanjutnya 
    currDate = datetime.date.today()
    nextNDate = currDate + datetime.timedelta(days=NDays)
    return get_task_between_date(currDate, nextNDate, include_completed, kata_penting)

def get_task_nextNWeeks(NWeeks, include_completed = True, kata_penting = None):
    # Mendapatkan task dalam "N" minggu selanjutnya 
    currDate = datetime.date.today()
    nextNDate = currDate + datetime.timedelta(weeks=NWeeks)
    return get_task_between_date(currDate, nextNDate, include_completed,kata_penting)

def get_task_thisday(include_completed = True,kata_penting = None):
    currDate = datetime.date.today()
    return get_task_between_date(currDate, currDate, include_completed, kata_penting)

def get_deadline(mata_kuliah, jenis_tugas = None):
    # mendapatkan semua deadline dari suatu tugas matkul tertentu
    db = get_db()
    cursor = db.cursor()
    mata_kuliah = str(mata_kuliah).upper()
    try:
        sql = "SELECT topik, tanggal FROM task WHERE Mata_Kuliah = '" + mata_kuliah + "'"
        if (jenis_tugas != None):
            sql = sql + " AND (Jenis = '" + jenis_tugas + "')"
        cursor.execute(sql)
        print("Berhasil mendapatkan list deadline untuk " + (jenis_tugas if (jenis_tugas != None) else "tugas") + " " + mata_kuliah)
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []

def update_deadline(ID,date):
    # Melakukan update deadline suatu task, return pesan sukses /pesan kesalahan
    date = str(date)
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * From task WHERE ID = " + str(ID))
        if (len(cursor.fetchall()) != 0):
            sql = "UPDATE task SET tanggal ='" + date + "' WHERE ID = " + str(ID)
            cursor.execute(sql)
            print("Sukses merubah deadline task " + str(ID) + " menjadi " + date)
            db.commit()
            return ("Sukses merubah deadline task " + str(ID) + " menjadi " + date)
        else:
            print("Task tidak dikenali")
            return ("Tidak ada task dengan id tersebut")
    except sqlite3.Error as er:
        print(er)
        return  ("Gagal mengupdate task")

def finish_task(ID):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * From task WHERE ID = " + str(ID))
        if (len(cursor.fetchall()) != 0):
            sql = "UPDATE task SET selesai = 1 WHERE ID = " + str(ID)
            cursor.execute(sql)
            print("Sukses menyelesaikan task " + str(ID))
            db.commit()
            return ("Sukses menyelesaikan task " + str(ID))
        else:
            print("Task tidak dikenali")
            return ("Tidak ada task dengan id tersebut")
    except sqlite3.Error as er:
        print(er)
        return ("Gagal menyelesaikan task")

def dell_all_task():
    # Menghapus semua task
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM task")
        db.commit()
        create_tabel_task()
        print("Berhasil menghapus semua task")
    except sqlite3.Error as er:
        print(er)

def create_tabel_chat():
    # Membuat tabel chat
    # Apabila gagal print pesan kesalahan
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""CREATE TABLE chat(
            Chat TEXT ,
            Bot INT DEFAULT 0
        )""")
        print("Sukses membuat tabel chat")
    except sqlite3.Error as er:
        print(er)

def add_new_chat(chat, Bot = 0):
    # Menambahkan chat baru
    # Task adalah objek kelas chat
    new_chat = [chat, Bot]
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO chat(Chat, Bot) VALUES(?, ?)", new_chat)
        # print("Berhasil menambahkan chat " + chat)
        db.commit()
    except sqlite3.Error as er:
        print(er)

def get_all_chat():
    # Mendapatkan semua chat
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM chat")
        print("Berhasil mendapatkan semua chat ")
        return cursor.fetchall()
    except sqlite3.Error as er:
        print(er)
        return []

def dell_all_chat():
    # Menghapus semua chat
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE chat")
        db.commit()
        create_tabel_chat()
        print("Berhasil menghapus semua chat ")
        return 1
    except sqlite3.Error as er:
        print(er)
        return -1

def task_deadline_completeChatbuilder(listOfTaskQuery):
    # Mereturn string dengan format /n diganti <br> untuk keperluan html
    # Format isi string disesuaikan dengan spek
    if(len(listOfTaskQuery)==0):
        return("Tidak ada")
    else:
        result = "[Berhasil semua Task]"
        for count, task in enumerate(listOfTaskQuery, start=1):
            dt = datetime.datetime.strptime(str(task[3]), '%Y-%m-%d').strftime('%d/%m/%Y')
            result = result + "<br>"+str(count) +".  (ID : "+ str(task[0]) +") " +dt+" - "+ task[2] +" - "+ task[1]+" - "+ task[4] + " - " + ("selesai" if task[5] == 1 else "belum selesai")
    return result

def task_deadline_chatbuilder(listOfTaskQuery):
    # Mereturn string dengan format /n diganti <br> untuk keperluan html
    # Format isi string disesuaikan dengan spek
    if(len(listOfTaskQuery)==0):
        return("Tidak ada")
    else:
        result = "[Berhasil mendapatkan daftar]"
        for count, task in enumerate(listOfTaskQuery, start=1):
            dt = datetime.datetime.strptime(str(task[3]), '%Y-%m-%d').strftime('%d/%m/%Y')
            result = result + "<br>"+str(count) +".  (ID : "+ str(task[0]) +") "+ dt+" - "+ task[2] +" - "+ task[1]+" - "+ task[4]
    return result

def task_deadline_Shortchatbuilder(listOfTaskQuery):
    # Mereturn string dengan format /n diganti <br> untuk keperluan html
    # Format isi string disesuaikan dengan spek
    if(len(listOfTaskQuery)==0):
        return("Tidak ada")
    else:
        result = "[Berhasil mendapatkan daftar]"
        for count, task in enumerate(listOfTaskQuery, start=1):
            result = result + "<br>"+str(count) +". " +str(task[1])+" - "+ task[0]
    return result
    
def main():
    # Isi main program
    # Init + hapus tabel
    db = get_db()
    db.cursor().execute("DROP TABLE IF EXISTS chat")
    db.cursor().execute("DROP TABLE IF EXISTS task")

    # Buat Tabel
    create_tabel_task()
    create_tabel_chat()

    # Tambah data
    task1 = Task("Tubes", "IF2110", "2021-04-15", "STRING MATCHING")
    task2 = Task("Tubes", "IF2110", "2021-04-28", "STRING MATCHING2")
    task3 = Task("Tubes", "IF2110", "2021-05-28", "STRING MATCHING3")
    add_new_task(task1)
    add_new_task(task2)
    add_new_task(task3)
    chat = "Halo Bot"
    add_new_chat(chat)

    # Get data
    # all
    all_task = get_all_task()
    print(all_task)

    # between
    between = get_task_between_date("2020-08-18", "2022-12-20")
    print(between)

    # Next NDay
    nextNDay = get_task_nextNDays(NDays=4, kata_penting="Kuis", include_completed=False)
    print(nextNDay)

    # Next Nweek
    nextNWeek = get_task_nextNWeeks(NWeeks=8, include_completed=False)
    print(nextNWeek)

    # This day
    thisDay = get_task_thisday()
    print(thisDay)

    # get deadline
    deadline = get_deadline("IF2110", jenis_tugas="Tubes")
    print(deadline)

    # Update deadline
    res = update_deadline(5, "2020-10-10")
    print(res)

    # Finish task
    res = finish_task(1)
    print(res)
    
# Main Program
# main()

