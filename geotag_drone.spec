# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)
block_cipher = None


a = Analysis(['geotag_drone.py'],
             pathex=['D:\\to_compile\\v2.0'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('geotag_drone.ico', 'D:\\to_compile\\v2.0\\geotag_drone.ico',  'DATA'),
           ('image.png','D:\\to_compile\\v2.0\\image.png','DATA'),
           ('inovadrone.png','D:\\to_compile\\v2.0\\inovadrone.png','DATA'),
           ('innovadrone.png','D:\\to_compile\\v2.0\\innovadrone.png','DATA'),
           ('salt','D:\\to_compile\\v2.0\\salt','DATA')
           ]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='geotag_drone',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='geotag_drone.ico')
