param([int]$ProcessId,[int]$X,[int]$Y,[ValidateSet('Left','Right')][string]$Button='Left',[ValidateRange(-1200,1200)][int]$WheelDelta=0,[long]$WindowHandle=0,[int]$DragToX=-1,[int]$DragToY=-1,[switch]$DoubleClick)
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;using System.Runtime.InteropServices;
public class LabOwnedWindowClick {
 [StructLayout(LayoutKind.Sequential)] public struct POINT {public int X;public int Y;}
 [StructLayout(LayoutKind.Sequential)] public struct RECT {public int L;public int T;public int R;public int B;}
 [DllImport("user32.dll")]public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr c);
 [DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")]public static extern IntPtr ChildWindowFromPointEx(IntPtr h,POINT p,uint flags);
 [DllImport("user32.dll")]public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll")]public static extern bool ScreenToClient(IntPtr h,ref POINT p);
 [DllImport("user32.dll")]public static extern bool PostMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")]public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")]public static extern bool GetCursorPos(out POINT p);
 [DllImport("user32.dll")]public static extern IntPtr WindowFromPoint(POINT p);
 [DllImport("user32.dll")]public static extern void mouse_event(uint flags,uint dx,uint dy,uint data,UIntPtr extra);
}
'@
[LabOwnedWindowClick]::SetThreadDpiAwarenessContext([IntPtr](-4)) | Out-Null
$condition=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::ProcessIdProperty),$ProcessId
$wins=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,$condition)
$win=$wins | Where-Object {$_.Current.ClassName -like 'AE_CApplication*'} | Select-Object -First 1
if(!$win -and !$WindowHandle){throw 'No matching native Adobe window'}
$handle=if($win){[IntPtr]$win.Current.NativeWindowHandle}else{[IntPtr]::Zero}
if($WindowHandle){
 $handle=[IntPtr]$WindowHandle;[uint32]$windowOwner=0
 [LabOwnedWindowClick]::GetWindowThreadProcessId($handle,[ref]$windowOwner) | Out-Null
 if($windowOwner -ne $ProcessId){throw 'Requested dialog belongs to another process'}
}
$rect=New-Object LabOwnedWindowClick+RECT
[LabOwnedWindowClick]::GetWindowRect($handle,[ref]$rect) | Out-Null
if($X -lt 0 -or $Y -lt 0 -or $X -ge ($rect.R-$rect.L) -or $Y -ge ($rect.B-$rect.T)){throw 'Coordinates outside observed native window'}
$screenX=$rect.L+$X;$screenY=$rect.T+$Y;$target=$handle
if(($DragToX -ge 0) -or ($DragToY -ge 0)){
 if($DragToX -lt 0 -or $DragToY -lt 0 -or $DragToX -ge ($rect.R-$rect.L) -or $DragToY -ge ($rect.B-$rect.T) -or $Button -ne 'Left' -or $WheelDelta){throw 'Invalid owned-window drag'}
}
for($depth=0;$depth -lt 12;$depth++){
 $point=New-Object LabOwnedWindowClick+POINT;$point.X=$screenX;$point.Y=$screenY
 [LabOwnedWindowClick]::ScreenToClient($target,[ref]$point) | Out-Null
 $child=[LabOwnedWindowClick]::ChildWindowFromPointEx($target,$point,7)
 if($child -eq [IntPtr]::Zero -or $child -eq $target){break}
 $target=$child
}
[uint32]$owner=0;[LabOwnedWindowClick]::GetWindowThreadProcessId($target,[ref]$owner) | Out-Null
if($owner -ne $ProcessId){throw 'Unexpected target owner'}
if($DragToX -ge 0){
 $priorCursor=New-Object LabOwnedWindowClick+POINT
 [LabOwnedWindowClick]::GetCursorPos([ref]$priorCursor) | Out-Null
 [LabOwnedWindowClick]::SetForegroundWindow($handle) | Out-Null
 Start-Sleep -Milliseconds 100
 try{
  # Check the full path before pressing; another application's window must not receive the drag.
  for($step=0;$step -le 20;$step++){
   $dragPoint=New-Object LabOwnedWindowClick+POINT
   $dragPoint.X=$screenX+[int](($DragToX-$X)*$step/20);$dragPoint.Y=$screenY+[int](($DragToY-$Y)*$step/20)
   [uint32]$dragOwner=0
   [LabOwnedWindowClick]::GetWindowThreadProcessId([LabOwnedWindowClick]::WindowFromPoint($dragPoint),[ref]$dragOwner) | Out-Null
   if($dragOwner -ne $ProcessId){throw 'Drag path is covered by another application'}
  }
  [LabOwnedWindowClick]::SetCursorPos($screenX,$screenY) | Out-Null
  Start-Sleep -Milliseconds 300
  [LabOwnedWindowClick]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
  for($step=1;$step -le 20;$step++){
   [LabOwnedWindowClick]::SetCursorPos(($screenX+[int](($DragToX-$X)*$step/20)),($screenY+[int](($DragToY-$Y)*$step/20))) | Out-Null
   Start-Sleep -Milliseconds 100
  }
  # Let the native control consume the last pointer update before releasing capture.
  Start-Sleep -Milliseconds 1000
 }finally{
  [LabOwnedWindowClick]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
  [LabOwnedWindowClick]::SetCursorPos($priorCursor.X,$priorCursor.Y) | Out-Null
 }
 Write-Output 'Dragged inside the observed Adobe window; verify the application result.'
 return
}
$point=New-Object LabOwnedWindowClick+POINT;$point.X=$screenX;$point.Y=$screenY
[LabOwnedWindowClick]::ScreenToClient($target,[ref]$point) | Out-Null
$pos=[IntPtr](($point.Y -shl 16) -bor ($point.X -band 0xffff))
[LabOwnedWindowClick]::PostMessage($target,0x200,[IntPtr]0,$pos) | Out-Null
if($WheelDelta){
 $screenPos=[IntPtr](($screenY -shl 16) -bor ($screenX -band 0xffff))
 [LabOwnedWindowClick]::PostMessage($target,0x20A,[IntPtr]($WheelDelta -shl 16),$screenPos) | Out-Null
 Write-Output 'Wheel message posted to the observed Adobe control; verify the application result.'
 return
}
if($Button -eq 'Right'){
 [LabOwnedWindowClick]::PostMessage($target,0x204,[IntPtr]2,$pos) | Out-Null
 [LabOwnedWindowClick]::PostMessage($target,0x205,[IntPtr]0,$pos) | Out-Null
 $screenPos=[IntPtr](($screenY -shl 16) -bor ($screenX -band 0xffff))
 [LabOwnedWindowClick]::PostMessage($target,0x7B,$target,$screenPos) | Out-Null
}else{
 [LabOwnedWindowClick]::PostMessage($target,0x201,[IntPtr]1,$pos) | Out-Null
 [LabOwnedWindowClick]::PostMessage($target,0x202,[IntPtr]0,$pos) | Out-Null
 if($DoubleClick){
  [LabOwnedWindowClick]::PostMessage($target,0x203,[IntPtr]1,$pos) | Out-Null
  [LabOwnedWindowClick]::PostMessage($target,0x202,[IntPtr]0,$pos) | Out-Null
 }
}
Write-Output 'Mouse messages posted to the observed Adobe control; verify the application result.'
