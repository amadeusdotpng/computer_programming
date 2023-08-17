

def sift_down(array,index):
	L=index*2+1
	R=index*2+2
	biggest_index=index
	if L<len(array) and array[L]>array[biggest_index]:
		biggest_index=L
	if R<len(array) and array[R]>array[biggest_index]:
		biggest_index=R
	if index!=biggest_index:
		array[biggest_index],array[index]=array[index],array[biggest_index]
		sift_down(array,biggest_index)

def heapify(m):
	for i in reversed(range(len(m)//2+1)):
		sift_down(m,i)

def heapsort(m):
	heapify(m)
	out=[]
	while m:
		out.insert(0,m[0])
		v=m.pop()
		if m:
			m[0]=v
			sift_down(m,0)
	return out
	
	
10
maxindex=9
lastparent=4

m=list(range(20))
import random
random.seed(0)
random.shuffle(m)

print(m)
input()
heapify(m)
print(m)
print(heapsort(m))
	
