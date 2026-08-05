"""
这个文件存放该程序需要的数据类型
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


@dataclass
class Todo:
    id: int | None = None  # 新建todo时没有id，id时数据库返回的
    text: str = ""  # 必须有内容
    priority: Priority = Priority.MEDIUM  # 默认中等
    status: int = 0  # 默认未完成
    created_at: datetime | None = None  # 存储加载时间
    stop_at: datetime | None = None  # 结束时间
