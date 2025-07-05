"""
应用程序启动器
用于确保在打包环境中正确设置工作目录
"""
import os
import sys
import logging
from pathlib import Path

def setup_environment():
    """设置应用程序环境"""
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='stray-words.log'  # 将日志写入文件，便于排查问题
    )
    logger = logging.getLogger(__name__)
    
    try:
        # 确定应用程序根目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的环境
            app_dir = Path(os.path.dirname(sys.executable))
            logger.debug(f"Running in packaged environment. App directory: {app_dir}")
            
            # 将src目录添加到Python路径
            if hasattr(sys, '_MEIPASS'):
                sys.path.insert(0, sys._MEIPASS)
                logger.debug(f"Added PyInstaller _MEIPASS to path: {sys._MEIPASS}")
        else:
            # 如果是开发环境
            app_dir = Path(__file__).resolve().parent.parent
            logger.debug(f"Running in development environment. App directory: {app_dir}")
            
            # 将src目录添加到Python路径
            src_dir = app_dir / "src"
            sys.path.insert(0, str(src_dir))
            logger.debug(f"Added src directory to path: {src_dir}")
        
        # 检查配置和资源目录是否存在
        config_dir = app_dir / "config"
        resource_dir = app_dir / "resource"
        
        logger.debug(f"Checking for config directory: {config_dir}")
        if not config_dir.exists():
            logger.error(f"Config directory not found: {config_dir}")
            print(f"错误: 未找到配置目录 {config_dir}")
            print("请确保 config 目录与应用程序在同一目录下")
            return False
        
        logger.debug(f"Checking for resource directory: {resource_dir}")
        if not resource_dir.exists():
            logger.error(f"Resource directory not found: {resource_dir}")
            print(f"错误: 未找到资源目录 {resource_dir}")
            print("请确保 resource 目录与应用程序在同一目录下")
            return False
        
        # 设置工作目录为应用程序根目录
        os.chdir(app_dir)
        logger.debug(f"Working directory set to: {os.getcwd()}")
        
        # 打印当前Python路径，便于调试
        logger.debug(f"Python path: {sys.path}")
        
        return True
    except Exception as e:
        logger.exception(f"Error in setup_environment: {e}")
        print(f"设置环境时出错: {e}")
        return False

if __name__ == "__main__":
    # 这个文件不应该直接运行
    print("这个文件不应该直接运行。请运行 main.py")