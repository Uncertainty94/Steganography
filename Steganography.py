# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from math import log, sqrt
import numpy as np
import matplotlib.pyplot as plt

res_pixels = []  # [coords, new_blue, old_blue, value_inserting_bit]


# +
def new_blue(pixel, bit, lambd):
    lam = lambd  # then bigger lambda, then data in image are more visible and protected
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


def encoding(string, lambd, sigma):
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
    for i in range(sigma + 3, width - sigma - 1, sigma+1):
        for j in range(sigma + 3, height - sigma - 1, sigma+1):
            coord.append([i, j])

    index = 0
    for j in range(str_length):
        for iteration in range(r):
            x = coord[index+iteration][0]
            y = coord[index+iteration][1]
            red = pix[x, y][0]
            green = pix[x, y][1]
            # print pix[i, j]
            blue = int(new_blue(pix[x, y], int(string[j]), lambd))
            res_pixels.append([coord[index + iteration], blue, pix[x, y][2], int(string[j])])
            draw.point((x, y), (red, green, blue))
        index += r
    del draw
    image.save("ans.png", "PNG")


def count_blue_value(pix, i, j, sigma):
    # summa = pix[i-1, j][2] + pix[i-2, j][2] + pix[i-3, j][2] + pix[i+1, j][2] + pix[i+2, j][2] + pix[i+3, j][2] + pix[i, j-1][2] + pix[i, j-2][2] + pix[i, j-3][2] + pix[i, j+1][2] + pix[i, j+2][2] + pix[i, j+3][2]
    summa = 0
    for ind in range(i - sigma, i + sigma + 1):
        if ind != i:
            summa += pix[ind, j][2]

    for ind in range(j - sigma, j + sigma + 1):
        if ind != j:
            summa += pix[i, ind][2]

    return summa / (4 * sigma)


def decoding(length_message, sigma):
    len_message = length_message
    r = 5
    image = Image.open("ans.png")
    new_pix = image.load()

    result = ''
    for i in range(0, len(res_pixels), r):
        if len_message > 0:
            temp_values = []
            for iteration in range(r):
                x = res_pixels[i+iteration][0][0]
                y = res_pixels[i+iteration][0][1]
                current_pix = new_pix[x, y]
                avg_value = count_blue_value(new_pix, x, y, sigma)
                diff = current_pix[2] - avg_value
                if diff == 0 and current_pix[2] == 255:
                    diff = 0.5
                if diff == 0 and current_pix[2] == 0:
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


def diff_pix():
    image1 = Image.open("test.jpg")
    old_pix = image1.load()
    width = image1.size[0]
    height = image1.size[1]

    image2 = Image.open("ans.png")
    new_pix = image2.load()

    summa = 0
    for i in range(width):
        for j in range(height):
            summa += (old_pix[i, j][2] - new_pix[i, j][2]) ** 2

    return [summa, width, height, new_pix]


def test_mse():
    diff = diff_pix()
    mse = float(sqrt(diff[0])) / (diff[1] * diff[2])
    print "MSE = " + str(mse)
    return mse


def test_pnsr():
    diff = diff_pix()
    summa = 0
    for i in range(diff[1]):
        for j in range(diff[2]):
            summa += diff[3][i, j][2] ** 2
    result = 20 * log(summa / diff[0], 10)
    return result


def test_percent_err(input_data, output_data):
    count = 0
    for index in range(len(output_data)):
        if input_data[index] != output_data[index]:
            count += 1
    print 'Error = ' + str(count / (1.0 * len(output_data)) * 100) + '%'
    return str(count / (1.0 * len(output_data)) * 100)


def test_dependency_on_lambda(string, sigma):
    lamdas = np.arange(0.01, 0.105, 0.01)
    errors = []
    mses = []
    for l in lamdas:
        encoding(string, l, sigma)
        out = decoding(len(string), sigma)
        errors.append(test_percent_err(string, out))
        mses.append(test_mse())

    plt.figure("Error-Lambda")
    plt.plot(lamdas, errors)
    plt.ylabel("Error")
    plt.xlabel("Lambda")

    plt.figure("MSE-Lambda")
    plt.plot(lamdas, mses)
    plt.ylabel("MSE")
    plt.xlabel("Lambda")
    # plt.show()

    return lamdas, errors


def test_dependency_on_sigma(string, lambd):
    sigmas = np.arange(1, 6, 1)
    errors = []
    mses = []
    for sigma in sigmas:
        encoding(string, lambd, sigma)
        out = decoding(len(string), sigma)
        errors.append(test_percent_err(string, out))
        mses.append(test_mse())

    plt.figure("Error-Sigma")
    plt.plot(sigmas, errors)
    plt.ylabel("Error")
    plt.xlabel("Sigma")

    plt.figure("MSE-Sigma")
    plt.plot(sigmas, mses)
    plt.ylabel("MSE")
    plt.xlabel("Sigma")
    # plt.show()

    return sigmas, errors


def start():
    input_str = '101010101111111111000000001111111111111111111111000000000000000000000000000000000000000010101010101010'

    sig = 3
    lam = 0.1
    # encoding(input_str, lam, sig)
    # out = decoding(len(input_str), sig)

    # test_percent_err(input_str, out)
    # print "PNSR = " + str(test_pnsr())

    test_dependency_on_lambda(input_str, sig)
    test_dependency_on_sigma(input_str, lam)

    plt.show()

start()
