# 文件整理助手 (File Organizer)

一个简单高效的命令行工具，自动按文件类型整理文件夹中的文件，告别杂乱的下载目录。

## 功能特性

- 自动识别文件类型并分类到对应子文件夹
- 支持 **预览模式**（`--dry-run`），先看结果再执行，安全无风险
- 支持 **递归整理**（`--recursive`）子目录
- 自动处理重名文件（添加数字后缀）
- 纯 Python 标准库，零依赖

## 支持的分类

| 分类 | 扩展名 |
|------|--------|
| 图片 | jpg, png, gif, svg, webp, bmp ... |
| 文档 | pdf, doc, docx, txt, md, xlsx, csv ... |
| 视频 | mp4, avi, mkv, mov, webm ... |
| 音频 | mp3, wav, flac, aac ... |
| 压缩包 | zip, rar, 7z, tar, gz ... |
| 代码 | py, js, html, css, json, java, cpp ... |
| 安装包 | exe, msi, dmg, apk ... |
| 字体 | ttf, otf, woff ... |
| 其他 | 未匹配的文件 |

## 环境要求

- Python 3.6+

## 使用方法

```bash
# 整理当前目录
python organize.py

# 整理指定目录（如下载文件夹）
python organize.py ~/Downloads

# 预览整理结果（不实际移动文件）
python organize.py ~/Downloads --dry-run

# 递归整理子目录
python organize.py --recursive

# 查看帮助
python organize.py --help
```

## 使用示例

整理前：
```
Downloads/
├── report.pdf
├── photo.jpg
├── song.mp3
└── setup.exe
```

整理后：
```
Downloads/
├── 文档/
│   └── report.pdf
├── 图片/
│   └── photo.jpg
├── 音频/
│   └── song.mp3
└── 安装包/
    └── setup.exe
```

## 建议

1. 首次使用某个目录时，先加 `--dry-run` 预览
2. 定期整理下载文件夹，保持桌面整洁
3. 可将脚本加入系统 PATH，随时随地调用
