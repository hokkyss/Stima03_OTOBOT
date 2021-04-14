import re as regex

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

TASK_PENTING = ['Kuis', 'Ujian', 'Tucil', 'Tubes', 'Praktikum']
# KATA_PENTING[i].lower() --> ngambil semuanya huruf kecil
# KATA_PENTING[i].capitalize() --> Kapital huruf pertama, sisanya huruf kecil
class Task:
    num_of_task = 0
    def __init__(self, jenis, mata_kuliah, tanggal, topik):
        self.ID = Task.num_of_task
        Task.num_of_task += 1

        self.jenis = jenis
        self.mata_kuliah = mata_kuliah
        self.tanggal = tanggal
        self.topik = topik

    @staticmethod
    def convert(string):
        list_of_words = regex.split('\s', string)

        for words in list_of_words:
            if(words.capitalize() in TASK_PENTING):
                jenis = words.capitalize()
            elif(regex.findall(COURSE_REGEX, words)):
                mata_kuliah = regex.findall(COURSE_REGEX, words)[0]
            elif(regex.findall(DATE_REGEX, words)):
                tanggal = string_to_date(words)
            else:
                topik = '' # masih dibutuhkan
        return Task(jenis, mata_kuliah, tanggal, topik)

    @staticmethod
    def get_task_by_ID(id, task_list):
        i = 0
        for each_task in task_list:
            if(each_task.ID == id): return i
            i += 1
        return -1
    ''' tambahkan '''

KATA_PENTING = ['Deadline', 'Selesai', 'Diundur', 'Update', 'Task', 'Minggu', 'Hari', 
