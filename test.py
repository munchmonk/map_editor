#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

# m x n, m = 3, n = 2
# iterate n first, m second

a = [[0] * 3 for i in range(2)]
a[0][1] = 5

print(a)

for i in range(2):
	for j in range(3):
		print(a[i][j])
	print('')

