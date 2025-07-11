#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 (Configuration File)
管理Api-Finder的默认设置和配置 (Manage Api-Finder default settings and configuration)
"""
# 这里默认请求有类，但是没有设置 (Default request class, but not set)
# 默认请求有类 (Default request class)
DEFAULT_CONFIG = {
    # 请求相关 (Request related)
    "timeout": 10,
    "delay": 0.5,
    
    # 输出相关 (Output related)
    "silent_mode": False,
    "verbose_mode": False,
    
    # UA相关 (User-Agent related)
    "default_app": "common",
    "random_ua": False,
    
    # 代理相关 (Proxy related)
    "proxy_api_url": "https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=5",
    "proxy_count": 5,
    
    # 过滤相关 (Filter related)
    "filter_extensions": [".png", ".jpg", ".css", ".webp", ".apk", ".exe", ".dmg", ".ico", ".gif", ".svg"],
    
    # 输出格式 (Output formats)
    "supported_formats": [".txt", ".json", ".csv"],
    
    # 版本信息 (Version information)
    "version": "0.3.1",
    "description": "Api-Finder - Find API endpoints from frontend files",
    "github_url": "https://github.com/jujubooom/Api-Finder"
}

# 颜色配置 (Color configuration)
COLORS = {
    "red": "\033[0;31;40m",
    "green": "\033[0;32;40m", 
    "yellow": "\033[0;33;40m",
    "blue": "\033[0;34;40m",
    "cyan": "\033[0;36;40m",
    "reset": "\033[0m"
}

# 统计信息 (Statistics template)
STATS_TEMPLATE = {
    "total_urls": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "api_endpoints": 0
} 