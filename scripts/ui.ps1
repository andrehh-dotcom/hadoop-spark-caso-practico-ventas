Add-Type -AssemblyName System.Windows.Forms,System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, IntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
  public struct RECT { public int Left, Top, Right, Bottom; }
}
"@

function Get-PbiWindow {
    Get-Process PBIDesktop -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
}

function Focus-Pbi {
    $p = Get-PbiWindow
    if (-not $p) { return $false }
    [Win32]::ShowWindow($p.MainWindowHandle, 3) | Out-Null
    [Win32]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
    Start-Sleep -Milliseconds 500
    return $true
}

function Get-PbiRect {
    $p = Get-PbiWindow
    $r = New-Object Win32+RECT
    [Win32]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
    return $r
}

function Shot($path) {
    $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object Drawing.Bitmap $b.Width, $b.Height
    $g = [Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($b.Location, [Drawing.Point]::Empty, $b.Size)
    $bmp.Save($path, [Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    return $path
}

function ShotPbi($path) {
    $r = Get-PbiRect
    $w = $r.Right - $r.Left; $h = $r.Bottom - $r.Top
    $bmp = New-Object Drawing.Bitmap $w, $h
    $g = [Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.Left, $r.Top, 0, 0, (New-Object Drawing.Size $w, $h))
    $bmp.Save($path, [Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    return $path
}

function Click($x, $y) {
    [Win32]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 150
    [Win32]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    [Win32]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function DoubleClick($x, $y) {
    Click $x $y
    [Win32]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    [Win32]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Paste($text) {
    Set-Clipboard -Value $text
    Start-Sleep -Milliseconds 250
    [System.Windows.Forms.SendKeys]::SendWait("^v")
    Start-Sleep -Milliseconds 500
}

function Key($keys) {
    [System.Windows.Forms.SendKeys]::SendWait($keys)
    Start-Sleep -Milliseconds 500
}
