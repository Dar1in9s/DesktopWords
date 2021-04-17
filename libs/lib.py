import random
import config
import os

def choiseWord(wordDir):
    word_book = random.choice(os.listdir(wordDir)).strip()
    with open(wordDir+word_book, 'r', encoding="utf8") as f:
        words = f.readlines()
    allWords = []
    for word in words:
        tmp = word.strip()
        if tmp == "" or tmp[0] == "#":
            continue
        if "#" in tmp:
            tmp = tmp[:tmp.index("#")].strip()
        allWords.append(tmp)
    if allWords:
        word = random.choice(allWords).strip()
    else:
        word = choiseWord(wordDir)
    return word
