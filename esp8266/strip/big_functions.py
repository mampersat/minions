"""
big_functions

a resting space for code that works, but due to memory constraints had to
be removed from the main.py file
"""


def morse(t):
    """ morse
    blink the pixels index in morse code
    """
    CODE = {
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        }

    ditlen = 1
    dahlen = 2
    seplen = 1
    breaklen = 2
    maxindexlen = len(str(lights))
    maxlen = maxindexlen * 5 * dahlen + seplen * (maxindexlen - 1)
    print("maxlen= " + str(maxlen))

    for x in range(0, maxlen):  # for each 0/1 in the morse sequence
        print("x= " + str(x))
        for i in range(0, lights):  # for every light in the strip
            s = str(i)
            seq = ""
            for char in s:
                code = CODE[char]
                for char in code:
                    if char == '.':  # dit
                        seq += "1" * ditlen
                    else:  # dah
                        seq += "1" * dahlen
                    seq += "0" * seplen
                seq += "0" * breaklen
            print("index " + str(i) + " : " + seq)

            if x < len(seq):
                if seq[x] == '1':
                    np[i] = (255, 255, 255)
                else:
                    np[i] = (0, 0, 0)

        np.write()
        time.sleep_ms(10)
