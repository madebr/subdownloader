#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 SubDownloader Developers - See COPYING - GPLv3
"""Create a standalone executable using PyInstaller"""

import collections
import configparser
import os
from pathlib import Path
import platform
import subprocess
import shutil
import stat
import sys

DISTRIBUTION_PATH = Path(__file__).resolve().parent
SUBDOWNLOADER_ROOT = DISTRIBUTION_PATH.parents[1]
PYINSTALLER_WD = SUBDOWNLOADER_ROOT / 'pyinstaller_wd'

PYINSTALLER_DIST_PATH = PYINSTALLER_WD / 'dist'
PYINSTALLER_WORK_PATH = PYINSTALLER_WD / 'build'

PYINSTALLER_SUBDOWNLOADER_STANDALONE_PATH = PYINSTALLER_DIST_PATH / 'subdownloader'


def pyinstaller_run(clean=True, debug=False):
    if clean:
        shutil.rmtree(PYINSTALLER_DIST_PATH, ignore_errors=True)
        shutil.rmtree(PYINSTALLER_WORK_PATH, ignore_errors=True)
    PYINSTALLER_DIST_PATH.mkdir(parents=True, exist_ok=True)
    PYINSTALLER_WORK_PATH.mkdir(parents=True, exist_ok=True)

    pyinstaller_config_write(PyConfig(bit64=sys.maxsize > 2**32))

    arguments = [
        sys.executable, '-m', 'PyInstaller',
        str(DISTRIBUTION_PATH / 'pyinstaller' / 'subdownloader.spec'), '--noconfirm',
        '--distpath', str(PYINSTALLER_DIST_PATH),
        '--workpath', str(PYINSTALLER_WORK_PATH),
    ]
    if debug:
        arguments += ['-d', 'all', ]

    if clean:
        arguments += ['--clean', ]

    subprocess.check_call(arguments)

    pyinstaller_fix_PyQt5(PYINSTALLER_DIST_PATH / 'subdownloader')

    pyinstaller_check()


PyConfig = collections.namedtuple('PyConfig', ('bit64', ))


def pyinstaller_config_read():
    metadata = configparser.ConfigParser()
    metadata.read(PYINSTALLER_WD / 'metadata.txt')
    cfg = PyConfig(bool(metadata['system.architecture']))
    print(cfg)
    return cfg


def pyinstaller_config_write(cfg):
    metadata = configparser.ConfigParser()
    metadata['system.architecture'] = {
        '64bit': cfg.bit64,
    }
    metadata.write(PYINSTALLER_WD / 'metadata.txt')
    print(cfg)
    return cfg


def pyinstaller_check():
    cfg = pyinstaller_config_read()
    assert cfg is not None

    if platform.system() == 'Windows':
        path_exe = PYINSTALLER_SUBDOWNLOADER_STANDALONE_PATH / 'subdownloader.exe'
    elif platform.system() == 'Linux':
        path_exe = PYINSTALLER_SUBDOWNLOADER_STANDALONE_PATH / 'subdownloader'
    else:
        raise RuntimeError('Unsupported platform: {}'.format(platform.system()))

    if not os.path.exists(path_exe):
        raise RuntimeError('Executable does not exist')

    if platform.system() == 'Linux':
        s = os.stat(path_exe)
        exec_flags = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
        if (s.st_mode & exec_flags) != exec_flags:
            raise RuntimeError('Executable has incorrect mode flags')
    if not os.path.exists(path_exe):
        raise RuntimeError('Executable does not exist')


def pyinstaller_fix_PyQt5(subdl_dist_path):
    qt5_bin_path = subdl_dist_path / 'PyQt5' / 'Qt' / 'bin'
    assert qt5_bin_path.exists()

    if platform.system() == 'Windows':
        for f in qt5_bin_path.iterdir():
            f.unlink()

        p = Path(subdl_dist_path)
        for f in p.iterdir():
            if f.is_file() and f.stem.startswith('Qt5') and f.suffix == '.dll':
                if f.stem not in ('Qt5Core', 'Qt5Gui', 'Qt5Widgets', ):
                    f.unlink()
                    continue
                f.rename(qt5_bin_path / f.name)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    clean_keep = parser.add_mutually_exclusive_group()
    clean_keep.add_argument('--keep', dest='clean', action='store_false',
                            help='Incremental build on current build.')
    clean_keep.add_argument('--clean', dest='clean', action='store_true',
                            help='Clean current build before rebuilding.')
    clean_keep.set_defaults(clean=True)
    ns = parser.parse_args()
    pyinstaller_run(clean=ns.clean, debug=ns.debug)


if __name__ == '__main__':
    sys.exit(main())
