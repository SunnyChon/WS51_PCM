# WS51_PCM
PCM sample playback code for the WS51F6240 MCU.

# Software requirements
* FFmpeg
* Python 3
* Keil µVision C51 or SDCC

# Hardware requirements
* WS51F6240 MCU
* Programmer for WS51 series MCU
* A speaker or buzzer

# Hardware setup
Use either a single transistor amplifier or a amplifier IC as shown in the picture:
<img width="1745" height="547" alt="螢幕擷取畫面 2026-07-09 001327" src="https://github.com/user-attachments/assets/1f60ee01-e840-4482-91b8-3549fe201ead" />

# Software usage
Use the command below to generate a C code base on the audio file
<br>
* <code>python3 PCM2C.py [audio file path] [playback mode(0 = once , 1 = loop , default = 0)] [output file path]</code>
<br>
The absolute maximum PCM data size is 16000B - 489B = 15511B (2.5851s / 6KHz). Limited to 15480B for safety. (2.58s / 6kHz).
