from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from KMP_algorithm import kmpMatch
import re as regex
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# factory = StopWordRemoverFactory()
newStopFactory = StopWordRemoverFactory().get_stop_words()
newStopFactory.remove("sampai")
stopword = StopWordRemover(ArrayDictionary(newStopFactory))

# stopword = factory.create_stop_word_remover()

ANYTHING = '.*'
DAY_REGEX = '(0[1-9]|[1-2][0-9]|3[0-1])'
MONTH_REGEX = '(0[1-9]|1[0-2])'
YEAR_REGEX = '([0-9]{4})'
DATE_DELIM = '[-/]'
DATE_REGEX = DAY_REGEX + DATE_DELIM + MONTH_REGEX + DATE_DELIM + YEAR_REGEX

class Date:
    def __init__(self, D, M, Y):
        self.DD = D
        self.MM = M
        self.YYYY = Y

    def __str__(self):
        return "{:04d}-{:02d}-{:02d}".format(self.YYYY, self.MM, self.DD)

    @staticmethod
    def string_to_date(string):
        '''
        prekondisi : string sudah memenuhi regex DATE_REGEX alias DD.MM.YYYY dengan . adalah karakter bebas
        mereturn sebuah tuple (DD, MM, YYYY) yang menyatakan tanggal
        '''
        DD = int(string[0:2])
        MM = int(string[3:5])
        YYYY = int(string[6:10])
        return Date(DD, MM, YYYY)

    @staticmethod
    def tuple_to_date(tuple):
        '''
        prekondisi : tuple adalah (D, M, Y) dari find_all_dates, D, M, Y dalam string
        return tuple(DD, MM, YYYY) yang menyatakan tanggal.
        '''

        (D, M, Y) = tuple
        DD = int(D)
        MM = int(M)
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
            result.append(tuple_to_date(tuple))
        
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
        list_of_words = regex.split('\s', string)
        jenis = None
        mata_kuliah = None
        tanggal = None
        tanggal2 = None
        topik = None
        for words in list_of_words:
            if(words.capitalize() in KATA_PENTING):
                jenis = words.capitalize()
            elif(regex.findall(COURSE_REGEX, words)):
                mata_kuliah = regex.findall(COURSE_REGEX, words)[0]
            elif(regex.findall(DATE_REGEX, words)):
                tanggal2 = words
                tanggal = Date.string_to_date(words)
        
        # ada yang gak terisi
        if(jenis == None or mata_kuliah == None or tanggal == None):
            return None

        # Asumsi topik selalu berada diantara nama matkul dan tanggal 
        noStopword = stopword.remove(string)
        topik = noStopword[kmpMatch(noStopword,mata_kuliah,True)+len(mata_kuliah):kmpMatch(noStopword,tanggal2,True)]
        return Task(jenis, mata_kuliah, tanggal, topik)

    ''' tambahkan '''

# KATA_PENTING = ['Deadline', 'Selesai', 'Diundur', 'Update', 'Task', 'Minggu', 'Hari']
