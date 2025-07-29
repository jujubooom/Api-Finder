#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出管理模块 (Output Manager Module)
负责处理Api-Finder的所有输出功能，包括终端输出和文件输出
"""

import os
import json
import time
from datetime import datetime
from urllib.parse import urlparse
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.rule import Rule
from rich.markdown import Markdown
from .i18n import i18n


class OutputManager:
    """
    使用Rich库的输出管理器类，提供美观的终端输出和多种文件输出格式
    
    Attributes:
        silent_mode (bool): 静默模式，只输出发现的API端点
        verbose_mode (bool): 详细输出模式
        output_file (str): 输出文件路径
        results (list): 结果列表
        stats (dict): 统计信息
        console (Console): Rich console对象
        results_table (Table): 结果表格
    """
    
    def __init__(self, silent_mode, verbose_mode=False, output_file=None):
        """
        初始化输出管理器
        
        Args:
            silent_mode (bool): 静默模式
            verbose_mode (bool): 详细输出模式
            output_file (str): 输出文件路径
        """
        self.silent_mode = silent_mode
        self.verbose_mode = verbose_mode
        self.output_file = output_file
        self.console = Console()
        self.results = []
        self.stats = {
            "total_urls": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "api_endpoints": 0,
            "start_time": datetime.now()
        }
        self.results_table = Table(title="🔍 Discovered API Endpoints", border_style="green")
        self.results_table.add_column("📍 URL", style="cyan", no_wrap=False)
        self.results_table.add_column("📄 Source", style="yellow", max_width=30)
        self.results_table.add_column("⏰ Time", style="dim", max_width=10)
    
    def print_info(self, text):
        """打印信息"""
        if not self.silent_mode:
            self.console.print(text)
    
    def print_verbose(self, text):
        """打印详细信息"""
        if self.verbose_mode and not self.silent_mode:
            self.console.print(f"[dim][DEBUG][/dim] {text}")
    
    def print_url(self, url, source="", IsSuccess=True):
        """打印发现的URL"""
        if self.silent_mode:
            # 静默模式：输出可点击链接（如果终端支持）
            clickable_url = self._make_clickable_url(url)
            self.console.print(clickable_url, highlight=False)
        else:
            # 添加到结果表格
            source_display = source.split('/')[-1] if source else "unknown"
            time_display = datetime.now().strftime("%H:%M:%S")
            
            # 创建可点击的URL用于表格
            clickable_url = self._make_clickable_url(url)
            self.results_table.add_row(clickable_url, source_display, time_display)
            
            # 终端输出也使用可点击链接
            if source:
                self.console.print(f"[green bold]✓[/green bold] {clickable_url} [dim](from: {source_display})[/dim]")
            else:
                self.console.print(f"[green bold]✓[/green bold] {clickable_url}")
        
        if IsSuccess:
        # 保存结果
            self.results.append({
                "url": url,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
            self.stats["api_endpoints"] += 1
        else:
            pass
    
    def _make_clickable_url(self, url):
        """创建可点击的URL（支持的终端中）"""
        # 检查终端是否支持超链接
        if hasattr(self.console, 'file') and hasattr(self.console.file, 'isatty'):
            if self.console.file.isatty():
                # 使用ANSI转义序列创建可点击链接
                # 格式：\033]8;;URL\033\\显示文本\033]8;;\033\\
                display_text = url
                if len(url) > 80:
                    display_text = url[:40] + "..." + url[-37:]
                
                clickable = f"\033]8;;{url}\033\\{display_text}\033]8;;\033\\"
                return Text.from_ansi(clickable)
        
        # 如果不支持或检测失败，返回普通的彩色文本
        return Text(url, style="cyan underline")
    
    def print_error(self, text):
        """打印错误信息"""
        if not self.silent_mode:
            self.console.print(f"[red bold]✗[/red bold] {text}")
    
    def print_warning(self, text):
        """打印警告信息"""
        if not self.silent_mode:
            self.console.print(f"[yellow bold]⚠[/yellow bold] {text}")
    
    def print_success(self, text):
        """打印成功信息"""
        if not self.silent_mode:
            self.console.print(f"[green bold]✓[/green bold] {text}")

    def print_title(self, url, title):
        """打印成功请求的页面标题"""
        if not self.silent_mode:
            text = Text()
            text.append("📄 ", style="green")
            text.append(f"{title}", style="yellow")
            text.append(" → ", style="dim")
            text.append(f"{url}", style="cyan dim")
            self.console.print(text)

    def print_proxy_mode(self, proxies):
        """输出使用的代理模式"""
        if not self.silent_mode:
            if proxies:
                proxy_table = Table(title="🌐 Proxy Configuration", border_style="blue")
                proxy_table.add_column("Type", style="cyan")
                proxy_table.add_column("Address", style="green")
                
                if isinstance(proxies, list):
                    for proxy in proxies:
                        proxy_table.add_row("SOCKS5", proxy)
                elif isinstance(proxies, dict):
                    for protocol, proxy in proxies.items():
                        proxy_table.add_row(protocol.upper(), proxy)
                
                self.console.print(proxy_table)
            else:
                self.console.print("[yellow]💻 Direct connection (no proxy)[/yellow]")
            self.console.print(Rule(style="dim"))

    def print_stats(self):
        """打印统计信息"""
        if not self.silent_mode:
            # 计算扫描时间
            scan_duration = datetime.now() - self.stats["start_time"]
            duration_str = f"{scan_duration.total_seconds():.1f}s"
            
            # 创建统计表格
            stats_table = Table(title="📊 Scan Statistics", border_style="cyan")
            stats_table.add_column("Item", style="yellow bold")
            stats_table.add_column("Value", style="green bold", justify="right")
            
            stats_table.add_row("🎯 Total URLs", str(self.stats['total_urls']))
            stats_table.add_row("✅ Successful Requests", str(self.stats['successful_requests']))
            stats_table.add_row("❌ Failed Requests", str(self.stats['failed_requests']))
            stats_table.add_row("🔍 API Endpoints Found", str(self.stats['api_endpoints']))
            stats_table.add_row("⏱️ Scan Duration", duration_str)
            
            # 计算成功率
            total_requests = self.stats['successful_requests'] + self.stats['failed_requests']
            if total_requests > 0:
                success_rate = (self.stats['successful_requests'] / total_requests) * 100
                stats_table.add_row("📈 Success Rate", f"{success_rate:.1f}%")
            
            self.console.print(Rule(style="dim"))
            self.console.print(stats_table)
            
            # 如果找到了API端点，显示结果表格
            if self.stats['api_endpoints'] > 0 and not self.silent_mode:
                self.console.print(Rule(style="dim"))
                self.console.print(self.results_table)
    
    def create_progress(self, total_tasks=None):
        """创建进度条"""
        if self.silent_mode:
            return None
        
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            expand=True
        )

    def print_scan_start(self, url=None, batch=False):
        """统一输出扫描开始信息"""
        if batch:
            self.print_info(f"🎯 [bold blue]Starting batch scan...[/bold blue]")
        elif url:
            self.print_info(f"🎯 [bold blue]Starting scan target:[/bold blue] [green]{url}[/green]")
        else:
            self.print_info(f"🎯 [bold blue]Starting scan...[/bold blue]")

    def print_scan_end(self, found_count=None, batch=False):
        """统一输出扫描结束信息"""
        if batch:
            self.print_info(f"🎉 [bold green]Batch scan completed![/bold green]")
        elif found_count is not None:
            if found_count > 0:
                self.print_info(f"🎉 [bold green]Scan completed! Found {found_count} API endpoints.[/bold green]")
            else:
                self.print_info(f"✅ [bold yellow]Scan completed. No API endpoints found.[/bold yellow]")
        else:
            self.print_info(f"🎉 [bold green]Scan completed![/bold green]")

    def print_json_stats(self):
        """统一输出JSON响应统计"""
        if self.stats.get("json_responses", 0) > 0:
            self.console.print(f"[bold green]共发现 {self.stats['json_responses']} 个JSON响应[/bold green]")

