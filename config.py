#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
管理Api-Finder的默认设置和配置
"""
# 这里默认请求有类，但是没有设置
# 默认请求有类
DEFAULT_CONFIG = {
    # 请求相关
    "timeout": 10,
    "delay": 0.5,
    
    # 输出相关
    "silent_mode": False,
    "verbose_mode": False,
    
    # UA相关
    "default_app": "common",
    "random_ua": False,
    
    # 代理相关
    "proxy_api_url": "https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=5",
    "proxy_count": 5,
    
    # 过滤相关
    "filter_extensions": [".png", ".jpg", ".css", ".webp", ".apk", ".exe", ".dmg", ".ico", ".gif", ".svg"],
    
    # 输出格式
    "supported_formats": [".txt", ".json", ".csv"],
    
    # 版本信息
    "version": "0.3.1",
    "description": "Api-Finder - 从前端文件查找API端点",
    "github_url": "https://github.com/jujubooom/Api-Finder"
}

# 颜色配置
COLORS = {
    "red": "\033[0;31;40m",
    "green": "\033[0;32;40m", 
    "yellow": "\033[0;33;40m",
    "blue": "\033[0;34;40m",
    "cyan": "\033[0;36;40m",
    "reset": "\033[0m"
}

# 统计信息
STATS_TEMPLATE = {
    "total_urls": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "api_endpoints": 0
} 