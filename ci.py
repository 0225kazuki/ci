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

        #data_list=[]
        #for line in data:
        #    data_list.append([w=="\u3000" for w in line])
        #data_array = np.array(data_list)
        #
        #sep_index=[]
        #for i in range(data_array.shape[1]):
        #    if all(data_array[:,i]):
        #        sep_index.append(i)
        #sep_index.append(data_array.shape[1])

        blank_array = np.array([[w=="\u3000" for w in line] for line in data])
        sep_index = np.where(np.array([all(row) for row in blank_array.T])==True)[0]
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

if __name__ == "__main__":
    asci_nums = dict()
    for i in range(10):
        asci_nums[i] = read_txt(str(i))

    input_nums = [int(i) for i in sys.argv[1]]

    write_data = [i for i in asci_nums[input_nums[0]]]
    for input_num in input_nums[1:]:
        for i in range(len(asci_nums[input_num])):
            write_data[i] += "\u3000" + asci_nums[input_num][i]

    print(write_data)
    write_txt("test",write_data)

    print(read_asci("test",asci_nums))
