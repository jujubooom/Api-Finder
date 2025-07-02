import requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="The website" ,required=True)
parser.add_argument("-c", "--cookie", help="The website cookie")
arg = parser.parse_args()



def do_request(url):
	header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
	print(f"[+]正在尝试请求{url}")
	try:
		get_res = requests.get(url,headers=header,cookies=arg.cookie).text.replace(" ","").replace("\n","")
		print(f"[+]GET请求回显")
		print(f"{get_res[:200]}......")
	except Exception as e:
		print("[-]GET请求失败")
	try:
		post_res = requests.post(url,headers=header,cookies=arg.cookie).text.replace(" ","").replace("\n","")
		print(f"[+]POST请求回显")
		print(f"{post_res[:200]}......")
	except Exception as e:
		print("[-]POST请求失败")
		time.sleep(0.5)
	
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

def Extract_html(URL):
	header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
	try:
		raw = requests.get(URL, headers = header, timeout=3,cookies=arg.cookie)
		raw = raw.content.decode("utf-8", "ignore")
		#print(raw)
		return raw
	except:
		return None
	
def find_by_url(url):
		try:
			print("url:" + url)
		except:
			print("Please specify a URL like https://www.baidu.com")
		html_raw = Extract_html(url)
		if html_raw == None: 
			print("Fail to access " + url)
			return None
		#print(html_raw)
		html = BeautifulSoup(html_raw, "html.parser")
		html_scripts = html.findAll("script")
		#print(html_scripts)
		script_array = {}
		script_temp = ""
		for html_script in html_scripts:
			script_src = html_script.get("src")
			if script_src == None:
				script_temp += html_script.get_text() + "\n"
			else:
				purl = process_url(url, script_src)
				script_array[purl] = Extract_html(purl)
		script_array[url] = script_temp
		#for i in script_array:
		#	print(i)
		allurls = {}
		for script in script_array:
			#print(script)
			temp_urls = extract_URL(script_array[script])
			if len(temp_urls) == 0: continue
			for temp_url in temp_urls:
				allurls[script] = temp_urls 
		result = []
		for i in allurls:
			for j in allurls[i]:
				print(f"[+]{j}发现于{i}")
				temp1 = urlparse(j)
				temp2 = urlparse(url)
				print(temp1.netloc)
				if temp1.netloc != urlparse("1").netloc:
					do_request(j)
				else:
					do_request(temp2.scheme+"://"+temp2.netloc+j)
				
		return result

find_by_url(arg.url)
