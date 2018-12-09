"""
big_functions

a resting space for code that works, but due to memory constraints had to
be removed from the main.py file
"""

    if cliend_id == "dead test segment, so sad":
        publish("Config small test segment")
        lights = 27
        segment[0] = [i for i in range(3, 8)]    # a
        segment[1] = [i for i in range(0, 4)]    # b
        segment[2] = [i for i in range(18, 23)]  # c
        segment[3] = [i for i in range(14, 18)]  # d
        segment[4] = [i for i in range(11, 14)]  # e
        segment[5] = [i for i in range(7, 12)]   # f
        segment[6] = [i for i in range(22, 27)]  # g


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




        def party():
            """ Show a lot of colors and animation
            """
            publish("Party")
            for i in range(0, np.n):
                np[i] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])

            np.write()

def gotMessage(topic, msg):
    print(topic)
    print(msg)

    # Address single light via topc - disabled
    # light = int(topic.decode("utf-8").split('/')[-1])
    s_msg = msg.decode("utf-8")

    print("Got message ", msg)
    command = s_msg.split(' ')[0]
    payload = s_msg.split(' ')[1]

    print("Command ", command, "Paylod ", payload)

    if command == "b":
        i = int(payload)
        set_binary(i)

    if command == "d":
        d = int(payload)
        set_digit(d)

    if msg == b'on':
        test_digits()

    if msg == b'off':
        allOff()

    if msg == b'party':
        party()
        print("Party")


def test_digits():
    """ Run through 0->9
    """
    publish("Test Digits")
    for i in range(0, 10):
        print(i)
        set_char(str(i))
        time.sleep_ms(750)
        set_binary(0)
        time.sleep_ms(250)


def random_flake():
    """ Initialize a snow flake
    """
    flake = {}

    # Either left or right side of window
    if uos.urandom(1)[0] > 128:
        flake['path'] = segment[1] + segment[2]
    else:
        flake['path'] = segment[5] + segment[4]

    flake['pos'] = 0
    return flake


def snow(t):
    """ using segments A B and F E, show snow falling
    """
    publish("snow")

    storm = []
    for i in range(0, 1):
        storm.append(random_flake())

    for i in range(0, t):
        for flake in storm:
            print(flake['path'])

            pos = flake['pos']

            pixel = flake['path'][pos]
            print("pixel = off", pixel)

            # clear prev pixel
            np[pixel] = [0, 0, 0]

            flake['pos'] += 1
            pos = flake['pos']

            if flake['pos'] >= len(flake['path']):
                storm.remove(flake)
                storm.append(random_flake())
            else:
                pixel = flake['path'][pos]
                print("pixel ON= ", pixel)

                np[pixel] = [25, 25, 25]

        np.write()
        time.sleep_ms(500)


        def twinkle(t):
            """ twikling star pattern
            """
            publish("twinkle")

            starfield = []
            for i in range(0, 30):
                starfield.append(random_star())

            for i in range(0, t * 20):
                for star in starfield:
                    r = star['color'][0]
                    g = star['color'][1]
                    b = star['color'][2]
                    r = int(r * star['speed'])
                    g = int(g * star['speed'])
                    b = int(b * star['speed'])
                    new_color = (r, g, b)
                    star['color'] = new_color
                    np[star['pixel']] = star['color']

                    if (r+g+b) == 0:
                        starfield.remove(star)
                        starfield.append(random_star())

                np.write()
                time.sleep_ms(100)
            allOff()
