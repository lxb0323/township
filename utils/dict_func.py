def filter_dict_func(adict):
    '''
        TODO: 多个字段，返回非空值得新字典
    '''
    new_d = list(adict.keys())
    print(new_d)
    bdict = {}
    for i in new_d:
        if adict[i] is not None:
            bdict[i] = adict[i]
    return bdict