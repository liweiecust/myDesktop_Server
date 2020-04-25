import os 

def files(path):
    test_path(path)
    dir=[]
    file_list=[]
    items=os.listdir(path)
    items_path=[os.path.join(path,x) for x in items]
    for item in items_path:
        if(os.path.isdir(item)):
            dir.append(item)
        else:
            file_list.append(item)
    new_list=list()
    new_list.append(dir)
    new_list.append(file_list)
    return new_list

def test_path(path):
    if(os.path.exists(path)):
        pass
    else:
        raise IOError("path %s not found." % path)






