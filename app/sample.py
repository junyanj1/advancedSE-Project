def simply_add(a, b):
    """Simple function for test"""
    if type(a) is not int or type(b) is not int:
        raise TypeError('Inputs must be int')
    return a + b

def simply_multiply(a, b):
    """Simple function for test"""
    if type(a) is not int or type(b) is not int:
        raise TypeError('Inputs must be int')
    return a * b
