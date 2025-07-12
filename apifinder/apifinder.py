"""
@date: 2025
@version: 0.3.1
@description: 用于扫描API端点
"""

import random
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import time
import sys
import json
import os
from datetime import datetime
from .ua_manager import UaManager
from .utils import URLProcessor, URLExtractor, UpdateManager
from .i18n import i18n
import threading
import pyfiglet
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.align import Align
from rich.live import Live
from rich.status import Status
from rich.json import JSON
from rich.traceback import install
from rich.columns import Columns
from rich.rule import Rule

# 安装Rich的异常处理
install()

parser = argparse.ArgumentParser(description="Api-Finder v0.3")
parser.add_argument("-u", "--url", help=i18n.get('arg_url_help'), required=True)
parser.add_argument("-c", "--cookie", help=i18n.get('arg_cookie_help'))
parser.add_argument("-p", "--proxy", help=i18n.get('arg_proxy_help'))
parser.add_argument("-s", "--silent", action="store_true", help=i18n.get('arg_silent_help'))
parser.add_argument("-o", "--output", help=i18n.get('arg_output_help'))
parser.add_argument("-t", "--timeout", type=int, default=10, help=i18n.get('arg_timeout_help'))
parser.add_argument("-d", "--delay", type=float, default=0.5, help=i18n.get('arg_delay_help'))
parser.add_argument("-v", "--verbose", action="store_true", help=i18n.get('arg_verbose_help'))
parser.add_argument("-r", "--random", action="store_true", help=i18n.get('arg_random_help'))
parser.add_argument("-a", "--app", help=i18n.get('arg_app_help'), default='common')
parser.add_argument("-U", "--update", action="store_true", help=i18n.get('arg_update_help'))
arg = parser.parse_args()

# 初始化Rich Console (Initialize Rich Console)
console = Console()

# 初始化UA管理器 (Initialize UA Manager)
Uam = UaManager(arg.app, arg.random)

# 使用Rich重构的Logo显示
def show_logo():
	"""使用Rich和pyfiglet显示精美logo"""
	try:
		# 生成ASCII art
		logo_text = pyfiglet.figlet_format("Api-Finder", font="slant")
		
		# 创建带颜色的logo文本
		logo = Text(logo_text, style="cyan bold")
		
		# 创建项目信息文本
		info_text = Text()
		info_text.append("API Endpoint Scanner v0.5", style="green bold")
		info_text.append("     Github: github.com/jujubooom/Api-Finder\n", style="blue")
		info_text.append("Developed by jujubooom,bx,orxiain", style="green bold")
		
		# 创建面板
		logo_panel = Panel(
			Align.center(logo),
			title="[yellow bold]🚀 API-Finder 🚀[/yellow bold]",
			border_style="cyan",
			padding=(1, 2)
		)
		
		info_panel = Panel(
			Align.center(info_text),
			border_style="green",
			padding=(0, 2)
		)
		
		# 显示logo和信息
		console.print(logo_panel)
		console.print(info_panel)
		console.print(Rule(style="dim"))
		
	except Exception as e:
		# 急救措施 - 使用简单的Rich显示
		console.print(Panel(
			"[cyan bold]Api-Finder v0.3[/cyan bold]\n"
			"[blue]Github: github.com/jujubooom/Api-Finder[/blue]",
			title="🚀 API-Finder 🚀",
			border_style="cyan"
		))


# Rich赋能的输出管理器类
class OutputManager:
	"""
	使用Rich库重构的OutputManager类，提供更美观的终端输出
	
	silent_mode: 静默模式，只输出发现的API端点 (Silent mode, only output discovered API endpoints)
	verbose_mode: 详细输出模式 (Verbose output mode)
	output_file: 输出文件路径 (Output file path)
	results: 结果列表 (Results list)
	stats: 统计信息 (Statistics)
	"""
	def __init__(self, silent_mode, verbose_mode=False, output_file=None):
		self.silent_mode = silent_mode
		self.verbose_mode = verbose_mode
		self.output_file = output_file
		self.console = console  # 使用全局的Rich console
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
		if not self.silent_mode:
			self.console.print(text)
	
	def print_verbose(self, text):
		if self.verbose_mode and not self.silent_mode:
			self.console.print(f"[dim][DEBUG][/dim] {text}")
	
	def print_url(self, url, source=""):
		if self.silent_mode:
			# 静默模式使用Rich的print而不是普通print
			self.console.print(url, highlight=False)
		else:
			# 添加到结果表格
			source_display = source.split('/')[-1] if source else "unknown"
			time_display = datetime.now().strftime("%H:%M:%S")
			self.results_table.add_row(url, source_display, time_display)
			
			if source:
				self.console.print(f"[green bold]✓[/green bold] [blue]{url}[/blue] [dim](from: {source_display})[/dim]")
			else:
				self.console.print(f"[green bold]✓[/green bold] [blue]{url}[/blue]")
		
		# 保存结果 (Save results)
		self.results.append({
			"url": url,
			"source": source,
			"timestamp": datetime.now().isoformat()
		})
		self.stats["api_endpoints"] += 1
	
	def print_error(self, text):
		if not self.silent_mode:
			self.console.print(f"[red bold]✗[/red bold] {text}")
	
	def print_warning(self, text):
		if not self.silent_mode:
			self.console.print(f"[yellow bold]⚠[/yellow bold] {text}")
	
	def print_success(self, text):
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

	# 输出使用的代理模式 (Output proxy mode used)
	def print_proxy_mode(self, proxies):
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
	
	def save_results(self):
		if not self.output_file:
			return
		
		try:
			file_ext = os.path.splitext(self.output_file)[1].lower()
			
			if file_ext == '.json':
				with open(self.output_file, 'w', encoding='utf-8') as f:
					json.dump({
						"scan_info": {
							"target_url": arg.url,
							"scan_time": datetime.now().isoformat(),
							"stats": {
								**self.stats,
								"start_time": self.stats["start_time"].isoformat()
							}
						},
						"results": self.results
					}, f, ensure_ascii=False, indent=2)
			
			elif file_ext == '.txt':
				with open(self.output_file, 'w', encoding='utf-8') as f:
					f.write(f"{i18n.get('output_header')}\n")
					f.write(f"{i18n.get('output_target')}: {arg.url}\n")
					f.write(f"{i18n.get('output_scan_time')}: {datetime.now().isoformat()}\n")
					f.write(f"{i18n.get('output_endpoints_found')}: {self.stats['api_endpoints']}\n")
					f.write("-" * 50 + "\n")
					for result in self.results:
						f.write(f"{result['url']}\n")
			
			elif file_ext == '.csv':
				import csv
				with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
					writer = csv.writer(f)
					writer.writerow(['URL', 'Source', 'Timestamp'])
					for result in self.results:
						writer.writerow([result['url'], result['source'], result['timestamp']])
			
			if not self.silent_mode:
				self.console.print(f"\n[green bold]💾 Results saved to:[/green bold] [blue]{self.output_file}[/blue]")
				
		except Exception as e:
			self.print_error(f"Save failed: {str(e)}")
	
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

# 初始化输出管理器 (Initialize output manager)
output = OutputManager(arg.silent, arg.verbose, arg.output)
proxies_global = None

def do_proxys():
	global proxies_global
	
	if proxies_global is not None:
		return proxies_global
	
	if arg.proxy == "0":
		# 自动获取代理列表 (Auto fetch proxy list)
		header = {"User-Agent": Uam.getUa()}
		proxy_response = requests.get("https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=5", headers=header).text
		proxy_data = json.loads(proxy_response)
		if proxy_data.get("code") == 200 and "data" in proxy_data and "proxies" in proxy_data["data"]:
			proxies_global = proxy_data["data"]["proxies"]
		else:
			output.print_error(i18n.get('proxy_fetch_failed'))
			proxies_global = []

	elif arg.proxy:
		# 判断代理类型是否为socks5
		if arg.proxy.startswith('socks5://'):
			proxies_global = {
				"http": arg.proxy,
				"https": arg.proxy
			}
		# 普通http/https代理
		else:
			proxies_global = {
				"http": arg.proxy if arg.proxy.startswith('http') else f'http://{arg.proxy}',
				"https": arg.proxy if arg.proxy.startswith('http') else f'http://{arg.proxy}'
			}
	
	return proxies_global

# 创建线程安全的结果存储结构 (Create thread-safe result storage structure)
class ResultStore:
	def __init__(self):
		self.results = {"GET": {}, "POST": {}}
		self.lock = threading.Lock()

	def update(self, method, success, response_text, error=None):
		with self.lock:
			self.results[method] = {
				"success": success,
				"response": response_text,
				"error": error
			}


# 请求执行函数 (Request execution function)
def make_request(method, url, cookies, timeout, store):
	# 请求前的配置 (Request configuration)
	proxies = do_proxys()
	if proxies and isinstance(proxies, list):
		proxies = {
			"socks5": proxies[random.randint(0,len(proxies)-1)],
		}
	header = {"User-Agent": Uam.getUa()}

	try:
		if method == "GET":
			if proxies:
				res = requests.get(url, headers=header, cookies=cookies,
								   timeout=timeout, proxies=proxies)
			else:
				res = requests.get(url, headers=header, cookies=cookies,
								   timeout=timeout)
		else:  # POST
			if proxies:
				res = requests.post(url, headers=header, cookies=cookies,
								   timeout=timeout, proxies=proxies)
			else:
				res = requests.post(url, headers=header, cookies=cookies,
								   timeout=timeout)

		res.raise_for_status()
		response_text = res.text.replace(" ", "").replace("\n", "")
		store.update(method, True, response_text)

	except requests.exceptions.RequestException as e:
		store.update(method, False, None, str(e))
	except Exception as e:
		store.update(method, False, None, str(e))


def do_request(url):
	result_store = ResultStore()

	# 创建并启动线程
	get_thread = threading.Thread(
		target=make_request,
		args=("GET", url, {"Cookie": arg.cookie}, arg.timeout, result_store)
	)

	post_thread = threading.Thread(
		target=make_request,
		args=("POST", url, {"Cookie": arg.cookie}, arg.timeout, result_store)
	)

	# 启动线程
	get_thread.start()
	post_thread.start()

	# 等待两个线程完成
	get_thread.join()
	post_thread.join()
	
	response_text_to_return = None

	# 统一输出结果 (Unified output results)
	for method in ["GET", "POST"]:
		result = result_store.results[method]
		if result["success"]:
			response_text = result['response']
			
			if method == "GET":
				response_text_to_return = response_text
				# 尝试解析和打印标题
				try:
					if response_text and '<html' in response_text.lower():
						soup = BeautifulSoup(response_text, 'html.parser')
						if soup.title and soup.title.string:
							title = soup.title.string.strip().replace('\\n', '').replace('\\r', '')
							if title:
								output.print_title(url, title)
				except Exception as e:
					output.print_verbose(f"Could not parse title from {url}: {e}")

			if method == "GET" and output.silent_mode:
				output.console.print(url, highlight=False)
			elif not output.silent_mode:
				output.print_success(f"{method} request successful for {url}")
				if output.verbose_mode:
					res_len = len(response_text)
					output.print_verbose(f"📏 Response length: {res_len} characters")
					output.print_verbose(f"👀 Response preview: {response_text[:200]}...")

			output.stats["successful_requests"] += 1
		else:
			output.print_error(f"{method} request failed for {url}: {result['error']}")
			output.stats["failed_requests"] += 1
	
	# 请求间隔
	time.sleep(arg.delay)
	return response_text_to_return


# 获取HTML内容 (Extract HTML content)
def Extract_html(URL):
	"""
	URL: 目标URL (Target URL)
	header: 请求头 (Request headers)
	raw: 请求返回的内容 (Raw response content)
	content: 解析后的HTML内容 (Parsed HTML content)
	return: 返回HTML内容 (Return HTML content)
	"""
	header = {"User-Agent": Uam.getUa()}
	try:
		raw = requests.get(URL, headers=header, timeout=arg.timeout, cookies=arg.cookie)
		raw.raise_for_status()
		content = raw.content.decode("utf-8", "ignore")
		output.print_verbose(f"✅ Successfully retrieved HTML content: {URL}")
		return content
	except requests.exceptions.RequestException as e:
		output.print_error(f"Failed to get HTML {URL}: {str(e)}")
		return None
	except Exception as e:
		output.print_error(f"HTML extraction exception {URL}: {str(e)}")
		return None


def find_by_url(url):
	try:
		output.print_info(f"🎯 [bold blue]Starting scan target:[/bold blue] [green]{url}[/green]")
	except:
		output.print_info("❌ Please specify a valid URL, e.g.: https://www.baidu.com")
		return None
	
	# 使用状态显示
	if not output.silent_mode:
		with Status("[bold green]🔍 Fetching target page...", console=output.console):
			html_raw = Extract_html(url)
	else:
		html_raw = Extract_html(url)
	
	if html_raw == None: 
		output.print_error(f"Cannot access {url}")
		return None
	
	output.print_verbose("🔍 Starting to parse HTML content...")
	html = BeautifulSoup(html_raw, "html.parser")
	html_scripts = html.findAll("script")
	output.print_verbose(f"📄 Found {len(html_scripts)} script tags")
	
	script_array = {}
	script_temp = ""
	
	# 创建进度条来显示脚本处理进度
	progress = output.create_progress()
	if progress:
		with progress:
			script_task = progress.add_task("[cyan]📄 Processing scripts...", total=len(html_scripts))
			
			for html_script in html_scripts:
				script_src = html_script.get("src")
				if script_src == None:
					script_temp += html_script.get_text() + "\n"
				else:
					purl = URLProcessor.process_url(url, script_src)
					progress.update(script_task, description=f"[cyan]📄 Fetching: {purl.split('/')[-1]}")
					script_content = Extract_html(purl)
					if script_content:
						script_array[purl] = script_content
					else:
						output.print_warning(f"Cannot get external script: {purl}")
				
				progress.advance(script_task)
	else:
		# 静默模式或无进度条时的处理
		for html_script in html_scripts:
			script_src = html_script.get("src")
			if script_src == None:
				script_temp += html_script.get_text() + "\n"
			else:
				purl = URLProcessor.process_url(url, script_src)
				script_content = Extract_html(purl)
				if script_content:
					script_array[purl] = script_content
				else:
					output.print_warning(f"Cannot get external script: {purl}")
	
	script_array[url] = script_temp
	
	# 分析脚本以提取URL
	allurls = {}
	total_scripts = len(script_array)
	
	if not output.silent_mode:
		output.print_info(f"🔎 [bold yellow]Analyzing {total_scripts} scripts for API endpoints...[/bold yellow]")
	
	progress = output.create_progress()
	if progress:
		with progress:
			analyze_task = progress.add_task("[green]🔍 Analyzing scripts...", total=total_scripts)
			
			for script in script_array:
				script_name = script.split('/')[-1] if '/' in script else script
				progress.update(analyze_task, description=f"[green]🔍 Analyzing: {script_name}")
				
				output.print_verbose(f"🔎 Analyzing script: {script}")
				temp_urls = URLExtractor.extract_urls(script_array[script])
				
				if len(temp_urls) == 0: 
					output.print_verbose("🔍 No URLs found")
				else:
					output.print_verbose(f"✅ Found {len(temp_urls)} URLs")
					allurls[script] = temp_urls
				
				progress.advance(analyze_task)
	else:
		# 静默模式处理
		for script in script_array:
			output.print_verbose(f"🔎 Analyzing script: {script}")
			temp_urls = URLExtractor.extract_urls(script_array[script])
			if len(temp_urls) == 0: 
				output.print_verbose("🔍 No URLs found")
			else:
				output.print_verbose(f"✅ Found {len(temp_urls)} URLs")
				allurls[script] = temp_urls
	
	# 处理发现的URL
	total_urls = sum(len(urls) for urls in allurls.values())
	if total_urls > 0:
		output.print_info(f"🎯 [bold green]Found {total_urls} potential API endpoints. Testing them...[/bold green]")
		
		progress = output.create_progress()
		if progress:
			with progress:
				test_task = progress.add_task("[blue]🌐 Testing endpoints...", total=total_urls)
				
				for i in allurls:
					for j in allurls[i]:
						# 显示当前正在测试的URL
						url_display = j[:50] + "..." if len(j) > 50 else j
						progress.update(test_task, description=f"[blue]🌐 Testing: {url_display}")
						
						output.print_url(j, i)
						temp1 = urlparse(j)
						temp2 = urlparse(url)
						
						if temp1.netloc != urlparse("1").netloc:
							do_request(j)
						else:
							do_request(temp2.scheme+"://"+temp2.netloc+j)
						
						progress.advance(test_task)
		else:
			# 静默模式处理
			for i in allurls:
				for j in allurls[i]:
					output.print_url(j, i)
					temp1 = urlparse(j)
					temp2 = urlparse(url)
					
					if temp1.netloc != urlparse("1").netloc:
						do_request(j)
					else:
						do_request(temp2.scheme+"://"+temp2.netloc+j)
	else:
		output.print_warning("⚠️ No API endpoints discovered in the scanned content")
	
	# 更新统计信息
	output.stats["total_urls"] = total_urls



# 设置一个主函数，方便后续添加新的功能
def main():
	"""主函数"""
	
	# 首先处理更新检查
	if arg.update:
		with Status("[bold blue]🔄 Checking for updates...", console=output.console):
			UpdateManager.check_for_updates(force_update=True)
		sys.exit(0)
	else:
		with Status("[bold blue]🔄 Checking for updates...", console=output.console):
			UpdateManager.check_for_updates(force_update=False)

	if not arg.silent:
		show_logo()
	
	try:
		url = arg.url
		
		# 显示代理模式
		output.print_proxy_mode(do_proxys())

		# 开始扫描
		output.print_info(f"🚀 [bold green]Starting API endpoint scan...[/bold green]")
		results = find_by_url(url)
		
		if not output.silent_mode:
			if output.stats["api_endpoints"] > 0:
				output.print_info(f"🎉 [bold green]Scan completed! Found {output.stats['api_endpoints']} API endpoints.[/bold green]")
			else:
				output.print_info(f"✅ [bold yellow]Scan completed. No API endpoints found.[/bold yellow]")
	
	except KeyboardInterrupt:
		output.print_warning("\n⚠️ Scan interrupted by user")
		sys.exit(1)
	except Exception as e:
		output.print_error(f"Error: {str(e)}")
		raise  # 让Rich的异常处理器处理
	
	finally:
		output.print_stats()
		output.save_results()

if __name__ == '__main__':
	main()