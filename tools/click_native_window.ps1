param([int]$ProcessId,[int]$X,[int]$Y,[ValidateSet('Left','Right')][string]$Button='Left',[ValidateRange(-1200,1200)][int]$WheelDelta=0,[long]$WindowHandle=0)
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
}
'@
[LabOwnedWindowClick]::SetThreadDpiAwarenessContext([IntPtr](-4)) | Out-Null
$condition=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::ProcessIdProperty),$ProcessId
$wins=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,$condition)
$win=$wins | Where-Object {$_.Current.ClassName -like 'AE_CApplication*'} | Select-Object -First 1
if(!$win){throw 'No matching native Adobe window'}
$handle=[IntPtr]$win.Current.NativeWindowHandle
if($WindowHandle){
 $handle=[IntPtr]$WindowHandle;[uint32]$windowOwner=0
 [LabOwnedWindowClick]::GetWindowThreadProcessId($handle,[ref]$windowOwner) | Out-Null
 if($windowOwner -ne $ProcessId){throw 'Requested dialog belongs to another process'}
}
$rect=New-Object LabOwnedWindowClick+RECT
[LabOwnedWindowClick]::GetWindowRect($handle,[ref]$rect) | Out-Null
if($X -lt 0 -or $Y -lt 0 -or $X -ge ($rect.R-$rect.L) -or $Y -ge ($rect.B-$rect.T)){throw 'Coordinates outside observed native window'}
$screenX=$rect.L+$X;$screenY=$rect.T+$Y;$target=$handle
for($depth=0;$depth -lt 12;$depth++){
 $point=New-Object LabOwnedWindowClick+POINT;$point.X=$screenX;$point.Y=$screenY
 [LabOwnedWindowClick]::ScreenToClient($target,[ref]$point) | Out-Null
 $child=[LabOwnedWindowClick]::ChildWindowFromPointEx($target,$point,7)
 if($child -eq [IntPtr]::Zero -or $child -eq $target){break}
 $target=$child
}
[uint32]$owner=0;[LabOwnedWindowClick]::GetWindowThreadProcessId($target,[ref]$owner) | Out-Null
if($owner -ne $ProcessId){throw 'Unexpected target owner'}
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
}
Write-Output 'Mouse messages posted to the observed Adobe control; verify the application result.'
