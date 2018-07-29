

def square(a, b, c):
	d = b*b + (- 4 * (c * a))
	x1 = (-b + math.sqrt(d)) / (2 * a)
	x2 = (-b - math.sqrt(d)) / (2 * a)
	return x1, x2



result = izvajdane(result, 2)
print(result)

print(square(1, 3, -4))
