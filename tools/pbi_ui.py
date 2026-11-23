"""Helper mínimo para automatizar Power BI Desktop vía UIA (pywinauto)."""
from __future__ import annotations

import time

from pywinauto import Desktop

MAIN_CLASS_PREFIX = "WindowsForms10"


def desktop():
    return Desktop(backend="uia")


def main_window(timeout: float = 20):
    """Devuelve la ventana principal de Power BI Desktop."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        for w in desktop().windows():
            try:
                txt = w.window_text()
                cls = w.class_name()
                if cls.startswith(MAIN_CLASS_PREFIX) and (
                    txt.endswith("Power BI Desktop") or txt.endswith(".pbix")
                    or "Power BI" in txt or txt in (
                        "laboratorio_bigdata", "Dashboard_Ventas")
                ):
                    return w
            except Exception:  # noqa: BLE001
                pass
        time.sleep(0.5)
    raise RuntimeError("No se encontró la ventana de Power BI Desktop")


def descendants(win, **filters):
    """descendants() con filtros cómodos sobre element_info."""
    out = []
    for el in win.descendants(**filters):
        out.append(el)
    return out


def find(win, name=None, auto_id=None, control_type=None, contains=False,
         timeout: float = 10, visible_only=True):
    """Busca un control por nombre / automation id / tipo."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = []
        for el in win.descendants():
            try:
                info = el.element_info
                nm = info.name or ""
                aid = info.automation_id or ""
                ct = info.control_type or ""
                if name is not None:
                    ok = (name in nm) if contains else (name == nm)
                    if not ok:
                        continue
                if auto_id is not None and aid != auto_id:
                    continue
                if control_type is not None and ct != control_type:
                    continue
                if visible_only and not el.is_visible():
                    continue
                matches.append(el)
            except Exception:  # noqa: BLE001
                pass
        if matches:
            return matches[0]
        time.sleep(0.4)
    raise LookupError(
        f"No encontrado: name={name!r} aid={auto_id!r} type={control_type!r} "
        f"contains={contains}"
    )


def click(el):
    el.click_input()
    time.sleep(0.3)


def write(el, text: str):
    el.click_input()
    el.type_keys("^a")
    el.type_keys(text, with_spaces=True, pause=0.01)
    time.sleep(0.2)


def dump(win, root=None, depth: int = 8, max_lines: int = 300):
    counter = [0]
    node = root or win

    def walk(el, level):
        if counter[0] >= max_lines or level > depth:
            return
        try:
            i = el.element_info
            print(
                "  " * level
                + f"[{i.control_type}] {(i.name or '')[:95]!r} "
                + f"cls={(i.class_name or '')[:55]!r} aid={(i.automation_id or '')!r}"
            )
            counter[0] += 1
        except Exception:  # noqa: BLE001
            return
        try:
            for child in el.children():
                walk(child, level + 1)
        except Exception:  # noqa: BLE001
            pass

    walk(node, 0)
