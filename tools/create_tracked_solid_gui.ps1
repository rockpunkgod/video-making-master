param([int]$ProcessId,[int]$X,[int]$Y,[int]$EndX=-1,[int]$EndY=-1,[string]$Points='',[switch]$SelectOnly,[int]$ContextX=-1,[int]$ContextY=-1)
# Tracker hit-testing depends on the real cursor; restore foreground and pointer after this bounded native interaction.
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;using System.Text;using System.Runtime.InteropServices;
public class LabTrackerPhysicalAction {
 [StructLayout(LayoutKind.Sequential)]public struct POINT{public int X;public int Y;}
 [StructLayout(LayoutKind.Sequential)]public struct RECT{public int L;public int T;public int R;public int B;}
 [DllImport("user32.dll")]public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr c);
 [DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")]public static extern bool GetPhysicalCursorPos(out POINT p);
 [DllImport("user32.dll")]public static extern bool SetPhysicalCursorPos(int x,int y);
 [DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")]public static extern bool SetWindowPos(IntPtr h,IntPtr after,int x,int y,int w,int he,uint flags);
 [DllImport("user32.dll")]public static extern IntPtr WindowFromPoint(POINT p);
 [DllImport("user32.dll")]public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern int GetWindowText(IntPtr h,StringBuilder text,int max);
 [DllImport("user32.dll")]public static extern void mouse_event(uint flags,uint x,uint y,uint data,UIntPtr extra);
 [DllImport("user32.dll")]public static extern void keybd_event(byte key,byte scan,uint flags,UIntPtr extra);
}
'@
[LabTrackerPhysicalAction]::SetThreadDpiAwarenessContext([IntPtr](-4)) | Out-Null
$process=Get-Process -Id $ProcessId
$condition=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::ProcessIdProperty),$ProcessId
$wins=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,$condition)
$win=$wins | Where-Object {$_.Current.ClassName -like 'AE_CApplication*'} | Select-Object -First 1
if(!$win){throw 'No native AE window'}
$handle=[IntPtr]$win.Current.NativeWindowHandle
$title=New-Object System.Text.StringBuilder 1000;[LabTrackerPhysicalAction]::GetWindowText($handle,$title,1000) | Out-Null
if($title.ToString() -notlike '*tracking-attempt.aep*'){throw ('Expected the lab tracking attempt, not another project: '+$title.ToString())}
$oldForeground=[LabTrackerPhysicalAction]::GetForegroundWindow();$oldPointer=New-Object LabTrackerPhysicalAction+POINT
[LabTrackerPhysicalAction]::GetPhysicalCursorPos([ref]$oldPointer) | Out-Null
$rect=New-Object LabTrackerPhysicalAction+RECT;[LabTrackerPhysicalAction]::GetWindowRect($handle,[ref]$rect) | Out-Null
try{
 [LabTrackerPhysicalAction]::SetForegroundWindow($handle) | Out-Null
 # Foreground activation and z-order updates may be asynchronous after native rendering.
 Start-Sleep -Milliseconds 200
 $point=New-Object LabTrackerPhysicalAction+POINT;$point.X=$rect.L+$X;$point.Y=$rect.T+$Y
 $target=[LabTrackerPhysicalAction]::WindowFromPoint($point);[uint32]$owner=0;[LabTrackerPhysicalAction]::GetWindowThreadProcessId($target,[ref]$owner) | Out-Null
 if($owner -ne $ProcessId){throw ('AE control is covered or outside the physical display; no physical click sent. point='+$point.X+','+$point.Y+' owner='+$owner+' foreground='+[LabTrackerPhysicalAction]::GetForegroundWindow())}
 if($Points){
  $pairs=$Points.Split(';') | ForEach-Object {if($_ -notmatch '^(\d+),(\d+)$'){throw 'Invalid observed point coordinates'};[pscustomobject]@{X=[int]$Matches[1];Y=[int]$Matches[2]}}
  if($pairs.Count -lt 3){throw 'At least three observed points required'}
  for($idx=0;$idx -lt $pairs.Count;$idx++){
   if($idx -eq 1){[LabTrackerPhysicalAction]::keybd_event(16,0,0,[UIntPtr]::Zero)}
   [LabTrackerPhysicalAction]::SetPhysicalCursorPos($rect.L+$pairs[$idx].X,$rect.T+$pairs[$idx].Y) | Out-Null
   Start-Sleep -Milliseconds 90
   [LabTrackerPhysicalAction]::mouse_event(2,0,0,0,[UIntPtr]::Zero);[LabTrackerPhysicalAction]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
  }
  [LabTrackerPhysicalAction]::keybd_event(16,0,2,[UIntPtr]::Zero)
  if($SelectOnly){Write-Output 'Observed tracking points selected; inspect the native target before creation.';return}
  $centerX=[int](($pairs | Measure-Object X -Average).Average);$centerY=[int](($pairs | Measure-Object Y -Average).Average)
  [LabTrackerPhysicalAction]::SetPhysicalCursorPos($rect.L+$centerX,$rect.T+$centerY) | Out-Null
 }else{
 [LabTrackerPhysicalAction]::SetPhysicalCursorPos($point.X,$point.Y) | Out-Null
 [LabTrackerPhysicalAction]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 if($EndX -ge 0 -and $EndY -ge 0){
  Start-Sleep -Milliseconds 120
  [LabTrackerPhysicalAction]::SetPhysicalCursorPos($rect.L+$EndX,$rect.T+$EndY) | Out-Null
  Start-Sleep -Milliseconds 120
 }
 [LabTrackerPhysicalAction]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 if($EndX -ge 0 -and $EndY -ge 0){
  [LabTrackerPhysicalAction]::SetPhysicalCursorPos($rect.L+[int](($X+$EndX)/2),$rect.T+[int](($Y+$EndY)/2)) | Out-Null
 }
 }
 if($ContextX -ge 0 -and $ContextY -ge 0){[LabTrackerPhysicalAction]::SetPhysicalCursorPos($rect.L+$ContextX,$rect.T+$ContextY) | Out-Null}
 Start-Sleep -Milliseconds 180
 [LabTrackerPhysicalAction]::mouse_event(8,0,0,0,[UIntPtr]::Zero);[LabTrackerPhysicalAction]::mouse_event(16,0,0,0,[UIntPtr]::Zero)
 $deadline=[DateTime]::UtcNow.AddSeconds(3);$menu=$null
 do{
  $all=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
  $menu=$all | Where-Object {$_.Current.ClassName -eq '#32768' -and $_.Current.ProcessId -eq $ProcessId} | Select-Object -First 1
 }while(!$menu -and [DateTime]::UtcNow -lt $deadline)
 if(!$menu){throw 'Tracker context menu did not appear'}
 $item=$null
 foreach($knownName in @('创建实底','创建实底和摄像机')){
  $nameCondition=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::NameProperty),$knownName
  $item=$menu.FindFirst([System.Windows.Automation.TreeScope]::Descendants,$nameCondition)
  if($item){break}
 }
 if(!$item -or !$item.Current.IsEnabled){$menuItems=$menu.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition);$menuItems | ForEach-Object {$_.Current.Name};throw 'Observed create-solid action is unavailable'}
 $bounds=$item.Current.BoundingRectangle
 [LabTrackerPhysicalAction]::SetPhysicalCursorPos([int]($bounds.X+$bounds.Width/2),[int]($bounds.Y+$bounds.Height/2)) | Out-Null
 [LabTrackerPhysicalAction]::mouse_event(2,0,0,0,[UIntPtr]::Zero);[LabTrackerPhysicalAction]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 Write-Output 'Native tracker menu selected with the real pointer; verify project layer creation.'
}finally{
 [LabTrackerPhysicalAction]::keybd_event(16,0,2,[UIntPtr]::Zero)
 [LabTrackerPhysicalAction]::SetPhysicalCursorPos($oldPointer.X,$oldPointer.Y) | Out-Null
 [LabTrackerPhysicalAction]::SetForegroundWindow($oldForeground) | Out-Null
}
