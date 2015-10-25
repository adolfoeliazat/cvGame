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

    # Create mouse event
    def answer(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            if not (height + 25 <= y <= height + 75):
                return

            if 50 + 100 * place_piece_success >= x >= 100 * place_piece_success:
                cv.circle(img_game, (x, y), 10, (255, 0, 0), -1)
            else:
                cv.circle(img_game, (x, y), 10, (0, 0, 255), -1)

    cv.namedWindow('image')
    cv.setMouseCallback('image', answer)

    # Start game
    while True:
        cv.imshow('image', img_game)
        if cv.waitKey(20) & 0xFF == 27:
            break
    cv.destroyAllWindows()


game()
