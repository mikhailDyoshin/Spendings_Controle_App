import math


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 1) / multiplier

def round_up(number:float) -> float:
    """
        Rounds a number 
        to the penultimate exponent 
        that is in the number.
    """

    parts = str(number).split('.')

    if len(parts) == 1:
        if number < 10:
            return number
        
        return int(round_half_up(number, -1))
    
    nFracts = len(parts[1])
    return round_half_up(number, nFracts-1)
    

# numbers = list(range(100))
numbers = [n/100 for n in range(100)]

for number in numbers:
    print(f'{number} --> {round_up(number)}')
    # print(round_half_up(number, -1))
