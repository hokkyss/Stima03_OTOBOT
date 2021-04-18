"""Algoritma Boyer Moore
"""
    
def bmMatch(text, pattern, caseSensitive=False):
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


