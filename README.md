# 🔐 图片混淆插件 (anr_plugin_image_encrypt)

[Auto-NovelAI-Refactor](https://github.com/zhulinyv/Auto-NovelAI-Refactor) 的图片混淆插件, 基于 **Gilbert 空间填充曲线的像素重排** 对图片进行混淆 / 解混淆, 支持单张或批量处理。

## ✨ 功能特性

- 🔒 **混淆 / 解混淆**: 使用广义 Hilbert (Gilbert) 空间填充曲线重排图片像素, 达到"打乱图片"的混淆效果, 且可无损还原
- 🖼️ **单张与批处理**: 支持直接上传单张图片, 也可指定目录批量处理全部图片
- 📋 **元数据保留**: JPEG 保留 EXIF 信息, PNG 还原原始元数据 (生成参数等)
- ⏹️ **可随时停止**: 处理过程中可随时停止任务

## 📦 依赖

- piexif
- pillow
- ujson

## 🚀 使用方法

1. 在 [Auto-NovelAI-Refactor](https://github.com/zhulinyv/Auto-NovelAI-Refactor) 的插件商店中安装本插件
2. 打开「图片混淆」面板
3. 选择「批处理路径」(整个目录) 或「上传单张图片」
4. 点击 **🔒 混淆** 加密图片, 或 **🔓 解混淆** 还原图片
5. 处理结果会显示在输出区

## ⚠️ 注意事项

- 混淆后的图片**仅作混淆展示**, 如需在 NovelAI 等平台使用, 请先解密还原
- 加密与解密使用相同的算法与偏移量, 二者互为逆操作
