"""
Api-Finder - API端点扫描工具

这是一个用于从前端文件中发现API端点的工具包。
"""

from .output_manager import OutputManager, FileOutputManager
from .utils import URLProcessor, URLExtractor, UpdateManager
from .ua_manager import UaManager
from .config import DEFAULT_CONFIG
from .i18n import I18nManager

__version__ = "0.5"
__author__ = "jujubooom,bx33661,Rxiain"
__github_url__ = "https://github.com/jujubooom/Api-Finder"
__description__ = "Find API endpoints from frontend files"

__all__ = [
    'OutputManager',
    'FileOutputManager',
    'URLProcessor',
    'URLExtractor',
    'UpdateManager',
    'UaManager',
    'DEFAULT_CONFIG',
    'I18nManager'
] 