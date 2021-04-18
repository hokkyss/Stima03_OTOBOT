
def kmpMatch(text, pattern, caseSensitive=False):
    """Mencari kemunculan pertama pattern pada text

    Args:
        text (String): string yang akan dicari kemunculan pattern
        pattern (String): pattern suatu string
        caseSensitive (Boolean) : caseSensitive pattern terhadap string, default False

    Returns:
        Integer: Index pertama kemunculan pattern, -1 jika tidak ditemukan
    """
    if caseSensitive:
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


