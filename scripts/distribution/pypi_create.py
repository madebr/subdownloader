#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 SubDownloader Developers - See COPYING - GPLv3

from pathlib import Path
import subprocess
import shutil
import sys


def pypi_create():
    project_dir = Path(__file__).resolve().parents[2]

    sys.path += [str(project_dir)]

    import subdownloader.project

    setup_file = project_dir / 'setup.py'

    shutil.rmtree(project_dir / 'build', ignore_errors=True)

    subprocess.check_call([sys.executable, str(setup_file), 'clean'], cwd=project_dir)

    subprocess.check_call([sys.executable, str(setup_file), 'pytest'], cwd=project_dir)

    subprocess.check_call([sys.executable, str(setup_file), 'bdist'], cwd=project_dir)
    subprocess.check_call([sys.executable, str(setup_file), 'bdist_wheel'], cwd=project_dir)
    subprocess.check_call([sys.executable, str(setup_file), 'sdist'], cwd=project_dir)

    print()
    print('Created distributable files for version {}'.format(subdownloader.project.PROJECT_VERSION_FULL_STR))
    print('Upload them to pypi using "twine upload FILES" (after manual inspection)')
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.parse_args()
    pypi_create()


if __name__ == '__main__':
    sys.exit(main())
