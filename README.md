About the wav_file_writer module
================================

The wav_file_writer module provides a minimalistic interface for writing single- or
multi-channel WAV files, with either integer or floating-point sample values.

Performance
-----------

The current implementation is not optimized for speed, as samples are added one by
one. For many applications, this is not a problem.

In the future, an 'append_numpy_samples' method will be added to support applications
where performance considerations are important.

Background information
----------------------

Information on the WAV file format can be found here:

http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
