def length_less(s):
    if len(s)>=20:
        return True
    return False

def length_not_20(data):
    not_length={}
    Product_Name=[]
    for i in range(1,len(data)+1):
        Product_Name.append(data[str(i)]['Product_Name'])
    j=1
    for i in Product_Name:
        if length_less(i):
            if j not in not_length:
                not_length[j] = {}
            if 'Product_Name' not in not_length[j]:
                not_length[j]['Product_Name'] = []
            not_length[j]['Product_Name'].append(i)
        j+=1
    return not_length