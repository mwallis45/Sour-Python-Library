import pathlib
import librosa
import soundfile as sf # type: ignore
import numpy as np
from PIL import Image
import math
from sympy.ntheory import primefactors #type: ignore
from pathlib import Path

class Sour():
    '''
    EXAMPLE OF CODE
    ----------------------------------------------------------------------
    sour = Sour() # creation of Class

    # Audio to Image
    file_to_process = "example_audio_1.mp3"
    sour.sound_to_image(file_to_process, verbose=True)

    # Image to Audio
    file_to_process = "example_audio_1-[mp3]-44100-16-2745x2745.png"
    sour.image_to_sound(file_to_process, verbose=True)
    '''


    # +--------------------------------------------------------------------+
    # | GLOBAL VARIABLES                                                   |
    # +--------------------------------------------------------------------+
    # Data handeling
    formats: dict[str, list[str]] = {
        "audio_formats": [".mp3", ".wav"],
        "image_formats": [".sour", ".jpeg", ".png", ".jpg"],
        "bit_depths": ["8", "16", "24"],
        "sample_rates": ["44100", "48000", "96000"]
    }
    # Audio Information
    audio_stream: np.ndarray = np.array([])
    audio_sample_rate: float = 0.0
    audio_duration: float = 0.0
    audio_bit_depth: int = 0
    audio_channels: int = 0
    audio_format: str = ""
    # Image Information
    image_stream: np.ndarray = np.array([])


    # +--------------------------------------------------------------------+
    # | VALIDATION CHECKS                                                  |
    # +--------------------------------------------------------------------+
    def valid_audio_format(self, suffix: str) -> bool:
        '''Checks if the suffix is a valid audio format.'''
        try:
            self.formats["audio_formats"].index(suffix)
        except:
            return False
        return True
    

    def valid_image_format(self, suffix: str) -> bool:
        '''Checks if the suffix is a valid image format.'''
        try:
            self.formats["image_formats"].index(suffix)
        except:
            return False
        return True
    

    def valid_file_path(self, file_path: Path) -> bool:
        '''Checks if the file path is valid.'''
        if str(file_path).strip(" ") == "":
            raise ValueError(f"File path {file_path} is empty")
        
        file = pathlib.Path(file_path)
        try:
            suffix = file.suffix
            file.name
        except:
            raise ValueError(f"File path {file_path} is not valid")

        if not self.valid_audio_format(suffix) and not self.valid_image_format(suffix):
            raise ValueError(f"{suffix} is not a valid suffix")
        return True
    
    
    def valid_sample_rate(self, sample_rate: float) -> bool:
        '''Checks if the sample rate is a valid choice.'''
        try:
            self.formats["sample_rates"].index(str(int(sample_rate)))
        except:
            return False
        return True
    

    def valid_bit_depth(self, bit_depth: int) -> bool:
        '''Checks if the bit depth is a valid choice.'''
        try:
            self.formats["bit_depths"].index(str(bit_depth))
        except:
            return False
        return True
    

    def valid_channels(self, channels: int) -> bool:
        '''Checks if the total channels is a valid amount.'''
        if str(channels) not in ["1", "2"]:
            return False
        return True
    

    def valid_meta_data(self, meta_data: list[str]) -> bool:
        '''Checks the users metadata that it is valid inputs.'''
        if len(meta_data) != 4:
            raise ValueError(f"Not the correct amount of Meta Data. Expected 4 got {len(meta_data)}")
        audio_format = meta_data[0].strip("[]")
        audio_sample_rate = meta_data[1]
        audio_bit_depth = meta_data[2]
        audio_channels = meta_data[3]

        if not self.valid_audio_format(audio_format):
            raise ValueError(f"Audio Format of {audio_format} is not a valid format")
        
        if not self.valid_sample_rate(float(audio_sample_rate)):
            raise ValueError(f"Sample Rate of {audio_sample_rate} is not a valid number")
        
        if not self.valid_bit_depth(int(audio_bit_depth)):
            raise ValueError(f"Bit Depth {audio_bit_depth} is not a valid number")
        
        if not self.valid_channels(int(audio_channels)):
            raise ValueError(f"{audio_channels} is not a valid amount of channels")
        return True


    def valid_chunk_size(self, chunk_size: int) -> bool:
        '''Checks that chunk size is within the correct bounds.'''
        max_chunk = len(self.image_stream)
        if chunk_size < 1 or chunk_size > max_chunk:
            raise ValueError(f"{chunk_size} is outside the bounds 1 - {max_chunk}")
        return True
        
    
    def valid_percentage(self, percentage: float) -> bool:
        '''Checks the percentage is in the correct bounds.'''
        if percentage < 0.0 or percentage > 100.0:
            raise ValueError(f"{percentage} is outside the bounds 0 - 100")
        return True


    def valid_audio(self) -> bool:
        '''Checks audio has been loaded correctly.'''
        if self.audio_stream.size == 0:
            return False
        if self.audio_sample_rate == 0.0:
            return False
        if self.audio_duration == 0.0:
            return False
        if self.audio_bit_depth == 0:
            return False
        if self.audio_channels == 0:
            return False
        if self.audio_format == "":
            return False
        return True
    

    def valid_image(self) -> bool:
        '''Checks image has been loaded correctly.'''
        if self.image_stream.size == 0:
            return False
        return True
    

    def clean_up(self) -> None:
        '''Resets values for the class.'''
        self.audio_stream = np.array([])
        self.audio_sample_rate = 0.0
        self.audio_duration = 0.0
        self.audio_bit_depth = 0
        self.audio_channels = 0
        self.image_stream = np.array([])


    # +--------------------------------------------------------------------+
    # | GET METHODS                                                        |
    # +--------------------------------------------------------------------+
    def get_formats(self) -> dict[str, list[str]]:
        return self.formats
    

    def get_audio_stream(self) -> np.ndarray:
        return self.audio_stream
    

    def get_audio_sample_rate(self) -> float:
        return self.audio_sample_rate
    

    def get_audio_duration(self) -> float:
        return self.audio_duration
    

    def get_audio_bit_depth(self) -> int:
        return self.audio_bit_depth
    

    def get_audio_channels(self) -> int:
        return self.audio_channels
    

    def get_audio_format(self) -> str:
        return self.audio_format
    

    def get_image_stream(self) -> np.ndarray:
        return self.image_stream
    

    # +--------------------------------------------------------------------+
    # | SET METHODS                                                        |
    # +--------------------------------------------------------------------+
    def set_audio_stream(self, value: np.ndarray) -> None:
        if value.size > 0:
            self.audio_stream = value
    

    def set_audio_sample_rate(self, value: float) -> None:
        if self.valid_sample_rate(value):
            self.audio_sample_rate = value
    

    def set_audio_duration(self, value: float) -> None:
        if value > 0.0:
            self.audio_duration = value
    

    def set_audio_bit_depth(self, value: int) -> None:
        if self.valid_bit_depth(value):
            self.audio_bit_depth = value
    

    def set_audio_channels(self, value: int) -> None:
        if self.valid_channels(value):
            self.audio_channels = value
    

    def set_audio_format(self, value: str) -> None:
        if self.valid_audio_format(value):
            self.audio_format = value
    

    def set_image_stream(self, value: np.ndarray) -> None:
        if value.size > 0:
            self.image_stream = value
    

    # +--------------------------------------------------------------------+
    # | SOUR FORMAT                                                        |
    # +--------------------------------------------------------------------+
    def pixel_data_encoder(self, verbose: bool = False, print_space: str = "") -> np.ndarray:
        '''
        Docstring for pixel_data_encoder

        :param self: Description
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        '''
        idx_sr = self.formats["sample_rates"].index(str(int(self.audio_sample_rate)))
        idx_br = self.formats["bit_depths"].index(str(self.audio_bit_depth))
        idx_ft = self.formats["audio_formats"].index(self.audio_format)
        bit_ch = self.audio_channels

        # RGB Mappings
        # R = 0000 0000 | sample rate options: 3   | Max R = 0000 0010
        # G = 0000 0000 | bit depth options: 3     | Max G = 0000 0010
        # B = 0000 0000 | audio formats options: 2 | audio channels: 2 | Max B = 0001 0001
        red = idx_sr
        green = idx_br
        blue = (idx_ft << 4) | (bit_ch & 0x0F)

        if verbose:
            print(f"{print_space} Sour Pixel Incoding")
            print(f"{print_space} Sample Rate: {self.audio_sample_rate} | Bit Depth: {self.audio_bit_depth} | File Format: {self.audio_format} | Channels: {self.audio_channels}")
            print(f"{print_space} Red: {red} | Green: {green} | Blue: {blue}")
        return np.array([red, green, blue], dtype=np.uint8)
    

    def pixel_data_decoder(self, pixel: np.ndarray, verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for pixel_data_decoder

        :param self: Description
        :param pixel: Description
        :type pixel: np.ndarray
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        red, green, blue = map(int, pixel[:3])

        # RGB Mappings
        # R = 0000 0010 | sample rate options: 3
        # G = 0000 0010 | bit depth options: 3
        # B = 0001 0001 | audio formats options: 2 | audio channels: 2
        idx_sr = red
        idx_br = green
        idx_ft = (blue >> 4) & 0x0F  # Shift right to get the top 4 bits
        bit_ch = blue & 0x0F

        self.audio_sample_rate = float(self.formats["sample_rates"][int(idx_sr)])
        self.audio_bit_depth = int(self.formats["bit_depths"][int(idx_br)])
        self.audio_format = str(self.formats["audio_formats"][int(idx_ft)])
        self.audio_channels = bit_ch

        if verbose:
            print(f"{print_space} Sour Pixel Decoding")
            print(f"{print_space} Red: {red} | Green: {green} | Blue: {blue}")
            print(f"{print_space} Sample Rate: {self.audio_sample_rate} | Bit Depth: {self.audio_bit_depth} | File Format: {self.audio_format} | Channels: {self.audio_channels}")
    

    # +--------------------------------------------------------------------+
    # | ATRIBUTE LOADERS                                                   |
    # +--------------------------------------------------------------------+
    def find_audio_info(self, file_path: str | Path, mono: bool = True, verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for find_audio_info

        :param self: Description
        :param file_path: Description
        :type file_path: str | Path
        :param mono: Description
        :type mono: bool
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        self.audio_stream, self.audio_sample_rate = librosa.load(file_path, sr=None, mono=mono)
        if verbose:
            print(f"{print_space} Audio Loaded")
            print(f"{print_space} Sample Rate Loaded")

        self.audio_duration = librosa.get_duration(y=self.audio_stream, sr=self.audio_sample_rate)
        if verbose:
            print(f"{print_space} Duration of Audio Loaded")


    def find_bit_depth(self, file_path: str | Path, verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for find_bit_depth

        :param self: Description
        :param file_path: Description
        :type file_path: str | Path
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        sf_info = sf.info(file_path) # type: ignore
        original_bit_depth_str = sf_info.subtype
        calculated_bitrate: int = 16

        if original_bit_depth_str:
            if "PCM" in original_bit_depth_str:
                try:
                    bd: int = int(original_bit_depth_str.split("_")[1])
                    if bd in [8, 16, 24, 32]:
                        calculated_bitrate = bd
                except (IndexError, ValueError):
                    pass
            elif "FLOAT" in original_bit_depth_str or "DOUBLE" in original_bit_depth_str:
                calculated_bitrate = 24
        self.audio_bit_depth = calculated_bitrate

        if verbose:
            print(f"{print_space} Bit Rate Loaded")


    def find_image_path_format(self, file_path_name: str, meta_data: list[str] = [], verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for find_image_path_format

        :param self: Description
        :param file_path: Description
        :type file_path: str
        :param meta_data: Description
        :type meta_data: list[str]
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if len(meta_data) != 4:
            raise ValueError(f"Not the correct amount of Meta Data. Expected 5 got {len(meta_data)}")
        
        self.audio_format = meta_data[0].strip("[]")
        self.audio_sample_rate = float(meta_data[1])
        self.audio_bit_depth = int(meta_data[2])
        self.audio_channels = int(meta_data[3])

        if verbose:
            print(f"{print_space} Image format loaded correctly")
            self.print_audio_info(file_path_name, print_space=print_space+" ")
    

    def find_bit_rate(self) -> str:
        '''Returns the bit rate of the audio loaded.'''
        bit_rate = self.audio_sample_rate * self.audio_bit_depth * self.audio_channels
        return str(round(bit_rate/1000, 1)) + "k"
    

    # +--------------------------------------------------------------------+
    # | PRINTS                                                             |
    # +--------------------------------------------------------------------+
    def print_audio_info(self, file_path_name: str, print_space: str = "") -> None:
        '''Prints the infomation of the audio file loaded.'''
        print(
            f"{print_space} File: {file_path_name}\n"
            f"{print_space} Sample Rate: {self.audio_sample_rate} Hz\n"
            f"{print_space} Duration: {self.audio_duration:.2f} seconds\n"
            f"{print_space} Original Bit Depth {self.audio_bit_depth}\n"
            f"{print_space} File Type: {self.audio_format}\n"
            f"{print_space} Audio Channels: {self.audio_channels}"
        )

    
    def print_formats(self) -> None:
        '''Prints all formats.'''
        for keys, values in self.formats.items():
            for value in values:
                print(f"{keys}: {value}")

    
    # +--------------------------------------------------------------------+
    # | Helpers                                                            |
    # +--------------------------------------------------------------------+
    def factorize(self, num: int) -> list[int]:
        '''Returns the factors of the number.'''
        return [n for n in range(1, num + 1) if num % n == 0]   


    def grid_size(self, override: int = 0,
                  verbose: bool = False,
                  print_space: str = ""
                  ) -> tuple[int, int]:
        '''
        Docstring for grid_size

        :param self: Description
        :param override: Description
        :type override: int
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        :return: Description
        :rtype: tuple[int, int]
        '''
        total_pixels = override if override != 0 else len(self.image_stream)
        factors = self.factorize(total_pixels)
        total_factors = len(factors)
        mid = total_factors // 2
        x, y = 0, 0

        if total_factors % 2 == 0 and total_factors > 2:
            x, y = factors[mid - 1], factors[mid]
        elif total_factors % 2 == 1 and total_factors > 2:
            x, y = factors[mid], factors[mid]
        
        if verbose:
            print(f"{print_space} total Pixels: {total_pixels}\n"
                  f"{print_space} Factors: {factors}\n"
                  f"{print_space} Total Factors: {total_factors}\n"
                  f"{print_space} Mid: {mid}"
                  )

        if y - x > math.sqrt((x ** 2) + ((y / 3) ** 2)) or total_factors < 3:
            side = int(math.ceil(math.sqrt(total_pixels)))
            if verbose:
                print(f"{print_space} x, y: {side}, {side}")
            return side, side
        if verbose:
            print(f"{print_space} x, y: {x}, {y}")
        return x, y
    

    # +--------------------------------------------------------------------+
    # | IMAGE AVARAGING                                                    |
    # +--------------------------------------------------------------------+
    def reduce_image(self,
                     file_path: Path,
                     style: str = "SLICE",
                     chunk_size: int = 1,
                     percentage: float = 0.0,
                     full_resize: bool = False,
                     max_size: int = 0,
                     verbose: bool = False,
                     print_space: str = ""
                     ) -> None:
        '''
        Docstring for reduce_image

        :param self: Description
        :param file_path: Description
        :type file_path: str
        :param style: Description
        :type style: str
        :param chunk_size: Description
        :type chunk_size: int
        :param percentage: Description
        :type percentage: float
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if not self.valid_file_path(file_path):
            return

        if not self.valid_image():
            if verbose:
                print(f"{print_space} No Image generated")
                print(f"{print_space} Auto generating Image from File Path")
            self.gen_image(file_path, verbose=verbose)

        if style not in ["AVG", "SLICE"]:
            return

        if not self.valid_chunk_size(chunk_size):
            return
        
        if not self.valid_percentage(percentage):
            return
        
        if full_resize:
            decrease: float = len(self.image_stream) / (max_size ** 2)
            chunk_size = int(decrease)
        
        header_pixel = self.image_stream[0].reshape(1, 3).astype(np.uint8)
        data_to_process = self.image_stream[1:]
        chunks = chunk_size if percentage == 0 else int(round(len(data_to_process)/self.audio_sample_rate) * (percentage/100))
        chunks = max(1, chunks)

        reduced_list: list[np.ndarray] = []
        if style == "AVG":
            for i in range(0, len(data_to_process), chunks):
                chunk = data_to_process[i : i + chunks]
                if len(chunk) == 0:
                    continue
                avg_pixel = np.mean(chunk, axis=0).astype(np.uint8)
                reduced_list.append(avg_pixel)

        if style == "SLICE":
            for i in range(0, len(data_to_process), chunks):
                chunk = data_to_process[i]
                if len(chunk) == 0:
                    continue
                reduced_list.append(chunk)

        self.image_stream = np.vstack([header_pixel, np.array(reduced_list, dtype=np.uint8)])


    # +--------------------------------------------------------------------+
    # | AUDIO TO IMAGE                                                     |
    # +--------------------------------------------------------------------+
    def load_audio(self,
                   file_path: Path,
                   mono: bool = False,
                   verbose: bool = False,
                   print_space: str = ""
                   ) -> None:
        '''
        Docstring for load_audio

        :param self: Description
        :param file_path: Description
        :type file_path: str
        :param mono: Description
        :type mono: bool
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if verbose:
            print(f"{print_space} Loading Audio...")

        if not self.valid_file_path(file_path):
            return
        
        if verbose:
            print(f"{print_space} File Checked")

        self.audio_format = file_path.suffix
        self.audio_channels = 1 if mono else 2

        try:
            self.find_audio_info(file_path, mono=mono , verbose=verbose, print_space=print_space+" ")
            self.find_bit_depth(file_path, verbose=verbose, print_space=print_space+" ")
            if verbose:
                self.print_audio_info(file_path.name, print_space=print_space+" ")
                print(f"{print_space} Audio Loaded Correctly.")
            return
        except Exception as e:
            print(f"{print_space} Error processing file: {e}")
            return


    def gen_image(self,
                  file_path: Path,
                  mono: bool = False,
                  verbose: bool = False,
                  print_space: str = ""
                  ) -> None:
        '''
        Docstring for gen_image

        :param self: Description
        :param file_path: Description
        :type file_path: str
        :param mono: Description
        :type mono: bool
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if not self.valid_audio():
            if verbose:
                print(f"{print_space} No Audio Loaded")
                print(f"{print_space} Auto Loading Audio from File Path")
            self.load_audio(file_path, mono=mono, verbose=verbose, print_space=print_space+" ")

        if self.audio_bit_depth == 24:
            max_24 = (2**23) - 1
            samples = (self.audio_stream * max_24).astype(np.int32)
            b1 = (samples >> 16) & 0xFF
            b2 = (samples >> 8) & 0xFF
            b3 = samples & 0xFF
            raw_bytes = np.stack((b1, b2, b3), axis=-1).astype(np.uint8).flatten()

        elif self.audio_bit_depth == 16:
            samples = (self.audio_stream * 32767).astype(np.int16)
            raw_bytes = samples.view(np.uint8)

        else:
            raw_bytes = ((self.audio_stream + 1.0) / 2.0 * 255).astype(np.uint8)

        remainder = len(raw_bytes) % 3
        if remainder > 0:
            padding = np.zeros(3 - remainder, dtype=np.uint8)
            raw_bytes = np.concatenate([raw_bytes, padding])

        self.image_stream = raw_bytes.reshape(-1, 3)
        if verbose:
            print(f"{print_space} Image created. Total Pixels: {len(self.image_stream)}")


    def save_image(self,
            file_path: str | Path,
            mono: bool = False,
            save_as: str | Path = "",
            file_type: str = ".png",
            max_size: int = 0,
            sour_png: bool = False,
            fill: bool = False,
            verbose: bool = False,
            print_space: str = ""
        ) -> None:
        '''
        Docstring for save_image

        :param self: Description
        :param file_path: Description
        :type file_path: str | path
        :param mono: Description
        :type mono: bool
        :param save_as: Description
        :type save_as: str | Path
        :param file_type: Description
        :type file_type: str
        :param max_size: Description
        :type max_size: int
        :param sour_png: Description
        :type sour_png: bool
        :param fill: Description
        :type fill: bool
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        file_path = Path(file_path)
        if not self.valid_file_path(file_path):
            return
        
        if not self.valid_image():
            if verbose:
                print(f"{print_space} No Image generated")
                print(f"{print_space} Auto generating Image from File Path")
            self.gen_image(file_path, mono=mono, verbose=verbose, print_space=print_space+" ")

        if not self.valid_image_format(file_type):
            return

        save_as = Path(save_as) if save_as else ""
        data_to_save = self.image_stream

        sour_png = True if file_type == ".sour" else sour_png
        if sour_png:
            header_pixel = self.pixel_data_encoder(verbose=verbose, print_space=print_space+" ").reshape(1, 3)
            data_to_save = np.vstack([header_pixel, data_to_save])

        num_pixels = len(data_to_save)
        if max_size == 0:
            x, y = self.grid_size(override=num_pixels, verbose=verbose, print_space=print_space+" ")
        else:
            x, y = max_size, max_size
            if verbose:
                print(f"{print_space} x, y: {x}, {y}")

        total_required = x * y
        if verbose:
            print(f"{print_space} Imaged resized to {total_required} pixels")
        if num_pixels > total_required:
            data_to_save = data_to_save[:total_required]
    
        elif num_pixels < total_required:
            padding_pixels = total_required - num_pixels
            if fill:
                repeats = (padding_pixels // len(self.image_stream)) + 1
                padding = np.tile(self.image_stream, (repeats, 1))[:padding_pixels]
            else:
                padding = np.zeros((padding_pixels, 3), dtype=np.uint8)
            data_to_save = np.vstack([data_to_save, padding])

        img_array = data_to_save.reshape((x, y, 3))
        img = Image.fromarray(img_array, "RGB")
        if save_as != "":
            final_name = save_as.with_suffix(file_type)
        else:
            meta = f"[{file_path.suffix[1:]}]-{int(self.audio_sample_rate)}-{self.audio_bit_depth}-{math.ceil(self.audio_duration)}-{x}x{y}"
            final_name = f"{file_path.stem}-{meta}{file_type}"

        final_name = pathlib.Path(final_name)
        save_format = "PNG" if file_type.lower() == ".sour" else "PNG"
        if sour_png:
            final_name_sour = f"{final_name.stem}.sour"
            img.save(final_name_sour, format="PNG")
        img.save(str(final_name), format=save_format)
        if verbose:
            print(f"{print_space} Saved {file_type} file: {final_name}\n\n")

    
    def audio_to_image(self, file_path: str | Path, mono: bool = False, max_size: int = 0, save_as: str | Path = "", file_type: str = ".png", sour_png: bool = False, style: str = "SLICE", chunk_size:int = 1, percentage: float = 0.0, full_resize: bool = False, fill: bool = False, verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for audio_to_image

        :param self: Description
        :param file_path: Description
        :type file_path: str | Path
        :param mono: Description
        :type mono: bool
        :param max_size: Description
        :type max_size: int
        :param save_as: Description
        :type save_as: str
        :param file_type: Description
        :type file_type: str
        :param sour_png: Description
        :type sour_png: bool
        :param style: Description
        :type style: str
        :param chunk_size: Description
        :type chunk_size: int
        :param percentage: Description
        :type percentage: float
        :param fill: Description
        :type fill: bool
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        file_path = Path(file_path)
        if not self.valid_file_path(file_path):
            return
        
        self.load_audio(file_path, mono=mono, verbose=verbose, print_space=print_space)
        self.gen_image(file_path, verbose=verbose, print_space=print_space)
        if chunk_size != 1 or percentage != 0.0 or full_resize:
            self.reduce_image(file_path, style=style, chunk_size=chunk_size, percentage=percentage, full_resize=full_resize, max_size=max_size, verbose=verbose, print_space=print_space)
        self.save_image(file_path, save_as=save_as, max_size=max_size, file_type=file_type, sour_png=sour_png, fill=fill, verbose=verbose, print_space=print_space)


    # +--------------------------------------------------------------------+
    # |  IMAGE TO AUDIO                                                    |
    # +--------------------------------------------------------------------+
    def load_image(self, file_path: Path, meta_data: list[str] = [], verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for load_image

        :param self: Description
        :param file_path: Description
        :type file_path: Path
        :param meta_data: Description
        :type meta_data: list[str]
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if not self.valid_file_path(file_path):
            return

        if file_path.suffix != ".sour":
            if not self.valid_meta_data(meta_data=meta_data):
                return

        img = Image.open(file_path).convert("RGB")
        img_array = np.array(img).reshape(-1, 3)
        
        if file_path.suffix == ".sour":
            if verbose:
                print(f"{print_space} Detected .sour format. Extracting header pixel...")
            header_pixel = img_array[0]
            data_pixels = img_array[1:]
            self.pixel_data_decoder(header_pixel, verbose=verbose, print_space=print_space + " ")
        else:
            if verbose:
                print(f"{print_space} Standard image format. Attempting to parse filename for metadata...")
            data_pixels = img_array
            self.find_image_path_format(file_path.name, meta_data=meta_data, verbose=verbose, print_space=print_space + " ")

        header = 1 if file_path.suffix.lower() == ".sour" else 0
        self.audio_duration = ((len(data_pixels)-header) * 3) / ((self.audio_bit_depth // 8) * self.audio_channels * self.audio_sample_rate)
        self.image_stream = data_pixels

        if verbose:
            print(f"{print_space} Audio Duration: {self.audio_duration}")
            print(f"{print_space} Image Loaded.")


    def gen_audio(self, file_path: Path, meta_data: list[str] = [], verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for gen_audio

        :param self: Description
        :param file_path: Description
        :type file_path: Path
        :param meta_data: Description
        :type meta_data: list[str]
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if not self.valid_image():
            if verbose:
                print(f"{print_space} No Image loaded")
                print(f"{print_space} Automaticaly loading fomr File Path")
            self.load_image(file_path, meta_data=meta_data, verbose=verbose, print_space=print_space+" ")

        raw_bytes = self.image_stream.flatten()
        if self.audio_bit_depth == 24:
            rgb_data = raw_bytes.reshape(-1, 3).astype(np.int32)
            samples_int = (rgb_data[:, 0] << 16) | (rgb_data[:, 1] << 8) | rgb_data[:, 2]
            samples_int[samples_int >= 0x800000] -= 0x1000000
            audio = samples_int.astype(np.float32) / ((2**23) - 1)

        elif self.audio_bit_depth == 16:
            audio_bytes = raw_bytes[:(len(raw_bytes) // 2) * 2]
            samples_int = audio_bytes.view(np.int16)
            audio = samples_int.astype(np.float32) / 32767.0

        else:
            audio = (raw_bytes.astype(np.float32) / 255.0 * 2.0) - 1.0

        self.audio_stream = audio

        if verbose:
            print(f"{print_space} Audio has been loaded from Image data.")


    def save_audio(self, file_path: Path, meta_data: list[str] = [], file_format: str = "", save_as: str = "", verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for save_audio

        :param self: Description
        :param file_path: Description
        :type file_path: Path
        :param meta_data: Description
        :type meta_data: list[str]
        :param file_format: Description
        :type file_format: str
        :param save_as: Description
        :type save_as: str
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        if not self.valid_file_path(file_path):
            return

        if not self.valid_audio():
            if verbose:
                print(f"{print_space} No Audio data has been loaded")
                print(f"{print_space} Automatically generating from File Path")
            self.gen_audio(file_path, meta_data=meta_data, verbose=verbose, print_space=print_space+" ")

        if file_format == "" and self.audio_format == "":
            file_format = ".mp3"
        elif file_format == "":
            file_format = self.audio_format

        if not self.valid_audio_format(file_format):
            return

        p = pathlib.Path(file_path)
        expected_samples = int(self.audio_sample_rate * self.audio_duration)
        self.audio_stream = self.audio_stream[:expected_samples]

        if save_as != "":
            final_name = f"{save_as}{file_format}"
        else:
            final_name = f"{p.stem}{file_format}"

        sf.write(final_name, self.audio_stream, int(self.audio_sample_rate)) # type: ignore
        if verbose:
            print(f"{print_space} Success! Audio saved as {final_name}\n\n")


    def image_to_audio(self, file_path: str | Path, meta_data: list[str] = [], file_format: str = "", save_as: str = "", verbose: bool = False, print_space: str = "") -> None:
        '''
        Docstring for image_to_audio

        :param self: Description
        :param file_path: Description
        :type file_path: str | Path
        :param meta_data: Description
        :type meta_data: list[str]
        :param file_format: Description
        :type file_format: str
        :param save_as: Description
        :type save_as: str
        :param verbose: Description
        :type verbose: bool
        :param print_space: Description
        :type print_space: str
        '''
        file_path = Path(file_path)
        if not self.valid_file_path(file_path):
            return

        self.load_image(file_path, meta_data=meta_data, verbose=verbose, print_space=print_space+" ")
        self.gen_audio(file_path, meta_data=meta_data, verbose=verbose, print_space=print_space+" ")
        self.save_audio(file_path, meta_data=meta_data, file_format=file_format, save_as=save_as, verbose=verbose, print_space=print_space+" ")
        self.clean_up()
