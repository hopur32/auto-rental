def kennitala_check(kt):
    'Settur inn kennitölu, skilar bool og ef hún er vitlaus skilar hún líka sterng af því hvað er ekki að virka'
    kt = str(kt)
    try: 
        int(kt)
    except ValueError:  	
        return False, 'kennitala can only be intigers'
    else:
        if len(kt) == 10:
            sum1= ((3 * int(kt[0])) +
            (2 * int(kt[1])) +
            (7 * int(kt[2])) +
            (6 * int(kt[3])) +
            (5 * int(kt[4])) +
            (4 * int(kt[5])) +
            (3 * int(kt[6])) +
            (2 * int(kt[7])) + 
                 int(kt[8]))

            if (sum1 % 11) == 0: 
                return True 
            else:           
                return False, 'Invalid kennitala'
        else:               
            return False, 'Kennitala has invalid lenth'

