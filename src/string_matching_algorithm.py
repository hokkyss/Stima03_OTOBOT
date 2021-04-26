"""Algoritma KMP"""

def kmpMatch_getAllMatchPattern(text,listOfPattern,caseSensitive=False):
    """Mencari pattern apa saja yang muncul di text dari sekumpulan pattern

    Args:
        text (String): string yang akan dicari kemunculan pattern
        listOfPattern (List<String>): kumpulan pattern 
        caseSensitive (Boolean) : caseSensitive pattern terhadap string, default False

    Returns:
        List<Integer>: kumpulan pattern yang muncul pada suatu text, kosong jika tidak ada
    """
    result = []
    for pattern in listOfPattern:
        if(kmpMatch(text,pattern,caseSensitive)!= -1):
            result.append(pattern)
    return result

def kmpMatch(text, pattern, notCaseSensitive=True):
    """Mencari kemunculan pertama pattern pada text

    Args:
        text (String): string yang akan dicari kemunculan pattern
        pattern (String): pattern suatu string
        caseSensitive (Boolean) : caseSensitive pattern terhadap string, default False

    Returns:
        Integer: Index pertama kemunculan pattern, -1 jika tidak ditemukan
    """
    if notCaseSensitive:
        text = text.lower()
        pattern = pattern.lower()
       
    fail = computeFail(pattern) 
    
    n = len(text)
    m = len(pattern)
    j = 0
    i = 0
    
    while i < n:
        if pattern[j] == text[i]:
            if j == m-1:
                return i - m + 1
            i += 1
            j += 1
        elif j > 0:
            j = fail[j-1]
        else:
            i += 1
    
    return -1
                
    
def computeFail(pattern):
    """Mencari prefix terbesar dari suffix pattern

    Args:
        pattern (String): Pattern yang ingin dicari

    Returns:
        Array of Integer: Array yang menyatakan prefix terbesar dari suatu suffix pattern pada posisi ke i
    """
    fail = [0 for i in range(len(pattern))]
    m = len(pattern)
    j = 0
    i = 1
    while i < m:
        if (pattern[j] == pattern[i]):
            fail[i] = j+1
            i += 1
            j += 1
        elif (j > 0):
            j = fail[j-1]
        else:
            fail[i] = 0
            i += 1
    
    return fail


"""Algoritma Boyer Moore """

def bMMatch_getAllMatchPattern(text,listOfPattern,caseSensitive=False):
    """Mencari pattern apa saja yang muncul di text dari sekumpulan pattern

    Args:
        text (String): string yang akan dicari kemunculan pattern
        listOfPattern (List<String>): kumpulan pattern 
        caseSensitive (Boolean) : caseSensitive pattern terhadap string, default False

    Returns:
        List<Integer>: kumpulan pattern yang muncul pada suatu text, kosong jika tidak ada
    """
    result = []
    for pattern in listOfPattern:
        if(bmMatch(text,pattern,caseSensitive)!= -1):
            result.append(pattern)
    return result
    
def bmMatch(text, pattern, notCaseSensitive=True):
    """Mencari kemunculan pertama pattern pada text

    Args:
        text (String): string yang akan dicari kemunculan pattern
        pattern (String): pattern suatu string
        caseSensitive (Boolean) : caseSensitive pattern terhadap string, default False

    Returns:
        Integer: Index pertama kemunculan pattern, -1 jika tidak ditemukan
    """
    
    if notCaseSensitive:
        text = text.lower()
        pattern = pattern.lower()
    
    last = buildLast(pattern)
    n = len(text)
    m = len(pattern)
    i = m-1     # Index pencarian di text
    j = m-1     # Index pencarian di pattern
    
    if (i > n-1):
        # Tidak ada hasil jika pattern lebih panjang daripada text
        return -1
    
    while (i < n):
        if pattern[j] == text[i]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            lo = last[ord(text[i])]  # Kemunculan terakhir character text pada pattern
            i = i + m - min(j, 1+lo)
            j = m-1
        
        
    # Gagal ditemukan
    return -1


def buildLast(pattern):
    """Menghasilkan array yang merepresentasikan index kemunculan terakhir karakter

    Args:
        pattern (String): Pattern suatu string
        
    Returns:
        Array of Integer: array yang merepresentasikan index kemunculan terakhir karakter
    """

    last = [-1 for i in range(128)]
    
    for i in range(len(pattern)):
        last[ord(pattern[i])] = i
        
    return last

def levenshtein_distance(s, t, caseSensitive = False):
    """ 
    Menghitung jarak levenshtein (banyaknya edit,insert, atau delete) dari string s dan string t supaya kedua string sama
    Argument:
    s : String (string pertama yang akan dicompare) 
    t : String (string kedua yang akan dicompare) 
    caseSensitive : Boolean (apakah perhitungan mempertimbangkan huruf besar dan kecil)
    """
    if (not (caseSensitive)):
        s = s.lower()
        t = t.lower()
    rows = len(s)+1
    cols = len(t)+1
    levenshtein_matrix = [[0 for j in range(cols)] for i in range(rows)]

    # Inisialisasi distance untuk string kosong pada matrix levenshtein distance (base case)
    # Apabila s merupakan string kosong maka s dapat dibentuk menjadi string t dengan menginsert element t ke s satu persatu 
    for i in range(1, cols):
        levenshtein_matrix[0][i] = i
    # Apabila t merupakan string kosong maka s dapat dibentuk menjadi t dengan menghapus elemen dari s satu persatu
    for i in range(1, rows):
        levenshtein_matrix[i][0] = i
    
    # Pengisan matrix levenshtein distance untuk string tidak kosong (iterative recursive case)
    for row in range(1, rows):
        for col in range(1, cols):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            a = levenshtein_matrix[row-1][col] + 1      # Kasus deletion
            b = levenshtein_matrix[row][col-1] + 1      # Kasus insertion
            c = levenshtein_matrix[row-1][col-1] + cost   # Kasus substitution (perhatikan bahwa apabila huruf sama maka biaya substitutionnya 0)
            levenshtein_matrix[row][col] = min (a,b,c)
    
    return levenshtein_matrix[rows-1][cols-1]

def levenshtein_ratio(s, t, caseSensitive = False):
    """ 
    Menghitung jarak levenshtein dalam bentuk rasio (banyaknya edit,insert, atau delete) dari string s dan string t supaya kedua string sama
    Argument:
    s : String (string pertama yang akan dicompare) 
    t : String (string kedua yang akan dicompare) 
    caseSensitive : Boolean (apakah perhitungan mempertimbangkan huruf besar dan kecil)
    """
    return float(1-(levenshtein_distance(s,t,caseSensitive)/max(len(t),len(s))))


