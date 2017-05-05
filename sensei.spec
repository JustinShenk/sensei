# -*- mode: python -*-

block_cipher = None


a = Analysis(['sensei.py'],
             pathex=['/Users/justinshenk/Projects/sensei'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('posture.png','posture.png','DATA')]
a.datas += [('exit.png','exit.png','DATA')]
a.datas += [('face.xml','face.xml','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Sensei',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
	  icon='meditate.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Sensei')
app = BUNDLE(coll,
             name='Sensei.app',
             icon='meditate.icns',
             bundle_identifier=None)
