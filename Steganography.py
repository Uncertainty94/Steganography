# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
res_pixels = []


# +
def new_blue(pixel, bit):
    lam = 0.1  # then bigger lambda, then data in image are more visible and protected
    yxy = 0.298*pixel[0]+0.586*pixel[1]+0.114*pixel[2]
    # if blue component is 0
    if yxy == 0:
        yxy = 5/lam

    if bit == 1:
        result = pixel[2] + lam * yxy
    else:
        result = pixel[2] - lam * yxy

    # if component is over
    if result > 255:
        result = 255
    if result < 0:
        result = 0
    return result


# Returns string of bin code of one char. Adds '0' before the code to complete it to full byte.
def get_bin_code_of_char(symb):
    code = bin(ord(symb))
    code = code[2:]
    return '0' * (8 - len(code)) + code


# Returns bin equivalent of a string.
def get_bin_code_of_string(string):
    bin_form = ''
    for char in string:
        bin_form += get_bin_code_of_char(char)
    return bin_form  # int('0b' + bin_form, 2)


def encoding(string_in):
    string = get_bin_code_of_string(string_in)
    str_length = len(string_in)
    r = 5  # Количество встраиваний каждого бита сообщения

    image = Image.open("test.jpg")
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    coord = []
    for i in range(3, width-3, 4):
        for j in range(3, height-3, 4):
            coord.append([i, j])

    for j in range(str_length):
        for iteration in range(r):
            red = pix[coord[j+iteration][0], coord[j+iteration][1]][0]
            green = pix[coord[j+iteration][0], coord[j+iteration][1]][1]
            # print pix[i, j]
            blue = int(new_blue(pix[coord[j+iteration][0], coord[j+iteration][1]], int(string[j])))
            draw.point((coord[j+iteration][0], coord[j+iteration][1]), (red, green, blue))
            res_pixels.append([coord[j+iteration], blue])
    image.save("ans.jpg", "JPEG")
    del draw


def count_blue_value(pix, i, j):
    return (pix[i-1, j][2] + pix[i-2, j][2] + pix[i-3, j][2] + pix[i+1, j][2] +
            pix[i+2, j][2] + pix[i+3, j][2] + pix[i, j-1][2] + pix[i, j-2][2] +
            pix[i, j-3][2] + pix[i, j+1][2] + pix[i, j+2][2] + pix[i, j+3][2]) / 12


def decoding(length_message):
    count = length_message
    r = 5
    image = Image.open("ans.jpg")
    pix = image.load()

    result = ''
    for i in range(len(res_pixels[0])):
        if count > 0:
            prog_values = []
            for iteration in range(r):
                x = res_pixels[0][i][0]
                y = res_pixels[0][i][1]
                current_pix = pix[x, y]
                val = count_blue_value(current_pix, x, y)
                diff = current_pix[2] - val

                if diff == 0 and current_pix[2] == 255:
                    diff = 0.5
                if diff == 0 and current_pix[2] == 0:
                    diff = -0.5

                if diff > 0:
                    prog_values.append(1)
                else:
                    prog_values.append(0)
            result += str(int(round(sum(prog_values) / float(r))))
            count -= 1
        else:
            break
    print(result)
    return result


input_str = 'ashfb,d,fk'
print("Input: %s" % input_str)
encoding(input_str)
out = decoding(len(input_str))

count = 0
for i in range(len(out)):
    if input_str[i] != out[i]:
        count += 1
print (count / (1.0 * len(out)) * 100)
