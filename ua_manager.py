"""
@author: Ewoji
@date: 2025
@version: 1.0.0
@description: 用于管理User-Agent字符串
"""


import random

class UaManager:
    """
    UaManager类用于管理User-Agent字符串
    支持不同类型的设备UA：common(电脑浏览器)、weixin(微信)、phone(手机)
    支持随机选择UA或固定使用第一个UA
    """
    
    MyUa = {
        'common': [
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        ],
        'weixin': [
            "Mozilla/5.0 (Linux; Android 9; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.3527.52 MQQBrowser/6.2 TBS/044607 Mobile Safari/537.36 MMWEBID/7140 MicroMessenger/7.0.4.1420(0x27000437) Process/tools NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 13; V2148A Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160117 MMWEBSDK/20240404 MMWEBID/8833 MicroMessenger/8.0.49.2600(0x28003137) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 12; NOH-AL00 Build/HUAWEINOH-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160117 MMWEBSDK/20240404 MMWEBID/6916 MicroMessenger/8.0.49.2600(0x28003136) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 11; SM-G9910 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 XWEB/1200117 MMWEBSDK/20241201 MMWEBID/8833 MicroMessenger/8.0.50.2600(0x28003237) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 13; SM-S9180 Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 XWEB/1200117 MMWEBSDK/20241201 MMWEBID/8833 MicroMessenger/8.0.50.2600(0x28003237) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7 Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 XWEB/1200117 MMWEBSDK/20241201 MMWEBID/8833 MicroMessenger/8.0.50.2600(0x28003237) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 13; iPhone Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 XWEB/1200117 MMWEBSDK/20241201 MMWEBID/8833 MicroMessenger/8.0.50.2600(0x28003237) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Mozilla/5.0 (Linux; Android 12; OPPO Find X5 Pro Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 XWEB/1200117 MMWEBSDK/20241201 MMWEBID/8833 MicroMessenger/8.0.50.2600(0x28003237) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64"
        ],
        'phone': [
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 5 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.8",
            "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.2.3 (Baidu; P1 9)",
            "Mozilla/5.0 (Linux; Android 11; SM-G9910 Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S9180 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7 Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 12; OPPO Find X5 Pro Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; OnePlus 9 Pro Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; vivo X60 Pro+ Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; HUAWEI P50 Pro Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        ],
    }

    def __init__(self, app='common', isRand=False):
        """
        初始化UaManager
        
        Args:
            app (str): 设备类型，默认为'common'
                - 'common': 电脑浏览器UA
                - 'weixin': 微信UA
                - 'phone': 手机UA
            isRand (bool): 是否随机选择UA，默认为False
        """
        self.app = app
        self.isRand = isRand

    def getUa(self):
        """
        获取User-Agent字符串
        
        Returns:
            str: User-Agent字符串
        """
        if self.isRand:
            return self.MyUa[self.app][random.randint(0, len(self.MyUa[self.app])-1)]
        else:
            return self.MyUa[self.app][0] 