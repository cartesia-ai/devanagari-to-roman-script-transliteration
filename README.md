# Devanagari to Roman Script Transliteration

A Python package for transliterating Hindi (Devanagari) text to Roman script. This is based on the work by [Ritwik Mishra](https://github.com/ritwikmishra/devanagari-to-roman-script-transliteration).

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

## Citation

If you use this code, please cite the original work:

```bibtex
@misc{Mishra2019,
  author       = {Mishra, Ritwik},
  title        = {devanagari-to-roman-script-transliteration},
  year         = {2019},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/ritwikmishra/devanagari-to-roman-script-transliteration}},
}
```
