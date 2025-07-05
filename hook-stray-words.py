
# PyInstaller hook file
import os
import sys
import site
from pathlib import Path

# 添加src目录到Python路径
src_dir = Path(__file__).resolve().parent / "src"
site.addsitedir(str(src_dir))
