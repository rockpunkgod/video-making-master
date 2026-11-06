"""One bounded physical click on an already observed, process-owned Adobe dialog."""
import argparse,ctypes,time
ap=argparse.ArgumentParser();ap.add_argument('--pid',type=int,required=True);ap.add_argument('--window',type=int,required=True);ap.add_argument('--x',type=int,required=True);ap.add_argument('--y',type=int,required=True);ap.add_argument('--raise-owned-window',action='store_true');a=ap.parse_args()
u=ctypes.windll.user32
class Point(ctypes.Structure):_fields_=[('x',ctypes.c_long),('y',ctypes.c_long)]
u.SetThreadDpiAwarenessContext(ctypes.c_void_p(-4));u.WindowFromPoint.argtypes=[Point];u.WindowFromPoint.restype=ctypes.c_void_p;u.GetForegroundWindow.restype=ctypes.c_void_p
owner=ctypes.c_ulong();u.GetWindowThreadProcessId(a.window,ctypes.byref(owner))
if owner.value!=a.pid:raise ValueError('Wrong window owner')
old=Point();u.GetPhysicalCursorPos(ctypes.byref(old));foreground=u.GetForegroundWindow()
was_topmost=bool(u.GetWindowLongW(a.window,-20)&8)
try:
 if a.raise_owned_window:u.SetWindowPos(a.window,ctypes.c_void_p(-1),0,0,0,0,0x13)
 u.SetForegroundWindow(a.window);time.sleep(.2);p=Point(a.x,a.y);target=u.WindowFromPoint(p);u.GetWindowThreadProcessId(ctypes.c_void_p(target),ctypes.byref(owner))
 if owner.value!=a.pid:raise RuntimeError('Observed dialog is covered; no click sent')
 u.SetPhysicalCursorPos(a.x,a.y);time.sleep(.15);u.mouse_event(2,0,0,0,0);u.mouse_event(4,0,0,0,0);time.sleep(.25);print('Click sent; inspect native result')
finally:
 if a.raise_owned_window and not was_topmost:u.SetWindowPos(a.window,ctypes.c_void_p(-2),0,0,0,0,0x13)
 u.SetPhysicalCursorPos(old.x,old.y);u.SetForegroundWindow(ctypes.c_void_p(foreground))
