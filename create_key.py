import pyotp
import base64
import time
import hashlib
import binascii
from gmssl import sm4,sm3


def truncate_hash(hex_hash):
    # 将十六进制的hash值转换为字节串
    hash_bytes = binascii.unhexlify(hex_hash.encode())

    # 定义S1到S8，并根据算法赋值
    S1 = (hash_bytes[0] << 24) | (hash_bytes[1] << 16) | (hash_bytes[2] << 8) | hash_bytes[3]
    S2 = (hash_bytes[4] << 24) | (hash_bytes[5] << 16) | (hash_bytes[6] << 8) | hash_bytes[7]
    S3 = (hash_bytes[8] << 24) | (hash_bytes[9] << 16) | (hash_bytes[10] << 8) | hash_bytes[11]
    S4 = (hash_bytes[12] << 24) | (hash_bytes[13] << 16) | (hash_bytes[14] << 8) | hash_bytes[15]
    S5 = (hash_bytes[16] << 24) | (hash_bytes[17] << 16) | (hash_bytes[18] << 8) | hash_bytes[19]
    S6 = (hash_bytes[20] << 24) | (hash_bytes[21] << 16) | (hash_bytes[22] << 8) | hash_bytes[23]
    S7 = (hash_bytes[24] << 24) | (hash_bytes[25] << 16) | (hash_bytes[26] << 8) | hash_bytes[27]
    S8 = (hash_bytes[28] << 24) | (hash_bytes[29] << 16) | (hash_bytes[30] << 8) | hash_bytes[31]

    # 计算OD并取模
    OD = (S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8) % (2**32)

    return OD

# 用户账号密码库
def userlist(file_path: str) -> dict:
    user_database = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password = line.strip().split(':')
            user_database[username] = {"password": password}
    return user_database


def create_key(username: str, password: str) -> str:
    seed = username + password
    timestamp = int(time.time()/30)
    timestamp_bytes = timestamp.to_bytes(8, 'big')
    key=seed + str(bytearray(timestamp_bytes))
    return key.encode()

def creat_dynamic_password(username: str, password: str) -> str:
    # 生成密钥
    secret_key = create_key(username, password)
    
    # 使用共享密钥生成TOTP对象
    hash_value = sm3.sm3_hash(secret_key)

    hex_hash = binascii.hexlify(hash_value.encode()).decode()
    print(hex_hash)
    #截位函数
    od=truncate_hash(hex_hash)
    p=od % (pow(10,6))
    if p<10:
        p='00000'+str(p)
    elif p<100:
        p='0000'+str(p)
    elif p<1000:
        p='000'+ str(p)
    elif p<10000:
        p='00'+str(p)
    elif p<100000:
        p='0'+str(p)
    else:
        p=str(p)
    return p

if __name__ == '__main__':
    user_database = userlist("user.txt")
    
    while True:
        with open('user1.txt', 'w') as file:
            for username, user_info in user_database.items():
                password = user_info["password"]
                dynamic_password = creat_dynamic_password(username, password)
                file.write(f"{username}:{password}:{dynamic_password}\n")
                print(f"用户 '{username}' 的动态口令：{dynamic_password}")
            print('---------------------------------------')
        time.sleep(30)