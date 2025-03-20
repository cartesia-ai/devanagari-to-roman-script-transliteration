"""Data Mapping for Hindi Transliteration"""

HINDI_VOWELS = dict(
    [
        ("ँ", "n"),
        ("ं", "n"),
        ("ः", "a"),
        ("अ", "a"),
        ("आ", "aa"),
        ("इ", "i"),
        ("ई", "ee"),
        ("उ", "u"),
        ("ऊ", "oo"),
        ("ऋ", "ri"),
        ("ऌ", "l"),
        ("ए", "e"),
        ("ऐ", "ae"),
        ("ओ", "o"),
        ("औ", "au"),
        ("ा", "a"),
        ("ि", "i"),
        ("ी", "i"),
        ("ु", "u"),
        ("ू", "oo"),
        ("ृ", "ri"),
        ("े", "e"),
        ("ै", "ai"),
        ("ो", "o"),
        ("ौ", "au"),
        ("ऍ", "e"),
        ("ॅ", "a"),
        ("ऑ", "au"),
        ("ॲ", "a"),
        ("ॉ", "au"),
    ]
)

# https://github.com/ritwikmishra/devanagari-to-roman-script-transliteration/blob/master/createDict.py
HINDI_CONSONANTS = dict(
    [
        ("क", "k"),
        ("क़", "k"),
        ("ख", "kh"),
        ("ख़", "kh"),
        ("ग", "g"),
        ("ग़", "g"),
        ("घ", "gh"),
        ("ङ", "ng"),
        ("च", "ch"),
        ("छ", "chh"),
        ("ज", "j"),
        ("ज़", "z"),
        ("झ", "jh"),
        ("ञ", "nj"),
        ("ट", "t"),
        ("ठ", "th"),
        ("ड", "d"),
        ("ड़", "r"),
        ("ढ", "dh"),
        ("ढ़", "d"),
        ("ण", "n"),
        ("त", "t"),
        ("थ", "th"),
        ("द", "d"),
        ("ध", "dh"),
        ("न", "n"),
        ("प", "p"),
        ("फ", "ph"),
        ("फ़", "ph"),
        ("ब", "b"),
        ("भ", "bh"),
        ("म", "m"),
        ("य", "y"),
        ("य़", "y"),
        ("र", "r"),
        ("ऱ", "r"),
        ("ल", "l"),
        ("ळ", "l"),
        ("ऴ", "l"),
        ("व", "v"),
        ("श", "sh"),
        ("ष", "sh"),
        ("स", "s"),
        ("ह", "h"),
        ("क्ष", "ksh"),
        ("त्र", "tr"),
        ("ज्ञ", "gy"),
    ]
)

# CARTESIA: We added this to keep sure devanagari digits are converted to english digits
HINDI_DIGITS = dict(
    [
        ("०", "0"),
        ("१", "1"),
        ("२", "2"),
        ("३", "3"),
        ("४", "4"),
        ("५", "5"),
        ("६", "6"),
        ("७", "7"),
        ("८", "8"),
        ("९", "9"),
    ]
)


# CARTESIA: These are additional symbols mainly from sanskrit, which are rare in hindi apart from the om symbol.
# Added to them to ensure complete coverage.
HINDI_SYMBOLS = dict(
    [
        ("॰", "."),
        ("।", "."),
        ("॥", ".."),
        ("ऽ", "'"),
        ("ॐ", "om"),
    ]
)

# CARTESIA: We added this to keep sure nukta combinations are converted to their combined forms
# Basically converting them to unicode characters
NUKTA_COMBINATIONS = {
    "ड\u093c": "\u095c",  # ड + nukta -> ड़
    "ढ\u093c": "\u095d",  # ढ + nukta -> ढ़
    "क\u093c": "\u0958",  # क + nukta -> क़
    "ख\u093c": "\u0959",  # ख + nukta -> ख़
    "ग\u093c": "\u095a",  # ग + nukta -> ग़
    "ज\u093c": "\u095b",  # ज + nukta -> ज़
    "फ\u093c": "\u095e",  # फ + nukta -> फ़
    "य\u093c": "\u095f",  # य + nukta -> य़
}
