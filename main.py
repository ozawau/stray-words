#!/usr/bin/env python3
import sys
import os

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    if sys.platform == 'darwin':
        from platform.macos import main
    else:
        from platform.windows import main
    
    main()