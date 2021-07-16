import pickle

try:
    with open("file.pickle", mode="rb") as fileObj:
        obj=pickle.load(fileObj)

        print(obj)

except KeyboardInterrupt:
    print('stopped')