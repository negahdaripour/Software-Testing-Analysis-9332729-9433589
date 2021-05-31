def get_var_string_name(s):
    output = []
    l = s.split(' ')
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(l)):
        if '(' in l[i] and 'z3' not in l[i]:
            indx = l[i].find('(')
            name = l[i][indx+1:]
            output.append(name)
        if "z3.Not" in l[i]:
            indx = l[i].find('Not')
            name = l[i][indx+4:]    
            output.append(name)
        if "z3.And" in l[i]:
            indx = l[i].find('And')
            name = l[i][indx+4:]    
            output.append(name)
        if "z3.Or" in l[i]:
            indx = l[i].find('Or')
            name = l[i][indx+2:]    
            output.append(name)
        if ',' in l[i]:
            indx = l[i].find(',')
            name = l[i][:indx]
            output.append(name)
            
        if '(' not in l[i] and '=' not in l[i]  and '<' not in l[i] and '>' not in l[i] and ',' not in l[i] and ')' not in l[i] and 'z3.Not' not in l[i] and 'and' not in l[i] and 'or' not in l[i] and 'not' not in l[i] :
            if '+' not in l[i] and '-' not in l[i] and '*' not in l[i] and '%' not in l[i] and '/' not in l[i]:
                if l[i][0] not in digits:
                    name = l[i]
                    output.append(name)


            
        if ')' in l[i] and l[i][0] not in digits:
            indx = l[i].find(')')
            name = l[i][:indx]
            output.append(name)
            
    return output

