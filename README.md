# Api-Finder
一款从前端文件查找出api的工具

代码在[JSFINDER](https://github.com/Threezh1/JSFinder)的基础上进行修改

# Usage
python apifinder.py -u xxx

## 参数说明
- `-u, --url`: 必需参数，指定要扫描的网站URL
- `-c, --cookie`: 可选参数，用于认证的Cookie
- `-s, --silent`: 可选参数，静默模式，只输出发现的API端点

## 使用示例
```bash
# 基本用法
python apifinder.py -u https://example.com

# 带Cookie的用法
python apifinder.py -u https://example.com -c "session=abc123"

# 静默模式，只输出API端点
python apifinder.py -u https://example.com -s

# 静默模式 + Cookie
python apifinder.py -u https://example.com -c "session=abc123" -s
```
