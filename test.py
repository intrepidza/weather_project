def test_deco(msg):
    def inner_deco(func):
        def wrapper(a, b):
            lst = ['begin', 'end']
            print('test')
            print(msg + ' - ' + lst[0])
            func(a, b)
            print('end')
            print(msg + ' - ' +  lst[1])
        return wrapper
    return inner_deco

@test_deco('blahblah')
def test_func(a, b):
    print(a, b)

test_func(1, 2)