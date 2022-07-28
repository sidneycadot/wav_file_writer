#! /usr/bin/env -S python3 -B

"""Test the WAV file writer.

We write four WAV files with three channels each, using a sample rate of 48 kHz,
with a duration of 5 seconds, and different types of samples.
"""

import math

from wav_file_writer import SampleFormat, WavFileWriter


def main():

    testcases = [
        ('uint8'   , SampleFormat.UINT8   ),
        ('int16'   , SampleFormat.INT16   ),
        ('float32' , SampleFormat.FLOAT32 ),
        ('float64' , SampleFormat.FLOAT64 )
    ]

    sample_rate = 48000  # Hz
    num_channels = 3
    duration = 5.0
    freq = 440.0
    num_samples  = round(sample_rate * duration)

    for (filename_prefix, sample_format) in testcases:

        filename = "test_{}.wav".format(filename_prefix)

        print("writing", filename, "...")

        with WavFileWriter(filename, sample_rate, num_channels, sample_format) as wav:
            for i in range(num_samples):
                t = i / sample_rate
                phase = t * freq * math.tau
                ch1 = math.cos(phase)
                ch2 = math.sin(phase)
                ch3 = math.sin(2 * phase)  # A sine signal at (2 * freq).

                wav.append_sample(ch1, ch2, ch3)


if __name__ == "__main__":
    main()
