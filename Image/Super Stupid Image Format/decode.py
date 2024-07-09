# Imports
import PIL
from PIL import Image
import numpy as np
import os
import binascii
import datetime


def rgb565_to_rgb888(rgb565):
    r = (rgb565 & 0xF800) >> 8
    g = (rgb565 & 0x07E0) >> 3
    b = (rgb565 & 0x001F) << 3
    return (r, g, b)


def rgb888_to_rgb565(rgb888):
    r, g, b = rgb888
    r = (r >> 3) << 11
    g = (g >> 2) << 5
    b = b >> 3
    return r | g | b


def decode_image(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    if data[:0x4] != b"SSIF":
        raise ValueError("Invalid file format")

    width = int.from_bytes(data[0xB:0xD], "little")
    height = int.from_bytes(data[0xD:0xF], "little")

    image_data = data[0x20:]

    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            offset = (y * width + x) * 2
            rgb565 = int.from_bytes(image_data[offset : offset + 2], "little")
            rgb888 = rgb565_to_rgb888(rgb565)
            pixels[x, y] = rgb888

    return image


def encode_image(image, file_path):
    width, height = image.size

    image_data = bytearray()

    for y in range(height):
        for x in range(width):
            rgb888 = image.getpixel((x, y))
            rgb565 = rgb888_to_rgb565(rgb888)
            image_data += rgb565.to_bytes(2, "little")

    data = bytearray(b"SSIF")
    data += b"\x00\x01"  # Version
    data += b"\x01"  # Reserved
    data += int(datetime.datetime.now().timestamp()).to_bytes(4, "little")
    data += width.to_bytes(2, "little")
    data += height.to_bytes(2, "little")
    data += binascii.crc32(image_data).to_bytes(4, "little")
    data += b"\x00" * 0xA  # Reserved
    data += b"END"
    data += image_data

    with open(file_path, "wb") as f:
        f.write(data)


def image_info(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    if data[:0x4] == b"SSIF":
        valid = True
    else:
        valid = False

    major_version = int.from_bytes(data[0x4:0x5], "little")
    minor_version = int.from_bytes(data[0x5:0x6], "little")

    timestamp = int.from_bytes(data[0x7:0xB], "little")
    if timestamp == 0:
        creation_date = "Unknown"
    else:
        creation_date = datetime.datetime.fromtimestamp(timestamp)

    width = int.from_bytes(data[0xB:0xD], "little")
    height = int.from_bytes(data[0xD:0xF], "little")

    crc32 = int.from_bytes(data[0xF:0x13], "little")

    if crc32 == 0:
        crc32 = "Unknown"

    calculated_crc32 = binascii.crc32(data[0x20:])

    if crc32 != "Unknown" and crc32 != calculated_crc32:
        corrupted = True
    else:
        corrupted = False

    image_data_size = len(data[0x20:])

    print(f"File: {file_path}")
    print(f"Valid: {valid}")
    print(f"Version: {major_version}.{minor_version}\n")

    print(f"Creation date: {creation_date}\n")
    print(f"Width: {width}")
    print(f"Height: {height}\n")

    print(f"CRC32: {crc32}")
    print(f"Calculated CRC32: {calculated_crc32}")
    print(f"Possibly corrupted: {corrupted}\n")

    print(f"Image data size: {image_data_size} bytes")
    print(f"Total size: {len(data)} bytes")
    print("\n")


def decode_to_png(file_path, output_path=None):
    image = decode_image(file_path)
    if output_path is None:
        output_path = os.path.splitext(file_path)[0] + ".png"
    image.save(output_path, "PNG")
