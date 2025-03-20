import unicodedata

from .constants import (
    HINDI_CONSONANTS,
    HINDI_DIGITS,
    HINDI_SYMBOLS,
    HINDI_VOWELS,
    NUKTA_COMBINATIONS,
)


class HindiTransliterator:
    """Handles transliteration of Hindi (Devanagari) text to Roman script."""

    def __init__(
        self, vowels: dict[str, str] = HINDI_VOWELS, consonants: dict[str, str] = HINDI_CONSONANTS
    ):
        self.vowels = vowels
        self.consonants = consonants

    def _normalize_nukta_combinations(self, text: str) -> str:
        """Normalize split nukta combinations into their proper combined forms."""
        for base_nukta, combined in NUKTA_COMBINATIONS.items():
            text = text.replace(base_nukta, combined)
        return text

    def _normalize_additional_symbols(self, text: str) -> str:
        """Normalize additional symbols."""
        for symbol, replacement in HINDI_SYMBOLS.items():
            text = text.replace(symbol, replacement)
        return text

    # Copied from https://github.com/ritwikmishra/devanagari-to-roman-script-transliteration/blob/a179b88affce6978161fbe0b277c430e56e66cf8/runTransliteration.py
    # CARTESIA: we have modified this script in various ways, notably:
    # - Input is expected to be in NFC Unicode-normalized format (favoring precomposed single-codepoint nuktas).
    # - Output will be similarly returned in NFC format.
    # - Added support for digits.
    # - Added a few more rare consonants.
    def transliterate(self, text: str) -> str:
        print(text)
        content = unicodedata.normalize("NFC", text)
        print(content)
        content = self._normalize_nukta_combinations(content)
        print(content)
        content = self._normalize_additional_symbols(content)
        print(content)
        # CARTESIA: not sure what this comment means...
        # if ज्ञ appears in beginning then [gy], otherwise gya
        # if क्ष appears in beginning then sh, otherwise [ksh]
        # square brackets means default value

        # --------------- shwa sound addition ---------------
        content2 = ""
        i = 0
        while i < len(content):
            if content[i] == "\u094d":
                # since we are already covering halants below, entering this loop will be very rare
                # we will enter it when there is
                # <hindi-cons><halant><hindi-cons><halant><hindi-cons>
                #     -3         -2       -1        i^        +1
                # example: ???
                # let us preserve the halant
                content2 += content[i]
            # NOTE: This elif statement is not present in the original github code
            # it is added to catch any hindi digits that were missed by the normalizer
            elif content[i] in HINDI_DIGITS.keys():
                content2 += HINDI_DIGITS[content[i]]
            elif i + 1 < len(content):
                if content[i + 1] == "\u094d":  # halant
                    if i + 3 < len(content):
                        if (
                            content[i] in self.consonants.keys()
                            and content[i + 3] in self.consonants.keys()
                        ):
                            # <hindi-cons><halant><hindi-cons><hindi-cons>
                            #   i^           +1       +2         +3
                            # example: prashn
                            content2 = content2 + content[i] + content[i + 1] + content[i + 2] + "a"
                        else:
                            # <hindi-cons><halant><hindi-cons><not-hindi-cons>
                            #   i^           +1       +2         +3
                            # here <not-hindi-cons> can mean hindi-vowel or a punctuation mark or whitespace
                            # example: pyaar
                            content2 = content2 + content[i] + content[i + 1] + content[i + 2]
                        i += 2
                    elif i + 2 < len(content):
                        # <hindi-cons><halant><hindi-cons><end-of-seq>
                        #   i^           +1       +2         +3
                        # example: jashn
                        content2 = content2 + content[i] + content[i + 1] + content[i + 2]
                        i += 2
                    else:
                        # <hindi-cons><halant><end-of-seq>
                        #   i^           +1       +2
                        # a rare word which is ending with a hindi consonant having a halant
                        # example: ??
                        # let us preserve the halant
                        content2 = content2 + content[i] + content[i + 1]
                        i += 1
                else:
                    if (
                        content[i] in self.consonants.keys()
                        and content[i + 1] in self.consonants.keys()
                    ):
                        if i == 0:
                            # <beg-of-seq><hindi-cons><hindi-cons>
                            #      -1          i^           +1
                            # example: हर --> har
                            content2 = content2 + content[i] + "a"
                        elif content[i - 1] in [" ", "\n", "\t", ":"]:
                            # <sep><hindi-cons><hindi-cons>
                            #   -1    i^           +1
                            # new word starts after <sep>
                            # <sep> can be whitespace or new line
                            # example: _हर --> har
                            content2 = content2 + content[i] + "a"
                        elif (
                            content[i - 1] in self.vowels.keys()
                            or content[i - 1] in self.consonants.keys()
                        ):
                            if i + 2 == len(content) or content[i + 2] not in self.vowels.keys():
                                # <hindi-vow or hindi-cons><hindi-cons><hindi-cons><eos or not-hindi-vow>
                                #            -1                  ^i           +1            +2
                                # example: अमल --> amal , विमल --> vimal
                                # example: कमल --> kamal
                                content2 = content2 + content[i] + "a"
                            else:
                                # <hindi-vow or hindi-cons><hindi-cons><hindi-cons><hindi-vow>
                                #            -1                  ^i           +1       +2
                                # example: अमली --> amli , विमला --> vimla
                                # example: कमला --> kamla
                                content2 = content2 + content[i]
                        else:
                            # we assume <sep>
                            # example: #बज --> #baj
                            content2 = content2 + content[i] + "a"

                    else:
                        if content[i + 1] == "ा":
                            if i + 2 < len(content):
                                if content[i + 2] in self.consonants.keys() or content[i + 2] == "ँ":
                                    # <hindi-cons><sound-of-A><hindi-cons or chandra-bindu>
                                    #   i^           +1          +2
                                    # example: हार --> haar, चाँद --> chaand
                                    content2 = content2 + content[i] + "a"
                                else:
                                    # <hindi-cons><sound-of-A><not-hindi-cons>
                                    #   i^           +1          +2
                                    # here <not-hindi-cons> can mean hindi-vowel or a punctuation mark or whitespace
                                    # example: गया --> gaya , मनाओ --> manao
                                    content2 += content[i]
                            else:
                                # <hindi-cons><sound-of-A><end-of-seq>
                                #   i^           +1           +2
                                # example: का --> ka
                                content2 += content[i]

                        elif content[i + 1] == "ं":
                            if i + 2 < len(content):
                                if (
                                    content[i] in self.consonants.keys()
                                    and content[i + 2] in self.consonants.keys()
                                ):
                                    # <hindi-cons><sound-n><hindi-cons>
                                    #   i^           +1       +2
                                    # example: छंद --> chhand
                                    content2 = content2 + content[i] + "a"
                                else:
                                    # <hindi-cons><sound-n><not-hindi-cons>
                                    #   i^           +1       +2
                                    # here <not-hindi-cons> can mean hindi-vowel or a punctuation mark or whitespace
                                    # example:
                                    content2 = content2 + content[i]

                            else:
                                # <hindi-cons><sound-n><end-of-seq>
                                #   i^           +1       +2
                                # example: मैं --> main
                                content2 = content2 + content[i]

                        else:
                            # <hindi-cons><hindi-vow>
                            #   i^           +1
                            # example: से --> se
                            content2 += content[i]
            else:
                content2 += content[i]
            i += 1
        content = content2
        # ---------------------------------------------------

        # print(content)

        for vk in self.vowels.keys():
            content = content.replace(vk, self.vowels[vk])

        for ck in self.consonants.keys():
            if ck in content[: len(ck)]:  # consonant in the beginning
                content = "^" + content
            # a character appears in the beginning of a word if
            # 1) if the word is the first word of the text
            # 2) if the word has any of the following before it: <whitespace> ' ' <tab> '\t' <new-line> '\n'
            if ck == "ज्ञ":
                content = content.replace("^" + ck, self.consonants[ck] + "a")
                content = content.replace(" " + ck, " " + self.consonants[ck] + "a")
                content = content.replace("\t" + ck, "\t" + self.consonants[ck] + "a")
                content = content.replace("\n" + ck, "\n" + self.consonants[ck] + "a")
            elif ck == "क्ष":
                content = content.replace("^" + ck, self.consonants[ck][1:])
                content = content.replace(" " + ck, " " + self.consonants[ck][1:])
                content = content.replace("\t" + ck, "\t" + self.consonants[ck][1:])
                content = content.replace("\n" + ck, "\n" + self.consonants[ck][1:])
            if len(content) > 0 and "^" == content[0]:
                content = content[1:]
            content = content.replace(ck, self.consonants[ck])

        content = content.replace("\u094d", "")  # removing all halants
        content = content.replace("।", ".")  # removing all purn viraam

        return unicodedata.normalize("NFC", content)
