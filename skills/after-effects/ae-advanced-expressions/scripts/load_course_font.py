"""Temporarily register the bundled OFL course font in this Windows session.

No administrator install or registry mutation. Check the AE font probe first;
this registration receipt alone does not prove the AE host recognized the font.
"""
import ctypes,json,os
from pathlib import Path
if os.name!='nt':raise OSError('Windows font registration helper; use the host font system on other platforms')
font=Path(__file__).resolve().parents[1]/'assets/fonts/DMSans-Bold.ttf'
if not font.is_file():raise FileNotFoundError(font)
gdi=ctypes.windll.gdi32;gdi.AddFontResourceExW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint,ctypes.c_void_p];gdi.AddFontResourceExW.restype=ctypes.c_int
count=gdi.AddFontResourceExW(str(font),0,None)
if count<1:raise RuntimeError('Windows did not register the supplied font')
ctypes.windll.user32.SendNotifyMessageW(ctypes.c_void_p(0xffff),0x001D,0,0)
print(json.dumps(dict(status='registered_windows_session_only',font=str(font),font_faces_registered=count,registry_modified=False,ae_availability='must_check_native_font_probe')))
