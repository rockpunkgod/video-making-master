import ctypes,json
u=ctypes.windll.user32;u.GetClassNameW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_int];u.GetDlgCtrlID.argtypes=[ctypes.c_void_p]
rows=[]
@ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)
def f(h,p):
 b=ctypes.create_unicode_buffer(256);u.GetClassNameW(h,b,256)
 if b.value in ['Edit','Button','ComboBox','ComboBoxEx32']:rows.append({'handle':h,'class':b.value,'id':u.GetDlgCtrlID(h)})
 return True
u.EnumChildWindows(1183932,f,0);print(json.dumps(rows,indent=2))
