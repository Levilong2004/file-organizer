#!/usr/bin/env python3
"""
文件整理助手 (File Organizer)

自动按文件类型整理指定目录中的文件，将它们移动到分类子文件夹中。
支持预览模式（--dry-run），安全无风险。
"""

import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

# 文件类型分类规则
CATEGORIES = {
    "图片": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "文档": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"},
    "视频": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "音频": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "压缩包": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "代码": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", ".go", ".rs", ".rb", ".php"},
    "安装包": {".exe", ".msi", ".dmg", ".apk", ".deb", ".rpm"},
    "字体": {".ttf", ".otf", ".woff", ".woff2"},
}


def get_category(filename: str) -> str:
    """根据文件扩展名返回分类名称。"""
    ext = Path(filename).suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "其他"


def organize(directory: Path, dry_run: bool = False, recursive: bool = False) -> dict:
    """
    整理目录中的文件。

    Args:
        directory: 要整理的目录
        dry_run: 仅预览，不实际移动
        recursive: 是否递归处理子目录

    Returns:
        统计信息字典
    """
    stats = {"moved": 0, "skipped": 0, "categories": {}}

    if recursive:
        files = [f for f in directory.rglob("*") if f.is_file()]
    else:
        files = [f for f in directory.iterdir() if f.is_file()]

    for file_path in files:
        # 跳过脚本自身和隐藏文件
        if file_path.name == Path(__file__).name or file_path.name.startswith("."):
            stats["skipped"] += 1
            continue

        category = get_category(file_path.name)
        target_dir = directory / category

        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        target_path = target_dir / file_path.name

        # 处理重名文件
        if target_path.exists() and target_path != file_path:
            stem = file_path.stem
            suffix = file_path.suffix
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        action = "移动" if not dry_run else "预览"
        print(f"[{action}] {file_path.name} -> {category}/")

        if not dry_run:
            shutil.move(str(file_path), str(target_path))

        stats["moved"] += 1
        stats["categories"][category] = stats["categories"].get(category, 0) + 1

    return stats


def print_stats(stats: dict, dry_run: bool) -> None:
    """打印整理统计信息。"""
    print("\n" + "=" * 40)
    mode = "预览" if dry_run else "整理"
    print(f"{mode}完成！")
    print(f"处理文件数: {stats['moved']}")
    if stats["skipped"]:
        print(f"跳过文件数: {stats['skipped']}")
    if stats["categories"]:
        print("\n分类统计:")
        for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count} 个文件")
    print("=" * 40)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="文件整理助手 - 按类型自动整理文件夹",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 整理当前目录
  %(prog)s Downloads                # 整理 Downloads 目录
  %(prog)s --dry-run                # 预览整理结果（不实际移动）
  %(prog)s --recursive              # 递归整理子目录
  %(prog)s Downloads --dry-run      # 预览 Downloads 目录的整理结果
        """,
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="要整理的目录路径（默认: 当前目录）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，只显示将执行的操作，不实际移动文件",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="递归处理子目录中的文件",
    )

    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"错误: 目录不存在 - {directory}", file=sys.stderr)
        sys.exit(1)
    if not directory.is_dir():
        print(f"错误: 不是一个目录 - {directory}", file=sys.stderr)
        sys.exit(1)

    mode_msg = "预览模式（不实际移动）" if args.dry_run else "整理模式"
    print(f"文件整理助手 - {mode_msg}")
    print(f"目标目录: {directory}")
    print("-" * 40)

    stats = organize(directory, dry_run=args.dry_run, recursive=args.recursive)
    print_stats(stats, args.dry_run)


if __name__ == "__main__":
    main()
