# coding:utf8
import uuid
import random
from PIL import ImageDraw, Image, ImageFilter, ImageFont
import os

class Codes:
    def random_chr(self):
        num = random.randint(1,3)
        if num == 1:
            char = random.randint(48,57)
        elif num == 2:
            char = random.randint(97,122)
        else:
            char = random.randint(65,90)
        return chr(char)

    def random_dis(self):
        arr = ["^","~","-","`","="]
        return arr[random.randint(0,len(arr)-1)]

    def random_color1(self):
        return (random.randint(64,255), random.randint(64,255), random.randint(64,255))

    def random_color2(self):
        return (random.randint(32,127), random.randint(32,127), random.randint(32,127))
    def create_code(self):
        width = 240
        height = 60
        image = Image.new("RGB",(width, height), (192, 192, 192))
        #image.show()
        font_name = random.randint(1,3)
        font_file = os.path.join(os.path.dirname(__file__),"static/fonts") + "/%d.ttf" % font_name
        font = ImageFont.truetype(font_file,40)
        draw = ImageDraw.Draw(image)
        for x in range(0,width,5):
            for y in range(0,height,5):
                draw.point((x,y), fill=self.random_color1())
        for v in range(0,width,30):
            dis = self.random_dis()
            w = v + 5
            h = random.randint(5,15)
            draw.text((w,h),dis,font=font,fill=self.random_color1())
        chars = ""
        for v in range(0,4):
            c = self.random_chr()
            chars += str(c)
            h = random.randint(5,15)
            w = width/4*v + 10
            draw.text((w,h),c,font=font,fill=self.random_color2())
        image.filter(ImageFilter.BLUR)
        image_name = " %s.jpg" % uuid.uuid4().hex
        save_dir = os.path.join(os.path.dirname(__file__),"static/Codes")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image.save(save_dir + "/" + image_name, "jpeg")
        return dict(
            img_name=image_name,
            codes = chars
        )
        image.show()


if __name__ == "__main__":
    c = Codes
    c.create_code()

