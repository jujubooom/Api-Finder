"""
@date: 2025
@version: 0.3.1
@description: 用于扫描API端点
"""

import random
import requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import time
import sys
import json
import os
from datetime import datetime
from ua_manager import UaManager
from utils import URLProcessor, URLExtractor
from i18n import i18n
import threading

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
arg = parser.parse_args()

# 初始化UA管理器 (Initialize UA Manager)
Uam = UaManager(arg.app, arg.random)

# 输出管理器类 (Output Manager Class)
class OutputManager:
	"""
	OutputManager类是用来管理输出的，包括打印信息、保存结果
	(OutputManager class is used to manage output, including printing information and saving results)
	
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
		self.results = []
		self.stats = {
			"total_urls": 0,
			"successful_requests": 0,
			"failed_requests": 0,
			"api_endpoints": 0
		}
	
	def color(self, c, text):
		if self.silent_mode:
			return ""
		if c=="red":
			return "\033[0;31;40m"+text+"\033[0m"
		if c=="green":
			return "\033[0;32;40m"+text+"\033[0m"
		if c=="yellow":
			return "\033[0;33;40m"+text+"\033[0m"
		if c=="blue":
			return "\033[0;34;40m"+text+"\033[0m"
		if c=="cyan":
			return "\033[0;36;40m"+text+"\033[0m"
	
	def print_info(self, text):
		if not self.silent_mode:
			print(text)
	
	def print_verbose(self, text):
		if self.verbose_mode and not self.silent_mode:
			print(self.color("cyan", f"[DEBUG] {text}"))
	
	def print_url(self, url, source=""):
		if self.silent_mode:
			print(url)
		else:
			output_text = f"[+]{url}"
			if source:
				output_text += f" (发现于: {source})"
			print(self.color("green", output_text))
		
		# 保存结果 (Save results)
		self.results.append({
			"url": url,
			"source": source,
			"timestamp": datetime.now().isoformat()
		})
		self.stats["api_endpoints"] += 1
	
	def print_error(self, text):
		if not self.silent_mode:
			print(self.color("red", f"[-] {text}"))
	
	def print_warning(self, text):
		if not self.silent_mode:
			print(self.color("yellow", f"[!] {text}"))
	
	def print_success(self, text):
		if not self.silent_mode:
			print(self.color("green", f"[+] {text}"))

	# 输出使用的代理模式 (Output proxy mode used)
	def print_proxy_mode(self, proxies):
		if not self.silent_mode:
			print(self.color("blue", i18n.get('proxy_mode')))
			if proxies:
				if isinstance(proxies, list):
					for proxy in proxies:
						print(self.color("blue", f" - {proxy}"))
				elif isinstance(proxies, dict):
					for protocol, proxy in proxies.items():
						print(self.color("blue", f" - {protocol}: {proxy}"))

	
	def print_stats(self):
		if not self.silent_mode:
			print("\n" + "="*50)
			print(self.color("blue", i18n.get('stats_title')))
			print(f"{i18n.get('stats_total_urls')}: {self.stats['total_urls']}")
			print(f"{i18n.get('stats_successful_requests')}: {self.stats['successful_requests']}")
			print(f"{i18n.get('stats_failed_requests')}: {self.stats['failed_requests']}")
			print(f"{i18n.get('stats_api_endpoints')}: {self.stats['api_endpoints']}")
			print("="*50)
	
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
							"stats": self.stats
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
				print(self.color("green", f"[+] {i18n.get('results_saved')} {self.output_file}"))
				
		except Exception as e:
			self.print_error(f"{i18n.get('save_failed')} {str(e)}")

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
		args=("GET", url, arg.cookie, arg.timeout, result_store)
	)

	post_thread = threading.Thread(
		target=make_request,
		args=("POST", url, arg.cookie, arg.timeout, result_store)
	)

	# 启动线程
	get_thread.start()
	post_thread.start()

	# 等待两个线程完成
	get_thread.join()
	post_thread.join()

	# 统一输出结果 (Unified output results)
	for method in ["GET", "POST"]:
		result = result_store.results[method]
		if result["success"]:
			if method == "GET" and output.silent_mode:
				print(url)
			elif not output.silent_mode:
				output.print_success(f"{method} request successful")
				if output.verbose_mode:
					res_len = len(result["response"])
					output.print_verbose(f"Response length: {res_len} characters")
					output.print_verbose(f"Response preview: {result['response'][:200]}...")

			output.stats["successful_requests"] += 1
		else:
			output.print_error(f"{method} request failed: {result['error']}")
			output.stats["failed_requests"] += 1
	# 请求间隔
	time.sleep(arg.delay)

def find_last(string,str):
	positions = []
	last_position=-1
	while True:
		position = string.find(str,last_position+1)
		if position == -1:break
		last_position = position
		positions.append(position)
	return positions

# Handling relative URLs
# 删除原有的 process_url 和 extract_URL 函数定义

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
		output.print_verbose(f"Successfully retrieved HTML content: {URL}")
		return content
	except requests.exceptions.RequestException as e:
		output.print_error(f"Failed to get HTML {URL}: {str(e)}")
		return None
	except Exception as e:
		output.print_error(f"HTML extraction exception {URL}: {str(e)}")
		return None


def find_by_url(url):
	try:
		output.print_info(f"Starting scan target: {url}")
	except:
		output.print_info("Please specify a valid URL, e.g.: https://www.baidu.com")
		return None
	
	html_raw = Extract_html(url)
	if html_raw == None: 
		output.print_error(f"Cannot access {url}")
		return None
	
	output.print_verbose("Starting to parse HTML content...")
	html = BeautifulSoup(html_raw, "html.parser")
	html_scripts = html.findAll("script")
	output.print_verbose(f"Found {len(html_scripts)} script tags")
	
	script_array = {}
	script_temp = ""
	
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
	
	allurls = {}
	for script in script_array:
		output.print_verbose(f"Analyzing script: {script}")
		temp_urls = URLExtractor.extract_urls(script_array[script])
		if len(temp_urls) == 0: 
			output.print_verbose("No URLs found")
			continue
		output.print_verbose(f"Found {len(temp_urls)} URLs")
		for temp_url in temp_urls:
			allurls[script] = temp_urls
	result_store = ResultStore()

	for i in allurls:
		for j in allurls[i]:
			output.print_url(j, i)
			temp1 = urlparse(j)
			temp2 = urlparse(url)
			
			if temp1.netloc != urlparse("1").netloc:
				do_request(j)
			else:
				do_request(temp2.scheme+"://"+temp2.netloc+j)



# 设置一个主函数，方便后续添加新的功能 (Set up a main function for future feature additions)
def main():
	try:
		output.print_info("="*50)
		# 这里添加一个版本号 (Add version number here)
		output.print_info("Api-Finder v0.3")
		# Github仓库 : https://github.com/jujubooom/Api-Finder
		output.print_info("Github: https://github.com/jujubooom/Api-Finder")
		output.print_info("="*50)

		# 显示代理模式 (Display proxy mode)
		output.print_proxy_mode(do_proxys())

		results = find_by_url(arg.url)
		# 显示统计信息 (Display statistics)
		output.print_stats()
		
		# 保存结果 (Save results)
		output.save_results()

	# 处理中途退出情况，防止输出一堆报错 (Handle interruption to prevent error output)
	except KeyboardInterrupt:
		output.print_warning("User interrupted scan")
		output.print_stats()
		output.save_results()
	except Exception as e:
		output.print_error(f"Program execution exception: {str(e)}")
		sys.exit(1)

if __name__ == "__main__":
	main()