@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 开始打包应用...
python package.py

echo.
echo 如果打包成功，可执行文件将位于 release 目录中
echo 请确保在分发时，config 和 resource 目录与 stray-words.exe 位于同一目录下
pause