import timeit
import random
from eval import eval

if __name__ == "__main__":
    # generate random choices
    choices = [random.randint(-3, 3) for _ in range(60)]
    print(choices)
    result_name = "result"
    # timeit
    print(timeit.timeit(lambda: eval(choices, result_name), number=1))