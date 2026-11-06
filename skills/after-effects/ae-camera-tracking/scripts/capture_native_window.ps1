param([int]$ProcessId,[string]$OutputPath)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;using System.Runtime.InteropServices;
public class LabWindowCapture {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern IntPtr SetThreadDpiAwarenessContext(IntPtr context);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr dc,uint flags);
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
$rect=New-Object LabWindowCapture+RECT
[LabWindowCapture]::GetWindowRect($handle,[ref]$rect) | Out-Null
$bitmap=New-Object System.Drawing.Bitmap ($rect.Right-$rect.Left),($rect.Bottom-$rect.Top)
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
$dc=$graphics.GetHdc()
$printed=[LabWindowCapture]::PrintWindow($handle,$dc,2)
$graphics.ReleaseHdc($dc)
if(!$printed){throw 'Window capture failed; refusing to capture unrelated desktop content'}
$bitmap.Save($OutputPath)
$graphics.Dispose();$bitmap.Dispose()
Write-Output $OutputPath
Write-Output ([pscustomobject]@{Handle=$handle;Left=$rect.Left;Top=$rect.Top;Width=$bitmap.Width;Height=$bitmap.Height})
