from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from string_matching_algorithm import *
import re as regex
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# factory = StopWordRemoverFactory()
newStopFactory = StopWordRemoverFactory().get_stop_words()
newStopFactory.remove("sampai")
newStopFactory.append("tanggal")
stopword = StopWordRemover(ArrayDictionary(newStopFactory))

# Regex untuk bulan
JANUARI_REGEX ='Jan(?:uari)?'
FEBRUARI_REGEX ='Feb(?:ruari)?'
MARET_REGEX ='Mar(?:et)?'
APRIL_REGEX ='Apr(?:il)?'
MEI_REGEX ='Mei'
JUNI_REGEX ='Juni?'
JULI_REGEX ='Juli?'
AGUSTUS_REGEX ='Agu(?:stus)?'
SEPTEMBER_REGEX ='Sep(?:tember)?'
OKTOBER_REGEX ='Okt(?:ober)?'
NOVEMBER_REGEX ='Nov(?:ember)?'
DESEMBER_REGEX ='Des(?:ember)?'

# Regex untuk keutuhan tanggal
ANYTHING = '.*'
DAY_REGEX = '(0[1-9]|[1-2][0-9]|3[0-1])'
MONTH_REGEX = '(0[1-9]|1[0-2]|'+JANUARI_REGEX+'|'+FEBRUARI_REGEX+'|'+MARET_REGEX+'|'+APRIL_REGEX+'|'+MEI_REGEX+'|'+JUNI_REGEX+'|'+JULI_REGEX+'|'+AGUSTUS_REGEX+'|'+SEPTEMBER_REGEX+'|'+OKTOBER_REGEX+'|'+NOVEMBER_REGEX+'|'+DESEMBER_REGEX+')'
YEAR_REGEX = '([0-9]{4})'
DATE_DELIM = '([-/ ])'
DATE_REGEX = DAY_REGEX + DATE_DELIM + MONTH_REGEX + DATE_DELIM + YEAR_REGEX
# print(regex.findall(DATE_REGEX,"11/Januari/2020"))


class Date:
    def __init__(self, D, M, Y):
        self.DD = D
        self.MM = M
        self.YYYY = Y

    def __str__(self):
        return "{:04d}-{:02d}-{:02d}".format(self.YYYY, self.MM, self.DD)

    @staticmethod
    def resolveMonth(string):
        if (len(regex.findall(JANUARI_REGEX,string)) != 0): return '01'
        elif (len(regex.findall(FEBRUARI_REGEX,string)) != 0): return '02'
        elif (len(regex.findall(MARET_REGEX,string)) != 0): return '03'
        elif (len(regex.findall(APRIL_REGEX,string)) != 0): return '04'
        elif (len(regex.findall(MEI_REGEX,string)) != 0): return '05'
        elif (len(regex.findall(JUNI_REGEX,string)) != 0): return '06'
        elif (len(regex.findall(JULI_REGEX,string)) != 0): return '07'
        elif (len(regex.findall(AGUSTUS_REGEX,string)) != 0): return '08'
        elif (len(regex.findall(SEPTEMBER_REGEX,string)) != 0): return '09'
        elif (len(regex.findall(OKTOBER_REGEX,string)) != 0): return '10'
        elif (len(regex.findall(NOVEMBER_REGEX,string)) != 0): return '11'
        else : return '12'

    @staticmethod
    def string_to_date(string):
        '''
        prekondisi : string sudah memenuhi regex DATE_REGEX alias DD.MM.YYYY atau DD.Nama_Bulan.YYYY dengan . adalah pembatas tanggal
        mereturn sebuah tuple (DD, MM, YYYY) yang menyatakan tanggal
        '''
        DD = int(string[0:2])
        if(len(string) == 10):
            MM = int(string[3:5])
        else :
            MM = int(Date.resolveMonth(string[3:len(string)-5]))
        YYYY = int(string[len(string)-4:len(string)])
        return Date(DD, MM, YYYY)


    @staticmethod
    def tuple_to_date(tuple):
        '''
        prekondisi : tuple adalah (D, Del1, M, Del2, Y)  D, M, Y dalam string, Del 1 dan Del 2 adalah delimiter
        return tuple(DD, MM, YYYY) yang menyatakan tanggal.
        '''

        (D, Del1, M, Del2, Y) = tuple
        DD = int(D)
        try:
            MM = int(M)
        except :
            MM = int(Date.resolveMonth(M))
        YYYY = int(Y)
        return Date(DD, MM, YYYY)
    
    @staticmethod
    def find_all_dates_in(string):
        '''
        returns array of dates contained in a string
        '''
        list_of_tuples = regex.findall(DATE_REGEX, string)
        result = []

        for tuple in list_of_tuples:
            result.append(Date.tuple_to_date(tuple))
        
        return result

    def is_before(self, date):
        '''
            returns a True if current date is before "date"
        '''

        if(self.YYYY > date.YYYY): return False
        if(self.YYYY < date.YYYY): return True
        
        # tahunnya sama
        if(self.MM > date.MM): return False
        if(self.MM < date.MM): return True

        # bulannya sama
        if(self.DD >= date.DD): return False
        return True

    def is_same(self, date):
        '''
            returns a True if current date is the same as "date"
        '''
        if(self.YYYY > date.YYYY): return False
        if(self.YYYY < date.YYYY): return False
        # tahunnya sama
        if(self.MM > date.MM): return False
        if(self.MM < date.MM): return False
        # bulannya sama
        if(self.DD > date.DD): return False
        if(self.DD < date.DD): return False
        
        return True

    def is_after(self, date):
        '''
            returns a True if current date is after "date"
        '''
        if(self.YYYY < date.YYYY): return False
        if(self.YYYY > date.YYYY): return True
        
        # tahunnya sama
        if(self.MM < date.MM): return False
        if(self.MM > date.MM): return True

        # bulannya sama
        if(self.DD <= date.DD): return False
        return True

    def update(self, D, M, Y):
        '''
            a setter for DD, MM, YYYY attribute
        '''
        self.DD = D
        self.MM = M
        self.YYYY = Y

    def to_string(self):
        '''
            returns a string of format DDDD-MM-YY (for SQL)
        '''
        return self.YYYY + "-" + self.MM + "-" + self.DD


    '''
        setAttr(instance_name, 'attribute_name', value) sebagai sebuah setter
    '''

COURSE_REGEX = '[A-Za-z]{2}[0-9]{4}'

KATA_PENTING = ['Kuis', 'Ujian', 'Tucil', 'Tubes', 'Praktikum','Tugas']
TUGAS = ['Tucil', 'Tubes','Tugas']
# KATA_PENTING[i].lower() --> ngambil semuanya huruf kecil
# KATA_PENTING[i].capitalize() --> Kapital huruf pertama, sisanya huruf kecil
class Task:
    def __init__(self, jenis, mata_kuliah, tanggal, topik):
        self.jenis = jenis
        self.mata_kuliah = mata_kuliah
        self.tanggal = tanggal
        self.topik = topik

    @staticmethod
    def convert(string):
        jenis = None
        mata_kuliah = None
        tanggal = None
        topik = None

        # Pastikan hanya ada jenis task yang muncul di kalimat
        # Asumsikan jenis tugas diambil hanya yang pertama muncul
        allPattern =  kmpMatch_getAllMatchPattern(string,KATA_PENTING,True)
        if (len(allPattern) != 0):
            jenis = allPattern[0]

        # Pastikan hanya ada satu mata kuliah di kalimat 
        allMatkul = regex.findall(COURSE_REGEX, string)
        if (len(allMatkul) == 1):
            mata_kuliah = allMatkul[0]

        # Pastikan hanya ada satu tanggal di kalimat
        allTanggal = Date.find_all_dates_in(string)
        if (len(allTanggal) == 1):
            tanggal = allTanggal[0]
            stringTanggal = ''.join(regex.findall(DATE_REGEX, string)[0])

        # list_of_words = regex.split('\s', string)
        # for words in list_of_words:
        #     if(words.capitalize() in KATA_PENTING):
        #         jenis = words.capitalize()
        #     elif(regex.findall(COURSE_REGEX, words)):
        #         mata_kuliah = regex.findall(COURSE_REGEX, words)[0]
        #     elif(regex.findall(DATE_REGEX, words)):
        #         tanggal2 = words
        #         tanggal = Date.string_to_date(words)        
        
        # ada yang gak terisi
        if(jenis == None or mata_kuliah == None or tanggal == None):
            return None

        # Asumsi topik selalu berada diantara nama matkul dan tanggal 
        noStopword = stopword.remove(string)
        topik = noStopword[kmpMatch(noStopword,mata_kuliah,True)+len(mata_kuliah)+1:kmpMatch(noStopword,stringTanggal,True)]
        if (len(topik) <= 1):
            return None
        return Task(jenis, mata_kuliah, tanggal, topik)

    ''' tambahkan '''

# KATA_PENTING = ['Deadline', 'Selesai', 'Diundur', 'Update', 'Task', 'Minggu', 'Hari']


