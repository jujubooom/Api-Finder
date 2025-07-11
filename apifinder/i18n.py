#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化模块 (Internationalization Module)
管理Api-Finder的英文界面文本
输出管理
"""

import os
import json
from typing import Dict, Any

class I18nManager:
    """
    国际化管理器 (Internationalization Manager)
    用于管理英文界面文本和消息
    """
    
    def __init__(self):
        """
        初始化国际化管理器，默认使用英文
        """
        self.messages = self._load_messages()
    
    def _load_messages(self) -> Dict[str, Any]:
        """
        加载英文消息 (Load English messages)
        
        Returns:
            Dict[str, Any]: 英文消息字典
        """
        messages = {
            # Command line arguments (命令行参数)
            'arg_url_help': 'Target website URL',
            'arg_cookie_help': 'Website Cookie for authentication',
            'arg_proxy_help': 'Proxy address, use "0" for auto proxy pool, supports socks5 and http',
            'arg_silent_help': 'Silent mode, only output discovered API endpoints',
            'arg_output_help': 'Output file path (supports .txt, .json, .csv formats, default: no output)',
            'arg_timeout_help': 'Request timeout (default: 10 seconds)',
            'arg_delay_help': 'Request interval (default: 0.5 seconds)',
            'arg_verbose_help': 'Verbose output mode',
            'arg_random_help': 'Random User-Agent',
            'arg_app_help': 'Device User-Agent, default: common browser, weixin: WeChat, phone: mobile',
            
            # Output messages (输出消息)
            'scan_start': 'Starting API endpoint scan...',
            'scan_complete': 'Scan completed',
            'proxy_mode': 'Proxy mode used:',
            'stats_title': 'Scan Statistics:',
            'stats_total_urls': 'Total URLs',
            'stats_successful_requests': 'Successful Requests',
            'stats_failed_requests': 'Failed Requests', 
            'stats_api_endpoints': 'API Endpoints Found',
            'results_saved': 'Results saved to:',
            'save_failed': 'Failed to save results:',
            
            # Error messages (错误消息)
            'proxy_fetch_failed': 'Failed to fetch proxy list',
            'request_failed': 'Request failed',
            'invalid_url': 'Invalid URL',
            'connection_error': 'Connection error',
            
            # Success messages (成功消息)
            'url_found': 'URL found',
            'discovered_from': 'Discovered from:',
            
            # File output messages (文件输出消息)
            'output_header': 'API Endpoint Scan Results',
            'output_target': 'Target URL',
            'output_scan_time': 'Scan Time',
            'output_endpoints_found': 'Endpoints Found',
            
            # Version and description (版本和描述)
            'version': '0.3.1',
            'description': 'Api-Finder - Find API endpoints from frontend files',
            'github_url': 'https://github.com/jujubooom/Api-Finder'
        }
        
        return messages
    
    def get(self, key: str, default: str = None) -> str:
        """
        获取英文文本 (Get English text)
        
        Args:
            key (str): 消息键 (Message key)
            default (str): 默认值 (Default value)
            
        Returns:
            str: 英文文本 (English text)
        """
        return self.messages.get(key, default or key)

# 全局国际化管理器实例 (Global i18n manager instance)
i18n = I18nManager() 