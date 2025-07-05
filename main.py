#!/usr/bin/env python3
import sys
import os
import subprocess
import logging
import traceback

# 配置日志
try:
    # 动态确定 logs 目录
    from pathlib import Path
    log_dir = Path(__file__).resolve().parent / "logs"
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "stray-words.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=str(log_file)  # 日志写入 logs 目录
    )
    logger = logging.getLogger(__name__)
    logger.debug("Starting application...")
except Exception as e:
    print(f"无法配置日志: {e}")

try:
    # 将 src 目录添加到 Python 路径
    # 检查是否是打包后的环境
    if getattr(sys, 'frozen', False):
        # 如果是打包后的环境，将src目录添加到路径
        # PyInstaller创建临时文件夹tmp_，将路径存储在_MEIPASS中
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(sys.executable)))
        sys.path.insert(0, base_path)
        logger.debug(f"Running in packaged environment. Base path: {base_path}")
        
        # 添加src目录到Python路径
        src_path = os.path.join(base_path, 'src')
        if os.path.exists(src_path):
            sys.path.insert(0, src_path)
            logger.debug(f"Added src directory to path: {src_path}")
        
        # 在打包环境中，确保当前工作目录是可执行文件所在目录
        exe_dir = os.path.dirname(sys.executable)
        os.chdir(exe_dir)
        logger.debug(f"Changed working directory to: {exe_dir}")
    else:
        # 如果是开发环境，使用原来的逻辑
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.insert(0, src_path)
        logger.debug(f"Running in development environment. Src path: {src_path}")

    # 打印当前Python路径，便于调试
    logger.debug(f"Python path: {sys.path}")
    logger.debug(f"Current working directory: {os.getcwd()}")
    
    # 检查配置和资源目录是否存在
    config_dir = os.path.join(os.getcwd(), "config")
    resource_dir = os.path.join(os.getcwd(), "resource")
    
    logger.debug(f"Checking for config directory: {config_dir}")
    if not os.path.exists(config_dir):
        logger.error(f"Config directory not found: {config_dir}")
        print(f"错误: 未找到配置目录 {config_dir}")
        print("请确保 config 目录与应用程序在同一目录下")
        sys.exit(1)
    
    logger.debug(f"Checking for resource directory: {resource_dir}")
    if not os.path.exists(resource_dir):
        logger.error(f"Resource directory not found: {resource_dir}")
        print(f"错误: 未找到资源目录 {resource_dir}")
        print("请确保 resource 目录与应用程序在同一目录下")
        sys.exit(1)

    # 尝试直接导入模块
    try:
        # 尝试直接从src导入
        sys.path.insert(0, os.path.join(os.getcwd(), "src"))
        from src.service.config_loader import load_config
        from src.service.words_loader import load_words
        logger.debug("Successfully imported required modules from src package")
    except ImportError as e:
        logger.warning(f"Failed to import from src package: {e}")
        # 尝试不使用src前缀导入
        try:
            from service.config_loader import load_config
            from service.words_loader import load_words
            logger.debug("Successfully imported required modules without src prefix")
        except ImportError as e:
            logger.error(f"Failed to import required modules: {e}")
            logger.error(f"Python path: {sys.path}")
            print(f"导入错误: {e}")
            print(f"Python路径: {sys.path}")
            sys.exit(1)
except Exception as e:
    if 'logger' in locals():
        logger.exception(f"Unhandled exception during startup: {e}")
    print(f"启动时发生错误: {e}")
    print(traceback.format_exc())
    sys.exit(1)

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