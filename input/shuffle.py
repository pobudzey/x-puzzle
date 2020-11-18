import random

l = [0, 1, 2, 3, 4, 5, 6, 7]
with open("samplePuzzles.txt", "w") as f:
    for x in range(50):
        random.shuffle(l)
        s = " ".join(str(e) for e in l)
        if x == 49:
            f.write(s)
        else:
            f.write(s + "\n")