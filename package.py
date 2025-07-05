#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("开始打包 Stray Words 应用...")
    
    # 确保当前目录是项目根目录
    project_root = Path(__file__).resolve().parent
    os.chdir(project_root)
    
    # 创建输出目录
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # 清理旧的构建文件
    if dist_dir.exists():
        print("清理旧的 dist 目录...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        print("清理旧的 build 目录...")
        shutil.rmtree(build_dir)
    
    # 使用 PyInstaller 打包应用
    print("使用 PyInstaller 打包应用...")
    
    # 创建一个简单的打包命令，专注于解决模块导入问题
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=stray-words",
        "--onefile",
        "--noconsole",
        "--clean",
        "--paths=./src",  # 添加src目录到Python路径
        "--hidden-import=pystray",  # 确保包含pystray库
        "--hidden-import=PIL",  # 确保包含PIL库
        "--hidden-import=PIL._tkinter_finder",  # 确保包含PIL依赖
        "--hidden-import=PIL.Image",  # 确保包含PIL.Image
        "--hidden-import=PIL.ImageDraw",  # 确保包含PIL.ImageDraw
        "--hidden-import=PIL.ImageFont",  # 确保包含PIL.ImageFont
        "--hidden-import=pyperclip",  # 确保包含pyperclip
        "--hidden-import=yaml",  # 确保包含yaml
        "--hidden-import=sqlite3",  # 确保包含sqlite3
        "--hidden-import=service",
        "--hidden-import=service.config_loader",
        "--hidden-import=service.words_loader",
        "--hidden-import=service.wordbook_service",
        "--hidden-import=service.view_menu_service",
        "--hidden-import=service.dao",
        "--hidden-import=service.dao.wordbook_dao",
        "--hidden-import=service.dao.wordlist_dao",
        "--hidden-import=model",
        "--hidden-import=model.config",
        "--hidden-import=model.constants",
        "--hidden-import=model.sqlite",
        "--hidden-import=model.sqlite.base_model",
        "--hidden-import=model.sqlite.wordbook",
        "--hidden-import=model.sqlite.wordlist",
        "--hidden-import=app_platform",
        "--hidden-import=app_platform.windows",
        "--hidden-import=app_platform.macos",
        "--add-data=src;src",  # 将src目录添加到打包文件中
        "--add-data=wordlists;wordlists",  # 添加词表数据
        "main.py"
    ]
    
    # 执行 PyInstaller 命令
    try:
        subprocess.run(pyinstaller_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller 打包失败: {e}")
        return 1
    
    # 创建发布包目录结构
    release_dir = project_root / "release"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制可执行文件到发布目录
    exe_file = dist_dir / "stray-words.exe"
    if not exe_file.exists():
        print("错误：可执行文件未生成！")
        return 1
    
    shutil.copy(exe_file, release_dir)
    
    # 复制配置和资源目录
    print("复制配置和资源文件...")
    shutil.copytree(project_root / "config", release_dir / "config")
    shutil.copytree(project_root / "resource", release_dir / "resource")
    
    # 创建README文件
    with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write("""Stray Words 应用

使用说明：
1. 确保 config 和 resource 目录与可执行文件在同一目录下
2. 双击 stray-words.exe 运行应用

注意：请勿移动或删除 config 和 resource 目录，否则应用将无法正常工作。
""")
    
    print(f"打包完成！发布包位于: {release_dir.absolute()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())