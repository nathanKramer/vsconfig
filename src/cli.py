from vsconfig import diff, help, install, reset

def parse_flags(flags):
    parsed_flags = {}
    l = range(0, len(flags))
    for k, v in zip(l[0::2], l[1::2]):
        flag = flags[k]
        if not flag.startswith('--'):
            continue
        parsed_flags[flag.lstrip('-')] = flags[v]
    
    return parsed_flags
