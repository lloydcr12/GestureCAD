import pickle

x = 1

pickle_out = open("dict.pickle","wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()

n = 1
x = 1
try:
    while n==1:
        print(str(x))
        write_csv([x])
        x = x+1
except KeyboardInterrupt:
    print('stopped')