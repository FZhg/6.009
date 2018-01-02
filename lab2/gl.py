val = [1,23,45,67,78]
def good_ex(a):
    global val
    if a != val:
        val = a
    return val

print(good_ex([23,45]))
