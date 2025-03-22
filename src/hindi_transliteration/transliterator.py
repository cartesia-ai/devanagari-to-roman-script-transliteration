import unicodedata

from .constants import (
    HINDI_CONJUNCTS,
    HINDI_CONSONANTS,
    HINDI_DEPENDENT_VOWELS,
    HINDI_DIACRITICS,
    HINDI_DIGITS,
    HINDI_INDEPENDENT_VOWELS,
    HINDI_NUKTA_CONSONANTS,
    HINDI_SYMBOLS,
    NUKTA_COMBINATIONS,
)


class HindiTransliterator:
    """Handles transliteration of Hindi (Devanagari) text to Roman script."""

    def __init__(
        self,
        independent_vowels=HINDI_INDEPENDENT_VOWELS,
        dependent_vowels=HINDI_DEPENDENT_VOWELS,
        consonants=HINDI_CONSONANTS,
        nukta_consonants=HINDI_NUKTA_CONSONANTS,
        conjuncts=HINDI_CONJUNCTS,
        diacritics=HINDI_DIACRITICS,
        digits=HINDI_DIGITS,
        symbols=HINDI_SYMBOLS,
    ):
        self.independent_vowels = independent_vowels
        self.dependent_vowels = dependent_vowels
        self.consonants = consonants
        self.nukta_consonants = nukta_consonants
        self.conjuncts = conjuncts
        self.diacritics = diacritics
        self.digits = digits
        self.symbols = symbols

        self.all_mappings = {
            **independent_vowels,
            **dependent_vowels,
            **consonants,
            **nukta_consonants,
            **conjuncts,
            **diacritics,
            **digits,
            **symbols,
        }

        # Define word boundary characters
        self.word_boundaries = [" ", "\n", "\t", ":", "।", ".", ",", "!", "?", ";", "-"]

        self.special_vowel_mappings = dependent_vowels.copy()
        if "ा" in self.special_vowel_mappings:
            self.special_vowel_mappings["ा"] = "a"
        if "ी" in self.special_vowel_mappings:
            self.special_vowel_mappings["ी"] = "i"

    def _normalize_nukta_combinations(self, text: str) -> str:
        """Normalize split nukta combinations into their proper combined forms."""
        for base_nukta, combined in NUKTA_COMBINATIONS.items():
            text = text.replace(base_nukta, combined)
        return text

    def _normalize_additional_symbols(self, text: str) -> str:
        """Normalize additional symbols."""
        for symbol, replacement in self.symbols.items():
            text = text.replace(symbol, replacement)
        return text

    def _is_consonant(self, char: str) -> bool:
        """Check if a character is a Hindi consonant."""
        return char in self.consonants.keys() or char in self.nukta_consonants.keys()

    def _is_diacritic(self, char: str) -> bool:
        """Check if a character is a Hindi diacritic."""
        return char in self.diacritics.keys()

    def _is_independent_vowel(self, char: str) -> bool:
        """Check if a character is a Hindi independent vowel."""
        return char in self.independent_vowels.keys()

    def _is_dependent_vowel(self, char: str) -> bool:
        """Check if a character is a Hindi dependent vowel (matra)."""
        return char in self.dependent_vowels.keys()

    def _is_vowel(self, char: str) -> bool:
        """Check if a character is any Hindi vowel."""
        return self._is_independent_vowel(char) or self._is_dependent_vowel(char)

    def _is_word_boundary(self, char: str) -> bool:
        """Check if a character is a word boundary marker."""
        return char in self.word_boundaries or char is None  # None handles end of string

    def transliterate(self, text: str) -> str:
        """Transliterates Hindi text to Roman script with proper conjunct consonant handling."""
        # Normalize the input text
        content = unicodedata.normalize("NFC", text)
        content = self._normalize_nukta_combinations(content)
        content = self._normalize_additional_symbols(content)

        i = 0
        # Step 1: Process text to handle implicit "a" and special cases
        content2 = ""
        while i < len(content):
            if content[i] == "\u094d":  # halant
                content2 += content[i]
            elif content[i] in self.digits.keys():
                content2 += self.digits[content[i]]
            elif i + 1 < len(content):
                # Handle special cases for halant
                if content[i + 1] == "\u094d":  # halant
                    # Check for conjunct consonants
                    if i + 2 < len(content):
                        # Try to match a 3-character conjunct (consonant + halant + consonant)
                        conjunct = content[i] + content[i + 1] + content[i + 2]
                        if conjunct in self.conjuncts:
                            # Check if we need to add "a" - only if next char is not a vowel or vowel sign
                            if i + 3 < len(content) and (not self._is_vowel(content[i + 3])):
                                content2 += (
                                    self.conjuncts[conjunct] + "a"
                                    if i == 0
                                    else self.conjuncts[conjunct]
                                )
                            else:
                                content2 += self.conjuncts[conjunct]
                            i += 3
                            continue

                    # If no conjunct matched, proceed with regular halant handling
                    if i + 3 < len(content):
                        if (
                            content[i] in self.consonants.keys()
                            and content[i + 3] in self.consonants.keys()
                        ):
                            # Check if we need to add "a" - only if next char is not a vowel
                            if i + 4 < len(content) and (not self._is_vowel(content[i + 4])):
                                content2 = (
                                    content2 + content[i] + content[i + 1] + content[i + 2] + "a"
                                )
                            else:
                                content2 = content2 + content[i] + content[i + 1] + content[i + 2]
                        else:
                            content2 = content2 + content[i] + content[i + 1] + content[i + 2]
                        i += 2
                    elif i + 2 < len(content):
                        content2 = content2 + content[i] + content[i + 1] + content[i + 2]
                        i += 2
                    else:
                        content2 = content2 + content[i] + content[i + 1]
                        i += 1
                else:
                    # Only apply the "ein" rule at word boundaries
                    if i > 0 and content[i] == "े" and content[i + 1] == "ं":
                        # Check if this is at a word boundary (next char is a boundary or end of string)
                        next_char = content[i + 2] if i + 2 < len(content) else None
                        if self._is_word_boundary(next_char):
                            # Replace the usual "n" with "ein" when anusvara follows e-matra at word boundary
                            content2 += "ein"
                            i += 2
                            continue

                    # Special case for "ा" (aa vowel sign) - never add implicit "a"
                    if content[i + 1] == "ा":
                        content2 += content[i]
                        i += 1
                        continue

                    # Special case for chandrabindu after aa-matra (for चाँद -> chaand)
                    if content[i + 1] == "ा" and i + 2 < len(content) and content[i + 2] == "ँ":
                        content2 += content[i]
                        i += 1
                        continue

                    # Only add "a" if next character is not a vowel
                    next_is_vowel = i + 1 < len(content) and self._is_vowel(content[i + 1])

                    # Special handling for nukta characters:
                    # If the next character is not a vowel and not a word boundary, add "a" if followed by and ee or oo phonetic
                    if (
                        content[i] in self.nukta_consonants.keys()
                        and not next_is_vowel
                        and not self._is_word_boundary(content[i + 1])
                    ):
                        if i + 2 < len(content):
                            if self._is_vowel(content[i + 2]):
                                if content[i + 2] == "ू" or content[i + 2] == "ी":
                                    content2 = content2 + content[i] + "a"
                                else:
                                    content2 = content2 + content[i]
                        else:
                            content2 = content2 + content[i] + "a"
                        i += 1
                        continue

                    if self._is_consonant(content[i]) and self._is_consonant(content[i + 1]):
                        if (
                            i == 0 or content[i - 1] in [" ", "\n", "\t", ":", "।"]
                        ) and not next_is_vowel:
                            # At beginning or after separator, add "a" unless next char is vowel
                            content2 = content2 + content[i] + "a"
                        elif self._is_vowel(content[i - 1]) or self._is_consonant(content[i - 1]):
                            if (
                                i + 2 < len(content) and (not self._is_vowel(content[i + 2]))
                            ) and not next_is_vowel:
                                # Add "a" only if not followed by a vowel
                                content2 = content2 + content[i] + "a"
                            else:
                                content2 = content2 + content[i]
                        elif not next_is_vowel:
                            # we assume <sep>, add "a" unless next char is vowel
                            content2 = content2 + content[i] + "a"
                        else:
                            content2 = content2 + content[i]
                    else:
                        if content[i + 1] == "ं":  # anusvara
                            if i + 2 < len(content):
                                if self._is_consonant(content[i]) and not self._is_vowel(
                                    content[i + 2]
                                ):
                                    content2 = content2 + content[i] + "a"
                                else:
                                    content2 = content2 + content[i]
                            else:
                                content2 = content2 + content[i]
                        elif self._is_dependent_vowel(content[i + 1]):
                            # <hindi-cons><vowel-sign>
                            content2 += content[i]
                        else:
                            content2 += content[i]
            else:
                # Single character at end of string - don't add "a"
                content2 += content[i]
            i += 1

        content = content2

        # Step 2: Process the transliteration, with special handling for word boundaries and vowel sequences
        i = 0
        result = ""

        while i < len(content):
            # Check for special cases for vowel signs
            # Case 1: Badi aa ki matra (ा) at word boundary or before chandrabindu
            if content[i] == "ा":
                next_char = content[i + 1] if i + 1 < len(content) else None
                is_at_word_end = self._is_word_boundary(next_char)
                # Case 1a: At word boundary
                if is_at_word_end:
                    result += self.special_vowel_mappings["ा"]
                # Case 1b: Next to another vowel
                elif next_char and self._is_vowel(next_char):
                    result += self.special_vowel_mappings["ा"]
                else:
                    result += self.dependent_vowels["ा"]

            # Case 2: Badi ee ki matra (ी) at word boundary
            elif content[i] == "ी":
                next_char = content[i + 1] if i + 1 < len(content) else None
                is_at_word_end = self._is_word_boundary(next_char)

                if is_at_word_end:
                    result += self.special_vowel_mappings["ी"]
                elif next_char and self._is_diacritic(next_char):
                    result += self.special_vowel_mappings["ी"]
                else:
                    result += self.dependent_vowels["ी"]

            elif content[i] in self.independent_vowels:
                result += self.independent_vowels[content[i]]

            elif content[i] in self.dependent_vowels:
                result += self.dependent_vowels[content[i]]

            elif content[i] in self.consonants:
                result += self.consonants[content[i]]

            elif content[i] in self.nukta_consonants:
                result += self.nukta_consonants[content[i]]

            elif content[i] in self.diacritics:
                result += self.diacritics[content[i]]

            else:
                result += content[i]

            i += 1

        # Remove halants and replace punctuation
        result = result.replace("\u094d", "")  # removing all halants
        result = result.replace("।", ".")  # replacing danda with period

        return unicodedata.normalize("NFC", result)
