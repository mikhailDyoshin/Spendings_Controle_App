from handy import get_quotient_and_remainder, reverse_tuple


rects = list(range(371))

dates = list(range(371))



rectsTuples = [reverse_tuple(get_quotient_and_remainder(rect, 53)) for rect in rects]
datesTuples = [get_quotient_and_remainder(date, 7) for date in dates]

print(rectsTuples[:54])
print(datesTuples[:54])