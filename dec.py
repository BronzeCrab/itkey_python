#Testing how decorator working

def decorator(test_func):
	def wrapper():
		try:
			test_func() 
		finally:
			print 'decorator is working'	    
	return wrapper

@decorator
def test_func():
	print 'hello world'
	raise Exception

test_func()


