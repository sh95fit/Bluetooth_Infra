from datetime import datetime


def data_parser(message):
    data = {
        "device_id": int(message[0:2], 16),
        "outar": int(message[8:12], 16)/10,
        "outas": int(message[12:16], 16)/10,
        "outat": int(message[16:20], 16)/10,
        "outvrs": int(message[20:24], 16),
        "outvst": int(message[24:28], 16),
        "outvtr": int(message[28:32], 16),
        "tpg": int(message[32:40], 16)/100,
        "operation": int(message[40:44], 16),
        "message": int(message[44:52], 16),
        "cpg": int(message[52:60], 16),
        "ina1": int(message[60:64], 16)/10,
        "inv1": int(message[64:68], 16),
        "ina2": int(message[68:72], 16)/10,
        "inv2": int(message[72:76], 16),
        "ina3": int(message[76:80], 16)/10,
        "inv3": int(message[80:84], 16),
        "ina4": int(message[84:88], 16)/10,
        "inv4": int(message[88:92], 16),
        "ina5": int(message[92:96], 16)/10,
        "inv5": int(message[96:100], 16),
        "ina6": int(message[100:104], 16)/10,
        "inv6": int(message[104:108], 16),
        "temp": int(message[108:112], 16),
        "fr": int(message[112:116], 16),
        "savetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    # print(data)

    return data
