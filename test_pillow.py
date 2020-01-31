from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random

#private func
def randomChar():
    return chr(random.randint(65,90))

def randomColor(L=[]):
    if L is None:
        L = []
    return (random.randint(L[0],L[1]), random.randint(L[0],L[1]), random.randint(L[0],L[1]))


#public func
def pic_add_num(img):   #1
    font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 30)
    fillcolor = "#ff0000"

    im = Image.open(img)
    w,h = im.size
    draw = ImageDraw.Draw(im)
    draw.text((w-20,0), '1', font=font, fill=fillcolor)
    im.save('pic/dramNum.jpg', 'jpeg')

def pic_narrow(img):    #2
    im = Image.open(img)
    w,h = im.size
    im.thumbnail((w//2, h//2))
    im.save('pic/narrow.jpg', 'jpeg')

def pic_fuzzy(img):    #3
    im = Image.open(img)
    im2 = im.filter(ImageFilter.BLUR)
    im2.save('pic/fuzzy.jpg', 'jpeg')

def pic_creatVerificationCode():    #4
    #240 x 60
    width = 60 * 4
    height = 60

    im = Image.new('RGB',(width,height),(255,255,255))
    font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
    draw = ImageDraw.Draw(im)

    #填充每个像素
    list1 = [64,255]
    for x in range(width):
        for y in range(height):
            draw.point((x,y),fill=randomColor(list1))

    #输出文字
    list2 = [32,127]
    for t in range(4):
        draw.text((60 * t + 10, 10), randomChar(), font = font, fill = randomColor(list2))

    #模糊
    im = im.filter(ImageFilter.BLUR)
    im.save('pic/veriCode.jpg', 'jpeg')

if __name__=='__main__':
    #pic_add_num('pic/src_1.jpg')
    #pic_narrow('pic/src_1.jpg')
    #pic_fuzzy('pic/src_2.jpg')
    pic_creatVerificationCode()
    #end end







