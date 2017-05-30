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
    
        blank_array = np.array([[w=="\u3000" for w in line] for line in data])
        sep_index = np.where(np.array([all(row) for row in blank_array.T])==True)[0]
        print(blank_array.T,[all(row) for row in blank_array.T],sep_index)
        sep_index = np.append(sep_index,blank_array.shape[1])

        read_nums = []
        read_nums.append([line[0:sep_index[0]] for line in data])
        for i in range(len(sep_index)-1):
            read_nums.append([line[sep_index[i]+1:sep_index[i+1]] for line in data])

        read_num_result = []
        for read_num in read_nums:
            match_list = [k for k,v in correct_data.items() if v == read_num]
            read_num_result.append(match_list[0])

        return read_num_result


def set_write_ascis(input_nums, input_pos,input_spaces, asci_nums):
    write_data = []
    write_height = max(input_pos)+5
    for num,pos,space in zip(input_nums,input_pos,[0]+input_spaces):
        if space == 0:
            asci_num = [list(i) for i in asci_nums[num]]
        else:
            asci_num = [["\u3000"]*space + [i] for i in asci_nums[num]] # deep copy with left space

        for i in range(pos):
            asci_num.insert(0, ["\u3000"]*len(asci_num[0])) # set head space
 
        while len(asci_num) < write_height: # adjust height
            asci_num.append(["\u3000"]*len(asci_num[0]))
        
        if write_data == []:
            write_data = asci_num
        else:
            for i in range(len(write_data)):
                write_data[i].extend(asci_num[i])

    return write_data


if __name__ == "__main__":
    asci_nums = dict()
    for i in range(10):
        asci_nums[i] = read_txt(str(i))
    args = sys.argv[1].split(",")
    input_nums = [int(i) for i in args[0]]
    input_pos = [int(j) for i in range(1,len(args),2) for j in args[i]]
    input_spaces = [int(j) for i in range(2,len(args),2) for j in args[i]]

    write_data = set_write_ascis(input_nums, input_pos, input_spaces, asci_nums)

    write_txt("test",write_data)
    
    print(read_asci("test",asci_nums))
