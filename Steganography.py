# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
res_pixels = []


# +
def new_blue(pixel, bit):
    lam = 0.1  # then bigger lambda, then data in image are more visible and protected
    yxy = int(0.298*pixel[0]+0.586*pixel[1]+0.114*pixel[2])
    # if blue component is 0
    if yxy == 0:
        yxy = int(5 / lam)

    if bit == 1:
        result = int(pixel[2] + lam * yxy)
    else:
        result = int(pixel[2] - lam * yxy)

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


def encoding(string):
    str_length = len(string)
    r = 5  # Количество встраиваний каждого бита сообщения
    print string
    image = Image.open("test.jpg")
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    # TODO: поправить coord
    coord = []
    amount = str_length * r
    for i in range(3, width - 3, 4):
        for j in range(3, height - 3, 4):
            coord.append([i, j])

    index = 0
    for j in range(str_length):
        for iteration in range(r):
            red = pix[coord[index+iteration][0], coord[index+iteration][1]][0]
            green = pix[coord[index+iteration][0], coord[index+iteration][1]][1]
            # print pix[i, j]
            blue = int(new_blue(pix[coord[index+iteration][0], coord[index+iteration][1]], int(string[j])))
            draw.point((coord[index+iteration][0], coord[index+iteration][1]), (red, green, blue))
            res_pixels.append([coord[index+iteration], blue, int(string[j])])
        index += r
    image.save("ans.jpg", "JPEG")

    del draw


def count_blue_value(pix, i, j):
    summa = pix[i-1, j][2] + pix[i-2, j][2] + pix[i-3, j][2] + pix[i+1, j][2] + pix[i+2, j][2] + pix[i+3, j][2] + pix[i, j-1][2] + pix[i, j-2][2] + pix[i, j-3][2] + pix[i, j+1][2] + pix[i, j+2][2] + pix[i, j+3][2]
    return summa / 12


def decoding(length_message):
    len_message = length_message
    r = 5
    image = Image.open("ans.jpg")
    pix = image.load()

    result = ''
    for i in range(0, len(res_pixels), r):
        if len_message > 0:
            temp_values = []
            for iteration in range(r):
                x = res_pixels[i+iteration][0][0]
                y = res_pixels[i+iteration][0][1]
                # current_pix = pix[x, y]
                avg_value = count_blue_value(pix, x, y)
                diff = res_pixels[i+iteration][1] - avg_value
                # diff = current_pix[2] - avg_value
                if diff == 0 and res_pixels[i+iteration][1] == 255:
                    diff = 0.5
                if diff == 0 and res_pixels[i+iteration][1] == 0:
                    diff = -0.5

                if diff > 0:
                    temp_values.append(1)
                else:
                    temp_values.append(0)
            result += str(int(round(sum(temp_values) / float(r))))
            len_message -= 1
        else:
            break
    print result
    return result

#
# string_in = 'ashfb,d,fk'
# input_str = get_bin_code_of_string(string_in)
# print input_str
# print("Input: %s" % input_str)
input_str = '10101010111111111100000000'

encoding(input_str)
out = decoding(len(input_str))

count = 0
for ind in range(len(out)):
    if input_str[ind] != out[ind]:
        count += 1
print 'Error = ' + str(int(count / (1.0 * len(out)) * 100)) + '%'
