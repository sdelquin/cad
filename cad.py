import logging
import os
import re
import shlex
import subprocess
from pathlib import Path

import coloredlogs
from jinja2 import Environment, FileSystemLoader


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


def pdf2png(source_path, target_path):
    cmd = f'convert {source_path} {target_path}'
    logger.info(cmd)
    subprocess.run(shlex.split(cmd), stderr=subprocess.DEVNULL)


def build_design_options(force_rewrite=False):
    desing_options = []
    for dirpath, _, filenames in os.walk('designs'):
        if 'render.png' in filenames:
            logger.info(f'Building design at {dirpath}')
            if 'drawing.pdf' not in filenames:
                logger.error(f'drawing.pdf not found at {dirpath}')
            else:
                if force_rewrite or 'drawing.png' not in filenames:
                    drawing_pdf = os.path.join(dirpath, 'drawing.pdf')
                    drawing_png = os.path.join(dirpath, 'drawing.png')
                    pdf2png(drawing_pdf, drawing_png)
            cleanpath = re.sub(r'^designs/?', '', dirpath)
            option = f'<option>{cleanpath}</option>'
            desing_options.append(option)
    return desing_options


def build():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('index.tmpl.html')
    p = Path('index.html')
    p.write_text(template.render(designs=build_design_options(True)))


build()
