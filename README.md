# Sour Python Library

Sour (Sound to Colour) is a python library aim at being able to convert the audio formats to image formats.

Current Status: **v1.0**

---

## Overview

Sour is aimed at converting audio to images and images to audio. This can be used to perform compression but also hide audio as images.

Audio can be understood at a string of 24 bits every sample. Using a standard RGB value of 0-255 we can get a single pixel of RGB from one sample of audio. For different bit depths, the audio is cut into 24 bits with extra sample audio contained.

`.sour` format includes a header pixel which contians the information of the audio to help convert back into the correct format.

---

## Installation & Setup

### Requirements
* librosa == 0.11.0
* numpy == 2.5.4
* Pillow == 13.0.0
* soundfile == 0.13.1
* sympy == 1.14.0
* tqdm == 4.67.3

### Build Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/mwallis45/Sour-Python-Library
   ```
2. Include the `sour.py` in your files.
3. Add the class into your python file you need:
    ```python
    from sour import Sour
    ```

---

## Contributing

Contributions, bug reports, and pull requests are welcome! Feel free to open an issue or submit a PR.

---

## Licensing

This project's code is licensed under the MIT License.

*Last Updated: November 3, 2026*