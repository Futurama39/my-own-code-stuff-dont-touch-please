import ctypes
import asyncio

ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
asyncio.sleep(15)
ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door closed", None, 0, None)