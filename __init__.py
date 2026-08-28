"""图片混淆插件: 加密 / 解密图片 (基于 LSB 隐写)。"""
from __future__ import annotations

import os
from pathlib import Path

import ujson as json

from plugins.anr_plugin_image_encrypt.utils import decrypt_image, encrypt_image
from utils.helpers import check_stop, playsound, read_json
from utils.logger import logger
from utils.plugins import Action, Field, Panel, Plugin


def _input_images(input_path: str | None, input_image: str | None) -> list[str]:
    """收集待处理图片: 先单张图片, 再目录内全部图片 (同时输入时两者都处理)。"""
    os.makedirs("./outputs", exist_ok=True)
    with open("./outputs/temp_break.json", "w") as f:
        json.dump({"break": False}, f)
    images = []
    if input_image:
        images.append(input_image)
    if input_path:
        images.extend(str(Path(input_path) / f) for f in sorted(os.listdir(input_path)))
    # 去重 (保留顺序: 先图片, 再目录)
    seen = set()
    result = []
    for img in images:
        key = os.path.abspath(img)
        if key not in seen:
            seen.add(key)
            result.append(img)
    return result


def _process(values: dict, action: str) -> dict:
    image_list = []
    for image in _input_images(values.get("path"), values.get("image")):
        if check_stop():
            logger.warning("已停止处理!")
            break
        name, extension = os.path.splitext(os.path.basename(image))
        output_path = f"{os.path.dirname(os.path.abspath(image))}\\{name}_{action}{extension}"
        func = encrypt_image if action == "encrypt" else decrypt_image
        if func(image, output_path):
            image_list.append(output_path)
            logger.success(f"{'加密' if action == 'encrypt' else '解密'}完成: {output_path}")
    playsound("./assets/finish.mp3")
    return {"images": image_list, "message": f"{'加密' if action == 'encrypt' else '解密'}处理完成!"}


def register(plugin: Plugin):
    panel = Panel(
        id="image_encrypt",
        title="图片混淆",
        icon="🔐",
        description="基于 LSB 隐写的图片加密 / 解密, 支持单张或批处理",
        fields=[
            Field(id="path", label="批处理路径", type="path", folder=True, file=False),
            Field(id="image", label="或上传单张图片", type="image"),
        ],
        actions=[
            Action(id="encrypt", label="🔒 混淆", inputs=["path", "image"], handler=lambda v: _process(v, "encrypt")),
            Action(id="decrypt", label="🔓 解混淆", inputs=["path", "image"], handler=lambda v: _process(v, "decrypt")),
        ],
    )
    plugin.title = "图片混淆"
    plugin.description = "图片 LSB 隐写加密插件"
    plugin.icon = "🔐"
    plugin.panels.append(panel)
