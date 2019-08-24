#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 SubDownloader Developers - See COPYING - GPLv3
"""Create a windows setup executable using NSIS"""

from pathlib import Path
import subprocess
import sys

DISTRIBUTION_PATH = Path(__file__).resolve().parent
NSIS_TEMPLATE_PATH = DISTRIBUTION_PATH / 'subdownloader.nsi.in'

sys.path.append(DISTRIBUTION_PATH)

from pyinstaller_create import SUBDOWNLOADER_ROOT, PYINSTALLER_SUBDOWNLOADER_STANDALONE_PATH, \
    pyinstaller_config_read, pyinstaller_check, PYINSTALLER_WORK_PATH

sys.path.append(str(SUBDOWNLOADER_ROOT))

import subdownloader.project


def version_tuple_to_long(t):
    return (t[0] << 24) | (t[1] << 16) | (t[2])


def nsis_run(outputpath=None):
    if outputpath is None:
        outputpath = Path()
    pyinstaller_check()

    pycfg = pyinstaller_config_read()

    nsis_script = NSIS_TEMPLATE_PATH.read_text() % {
        'license_file': str(SUBDOWNLOADER_ROOT / 'COPYING'),
        'name': subdownloader.project.PROJECT_TITLE,
        'version': subdownloader.project.PROJECT_VERSION_FULL_STR,
        'version_major': subdownloader.project.PROJECT_VERSION[0],
        'version_minor': subdownloader.project.PROJECT_VERSION[1],
        'version_long': hex(version_tuple_to_long(subdownloader.project.PROJECT_VERSION)),
        'publisher': subdownloader.project.PROJECT_AUTHOR_COLLECTIVE,
        'contact': subdownloader.project.WEBSITE_ISSUES,
        'updates': subdownloader.project.WEBSITE_RELEASES,
        'url': subdownloader.project.WEBSITE_MAIN,
        'exe_base': 'subdownloader.exe',
        'exe_dir': str(PYINSTALLER_SUBDOWNLOADER_STANDALONE_PATH),
        'is_64_bit_01': '1' if pycfg.bit64 else '0',
    }
    nsis_script_path = PYINSTALLER_WORK_PATH / 'subdownloader.nsi'
    nsis_script_path.write_text(nsis_script)

    subprocess.check_call(['makensis', '-NOCONFIG', '-NOCD', str(nsis_script_path), ], cwd=outputpath)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputdir', metavar='OUTPUTDIR', dest='outputpath', type=Path, default=Path(),
                        help='Target directory of the build')
    ns = parser.parse_args()
    nsis_run(outputpath=ns.outputpath)


if __name__ == '__main__':
    sys.exit(main())
