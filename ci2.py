import sys
import numpy as np

def read_txt(file_name):
    with open(file_name,'r') as f:
        read_data = []
        line = f.readline()
        while line:
            read_data.append(line[:-1])
            line = f.readline()
    return read_data


def write_txt(file_name,write_data):
    with open(file_name,'w') as f:
        for i in range(len(write_data)):
            for w in write_data[i]:
                f.write(w)
            f.write('\n')


def read_asci(file_name, correct_data):
    with open(file_name,'r') as f:
        data = f.readlines()
        data = [i[:-1] for i in data]

        # find blank row index
        blank_array = np.array([[w=="\u3000" for w in line] for line in data])
        blank_index = np.where(np.array([all(row) for row in blank_array.T])==True)[0]

        # find number position from blank index
        num_end = [blank_index[0]] + [i for i,j in zip(blank_index[1:],blank_index[:-1]) if i-1 != j]
        num_start = [i for i,j in zip(blank_index[:-1],blank_index[1:]) if i+1 != j] + [blank_index[-1]]
        num_end = num_end + [blank_array.shape[1]]
        num_start = [-1] + num_start

        # parse asci
        read_nums = []
        for st,en in zip(num_start,num_end):
            read_nums.append([line[st+1:en] for line in data if not all( [j=="\u3000" for j in line[st+1:en]] )])

        # num check
        read_num_result = []
        for read_num in read_nums:
            match_list = [k for k,v in correct_data.items() if v == read_num]
            read_num_result += match_list

        return read_num_result


def set_write_ascis(input_nums, input_pos,input_spaces, asci_nums):
    write_data = []
    write_height = max(input_pos)+5
    for num,pos,space in zip(input_nums,input_pos,[0]+input_spaces):
        if space == 0: # deep copy with left space
            asci_num = [i for i in asci_nums[num]]
        else:
            asci_num = ["\u3000"*space + i for i in asci_nums[num]]

        for i in range(pos): # set head space
            asci_num.insert(0, "\u3000"*len(asci_num[0]))

        while len(asci_num) < write_height: # adjust height
            asci_num.append("\u3000"*len(asci_num[0]))

        if write_data == []:
            write_data = asci_num
        else:
            for i in range(len(write_data)):
                write_data[i] += asci_num[i]

    return write_data


if __name__ == "__main__":
    # load asci numbers
    asci_nums = dict()
    for i in range(10):
        asci_nums[i] = read_txt(str(i))

    # parse args
    args = sys.argv[1].split(",")
    input_nums = [int(i) for i in args[0]]
    input_pos = [int(j) for i in range(1,len(args),2) for j in args[i]]
    input_spaces = [int(j) for i in range(2,len(args),2) for j in args[i]]

    if len(input_nums) != len(input_pos) or len(input_pos) != len(input_spaces):
        print("arg error");exit()

    # write and read
    write_data = set_write_ascis(input_nums, input_pos, input_spaces, asci_nums)
    write_txt("test",write_data)

    print(read_asci("test",asci_nums))
