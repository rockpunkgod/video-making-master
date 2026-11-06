import ctypes,json,argparse
ap=argparse.ArgumentParser();ap.add_argument('--pid',type=int,required=True);a=ap.parse_args()
u=ctypes.windll.user32
u.GetWindowThreadProcessId.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulong)];u.GetWindowTextW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_int];u.GetClassNameW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_int]
rows=[]
@ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)
def collect(h,p):
 owner=ctypes.c_ulong();u.GetWindowThreadProcessId(h,ctypes.byref(owner))
 if owner.value==a.pid:
  title=ctypes.create_unicode_buffer(1000);cl=ctypes.create_unicode_buffer(256);u.GetWindowTextW(h,title,1000);u.GetClassNameW(h,cl,256);rows.append({'handle':h,'title':title.value,'class':cl.value,'visible':bool(u.IsWindowVisible(h)),'enabled':bool(u.IsWindowEnabled(h))})
 return True
u.EnumWindows(collect,0)
print(json.dumps([r for r in rows if r['visible']],ensure_ascii=False,indent=2))
