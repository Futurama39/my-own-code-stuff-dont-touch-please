import ctypes
import time

ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
time.sleep(15)
ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door closed", None, 0, None)