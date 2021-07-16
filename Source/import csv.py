import csv

def write_csv(data):
    with open('example.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)
n = 1
x = 1
try:
    while n==1:
        print(str(x))
        write_csv([x])
        x = x+1
except KeyboardInterrupt:
    print('stopped')

