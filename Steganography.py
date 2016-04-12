from PIL import Image, ImageDraw


def new_blue(pixel, bit):
    lam = 0.1
    yxy = 0.3*pixel[0]+0.59*pixel[1]+0.11*pixel[2]
    if bit == 1:
        result = pixel[2] + lam * yxy
    else:
        result = pixel[2] - lam * yxy
    if result > 255:
        result = 255
    if result < 0:
        result = 0
    return result


# Returns string of bin code of one char. Adds '0' before the code to complete it to full byte.
def get_bin_code_of_char(symb):
    code = bin(ord(symb))
    code = code[2:]
    return "0" * (8 - len(code)) + code


# Returns int equivalent of bin code of a string.
def get_bin_code_of_string(string):
    bin_form = ''
    for char in string:
        bin_form += get_bin_code_of_char(char)
    return int('0b'+bin_form, 2)


def encoding(string_in):
    string = string_in
    image = Image.open("test.jpg")
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    for i in range(3, width-3, 4):
        for j in range(3, height-3, 4):
            a = pix[i, j][0]
            b = pix[i, j][1]
            # print pix[i, j]
            if len(string) != 0:
                c = int(new_blue(pix[i, j], int(string[0])))
                string = string[1:]
                draw.point((i, j), (a, b, c))
            else:
                break
    image.save("ans.jpg", "JPEG")
    del draw


def decoding(length):
    count = length
    image = Image.open("ans.jpg")
    # draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    old_image = Image.open("test.jpg")
    old_pix = old_image.load()

    result = ''
    for i in range(3, width-3, 4):
        for j in range(3, height-3, 4):
            # print 'new', pix[i, j]
            if count > 0:
                current_pix = pix[i, j]
                old_pixels = old_pix[i, j]
                val = (pix[i-1, j][2] + pix[i-2, j][2] + pix[i-3, j][2] + pix[i+1, j][2] +
                       pix[i+2, j][2] + pix[i+3, j][2] + pix[i, j-1][2] + pix[i, j-2][2] +
                       pix[i, j-3][2] + pix[i, j+1][2] + pix[i, j+2][2] + pix[i, j+3][2]) / 12
                if pix[i, j][2] >= val:
                    result += '1'
                else:
                    result += '0'
                count -= 1
            else:
                break
    # del draw
    print result
    return result


in_string = '101011111'
print in_string
encoding(in_string)
out = decoding(len(in_string))

count = 0
for i in range(len(out)):
    if in_string[i] != out[i]:
        count += 1
print count/(1.0 * len(out)) * 100
