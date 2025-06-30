from django.conf import settings
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def check_code(width=120, height=30, char_length=5, font_size=28):
    
    # 使用os.path.join构建可靠的路径
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Monaco.ttf')
    
    # 确保字体文件存在，否则使用默认字体
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # 如果找不到指定字体，使用PIL默认字体
        font = ImageFont.load_default()
        
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
       
    # 其他验证码生成逻辑...
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())
    
    # 其他绘制干扰线、点等代码...
    
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)