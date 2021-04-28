# OTOBOT
## Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant Semester II Tahun 2020/2021

### *Tugas Besar I IF2211 Strategi Algoritma*

*Program Studi Teknik Informatika* <br />
*Sekolah Teknik Elektro dan Informatika* <br />
*Institut Teknologi Bandung* <br />

*Semester II Tahun 2020/2021*

## Author
1. Muhammad Azhar Faturahman	(13519020)
2. Reihan Andhika Putra 		(13519043)
3. Hokki Suwanda			(13519143)

## Algoritma KMP
Algoritma Knuth-Morris-Pratt atau yang biasa disebut sebagai KMP adalah sebuah algoritma yang digunakan untuk mencari sebuah pattern pada text dari kanan ke kiri, algoritma ini mirip dengan algorita brute force. Perbedaan antara algoritma ini dengan brute force adalah algoritma ini akan melakukan penggeseran terhadap pattern secara lebih pintar daripada secara brute force. 

## Algoritma Booyer-Moore
Algoritma Boyer-Moore algoritma pencocokan string yang didasari oleh dua teknik, yaitu teknik the looking glass dan teknik the character jump. Teknik the looking glass merupakan teknik pencocokan pattern pada string dimulai dari indeks terakhir pattern dan indeks pada string dimulai dari awal menyesuaikan dengan indeks pattern. Sedangkan teknik the character jump merupakan teknik melompat jika terjadi mismatch pada karakter pattern dan string. 

## Regex
Regular Expression (Regex) adalah sebuah notasi yang dapat digunakan untuk mendeskripsikan pola dari kata yang ingin dicari. Regular expression juga salah satu metode dalam pencarian data dalam string. Regular expression tidak seperti algoritma pencocokan string pada umumnya karena didalam regular expression terdapat dua tipe karakter yaitu literal character dan metacharacter. Literal character ialah karakter biasa yang benar-benar ada wujudnya misalnya seperti yang terdapat pada ASCII yang terdiri dari berbagai huruf, angka, hingga tanda baca. Metacharacter adalah karakter yang tidak memiliki wujud seperti literal character namun memiliki aturan yang bisa menunjukan apakah suatu string dapat diterima atau tidak. 

## Requirements
- [Python 3](https://www.python.org/downloads/)

## Link Deployment
[OTOBOT](https://otobotagenda.herokuapp.com/) <br />
Apabila terjadi error seperti gagal menambahkan task, ketik perintah berikut pada ChatBot
```
createTask
createChat
resetChat
resetTask
```

## Installation And Run
Clone the repository
```bash
git clone https://github.com/hokkyss/Stima03_OTOBOT.git
cd src
```
### Automatic Setup
#### First Time Setup
1. Open `setup.bat`
2. Wait until the installation is finished
3. The setup will automatically open the web browser
4. If the page failed to load, wait a moment then refresh the page

#### Run
1. Open `run.bat`
2. It will automatically open the web browser
3. If the page failed to load, wait a moment then refresh the page

#### Manual Setup
After cloning the repository
```bash 
cd src
python -m venv virt
virt\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open your web browser and go to [localhost:5000](http://localhost:5000)
