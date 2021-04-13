import re as regex

DAY_REGEX = '(0[1-9]|[1-2][0-9]|3[0-1])'
MONTH_REGEX = '(0[1-9]|1[0-2])'
YEAR_REGEX = '([0-9]{4})'
DATE_DELIM_REGEX = '([/])'

# ini untuk mengambil tuple date nya
DATE_REGEX = DAY_REGEX + '[-/]' + MONTH_REGEX + '[-/]' + YEAR_REGEX

# yang ini untuk mengambil full date nya (bisa diconvert di string_to_date.
# DATE_REGEX = '0[1-9][-/]0[1-9][-/][0-9]{4}|0[1-9][-/]1[0-2][-/][0-9]{4}|[1-2][0-9][-/]0[1-9][-/][0-9]{4}|[1-2][0-9][-/]1[0-2][-/][0-9]{4}|3[0-1][-/]0[1-9][-/][0-9]{4}|3[0-1][-/]1[0-2][-/][0-9]{4}'

def string_to_date(string):
    '''
    prekondisi : string sudah memenuhi regex DATE_REGEX alias DD.MM.YYYY dengan . adalah karakter bebas

    mereturn sebuah tuple (DD, MM, YYYY) yang menyatakan tanggal
    '''
    DD = int(string[0:2])
    MM = int(string[3:5])
    YYYY = int(string[6:10])
    return(DD, MM, YYYY)

def tuple_to_date(tuple):
    '''
    prekondisi : tuple adalah (D, M, Y) dari find_all_dates, D, M, Y dalam string

    return tuple(DD, MM, YYYY) yang menyatakan tanggal.
    '''

    (D, M, Y) = tuple
    DD = int(D)
    MM = int(M)
    YYYY = int(Y)
    return(DD, MM, YYYY)

def find_all_dates_in(string):
    list_of_tuples = regex.findall(DATE_REGEX, string)
    result = []

    for tuple in list_of_tuples:
        result.append(tuple_to_date(tuple))
        
    return result
