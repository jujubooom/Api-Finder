#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具类 (Utility Classes)
包含Api-Finder中使用的通用功能 (Contains common functionality used in Api-Finder)
"""

import re
from urllib.parse import urlparse
from config import DEFAULT_CONFIG

class URLProcessor:
    """URL处理工具类 (URL processing utility class)"""
    
    @staticmethod
    def process_url(base_url, relative_url):
        """
        处理相对URL，转换为绝对URL (Process relative URL, convert to absolute URL)
        
        Args:
            base_url (str): 基础URL (Base URL)
            relative_url (str): 相对URL (Relative URL)
            
        Returns:
            str: 绝对URL (Absolute URL)
        """
        black_url = ["javascript:"]
        url_raw = urlparse(base_url)
        ab_url = url_raw.netloc
        host_url = url_raw.scheme
        
        if relative_url[0:2] == "//":
            result = host_url + ":" + relative_url
        elif relative_url[0:4] == "http":
            result = relative_url
        elif relative_url[0:2] != "//" and relative_url not in black_url:
            if relative_url[0:1] == "/":
                result = host_url + "://" + ab_url + relative_url
            else:
                if relative_url[0:1] == ".":
                    if relative_url[0:2] == "..":
                        result = host_url + "://" + ab_url + relative_url[2:]
                    else:
                        result = host_url + "://" + ab_url + relative_url[1:]
                else:
                    result = host_url + "://" + ab_url + "/" + relative_url
        else:
            result = base_url
        return result

class URLExtractor:
    """URL提取工具类 (URL extraction utility class)"""
    
    @staticmethod
    def extract_urls(js_content):
        """
        从JavaScript内容中提取URL (Extract URLs from JavaScript content)
        
        Args:
            js_content (str): JavaScript内容 (JavaScript content)
            
        Returns:
            list: 提取到的URL列表 (List of extracted URLs)
        """
        filter_key = DEFAULT_CONFIG["filter_extensions"]
        pattern_raw = r"""
          (?:"|')                               # Start newline delimiter
          (
            ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
            [^"'/]{1,}\.                        # Match a domainname (any character + dot)
            [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
            |
            ((?:/|\.\./|\./)                    # Start with /,../,./
            [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
            [^"'><,;|()]{1,})                   # Rest of the characters can't be
            |
            ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
            [a-zA-Z0-9_\-/]{1,}                 # Resource name
            \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
            (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
            |
            ([a-zA-Z0-9_\-]{1,}                 # filename
            \.(?:php|asp|aspx|jsp|json|
                 action|html|js|txt|xml)             # . + extension
            (?:\?[^"|']{0,}|))                  # ? mark with parameters
          )
          (?:"|')                               # End newline delimiter
        """
        pattern = re.compile(pattern_raw, re.VERBOSE)
        result = re.finditer(pattern, str(js_content))
        urls = []
        
        if result is None:
            return urls
            
        for match in result:
            if any(sub in match.group() for sub in filter_key):
                continue
            else:
                urls.append(match.group().strip('"').strip("'"))
        
        return urls

class ProxyManager:
    """代理管理工具类 (Proxy management utility class)"""
    
    @staticmethod
    def format_proxy(proxy_url):
        """
        格式化代理URL (Format proxy URL)
        
        Args:
            proxy_url (str): 代理URL (Proxy URL)
            
        Returns:
            dict: 格式化后的代理配置 (Formatted proxy configuration)
        """
        if proxy_url.startswith('socks5://'):
            return {
                "http": proxy_url,
                "https": proxy_url
            }
        else:
            return {
                "http": proxy_url if proxy_url.startswith('http') else f'http://{proxy_url}',
                "https": proxy_url if proxy_url.startswith('http') else f'http://{proxy_url}'
            } 