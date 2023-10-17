# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
import re


def convert_link_to_format(text):
    """
        将 markdown 格式的链接转换为自定义格式化的文本
    """
    # 先将 markdown 格式的图片链接转换为自定义格式化的文本
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    text = re.sub(pattern, lambda match: f" {match.group(2)} " if match.group(1) == match.group(
        2) else f"《{match.group(1)}》:{match.group(2)} ", text)

    # 再将 markdown 格式的链接转换为自定义格式化的文本
    pattern = r"\[(.*?)\]\((.*?)\)"
    text = re.sub(pattern, lambda match: f" {match.group(2)} " if match.group(1) == match.group(
        2) else f"《{match.group(1)}》:{match.group(2)} ", text)
    return text


@plugins.register(
    name="ReplyFormatter",
    desire_priority=100,
    hidden=True,
    desc="将回复的内容格式规范化",
    version="0.1",
    author="hantuo",
)
class ReplyFormatter(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_DECORATE_REPLY] = self.on_handle_context

        logger.info("[ReplyFormatter] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["reply"].type not in [ReplyType.TEXT]:
            return
        # 格式化链接
        e_context["reply"].content = convert_link_to_format(e_context["reply"].content)
        # 继续到下一个插件
        e_context.action = EventAction.CONTINUE
        return
