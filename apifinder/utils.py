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
    def extract_urls_from_html(html_content):
        """
        从HTML内容中提取URL (Extract URLs from HTML content)
        
        Args:
            html_content (str): HTML内容 (HTML content)
            
        Returns:
            list: 提取到的URL列表 (List of extracted URLs)
        """
        from bs4 import BeautifulSoup
        filter_key = DEFAULT_CONFIG["filter_extensions"]
        ignored_domains = RULES.get('ignored_domains', [])
        
        urls = []
        
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # 定义要查找的HTML属性
            url_attributes = [
                ('a', 'href'),
                ('link', 'href'),
                ('img', 'src'),
                ('script', 'src'),
                ('iframe', 'src'),
                ('form', 'action'),
                ('area', 'href'),
                ('source', 'src'),
                ('track', 'src'),
                ('audio', 'src'),
                ('video', 'src'),
                ('embed', 'src'),
                ('object', 'data'),
                ('frame', 'src'),
                ('meta', 'content'),
                ('base', 'href'),
            ]
            
            # 提取所有可能的URL
            for tag_name, attr_name in url_attributes:
                tags = soup.find_all(tag_name)
                for tag in tags:
                    url = tag.get(attr_name)
                    if url and isinstance(url, str):
                        # 清理URL
                        url = url.strip().strip('"').strip("'")
                        
                        # 过滤掉无效的URL
                        if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:') or url.startswith('tel:'):
                            continue
                        
                        # 过滤掉不需要的文件扩展名
                        if any(ext in url.lower() for ext in filter_key):
                            continue
                            
                        # 过滤掉被忽略的域名
                        if any(domain in url.lower() for domain in ignored_domains):
                            continue
                        
                        # 只保留相对路径或API相关的URL
                        if (url.startswith('/') or 
                            url.startswith('./') or 
                            url.startswith('../') or
                            'api' in url.lower() or
                            'ajax' in url.lower() or
                            'json' in url.lower() or
                            'xml' in url.lower() or
                            url.endswith('.php') or
                            url.endswith('.jsp') or
                            url.endswith('.asp') or
                            url.endswith('.aspx') or
                            url.endswith('.action') or
                            url.endswith('.do') or
                            url.endswith('.json') or
                            url.endswith('.xml') or
                            url.endswith('.txt') or
                            url.endswith('.html') or
                            url.endswith('.htm')):
                            
                            if url not in urls:
                                urls.append(url)
            
            # 也查找data属性中的URL
            all_tags = soup.find_all()
            for tag in all_tags:
                if tag.attrs:
                    for attr, value in tag.attrs.items():
                        if attr.startswith('data-') and isinstance(value, str):
                            # 使用正则表达式查找URL模式
                            import re
                            url_pattern = r'["\']([^"\']+(?:\.php|\.jsp|\.asp|\.aspx|\.action|\.do|\.json|\.xml|/api/|/ajax/)[^"\']*)["\']'
                            matches = re.findall(url_pattern, value)
                            for match in matches:
                                if match not in urls:
                                    urls.append(match)
            
        except Exception as e:
            # 如果HTML解析失败，返回空列表
            pass
            
        return urls
    
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

        