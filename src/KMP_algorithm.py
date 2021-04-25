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


