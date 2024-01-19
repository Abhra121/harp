import json
from pyModbusTCP.utils import encode_ieee, long_list_to_word


def write_float(client, address, floats_list):
    b32_l = [encode_ieee(f) for f in floats_list]
    b16_l = long_list_to_word(b32_l)
    return client.write_multiple_registers(address, b16_l)


def get_hw_id():
    with open('/home/pi/hardwareid.txt', 'r') as f:
        HwId = f.read()
    return int(HwId)


def convert_back(bin_num):
    value = 0

    n = list(bin_num)

    if n[0] == '1':
        value = value + (2 ** 15)
    if n[1] == '1':
        value = value + (2 ** 14)
    if n[2] == '1':
        value = value + (2 ** 13)
    if n[3] == '1':
        value = value + (2 ** 12)
    if n[4] == '1':
        value = value + (2 ** 11)
    if n[5] == '1':
        value = value + (2 ** 10)
    if n[6] == '1':
        value = value + (2 ** 9)
    if n[7] == '1':
        value = value + (2 ** 8)
    if n[8] == '1':
        value = value + (2 ** 7)
    if n[9] == '1':
        value = value + (2 ** 6)
    if n[10] == '1':
        value = value + (2 ** 5)
    if n[11] == '1':
        value = value + (2 ** 4)
    if n[12] == '1':
        value = value + (2 ** 3)
    if n[13] == '1':
        value = value + (2 ** 2)
    if n[14] == '1':
        value = value + (2 ** 1)
    if n[15] == '1':
        value = value + (2 ** 0)

    # print(value)

    return value


def arrange(res):
    global a
    a = []
    a.append(res[-9])
    a.append(res[-10])
    a.append(res[-11])
    a.append(res[-12])

    a.append(res[-13])
    a.append(res[-14])
    a.append(res[-15])
    a.append(res[-16])

    a.append(res[-1])
    a.append(res[-2])
    a.append(res[-3])
    a.append(res[-4])

    a.append(res[-5])
    a.append(res[-6])
    a.append(res[-7])
    a.append(res[-8])

    return a


def process_web_hw_status(msg, c, log):
    m_decode = str(msg.payload.decode("UTF-8", "ignore"))
    data = json.loads(m_decode)
    log.info(f'From Write fn RAW data - {data}')
    ID = data['HardwareID']
    log.info(f'From Write fn HW- {ID}')
    log.info(f'From local {get_hw_id()}')

    if get_hw_id() == ID:
        if data['object']['DataType'] == "1":
            tag_i = data['object']['Value']
            ad_i = data['object']['Address']
            tag_I = int(tag_i)
            ad_I = int(ad_i)
            ad_I = ad_I - 1
            c.write_single_register(ad_I, tag_I)
        if data['object']['DataType'] == '3':
            tag_i = data['object']['Value']
            ad_i = data['object']['Address']
            tag_1 = float(tag_i)
            ad_1 = int(ad_i)
            ad_1 = ad_1 - 1
            write_float(c, ad_1, [tag_1])

        if data['object']['DataType'] == '2':
            maskW = []
            tagB = data['object']['Value']
            ad_B = data['object']['Address']
            maskW = data['object']['Mask']
            maskW = int(maskW)
            print(maskW)

            ad_b = int(ad_B)
            tagb = int(tagB)
            print(tagb)
            ad_b = ad_b - 1

            regs_l = c.read_holding_registers(ad_b, 1)

            try:
                
                integer = int(regs_l[0])
    
                binary = bin(integer)
    
                regs_1_bin = str(format(integer, '016b'))
    
                res = []
    
                for x in range(16):
                    res.append(regs_1_bin[x])
    
                lis = [eval(i) for i in res]
    
                r1 = res[0] + res[1] + res[2] + res[3] + res[4] + res[5] + res[6] + res[7] + res[8] + res[9] + res[10] + \
                     res[11] + res[12] + res[13] + res[14] + res[15]
    
                if (maskW == 256):
                    lis[7] = tagb
                if (maskW == 512):
                    lis[6] = tagb
                if (maskW == 1024):
                    lis[5] = tagb
                if (maskW == 2048):
                    lis[4] = tagb
    
                if (maskW == 4096):
                    lis[3] = tagb
                if (maskW == 8192):
                    lis[2] = tagb
                if (maskW == 16384):
                    lis[1] = tagb
                if (maskW == 32768):
                    lis[0] = tagb
    
                if (maskW == 1):
                    lis[15] = tagb
                if (maskW == 2):
                    lis[14] = tagb
                if (maskW == 4):
                    lis[13] = tagb
                if (maskW == 8):
                    lis[12] = tagb
    
                if (maskW == 16):
                    lis[11] = tagb
                if (maskW == 32):
                    lis[10] = tagb
                if (maskW == 64):
                    lis[9] = tagb
                if (maskW == 128):
                    lis[8] = tagb
    
                r1_new = ""
    
                r1_new = str(lis[0]) + str(lis[1]) + str(lis[2]) + str(lis[3]) + str(lis[4]) + str(lis[5]) + str(
                    lis[6]) + str(lis[7]) + str(lis[8]) + str(lis[9]) + str(lis[10]) + str(lis[11]) + str(lis[12]) + str(
                    lis[13]) + str(lis[14]) + str(lis[15])
    
                convert_back(r1_new)
                reg_value = convert_back(r1_new)
                new = 0
                ad = 0
                c.write_single_register(ad_b, reg_value)
            except Exception as x:
                print(x)
