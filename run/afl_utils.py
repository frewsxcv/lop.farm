def stats(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [i.split(':', 1) for i in lines]
    for i, x in enumerate(lines):
        lines[i][0] = lines[i][0].strip()
        lines[i][1] = lines[i][1].strip()
    return lines
