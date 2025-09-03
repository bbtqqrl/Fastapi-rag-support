def x():
    a = 1 / 0
    return a

def y():
    try:
        result = x()
        return result
    except Exception as e:
        print(e) 
    

a = y()
print(a)