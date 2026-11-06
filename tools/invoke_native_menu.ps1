param([int]$ProcessId,[string]$ItemName)
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;using System.Runtime.InteropServices;
public class LabObservedMenuAction {
 [StructLayout(LayoutKind.Sequential)]public struct POINT{public int X;public int Y;}
 [DllImport("user32.dll")]public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr c);
 [DllImport("user32.dll")]public static extern bool ScreenToClient(IntPtr h,ref POINT p);
 [DllImport("user32.dll")]public static extern IntPtr SendMessageTimeout(IntPtr h,uint m,IntPtr w,IntPtr l,uint flags,uint timeout,out IntPtr result);
}
'@
[LabObservedMenuAction]::SetThreadDpiAwarenessContext([IntPtr](-4)) | Out-Null
$wins=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$menu=$wins | Where-Object {$_.Current.ClassName -eq '#32768' -and $_.Current.ProcessId -eq $ProcessId} | Select-Object -First 1
if(!$menu){throw 'Expected native menu is not open'}
$cond=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::NameProperty),$ItemName
$item=$menu.FindFirst([System.Windows.Automation.TreeScope]::Descendants,$cond)
if(!$item -or !$item.Current.IsEnabled){throw 'Observed menu item is unavailable'}
$r=$item.Current.BoundingRectangle
$p=New-Object LabObservedMenuAction+POINT;$p.X=[int]($r.X+$r.Width/2);$p.Y=[int]($r.Y+$r.Height/2)
$h=[IntPtr]$menu.Current.NativeWindowHandle
[LabObservedMenuAction]::ScreenToClient($h,[ref]$p) | Out-Null
$pos=[IntPtr](($p.Y -shl 16) -bor ($p.X -band 0xffff));$reply=[IntPtr]::Zero
foreach($event in @(@(0x200,0),@(0x201,1),@(0x202,0))){
 $sent=[LabObservedMenuAction]::SendMessageTimeout($h,$event[0],[IntPtr]$event[1],$pos,2,3000,[ref]$reply)
 if($sent -eq [IntPtr]::Zero){throw 'Native menu did not respond; verify state before any retry'}
}
Write-Output 'Observed native menu item selected; native project result still requires inspection.'
