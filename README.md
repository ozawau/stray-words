# Stray Words

一个用于学习单词的桌面应用程序，支持多语言单词本和自定义显示方式。

## 功能特点

- 支持多语言单词本
- 系统托盘显示单词
- 自定义单词显示格式
- 单词记忆状态标记
- 支持Windows和macOS平台

## 开发环境设置

1. 克隆仓库
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行应用：
   ```
   python main.py
   ```

## 项目结构

- `config/`: 配置文件目录
- `resource/`: 资源文件目录，包含SQLite数据库
- `src/`: 源代码目录
- `wordlists/`: 词表文件目录

## 打包为可执行文件

### Windows

1. 运行打包脚本：
   ```
   build.bat
   ```
   或者手动执行：
   ```
   pip install -r requirements.txt
   python build.py
   ```

2. 打包完成后，可执行文件将位于`release`目录中

### 分发和使用

打包后的应用程序需要以下文件结构：

```
stray-words.exe
config/
  └── config.yaml
resource/
  └── stray-words.db
  └── sql/
      ├── wordbook.sql
      └── wordlist.sql
```

**注意**：确保`config`和`resource`目录与可执行文件位于同一目录下，否则应用将无法正常工作。

## 配置文件

配置文件位于`config/config.yaml`，可以自定义以下设置：

- `wordbook_id`: 当前选择的单词本ID
- `view`: 单词显示格式配置
- `click_action`: 点击托盘图标的默认操作

## 许可证

[许可证信息]
