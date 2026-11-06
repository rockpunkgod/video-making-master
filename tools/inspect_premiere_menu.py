import ctypes,json
u=ctypes.windll.user32;hwnd=1575204
u.GetMenu.restype=ctypes.c_void_p;u.GetSubMenu.restype=ctypes.c_void_p;u.GetSubMenu.argtypes=[ctypes.c_void_p,ctypes.c_int];u.GetMenuItemCount.argtypes=[ctypes.c_void_p];u.GetMenuStringW.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_wchar_p,ctypes.c_int,ctypes.c_uint];u.GetMenuItemID.argtypes=[ctypes.c_void_p,ctypes.c_int];u.GetClassNameW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_int]
b=ctypes.create_unicode_buffer(256);u.GetClassNameW(hwnd,b,256);print('class',b.value);m=u.GetMenu(hwnd);print('menu',m)
def items(m,depth=0):
 for i in range(u.GetMenuItemCount(m)):
  b=ctypes.create_unicode_buffer(512);u.GetMenuStringW(m,i,b,512,0x400)
  if depth==0 and not b.value.startswith('窗口'):continue
  sub=u.GetSubMenu(m,i);print(' '*depth,repr(b.value),u.GetMenuItemID(m,i),'sub',sub)
  if sub and depth<2:items(sub,depth+1)
if m:items(m)
