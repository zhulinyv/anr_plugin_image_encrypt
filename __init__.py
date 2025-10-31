import os
from pathlib import Path

import gradio as gr
import ujson as json

from plugins.anr_plugin_image_encrypt.utils import decrypt_image, encrypt_image
from utils import (
    playsound,
    read_json,
    stop_generate,
    tk_asksavefile_asy,
)
from utils.image_tools import return_array_image
from utils.logger import logger


def before_process(encrypt_input_path, encrypt_input_image):
    with open("./outputs/temp_break.json", "w") as f:
        json.dump({"break": False}, f)

    if encrypt_input_image:
        image_list = [encrypt_input_image]
    else:
        image_list = [
            Path(encrypt_input_path) / file for file in os.listdir(encrypt_input_path)
        ]

    return image_list


def encrypt(encrypt_input_path, encrypt_input_image):
    image_list = []
    for image in before_process(encrypt_input_path, encrypt_input_image):
        _break = read_json("./outputs/temp_break.json")
        if _break["break"]:
            logger.warning("已停止生成!")
            break
        name, extension = os.path.splitext(os.path.basename(image))
        output_path = (
            f"{os.path.dirname(os.path.abspath(image))}\\{name}_encrypt{extension}"
        )
        if encrypt_image(image, output_path):
            image_list.append(return_array_image(output_path))
    playsound("./assets/finish.mp3")
    return image_list


def decrypt(encrypt_input_path, encrypt_input_image):
    image_list = []
    for image in before_process(encrypt_input_path, encrypt_input_image):
        _break = read_json("./outputs/temp_break.json")
        if _break["break"]:
            logger.warning("已停止生成!")
            break
        name, extension = os.path.splitext(os.path.basename(image))
        output_path = (
            f"{os.path.dirname(os.path.abspath(image))}\\{name}_decrypt{extension}"
        )
        if decrypt_image(image, output_path):
            image_list.append(return_array_image(output_path))
    playsound("./assets/finish.mp3")
    return image_list


def plugin():
    with gr.Tab("图片混淆"):
        encrypt_input_path = gr.Textbox(
            label="批处理路径(同时输入路径和图片时仅处理图片)"
        )
        with gr.Row():
            with gr.Column():
                encrypt_input_image = gr.Image(
                    type="numpy", interactive=False, label="Input"
                )
                with gr.Row():
                    encrypt_input_text = gr.Textbox(visible=False)
                    encrypt_input_btn = gr.Button("选择图片")
                    encrypt_clear_btn = gr.Button("清除选择")
            encrypt_clear_btn.click(
                lambda x: x, gr.Textbox(None, visible=False), encrypt_input_text
            )
            encrypt_input_btn.click(
                tk_asksavefile_asy, inputs=[], outputs=[encrypt_input_text]
            )
            encrypt_input_text.change(
                return_array_image, encrypt_input_text, encrypt_input_image
            )
            encrypt_output_image = gr.Gallery(interactive=False, label="Output")
        with gr.Row():
            encrypt_button = gr.Button("混淆")
            encrypt_button.click(
                encrypt,
                inputs=[encrypt_input_path, encrypt_input_text],
                outputs=encrypt_output_image,
            )
            decrypt_button = gr.Button("解混淆")
            decrypt_button.click(
                decrypt,
                inputs=[encrypt_input_path, encrypt_input_text],
                outputs=encrypt_output_image,
            )
        encrypt_stop_button = gr.Button("停止处理")
        encrypt_stop_button.click(stop_generate)
