from numbers import Number
from random import Random, random
from weakref import proxy
import requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import time
import sys
import fake_useragent
import json
import os
from datetime import datetime

# 使用fake_useragent生成随机UA
ua = fake_useragent.UserAgent()

parser = argparse.ArgumentParser(description="Api-Finder v0.3")
parser.add_argument("-p", "--proxy", help="代理地址，若输入为0自动获取代理池并使用，支持socks5和http")
parser.add_argument("-u", "--url", help="目标网站URL", required=True)
parser.add_argument("-c", "--cookie", help="网站Cookie")
parser.add_argument("-s", "--silent", action="store_true", help="静默模式，只输出发现的API端点")
parser.add_argument("-o", "--output", help="输出文件路径 (目前支持 .txt, .json, .csv 格式, 默认不输出)")
parser.add_argument("-t", "--timeout", type=int, default=10, help="请求超时时间 (默认: 10秒)")
parser.add_argument("-d", "--delay", type=float, default=0.5, help="请求间隔时间 (默认: 0.5秒)")
parser.add_argument("-v", "--verbose", action="store_true", help="详细输出模式")
arg = parser.parse_args()

# 我这里把之前的print_silent函数改成了OutputManager类，后续好添加新的功能
class OutputManager:
	"""
	OutputManager类是用来管理输出的，包括打印信息、保存结果
	silent_mode: 静默模式，只输出发现的API端点
	verbose_mode: 详细输出模式
	output_file: 输出文件路径
	results: 结果列表
	stats: 统计信息
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
		
		# 保存结果
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

	# 输出使用的代理模式
	def print_proxy_mode(self, proxies):
		if not self.silent_mode:
			print(self.color("blue", "使用的代理模式:"))
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
			print(self.color("blue", "扫描统计信息:"))
			print(f"总URL数: {self.stats['total_urls']}")
			print(f"成功请求: {self.stats['successful_requests']}")
			print(f"失败请求: {self.stats['failed_requests']}")
			print(f"发现API端点: {self.stats['api_endpoints']}")
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
					f.write(f"API端点扫描结果\n")
					f.write(f"目标URL: {arg.url}\n")
					f.write(f"扫描时间: {datetime.now().isoformat()}\n")
					f.write(f"发现端点数: {self.stats['api_endpoints']}\n")
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
				print(self.color("green", f"[+] 结果已保存到: {self.output_file}"))
				
		except Exception as e:
			self.print_error(f"保存结果失败: {str(e)}")

# 初始化输出管理器
output = OutputManager(arg.silent, arg.verbose, arg.output)
proxies_global = None

def do_proxys():
	global proxies_global
	
	if proxies_global is not None:
		return proxies_global
	
	if arg.proxy == "0":
		# 自动获取代理列表
		header = {"User-Agent": ua.random}
		proxy_response = requests.get("https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=5", headers=header).text
		proxy_data = json.loads(proxy_response)
		if proxy_data.get("code") == 200 and "data" in proxy_data and "proxies" in proxy_data["data"]:
			proxies_global = proxy_data["data"]["proxies"]
		else:
			output.print_error("获取代理列表失败")
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

	



def do_request(url):
	header = {"User-Agent": ua.random}
	output.print_verbose(f"正在尝试请求: {url}")
	output.stats["total_urls"] += 1

	proxies = do_proxys()
	if proxies and isinstance(proxies, list):
		proxies = {
			"socks5": proxies[Random().randint(0,len(proxies)-1)],
		}


	# GET
	try:
		if proxies:
			get_res = requests.get(url, headers=header, cookies=arg.cookie, timeout=arg.timeout, proxies=proxies)
			# print(proxies)
		else:
			get_res = requests.get(url, headers=header, cookies=arg.cookie, timeout=arg.timeout)
		get_res.raise_for_status()
		response_text = get_res.text.replace(" ", "").replace("\n", "")
		
		if output.silent_mode:
			print(url)
		else:
			output.print_success("GET请求成功")
			if output.verbose_mode:
				output.print_verbose(f"响应长度: {len(response_text)} 字符")
				output.print_verbose(f"响应预览: {response_text[:200]}...")
		
		output.stats["successful_requests"] += 1
		
	except requests.exceptions.RequestException as e:
		output.print_error(f"GET请求失败: {str(e)}")
		output.stats["failed_requests"] += 1
	except Exception as e:
		output.print_error(f"GET请求异常: {str(e)}")
		output.stats["failed_requests"] += 1
	
	# POST请求
	try:
		post_res = requests.post(url, headers=header, cookies=arg.cookie, timeout=arg.timeout)
		post_res.raise_for_status()
		response_text = post_res.text.replace(" ", "").replace("\n", "")
		
		if not output.silent_mode:
			output.print_success("POST请求成功")
			if output.verbose_mode:
				output.print_verbose(f"响应长度: {len(response_text)} 字符")
				output.print_verbose(f"响应预览: {response_text[:200]}...")
		
		output.stats["successful_requests"] += 1
		
	except requests.exceptions.RequestException as e:
		output.print_error(f"POST请求失败: {str(e)}")
		output.stats["failed_requests"] += 1
	except Exception as e:
		output.print_error(f"POST请求异常: {str(e)}")
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
def process_url(URL, re_URL):
	black_url = ["javascript:"]	# Add some keyword for filter url.
	URL_raw = urlparse(URL)
	ab_URL = URL_raw.netloc
	host_URL = URL_raw.scheme
	if re_URL[0:2] == "//":
		result = host_URL  + ":" + re_URL
	elif re_URL[0:4] == "http":
		result = re_URL
	elif re_URL[0:2] != "//" and re_URL not in black_url:
		if re_URL[0:1] == "/":
			result = host_URL + "://" + ab_URL + re_URL
		else:
			if re_URL[0:1] == ".":
				if re_URL[0:2] == "..":
					result = host_URL + "://" + ab_URL + re_URL[2:]
				else:
					result = host_URL + "://" + ab_URL + re_URL[1:]
			else:
				result = host_URL + "://" + ab_URL + "/" + re_URL
	else:
		result = URL
	return result

# Regular expression comes from https://github.com/GerbenJavado/LinkFinder
def extract_URL(JS):
	filter_key = [".png",".jpg",".css",".webp",".apk",".exe",".dmg"]
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
	result = re.finditer(pattern, str(JS))
	rr = []
	if result == None:
		return None
	for match in result:
		if any(sub in match.group() for sub in filter_key):
			pass
		else:
			rr.append(match.group().strip('"').strip("'"))
	return rr

# 获取HTML内容
def Extract_html(URL):
	"""
	URL: 目标URL
	header: 请求头
	raw: 请求返回的内容
	content: 解析后的HTML内容
	return: 返回HTML内容
	"""
	header = {"User-Agent": ua.random}
	try:
		raw = requests.get(URL, headers=header, timeout=arg.timeout, cookies=arg.cookie)
		raw.raise_for_status()
		content = raw.content.decode("utf-8", "ignore")
		output.print_verbose(f"成功获取HTML内容: {URL}")
		return content
	except requests.exceptions.RequestException as e:
		output.print_error(f"获取HTML失败 {URL}: {str(e)}")
		return None
	except Exception as e:
		output.print_error(f"获取HTML异常 {URL}: {str(e)}")
		return None


def find_by_url(url):
	try:
		output.print_info(f"开始扫描目标: {url}")
	except:
		output.print_info("请指定一个有效的URL，例如: https://www.baidu.com")
		return None
	
	html_raw = Extract_html(url)
	if html_raw == None: 
		output.print_error(f"无法访问 {url}")
		return None
	
	output.print_verbose("开始解析HTML内容...")
	html = BeautifulSoup(html_raw, "html.parser")
	html_scripts = html.findAll("script")
	output.print_verbose(f"发现 {len(html_scripts)} 个script标签")
	
	script_array = {}
	script_temp = ""
	
	for html_script in html_scripts:
		script_src = html_script.get("src")
		if script_src == None:
			script_temp += html_script.get_text() + "\n"
		else:
			purl = process_url(url, script_src)
			script_content = Extract_html(purl)
			if script_content:
				script_array[purl] = script_content
			else:
				output.print_warning(f"无法获取外部脚本: {purl}")
	
	script_array[url] = script_temp
	
	allurls = {}
	for script in script_array:
		output.print_verbose(f"分析脚本: {script}")
		temp_urls = extract_URL(script_array[script])
		if len(temp_urls) == 0: 
			output.print_verbose("未发现URL")
			continue
		output.print_verbose(f"发现 {len(temp_urls)} 个URL")
		for temp_url in temp_urls:
			allurls[script] = temp_urls
	
	result = []
	for i in allurls:
		for j in allurls[i]:
			output.print_url(j, i)
			temp1 = urlparse(j)
			temp2 = urlparse(url)
			
			if temp1.netloc != urlparse("1").netloc:
				do_request(j)
			else:
				do_request(temp2.scheme+"://"+temp2.netloc+j)
	
	return result


# 设置一个主函数，方便后续添加新的功能
def main():
	try:
		output.print_info("="*50)
		# 这里添加一个版本号
		output.print_info("Api-Finder v0.3")
		# Github仓库 : https://github.com/jujubooom/Api-Finder
		output.print_info("Github: https://github.com/jujubooom/Api-Finder")
		output.print_info("="*50)

		# 显示代理模式
		output.print_proxy_mode(do_proxys())

		results = find_by_url(arg.url)
		# 显示统计信息
		output.print_stats()
		
		# 保存结果
		output.save_results()

	# 处理中途退出情况，防止输出一堆报错	
	except KeyboardInterrupt:
		output.print_warning("用户中断扫描")
		output.print_stats()
		output.save_results()
	except Exception as e:
		output.print_error(f"程序执行异常: {str(e)}")
		sys.exit(1)

if __name__ == "__main__":
	main()