"""Explicit cold-open of a caller-specified lab project, then the guarded native runner.
Never kill/restart an existing Premiere instance or open its recent projects.
"""
import argparse
import csv
import ctypes
import io
import json
import subprocess
import time
from pathlib import Path
from launch_adobe import launch
from run_pr import execute

def existing_processes():
    result=subprocess.run(['tasklist','/FI','IMAGENAME eq Adobe Premiere Pro.exe','/FO','CSV','/NH'],capture_output=True,check=True)
    return [row for row in csv.reader(io.StringIO(result.stdout.decode(errors='replace'))) if row and row[0].lower()=='adobe premiere pro.exe']

def wait_project(process,project,timeout=35):
    u=ctypes.windll.user32;expected=str(Path(project).resolve()).lower()
    u.GetWindowThreadProcessId.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulong)];u.GetWindowTextW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_int]
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if process.poll() is not None:raise RuntimeError('Started Premiere process exited before opening the requested project: '+str(process.returncode))
        found=[]
        @ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)
        def inspect(handle,param):
            owner=ctypes.c_ulong();u.GetWindowThreadProcessId(handle,ctypes.byref(owner))
            if owner.value==process.pid:
                title=ctypes.create_unicode_buffer(1024);u.GetWindowTextW(handle,title,1024)
                if expected in title.value.lower() and u.IsWindowEnabled(handle):found.append(handle)
            return True
        u.EnumWindows(inspect,0)
        if found:return found[0]
        time.sleep(.25)
    raise TimeoutError('No enabled native window for the exact requested project; inspect this same live process, do not restart it')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('jsx');ap.add_argument('--pr',required=True);ap.add_argument('--ae',required=True);ap.add_argument('--project',required=True);ap.add_argument('--out',required=True);ap.add_argument('--timeout',type=int,default=150);a=ap.parse_args()
    process=None
    if not existing_processes():
        process,info=launch(a.pr,[a.project]);print(json.dumps({'cold_launch':info}),flush=True);wait_project(process,a.project)
    else:print('Existing Premiere instance preserved; native runner will verify the exact project.',flush=True)
    result=execute(a.jsx,a.ae,a.project,a.out,a.timeout)
    if process is not None:result['launched_process_exit_at_completion']=process.poll()
    print(json.dumps(result,indent=2,ensure_ascii=True));raise SystemExit(0 if result.get('status')=='executed' else 2)
