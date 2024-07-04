def is_first_letter_uppercase_each_word(s):
    words = s.split()
    return all(word[0].isupper() for word in words if word[0].isalpha())

def first(data):
    not_title={}
    Product_Name=[]
    for i in range(1,len(data)+1):
        Product_Name.append(data[str(i)]['Product_Name'])
    j=1
    for i in Product_Name:
        if not is_first_letter_uppercase_each_word(i):
            if str(j) not in not_title:
                not_title[str(j)] = {}
            if 'Product_Name' not in not_title[str(j)]:
                not_title[str(j)]['Product_Name'] = []
            not_title[str(j)]['Product_Name'].append(i)
        j+=1

    return not_title