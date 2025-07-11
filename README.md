# Api-Finder

[中文文档](README_CN.md) | [English](README.md)

A tool for finding API endpoints from frontend files

Modified based on [JSFINDER](https://github.com/Threezh1/JSFinder)

## Project Structure

```
Api-Finder/
├── apifinder.py      # Main program file
├── ua_manager.py     # User-Agent manager
├── i18n.py          # Internationalization module
├── config.py         # Configuration file
├── utils.py          # Utility classes
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Usage

```bash
python apifinder.py -u <target_url>
```

## Parameters

- `-u, --url`: Required parameter, specify target website URL
- `-c, --cookie`: Optional parameter, Cookie for authentication
- `-p, --proxy`: Optional parameter, proxy address, use "0" for auto proxy pool, supports socks5 and http
- `-s, --silent`: Optional parameter, silent mode, only output discovered API endpoints
- `-o, --output`: Optional parameter, output file path (supports .txt, .json, .csv formats)
- `-t, --timeout`: Optional parameter, request timeout (default: 10 seconds)
- `-d, --delay`: Optional parameter, request interval (default: 0.5 seconds)
- `-v, --verbose`: Optional parameter, verbose output mode
- `-r, --random`: Optional parameter, random User-Agent
- `-a, --app`: Optional parameter, device UA type (common-desktop browser, weixin-WeChat, phone-mobile, default: common)

## Usage Examples

```bash
# Basic usage
python apifinder.py -u https://example.com

# With Cookie
python apifinder.py -u https://example.com -c "session=abc123"

# Silent mode, only output API endpoints
python apifinder.py -u https://example.com -s

# With proxy
python apifinder.py -u https://example.com -p "http://127.0.0.1:8080"

# Auto proxy pool
python apifinder.py -u https://example.com -p "0"

# With WeChat UA
python apifinder.py -u https://example.com -a weixin

# Random UA
python apifinder.py -u https://example.com -r

# Output to file
python apifinder.py -u https://example.com -o results.json

# Verbose mode
python apifinder.py -u https://example.com -v
```


## Installation

1. Clone the repository:

```bash
git clone https://github.com/jujubooom/Api-Finder.git
cd Api-Finder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tool:

```bash
python apifinder.py -u https://example.com
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- Based on [JSFINDER](https://github.com/Threezh1/JSFinder)
- Thanks to all contributors and users

## Links

- [GitHub Repository](https://github.com/jujubooom/Api-Finder)
- [Issues](https://github.com/jujubooom/Api-Finder/issues)
- [Releases](https://github.com/jujubooom/Api-Finder/releases)

---

