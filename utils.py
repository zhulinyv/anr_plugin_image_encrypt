import math

import piexif
from PIL import Image

from utils.image_tools import revert_image_info
from utils.logger import logger


def gilbert2d(width, height):
    """
    Generalized Hilbert ('gilbert') space-filling curve for arbitrary-sized
    2D rectangular grids. Generates discrete 2D coordinates to fill a rectangle
    of size (width x height).
    """
    coordinates = []

    if width >= height:
        generate2d(0, 0, width, 0, 0, height, coordinates)
    else:
        generate2d(0, 0, 0, height, width, 0, coordinates)

    return coordinates


def generate2d(x, y, ax, ay, bx, by, coordinates):
    w = abs(ax + ay)
    h = abs(bx + by)

    dax = 1 if ax > 0 else -1 if ax < 0 else 0
    day = 1 if ay > 0 else -1 if ay < 0 else 0
    dbx = 1 if bx > 0 else -1 if bx < 0 else 0
    dby = 1 if by > 0 else -1 if by < 0 else 0

    if h == 1:
        # trivial row fill
        for i in range(w):
            coordinates.append([x, y])
            x += dax
            y += day
        return

    if w == 1:
        # trivial column fill
        for i in range(h):
            coordinates.append([x, y])
            x += dbx
            y += dby
        return

    ax2 = ax // 2
    ay2 = ay // 2
    bx2 = bx // 2
    by2 = by // 2

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2 * w > 3 * h:
        if (w2 % 2) and (w > 2):
            # prefer even steps
            ax2 += dax
            ay2 += day

        # long case: split in two parts only
        generate2d(x, y, ax2, ay2, bx, by, coordinates)
        generate2d(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by, coordinates)

    else:
        if (h2 % 2) and (h > 2):
            # prefer even steps
            bx2 += dbx
            by2 += dby

        # standard case: one step up, one long horizontal, one step down
        generate2d(x, y, bx2, by2, ax2, ay2, coordinates)
        generate2d(x + bx2, y + by2, ax, ay, bx - bx2, by - by2, coordinates)
        generate2d(
            x + (ax - dax) + (bx2 - dbx),
            y + (ay - day) + (by2 - dby),
            -bx2,
            -by2,
            -(ax - ax2),
            -(ay - ay2),
            coordinates,
        )


def encrypt_image(input_path, output_path):
    try:
        logger.info(f"正在混淆 {input_path}...")
        image = Image.open(input_path)
        width, height = image.size

        if image.mode != "RGB":
            image = image.convert("RGB")

        pixels = image.load()

        curve = gilbert2d(width, height)
        offset = round((math.sqrt(5) - 1) / 2 * width * height)

        new_image = Image.new("RGB", (width, height))
        new_pixels = new_image.load()

        for i in range(width * height):
            old_pos = curve[i]
            new_pos = curve[(i + offset) % (width * height)]

            if 0 <= old_pos[0] < width and 0 <= old_pos[1] < height:
                pixel_value = pixels[old_pos[0], old_pos[1]]
            else:
                pixel_value = (0, 0, 0)

            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height:
                new_pixels[new_pos[0], new_pos[1]] = pixel_value

        format_str = "JPEG"
        if str(input_path).lower().endswith(".png"):
            format_str = "PNG"

        if format_str == "JPEG":
            try:
                exif_dict = piexif.load(input_path)
                exif_bytes = piexif.dump(exif_dict)
                new_image.save(
                    output_path, format=format_str, quality=95, exif=exif_bytes
                )
            except Exception:
                new_image.save(output_path, format=format_str, quality=95)
        else:
            new_image.save(output_path, format=format_str)
            logger.debug("正在还原元数据...")
            if revert_image_info(input_path, output_path):
                logger.success("还原成功!")
            else:
                logger.error("还原失败!")

        logger.success(f"混淆完成, 图片已保存到: {output_path}")
        return True

    except Exception as e:
        logger.error(f"混淆失败: {e}")
        return False


def decrypt_image(input_path, output_path):
    try:
        logger.info(f"正在解混淆 {input_path}...")
        image = Image.open(input_path)
        width, height = image.size

        if image.mode != "RGB":
            image = image.convert("RGB")

        pixels = image.load()

        curve = gilbert2d(width, height)
        offset = round((math.sqrt(5) - 1) / 2 * width * height)

        new_image = Image.new("RGB", (width, height))
        new_pixels = new_image.load()

        for i in range(width * height):
            old_pos = curve[i]
            new_pos = curve[(i + offset) % (width * height)]

            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height:
                pixel_value = pixels[new_pos[0], new_pos[1]]
            else:
                pixel_value = (0, 0, 0)

            if 0 <= old_pos[0] < width and 0 <= old_pos[1] < height:
                new_pixels[old_pos[0], old_pos[1]] = pixel_value

        format_str = "JPEG"
        if str(input_path).lower().endswith(".png"):
            format_str = "PNG"

        if format_str == "JPEG":
            try:
                exif_dict = piexif.load(input_path)
                exif_bytes = piexif.dump(exif_dict)
                new_image.save(
                    output_path, format=format_str, quality=95, exif=exif_bytes
                )
            except Exception:
                new_image.save(output_path, format=format_str, quality=95)
        else:
            new_image.save(output_path, format=format_str)
            logger.debug("正在还原元数据...")
            if revert_image_info(input_path, output_path):
                logger.success("还原成功!")
            else:
                logger.error("还原失败!")

        logger.success(f"解混淆完成, 图片已保存到: {output_path}")
        return True

    except Exception as e:
        logger.error(f"解混淆失败: {e}")
        return False
