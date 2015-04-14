
def decorator(test_func):
    def wrapper():
        test_func()
        print 'decorator is working'
    return wrapper

@decorator
def test_func():
    print 'hello world'
    
test_func()
