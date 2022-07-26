"""A module for writing WAV files."""

# See http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

import struct
from typing import NamedTuple
from enum import Enum


class _SampleFormatInfo(NamedTuple):
    audio_format: int
    bytes_per_sample: int
    struct_pack_letter: str


class WaveFormat(Enum):
    PCM        = 1
    IEEE_FLOAT = 3


class SampleFormat(Enum):
    UINT8   = 1
    INT16   = 2
    FLOAT32 = 3
    FLOAT64 = 4


_sample_format_info = {
    SampleFormat.UINT8   : _SampleFormatInfo(WaveFormat.PCM       , 1, 'B'),
    SampleFormat.INT16   : _SampleFormatInfo(WaveFormat.PCM       , 2, 'h'),
    SampleFormat.FLOAT32 : _SampleFormatInfo(WaveFormat.IEEE_FLOAT, 4, 'f'),
    SampleFormat.FLOAT64 : _SampleFormatInfo(WaveFormat.IEEE_FLOAT, 8, 'd')
}


def _uint8_converter(x: float):
    """Map a floating-point value in the range [-1 .. +1] to an 8-bit unsigned integer in the range [0 .. 255]."""
    xi = round(128.0 * x + 127.5)
    return min(max(0, xi), 255)


def _int16_converter(x: float):
    """Map a floating-point value in the range [-1 .. +1] to a 16-bit signed integer in the range [-32767 .. +32767].

    This function will never return -32768, keeping the range fully symmetric.
    """
    xi = round(32767.5 * x)
    return min(max(-32767, xi), 32767)


class WavFileWriter:

    def __init__(self, filename: str, sample_rate: int, num_channels: int, sample_format: SampleFormat):
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.sample_format = sample_format
        self.sample_struct_format = "<{}{}".format(num_channels, _sample_format_info[sample_format].struct_pack_letter)
        self.num_samples = 0
        self.wavfile = open(filename, "wb")
        self._write_header()
        self.is_open = True

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def close(self):
        """Close the WavFileWriter."""
        if not self.is_open:
            raise RuntimeError("Attempt to close a WavFileWriter that is already closed.")
        self.wavfile.seek(0)
        self._write_header()
        self.wavfile.close()
        self.is_open = False

    def _write_header(self):

        format_info = _sample_format_info[self.sample_format]

        binary_header = struct.pack(
            "<HHL",
            format_info.audio_format.value,
            self.num_channels,
            self.sample_rate
        )

        binary_header = struct.pack(
            "<4sL4s4sLHHLLHH4sL",
            b"RIFF",
            36 + self.num_samples * self.num_channels * format_info.bytes_per_sample,
            b"WAVE",
            b"fmt ",
            16,
            format_info.audio_format.value,
            self.num_channels,
            self.sample_rate,
            self.sample_rate * self.num_channels * format_info.bytes_per_sample,
            self.num_channels * format_info.bytes_per_sample,
            format_info.bytes_per_sample * 8,
            b"data",
            self.num_samples * self.num_channels * format_info.bytes_per_sample
        )

        self.wavfile.write(binary_header)

    def append_raw_sample(self, *sample):
        """Append a value to the WavFileWriter."""

        if not self.is_open:
            raise RuntimeError("Attempt to append sample to a WavFileWRiter that is closed.")

        binary_sample = struct.pack(self.sample_struct_format, *sample)

        self.wavfile.write(binary_sample)
        self.num_samples += 1

    def append_sample(self, *sample):
        """Append a value to the WavFileWriter. The sample value is nominally in the range [-1 .. +1]."""

        if self.sample_format == SampleFormat.UINT8:
            # Convert and clip the sample values to the range [0 .. 255].
            self.append_raw_sample(*map(_uint8_converter, sample))
        elif self.sample_format == SampleFormat.INT16:
            # Convert and clip the sample values to the range [-32767 .. +32767].
            self.append_raw_sample(*map(_int16_converter, sample))
        else:
            # Float format. We pass the values as-is, and accept values that are outside the [-1, +1] range.
            self.append_raw_sample(*sample)
