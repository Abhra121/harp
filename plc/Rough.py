from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import encode_ieee, decode_ieee, \
    long_list_to_word, word_list_to_long

import ssl

import subprocess
import json

context = ssl.create_default_context()

global write

global R
R = []


def read_float(cl, address, number=1):
    reg_l = cl.read_holding_registers(address, number * 2)
    if reg_l:
        return [decode_ieee(f) for f in word_list_to_long(reg_l)]
    else:
        return None


def getmac(command):
    return subprocess.check_output(command, shell=True)


def floatC(reg5):
    global f
    f = []
    s = ""
    for i in range(len(reg5)):
        try:

            s = [str(ft) for ft in reg5[i]]

            a_string = "".join(s)

            res = str(a_string)

            f.append(res)

        except Exception as x:
            print(x)

    res = list(filter(lambda item: item is not None, f))
    return (res)


def intC(reg91):
    global t
    t = []
    ss = ""

    for i in range(len(reg91)):
        try:

            ss = [str(ft) for ft in reg91[i]]
            a_string = "".join(ss)

            ress = str(a_string)

            t.append(ress)
        except Exception as x:
            print(x)

    res = list(filter(lambda item: item is not None, t))
    return (res)


def Cloning(li1):
    li_copy = li1[:]
    return li_copy


def unique(list1):
    global unique_list
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)


def CountFrequency(my_list):
    freq = {}
    R.clear()
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    for key, value in freq.items():
        R.append(int(value))


def CountIndex(my_list, element):
    global I
    I = []
    index = my_list.index(element)
    return index


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


def pop(la, number):
    if (number == 16):
        la = la
    if (number < 16):
        del la[number:16]

    return la


def parse_msg():
    try:
        with open('/home/pi/harp/dummy_data/sample.json', 'r') as openfile:
            m_in = json.load(openfile)

        global m
        m = 0
        for key in m_in:
            m = m + 1

        global datT
        datT = []
        global name
        name = []
        global alarmID
        alarmID = []
        name = []
        add = []

        price = ""
        price1 = ""
        price2 = ""
        price3 = ""
        n = 0

        for item in m_in.items():

            price = m_in['object' + str(n)]['ParameterName']
            price1 = m_in['object' + str(n)]['Address']
            price2 = m_in['object' + str(n)]['DataType']
            price3 = m_in['object' + str(n)]['AlarmID']
            name.append(price)
            add.append(price1)
            datT.append(price2)
            alarmID.append(price3)
            if (n < (m - 2)):
                n = n + 1

        name = name[:-1]
        add = add[:-1]
        datT = datT[:-1]
        alarmID = alarmID[:-1]

        CountFrequency(add)
        global index1
        index1 = []
        global index2
        index2 = []
        q = 0
        unique(add)
        global res5

        res5 = [eval(i) for i in unique_list]

        res5 = list(map(lambda x: x - 1, res5))

        l = CountIndex(add, unique_list[3])
        values1 = range(len(unique_list))
        for i in values1:
            l = CountIndex(add, unique_list[i])
            index1.append(l)
        for j in index1:
            res = ""
            res = datT[j]
            index2.append(res)
        res2 = [eval(i) for i in index2]

        global R1
        R1 = []
        for i in range(len(R)):
            if R[i] > 1:
                R1.append(R[i])
        length = len(unique_list)

        global float2
        float2 = []
        global boolean2
        global int2
        u16 = 0

        length2 = len(res5)
        float2.clear()
        boolean2.clear()
        int2.clear()

        for i in range(length):
            if (res2[i] == 3):
                float2.append(res5[i])

            if (res2[i] == 2):
                boolean2.append(res5[i])

            if (res2[i] == 1):
                int2.append(res5[i])
        global float_l
        float_l = len(float2)
        global bool_l
        bool_l = len(boolean2)
        global integer_l
        integer_l = len(int2)


    except FileNotFoundError:
        print('File does not exist')


def test_function_ss(c):
    global R
    global float2
    global boolean2
    global int2
    global float_l
    global bool_l
    global integer_l
    global name
    global alarmID
    global R1
    global Dict

    f = open('/home/pi/hardwareid.txt', 'r')
    data = f.read()
    f.close()
    defaultid = int(data)

    write = 0
    boolean2 = []
    int2 = []
    float2 = []
    float_l = 0
    bool_l = 0
    integer_l = 0
    ID = ""
    R = []
    R1 = []
    name = []
    alarmID = []
    Dict = {"HardWareID": defaultid}
    parse_msg()

    l = bool_l
    Float = []

    for i in range(float_l):
        Float.append(read_float(c, float2[i], 1))
    Float = floatC(Float)

    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0
    reg5 = []
    Integer = []

    if len(int2) != 0:
        for i in range(integer_l):
            Integer.append(c.read_holding_registers(int2[i], 1))
        Integer = intC(Integer)

    if len(boolean2) == 0:
        
        final =  Float

        n = 1
        for i in range(len(name)):
            Dict["object" + str(i)] = {}

        for i in range(len(name)):
            try:

                Dict["object" + str(i)]['Description'] = "111"
                Dict["object" + str(i)]['ParameterName'] = name[i]
                Dict["object" + str(i)]['value'] = final[i]
                Dict["object" + str(i)]['AlarmID'] = alarmID[i]

            except Exception as x:
                print(x)

    payload = json.dumps(Dict)

    with open("/home/pi/harp/dummy_data/payload.json", "w") as outfile:
        json.dump(payload, outfile)
    return payload
