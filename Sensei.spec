# -*- mode: python -*-

block_cipher = None

options = [('v', None, 'OPTION'), ('W ignore', None, 'OPTION')]
a = Analysis(['Sensei.py'],
             pathex=['/Users/justinshenk/Projects/sensei'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pydoc', 'doctest'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('posture.png', 'posture.png', 'DATA')]
a.datas += [('meditate.png', 'meditate.png', 'DATA')]
a.datas += [('face.xml', 'face.xml', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          options,
          exclude_binaries=True,
          name='Sensei',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='meditate.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Sensei')
app = BUNDLE(coll,
             name='Sensei.app',
	     icon='meditate.icns',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True',
             'LSUIElement': '1',
             'LSBackgroundOnly': '1'
             }
             )
