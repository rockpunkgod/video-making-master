"""Launch Adobe with missing Windows system variables restored in the child only."""
import argparse
import os
import subprocess
from pathlib import Path

def child_environment():
    env=dict(os.environ);added=[]
    if os.name=='nt':
        import ctypes
        userenv=ctypes.WinDLL('userenv',use_last_error=True)
        userenv.CreateEnvironmentBlock.argtypes=[ctypes.POINTER(ctypes.c_void_p),ctypes.c_void_p,ctypes.c_int]
        userenv.CreateEnvironmentBlock.restype=ctypes.c_int
        userenv.DestroyEnvironmentBlock.argtypes=[ctypes.c_void_p]
        block=ctypes.c_void_p()
        if not userenv.CreateEnvironmentBlock(ctypes.byref(block),None,False):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            cursor=block.value
            while True:
                row=ctypes.wstring_at(cursor)
                if not row:break
                cursor+=len(row.encode('utf-16-le'))+2
                if row.startswith('='):continue
                key,value=row.split('=',1);key=key.upper()
                if key not in env:env[key]=value;added.append(key)
        finally:userenv.DestroyEnvironmentBlock(block)
    removed={key:env.pop(key) for key in ['LANG','LC_ALL','LC_CTYPE'] if key in env}
    return env,{'added_missing_system_variable_names':sorted(added),'removed_child_locale_overrides':removed,'system_settings_changed':False}

def launch(executable,args):
    executable=Path(executable).resolve();env,info=child_environment()
    # Premiere adds an extended-path prefix internally; preserve native separators.
    arguments=[str(Path(arg).resolve()) if Path(arg).is_file() else arg for arg in args]
    flags=0
    if os.name=='nt':flags=subprocess.DETACHED_PROCESS|subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.CREATE_BREAKAWAY_FROM_JOB
    p=subprocess.Popen([str(executable),*arguments],cwd=executable.parent,env=env,creationflags=flags,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)
    return p,dict(pid=p.pid,**info)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('executable',type=Path);ap.add_argument('args',nargs='*');a=ap.parse_args()
    p,info=launch(a.executable,a.args);print(info)
