prior = tuple()
trans = tuple()
emission = tuple()
q_type = ""
query = list()
k = -1

def norm(nums):
    sum_num = sum(nums)
    factor = 1 / sum_num
    norm_array = [num * factor for num in nums]
    return norm_array

def add_vectors(vector1, vector2):
    return [vector1[0] + vector2[0], vector1[1] + vector2[1]]

def mult_vectors(vector1, vector2):
    return [vector1[0] * vector2[0], vector1[1] * vector2[1]]

def scalar_mult(nums, x):
    return [nums[0]*x, nums[1]*x]

def select_sensor_col(is_umbrella):
    if is_umbrella:
        sensor_trans = [row[0] for row in emission]
    else:
        sensor_trans = [row[1] for row in emission]
    return sensor_trans

def forward_recursion(nums, normalize):
    is_umbrella = nums[-1]
    sensor_trans = select_sensor_col(is_umbrella)

    if len(nums) == 1:
        prev = prior
    else:
        prev = forward_recursion(nums[:-1], normalize)

    rain = scalar_mult(trans[0], prev[0])
    no_rain = scalar_mult(trans[1], prev[1])
    base = add_vectors(rain, no_rain)
    if normalize:
        return norm(mult_vectors(base, sensor_trans))
    else:
        return mult_vectors(base, sensor_trans)

def backward_recursion(nums):
    is_umbrella = nums[0]
    sensor_trans = select_sensor_col(is_umbrella)

    rain_col = [row[0] for row in trans]
    no_rain_col = [row[1] for row in trans]
    rain = scalar_mult(rain_col, sensor_trans[0])
    no_rain = scalar_mult(no_rain_col, sensor_trans[1])

    if len(nums) > 1:
        prev = backward_recursion(nums[1:])
        rain = scalar_mult(rain, prev[0])
        no_rain = scalar_mult(no_rain, prev[1])

    return add_vectors(rain, no_rain)

def mle(nums):
    if len(nums) == 1:
        return [forward_recursion(nums, True)]

    is_umbrella = nums[-1]
    sensor_trans = select_sensor_col(is_umbrella)

    return_list = mle(nums[:-1])
    prev = return_list[-1]
    value = max(prev)
    flag = prev.index(value) != 0
    rain_trans = trans[int(flag)]

    left = sensor_trans[0] * value * rain_trans[0]
    right = sensor_trans[1] * value * rain_trans[1]
    result = [left, right]
    return_list.append(result)
    return return_list

def smoothing():
    forward = query[:k]
    backward = query[k:]
    f_result = forward_recursion(forward, False)
    b_result = backward_recursion(backward)
    final_result = norm(mult_vectors(f_result, b_result))
    return final_result

def call_and_return_function():
    if q_type == 'S':
        return smoothing()
    elif q_type == 'F':
        return forward_recursion(query, True)
    elif q_type == 'L':
        return forward_recursion(query, False)
    elif q_type == 'M':
        return mle(query)

def print_formatted_output(return_val):
    if q_type == 'M':
        formatted_bool = "[" + " ".join("T" if elem[0] >= elem[1] else "F" for elem in return_val) + "]"
        formatted_values = "[" + ", ".join(["<{:.2f}, {:.2f}>".format(*elem) for elem in return_val]) + "]"
        formatted_string = formatted_bool + " " + formatted_values
    elif q_type == 'L':
        formatted_string = "{:.2f}".format(sum(return_val))
    else:
        formatted_string = "<{:.2f}, {:.2f}>".format(*return_val)

    print(formatted_string)

def read_and_arrange_input():

    # example : 0.34 0.42 0.56 0.13 0.81 S [T F F T F]

    global prior
    global trans
    global emission
    global q_type
    global query
    global k

    try:
        # take the input
        inp_arr = input().split()

        # assign the prior table
        prior_true = float(inp_arr[0])
        prior = (prior_true, 1 - prior_true)

        # assign the trans table
        trans_r_to_r = float(inp_arr[1])
        trans_no_r_to_r = float(inp_arr[2])
        first_row_t = (trans_r_to_r, 1-trans_r_to_r)
        sec_row_t = (trans_no_r_to_r, 1-trans_no_r_to_r)
        trans = (first_row_t, sec_row_t)

        # assign the emission table
        emission_r_to_u = float(inp_arr[3])
        emission_no_r_to_u = float(inp_arr[4])
        first_row_e = (emission_r_to_u, 1-emission_r_to_u)
        sec_row_e = (emission_no_r_to_u, 1-emission_no_r_to_u)
        emission = (first_row_e, sec_row_e)

        # assign the query type
        q_type = inp_arr[5]

        # assign the query
        if q_type == 'S':
            k = int(inp_arr[-1])
            inp_arr = inp_arr[:-1]

        query_str = inp_arr[6:]
        for string in query_str:
            if '[' in string:
                flag = string[1] == 'T'
            elif ']' in string:
                flag = string[0] == 'T'
            else:
                flag = string == 'T'
            query.append(flag)

    except:
        print("Forbidden input format.")

def main():
    read_and_arrange_input()
    result = call_and_return_function()
    print_formatted_output(result)



if __name__ == "__main__":
    main()