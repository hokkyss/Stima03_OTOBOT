PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE task(
            ID INTEGER PRIMARY KEY,
            Jenis TEXT NOT NULL,
            Mata_Kuliah TEXT NOT NULL,
            Tanggal DATE NOT NULL,
            Topik   TEXT NOT NULL,
            Selesai INT DEFAULT 0
        );
INSERT INTO task VALUES(1,'Tucil','IF2021','2021-05-22','Regex ',0);
INSERT INTO task VALUES(2,'Tubes','IF2321','2021-05-21','Cosine Similarity  ',0);
INSERT INTO task VALUES(3,'Praktikum','IF2301','2021-05-21','Inheritance ',0);
CREATE TABLE chat(
            Chat TEXT ,
            Bot INT DEFAULT 0
        );
INSERT INTO chat VALUES('Tucil IF2021 Regex pada tanggal 22 Mei 2021',0);
INSERT INTO chat VALUES('[TASK BERHASIL DICATAT]<br>(ID: 1) 2021-05-22 - IF2021 - Tucil - Regex ',1);
INSERT INTO chat VALUES('Tubes IF2321 Cosine Similarity  pada tanggal 21 Mei 2021',0);
INSERT INTO chat VALUES('[TASK BERHASIL DICATAT]<br>(ID: 2) 2021-05-21 - IF2321 - Tubes - Cosine Similarity  ',1);
INSERT INTO chat VALUES('Praktikum IF2301 Inheritance pada tanggal 21 Mei 2021',0);
INSERT INTO chat VALUES('[TASK BERHASIL DICATAT]<br>(ID: 3) 2021-05-21 - IF2301 - Praktikum - Inheritance ',1);
INSERT INTO chat VALUES('deadline',0);
INSERT INTO chat VALUES('[Berhasil mendapatkan daftar]<br>1.  (ID : 1) 22/05/2021 - IF2021 - Tucil - Regex <br>2.  (ID : 2) 21/05/2021 - IF2321 - Tubes - Cosine Similarity  <br>3.  (ID : 3) 21/05/2021 - IF2301 - Praktikum - Inheritance ',1);
INSERT INTO chat VALUES('help',0);
INSERT INTO chat VALUES('Perintah tidak dikenal, gunakan --help untuk <br> melihat command yang bisa dilakukan',1);
INSERT INTO chat VALUES('--help',0);
INSERT INTO chat VALUES(replace('\n    \n    <b>Utility Command</b>(not case sensitive)<br>\n    <b>--help</b> : Menampilkan list of command dan penjelasan<br>\n    <b>--createTask</b> : Membuat tabel task (untuk emergency)<br>\n    <b>--createChat</b> : Membuat tabel chat (untuk emergency)<br>\n    <b>--resetChat</b> : Merefresh chat<br>\n    <b>--resetTask</b> : Merefresh seluruh task<br>\n    <b>--showAllTask</b> : Menampilkan semua task<br>\n    <br>\n    <b>KATA_PENTING</b> = kuis, ujian, tucil, tubes, praktikum, dan tugas<br>\n    <b>KODE_MATKUL</b> = Dua buah huruf (a-z|A-Z) diikuti 4 angka (0-9) contoh IF2100<br>\n    <b>TANGGAL</b> mengikuti format yang terdapat di contoh sebagai berikut\n        - 19-02-2021<br>\n        - 19-02-21<br>\n        - 19/02/2021<br>\n        - 19/02/21<br>\n        - 19 Februari 2021<br>\n        - 19 Feb 2021<br>\n        - 19 Februari 21<br>\n        - 19 Feb 21<br>\n    note: <br>\n    KATA_PENTING(N) berarti keyword KATA_PENTING sebanyak <b>N buah</b><br>\n    KATA_PENTING(opt) berarti keyword KATA_PENTING <b>opsional</b><br>\n    <br>\n    List of Command :<br>\n    A) Menambah Task<br> \n    <b>f: KATA_PENTING(1) + KODE_MATKUL(1) + TOPIK + TANGGAL</b><br>\n    <br>\n    B) Menampilkan Daftar Deadline<br>\n    1) Periode<br>\n       <b>f: "deadline" + TANGGAL(2)</b><br> \n    2) N hari ke depan<br>\n       <b>f: "deadline" + N "hari" (N muncul tepat sebelum "hari")</b><br>\n    3) N minggu ke depan<br>\n       <b>f: "deadline" + N "minggu" (N muncul tepat sebelum "minggu")</b><br>\n    4) Hari ini<br>\n       <b>f: "deadline" + "hari_ini"</b><br>\n    5) Jenis Task (Semua deadline)<br>\n       <b>f: "deadline" + KATA_TUGAS(1) (Hanya tucil, tubes, tugas)</b><br>\n       KATA_TUGAS(1) (Hanya kuis, ujian, praktikum)<br> \n    6) Point no (1-4) dapat dikombinasikan dengan point no (5)<br>\n       contoh <b>"deadline" + JENIS_TUGAS(1) + TANGGAL(2)</b><br>\n       Note : Perhatikan bahwa apabila jenis tugas yang dipilih<br>\n       termasuk kuis, ujian, praktikum maka kata "deadline"<br> \n       <b>harus dihilangkan</b><br>\n    7) Semua deadline<br>\n       <b>f: "deadline"</b><br>\n    <br>\n    C) Menampilkan Deadline Task matkul tertentu<br>\n       <b>f: "deadline" + JENIS_TUGAS(1)(opt) + KODE_MATKUL(1)</b><br>\n       JENIS_TUGAS yang diperbolehkan adalah tucil, tubes, dan tugas<br>\n    <br>\n    D) Update tanggal task<br>\n       KATA_UPDATE = undur, tunda, maju, ubah, ganti, dan update<br>\n       <b>f: KATA_UPDATE(1) + TANGGAL(1) + ID_TASK(1)</b><br>\n    <br>\n    E) Menyelesaikan task<br>\n       KATA_SELESAI = selesai,beres,tamat, dan kelar<br>\n       <b>f: KATA_SELESAI(1) + ID_TASK(1)</b><br>\n    ','\n',char(10)),1);
INSERT INTO chat VALUES('dedline semua tASK',0);
INSERT INTO chat VALUES('Mungkin maksud kamu:<br>deadline semua tASK',1);
INSERT INTO chat VALUES('dedline semua tASK',0);
INSERT INTO chat VALUES('Mungkin maksud kamu:<br>deadline semua tASK',1);
INSERT INTO chat VALUES('deadline semua tASK',0);
INSERT INTO chat VALUES('[Berhasil mendapatkan daftar]<br>1.  (ID : 1) 22/05/2021 - IF2021 - Tucil - Regex <br>2.  (ID : 2) 21/05/2021 - IF2321 - Tubes - Cosine Similarity  <br>3.  (ID : 3) 21/05/2021 - IF2301 - Praktikum - Inheritance ',1);
COMMIT;
