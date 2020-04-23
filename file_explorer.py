import os 

def files(path):
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







