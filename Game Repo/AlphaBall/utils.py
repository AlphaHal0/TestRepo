# Special utilities
def clamp(n, minN, maxN):
    return max(min(maxN, n), minN)

def center_text(width,screen):
    return screen / 2 - width / 2
