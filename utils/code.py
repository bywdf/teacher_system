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
        """随机生成一个字母"""
        return chr(random.randint(65, 90))
        # return str(random.randint(0, 9)) 随机数字

    def rndColor():
        """随机生成RGB颜色"""
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
       
    # 写文字
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())
    
     # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
 
    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

     # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
 
        draw.line((x1, y1, x2, y2), fill=rndColor())

    
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


if __name__ == '__main__':
    # 1. 直接打开
    # img,code = check_code()
    # img.show()
 
    # 2. 写入文件
    # img,code = check_code()
    # with open('code.png','wb') as f:
    #     img.save(f,format='png')
 
    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()
 
    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()
    pass