"""Launch Adobe with the Windows user's native locale; do not inherit CLI-only C.UTF-8 overrides."""
import argparse
import os
import subprocess
from pathlib import Path

def launch(executable,args):
    executable=Path(executable).resolve();env=dict(os.environ)
    removed={key:env.pop(key) for key in ['LANG','LC_ALL','LC_CTYPE'] if key in env}
    # Premiere adds an extended-path prefix internally; preserve native separators.
    arguments=[str(Path(arg).resolve()) if Path(arg).is_file() else arg for arg in args]
    flags=0
    if os.name=='nt':flags=subprocess.DETACHED_PROCESS|subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.CREATE_BREAKAWAY_FROM_JOB
    p=subprocess.Popen([str(executable),*arguments],cwd=executable.parent,env=env,creationflags=flags,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)
    return p,{'pid':p.pid,'removed_child_locale_overrides':removed,'system_settings_changed':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('executable',type=Path);ap.add_argument('args',nargs='*');a=ap.parse_args()
    p,info=launch(a.executable,a.args);print(info)
