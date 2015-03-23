from operator import sub

def list_diff(former_list,current_list):
    diff = map(sub, current_list,former_list)
    return map(abs,diff)