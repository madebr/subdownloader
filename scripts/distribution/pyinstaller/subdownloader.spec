# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

spec_path = Path(SPECPATH).resolve()
subdownloader_root = spec_path.parents[2]

script = subdownloader_root / 'subdownloader' / 'client' / '__main__.py'

a = Analysis([script],
             hookspath=[spec_path / 'hooks'],
             # pathex=[subdownloader_root],
)

pyz = PYZ(a.pure,
          a.zipped_data
)

exe = EXE(pyz,
          a.scripts,
          icon=None,
          exclude_binaries=True,
          name='subdownloader',
          console=False,
)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               name='subdownloader',
)
