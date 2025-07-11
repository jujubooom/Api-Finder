#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具类 (Utility Classes)
包含Api-Finder中使用的通用功能 (Contains common functionality used in Api-Finder)
"""

import re
import yaml
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
from .config import DEFAULT_CONFIG

def load_rules():
    """从 rules.yaml 加载规则"""
    import os
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'rules.yaml')
    with open(rules_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

RULES = load_rules()

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
        pattern_raw = RULES.get('url_extractor_pattern', '')
        ignored_domains = RULES.get('ignored_domains', [])

        pattern = re.compile(pattern_raw, re.VERBOSE)
        result = re.finditer(pattern, str(js_content))
        urls = []
        
        if result is None:
            return urls
            
        for match in result:
            url = match.group().strip('"').strip("'")
            if any(sub in url for sub in filter_key):
                continue
            if any(domain in url for domain in ignored_domains):
                continue
            
            urls.append(url)
        
        return urls

class UpdateManager:
    """更新管理工具类"""

    @staticmethod
    def get_current_timestamp():
        """获取当前时间的 YYYYMMDDHHMMSS 格式时间戳"""
        return datetime.now().strftime('%Y%m%d%H%M%S')

    @staticmethod
    def check_for_updates(force_update=False):
        """
        检查并执行规则文件更新, 会合并用户自定义的列表规则。
        
        Args:
            force_update (bool): 是否强制更新
        """
        local_rules = RULES
        last_check_str = str(local_rules.get('last_check_timestamp', '20000101000000'))
        last_check_time = datetime.strptime(last_check_str, '%Y%m%d%H%M%S')
        update_interval = timedelta(days=DEFAULT_CONFIG['update_interval_days'])

        if not force_update and (datetime.now() - last_check_time < update_interval):
            return

        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        
        try:
            remote_url = DEFAULT_CONFIG['remote_rules_url']
            response = requests.get(remote_url, timeout=DEFAULT_CONFIG['timeout'])
            response.raise_for_status()
            
            remote_rules = yaml.safe_load(response.text)
            local_version = str(local_rules.get('version_timestamp', '0'))
            remote_version = str(remote_rules.get('version_timestamp', '0'))
            
            rules_updated = False
            if force_update or remote_version > local_version:
                if force_update:
                    console.print(Panel("🔄 [bold yellow]强制更新规则...[/bold yellow]", border_style="yellow"))
                else:
                    console.print(Panel(f"🆕 [bold green]发现新版本规则 (v{remote_version})，正在合并规则...[/bold green]", border_style="green"))

                # --- 合并逻辑 ---
                # 以远程规则为基础进行合并
                merged_rules = remote_rules.copy()

                # 合并所有列表类型的值
                for key, local_value in local_rules.items():
                    if isinstance(local_value, list):
                        remote_value = merged_rules.get(key, [])
                        if isinstance(remote_value, list):
                            # 合并本地和远程列表并去重
                            merged_list = sorted(list(set(local_value + remote_value)))
                            merged_rules[key] = merged_list
                
                # 更新最后检查时间戳
                merged_rules['last_check_timestamp'] = UpdateManager.get_current_timestamp()

                import os
                rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'rules.yaml')
                with open(rules_path, 'w', encoding='utf-8') as f:
                    yaml.dump(merged_rules, f, allow_unicode=True, sort_keys=False)
                
                console.print("✅ [bold green]规则文件更新并合并成功。[/bold green]")
                rules_updated = True

            else:
                console.print("ℹ️ [bold cyan]本地规则已是最新版本。[/bold cyan]")

            # 如果规则没有更新，仅更新检查时间戳
            if not rules_updated:
                local_rules['last_check_timestamp'] = UpdateManager.get_current_timestamp()
                import os
                rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'rules.yaml')
                with open(rules_path, 'w', encoding='utf-8') as f:
                    yaml.dump(local_rules, f, allow_unicode=True, sort_keys=False)

        except requests.RequestException as e:
            console.print(f"❌ [bold red]检查更新失败:[/bold red] {e}")
        except yaml.YAMLError as e:
            console.print(f"❌ [bold red]解析远程或本地规则文件失败:[/bold red] {e}")
        except Exception as e:
            console.print(f"❌ [bold red]更新过程中发生未知错误:[/bold red] {e}")

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