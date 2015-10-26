import os
import sys
import random
import numpy as np
import cv2 as cv
import copy


def game():
    random.seed()
    total_pieces = 10

    ###
    # Load image
    def get_random_image_at_path(path):
        def is_image_file(name):
            extension = name[-3:]

            return (extension == 'bmp') or (extension == 'png') or (extension == 'jpg')

        images_files = [f for f in os.listdir(path) if is_image_file(f)]
        return os.path.join(path, random.choice(images_files))

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            image_game_path = get_random_image_at_path(arg)
        else:
            image_game_path = arg
    else:
        script_path = os.path.dirname(os.path.realpath(__file__))
        image_game_path = get_random_image_at_path(script_path)

    img = cv.imread(image_game_path)
    height, width = img.shape[:2]

    if (height > 620) or (width > 620):
        # Large images too cause problems
        percent_to_reduce = 620 * 100 / max(height, width)
        img = cv.resize(img, (0,0), fx=percent_to_reduce / 100, fy=percent_to_reduce / 100)
        height, width = img.shape[:2]

    def decide_width():
        # The width should be able to fit all the game pieces
        min_width = total_pieces * 100
        if width > min_width:
            return width
        else:
            return min_width

    img_game = np.zeros((height + 100, decide_width(), 3), np.uint8)
    img_game[0:height, 0:width] = img

    ###
    # Create game pieces
    place_piece_success = random.randrange(total_pieces)

    def invert_piece(piece):
        return piece[::-1]

    def color_red_to_green(piece):
        for i in piece:
                    for i2 in i:
                        if (i2[2] > i2[1] + 40) and (i2[2] > i2[0] + 40):
                            i2[2], i2[1] = i2[1], i2[2]

        return piece

    def color_black_to_blue(piece):
        for i in piece:
            for i2 in i:
                if (np.array([80, 80, 80]) > i2).all():
                    i2[0] += 100

        return piece

    def median_filtering(piece):
        return cv.medianBlur(piece, 5)

    def morph_open(piece):
        return cv.morphologyEx(piece, cv.MORPH_OPEN, np.ones((5,5), np.uint8))

    def morph_close(piece):
        return cv.morphologyEx(piece, cv.MORPH_CLOSE, np.ones((3,3), np.uint8))

    piece_change_functions = [invert_piece, color_red_to_green, color_black_to_blue, median_filtering, morph_open, morph_close]

    fast = cv.FastFeatureDetector_create(nonmaxSuppression=True)
    kp = fast.detect(img_game, None)

    # Remove points close to the edge, it would not be possible to create the part of them
    kp = [i for i in kp if i.pt[0] + 25 < width and i.pt[1] + 25 < height]

    pieces = []
    for current_piece in range(total_pieces):
        kp_target = random.choice(kp)
        kp.remove(kp_target)

        y, x = kp_target.pt

        x -= 25
        if x < 0:
            x = 0

        y -= 25
        if y < 0:
            y = 0

        pieces.append({'img_game_pos': (int(y), int(x))})

        piece = copy.copy(img[x:x + 50, y:y + 50])

        if current_piece != place_piece_success:
            piece = random.choice(piece_change_functions)(piece)

        img_game[height + 25:height + 75, 100 * current_piece:50 + 100 * current_piece] = piece

    ###
    # Create mouse event
    def answer(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            if not (height + 25 <= y <= height + 75):
                return

            img_clicked, d = divmod(x, 100)
            if d > 50:
                # The player clicked on the black part
                return

            if img_clicked == place_piece_success:
                cv.circle(img_game, (x, y), 10, (255, 0, 0), -1)
            else:
                cv.circle(img_game, (x, y), 10, (0, 0, 255), -1)

            y, x = pieces[img_clicked]['img_game_pos']
            cv.rectangle(img_game, (y, x), (y + 50, x + 50), (127, 127, 127))

    cv.namedWindow('image')
    cv.setMouseCallback('image', answer)

    ###
    # Start game
    while True:
        cv.imshow('image', img_game)
        if cv.waitKey(20) & 0xFF == 27:
            break
    cv.destroyAllWindows()


game()
