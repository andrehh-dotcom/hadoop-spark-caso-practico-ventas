"""Captura las ventanas del entorno para el informe documental."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

EV = r'C:\hadoop-spark-cluster\evidencias'
os.makedirs(EV, exist_ok=True)


def find_window(*needles):
    for w in Desktop(backend='uia').windows():
        try:
            if not w.is_visible():
                continue
            t = w.window_text()
            if all(n.lower() in t.lower() for n in needles):
                return w
        except Exception:
            pass
    return None


def focus(w):
    if w is None:
        return False
    try:
        w.set_focus()
        time.sleep(0.9)
        return True
    except Exception:
        return False


def shot(name):
    p = os.path.join(EV, name + '.png')
    ImageGrab.grab().save(p)
    print('capturado:', p, os.path.getsize(p), flush=True)


def capture(title_needles, name):
    w = find_window(*title_needles)
    ttl = w.window_text().encode('ascii', 'replace').decode() if w else None
    print('buscando', title_needles, '->', ttl, flush=True)
    if focus(w):
        shot(name)
    return w


# 1. VS Code con docker-compose.yml
capture(('Visual Studio Code',), '01_vscode_compose')

# 2. Docker Desktop
capture(('Docker Desktop',), '02_docker_desktop')

# 3-6. Edge: cuatro pestañas
capture(('hadoop-spark-cluster', 'Explorador de archivos'), '00_explorador')
edge = capture(('Namenode information',), '03_namenode')
if edge:
    for key, name in ((2, '04_yarn'), (3, '05_spark'), (4, '06_dashboard_web')):
        focus(edge)
        send_keys('^%d' % key)
        time.sleep(2.2)
        shot(name)

# 7. Power BI Desktop con el informe terminado
capture(('Dashboard_Ventas',), '07_powerbi_final')

print('FIN DE CAPTURAS', flush=True)
