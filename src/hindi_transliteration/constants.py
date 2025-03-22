# Independent vowels (standalone form)
HINDI_INDEPENDENT_VOWELS = {
    "अ": "a",
    "आ": "aa",
    "इ": "i",
    "ई": "ee",
    "उ": "u",
    "ऊ": "oo",
    "ऋ": "ri",
    "ऌ": "l",
    "ए": "e",
    "ऐ": "ai",
    "ओ": "o",
    "औ": "au",
    "ऍ": "e",
    "ऑ": "au",
    "ॲ": "a",
}

# Dependent vowel marks (matras)
HINDI_DEPENDENT_VOWELS = {
    "ा": "aa",
    "ि": "i",
    "ी": "ee",
    "ु": "u",
    "ू": "oo",
    "ृ": "ri",
    "े": "e",
    "ै": "ai",
    "ो": "o",
    "ौ": "au",
    "ॅ": "a",
    "ॉ": "au",
}

# Nasalization markers and other diacritics
HINDI_DIACRITICS = {
    "ँ": "n",
    "ं": "n",
    "ः": "h",
    "्": "",
    "ऽ": "'",
}

# Consonants
HINDI_CONSONANTS = {
    "क": "k",
    "ख": "kh",
    "ग": "g",
    "घ": "gh",
    "ङ": "ng",
    "च": "ch",
    "छ": "chh",
    "ज": "j",
    "झ": "jh",
    "ञ": "nj",
    "ट": "t",
    "ठ": "th",
    "ड": "d",
    "ढ": "dh",
    "ण": "n",
    "त": "t",
    "थ": "th",
    "द": "d",
    "ध": "dh",
    "न": "n",
    "प": "p",
    "फ": "ph",
    "ब": "b",
    "भ": "bh",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "sh",
    "ष": "sh",
    "स": "s",
    "ह": "h",
    "ळ": "l",
    "ऱ": "r",
    "ऴ": "l",
}

# Nukta consonants (consonants with nukta)
HINDI_NUKTA_CONSONANTS = {
    "\u0958": "k",
    "\u0959": "kh",
    "\u095a": "g",
    "\u095b": "z",
    "\u095c": "r",
    "\u095d": "dh",
    "\u095e": "f",
    "\u095f": "y",
}

# Nukta combinations (characters + nukta -> combined form)
NUKTA_COMBINATIONS = {
    "क\u093c": "\u0958",  # क + nukta -> क़
    "ख\u093c": "\u0959",  # ख + nukta -> ख़
    "ग\u093c": "\u095a",  # ग + nukta -> ग़
    "ज\u093c": "\u095b",  # ज + nukta -> ज़
    "ड\u093c": "\u095c",  # ड + nukta -> ड़
    "ढ\u093c": "\u095d",  # ढ + nukta -> ढ़
    "फ\u093c": "\u095e",  # फ + nukta -> फ़
    "य\u093c": "\u095f",  # य + nukta -> य़
}

# Special conjunct consonants
HINDI_CONJUNCTS = {
    "\u0915\u094d\u0937": "ksh",  # क्ष
    "\u0936\u094d\u0930": "shr",  # श्र
    "\u091c\u094d\u091e": "gy",  # ज्ञ
    "\u0924\u094d\u0930": "tr",  # त्र
}

# Digits
HINDI_DIGITS = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9",
}

# Symbols
HINDI_SYMBOLS = {
    "॰": ".",
    "।": ".",
    "॥": "..",
    "ॐ": "om",
}

# Combined dictionary for transliteration (if needed)
HINDI_TO_ENGLISH = {
    **HINDI_INDEPENDENT_VOWELS,
    **HINDI_DEPENDENT_VOWELS,
    **HINDI_DIACRITICS,
    **HINDI_CONSONANTS,
    **HINDI_NUKTA_CONSONANTS,
    **HINDI_CONJUNCTS,
    **HINDI_DIGITS,
    **HINDI_SYMBOLS,
}
