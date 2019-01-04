set PIP=C:\Python27\Lib\pyinstaller-1.5.1\
python %PIP%Makespec.py --onefile --upx --tk --noconsole ../src/main.py --name=Clone --icon=../resources/clone.ico
python %PIP%Build.py Clone.spec

python %PIP%Makespec.py --onefile --upx --tk --console ../src/main_cmd.py --name=CloneCmdLine --icon=../resources/cmdline.ico
python %PIP%Build.py CloneCmdLine.spec

PAUSE