#!/usr/bin/env python3
import sys
import os

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from service.config_loader import load_config
from service.words_loader import load_words

if __name__ == "__main__":
    # 加载配置和词表
    load_config()
    load_words()
    
    # 根据平台调用对应的实现
    if sys.platform == 'darwin':
        from platform.macos import main
    else:
        from platform.windows import main
    
    main()