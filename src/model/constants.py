import os
import sys
from pathlib import Path

# Determine project root based on the script's location
try:
    # 检查是否是PyInstaller打包的环境
    if getattr(sys, 'frozen', False):
        # 如果是打包后的环境，使用可执行文件所在目录作为基准
        SCRIPT_DIR = Path(os.path.dirname(sys.executable))
        PROJECT_ROOT = SCRIPT_DIR
    else:
        # 如果是开发环境，使用原来的逻辑
        SCRIPT_DIR = Path(__file__).resolve().parent
        PROJECT_ROOT = SCRIPT_DIR.parent.parent
except NameError:
    # Fallback for interactive environments or when __file__ is not defined
    SCRIPT_DIR = Path.cwd()
    PROJECT_ROOT = SCRIPT_DIR

WORDLISTS_DIR = PROJECT_ROOT / "wordlists"