#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Api-Finder 
"""

if __name__ == "__main__":
    try:
        from apifinder.apifinder import main
        main()
    except ImportError as e:
        try:
            from rich.console import Console
            from rich.panel import Panel
            console = Console()
            console.print(Panel(
                f"❌ [bold red]无法导入apifinder模块:[/bold red] {e}\n\n"
                "💡 [yellow]解决方案:[/yellow]\n"
                "• 请确保您在正确的目录中运行此脚本\n"
                "• 确保已安装所有依赖: [cyan]pip install -r requirements.txt[/cyan]",
                title="🚨 模块导入错误",
                border_style="red"
            ))
        except ImportError:
            # 如果连rich都无法导入，使用普通输出
            print(f"[错误] 无法导入apifinder模块: {e}")
            print("请确保您在正确的目录中运行此脚本，并且已安装所有依赖。")
            print("运行 'pip install -r requirements.txt' 安装依赖。")
    except Exception as e:
        try:
            from rich.console import Console
            from rich.panel import Panel
            console = Console()
            console.print(Panel(
                f"💥 [bold red]程序执行失败:[/bold red] {e}",
                title="🚨 运行时错误",
                border_style="red"
            ))
        except ImportError:
            print(f"[错误] 程序执行失败: {e}") 