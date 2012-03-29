
def safe_decode(orig):  
    try:  
        return orig.decode('utf8')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('gb2312')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('gbk')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('big5')  
    except UnicodeDecodeError:  
        pass  
    return orig
