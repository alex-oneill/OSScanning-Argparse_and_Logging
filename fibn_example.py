import argparse

def fib(n):
    a, b = 0, 1 
    for i in range(n):
        a, b = b, a + b
    return a
    
    
def Main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action = "store_true")
    group.add_argument("-q", "--quiet", action = "store_true")
    
    parser.add_argument("num", help = "This module calculates Fibonacci numbers " + \
                        "based on the wall known formulat.", type = int)
    # parser.add_argument("-o", "--output", help = "Insert...", action = "store_true")
    parser.add_argument("-o", "--output", help = "Compute the Fib number and " + \
                        "the result will be insert into a file.", action = "store_true")
    args = parser.parse_args()
    
    result = fib(args.num)
    # print("The "+str(args.num)+"th fib number is "+str(result))
    
    if args.verbose:
        print("The "+str(args.num)+"the fib number is "+str(result))
    elif args.quiet:
        print(result)
    else:
        print("Fib("+str(args.num)+") = " + str(result))
    
    if args.output:
        f = open("fibonacci.txt", "a")
        f.write(str(result) + '\n')
        
if __name__ == "__main__":
    Main()