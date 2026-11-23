"""Deja Power BI Desktop como única ventana interactiva en primer plano."""
import ctypes
import time

from pywinauto import Desktop

SW_MINIMIZE = 6
SW_RESTORE = 9
SW_SHOW = 5


def minimize_other_windows(exclude_titles=("Power BI Desktop",)):
    u = ctypes.windll.user32
    for w in Desktop(backend="uia").windows():
        try:
            title = w.window_text()
            cls = w.class_name()
            if cls.startswith("WindowsForms10") or any(t in title for t in exclude_titles):
                continue
            if cls not in ("Chrome_WidgetWin_1", "WinUIDesktopWin32WindowClass",
                           "CASCADIA_HOSTING_WINDOW_CLASS", "CEF-OSC-WIDGET"):
                continue
            if not w.is_visible():
                continue
            r = w.rectangle()
            if r.width() < 100 or r.height() < 100:
                continue
            u.ShowWindow(w.handle, SW_MINIMIZE)
            print("minimizada:", title[:60])
        except Exception:  # noqa: BLE001
            pass
    time.sleep(1.0)


def focus_powerbi():
    for w in Desktop(backend="uia").windows():
        try:
            if w.class_name().startswith("WindowsForms10"):
                if ctypes.windll.user32.IsIconic(w.handle):
                    ctypes.windll.user32.ShowWindow(w.handle, SW_RESTORE)
                w.set_focus()
                time.sleep(0.8)
                return w
        except Exception:  # noqa: BLE001
            pass
    raise RuntimeError("Power BI Desktop no encontrada")


if __name__ == "__main__":
    focus_powerbi()
    minimize_other_windows()
    focus_powerbi()
    print("listo")
