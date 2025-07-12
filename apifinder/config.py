#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 (Configuration File)
管理Api-Finder的默认设置和配置 (Manage Api-Finder default settings and configuration)
"""

# 默认配置 (Default configuration)
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
    
    # 代理相关 (Proxy related),采用scdn.io的代理，免费的，而且速度很快
    "proxy_api_url": "https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=5",
    "proxy_count": 5,
    
    # 过滤相关 (Filter related)
    "filter_extensions": [".png", ".jpg", ".css", ".webp", ".apk", ".exe", ".dmg", ".ico", ".gif", ".svg"],
    
    # 更新相关 (Update related)
    "remote_rules_url": "https://raw.githubusercontent.com/jujubooom/Api-Finder/refs/heads/main/config/rules.yaml",
    "update_interval_days": 3,
    
    # 输出格式 (Output formats)
    "supported_formats": [".txt", ".json", ".csv"],
    
    # 版本信息 (Version information)
    "version": "0.3.1",
    "description": "Api-Finder - Find API endpoints from frontend files",
    "github_url": "https://github.com/jujubooom/Api-Finder"
}

# 配置文件结束 