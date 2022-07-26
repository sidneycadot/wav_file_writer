#! /usr/bin/env -S python3 -B

import math

from wav_file_writer import SampleFormat, WavFileWriter

def main():

    testcases = [
        ('uint8'   , SampleFormat.INT8    ,   125.0),
        ('int16'   , SampleFormat.INT16   , 32000.0),
        ('float32' , SampleFormat.FLOAT32 ,     1.0),
        ('float64' , SampleFormat.FLOAT64 ,     1.0)
    ]

    sample_rate = 48000  # Hz
    num_channels = 3
    duration = 5.0
    freq = 440.0
    num_samples  = round(sample_rate * duration)

    for (filename_prefix, sample_format, multiplier) in testcases:

        filename = "test_{}.wav".format(filename_prefix)

        print("writing", filename, "...")

        with WavFileWriter(filename, sample_rate, num_channels, sample_format) as wav:
            for i in range(num_samples):
                t = i / sample_rate
                phase = t * freq * math.tau
                ch1 = multiplier * math.cos(phase)
                ch2 = multiplier * math.sin(phase)
                ch3 = multiplier * math.sin(2 * phase)

                wav.append_sample(ch1, ch2, ch3)


if __name__ == "__main__":
    main()
