import pickle

n=1
obj = 2021

try:
    while n == 1:
        with open("file.pickle", mode="wb") as fileObj:
            pickle.dump(obj, fileObj, protocol=2)
        obj = obj+1
        print str(obj)

except KeyboardInterrupt:
    print('stopped')