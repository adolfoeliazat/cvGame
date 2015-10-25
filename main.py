import random
import numpy as np
import cv2 as cv
import copy


def game():
    random.seed()

    # Load image
    img = cv.imread('onepiece.png')
    height, width = img.shape[:2]

    img_game = np.zeros((height + 100, width, 3), np.uint8)
    img_game[0:height, 0:width] = img

    # Create game pieces
    total_pieces = 4

    place_piece_success = random.randrange(total_pieces)

    for current_piece in range(total_pieces):
        x = random.randrange(height - 50)
        y = random.randrange(width - 50)

        piece = copy.copy(img[x:x + 50, y:y + 50])

        if current_piece != place_piece_success:
            piece_type = random.randrange(3)

            if piece_type == 0:
                piece = piece[::-1]

            elif piece_type == 1:
                for i in piece:
                    for i2 in i:
                        if (i2[2] > i2[1] + 40) and (i2[2] > i2[0] + 40):
                            i2[2], i2[1] = i2[1], i2[2]

            elif piece_type == 2:
                for i in piece:
                    for i2 in i:
                        if (np.array([80, 80, 80]) > i2).all():
                            i2[0] += 100

        img_game[height + 25:height + 75, 100 * current_piece:50 + 100 * current_piece] = piece

    # Start game
    cv.imshow('image', img_game)
    cv.waitKey(0)
    cv.destroyAllWindows()


game()
