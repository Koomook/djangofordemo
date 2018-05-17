import os
import numpy as np
mp3dir = 'mp3' # 왜 ../../mp3 가 아닐까?
mp3s = [os.path.join(mp3dir, fn) for fn in os.listdir(mp3dir)]
print(mp3s)

def pickmp3():
    selected = np.random.choice(mp3s, 1)[0]
    song = "<audio src='{}' controls controlsList='nodownload'></audio>".format(
        selected)
    return song