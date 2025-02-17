# -*- mode: python -*-
a = Analysis(['Aplikace.py'],
             pathex=['C:\\Users\\strobladm\\Desktop\\NAO_aplikace\\Python_Zdrojovy_kod'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Aplikace.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
