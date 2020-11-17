import random

def des_encrypt(realText, step):
    outText = []
    uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for eachChar in realText:
        if eachChar in uppercase:
            index = uppercase.index(eachChar)
            crypting = (index + step) % 26
            newChar = uppercase[crypting]
            outText.append(newChar)

        elif eachChar in  digits:
            index = digits.index(eachChar)
            crypting = (index - step) % 10
            newChar = digits[crypting]
            outText.append(newChar)

        else:
            newChar = eachChar
            outText.append(newChar)

    random.shuffle(outText)

    return outText