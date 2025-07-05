#!/usr/bin/env python3
import sys
import os
import subprocess

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from service.config_loader import load_config
from service.words_loader import load_words

if __name__ == "__main__":
    # 加载配置和词表
    load_config()
    load_words()

    # 判断是否需要后台运行
    daemon_mode = any(arg in ("--daemon", "-d") for arg in sys.argv[1:])

    # 根据平台调用对应的实现
    if sys.platform == 'darwin':
        from app_platform.macos import main
        main(daemon_mode=daemon_mode)
    else:
        from app_platform.windows import main
        main(daemon_mode=daemon_mode)