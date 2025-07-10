# Api-Finder
一款从前端文件查找出api的工具

代码在[JSFINDER](https://github.com/Threezh1/JSFinder)的基础上进行修改

## 项目结构
```
Api-Finder/
├── apifinder.py      # 主程序文件
├── ua_manager.py     # User-Agent管理器
├── requirements.txt   # 项目依赖
└── README.md         # 项目说明文档
```

## Usage
python apifinder.py -u xxx

## 参数说明
- `-u, --url`: 必需参数，指定要扫描的网站URL
- `-c, --cookie`: 可选参数，用于认证的Cookie
- `-p, --proxy`: 可选参数，代理地址，若输入为0自动获取代理池并使用，支持socks5和http
- `-s, --silent`: 可选参数，静默模式，只输出发现的API端点
- `-o, --output`: 可选参数，输出文件路径 (支持 .txt, .json, .csv 格式)
- `-t, --timeout`: 可选参数，请求超时时间 (默认: 10秒)
- `-d, --delay`: 可选参数，请求间隔时间 (默认: 0.5秒)
- `-v, --verbose`: 可选参数，详细输出模式
- `-r, --random`: 可选参数，随机UA
- `-a, --app`: 可选参数，设备UA类型 (common-电脑浏览器, weixin-微信, phone-手机, 默认: common)

## 使用示例
```bash
# 基本用法
python apifinder.py -u https://example.com

# 带Cookie的用法
python apifinder.py -u https://example.com -c "session=abc123"

# 静默模式，只输出API端点
python apifinder.py -u https://example.com -s

# 使用代理
python apifinder.py -u https://example.com -p "http://127.0.0.1:8080"

# 自动获取代理池
python apifinder.py -u https://example.com -p "0"

# 使用微信UA
python apifinder.py -u https://example.com -a weixin

# 随机UA
python apifinder.py -u https://example.com -r

# 输出到文件
python apifinder.py -u https://example.com -o results.json

# 详细模式
python apifinder.py -u https://example.com -v
```
