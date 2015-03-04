import numpy

maxtemp = 50*10
mintemp = 5*10



def array16():
  arr = numpy.random.randint(mintemp, maxtemp, 16)
  return arr

arr = array16()
print arr


# gives a boolean array if the temp of pixel is over a certain degree
def somebody(arr):
  a = numpy.zeros(16)
  deg = 30
  for i in range(len(arr)):
    if (arr[i] >= deg*10):
      a[i] = 1;
  
  return a

a = somebody(arr)

print a 

#returns a boolean if the sum of boolean data is over 5
def there(a):
    if (sum(a) > 5):
        return 1
    else: 
        return 0

print there(a)
    

