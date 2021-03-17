from PIL import Image
import math


def dec_to_bin(x):
    l = []
    for i in range(8):
        if x % 2 == 0:
            l.append(0)
        else:
            l.append(1)
        x = x//2

    l.reverse()
      
    return l

def bin_to_dec(l):
    res = 0
    for i in range(8):
        if l[i] == 1:
            res = res + 2**(7-i)

    return res

def manipulate_image(img, message):
    pixelMap = img.convert('RGB').load()
    pixelamount = img.size[0] * img.size[1]
    msglength = len(message)
    bitamount = 1
    stride = 1
    if msglength > pixelamount:
        bitamount = math.ceil(msglength / pixelamount)
        stride = math.floor(pixelamount/(msglength/bitamount))
    else:
        stride = math.floor(pixelamount/msglength)

    imgNew = Image.new('RGB', img.size)
    pixelNew = imgNew.load()
    count = 0

    for i in range(img.size[1]):
        for j in range(img.size[0]):
            if len(message) > 0:
                count = count + 1
                if count == stride:
                    count = 0
                    binlist = dec_to_bin(pixelMap[j,i][2])
                    if len(message) < bitamount:
                         bitamount = len(message)
                    for k in range(bitamount):
                        binlist[7-k] = int(message[bitamount-1-k])
                    pixelNew[j,i] = (pixelMap[j,i][0], pixelMap[j,i][1], bin_to_dec(binlist))
                    #pixelNew[j,i] = (0, 0, 0)
                    message = message[bitamount:]
                else:
                    pixelNew[j,i] = pixelMap[j,i]
            else:
                pixelNew[j,i] = pixelMap[j,i]

    imgNew.save("out.png")

    
    imgNew.close()
    return
                    
def decrypt(img, msglength):
    pixelMap = img.load()
    pixelamount = img.size[0] * img.size[1]
    bitamount = 1
    stride = 1
    if msglength > pixelamount:
        bitamount = math.ceil(msglength / pixelamount)
        stride = math.floor(pixelamount / (msglength / bitamount))
    else:
        stride = math.floor(pixelamount / msglength)

    message = ''
    count = 0
    bytecount = 0
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            if msglength != 0:
                count = count + 1
                if count == stride:
                    count = 0
                    binlist = dec_to_bin(pixelMap[j,i][2])
                    if msglength == 1 and (bytecount + bitamount) > 8:
                        bitamount = 8 - bytecount
                    for k in range(bitamount):
                        message = message + str(binlist[7-bitamount+k+1])
                    bytecount = bytecount + bitamount
                    if bytecount >= 8:
                        bytecount = bytecount - 8
                        msglength = msglength - 1

    result = ''
    char = ''
    bytecount = 0
    if len(message) % 8 == 0:
        for i in range(len(message)):
            char = char + message[i]
            bytecount = bytecount + 1
            if bytecount == 8:
                result = result + chr(int(char, 2))
                char = ''
                bytecount = 0
                                         
    return result
    
def create_Message(string):
    b = ' '.join(map(bin,bytearray(string,'utf8'))).replace("0b", '')

    blist = b.split(' ')

    count = 0
    for i in blist:
        size = len(i)
        if size < 8:
            for j in range(8-size):
                i = '0' + i
        blist[count] = i
        count = count + 1

    message = ''.join(blist)
    return message




img = Image.open('Image.png')
message = create_Message("hidden message")
manipulate_image(img, message)
img.close()

imge = Image.open('out.png')
msglength = len(message)
result = decrypt(imge, msglength)
print(result)
print(msglength)

