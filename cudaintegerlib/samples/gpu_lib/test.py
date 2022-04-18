# import cuda_my_add
import sys
import time
import gmpy2

sys.path.append('./build')
import gpu_lib as gpu_cal

BITS = 2048


def to_32bit_binary_array(value: int):
    binary_str = bin(value)[2:]
    if len(binary_str) < BITS:
        binary_str = '0' * (BITS - len(binary_str)) + binary_str
    return binary_str


def to_32bit_int_array(value: int):
    binary_str = to_32bit_binary_array(value)
    # print(binary_str)
    result = []
    step = 32
    for i in range(0, len(binary_str), step):
        item_binary = binary_str[i:i + step]
        result.append(int(item_binary, 2))
    return result


def get_32bit_int_array(value: int):
    max_len = int(BITS / 32)
    result = [0] * max_len
    for i in range(max_len):
        if i > 0:
            value = value >> 32
        # result[max_len-i-1]=value & 0xffffffff
        result[i] = value & 0xffffffff

        # result.append(value & 0xffffffff)
    result.reverse()
    return result


def binary_array_to_pyint(value):
    pass


P = 3121551
Q = 11907246841353856953000737686416683990159472723163358934580534921772522564355009335878040841468065064013380393376377185905002534476062522959451900175351626
M = 141782527340931403452693053317696384382978668452649821765342352751649830223483053769539514791952315698099911040344999764316375778263746977924220680392292666375145707381314572022941882248599295999397614518959786261540094038843693421278686011091045965453689494808349096995191142933860322939491417230793091547129


def generate_big_number():
    pass


def powmod(a, b, c):
    return int(gmpy2.powmod(a, b, c))


TOTAL = 50000
BATCH_SIZE = 50000


def gpu_cal_time():
    start = time.time()

    batch_param = []

    for i in range(TOTAL):
        p = get_32bit_int_array(P)
        q = get_32bit_int_array(Q)
        m = get_32bit_int_array(M)
        batch_param.append(gpu_cal.powmod_param_int(p, q, m))
        if len(batch_param) == BATCH_SIZE:
            print(f'param_time:{time.time() - start}')
    print(f'gpu consume time:{time.time() - start}')


def deal_item(p, q, m):
    a = get_32bit_int_array(p)
    b = get_32bit_int_array(q)
    c = get_32bit_int_array(m)
    return (a, b, c)


def gpu_param_test():
    start = time.time()
    batch_param = []

    for i in range(TOTAL):

        batch_param.append((str(P), str(Q), str(M)))
        if len(batch_param) == BATCH_SIZE:
            print(f'param_time:{time.time() - start}')

            # result = gpu_cal.add_test()
            result = gpu_cal.powm_param_test(batch_param, len(batch_param))
            print(f'gpu_result_len:{result}')
            batch_param = []
    if batch_param:
        result = gpu_cal.powm_2048(batch_param, len(batch_param))
        print(f'gpu_result_len:{len(result)}')
        batch_param = []

    print(f'gpu consume time:{time.time() - start}')


def gpu_param_test2():
    print("enter test2")
    # powm_param_test
    start = time.time()
    batch_param = []

    p = get_32bit_int_array(P)
    q = get_32bit_int_array(Q)
    m = get_32bit_int_array(M)

    for i in range(TOTAL):
        # pool.apply_async()

        # batch_param.append((str(P),str(Q),str(M)))
        # batch_param.append((P,Q,M))
        # batch_param.append((p,q,m))
        batch_param.extend(p)
        batch_param.extend(q)
        batch_param.extend(m)

        if len(batch_param) == BATCH_SIZE * 3 * 64:
            print(f'param_time:{time.time() - start}')

            # result = gpu_cal.add_test()
            result = gpu_cal.powm_param_test2(batch_param, len(batch_param))
            print(f'gpu_result_len:{result}')
            batch_param = []
    # if batch_param:
    #     result = gpu_cal.powm_2048(batch_param, len(batch_param))
    #     print(f'gpu_result_len:{len(result)}')
    #     batch_param = []

    print(f'gpu consume time:{time.time() - start}')


def gpu_param_test4():
    TOTAL = 100
    
    start = time.time()
    for i in range(TOTAL):
        batch_param = []
        p_bytes = P.to_bytes(256, "little")
        q_bytes = Q.to_bytes(256, "little")
        m_bytes = M.to_bytes(256, "little")
        batch_param.append((p_bytes, q_bytes, m_bytes))
        if i == 0:
            print("p", int.from_bytes(p_bytes[0:4], "little"))
            print("q", int.from_bytes(q_bytes[0:4], "little"))
            print("m", int.from_bytes(m_bytes[0:4], "little"))

        result = gpu_cal.powm_2048(batch_param, len(batch_param))
    #print(result)
    print(int.from_bytes(result[0], "little"))
    print(f'gpu consume time4:{time.time() - start}')


def cpu_cal_time():
    start = time.time()
    for i in range(TOTAL):
        r = powmod(P, Q, M)
        #print(r)
    print(f'cpu consume time:{time.time() - start}')


if __name__ == '__main__':
    start = time.time()
    #cpu_cal_time()
    gpu_param_test4()
