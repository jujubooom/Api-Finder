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

from pyexpat.errors import messages


class I18nManager:
    """
    国际化管理器 (Internationalization Manager)
    用于管理英文界面文本和消息
    """
    
    def __init__(self,language="en"):
        """
        初始化国际化管理器，默认使用英文
        """
        self.language = language
        self.messages = {
            'en' : self._load_messages(),
            'zh' : self._load_zh_messages(),
        }
    
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
            'arg_output_help': 'Output file path (supports .txt, .json, .csv, .html, .xml, .xlsx, .md formats, default: no output)',
            'arg_timeout_help': 'Request timeout (default: 10 seconds)',
            'arg_delay_help': 'Request interval (default: 0.5 seconds)',
            'arg_verbose_help': 'Verbose output mode',
            'arg_random_help': 'Random User-Agent',
            'arg_app_help': 'Device User-Agent, default: common browser, weixin: WeChat, phone: mobile',
            'arg_update_help': 'Force update the rules file (Force update of the rules file)',
            'arg_threads_help': 'Select the number of threads. The default is 10',
            'arg_depth_help': 'Select the depth of the scan. The default is 1',
            'arg_urlsfile_help': 'Select the file path of the urls',


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
            'version': '0.6.5',
            'description': 'Api-Finder - Find API endpoints from frontend files',
            'github_url': 'https://github.com/jujubooom/Api-Finder'
        }
        
        return messages

    def _load_zh_messages(self) -> Dict[str, Any]:
        messages =  {
            # 命令行参数
            'arg_url_help': '目标网站URL',
            'arg_cookie_help': '网站Cookie认证信息',
            'arg_proxy_help': '代理地址，使用"0"表示自动代理池，支持socks5和http',
            'arg_silent_help': '静默模式，仅输出发现的API端点',
            'arg_output_help': '输出文件路径（支持.txt, .json, .csv, .html, .xml, .xlsx, .md格式，默认不输出）',
            'arg_timeout_help': '请求超时时间（默认：10秒）',
            'arg_delay_help': '请求间隔时间（默认：0.5秒）',
            'arg_verbose_help': '详细输出模式',
            'arg_random_help': '随机User-Agent',
            'arg_app_help': '设备User-Agent，默认：普通浏览器，weixin：微信，phone：手机',
            'arg_update_help': '强制更新规则文件',
            'arg_threads_help': '选择线程数量，默认为10',
            'arg_depth_help': '选择扫描深度，默认为1',
            'arg_urlsfile_help': '选择URL文件路径',

                # 输出消息
            'scan_start': '开始API端点扫描...',
            'scan_complete': '扫描完成',
            'proxy_mode': '使用的代理模式：',
            'stats_title': '扫描统计：',
            'stats_total_urls': '总URL数',
            'stats_successful_requests': '成功请求数',
            'stats_failed_requests': '失败请求数',
            'stats_api_endpoints': '发现的API端点数',
            'results_saved': '结果已保存至：',
            'save_failed': '保存结果失败：',

                # 错误消息
            'proxy_fetch_failed': '获取代理列表失败',
            'request_failed': '请求失败',
            'invalid_url': '无效的URL',
            'connection_error': '连接错误',

            'url_found': '发现URL',
            'discovered_from': '发现来源：',

            'output_header': 'API端点扫描结果',
            'output_target': '目标URL',
            'output_scan_time': '扫描时间',
            'output_endpoints_found': '发现的端点',

            'version': '0.6.5',
            'description': 'Api-Finder - 从前端文件中查找API端点',
            'github_url': 'https://github.com/jujubooom/Api-Finder'
            }
        return messages

    def set_language(self, language: str) -> None:
        """
        设置语言
        """
        if language in self.language:
            self.language = language



    def get(self, key: str, default: str = None) -> str:
        """
        获取英文文本 (Get English text)
        
        Args:
            key (str): 消息键 (Message key)
            default (str): 默认值 (Default value)
            
        Returns:
            str: 英文文本 (English text)
        """
        return self.messages[self.language].get(key, default or key)
    

i18n = I18nManager() 