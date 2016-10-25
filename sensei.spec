# -*- mode: python -*-

block_cipher = None


a = Analysis(['sensei.py'],
             pathex=['/Users/justinshenk/sensei'],
             binaries=None,
             datas=[('emoticon.png','/Users/justinshenk/sensei/emoticon.png')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sensei',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='sensei.app',
             icon=None,
             bundle_identifier=None)
