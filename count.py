from datetime import datetime

def factorize(*numbers):
    return [[i for i in range(1, num+1) if not num % i] for num in numbers]

if __name__ == '__main__':
    st = datetime.now()
    factorize(128, 255, 99999, 10651060)
    print(datetime.now()-st)
