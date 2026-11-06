param([int]$ProcessId,[string]$OutputPath,[long]$WindowHandle=0)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;using System.Runtime.InteropServices;
public class LabWindowCapture {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr context);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr dc,uint flags);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 public struct RECT { public int Left,Top,Right,Bottom; }
}
'@
[LabWindowCapture]::SetProcessDPIAware() | Out-Null
[LabWindowCapture]::SetThreadDpiAwarenessContext([IntPtr](-4)) | Out-Null
$process=Get-Process -Id $ProcessId
$condition=New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::ProcessIdProperty),$ProcessId
$windows=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,$condition)
$window=$windows | Where-Object {$_.Current.ClassName -like 'AE_CApplication*'} | Select-Object -First 1
$handle=$process.MainWindowHandle
if($window){$handle=[IntPtr]$window.Current.NativeWindowHandle}
if($WindowHandle){$handle=[IntPtr]$WindowHandle;[uint32]$owner=0;[LabWindowCapture]::GetWindowThreadProcessId($handle,[ref]$owner) | Out-Null;if($owner -ne $ProcessId){throw 'Requested window belongs to a different process'}}
$rect=New-Object LabWindowCapture+RECT
[LabWindowCapture]::GetWindowRect($handle,[ref]$rect) | Out-Null
$bitmap=New-Object System.Drawing.Bitmap ($rect.Right-$rect.Left),($rect.Bottom-$rect.Top)
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
$dc=$graphics.GetHdc()
$printed=[LabWindowCapture]::PrintWindow($handle,$dc,2)
$graphics.ReleaseHdc($dc)
if(!$printed){throw 'Window capture failed; refusing to capture unrelated desktop content'}
$bitmap.Save($OutputPath)
$width=$bitmap.Width;$height=$bitmap.Height
$graphics.Dispose();$bitmap.Dispose()
Write-Output $OutputPath
Write-Output ([pscustomobject]@{Handle=$handle;Left=$rect.Left;Top=$rect.Top;Width=$width;Height=$height})
