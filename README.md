# Devanagari to Roman Script Transliteration

A Python package for transliterating Hindi (Devanagari) text to Roman script.

## Installation

```bash
# Clone the repository
git clone git@github.com:cartesia-ai/devanagari-to-roman-script-transliteration.git
cd devanagari-to-roman-script-transliteration

# Basic install for most users
pip install -e .

# For developers who need testing/linting tools
pip install -e ".[dev]"

# Set up pre-commit hooks (for developers)
pre-commit install
```

## Usage

```python
from hindi_transliteration import HindiTransliterator

transliterator = HindiTransliterator()
roman_text = transliterator.transliterate("नमस्ते दुनिया")
print(roman_text)  # Output: "namaste duniya"
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
