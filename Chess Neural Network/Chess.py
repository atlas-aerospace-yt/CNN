import multiprocessing
import threading
import pygame
from pygame.locals import *
import os
import os.path
import random
import time
from tkinter import Tk
import math
from copy import deepcopy
import numpy
import NeuralNet

class Board():

    def __init__(self):

        self.dark_square = pygame.image.load(os.path.join("Textures/dark_square.png")).convert_alpha()
        self.dark_square = pygame.transform.scale(self.dark_square, (startup.tile_size, startup.tile_size))
        self.dark_square_rect = self.dark_square.get_rect()

        self.light_square = pygame.image.load(os.path.join("Textures/light_square.png")).convert_alpha()
        self.light_square = pygame.transform.scale(self.light_square, (startup.tile_size, startup.tile_size))
        self.light_square_rect = self.light_square.get_rect()

    def draw_board(self):

        for i in range(0, 8):

            x = startup.tile_size * i

            for j in range(0, 8):

                y = startup.tile_size * j

                if (i + j) % 2 == 0:

                    self.light_square_rect.x = x
                    self.light_square_rect.y = y

                    tile = self.light_square, self.light_square_rect

                else:

                    self.dark_square_rect.x = x
                    self.dark_square_rect.y = y

                    tile = self.dark_square, self.dark_square_rect

                startup.screen.blit(tile[0], tile[1])

class Pieces():

    def __init__(self):

        #[xpos, ypos, alive, selected, being dragged, unmoved]

        self.white_pawns_inf = [[0, 1, True, False, False, True], [1, 1, True, False, False, True], [2, 1, True, False, False, True], [3, 1, True, False, False, True], [4, 1, True, False, False, True], [5, 1, True, False, False, True], [6, 1, True, False, False, True], [7, 1, True, False, False, True]]
        self.white_bishops_inf = [[2, 0, True, False, False], [5, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.white_knights_inf = [[1, 0, True, False, False], [6, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.white_rooks_inf = [[0, 0, True, False, False, True], [7, 0, True, False, False, True], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False]]
        self.white_queens_inf = [[3, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.white_king_inf = [[4, 0, True, False, False, True]]

        self.black_pawns_inf = [[0, 6, True, False, False, True], [1, 6, True, False, False, True], [2, 6, True, False, False, True], [3, 6, True, False, False, True], [4, 6, True, False, False, True], [5, 6, True, False, False, True], [6, 6, True, False, False, True], [7, 6, True, False, False, True]]
        self.black_bishops_inf = [[2, 7, True, False, False], [5, 7, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.black_knights_inf = [[6, 7, True, False, False], [1, 7, True, False, False], [6, 3, False, False, False], [0, 3, False, False, False], [2, 0, False, False, False], [2, 6, False, False, False], [6, 2, False, False, False], [0, 2, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.black_rooks_inf = [[0, 7, True, False, False, True], [7, 7, True, False, False, True], [2, 0, False, False, False, False], [4, 6, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False]]
        self.black_queens_inf = [[3, 7, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
        self.black_king_inf = [[4, 7, True, False, False, True]]

        #[xpos, ypos, alive, clicked once]

        self.tile_outline_inf = [0, 0, False, False]

        self.piece_value_matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]]

        self.white_pawn_img = pygame.image.load(os.path.join("Textures/white_pawn.png")).convert_alpha()
        self.white_pawn_img = pygame.transform.scale(self.white_pawn_img, (startup.tile_size, startup.tile_size))
        self.white_pawn_img_rect = self.white_pawn_img.get_rect()

        self.white_knight_img = pygame.image.load(os.path.join("Textures/white_knight.png")).convert_alpha()
        self.white_knight_img = pygame.transform.scale(self.white_knight_img, (startup.tile_size, startup.tile_size))
        self.white_knight_img_rect = self.white_knight_img.get_rect()

        self.little_white_knight_img = pygame.image.load(os.path.join("Textures/white_knight.png")).convert_alpha()
        self.little_white_knight_img = pygame.transform.scale(self.little_white_knight_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_white_knight_img_rect = self.little_white_knight_img.get_rect()

        self.white_bishop_img = pygame.image.load(os.path.join("Textures/white_bishop.png")).convert_alpha()
        self.white_bishop_img = pygame.transform.scale(self.white_bishop_img, (startup.tile_size, startup.tile_size))
        self.white_bishop_img_rect = self.white_bishop_img.get_rect()

        self.little_white_bishop_img = pygame.image.load(os.path.join("Textures/white_bishop.png")).convert_alpha()
        self.little_white_bishop_img = pygame.transform.scale(self.little_white_bishop_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_white_bishop_img_rect = self.little_white_bishop_img.get_rect()

        self.white_rook_img = pygame.image.load(os.path.join("Textures/white_rook.png")).convert_alpha()
        self.white_rook_img = pygame.transform.scale(self.white_rook_img, (startup.tile_size, startup.tile_size))
        self.white_rook_img_rect = self.white_rook_img.get_rect()

        self.little_white_rook_img = pygame.image.load(os.path.join("Textures/white_rook.png")).convert_alpha()
        self.little_white_rook_img = pygame.transform.scale(self.little_white_rook_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_white_rook_img_rect = self.little_white_rook_img.get_rect()

        self.white_queen_img = pygame.image.load(os.path.join("Textures/white_queen.png")).convert_alpha()
        self.white_queen_img = pygame.transform.scale(self.white_queen_img, (startup.tile_size, startup.tile_size))
        self.white_queen_img_rect = self.white_queen_img.get_rect()

        self.white_king_img = pygame.image.load(os.path.join("Textures/white_king.png")).convert_alpha()
        self.white_king_img = pygame.transform.scale(self.white_king_img, (startup.tile_size, startup.tile_size))
        self.white_king_img_rect = self.white_king_img.get_rect()

        self.black_pawn_img = pygame.image.load(os.path.join("Textures/black_pawn.png")).convert_alpha()
        self.black_pawn_img = pygame.transform.scale(self.black_pawn_img, (startup.tile_size, startup.tile_size))
        self.black_pawn_img_rect = self.black_pawn_img.get_rect()

        self.black_knight_img = pygame.image.load(os.path.join("Textures/black_knight.png")).convert_alpha()
        self.black_knight_img = pygame.transform.scale(self.black_knight_img, (startup.tile_size, startup.tile_size))
        self.black_knight_img_rect = self.black_knight_img.get_rect()

        self.little_black_knight_img = pygame.image.load(os.path.join("Textures/black_knight.png")).convert_alpha()
        self.little_black_knight_img = pygame.transform.scale(self.little_black_knight_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_black_knight_img_rect = self.little_black_knight_img.get_rect()

        self.black_bishop_img = pygame.image.load(os.path.join("Textures/black_bishop.png")).convert_alpha()
        self.black_bishop_img = pygame.transform.scale(self.black_bishop_img, (startup.tile_size, startup.tile_size))
        self.black_bishop_img_rect = self.black_bishop_img.get_rect()

        self.little_black_bishop_img = pygame.image.load(os.path.join("Textures/black_bishop.png")).convert_alpha()
        self.little_black_bishop_img = pygame.transform.scale(self.little_black_bishop_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_black_bishop_img_rect = self.little_black_bishop_img.get_rect()

        self.black_rook_img = pygame.image.load(os.path.join("Textures/black_rook.png")).convert_alpha()
        self.black_rook_img = pygame.transform.scale(self.black_rook_img, (startup.tile_size, startup.tile_size))
        self.black_rook_img_rect = self.black_rook_img.get_rect()

        self.little_black_rook_img = pygame.image.load(os.path.join("Textures/black_rook.png")).convert_alpha()
        self.little_black_rook_img = pygame.transform.scale(self.little_black_rook_img, (startup.tile_size // 2, startup.tile_size // 2))
        self.little_black_rook_img_rect = self.little_black_rook_img.get_rect()

        self.black_queen_img = pygame.image.load(os.path.join("Textures/black_queen.png")).convert_alpha()
        self.black_queen_img = pygame.transform.scale(self.black_queen_img, (startup.tile_size, startup.tile_size))
        self.black_queen_img_rect = self.black_queen_img.get_rect()

        self.black_king_img = pygame.image.load(os.path.join("Textures/black_king.png")).convert_alpha()
        self.black_king_img = pygame.transform.scale(self.black_king_img, (startup.tile_size, startup.tile_size))
        self.black_king_img_rect = self.black_king_img.get_rect()

        self.tile_outline_img = pygame.image.load(os.path.join("Textures/tile_outline.png")).convert_alpha()
        self.tile_outline_img = pygame.transform.scale(self.tile_outline_img, (startup.tile_size, startup.tile_size))
        self.tile_outline_img_rect = self.tile_outline_img.get_rect()

        self.promotion_strip_img_1 = pygame.image.load(os.path.join("Textures/promotion_strip_1.png")).convert_alpha()
        self.promotion_strip_img_1 = pygame.transform.scale(self.promotion_strip_img_1, (startup.tile_size, startup.tile_size * 2))
        self.promotion_strip_img_1_rect = self.promotion_strip_img_1.get_rect()

        self.promotion_strip_img_2 = pygame.image.load(os.path.join("Textures/promotion_strip_2.png")).convert_alpha()
        self.promotion_strip_img_2 = pygame.transform.scale(self.promotion_strip_img_2, (startup.tile_size, startup.tile_size * 2))
        self.promotion_strip_img_2_rect = self.promotion_strip_img_2.get_rect()

        self.promotion_strip_inf = [0, 0, False, 0]

        self.white_occupation_x = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
        self.white_occupation_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

        self.black_occupation_x = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
        self.black_occupation_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

        self.en_passant_x_y = [8, 8]

        self.legal_moves = []
        self.final_legal_moves = []

        self.half_moves = 0
        self.half_move_limit = False
        self.turn_num = 1

    def draw_dragged_piece(self, img, img_rect):

        mouse_pos = pygame.mouse.get_pos()

        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]

        img_rect.x = mouse_pos_x - (startup.tile_size // 2)
        img_rect.y = mouse_pos_y - (startup.tile_size // 2)

        startup.screen.blit(img, img_rect)

    def draw_pieces_white(self):

        for i in range(0, 8):

            if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][4] == False:

                self.white_pawn_img_rect.x = self.white_pawns_inf[i][0] * startup.tile_size
                self.white_pawn_img_rect.y = self.white_pawns_inf[i][1] * startup.tile_size
                self.white_pawn_img_rect.y = self.white_pawn_img_rect.y - (self.white_pawn_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.white_pawn_img, self.white_pawn_img_rect)

        for i in range(0, 10):

            if self.white_bishops_inf[i][2] == True and self.white_bishops_inf[i][4] == False:

                self.white_bishop_img_rect.x = self.white_bishops_inf[i][0] * startup.tile_size
                self.white_bishop_img_rect.y = self.white_bishops_inf[i][1] * startup.tile_size
                self.white_bishop_img_rect.y = self.white_bishop_img_rect.y - (self.white_bishop_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.white_bishop_img, self.white_bishop_img_rect)

        for i in range(0, 10):

            if self.white_knights_inf[i][2] == True and self.white_knights_inf[i][4] == False:

                self.white_knight_img_rect.x = self.white_knights_inf[i][0] * startup.tile_size
                self.white_knight_img_rect.y = self.white_knights_inf[i][1] * startup.tile_size
                self.white_knight_img_rect.y = self.white_knight_img_rect.y - (self.white_knight_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.white_knight_img, self.white_knight_img_rect)

        for i in range(0, 10):

            if self.white_rooks_inf[i][2] == True and self.white_rooks_inf[i][4] == False:

                self.white_rook_img_rect.x = self.white_rooks_inf[i][0] * startup.tile_size
                self.white_rook_img_rect.y = self.white_rooks_inf[i][1] * startup.tile_size
                self.white_rook_img_rect.y = self.white_rook_img_rect.y - (self.white_rook_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.white_rook_img, self.white_rook_img_rect)

        for i in range(0, 9):

            if self.white_queens_inf[i][2] == True and self.white_queens_inf[i][4] == False:

                self.white_queen_img_rect.x = self.white_queens_inf[i][0] * startup.tile_size
                self.white_queen_img_rect.y = self.white_queens_inf[i][1] * startup.tile_size
                self.white_queen_img_rect.y = self.white_queen_img_rect.y - (self.white_queen_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.white_queen_img, self.white_queen_img_rect)

        if self.white_king_inf[0][2] == True and self.white_king_inf[0][4] == False:

            self.white_king_img_rect.x = self.white_king_inf[0][0] * startup.tile_size
            self.white_king_img_rect.y = self.white_king_inf[0][1] * startup.tile_size
            self.white_king_img_rect.y = self.white_king_img_rect.y - (self.white_king_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

            startup.screen.blit(self.white_king_img, self.white_king_img_rect)

        for i in range(0, 8):

            if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][4] == False:

                self.black_pawn_img_rect.x = self.black_pawns_inf[i][0] * startup.tile_size
                self.black_pawn_img_rect.y = self.black_pawns_inf[i][1] * startup.tile_size
                self.black_pawn_img_rect.y = self.black_pawn_img_rect.y - (self.black_pawn_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.black_pawn_img, self.black_pawn_img_rect)

        for i in range(0, 10):

            if self.black_bishops_inf[i][2] == True and self.black_bishops_inf[i][4] == False:

                self.black_bishop_img_rect.x = self.black_bishops_inf[i][0] * startup.tile_size
                self.black_bishop_img_rect.y = self.black_bishops_inf[i][1] * startup.tile_size
                self.black_bishop_img_rect.y = self.black_bishop_img_rect.y - (self.black_bishop_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.black_bishop_img, self.black_bishop_img_rect)

        for i in range(0, 10):

            if self.black_knights_inf[i][2] == True and self.black_knights_inf[i][4] == False:

                self.black_knight_img_rect.x = self.black_knights_inf[i][0] * startup.tile_size
                self.black_knight_img_rect.y = self.black_knights_inf[i][1] * startup.tile_size
                self.black_knight_img_rect.y = self.black_knight_img_rect.y - (self.black_knight_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.black_knight_img, self.black_knight_img_rect)

        for i in range(0, 10):

            if self.black_rooks_inf[i][2] == True and self.black_rooks_inf[i][4] == False:

                self.black_rook_img_rect.x = self.black_rooks_inf[i][0] * startup.tile_size
                self.black_rook_img_rect.y = self.black_rooks_inf[i][1] * startup.tile_size
                self.black_rook_img_rect.y = self.black_rook_img_rect.y - (self.black_rook_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.black_rook_img, self.black_rook_img_rect)

        for i in range(0, 9):

            if self.black_queens_inf[i][2] == True and self.black_queens_inf[i][4] == False:

                self.black_queen_img_rect.x = self.black_queens_inf[i][0] * startup.tile_size
                self.black_queen_img_rect.y = self.black_queens_inf[i][1] * startup.tile_size
                self.black_queen_img_rect.y = self.black_queen_img_rect.y - (self.black_queen_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

                startup.screen.blit(self.black_queen_img, self.black_queen_img_rect)

        if self.black_king_inf[0][2] == True and self.black_king_inf[0][4] == False:

            self.black_king_img_rect.x = self.black_king_inf[0][0] * startup.tile_size
            self.black_king_img_rect.y = self.black_king_inf[0][1] * startup.tile_size
            self.black_king_img_rect.y = self.black_king_img_rect.y - (self.black_king_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

            startup.screen.blit(self.black_king_img, self.black_king_img_rect)

        if self.tile_outline_inf[2] == True:

            self.tile_outline_img_rect.x = self.tile_outline_inf[0] * startup.tile_size
            self.tile_outline_img_rect.y = self.tile_outline_inf[1] * startup.tile_size
            self.tile_outline_img_rect.y = self.tile_outline_img_rect.y - (self.tile_outline_img_rect.y * 2) + (startup.screen_height - startup.tile_size)

            startup.screen.blit(self.tile_outline_img, self.tile_outline_img_rect)

        if self.promotion_strip_inf[2] == True:

            if self.promotion_strip_inf[1] == 7:

                self.promotion_strip_img_1_rect.x = self.promotion_strip_inf[0] * startup.tile_size
                self.promotion_strip_img_1_rect.y = self.promotion_strip_inf[1] * startup.tile_size
                self.promotion_strip_img_1_rect.y = self.promotion_strip_img_1_rect.y - (self.promotion_strip_img_1_rect.y * 2) + (startup.screen_height - startup.tile_size)

                self.white_queen_img_rect.x = self.promotion_strip_img_1_rect.x
                self.white_queen_img_rect.y = self.promotion_strip_img_1_rect.y

                self.little_white_rook_img_rect.x = self.promotion_strip_img_1_rect.x
                self.little_white_rook_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size

                self.little_white_bishop_img_rect.x = self.promotion_strip_img_1_rect.x + (startup.tile_size // 2)
                self.little_white_bishop_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size

                self.little_white_knight_img_rect.x = self.promotion_strip_img_1_rect.x + (startup.tile_size // 4)
                self.little_white_knight_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size + (startup.tile_size // 2)

                startup.screen.blit(self.promotion_strip_img_1, self.promotion_strip_img_1_rect)
                startup.screen.blit(self.white_queen_img, self.white_queen_img_rect)
                startup.screen.blit(self.little_white_rook_img, self.little_white_rook_img_rect)
                startup.screen.blit(self.little_white_bishop_img, self.little_white_bishop_img_rect)
                startup.screen.blit(self.little_white_knight_img, self.little_white_knight_img_rect)

            elif self.promotion_strip_inf[1] == 0:

                self.promotion_strip_img_2_rect.x = self.promotion_strip_inf[0] * startup.tile_size
                self.promotion_strip_img_2_rect.y = self.promotion_strip_inf[1] * startup.tile_size
                self.promotion_strip_img_2_rect.y = self.promotion_strip_img_2_rect.y - (self.promotion_strip_img_2_rect.y * 2) + (startup.screen_height - startup.tile_size)

                self.promotion_strip_img_2_rect.y -= startup.tile_size

                self.black_queen_img_rect.x = self.promotion_strip_img_2_rect.x
                self.black_queen_img_rect.y = self.promotion_strip_img_2_rect.y + startup.tile_size

                self.little_black_rook_img_rect.x = self.promotion_strip_img_2_rect.x
                self.little_black_rook_img_rect.y = self.promotion_strip_img_2_rect.y + (startup.tile_size // 2)

                self.little_black_bishop_img_rect.x = self.promotion_strip_img_2_rect.x + (startup.tile_size // 2)
                self.little_black_bishop_img_rect.y = self.promotion_strip_img_2_rect.y + (startup.tile_size // 2)

                self.little_black_knight_img_rect.x = self.promotion_strip_img_2_rect.x + (startup.tile_size // 4)
                self.little_black_knight_img_rect.y = self.promotion_strip_img_2_rect.y

                startup.screen.blit(self.promotion_strip_img_2, self.promotion_strip_img_2_rect)
                startup.screen.blit(self.black_queen_img, self.black_queen_img_rect)
                startup.screen.blit(self.little_black_rook_img, self.little_black_rook_img_rect)
                startup.screen.blit(self.little_black_bishop_img, self.little_black_bishop_img_rect)
                startup.screen.blit(self.little_black_knight_img, self.little_black_knight_img_rect)

        for i in range(0, 8):

            if self.white_pawns_inf[i][2] and self.white_pawns_inf[i][4]:

                self.draw_dragged_piece(self.white_pawn_img, self.white_pawn_img_rect)

        for i in range(0, 10):

            if self.white_bishops_inf[i][2] and self.white_bishops_inf[i][4]:

                self.draw_dragged_piece(self.white_bishop_img, self.white_bishop_img_rect)

        for i in range(0, 10):

            if self.white_knights_inf[i][2] and self.white_knights_inf[i][4]:

                self.draw_dragged_piece(self.white_knight_img, self.white_knight_img_rect)

        for i in range(0, 10):

            if self.white_rooks_inf[i][2] and self.white_rooks_inf[i][4]:

                self.draw_dragged_piece(self.white_rook_img, self.white_rook_img_rect)

        for i in range(0, 9):

            if self.white_queens_inf[i][2] and self.white_queens_inf[i][4]:

                self.draw_dragged_piece(self.white_queen_img, self.white_queen_img_rect)

        if self.white_king_inf[0][2] and self.white_king_inf[0][4]:

            self.draw_dragged_piece(self.white_king_img, self.white_king_img_rect)

        for i in range(0, 8):

            if self.black_pawns_inf[i][2] and self.black_pawns_inf[i][4]:

                self.draw_dragged_piece(self.black_pawn_img, self.black_pawn_img_rect)

        for i in range(0, 10):

            if self.black_bishops_inf[i][2] and self.black_bishops_inf[i][4]:

                self.draw_dragged_piece(self.black_bishop_img, self.black_bishop_img_rect)

        for i in range(0, 10):

            if self.black_knights_inf[i][2] and self.black_knights_inf[i][4]:

                self.draw_dragged_piece(self.black_knight_img, self.black_knight_img_rect)

        for i in range(0, 10):

            if self.black_rooks_inf[i][2] and self.black_rooks_inf[i][4]:

                self.draw_dragged_piece(self.black_rook_img, self.black_rook_img_rect)

        for i in range(0, 9):

            if self.black_queens_inf[i][2] and self.black_queens_inf[i][4]:

                self.draw_dragged_piece(self.black_queen_img, self.black_queen_img_rect)

        if self.black_king_inf[0][2] and self.black_king_inf[0][4]:

            self.draw_dragged_piece(self.black_king_img, self.black_king_img_rect)

    def draw_pieces_black(self):

        for i in range(0, 8):

            if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][4] == False:

                self.white_pawn_img_rect.x = self.white_pawns_inf[i][0] * startup.tile_size
                self.white_pawn_img_rect.x = self.white_pawn_img_rect.x - (self.white_pawn_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.white_pawn_img_rect.y = self.white_pawns_inf[i][1] * startup.tile_size

                startup.screen.blit(self.white_pawn_img, self.white_pawn_img_rect)

        for i in range(0, 2):

            if self.white_bishops_inf[i][2] == True and self.white_bishops_inf[i][4] == False:

                self.white_bishop_img_rect.x = self.white_bishops_inf[i][0] * startup.tile_size
                self.white_bishop_img_rect.x = self.white_bishop_img_rect.x - (self.white_bishop_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.white_bishop_img_rect.y = self.white_bishops_inf[i][1] * startup.tile_size

                startup.screen.blit(self.white_bishop_img, self.white_bishop_img_rect)

        for i in range(0, 2):

            if self.white_knights_inf[i][2] == True and self.white_knights_inf[i][4] == False:

                self.white_knight_img_rect.x = self.white_knights_inf[i][0] * startup.tile_size
                self.white_knight_img_rect.x = self.white_knight_img_rect.x - (self.white_knight_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.white_knight_img_rect.y = self.white_knights_inf[i][1] * startup.tile_size

                startup.screen.blit(self.white_knight_img, self.white_knight_img_rect)

        for i in range(0, 2):

            if self.white_rooks_inf[i][2] == True and self.white_rooks_inf[i][4] == False:

                self.white_rook_img_rect.x = self.white_rooks_inf[i][0] * startup.tile_size
                self.white_rook_img_rect.x = self.white_rook_img_rect.x - (self.white_rook_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.white_rook_img_rect.y = self.white_rooks_inf[i][1] * startup.tile_size

                startup.screen.blit(self.white_rook_img, self.white_rook_img_rect)

        if self.white_queens_inf[0][2] == True and self.white_queens_inf[i][4] == False:

            self.white_queen_img_rect.x = self.white_queens_inf[0][0] * startup.tile_size
            self.white_queen_img_rect.x = self.white_queen_img_rect.x - (self.white_queen_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
            self.white_queen_img_rect.y = self.white_queens_inf[0][1] * startup.tile_size

            startup.screen.blit(self.white_queen_img, self.white_queen_img_rect)

        if self.white_king_inf[0][2] == True and self.white_king_inf[0][4] == False:

            self.white_king_img_rect.x = self.white_king_inf[0][0] * startup.tile_size
            self.white_king_img_rect.x = self.white_king_img_rect.x - (self.white_king_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
            self.white_king_img_rect.y = self.white_king_inf[0][1] * startup.tile_size

            startup.screen.blit(self.white_king_img, self.white_king_img_rect)

        for i in range(0, 8):

            if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][4] == False:

                self.black_pawn_img_rect.x = self.black_pawns_inf[i][0] * startup.tile_size
                self.black_pawn_img_rect.x = self.black_pawn_img_rect.x - (self.black_pawn_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.black_pawn_img_rect.y = self.black_pawns_inf[i][1] * startup.tile_size

                startup.screen.blit(self.black_pawn_img, self.black_pawn_img_rect)

        for i in range(0, 2):

            if self.black_bishops_inf[i][2] == True and self.black_bishops_inf[i][4] == False:

                self.black_bishop_img_rect.x = self.black_bishops_inf[i][0] * startup.tile_size
                self.black_bishop_img_rect.x = self.black_bishop_img_rect.x - (self.black_bishop_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.black_bishop_img_rect.y = self.black_bishops_inf[i][1] * startup.tile_size

                startup.screen.blit(self.black_bishop_img, self.black_bishop_img_rect)

        for i in range(0, 2):

            if self.black_knights_inf[i][2] == True and self.black_knights_inf[i][4] == False:

                self.black_knight_img_rect.x = self.black_knights_inf[i][0] * startup.tile_size
                self.black_knight_img_rect.x = self.black_knight_img_rect.x - (self.black_knight_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.black_knight_img_rect.y = self.black_knights_inf[i][1] * startup.tile_size

                startup.screen.blit(self.black_knight_img, self.black_knight_img_rect)

        for i in range(0, 2):

            if self.black_rooks_inf[i][2] == True and self.black_rooks_inf[i][4] == False:

                self.black_rook_img_rect.x = self.black_rooks_inf[i][0] * startup.tile_size
                self.black_rook_img_rect.x = self.black_rook_img_rect.x - (self.black_rook_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.black_rook_img_rect.y = self.black_rooks_inf[i][1] * startup.tile_size

                startup.screen.blit(self.black_rook_img, self.black_rook_img_rect)

        if self.black_queens_inf[0][2] == True and self.black_queens_inf[i][4] == False:

            self.black_queen_img_rect.x = self.black_queens_inf[0][0] * startup.tile_size
            self.black_queen_img_rect.x = self.black_queen_img_rect.x - (self.black_queen_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
            self.black_queen_img_rect.y = self.black_queens_inf[0][1] * startup.tile_size

            startup.screen.blit(self.black_queen_img, self.black_queen_img_rect)

        if self.black_king_inf[0][2] == True and self.black_king_inf[0][4] == False:

            self.black_king_img_rect.x = self.black_king_inf[0][0] * startup.tile_size
            self.black_king_img_rect.x = self.black_king_img_rect.x - (self.black_king_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
            self.black_king_img_rect.y = self.black_king_inf[0][1] * startup.tile_size

            startup.screen.blit(self.black_king_img, self.black_king_img_rect)

        if self.tile_outline_inf[2] == True:

            self.tile_outline_img_rect.x = self.tile_outline_inf[0] * startup.tile_size
            self.tile_outline_img_rect.x = self.tile_outline_img_rect.x - (self.tile_outline_img_rect.x * 2) + (startup.screen_height - startup.tile_size)
            self.tile_outline_img_rect.y = self.tile_outline_inf[1] * startup.tile_size

            startup.screen.blit(self.tile_outline_img, self.tile_outline_img_rect)

        if self.promotion_strip_inf[2] == True:

            if self.promotion_strip_inf[1] == 0:

                self.promotion_strip_img_1_rect.x = self.promotion_strip_inf[0] * startup.tile_size
                self.promotion_strip_img_1_rect.x = self.promotion_strip_img_1_rect.x - (self.promotion_strip_img_1_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.promotion_strip_img_1_rect.y = self.promotion_strip_inf[1] * startup.tile_size

                self.black_queen_img_rect.x = self.promotion_strip_img_1_rect.x
                self.black_queen_img_rect.y = self.promotion_strip_img_1_rect.y

                self.little_black_rook_img_rect.x = self.promotion_strip_img_1_rect.x
                self.little_black_rook_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size

                self.little_black_bishop_img_rect.x = self.promotion_strip_img_1_rect.x + (startup.tile_size // 2)
                self.little_black_bishop_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size

                self.little_black_knight_img_rect.x = self.promotion_strip_img_1_rect.x + (startup.tile_size // 4)
                self.little_black_knight_img_rect.y = self.promotion_strip_img_1_rect.y + startup.tile_size + (startup.tile_size // 2)

                startup.screen.blit(self.promotion_strip_img_1, self.promotion_strip_img_1_rect)
                startup.screen.blit(self.black_queen_img, self.black_queen_img_rect)
                startup.screen.blit(self.little_black_rook_img, self.little_black_rook_img_rect)
                startup.screen.blit(self.little_black_bishop_img, self.little_black_bishop_img_rect)
                startup.screen.blit(self.little_black_knight_img, self.little_black_knight_img_rect)

            elif self.promotion_strip_inf[1] == 7:

                self.promotion_strip_img_2_rect.x = self.promotion_strip_inf[0] * startup.tile_size
                self.promotion_strip_img_2_rect.x = self.promotion_strip_img_2_rect.x - (self.promotion_strip_img_2_rect.x * 2) + (startup.screen_height - startup.tile_size)
                self.promotion_strip_img_2_rect.y = self.promotion_strip_inf[1] * startup.tile_size

                self.promotion_strip_img_2_rect.y -= startup.tile_size

                self.white_queen_img_rect.x = self.promotion_strip_img_2_rect.x
                self.white_queen_img_rect.y = self.promotion_strip_img_2_rect.y + startup.tile_size

                self.little_white_rook_img_rect.x = self.promotion_strip_img_2_rect.x
                self.little_white_rook_img_rect.y = self.promotion_strip_img_2_rect.y + (startup.tile_size // 2)

                self.little_white_bishop_img_rect.x = self.promotion_strip_img_2_rect.x + (startup.tile_size // 2)
                self.little_white_bishop_img_rect.y = self.promotion_strip_img_2_rect.y + (startup.tile_size // 2)

                self.little_white_knight_img_rect.x = self.promotion_strip_img_2_rect.x + (startup.tile_size // 4)
                self.little_white_knight_img_rect.y = self.promotion_strip_img_2_rect.y

                startup.screen.blit(self.promotion_strip_img_2, self.promotion_strip_img_2_rect)
                startup.screen.blit(self.white_queen_img, self.white_queen_img_rect)
                startup.screen.blit(self.little_white_rook_img, self.little_white_rook_img_rect)
                startup.screen.blit(self.little_white_bishop_img, self.little_white_bishop_img_rect)
                startup.screen.blit(self.little_white_knight_img, self.little_white_knight_img_rect)

    def white_black_occupation(self):

        self.white_occupation_x = []
        self.white_occupation_y = []

        self.black_occupation_x = []
        self.black_occupation_y = []

        for i in range(0, 8):

            if self.white_pawns_inf[i][2] == True:

                self.white_occupation_x.append(self.white_pawns_inf[i][0])
                self.white_occupation_y.append(self.white_pawns_inf[i][1])

        for i in range(0, 10):

            if self.white_knights_inf[i][2] == True:

                self.white_occupation_x.append(self.white_knights_inf[i][0])
                self.white_occupation_y.append(self.white_knights_inf[i][1])

        for i in range(0, 10):

            if self.white_bishops_inf[i][2] == True:

                self.white_occupation_x.append(self.white_bishops_inf[i][0])
                self.white_occupation_y.append(self.white_bishops_inf[i][1])

        for i in range(0, 10):

            if self.white_rooks_inf[i][2] == True:

                self.white_occupation_x.append(self.white_rooks_inf[i][0])
                self.white_occupation_y.append(self.white_rooks_inf[i][1])

        for i in range(0, 9):

            if self.white_queens_inf[i][2] == True:

                self.white_occupation_x.append(self.white_queens_inf[i][0])
                self.white_occupation_y.append(self.white_queens_inf[i][1])

        if self.white_king_inf[0][2] == True:

            self.white_occupation_x.append(self.white_king_inf[0][0])
            self.white_occupation_y.append(self.white_king_inf[0][1])

        for i in range(0, 8):

            if self.black_pawns_inf[i][2] == True:

                self.black_occupation_x.append(self.black_pawns_inf[i][0])
                self.black_occupation_y.append(self.black_pawns_inf[i][1])

        for i in range(0, 10):

            if self.black_knights_inf[i][2] == True:

                self.black_occupation_x.append(self.black_knights_inf[i][0])
                self.black_occupation_y.append(self.black_knights_inf[i][1])

        for i in range(0, 10):

            if self.black_bishops_inf[i][2] == True:

                self.black_occupation_x.append(self.black_bishops_inf[i][0])
                self.black_occupation_y.append(self.black_bishops_inf[i][1])

        for i in range(0, 10):

            if self.black_rooks_inf[i][2] == True:

                self.black_occupation_x.append(self.black_rooks_inf[i][0])
                self.black_occupation_y.append(self.black_rooks_inf[i][1])

        for i in range(0, 9):

            if self.black_queens_inf[i][2] == True:

                self.black_occupation_x.append(self.black_queens_inf[i][0])
                self.black_occupation_y.append(self.black_queens_inf[i][1])

        if self.black_king_inf[0][2] == True:

            self.black_occupation_x.append(self.black_king_inf[0][0])
            self.black_occupation_y.append(self.black_king_inf[0][1])

    def calc_legal_moves(self):

        self.legal_moves = []

        if startup.white_turn == True:

            for i in range(0, 8):

                if self.white_pawns_inf[i][2] == True:

                    pawn_N_1 = True
                    pawn_N_2 = True
                    pawn_NE_11 = False
                    pawn_NW_11 = False
                    en_p_NE_11 = False
                    en_p_NW_11 = False

                    for j in range(0, len(self.white_occupation_x)):

                        if self.white_pawns_inf[i][0] == self.white_occupation_x[j] and self.white_pawns_inf[i][1] + 1 == self.white_occupation_y[j]:

                            pawn_N_1 = False

                        if self.white_pawns_inf[i][5] == True and self.white_pawns_inf[i][0] == self.white_occupation_x[j] and self.white_pawns_inf[i][1] + 2 == self.white_occupation_y[j]:

                            pawn_N_2 = False

                    for j in range(0, len(self.black_occupation_x)):

                        if self.white_pawns_inf[i][0] == self.black_occupation_x[j] and self.white_pawns_inf[i][1] + 1 == self.black_occupation_y[j]:

                            pawn_N_1 = False

                        if self.white_pawns_inf[i][5] == True and self.white_pawns_inf[i][0] == self.black_occupation_x[j] and self.white_pawns_inf[i][1] + 2 == self.black_occupation_y[j]:

                            pawn_N_2 = False

                        if self.white_pawns_inf[i][0] + 1 == self.black_occupation_x[j] and self.white_pawns_inf[i][1] + 1 == self.black_occupation_y[j]:

                            pawn_NE_11 = True

                        if self.white_pawns_inf[i][0] - 1 == self.black_occupation_x[j] and self.white_pawns_inf[i][1] + 1 == self.black_occupation_y[j]:

                            pawn_NW_11 = True

                    if self.white_pawns_inf[i][0] + 1 == self.en_passant_x_y[0] and self.white_pawns_inf[i][1] == self.en_passant_x_y[1]:

                        pawn_NE_11 = True

                    elif self.white_pawns_inf[i][0] - 1 == self.en_passant_x_y[0] and self.white_pawns_inf[i][1] == self.en_passant_x_y[1]:

                        pawn_NW_11 = True

                    if pawn_N_1 == True:

                        legal_move_notation = notation.get_notation("P", self.white_pawns_inf[i][0], self.white_pawns_inf[i][1], self.white_pawns_inf[i][0], self.white_pawns_inf[i][1] + 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_N_2 == True and pawn_N_1 == True and self.white_pawns_inf[i][5] == True:

                        legal_move_notation = notation.get_notation("P", self.white_pawns_inf[i][0], self.white_pawns_inf[i][1], self.white_pawns_inf[i][0], self.white_pawns_inf[i][1] + 2)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_NE_11 == True:

                        legal_move_notation = notation.get_notation("P", self.white_pawns_inf[i][0], self.white_pawns_inf[i][1], self.white_pawns_inf[i][0] + 1, self.white_pawns_inf[i][1] + 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_NW_11 == True:

                        legal_move_notation = notation.get_notation("P", self.white_pawns_inf[i][0], self.white_pawns_inf[i][1], self.white_pawns_inf[i][0] - 1, self.white_pawns_inf[i][1] + 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

            for i in range(0, 10):

                if self.white_bishops_inf[i][2] == True:

                    move_list = ["bishop_NE_1", "bishop_NE_2", "bishop_NE_3", "bishop_NE_4", "bishop_NE_5", "bishop_NE_6", "bishop_NE_7", "bishop_SE_1", "bishop_SE_2", "bishop_SE_3", "bishop_SE_4", "bishop_SE_5", "bishop_SE_6", "bishop_SE_7", "bishop_SW_1", "bishop_SW_2", "bishop_SW_3", "bishop_SW_4", "bishop_SW_5", "bishop_SW_6", "bishop_SW_7", "bishop_NW_1", "bishop_NW_2", "bishop_NW_3", "bishop_NW_4", "bishop_NW_5", "bishop_NW_6", "bishop_NW_7"]

                    bishop_moves = {
                        "bishop_NE_1" : True,
                        "bishop_NE_2" : True,
                        "bishop_NE_3" : True,
                        "bishop_NE_4" : True,
                        "bishop_NE_5" : True,
                        "bishop_NE_6" : True,
                        "bishop_NE_7" : True,
                        "bishop_SE_1" : True,
                        "bishop_SE_2" : True,
                        "bishop_SE_3" : True,
                        "bishop_SE_4" : True,
                        "bishop_SE_5" : True,
                        "bishop_SE_6" : True,
                        "bishop_SE_7" : True,
                        "bishop_SW_1" : True,
                        "bishop_SW_2" : True,
                        "bishop_SW_3" : True,
                        "bishop_SW_4" : True,
                        "bishop_SW_5" : True,
                        "bishop_SW_6" : True,
                        "bishop_SW_7" : True,
                        "bishop_NW_1" : True,
                        "bishop_NW_2" : True,
                        "bishop_NW_3" : True,
                        "bishop_NW_4" : True,
                        "bishop_NW_5" : True,
                        "bishop_NW_6" : True,
                        "bishop_NW_7" : True,
                        }

                    for j in range(1, 8):

                        if self.white_bishops_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[8] == "W" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.white_bishops_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[7] == "S" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.white_bishops_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[8] == "E" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.white_bishops_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[7] == "N" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.white_bishops_inf[i][0] + j == self.white_occupation_x[k] and self.white_bishops_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "E" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] + j == self.white_occupation_x[k] and self.white_bishops_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "E" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] - j == self.white_occupation_x[k] and self.white_bishops_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "W" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] - j == self.white_occupation_x[k] and self.white_bishops_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "W" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.white_bishops_inf[i][0] + j == self.black_occupation_x[k] and self.white_bishops_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "E" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] + j == self.black_occupation_x[k] and self.white_bishops_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "E" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] - j == self.black_occupation_x[k] and self.white_bishops_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "W" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.white_bishops_inf[i][0] - j == self.black_occupation_x[k] and self.white_bishops_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "W" and int(move[10]) > j:

                                        bishop_moves[move] = False

                    for move in move_list:

                        if bishop_moves[move] == True:

                            if move[7] == "N" and move[8] == "E":

                                self.legal_moves.append(notation.get_notation("B", self.white_bishops_inf[i][0], self.white_bishops_inf[i][1], self.white_bishops_inf[i][0] + int(move[10]), self.white_bishops_inf[i][1] + int(move[10])))

                            elif move[7] == "S" and move[8] == "E":

                                self.legal_moves.append(notation.get_notation("B", self.white_bishops_inf[i][0], self.white_bishops_inf[i][1], self.white_bishops_inf[i][0] + int(move[10]), self.white_bishops_inf[i][1] - int(move[10])))

                            elif move[7] == "S" and move[8] == "W":

                                self.legal_moves.append(notation.get_notation("B", self.white_bishops_inf[i][0], self.white_bishops_inf[i][1], self.white_bishops_inf[i][0] - int(move[10]), self.white_bishops_inf[i][1] - int(move[10])))

                            elif move[7] == "N" and move[8] == "W":

                                self.legal_moves.append(notation.get_notation("B", self.white_bishops_inf[i][0], self.white_bishops_inf[i][1], self.white_bishops_inf[i][0] - int(move[10]), self.white_bishops_inf[i][1] + int(move[10])))

            for i in range(0, 10):

                if self.white_knights_inf[i][2] == True:

                    knight_NE_21 = True
                    knight_NE_12 = True
                    knight_SE_12 = True
                    knight_SE_21 = True
                    knight_SW_21 = True
                    knight_SW_12 = True
                    knight_NW_12 = True
                    knight_NW_21 = True

                    if self.white_knights_inf[i][0] - 1 < 0:

                        knight_SW_21 = False
                        knight_SW_12 = False
                        knight_NW_12 = False
                        knight_NW_21 = False

                    elif self.white_knights_inf[i][0] - 2 < 0:

                        knight_SW_12 = False
                        knight_NW_12 = False

                    if self.white_knights_inf[i][0] + 1 > 7:

                        knight_NE_21 = False
                        knight_NE_12 = False
                        knight_SE_12 = False
                        knight_SE_21 = False

                    elif self.white_knights_inf[i][0] + 2 > 7:

                        knight_NE_12 = False
                        knight_SE_12 = False

                    if self.white_knights_inf[i][1] - 1 < 0:

                        knight_SE_12 = False
                        knight_SE_21 = False
                        knight_SW_21 = False
                        knight_SW_12 = False

                    elif self.white_knights_inf[i][1] - 2 < 0:

                        knight_SE_21 = False
                        knight_SW_21 = False

                    if self.white_knights_inf[i][1] + 1 > 7:

                        knight_NE_21 = False
                        knight_NE_12 = False
                        knight_NW_12 = False
                        knight_NW_21 = False

                    elif self.white_knights_inf[i][1] + 2 > 7:

                        knight_NE_21 = False
                        knight_NW_21 = False

                    for j in range(0, len(self.white_occupation_x)):

                        if self.white_knights_inf[i][0] + 1 == self.white_occupation_x[j] and self.white_knights_inf[i][1] + 2 == self.white_occupation_y[j]:

                            knight_NE_21 = False

                        if self.white_knights_inf[i][0] + 2 == self.white_occupation_x[j] and self.white_knights_inf[i][1] + 1 == self.white_occupation_y[j]:

                            knight_NE_12 = False

                        if self.white_knights_inf[i][0] + 2 == self.white_occupation_x[j] and self.white_knights_inf[i][1] - 1 == self.white_occupation_y[j]:

                            knight_SE_12 = False

                        if self.white_knights_inf[i][0] + 1 == self.white_occupation_x[j] and self.white_knights_inf[i][1] - 2 == self.white_occupation_y[j]:

                            knight_SE_21 = False

                        if self.white_knights_inf[i][0] - 1 == self.white_occupation_x[j] and self.white_knights_inf[i][1] - 2 == self.white_occupation_y[j]:

                            knight_SW_21 = False

                        if self.white_knights_inf[i][0] - 2 == self.white_occupation_x[j] and self.white_knights_inf[i][1] - 1 == self.white_occupation_y[j]:

                            knight_SW_12 = False

                        if self.white_knights_inf[i][0] - 2 == self.white_occupation_x[j] and self.white_knights_inf[i][1] + 1 == self.white_occupation_y[j]:

                            knight_NW_12 = False

                        if self.white_knights_inf[i][0] - 1 == self.white_occupation_x[j] and self.white_knights_inf[i][1] + 2 == self.white_occupation_y[j]:

                            knight_NW_21 = False

                    if knight_NE_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] + 1, self.white_knights_inf[i][1] + 2))

                    if knight_NE_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] + 2, self.white_knights_inf[i][1] + 1))

                    if knight_SE_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] + 2, self.white_knights_inf[i][1] - 1))

                    if knight_SE_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] + 1, self.white_knights_inf[i][1] - 2))

                    if knight_SW_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] - 1, self.white_knights_inf[i][1] - 2))

                    if knight_SW_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] - 2, self.white_knights_inf[i][1] - 1))

                    if knight_NW_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] - 2, self.white_knights_inf[i][1] + 1))

                    if knight_NW_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.white_knights_inf[i][0], self.white_knights_inf[i][1], self.white_knights_inf[i][0] - 1, self.white_knights_inf[i][1] + 2))

            for i in range(0, 10):

                if self.white_rooks_inf[i][2] == True:

                    move_list = ["rook_N_1", "rook_N_2", "rook_N_3", "rook_N_4", "rook_N_5", "rook_N_6", "rook_N_7", "rook_E_1", "rook_E_2", "rook_E_3", "rook_E_4", "rook_E_5", "rook_E_6", "rook_E_7", "rook_S_1", "rook_S_2", "rook_S_3", "rook_S_4", "rook_S_5", "rook_S_6", "rook_S_7", "rook_W_1", "rook_W_2", "rook_W_3", "rook_W_4", "rook_W_5", "rook_W_6", "rook_W_7"]

                    rook_moves = {
                        "rook_N_1" : True,
                        "rook_N_2" : True,
                        "rook_N_3" : True,
                        "rook_N_4" : True,
                        "rook_N_5" : True,
                        "rook_N_6" : True,
                        "rook_N_7" : True,
                        "rook_E_1" : True,
                        "rook_E_2" : True,
                        "rook_E_3" : True,
                        "rook_E_4" : True,
                        "rook_E_5" : True,
                        "rook_E_6" : True,
                        "rook_E_7" : True,
                        "rook_S_1" : True,
                        "rook_S_2" : True,
                        "rook_S_3" : True,
                        "rook_S_4" : True,
                        "rook_S_5" : True,
                        "rook_S_6" : True,
                        "rook_S_7" : True,
                        "rook_W_1" : True,
                        "rook_W_2" : True,
                        "rook_W_3" : True,
                        "rook_W_4" : True,
                        "rook_W_5" : True,
                        "rook_W_6" : True,
                        "rook_W_7" : True,
                        }

                    for j in range(1, 8):

                        if self.white_rooks_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[5] == "W" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.white_rooks_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[5] == "S" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.white_rooks_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[5] == "E" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.white_rooks_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[5] == "N" and int(move[7]) >= j:

                                    rook_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.white_rooks_inf[i][0] == self.white_occupation_x[k] and self.white_rooks_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "N" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] + j == self.white_occupation_x[k] and self.white_rooks_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "E" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] == self.white_occupation_x[k] and self.white_rooks_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "S" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] - j == self.white_occupation_x[k] and self.white_rooks_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "W" and int(move[7]) >= j:

                                        rook_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.white_rooks_inf[i][0] == self.black_occupation_x[k] and self.white_rooks_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "N" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] + j == self.black_occupation_x[k] and self.white_rooks_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "E" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] == self.black_occupation_x[k] and self.white_rooks_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "S" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.white_rooks_inf[i][0] - j == self.black_occupation_x[k] and self.white_rooks_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "W" and int(move[7]) > j:

                                        rook_moves[move] = False

                    for move in move_list:

                        if rook_moves[move] == True:

                            if move[5] == "N":

                                self.legal_moves.append(notation.get_notation("R", self.white_rooks_inf[i][0], self.white_rooks_inf[i][1], self.white_rooks_inf[i][0], self.white_rooks_inf[i][1] + int(move[7])))

                            elif move[5] == "E":

                                self.legal_moves.append(notation.get_notation("R", self.white_rooks_inf[i][0], self.white_rooks_inf[i][1], self.white_rooks_inf[i][0] + int(move[7]), self.white_rooks_inf[i][1]))

                            elif move[5] == "S":

                                self.legal_moves.append(notation.get_notation("R", self.white_rooks_inf[i][0], self.white_rooks_inf[i][1], self.white_rooks_inf[i][0], self.white_rooks_inf[i][1] - int(move[7])))

                            elif move[5] == "W":

                                self.legal_moves.append(notation.get_notation("R", self.white_rooks_inf[i][0], self.white_rooks_inf[i][1], self.white_rooks_inf[i][0] - int(move[7]), self.white_rooks_inf[i][1]))

            for i in range(0, 9):

                if self.white_queens_inf[i][2] == True:

                    move_list = ["queen_N_1", "queen_N_2", "queen_N_3", "queen_N_4", "queen_N_5", "queen_N_6", "queen_N_7", "queen_NE_1", "queen_NE_2", "queen_NE_3", "queen_NE_4", "queen_NE_5", "queen_NE_6", "queen_NE_7", "queen_E_1", "queen_E_2", "queen_E_3", "queen_E_4", "queen_E_5", "queen_E_6", "queen_E_7", "queen_SE_1", "queen_SE_2", "queen_SE_3", "queen_SE_4", "queen_SE_5", "queen_SE_6", "queen_SE_7", "queen_S_1", "queen_S_2", "queen_S_3", "queen_S_4", "queen_S_5", "queen_S_6", "queen_S_7", "queen_SW_1", "queen_SW_2", "queen_SW_3", "queen_SW_4", "queen_SW_5", "queen_SW_6", "queen_SW_7", "queen_W_1", "queen_W_2", "queen_W_3", "queen_W_4", "queen_W_5", "queen_W_6", "queen_W_7", "queen_NW_1", "queen_NW_2", "queen_NW_3", "queen_NW_4", "queen_NW_5", "queen_NW_6", "queen_NW_7"]

                    queen_moves = {
                        "queen_N_1" : True,
                        "queen_N_2" : True,
                        "queen_N_3" : True,
                        "queen_N_4" : True,
                        "queen_N_5" : True,
                        "queen_N_6" : True,
                        "queen_N_7" : True,
                        "queen_NE_1" : True,
                        "queen_NE_2" : True,
                        "queen_NE_3" : True,
                        "queen_NE_4" : True,
                        "queen_NE_5" : True,
                        "queen_NE_6" : True,
                        "queen_NE_7" : True,
                        "queen_E_1" : True,
                        "queen_E_2" : True,
                        "queen_E_3" : True,
                        "queen_E_4" : True,
                        "queen_E_5" : True,
                        "queen_E_6" : True,
                        "queen_E_7" : True,
                        "queen_SE_1" : True,
                        "queen_SE_2" : True,
                        "queen_SE_3" : True,
                        "queen_SE_4" : True,
                        "queen_SE_5" : True,
                        "queen_SE_6" : True,
                        "queen_SE_7" : True,
                        "queen_S_1" : True,
                        "queen_S_2" : True,
                        "queen_S_3" : True,
                        "queen_S_4" : True,
                        "queen_S_5" : True,
                        "queen_S_6" : True,
                        "queen_S_7" : True,
                        "queen_SW_1" : True,
                        "queen_SW_2" : True,
                        "queen_SW_3" : True,
                        "queen_SW_4" : True,
                        "queen_SW_5" : True,
                        "queen_SW_6" : True,
                        "queen_SW_7" : True,
                        "queen_W_1" : True,
                        "queen_W_2" : True,
                        "queen_W_3" : True,
                        "queen_W_4" : True,
                        "queen_W_5" : True,
                        "queen_W_6" : True,
                        "queen_W_7" : True,
                        "queen_NW_1" : True,
                        "queen_NW_2" : True,
                        "queen_NW_3" : True,
                        "queen_NW_4" : True,
                        "queen_NW_5" : True,
                        "queen_NW_6" : True,
                        "queen_NW_7" : True,
                        }

                    for j in range(1, 8):

                        if self.white_queens_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[6] == "W" or move[7] == "W":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.white_queens_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[6] == "S":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.white_queens_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[6] == "E" or move[7] == "E":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.white_queens_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[6] == "N":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.white_queens_inf[i][0] == self.white_occupation_x[k] and self.white_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.white_occupation_x[k] and self.white_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "E" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.white_occupation_x[k] and self.white_queens_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "E" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.white_occupation_x[k] and self.white_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "E" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] == self.white_occupation_x[k] and self.white_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.white_occupation_x[k] and self.white_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "W" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.white_occupation_x[k] and self.white_queens_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "W" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.white_occupation_x[k] and self.white_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "W" and int(move[9]) >= j:

                                        queen_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.white_queens_inf[i][0] == self.black_occupation_x[k] and self.white_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.black_occupation_x[k] and self.white_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "E" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.black_occupation_x[k] and self.white_queens_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "E" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] + j == self.black_occupation_x[k] and self.white_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "E" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] == self.black_occupation_x[k] and self.white_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.black_occupation_x[k] and self.white_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "W" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.black_occupation_x[k] and self.white_queens_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "W" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.white_queens_inf[i][0] - j == self.black_occupation_x[k] and self.white_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "W" and int(move[9]) > j:

                                        queen_moves[move] = False

                    for move in move_list:

                        if queen_moves[move] == True:

                            if move[6] == "N" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0], self.white_queens_inf[i][1] + int(move[8])))

                            elif move[6] == "N" and move[7] == "E":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] + int(move[9]), self.white_queens_inf[i][1] + int(move[9])))

                            elif move[6] == "E" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] + int(move[8]), self.white_queens_inf[i][1]))

                            elif move[6] == "S" and move[7] == "E":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] + int(move[9]), self.white_queens_inf[i][1] - int(move[9])))

                            elif move[6] == "S" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0], self.white_queens_inf[i][1] - int(move[8])))

                            elif move[6] == "S" and move[7] == "W":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] - int(move[9]), self.white_queens_inf[i][1] - int(move[9])))

                            elif move[6] == "W" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] - int(move[8]), self.white_queens_inf[i][1]))

                            elif move[6] == "N" and move[7] == "W":

                                self.legal_moves.append(notation.get_notation("Q", self.white_queens_inf[i][0], self.white_queens_inf[i][1], self.white_queens_inf[i][0] - int(move[9]), self.white_queens_inf[i][1] + int(move[9])))

            if self.white_king_inf[0][2] == True:

                move_list = ["king_N_1", "king_NE_1", "king_E_1", "king_SE_1", "king_S_1", "king_SW_1", "king_W_1", "king_NW_1"]

                king_moves = {
                    "king_N_1" : True,
                    "king_NE_1" : True,
                    "king_E_1" : True,
                    "king_SE_1" : True,
                    "king_S_1" : True,
                    "king_SW_1" : True,
                    "king_W_1" : True,
                    "king_NW_1" : True,
                    }

                if self.white_king_inf[0][0] - 1 < 0:

                    for move in move_list:

                        if move[5] == "W" or move[6] == "W":

                            king_moves[move] = False

                if self.white_king_inf[0][1] - 1 < 0:

                    for move in move_list:

                        if move[5] == "S":

                            king_moves[move] = False

                if self.white_king_inf[0][0] + 1 > 7:

                    for move in move_list:

                        if move[5] == "E" or move[6] == "E":

                            king_moves[move] = False

                if self.white_king_inf[0][1] + 1 > 7:

                    for move in move_list:

                        if move[5] == "N":

                            king_moves[move] = False

                for i in range(0, len(self.white_occupation_x)):

                    if self.white_king_inf[0][0] == self.white_occupation_x[i] and self.white_king_inf[0][1] + 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "_":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] + 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] + 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "E":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] + 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "E" and move[6] == "_":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] + 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] - 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "E":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] == self.white_occupation_x[i] and self.white_king_inf[0][1] - 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "_":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] - 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] - 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "W":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] - 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "W" and move[6] == "_":

                                king_moves[move] = False

                    elif self.white_king_inf[0][0] - 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] + 1 == self.white_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "W":

                                king_moves[move] = False

                for move in move_list:

                    if king_moves[move] == True:

                        if move[5] == "N" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0], self.white_king_inf[0][1] + 1))

                        elif move[5] == "N" and move[6] == "E":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] + 1, self.white_king_inf[0][1] + 1))

                        elif move[5] == "E" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] + 1, self.white_king_inf[0][1]))

                        elif move[5] == "S" and move[6] == "E":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] + 1, self.white_king_inf[0][1] - 1))

                        elif move[5] == "S" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0], self.white_king_inf[0][1] - 1))

                        elif move[5] == "S" and move[6] == "W":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] - 1, self.white_king_inf[0][1] - 1))

                        elif move[5] == "W" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] - 1, self.white_king_inf[0][1]))

                        elif move[5] == "N" and move[6] == "W":

                            self.legal_moves.append(notation.get_notation("K", self.white_king_inf[0][0], self.white_king_inf[0][1], self.white_king_inf[0][0] - 1, self.white_king_inf[0][1] + 1))

            if self.white_king_inf[0][2] == True and self.white_king_inf[0][5] == True:

                move_list = ["O-O", "O-O-O"]

                king_moves = {
                    "O-O" : True,
                    "O-O-O" : True,
                    }

                for i in range(0, len(self.white_occupation_x)):

                    if self.white_king_inf[0][0] + 2 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O"] = False

                    elif self.white_king_inf[0][0] + 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O"] = False

                    if self.white_king_inf[0][0] - 3 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.white_king_inf[0][0] - 2 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.white_king_inf[0][0] - 1 == self.white_occupation_x[i] and self.white_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                for i in range(0, len(self.black_occupation_x)):

                    if self.white_king_inf[0][0] + 2 == self.black_occupation_x[i] and self.white_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O"] = False

                    elif self.white_king_inf[0][0] + 1 == self.black_occupation_x[i] and self.white_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O"] = False

                    if self.white_king_inf[0][0] - 3 == self.black_occupation_x[i] and self.white_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.white_king_inf[0][0] - 2 == self.black_occupation_x[i] and self.white_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.white_king_inf[0][0] - 1 == self.black_occupation_x[i] and self.white_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                for i in range(0, 2):

                    if self.white_rooks_inf[i][2] == False or self.white_rooks_inf[i][5] == False:

                        if i == 0:

                            king_moves["O-O-O"] = False

                        elif i == 1:

                            king_moves["O-O"] = False

                for move in move_list:

                    if king_moves[move] == True:

                        self.legal_moves.append(move)

        else:

            for i in range(0, 8):

                if self.black_pawns_inf[i][2] == True:

                    pawn_S_1 = True
                    pawn_S_2 = True
                    pawn_SE_11 = False
                    pawn_SW_11 = False
                    en_p_SE_11 = False
                    en_p_SW_11 = False

                    for j in range(0, len(self.black_occupation_x)):

                        if self.black_pawns_inf[i][0] == self.black_occupation_x[j] and self.black_pawns_inf[i][1] - 1 == self.black_occupation_y[j]:

                            pawn_S_1 = False

                        if self.black_pawns_inf[i][5] == True and self.black_pawns_inf[i][0] == self.black_occupation_x[j] and self.black_pawns_inf[i][1] - 2 == self.black_occupation_y[j]:

                            pawn_S_2 = False

                    for j in range(0, len(self.white_occupation_x)):

                        if self.black_pawns_inf[i][0] == self.white_occupation_x[j] and self.black_pawns_inf[i][1] - 1 == self.white_occupation_y[j]:

                            pawn_S_1 = False

                        if self.black_pawns_inf[i][5] == True and self.black_pawns_inf[i][0] == self.white_occupation_x[j] and self.black_pawns_inf[i][1] - 2 == self.white_occupation_y[j]:

                            pawn_S_2 = False

                        if self.black_pawns_inf[i][0] + 1 == self.white_occupation_x[j] and self.black_pawns_inf[i][1] - 1 == self.white_occupation_y[j]:

                            pawn_SE_11 = True

                        if self.black_pawns_inf[i][0] - 1 == self.white_occupation_x[j] and self.black_pawns_inf[i][1] - 1 == self.white_occupation_y[j]:

                            pawn_SW_11 = True

                    if self.black_pawns_inf[i][0] + 1 == self.en_passant_x_y[0] and self.black_pawns_inf[i][1] == self.en_passant_x_y[1]:

                        pawn_SE_11 = True

                    elif self.black_pawns_inf[i][0] - 1 == self.en_passant_x_y[0] and self.black_pawns_inf[i][1] == self.en_passant_x_y[1]:

                        pawn_SW_11 = True

                    if pawn_S_1 == True:

                        legal_move_notation = notation.get_notation("P", self.black_pawns_inf[i][0], self.black_pawns_inf[i][1], self.black_pawns_inf[i][0], self.black_pawns_inf[i][1] - 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_S_2 == True and pawn_S_1 == True and self.black_pawns_inf[i][5] == True:

                        legal_move_notation = notation.get_notation("P", self.black_pawns_inf[i][0], self.black_pawns_inf[i][1], self.black_pawns_inf[i][0], self.black_pawns_inf[i][1] - 2)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_SE_11 == True:

                        legal_move_notation = notation.get_notation("P", self.black_pawns_inf[i][0], self.black_pawns_inf[i][1], self.black_pawns_inf[i][0] + 1, self.black_pawns_inf[i][1] - 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

                    if pawn_SW_11 == True:

                        legal_move_notation = notation.get_notation("P", self.black_pawns_inf[i][0], self.black_pawns_inf[i][1], self.black_pawns_inf[i][0] - 1, self.black_pawns_inf[i][1] - 1)

                        if legal_move_notation[-1] == "=":

                            self.legal_moves.append(legal_move_notation + "Q")
                            self.legal_moves.append(legal_move_notation + "R")
                            self.legal_moves.append(legal_move_notation + "B")
                            self.legal_moves.append(legal_move_notation + "N")

                        else:

                            self.legal_moves.append(legal_move_notation)

            for i in range(0, 10):

                if self.black_bishops_inf[i][2] == True:

                    move_list = ["bishop_NE_1", "bishop_NE_2", "bishop_NE_3", "bishop_NE_4", "bishop_NE_5", "bishop_NE_6", "bishop_NE_7", "bishop_SE_1", "bishop_SE_2", "bishop_SE_3", "bishop_SE_4", "bishop_SE_5", "bishop_SE_6", "bishop_SE_7", "bishop_SW_1", "bishop_SW_2", "bishop_SW_3", "bishop_SW_4", "bishop_SW_5", "bishop_SW_6", "bishop_SW_7", "bishop_NW_1", "bishop_NW_2", "bishop_NW_3", "bishop_NW_4", "bishop_NW_5", "bishop_NW_6", "bishop_NW_7"]

                    bishop_moves = {
                        "bishop_NE_1" : True,
                        "bishop_NE_2" : True,
                        "bishop_NE_3" : True,
                        "bishop_NE_4" : True,
                        "bishop_NE_5" : True,
                        "bishop_NE_6" : True,
                        "bishop_NE_7" : True,
                        "bishop_SE_1" : True,
                        "bishop_SE_2" : True,
                        "bishop_SE_3" : True,
                        "bishop_SE_4" : True,
                        "bishop_SE_5" : True,
                        "bishop_SE_6" : True,
                        "bishop_SE_7" : True,
                        "bishop_SW_1" : True,
                        "bishop_SW_2" : True,
                        "bishop_SW_3" : True,
                        "bishop_SW_4" : True,
                        "bishop_SW_5" : True,
                        "bishop_SW_6" : True,
                        "bishop_SW_7" : True,
                        "bishop_NW_1" : True,
                        "bishop_NW_2" : True,
                        "bishop_NW_3" : True,
                        "bishop_NW_4" : True,
                        "bishop_NW_5" : True,
                        "bishop_NW_6" : True,
                        "bishop_NW_7" : True,
                        }

                    for j in range(1, 8):

                        if self.black_bishops_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[8] == "W" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.black_bishops_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[7] == "S" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.black_bishops_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[8] == "E" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                        if self.black_bishops_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[7] == "N" and int(move[10]) >= j:

                                    bishop_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.black_bishops_inf[i][0] + j == self.black_occupation_x[k] and self.black_bishops_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "E" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] + j == self.black_occupation_x[k] and self.black_bishops_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "E" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] - j == self.black_occupation_x[k] and self.black_bishops_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "W" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] - j == self.black_occupation_x[k] and self.black_bishops_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "W" and int(move[10]) >= j:

                                        bishop_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.black_bishops_inf[i][0] + j == self.white_occupation_x[k] and self.black_bishops_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "E" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] + j == self.white_occupation_x[k] and self.black_bishops_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "E" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] - j == self.white_occupation_x[k] and self.black_bishops_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "S" and move[8] == "W" and int(move[10]) > j:

                                        bishop_moves[move] = False

                            elif self.black_bishops_inf[i][0] - j == self.white_occupation_x[k] and self.black_bishops_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[7] == "N" and move[8] == "W" and int(move[10]) > j:

                                        bishop_moves[move] = False

                    for move in move_list:

                        if bishop_moves[move] == True:

                            if move[7] == "N" and move[8] == "E":

                                self.legal_moves.append(notation.get_notation("B", self.black_bishops_inf[i][0], self.black_bishops_inf[i][1], self.black_bishops_inf[i][0] + int(move[10]), self.black_bishops_inf[i][1] + int(move[10])))

                            elif move[7] == "S" and move[8] == "E":

                                self.legal_moves.append(notation.get_notation("B", self.black_bishops_inf[i][0], self.black_bishops_inf[i][1], self.black_bishops_inf[i][0] + int(move[10]), self.black_bishops_inf[i][1] - int(move[10])))

                            elif move[7] == "S" and move[8] == "W":

                                self.legal_moves.append(notation.get_notation("B", self.black_bishops_inf[i][0], self.black_bishops_inf[i][1], self.black_bishops_inf[i][0] - int(move[10]), self.black_bishops_inf[i][1] - int(move[10])))

                            elif move[7] == "N" and move[8] == "W":

                                self.legal_moves.append(notation.get_notation("B", self.black_bishops_inf[i][0], self.black_bishops_inf[i][1], self.black_bishops_inf[i][0] - int(move[10]), self.black_bishops_inf[i][1] + int(move[10])))

            for i in range(0, 10):

                if self.black_knights_inf[i][2] == True:

                    knight_NE_21 = True
                    knight_NE_12 = True
                    knight_SE_12 = True
                    knight_SE_21 = True
                    knight_SW_21 = True
                    knight_SW_12 = True
                    knight_NW_12 = True
                    knight_NW_21 = True

                    if self.black_knights_inf[i][0] - 1 < 0:

                        knight_SW_21 = False
                        knight_SW_12 = False
                        knight_NW_12 = False
                        knight_NW_21 = False

                    elif self.black_knights_inf[i][0] - 2 < 0:

                        knight_SW_12 = False
                        knight_NW_12 = False

                    if self.black_knights_inf[i][0] + 1 > 7:

                        knight_NE_21 = False
                        knight_NE_12 = False
                        knight_SE_12 = False
                        knight_SE_21 = False

                    elif self.black_knights_inf[i][0] + 2 > 7:

                        knight_NE_12 = False
                        knight_SE_12 = False

                    if self.black_knights_inf[i][1] - 1 < 0:

                        knight_SE_12 = False
                        knight_SE_21 = False
                        knight_SW_21 = False
                        knight_SW_12 = False

                    elif self.black_knights_inf[i][1] - 2 < 0:

                        knight_SE_21 = False
                        knight_SW_21 = False

                    if self.black_knights_inf[i][1] + 1 > 7:

                        knight_NE_21 = False
                        knight_NE_12 = False
                        knight_NW_12 = False
                        knight_NW_21 = False

                    elif self.black_knights_inf[i][1] + 2 > 7:

                        knight_NE_21 = False
                        knight_NW_21 = False

                    for j in range(0, len(self.black_occupation_x)):

                        if self.black_knights_inf[i][0] + 1 == self.black_occupation_x[j] and self.black_knights_inf[i][1] + 2 == self.black_occupation_y[j]:

                            knight_NE_21 = False

                        if self.black_knights_inf[i][0] + 2 == self.black_occupation_x[j] and self.black_knights_inf[i][1] + 1 == self.black_occupation_y[j]:

                            knight_NE_12 = False

                        if self.black_knights_inf[i][0] + 2 == self.black_occupation_x[j] and self.black_knights_inf[i][1] - 1 == self.black_occupation_y[j]:

                            knight_SE_12 = False

                        if self.black_knights_inf[i][0] + 1 == self.black_occupation_x[j] and self.black_knights_inf[i][1] - 2 == self.black_occupation_y[j]:

                            knight_SE_21 = False

                        if self.black_knights_inf[i][0] - 1 == self.black_occupation_x[j] and self.black_knights_inf[i][1] - 2 == self.black_occupation_y[j]:

                            knight_SW_21 = False

                        if self.black_knights_inf[i][0] - 2 == self.black_occupation_x[j] and self.black_knights_inf[i][1] - 1 == self.black_occupation_y[j]:

                            knight_SW_12 = False

                        if self.black_knights_inf[i][0] - 2 == self.black_occupation_x[j] and self.black_knights_inf[i][1] + 1 == self.black_occupation_y[j]:

                            knight_NW_12 = False

                        if self.black_knights_inf[i][0] - 1 == self.black_occupation_x[j] and self.black_knights_inf[i][1] + 2 == self.black_occupation_y[j]:

                            knight_NW_21 = False

                    if knight_NE_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] + 1, self.black_knights_inf[i][1] + 2))

                    if knight_NE_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] + 2, self.black_knights_inf[i][1] + 1))

                    if knight_SE_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] + 2, self.black_knights_inf[i][1] - 1))

                    if knight_SE_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] + 1, self.black_knights_inf[i][1] - 2))

                    if knight_SW_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] - 1, self.black_knights_inf[i][1] - 2))

                    if knight_SW_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] - 2, self.black_knights_inf[i][1] - 1))

                    if knight_NW_12 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] - 2, self.black_knights_inf[i][1] + 1))

                    if knight_NW_21 == True:

                        self.legal_moves.append(notation.get_notation("N", self.black_knights_inf[i][0], self.black_knights_inf[i][1], self.black_knights_inf[i][0] - 1, self.black_knights_inf[i][1] + 2))

            for i in range(0, 10):

                if self.black_rooks_inf[i][2] == True:

                    move_list = ["rook_N_1", "rook_N_2", "rook_N_3", "rook_N_4", "rook_N_5", "rook_N_6", "rook_N_7", "rook_E_1", "rook_E_2", "rook_E_3", "rook_E_4", "rook_E_5", "rook_E_6", "rook_E_7", "rook_S_1", "rook_S_2", "rook_S_3", "rook_S_4", "rook_S_5", "rook_S_6", "rook_S_7", "rook_W_1", "rook_W_2", "rook_W_3", "rook_W_4", "rook_W_5", "rook_W_6", "rook_W_7"]

                    rook_moves = {
                        "rook_N_1" : True,
                        "rook_N_2" : True,
                        "rook_N_3" : True,
                        "rook_N_4" : True,
                        "rook_N_5" : True,
                        "rook_N_6" : True,
                        "rook_N_7" : True,
                        "rook_E_1" : True,
                        "rook_E_2" : True,
                        "rook_E_3" : True,
                        "rook_E_4" : True,
                        "rook_E_5" : True,
                        "rook_E_6" : True,
                        "rook_E_7" : True,
                        "rook_S_1" : True,
                        "rook_S_2" : True,
                        "rook_S_3" : True,
                        "rook_S_4" : True,
                        "rook_S_5" : True,
                        "rook_S_6" : True,
                        "rook_S_7" : True,
                        "rook_W_1" : True,
                        "rook_W_2" : True,
                        "rook_W_3" : True,
                        "rook_W_4" : True,
                        "rook_W_5" : True,
                        "rook_W_6" : True,
                        "rook_W_7" : True,
                        }

                    for j in range(1, 8):

                        if self.black_rooks_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[5] == "W" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.black_rooks_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[5] == "S" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.black_rooks_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[5] == "E" and int(move[7]) >= j:

                                    rook_moves[move] = False

                        if self.black_rooks_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[5] == "N" and int(move[7]) >= j:

                                    rook_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.black_rooks_inf[i][0] == self.black_occupation_x[k] and self.black_rooks_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "N" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] + j == self.black_occupation_x[k] and self.black_rooks_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "E" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] == self.black_occupation_x[k] and self.black_rooks_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "S" and int(move[7]) >= j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] - j == self.black_occupation_x[k] and self.black_rooks_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "W" and int(move[7]) >= j:

                                        rook_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.black_rooks_inf[i][0] == self.white_occupation_x[k] and self.black_rooks_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "N" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] + j == self.white_occupation_x[k] and self.black_rooks_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "E" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] == self.white_occupation_x[k] and self.black_rooks_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "S" and int(move[7]) > j:

                                        rook_moves[move] = False

                            elif self.black_rooks_inf[i][0] - j == self.white_occupation_x[k] and self.black_rooks_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[5] == "W" and int(move[7]) > j:

                                        rook_moves[move] = False

                    for move in move_list:

                        if rook_moves[move] == True:

                            if move[5] == "N":

                                self.legal_moves.append(notation.get_notation("R", self.black_rooks_inf[i][0], self.black_rooks_inf[i][1], self.black_rooks_inf[i][0], self.black_rooks_inf[i][1] + int(move[7])))

                            elif move[5] == "E":

                                self.legal_moves.append(notation.get_notation("R", self.black_rooks_inf[i][0], self.black_rooks_inf[i][1], self.black_rooks_inf[i][0] + int(move[7]), self.black_rooks_inf[i][1]))

                            elif move[5] == "S":

                                self.legal_moves.append(notation.get_notation("R", self.black_rooks_inf[i][0], self.black_rooks_inf[i][1], self.black_rooks_inf[i][0], self.black_rooks_inf[i][1] - int(move[7])))

                            elif move[5] == "W":

                                self.legal_moves.append(notation.get_notation("R", self.black_rooks_inf[i][0], self.black_rooks_inf[i][1], self.black_rooks_inf[i][0] - int(move[7]), self.black_rooks_inf[i][1]))

            for i in range(0, 9):

                if self.black_queens_inf[i][2] == True:

                    move_list = ["queen_N_1", "queen_N_2", "queen_N_3", "queen_N_4", "queen_N_5", "queen_N_6", "queen_N_7", "queen_NE_1", "queen_NE_2", "queen_NE_3", "queen_NE_4", "queen_NE_5", "queen_NE_6", "queen_NE_7", "queen_E_1", "queen_E_2", "queen_E_3", "queen_E_4", "queen_E_5", "queen_E_6", "queen_E_7", "queen_SE_1", "queen_SE_2", "queen_SE_3", "queen_SE_4", "queen_SE_5", "queen_SE_6", "queen_SE_7", "queen_S_1", "queen_S_2", "queen_S_3", "queen_S_4", "queen_S_5", "queen_S_6", "queen_S_7", "queen_SW_1", "queen_SW_2", "queen_SW_3", "queen_SW_4", "queen_SW_5", "queen_SW_6", "queen_SW_7", "queen_W_1", "queen_W_2", "queen_W_3", "queen_W_4", "queen_W_5", "queen_W_6", "queen_W_7", "queen_NW_1", "queen_NW_2", "queen_NW_3", "queen_NW_4", "queen_NW_5", "queen_NW_6", "queen_NW_7"]

                    queen_moves = {
                        "queen_N_1" : True,
                        "queen_N_2" : True,
                        "queen_N_3" : True,
                        "queen_N_4" : True,
                        "queen_N_5" : True,
                        "queen_N_6" : True,
                        "queen_N_7" : True,
                        "queen_NE_1" : True,
                        "queen_NE_2" : True,
                        "queen_NE_3" : True,
                        "queen_NE_4" : True,
                        "queen_NE_5" : True,
                        "queen_NE_6" : True,
                        "queen_NE_7" : True,
                        "queen_E_1" : True,
                        "queen_E_2" : True,
                        "queen_E_3" : True,
                        "queen_E_4" : True,
                        "queen_E_5" : True,
                        "queen_E_6" : True,
                        "queen_E_7" : True,
                        "queen_SE_1" : True,
                        "queen_SE_2" : True,
                        "queen_SE_3" : True,
                        "queen_SE_4" : True,
                        "queen_SE_5" : True,
                        "queen_SE_6" : True,
                        "queen_SE_7" : True,
                        "queen_S_1" : True,
                        "queen_S_2" : True,
                        "queen_S_3" : True,
                        "queen_S_4" : True,
                        "queen_S_5" : True,
                        "queen_S_6" : True,
                        "queen_S_7" : True,
                        "queen_SW_1" : True,
                        "queen_SW_2" : True,
                        "queen_SW_3" : True,
                        "queen_SW_4" : True,
                        "queen_SW_5" : True,
                        "queen_SW_6" : True,
                        "queen_SW_7" : True,
                        "queen_W_1" : True,
                        "queen_W_2" : True,
                        "queen_W_3" : True,
                        "queen_W_4" : True,
                        "queen_W_5" : True,
                        "queen_W_6" : True,
                        "queen_W_7" : True,
                        "queen_NW_1" : True,
                        "queen_NW_2" : True,
                        "queen_NW_3" : True,
                        "queen_NW_4" : True,
                        "queen_NW_5" : True,
                        "queen_NW_6" : True,
                        "queen_NW_7" : True,
                        }

                    for j in range(1, 8):

                        if self.black_queens_inf[i][0] - j < 0:

                            for move in move_list:

                                if move[6] == "W" or move[7] == "W":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.black_queens_inf[i][1] - j < 0:

                            for move in move_list:

                                if move[6] == "S":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.black_queens_inf[i][0] + j > 7:

                            for move in move_list:

                                if move[6] == "E" or move[7] == "E":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                        if self.black_queens_inf[i][1] + j > 7:

                            for move in move_list:

                                if move[6] == "N":

                                    if move[7] == "_":

                                        if int(move[8]) >= j:

                                            queen_moves[move] = False

                                    elif int(move[9]) >= j:

                                        queen_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.black_occupation_x)):

                            if self.black_queens_inf[i][0] == self.black_occupation_x[k] and self.black_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.black_occupation_x[k] and self.black_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "E" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.black_occupation_x[k] and self.black_queens_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "E" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.black_occupation_x[k] and self.black_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "E" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] == self.black_occupation_x[k] and self.black_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.black_occupation_x[k] and self.black_queens_inf[i][1] - j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "W" and int(move[9]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.black_occupation_x[k] and self.black_queens_inf[i][1] == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "W" and move[7] == "_" and int(move[8]) >= j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.black_occupation_x[k] and self.black_queens_inf[i][1] + j == self.black_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "W" and int(move[9]) >= j:

                                        queen_moves[move] = False

                    for j in range(1, 8):

                        for k in range(0, len(self.white_occupation_x)):

                            if self.black_queens_inf[i][0] == self.white_occupation_x[k] and self.black_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.white_occupation_x[k] and self.black_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "E" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.white_occupation_x[k] and self.black_queens_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "E" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] + j == self.white_occupation_x[k] and self.black_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "E" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] == self.white_occupation_x[k] and self.black_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.white_occupation_x[k] and self.black_queens_inf[i][1] - j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "S" and move[7] == "W" and int(move[9]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.white_occupation_x[k] and self.black_queens_inf[i][1] == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "W" and move[7] == "_" and int(move[8]) > j:

                                        queen_moves[move] = False

                            elif self.black_queens_inf[i][0] - j == self.white_occupation_x[k] and self.black_queens_inf[i][1] + j == self.white_occupation_y[k]:

                                for move in move_list:

                                    if move[6] == "N" and move[7] == "W" and int(move[9]) > j:

                                        queen_moves[move] = False

                    for move in move_list:

                        if queen_moves[move] == True:

                            if move[6] == "N" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0], self.black_queens_inf[i][1] + int(move[8])))

                            elif move[6] == "N" and move[7] == "E":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] + int(move[9]), self.black_queens_inf[i][1] + int(move[9])))

                            elif move[6] == "E" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] + int(move[8]), self.black_queens_inf[i][1]))

                            elif move[6] == "S" and move[7] == "E":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] + int(move[9]), self.black_queens_inf[i][1] - int(move[9])))

                            elif move[6] == "S" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0], self.black_queens_inf[i][1] - int(move[8])))

                            elif move[6] == "S" and move[7] == "W":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] - int(move[9]), self.black_queens_inf[i][1] - int(move[9])))

                            elif move[6] == "W" and move[7] == "_":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] - int(move[8]), self.black_queens_inf[i][1]))

                            elif move[6] == "N" and move[7] == "W":

                                self.legal_moves.append(notation.get_notation("Q", self.black_queens_inf[i][0], self.black_queens_inf[i][1], self.black_queens_inf[i][0] - int(move[9]), self.black_queens_inf[i][1] + int(move[9])))

            if self.black_king_inf[0][2] == True:

                move_list = ["king_N_1", "king_NE_1", "king_E_1", "king_SE_1", "king_S_1", "king_SW_1", "king_W_1", "king_NW_1"]

                king_moves = {
                    "king_N_1" : True,
                    "king_NE_1" : True,
                    "king_E_1" : True,
                    "king_SE_1" : True,
                    "king_S_1" : True,
                    "king_SW_1" : True,
                    "king_W_1" : True,
                    "king_NW_1" : True,
                    }

                if self.black_king_inf[0][0] - 1 < 0:

                    for move in move_list:

                        if move[5] == "W" or move[6] == "W":

                            king_moves[move] = False

                if self.black_king_inf[0][1] - 1 < 0:

                    for move in move_list:

                        if move[5] == "S":

                            king_moves[move] = False

                if self.black_king_inf[0][0] + 1 > 7:

                    for move in move_list:

                        if move[5] == "E" or move[6] == "E":

                            king_moves[move] = False

                if self.black_king_inf[0][1] + 1 > 7:

                    for move in move_list:

                        if move[5] == "N":

                            king_moves[move] = False

                for i in range(0, len(self.black_occupation_x)):

                    if self.black_king_inf[0][0] == self.black_occupation_x[i] and self.black_king_inf[0][1] + 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "_":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] + 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] + 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "E":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] + 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "E" and move[6] == "_":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] + 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] - 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "E":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] == self.black_occupation_x[i] and self.black_king_inf[0][1] - 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "_":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] - 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] - 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "S" and move[6] == "W":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] - 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "W" and move[6] == "_":

                                king_moves[move] = False

                    elif self.black_king_inf[0][0] - 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] + 1 == self.black_occupation_y[i]:

                        for move in move_list:

                            if move[5] == "N" and move[6] == "W":

                                king_moves[move] = False

                for move in move_list:

                    if king_moves[move] == True:

                        if move[5] == "N" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0], self.black_king_inf[0][1] + 1))

                        elif move[5] == "N" and move[6] == "E":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] + 1, self.black_king_inf[0][1] + 1))

                        elif move[5] == "E" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] + 1, self.black_king_inf[0][1]))

                        elif move[5] == "S" and move[6] == "E":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] + 1, self.black_king_inf[0][1] - 1))

                        elif move[5] == "S" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0], self.black_king_inf[0][1] - 1))

                        elif move[5] == "S" and move[6] == "W":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] - 1, self.black_king_inf[0][1] - 1))

                        elif move[5] == "W" and move[6] == "_":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] - 1, self.black_king_inf[0][1]))

                        elif move[5] == "N" and move[6] == "W":

                            self.legal_moves.append(notation.get_notation("K", self.black_king_inf[0][0], self.black_king_inf[0][1], self.black_king_inf[0][0] - 1, self.black_king_inf[0][1] + 1))

            if self.black_king_inf[0][2] == True and self.black_king_inf[0][5] == True:

                move_list = ["O-O", "O-O-O"]

                king_moves = {
                    "O-O" : True,
                    "O-O-O" : True,
                    }

                for i in range(0, len(self.white_occupation_x)):

                    if self.black_king_inf[0][0] + 2 == self.white_occupation_x[i] and self.black_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O"] = False

                    elif self.black_king_inf[0][0] + 1 == self.white_occupation_x[i] and self.black_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O"] = False

                    if self.black_king_inf[0][0] - 3 == self.white_occupation_x[i] and self.black_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.black_king_inf[0][0] - 2 == self.white_occupation_x[i] and self.black_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.black_king_inf[0][0] - 1 == self.white_occupation_x[i] and self.black_king_inf[0][1] == self.white_occupation_y[i]:

                        king_moves["O-O-O"] = False

                for i in range(0, len(self.black_occupation_x)):

                    if self.black_king_inf[0][0] + 2 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O"] = False

                    elif self.black_king_inf[0][0] + 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O"] = False

                    if self.black_king_inf[0][0] - 3 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.black_king_inf[0][0] - 2 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                    elif self.black_king_inf[0][0] - 1 == self.black_occupation_x[i] and self.black_king_inf[0][1] == self.black_occupation_y[i]:

                        king_moves["O-O-O"] = False

                for i in range(0, 2):

                    if self.black_rooks_inf[i][2] == False or self.black_rooks_inf[i][5] == False:

                        if i == 0:

                            king_moves["O-O-O"] = False

                        elif i == 1:

                            king_moves["O-O"] = False

                for move in move_list:

                    if king_moves[move] == True:

                        self.legal_moves.append(move)

        #print(self.legal_moves)

        self.legal_moves_move_notation = self.legal_moves

    def check_checks(self):

        moves = deepcopy(self.legal_moves)

        white_short_castle_through_check_check = False
        white_long_castle_through_check_check = False
        black_short_castle_through_check_check = False
        black_long_castle_through_check_check = False

        for move in moves:

            white_pawns = deepcopy(self.white_pawns_inf)
            white_bishops = deepcopy(self.white_bishops_inf)
            white_knights = deepcopy(self.white_knights_inf)
            white_rooks = deepcopy(self.white_rooks_inf)
            white_queens = deepcopy(self.white_queens_inf)
            white_king = deepcopy(self.white_king_inf)

            black_pawns = deepcopy(self.black_pawns_inf)
            black_bishops = deepcopy(self.black_bishops_inf)
            black_knights = deepcopy(self.black_knights_inf)
            black_rooks = deepcopy(self.black_rooks_inf)
            black_queens = deepcopy(self.black_queens_inf)
            black_king = deepcopy(self.black_king_inf)

            #en_passant_xy = deepcopy(self.en_passant_x_y)

            #white_occ_x = deepcopy(self.white_occupation_x)
            #white_occ_y = deepcopy(self.white_occupation_y)

            #black_occ_x = deepcopy(self.black_occupation_x)
            #black_occ_y = deepcopy(self.black_occupation_y)

            notation_val, take = self.convert_to_easy_notation(move)

            if notation_val == "Ke1f1" and startup.white_turn == True:

                white_short_castle_through_check_check = True

            if notation_val == "Ke1d1" and startup.white_turn == True:

                white_long_castle_through_check_check = True

            if notation_val == "Ke8f8" and startup.white_turn == False:

                black_short_castle_through_check_check = True

            if notation_val == "Ke8d8" and startup.white_turn == False:

                black_long_castle_through_check_check = True

            if notation_val[0] == "B":

                fromx = notation.get_column_char(notation_val[1])
                fromy = int(notation_val[2]) - 1

                tox = notation.get_column_char(notation_val[3])
                toy = int(notation_val[4]) - 1

                if startup.white_turn == True:

                    for i in range(0, 10):

                        if white_bishops[i][2] == True and white_bishops[i][0] == fromx and white_bishops[i][1] == fromy:

                            white_bishops[i][0] = tox
                            white_bishops[i][1] = toy

                else:

                    for i in range(0, 10):

                        if black_bishops[i][2] == True and black_bishops[i][0] == fromx and black_bishops[i][1] == fromy:

                            black_bishops[i][0] = tox
                            black_bishops[i][1] = toy

            elif notation_val[0] == "N":

                fromx = notation.get_column_char(notation_val[1])
                fromy = int(notation_val[2]) - 1

                tox = notation.get_column_char(notation_val[3])
                toy = int(notation_val[4]) - 1

                if startup.white_turn == True:

                    for i in range(0, 10):

                        if white_knights[i][2] == True and white_knights[i][0] == fromx and white_knights[i][1] == fromy:

                            white_knights[i][0] = tox
                            white_knights[i][1] = toy

                else:

                    for i in range(0, 10):

                        if black_knights[i][2] == True and black_knights[i][0] == fromx and black_knights[i][1] == fromy:

                            black_knights[i][0] = tox
                            black_knights[i][1] = toy

            elif notation_val[0] == "R":

                fromx = notation.get_column_char(notation_val[1])
                fromy = int(notation_val[2]) - 1

                tox = notation.get_column_char(notation_val[3])
                toy = int(notation_val[4]) - 1

                if startup.white_turn == True:

                    for i in range(0, 10):

                        if white_rooks[i][2] == True and white_rooks[i][0] == fromx and white_rooks[i][1] == fromy:

                            white_rooks[i][0] = tox
                            white_rooks[i][1] = toy
                            white_rooks[i][5] = False

                else:

                    for i in range(0, 10):

                        if black_rooks[i][2] == True and black_rooks[i][0] == fromx and black_rooks[i][1] == fromy:

                            black_rooks[i][0] = tox
                            black_rooks[i][1] = toy
                            black_rooks[i][5] = False

            elif notation_val[0] == "Q":

                fromx = notation.get_column_char(notation_val[1])
                fromy = int(notation_val[2]) - 1

                tox = notation.get_column_char(notation_val[3])
                toy = int(notation_val[4]) - 1

                if startup.white_turn == True:

                    for i in range(0, 9):

                        if white_queens[i][2] == True and white_queens[i][0] == fromx and white_queens[i][1] == fromy:

                            white_queens[i][0] = tox
                            white_queens[i][1] = toy

                else:

                    for i in range(0, 9):

                        if black_queens[i][2] == True and black_queens[i][0] == fromx and black_queens[i][1] == fromy:

                            black_queens[i][0] = tox
                            black_queens[i][1] = toy

            elif notation_val[0] == "K":

                fromx = notation.get_column_char(notation_val[1])
                fromy = int(notation_val[2]) - 1

                tox = notation.get_column_char(notation_val[3])
                toy = int(notation_val[4]) - 1

                if startup.white_turn == True:

                    if white_king[0][2] == True and white_king[0][0] == fromx and white_king[0][1] == fromy:

                        white_king[0][0] = tox
                        white_king[0][1] = toy
                        white_king[0][5] = False

                else:

                    if black_king[0][2] == True and black_king[0][0] == fromx and black_king[0][1] == fromy:

                        black_king[0][0] = tox
                        black_king[0][1] = toy
                        black_king[0][5] = False

            elif notation_val[0] == "O":

                if startup.white_turn == True:

                    white_king[0][5] = False

                    if notation_val == "O-O":

                        white_rooks[1][5] = False

                        white_king[0][0] = 6
                        white_king[0][1] = 0

                        for i in range(0, 2):

                            if white_rooks[i][0] == 7:

                                white_rooks[i][0] = 5
                                white_rooks[i][1] = 0

                    elif notation_val == "O-O-O":

                        white_rooks[0][5] = False

                        white_king[0][0] = 2
                        white_king[0][1] = 0

                        for i in range(0, 2):

                            if white_rooks[i][0] == 0:

                                white_rooks[i][0] = 3
                                white_rooks[i][1] = 0

                else:

                    black_king[0][5] = False

                    if notation_val == "O-O":

                        black_rooks[1][5] = False

                        black_king[0][0] = 6
                        black_king[0][1] = 7

                        for i in range(0, 2):

                            if black_rooks[i][0] == 7:

                                black_rooks[i][0] = 5
                                black_rooks[i][1] = 7

                    elif notation_val == "O-O-O":

                        black_rooks[0][5] = False

                        black_king[0][0] = 2
                        black_king[0][1] = 7

                        for i in range(0, 2):

                            if black_rooks[i][0] == 0:

                                black_rooks[i][0] = 3
                                black_rooks[i][1] = 7

            else:

                if True:

                    if notation_val[-2] == "=":

                        tox = notation.get_column_char(notation_val[-4])
                        toy = int(notation_val[-3]) - 1

                    else:

                        tox = notation.get_column_char(notation_val[-2])
                        toy = int(notation_val[-1]) - 1

                    if take == True:

                        if notation_val[-2] == "=":

                            fromx = notation.get_column_char(notation_val[-5])

                        else:

                            fromx = notation.get_column_char(notation_val[-3])

                        if startup.white_turn == True:

                            fromy = toy - 1

                        else:

                            fromy = toy + 1

                    else:

                        fromx = tox

                        if startup.white_turn == True:

                            if toy == 3:

                                fromy = toy - 2

                                for i in range(0, 8):

                                    if white_pawns[i][2] == True and white_pawns[i][0] == fromx and white_pawns[i][1] == toy - 1:

                                        fromy = toy - 1

                            else:

                                fromy = toy - 1

                        else:

                            if toy == 4:

                                fromy = toy + 2

                                for i in range(0, 8):

                                    if black_pawns[i][2] == True and black_pawns[i][0] == fromx and black_pawns[i][1] == toy + 1:

                                        fromy = toy + 1

                            else:

                                fromy = toy + 1

                    if startup.white_turn == True:

                        for i in range(0, 8):

                            if white_pawns[i][2] == True and white_pawns[i][0] == fromx and white_pawns[i][1] == fromy:

                                if toy == 7:

                                    white_pawns[i][2] = False

                                    if notation_val[-1] == "Q":

                                        promotion_complete = False

                                        for i in range(1, 9):

                                            if white_queens[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                white_queens[i][0] = tox
                                                white_queens[i][1] = toy
                                                white_queens[i][2] = True

                                    elif notation_val[-1] == "R":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if white_rooks[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                white_rooks[i][0] = tox
                                                white_rooks[i][1] = toy
                                                white_rooks[i][2] = True
                                                white_rooks[i][5] = False

                                    elif notation_val[-1] == "B":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if white_bishops[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                white_bishops[i][0] = tox
                                                white_bishops[i][1] = toy
                                                white_bishops[i][2] = True

                                    elif notation_val[-1] == "N":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if white_knights[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                white_knights[i][0] = tox
                                                white_knights[i][1] = toy
                                                white_knights[i][2] = True

                                else:

                                    white_pawns[i][0] = tox
                                    white_pawns[i][1] = toy
                                    white_pawns[i][5] = False

                    else:

                        for i in range(0, 8):

                            if black_pawns[i][2] == True and black_pawns[i][0] == fromx and black_pawns[i][1] == fromy:

                                if toy == 0:

                                    black_pawns[i][2] = False

                                    if notation_val[-1] == "Q":

                                        promotion_complete = False

                                        for i in range(1, 9):

                                            if black_queens[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                black_queens[i][0] = tox
                                                black_queens[i][1] = toy
                                                black_queens[i][2] = True

                                    elif notation_val[-1] == "R":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if black_rooks[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                black_rooks[i][0] = tox
                                                black_rooks[i][1] = toy
                                                black_rooks[i][2] = True
                                                black_rooks[i][5] = False

                                    elif notation_val[-1] == "B":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if black_bishops[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                black_bishops[i][0] = tox
                                                black_bishops[i][1] = toy
                                                black_bishops[i][2] = True

                                    elif notation_val[-1] == "N":

                                        promotion_complete = False

                                        for i in range(2, 10):

                                            if black_knights[i][2] == False and promotion_complete == False:

                                                promotion_complete = True

                                                black_knights[i][0] = tox
                                                black_knights[i][1] = toy
                                                black_knights[i][2] = True

                                else:

                                    black_pawns[i][0] = tox
                                    black_pawns[i][1] = toy
                                    black_pawns[i][5] = False

            if take == True:

                piece_taken = False

                if startup.white_turn == True:

                    for i in range(0, 8):

                        if black_pawns[i][2] == True and black_pawns[i][0] == tox and black_pawns[i][1] == toy:

                            black_pawns[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if black_bishops[i][2] == True and black_bishops[i][0] == tox and black_bishops[i][1] == toy:

                            black_bishops[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if black_knights[i][2] == True and black_knights[i][0] == tox and black_knights[i][1] == toy:

                            black_knights[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if black_rooks[i][2] == True and black_rooks[i][0] == tox and black_rooks[i][1] == toy:

                            black_rooks[i][2] = False

                            piece_taken = True

                    for i in range(0, 9):

                        if black_queens[i][2] == True and black_queens[i][0] == tox and black_queens[i][1] == toy:

                            black_queens[i][2] = False

                            piece_taken = True

                    if piece_taken == False:

                        for i in range(0, 8):

                            if black_pawns[i][2] == True and black_pawns[i][0] == tox and black_pawns[i][1] == toy - 1:

                                black_pawns[i][2] = False

                else:

                    for i in range(0, 8):

                        if white_pawns[i][2] == True and white_pawns[i][0] == tox and white_pawns[i][1] == toy:

                            white_pawns[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if white_bishops[i][2] == True and white_bishops[i][0] == tox and white_bishops[i][1] == toy:

                            white_bishops[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if white_knights[i][2] == True and white_knights[i][0] == tox and white_knights[i][1] == toy:

                            white_knights[i][2] = False

                            piece_taken = True

                    for i in range(0, 10):

                        if white_rooks[i][2] == True and white_rooks[i][0] == tox and white_rooks[i][1] == toy:

                            white_rooks[i][2] = False

                            piece_taken = True

                    for i in range(0, 9):

                        if white_queens[i][2] == True and white_queens[i][0] == tox and white_queens[i][1] == toy:

                            white_queens[i][2] = False

                            piece_taken = True

                    if piece_taken == False:

                        for i in range(0, 8):

                            if white_pawns[i][2] == True and white_pawns[i][0] == tox and white_pawns[i][1] == toy + 1:

                                white_pawns[i][2] = False

            white_occ_x = []
            white_occ_y = []
            black_occ_x = []
            black_occ_y = []

            for i in range(0, 8):

                if white_pawns[i][2] == True:

                    white_occ_x.append(white_pawns[i][0])
                    white_occ_y.append(white_pawns[i][1])

            for i in range(0, 10):

                if white_knights[i][2] == True:

                    white_occ_x.append(white_knights[i][0])
                    white_occ_y.append(white_knights[i][1])

            for i in range(0, 10):

                if white_bishops[i][2] == True:

                    white_occ_x.append(white_bishops[i][0])
                    white_occ_y.append(white_bishops[i][1])

            for i in range(0, 10):

                if white_rooks[i][2] == True:

                    white_occ_x.append(white_rooks[i][0])
                    white_occ_y.append(white_rooks[i][1])

            for i in range(0, 9):

                if white_queens[i][2] == True:

                    white_occ_x.append(white_queens[i][0])
                    white_occ_y.append(white_queens[i][1])

            if white_king[0][2] == True:

                white_occ_x.append(white_king[0][0])
                white_occ_y.append(white_king[0][1])

            for i in range(0, 8):

                if black_pawns[i][2] == True:

                    black_occ_x.append(black_pawns[i][0])
                    black_occ_y.append(black_pawns[i][1])

            for i in range(0, 10):

                if black_knights[i][2] == True:

                    black_occ_x.append(black_knights[i][0])
                    black_occ_y.append(black_knights[i][1])

            for i in range(0, 10):

                if black_bishops[i][2] == True:

                    black_occ_x.append(black_bishops[i][0])
                    black_occ_y.append(black_bishops[i][1])

            for i in range(0, 10):

                if black_rooks[i][2] == True:

                    black_occ_x.append(black_rooks[i][0])
                    black_occ_y.append(black_rooks[i][1])

            for i in range(0, 9):

                if black_queens[i][2] == True:

                    black_occ_x.append(black_queens[i][0])
                    black_occ_y.append(black_queens[i][1])

            if black_king[0][2] == True:

                black_occ_x.append(black_king[0][0])
                black_occ_y.append(black_king[0][1])

            if startup.white_turn == True:

                for i in range(0, 8):

                    if white_king[0][0] + 1 == black_pawns[i][0] and white_king[0][1] + 1 == black_pawns[i][1] and black_pawns[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] - 1 == black_pawns[i][0] and white_king[0][1] + 1 == black_pawns[i][1] and black_pawns[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    if white_king[0][0] + 1 == black_knights[i][0] and white_king[0][1] + 2 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] + 2 == black_knights[i][0] and white_king[0][1] + 1 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] + 2 == black_knights[i][0] and white_king[0][1] - 1 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] + 1 == black_knights[i][0] and white_king[0][1] - 2 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] - 1 == black_knights[i][0] and white_king[0][1] - 2 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] - 2 == black_knights[i][0] and white_king[0][1] - 1 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] - 2 == black_knights[i][0] and white_king[0][1] + 1 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif white_king[0][0] - 1 == black_knights[i][0] and white_king[0][1] + 2 == black_knights[i][1] and black_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    remove = True

                    if black_bishops[i][2] == True and abs(black_bishops[i][0] - white_king[0][0]) == abs(black_bishops[i][1] - white_king[0][1]):

                        if black_bishops[i][0] > white_king[0][0]:

                            if black_bishops[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_bishops[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_bishops[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                        else:

                            if black_bishops[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_bishops[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_bishops[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                        if remove == True and move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    remove = True

                    if black_rooks[i][2] == True:

                        if black_rooks[i][0] == white_king[0][0]:

                            if black_rooks[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_rooks[i][1] - white_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_rooks[i][1] - white_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                        elif black_rooks[i][1] == white_king[0][1]:

                            if black_rooks[i][0] > white_king[0][0]:

                                for j in range(1, abs(black_rooks[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1]:

                                            remove = False

                            else:

                                for j in range(1, abs(black_rooks[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1]:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                for i in range(0, 9):

                    remove = True

                    if black_queens[i][2] == True and abs(black_queens[i][0] - white_king[0][0]) == abs(black_queens[i][1] - white_king[0][1]):

                        if black_queens[i][0] > white_king[0][0]:

                            if black_queens[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                        else:

                            if black_queens[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                        if remove == True and move in self.legal_moves:

                            self.legal_moves.remove(move)

                    remove = True

                    if black_queens[i][2] == True:

                        if black_queens[i][0] == white_king[0][0]:

                            if black_queens[i][1] > white_king[0][1]:

                                for j in range(1, abs(black_queens[i][1] - white_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] and white_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] and black_occ_y[k] == white_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(black_queens[i][1] - white_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] and white_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] and black_occ_y[k] == white_king[0][1] - j:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                        elif black_queens[i][1] == white_king[0][1]:

                            if black_queens[i][0] > white_king[0][0]:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] + j and white_occ_y[k] == white_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] + j and black_occ_y[k] == white_king[0][1]:

                                            remove = False

                            else:

                                for j in range(1, abs(black_queens[i][0] - white_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == white_king[0][0] - j and white_occ_y[k] == white_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == white_king[0][0] - j and black_occ_y[k] == white_king[0][1]:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                if abs(black_king[0][0] - white_king[0][0]) <= 1 and abs(black_king[0][1] - white_king[0][1]) <= 1:

                    if move in self.legal_moves:

                        self.legal_moves.remove(move)

            else:

                for i in range(0, 8):

                    if black_king[0][0] + 1 == white_pawns[i][0] and black_king[0][1] - 1 == white_pawns[i][1] and white_pawns[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] - 1 == white_pawns[i][0] and black_king[0][1] - 1 == white_pawns[i][1] and white_pawns[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    if black_king[0][0] + 1 == white_knights[i][0] and black_king[0][1] + 2 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] + 2 == white_knights[i][0] and black_king[0][1] + 1 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] + 2 == white_knights[i][0] and black_king[0][1] - 1 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] + 1 == white_knights[i][0] and black_king[0][1] - 2 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] - 1 == white_knights[i][0] and black_king[0][1] - 2 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] - 2 == white_knights[i][0] and black_king[0][1] - 1 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] - 2 == white_knights[i][0] and black_king[0][1] + 1 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                    elif black_king[0][0] - 1 == white_knights[i][0] and black_king[0][1] + 2 == white_knights[i][1] and white_knights[i][2] == True:

                        if move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    remove = True

                    if white_bishops[i][2] == True and abs(white_bishops[i][0] - black_king[0][0]) == abs(white_bishops[i][1] - black_king[0][1]):

                        if white_bishops[i][0] > black_king[0][0]:

                            if white_bishops[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_bishops[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_bishops[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                        else:

                            if white_bishops[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_bishops[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_bishops[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                        if remove == True and move in self.legal_moves:

                            self.legal_moves.remove(move)

                for i in range(0, 10):

                    remove = True

                    if white_rooks[i][2] == True:

                        if white_rooks[i][0] == black_king[0][0]:

                            if white_rooks[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_rooks[i][1] - black_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_rooks[i][1] - black_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                        elif white_rooks[i][1] == black_king[0][1]:

                            if white_rooks[i][0] > black_king[0][0]:

                                for j in range(1, abs(white_rooks[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1]:

                                            remove = False

                            else:

                                for j in range(1, abs(white_rooks[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1]:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                for i in range(0, 9):

                    remove = True

                    if white_queens[i][2] == True and abs(white_queens[i][0] - black_king[0][0]) == abs(white_queens[i][1] - black_king[0][1]):

                        if white_queens[i][0] > black_king[0][0]:

                            if white_queens[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                        else:

                            if white_queens[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                        if remove == True and move in self.legal_moves:

                            self.legal_moves.remove(move)

                    remove = True

                    if white_queens[i][2] == True:

                        if white_queens[i][0] == black_king[0][0]:

                            if white_queens[i][1] > black_king[0][1]:

                                for j in range(1, abs(white_queens[i][1] - black_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] and white_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] and black_occ_y[k] == black_king[0][1] + j:

                                            remove = False

                            else:

                                for j in range(1, abs(white_queens[i][1] - black_king[0][1])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] and white_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] and black_occ_y[k] == black_king[0][1] - j:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                        elif white_queens[i][1] == black_king[0][1]:

                            if white_queens[i][0] > black_king[0][0]:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] + j and white_occ_y[k] == black_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] + j and black_occ_y[k] == black_king[0][1]:

                                            remove = False

                            else:

                                for j in range(1, abs(white_queens[i][0] - black_king[0][0])):

                                    for k in range(0, len(white_occ_x)):

                                        if white_occ_x[k] == black_king[0][0] - j and white_occ_y[k] == black_king[0][1]:

                                            remove = False

                                    for k in range(0, len(black_occ_x)):

                                        if black_occ_x[k] == black_king[0][0] - j and black_occ_y[k] == black_king[0][1]:

                                            remove = False

                            if remove == True and move in self.legal_moves:

                                self.legal_moves.remove(move)

                if abs(white_king[0][0] - black_king[0][0]) <= 1 and abs(white_king[0][1] - black_king[0][1]) <= 1:

                    if move in self.legal_moves:

                        self.legal_moves.remove(move)

            if white_short_castle_through_check_check == True:

                white_short_castle_through_check_check = False

                if move not in self.legal_moves:

                    if "O-O" in self.legal_moves:

                        self.legal_moves.remove("O-O")

            elif white_long_castle_through_check_check == True:

                white_long_castle_through_check_check = False

                if move not in self.legal_moves:

                    if "O-O-O" in self.legal_moves:

                        self.legal_moves.remove("O-O-O")

            elif black_short_castle_through_check_check == True:

                black_short_castle_through_check_check = False

                if move not in self.legal_moves:

                    if "O-O" in self.legal_moves:

                        self.legal_moves.remove("O-O")

            elif black_long_castle_through_check_check == True:

                black_long_castle_through_check_check = False

                if move not in self.legal_moves:

                    if "O-O-O" in self.legal_moves:

                        self.legal_moves.remove("O-O-O")

        #print(self.legal_moves)

    def convert_to_easy_notation(self, notation_val):

        take = False

        if notation_val[-1] == "+":

            notation_val = notation_val.replace("+", "")

        for character in notation_val:

            if character == "x":

                take = True
                notation_val = notation_val.replace("x", "")

        return notation_val, take

    def move_piece(self, notation_val, take):

        self.en_passant_x_y = [8, 8]
        self.half_moves += 1

        if startup.white_turn == False:

            self.turn_num += 1

        if notation_val[0] == "B":

            from_x = notation.get_column_char(notation_val[1])
            from_y = int(notation_val[2]) - 1

            to_x = notation.get_column_char(notation_val[3])
            to_y = int(notation_val[4]) - 1

            if startup.white_turn == True:

                for i in range(0, 10):

                    if self.white_bishops_inf[i][2] == True and self.white_bishops_inf[i][0] == from_x and self.white_bishops_inf[i][1] == from_y:

                        self.white_bishops_inf[i][0] = to_x
                        self.white_bishops_inf[i][1] = to_y

            else:

                for i in range(0, 10):

                    if self.black_bishops_inf[i][2] == True and self.black_bishops_inf[i][0] == from_x and self.black_bishops_inf[i][1] == from_y:

                        self.black_bishops_inf[i][0] = to_x
                        self.black_bishops_inf[i][1] = to_y

        elif notation_val[0] == "N":

            from_x = notation.get_column_char(notation_val[1])
            from_y = int(notation_val[2]) - 1

            to_x = notation.get_column_char(notation_val[3])
            to_y = int(notation_val[4]) - 1

            if startup.white_turn == True:

                for i in range(0, 10):

                    if self.white_knights_inf[i][2] == True and self.white_knights_inf[i][0] == from_x and self.white_knights_inf[i][1] == from_y:

                        self.white_knights_inf[i][0] = to_x
                        self.white_knights_inf[i][1] = to_y

            else:

                for i in range(0, 10):

                    if self.black_knights_inf[i][2] == True and self.black_knights_inf[i][0] == from_x and self.black_knights_inf[i][1] == from_y:

                        self.black_knights_inf[i][0] = to_x
                        self.black_knights_inf[i][1] = to_y

        elif notation_val[0] == "R":

            from_x = notation.get_column_char(notation_val[1])
            from_y = int(notation_val[2]) - 1

            to_x = notation.get_column_char(notation_val[3])
            to_y = int(notation_val[4]) - 1

            if startup.white_turn == True:

                for i in range(0, 10):

                    if self.white_rooks_inf[i][2] == True and self.white_rooks_inf[i][0] == from_x and self.white_rooks_inf[i][1] == from_y:

                        self.white_rooks_inf[i][0] = to_x
                        self.white_rooks_inf[i][1] = to_y
                        self.white_rooks_inf[i][5] = False

            else:

                for i in range(0, 10):

                    if self.black_rooks_inf[i][2] == True and self.black_rooks_inf[i][0] == from_x and self.black_rooks_inf[i][1] == from_y:

                        self.black_rooks_inf[i][0] = to_x
                        self.black_rooks_inf[i][1] = to_y
                        self.black_rooks_inf[i][5] = False

        elif notation_val[0] == "Q":

            from_x = notation.get_column_char(notation_val[1])
            from_y = int(notation_val[2]) - 1

            to_x = notation.get_column_char(notation_val[3])
            to_y = int(notation_val[4]) - 1

            if startup.white_turn == True:

                for i in range(0, 9):

                    if self.white_queens_inf[i][2] == True and self.white_queens_inf[i][0] == from_x and self.white_queens_inf[i][1] == from_y:

                        self.white_queens_inf[i][0] = to_x
                        self.white_queens_inf[i][1] = to_y

            else:

                for i in range(0, 9):

                    if self.black_queens_inf[i][2] == True and self.black_queens_inf[i][0] == from_x and self.black_queens_inf[i][1] == from_y:

                        self.black_queens_inf[i][0] = to_x
                        self.black_queens_inf[i][1] = to_y

        elif notation_val[0] == "K":

            from_x = notation.get_column_char(notation_val[1])
            from_y = int(notation_val[2]) - 1

            to_x = notation.get_column_char(notation_val[3])
            to_y = int(notation_val[4]) - 1

            if startup.white_turn == True:

                if self.white_king_inf[0][2] == True and self.white_king_inf[0][0] == from_x and self.white_king_inf[0][1] == from_y:

                    self.white_king_inf[0][0] = to_x
                    self.white_king_inf[0][1] = to_y
                    self.white_king_inf[0][5] = False

            else:

                if self.black_king_inf[0][2] == True and self.black_king_inf[0][0] == from_x and self.black_king_inf[0][1] == from_y:

                    self.black_king_inf[0][0] = to_x
                    self.black_king_inf[0][1] = to_y
                    self.black_king_inf[0][5] = False

        elif notation_val[0] == "O":

            if startup.white_turn == True:

                self.white_king_inf[0][5] = False

                if notation_val == "O-O":

                    self.white_rooks_inf[1][5] = False

                    self.white_king_inf[0][0] = 6
                    self.white_king_inf[0][1] = 0

                    for i in range(0, 2):

                        if self.white_rooks_inf[i][0] == 7:

                            self.white_rooks_inf[i][0] = 5
                            self.white_rooks_inf[i][1] = 0

                elif notation_val == "O-O-O":

                    self.white_rooks_inf[0][5] = False

                    self.white_king_inf[0][0] = 2
                    self.white_king_inf[0][1] = 0

                    for i in range(0, 2):

                        if self.white_rooks_inf[i][0] == 0:

                            self.white_rooks_inf[i][0] = 3
                            self.white_rooks_inf[i][1] = 0

            else:

                self.black_king_inf[0][5] = False

                if notation_val == "O-O":

                    self.black_rooks_inf[1][5] = False

                    self.black_king_inf[0][0] = 6
                    self.black_king_inf[0][1] = 7

                    for i in range(0, 2):

                        if self.black_rooks_inf[i][0] == 7:

                            self.black_rooks_inf[i][0] = 5
                            self.black_rooks_inf[i][1] = 7

                elif notation_val == "O-O-O":

                    self.black_rooks_inf[0][5] = False

                    self.black_king_inf[0][0] = 2
                    self.black_king_inf[0][1] = 7

                    for i in range(0, 2):

                        if self.black_rooks_inf[i][0] == 0:

                            self.black_rooks_inf[i][0] = 3
                            self.black_rooks_inf[i][1] = 7

        else:

            self.half_moves = 0

            repetition_draw_file_write = open("repetition_draw_file.txt", "w")
            repetition_draw_file_write.write("")
            repetition_draw_file_write.close()

            if notation_val[-2] == "=":

                to_x = notation.get_column_char(notation_val[-4])
                to_y = int(notation_val[-3]) - 1

            else:

                to_x = notation.get_column_char(notation_val[-2])
                to_y = int(notation_val[-1]) - 1

            if take == True:

                if notation_val[-2] == "=":

                    from_x = notation.get_column_char(notation_val[-5])

                else:

                    from_x = notation.get_column_char(notation_val[-3])

                if startup.white_turn == True:

                    from_y = to_y - 1

                else:

                    from_y = to_y + 1
            else:

                from_x = to_x

                if startup.white_turn == True:

                    if to_y == 3:

                        from_y = to_y - 2

                        for i in range(0, 8):

                            if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][0] == from_x and self.white_pawns_inf[i][1] == to_y - 1:

                                from_y = to_y - 1

                    else:

                        from_y = to_y - 1

                else:

                    if to_y == 4:

                        from_y = to_y + 2

                        for i in range(0, 8):

                            if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][0] == from_x and self.black_pawns_inf[i][1] == to_y + 1:

                                from_y = to_y + 1

                    else:

                        from_y = to_y + 1

            if startup.white_turn == True:

                for i in range(0, 8):

                    if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][0] == from_x and self.white_pawns_inf[i][1] == from_y:

                        if to_y == 7:

                            self.white_pawns_inf[i][2] = False

                            if notation_val[-1] == "Q":

                                promotion_complete = False

                                for i in range(1, 9):

                                    if self.white_queens_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.white_queens_inf[i][0] = to_x
                                        self.white_queens_inf[i][1] = to_y
                                        self.white_queens_inf[i][2] = True

                            elif notation_val[-1] == "R":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.white_rooks_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.white_rooks_inf[i][0] = to_x
                                        self.white_rooks_inf[i][1] = to_y
                                        self.white_rooks_inf[i][2] = True
                                        self.white_rooks_inf[i][5] = False

                            elif notation_val[-1] == "B":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.white_bishops_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.white_bishops_inf[i][0] = to_x
                                        self.white_bishops_inf[i][1] = to_y
                                        self.white_bishops_inf[i][2] = True

                            elif notation_val[-1] == "N":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.white_knights_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.white_knights_inf[i][0] = to_x
                                        self.white_knights_inf[i][1] = to_y
                                        self.white_knights_inf[i][2] = True

                        else:

                            self.white_pawns_inf[i][0] = to_x
                            self.white_pawns_inf[i][1] = to_y
                            self.white_pawns_inf[i][5] = False

                            if to_y - from_y == 2:

                                self.en_passant_x_y = [to_x, to_y]

            else:

                for i in range(0, 8):

                    if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][0] == from_x and self.black_pawns_inf[i][1] == from_y:

                        if to_y == 0:

                            self.black_pawns_inf[i][2] = False

                            if notation_val[-1] == "Q":

                                promotion_complete = False

                                for i in range(1, 9):

                                    if self.black_queens_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.black_queens_inf[i][0] = to_x
                                        self.black_queens_inf[i][1] = to_y
                                        self.black_queens_inf[i][2] = True

                            elif notation_val[-1] == "R":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.black_rooks_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.black_rooks_inf[i][0] = to_x
                                        self.black_rooks_inf[i][1] = to_y
                                        self.black_rooks_inf[i][2] = True
                                        self.black_rooks_inf[i][5] = False

                            elif notation_val[-1] == "B":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.black_bishops_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.black_bishops_inf[i][0] = to_x
                                        self.black_bishops_inf[i][1] = to_y
                                        self.black_bishops_inf[i][2] = True

                            elif notation_val[-1] == "N":

                                promotion_complete = False

                                for i in range(2, 10):

                                    if self.black_knights_inf[i][2] == False and promotion_complete == False:

                                        promotion_complete = True

                                        self.black_knights_inf[i][0] = to_x
                                        self.black_knights_inf[i][1] = to_y
                                        self.black_knights_inf[i][2] = True

                        else:

                            self.black_pawns_inf[i][0] = to_x
                            self.black_pawns_inf[i][1] = to_y
                            self.black_pawns_inf[i][5] = False

                            if from_y - to_y == 2:

                                self.en_passant_x_y = [to_x, to_y]

        if take == True:

            self.half_moves = 0

            repetition_draw_file_write = open("repetition_draw_file.txt", "w")
            repetition_draw_file_write.write("")
            repetition_draw_file_write.close()

            peice_taken = False

            if startup.white_turn == True:

                for i in range(0, 8):

                    if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][0] == to_x and self.black_pawns_inf[i][1] == to_y:

                        self.black_pawns_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.black_bishops_inf[i][2] == True and self.black_bishops_inf[i][0] == to_x and self.black_bishops_inf[i][1] == to_y:

                        self.black_bishops_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.black_knights_inf[i][2] == True and self.black_knights_inf[i][0] == to_x and self.black_knights_inf[i][1] == to_y:

                        self.black_knights_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.black_rooks_inf[i][2] == True and self.black_rooks_inf[i][0] == to_x and self.black_rooks_inf[i][1] == to_y:

                        self.black_rooks_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 9):

                    if self.black_queens_inf[i][2] == True and self.black_queens_inf[i][0] == to_x and self.black_queens_inf[i][1] == to_y:

                        self.black_queens_inf[i][2] = False

                        peice_taken = True

                if peice_taken == False:

                    for i in range(0, 8):

                        if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][0] == to_x and self.black_pawns_inf[i][1] == to_y - 1:

                            self.black_pawns_inf[i][2] = False

            else:

                for i in range(0, 8):

                    if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][0] == to_x and self.white_pawns_inf[i][1] == to_y:

                        self.white_pawns_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.white_bishops_inf[i][2] == True and self.white_bishops_inf[i][0] == to_x and self.white_bishops_inf[i][1] == to_y:

                        self.white_bishops_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.white_knights_inf[i][2] == True and self.white_knights_inf[i][0] == to_x and self.white_knights_inf[i][1] == to_y:

                        self.white_knights_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 10):

                    if self.white_rooks_inf[i][2] == True and self.white_rooks_inf[i][0] == to_x and self.white_rooks_inf[i][1] == to_y:

                        self.white_rooks_inf[i][2] = False

                        peice_taken = True

                for i in range(0, 9):

                    if self.white_queens_inf[i][2] == True and self.white_queens_inf[i][0] == to_x and self.white_queens_inf[i][1] == to_y:

                        self.white_queens_inf[i][2] = False

                        peice_taken = True

                if peice_taken == False:

                    for i in range(0, 8):

                        if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][0] == to_x and self.white_pawns_inf[i][1] == to_y + 1:

                            self.white_pawns_inf[i][2] = False

    def stale_check_mate(self):

        checkmate = False

        if startup.white_turn == True:

            for i in range(0, 8):

                if checkmate == False and self.white_king_inf[0][0] + 1 == self.black_pawns_inf[i][0] and self.white_king_inf[0][1] + 1 == self.black_pawns_inf[i][1] and self.black_pawns_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] - 1 == self.black_pawns_inf[i][0] and self.white_king_inf[0][1] + 1 == self.black_pawns_inf[i][1] and self.black_pawns_inf[i][2] == True:

                    checkmate = True

            for i in range(0, 10):

                if checkmate == False and self.white_king_inf[0][0] + 1 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] + 2 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] + 2 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] + 1 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] + 2 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] - 1 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] + 1 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] - 2 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] - 1 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] - 2 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] - 2 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] - 1 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] - 2 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] + 1 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.white_king_inf[0][0] - 1 == self.black_knights_inf[i][0] and self.white_king_inf[0][1] + 2 == self.black_knights_inf[i][1] and self.black_knights_inf[i][2] == True:

                    checkmate = True

            for i in range(0, 10):

                remove = True

                if checkmate == False and self.black_bishops_inf[i][2] == True and abs(self.black_bishops_inf[i][0] - self.white_king_inf[0][0]) == abs(self.black_bishops_inf[i][1] - self.white_king_inf[0][1]):

                    if self.black_bishops_inf[i][0] > self.white_king_inf[0][0]:

                        if self.black_bishops_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_bishops_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_bishops_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                    else:

                        if self.black_bishops_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_bishops_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_bishops_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                    if remove == True:

                        checkmate = True

            for i in range(0, 10):

                remove = True

                if checkmate == False and self.black_rooks_inf[i][2] == True:

                    if self.black_rooks_inf[i][0] == self.white_king_inf[0][0]:

                        if self.black_rooks_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_rooks_inf[i][1] - self.white_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_rooks_inf[i][1] - self.white_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                        if remove == True:

                            checkmate = True

                    elif self.black_rooks_inf[i][1] == self.white_king_inf[0][1]:

                        if self.black_rooks_inf[i][0] > self.white_king_inf[0][0]:

                            for j in range(1, abs(self.black_rooks_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_rooks_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                        if remove == True:

                            checkmate = True

            for i in range(0, 9):

                remove = True

                if checkmate == False and self.black_queens_inf[i][2] == True and abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0]) == abs(self.black_queens_inf[i][1] - self.white_king_inf[0][1]):

                    if self.black_queens_inf[i][0] > self.white_king_inf[0][0]:

                        if self.black_queens_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                    else:

                        if self.black_queens_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                    if remove == True:

                        checkmate = True

                remove = True

                if checkmate == False and self.black_queens_inf[i][2] == True:

                    if self.black_queens_inf[i][0] == self.white_king_inf[0][0]:

                        if self.black_queens_inf[i][1] > self.white_king_inf[0][1]:

                            for j in range(1, abs(self.black_queens_inf[i][1] - self.white_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] and self.white_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] and self.black_occupation_y[k] == self.white_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_queens_inf[i][1] - self.white_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] and self.white_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] and self.black_occupation_y[k] == self.white_king_inf[0][1] - j:

                                        remove = False

                        if remove == True:

                            checkmate = True

                    elif self.black_queens_inf[i][1] == self.white_king_inf[0][1]:

                        if self.black_queens_inf[i][0] > self.white_king_inf[0][0]:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] + j and self.white_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] + j and self.black_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                        else:

                            for j in range(1, abs(self.black_queens_inf[i][0] - self.white_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.white_king_inf[0][0] - j and self.white_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.white_king_inf[0][0] - j and self.black_occupation_y[k] == self.white_king_inf[0][1]:

                                        remove = False

                        if remove == True:

                            checkmate = True

        else:

            for i in range(0, 8):

                if checkmate == False and self.black_king_inf[0][0] + 1 == self.white_pawns_inf[i][0] and self.black_king_inf[0][1] - 1 == self.white_pawns_inf[i][1] and self.white_pawns_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] - 1 == self.white_pawns_inf[i][0] and self.black_king_inf[0][1] - 1 == self.white_pawns_inf[i][1] and self.white_pawns_inf[i][2] == True:

                    checkmate = True

            for i in range(0, 10):

                if checkmate == False and self.black_king_inf[0][0] + 1 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] + 2 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] + 2 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] + 1 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] + 2 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] - 1 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] + 1 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] - 2 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] - 1 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] - 2 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] - 2 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] - 1 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] - 2 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] + 1 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

                elif checkmate == False and self.black_king_inf[0][0] - 1 == self.white_knights_inf[i][0] and self.black_king_inf[0][1] + 2 == self.white_knights_inf[i][1] and self.white_knights_inf[i][2] == True:

                    checkmate = True

            for i in range(0, 10):

                remove = True

                if checkmate == False and self.white_bishops_inf[i][2] == True and abs(self.white_bishops_inf[i][0] - self.black_king_inf[0][0]) == abs(self.white_bishops_inf[i][1] - self.black_king_inf[0][1]):

                    if self.white_bishops_inf[i][0] > self.black_king_inf[0][0]:

                        if self.white_bishops_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_bishops_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_bishops_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                    else:

                        if self.white_bishops_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_bishops_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_bishops_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                    if remove == True:

                        checkmate = True

            for i in range(0, 10):

                remove = True

                if checkmate == False and self.white_rooks_inf[i][2] == True:

                    if self.white_rooks_inf[i][0] == self.black_king_inf[0][0]:

                        if self.white_rooks_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_rooks_inf[i][1] - self.black_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_rooks_inf[i][1] - self.black_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                        if remove == True:

                            checkmate = True

                    elif self.white_rooks_inf[i][1] == self.black_king_inf[0][1]:

                        if self.white_rooks_inf[i][0] > self.black_king_inf[0][0]:

                            for j in range(1, abs(self.white_rooks_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_rooks_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                        if remove == True:

                            checkmate = True

            for i in range(0, 9):

                remove = True

                if checkmate == False and self.white_queens_inf[i][2] == True and abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0]) == abs(self.white_queens_inf[i][1] - self.black_king_inf[0][1]):

                    if self.white_queens_inf[i][0] > self.black_king_inf[0][0]:

                        if self.white_queens_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                    else:

                        if self.white_queens_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                    if remove == True:

                        checkmate = True

                remove = True

                if checkmate == False and self.white_queens_inf[i][2] == True:

                    if self.white_queens_inf[i][0] == self.black_king_inf[0][0]:

                        if self.white_queens_inf[i][1] > self.black_king_inf[0][1]:

                            for j in range(1, abs(self.white_queens_inf[i][1] - self.black_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] and self.white_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] and self.black_occupation_y[k] == self.black_king_inf[0][1] + j:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_queens_inf[i][1] - self.black_king_inf[0][1])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] and self.white_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] and self.black_occupation_y[k] == self.black_king_inf[0][1] - j:

                                        remove = False

                        if remove == True:

                            checkmate = True

                    elif self.white_queens_inf[i][1] == self.black_king_inf[0][1]:

                        if self.white_queens_inf[i][0] > self.black_king_inf[0][0]:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] + j and self.white_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] + j and self.black_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                        else:

                            for j in range(1, abs(self.white_queens_inf[i][0] - self.black_king_inf[0][0])):

                                for k in range(0, len(self.white_occupation_x)):

                                    if self.white_occupation_x[k] == self.black_king_inf[0][0] - j and self.white_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                                for k in range(0, len(self.black_occupation_x)):

                                    if self.black_occupation_x[k] == self.black_king_inf[0][0] - j and self.black_occupation_y[k] == self.black_king_inf[0][1]:

                                        remove = False

                        if remove == True:

                            checkmate = True

        return checkmate

    def convert_pieces_to_matrix(self):

        self.piece_value_matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]]

        if startup.playing_as_white == True:

            for i in range(0, 8):

                if self.white_pawns_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_pawns_inf[i][1]][self.white_pawns_inf[i][0]] = 1

            for i in range(0, 10):

                if self.white_bishops_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_bishops_inf[i][1]][self.white_bishops_inf[i][0]] = 3

            for i in range(0, 10):

                if self.white_knights_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_knights_inf[i][1]][self.white_knights_inf[i][0]] = 3

            for i in range(0, 10):

                if self.white_rooks_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_rooks_inf[i][1]][self.white_rooks_inf[i][0]] = 5

            for i in range(0, 9):

                if self.white_queens_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_queens_inf[i][1]][self.white_queens_inf[i][0]] = 9

            if self.white_king_inf[0][2] == True:

                self.piece_value_matrix[7 - self.white_king_inf[0][1]][self.white_king_inf[0][0]] = 100

            for i in range(0, 8):

                if self.black_pawns_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_pawns_inf[i][1]][self.black_pawns_inf[i][0]] = -1

            for i in range(0, 10):

                if self.black_bishops_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_bishops_inf[i][1]][self.black_bishops_inf[i][0]] = -3

            for i in range(0, 10):

                if self.black_knights_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_knights_inf[i][1]][self.black_knights_inf[i][0]] = -3

            for i in range(0, 10):

                if self.black_rooks_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_rooks_inf[i][1]][self.black_rooks_inf[i][0]] = -5

            for i in range(0, 9):

                if self.black_queens_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_queens_inf[i][1]][self.black_queens_inf[i][0]] = -9

            if self.black_king_inf[0][2] == True:

                self.piece_value_matrix[7 - self.black_king_inf[0][1]][self.black_king_inf[0][0]] = -100

        else:

            for i in range(0, 8):

                if self.white_pawns_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_pawns_inf[i][1]][self.white_pawns_inf[i][0]] = -1

            for i in range(0, 10):

                if self.white_bishops_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_bishops_inf[i][1]][self.white_bishops_inf[i][0]] = -3

            for i in range(0, 10):

                if self.white_knights_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_knights_inf[i][1]][self.white_knights_inf[i][0]] = -3

            for i in range(0, 10):

                if self.white_rooks_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_rooks_inf[i][1]][self.white_rooks_inf[i][0]] = -5

            for i in range(0, 9):

                if self.white_queens_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.white_queens_inf[i][1]][self.white_queens_inf[i][0]] = -9

            if self.white_king_inf[0][2] == True:

                self.piece_value_matrix[7 - self.white_king_inf[0][1]][self.white_king_inf[0][0]] = -100

            for i in range(0, 8):

                if self.black_pawns_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_pawns_inf[i][1]][self.black_pawns_inf[i][0]] = 1

            for i in range(0, 10):

                if self.black_bishops_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_bishops_inf[i][1]][self.black_bishops_inf[i][0]] = 3

            for i in range(0, 10):

                if self.black_knights_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_knights_inf[i][1]][self.black_knights_inf[i][0]] = 3

            for i in range(0, 10):

                if self.black_rooks_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_rooks_inf[i][1]][self.black_rooks_inf[i][0]] = 5

            for i in range(0, 9):

                if self.black_queens_inf[i][2] == True:

                    self.piece_value_matrix[7 - self.black_queens_inf[i][1]][self.black_queens_inf[i][0]] = 9

            if self.black_king_inf[0][2] == True:

                self.piece_value_matrix[7 - self.black_king_inf[0][1]][self.black_king_inf[0][0]] = 100

        return self.piece_value_matrix

    def find_piece_name(self, x, y):

        found = False

        for i in range(0, 8):

            if self.white_pawns_inf[i][2] == True and self.white_pawns_inf[i][0] == x and self.white_pawns_inf[i][1] == y:

                found = True

                return "P"

        for i in range(0, 10):

            if self.white_bishops_inf[i][2] == True and self.white_bishops_inf[i][0] == x and self.white_bishops_inf[i][1] == y:

                found = True

                return "B"

        for i in range(0, 10):

            if self.white_knights_inf[i][2] == True and self.white_knights_inf[i][0] == x and self.white_knights_inf[i][1] == y:

                found = True

                return "N"

        for i in range(0, 10):

            if self.white_rooks_inf[i][2] == True and self.white_rooks_inf[i][0] == x and self.white_rooks_inf[i][1] == y:

                found = True

                return "R"

        for i in range(0, 9):

            if self.white_queens_inf[i][2] == True and self.white_queens_inf[i][0] == x and self.white_queens_inf[i][1] == y:

                found = True

                return "Q"

        if self.white_king_inf[0][2] == True and self.white_king_inf[0][0] == x and self.white_king_inf[0][1] == y:

            found = True

            return "K"

        for i in range(0, 8):

            if self.black_pawns_inf[i][2] == True and self.black_pawns_inf[i][0] == x and self.black_pawns_inf[i][1] == y:

                found = True

                return "P"

        for i in range(0, 10):

            if self.black_bishops_inf[i][2] == True and self.black_bishops_inf[i][0] == x and self.black_bishops_inf[i][1] == y:

                found = True

                return "B"

        for i in range(0, 10):

            if self.black_knights_inf[i][2] == True and self.black_knights_inf[i][0] == x and self.black_knights_inf[i][1] == y:

                found = True

                return "N"

        for i in range(0, 10):

            if self.black_rooks_inf[i][2] == True and self.black_rooks_inf[i][0] == x and self.black_rooks_inf[i][1] == y:

                found = True

                return "R"

        for i in range(0, 9):

            if self.black_queens_inf[i][2] == True and self.black_queens_inf[i][0] == x and self.black_queens_inf[i][1] == y:

                found = True

                return "Q"

        if self.black_king_inf[0][2] == True and self.black_king_inf[0][0] == x and self.black_king_inf[0][1] == y:

            found = True

            return "K"

        if found == False:

            return "none"

    def no_moves(self):

        check_mate = self.stale_check_mate()

        if check_mate == True:

            if startup.white_turn == True:

                print("Black wins by Checkmate!")

                if startup.save_game_data == True:

                    startup.game_save_winner = -1

            else:

                print("White wins by Checkmate!")

                if startup.save_game_data == True:

                    startup.game_save_winner = 1

        else:

            print("It's a draw by stalemate!")

            if startup.save_game_data == True:

                startup.game_save_winner = 0

    def check_draw_by_insufficient_material(self):

        keep_checking_for_draw = True

        white_minor_pieces_num = 0
        black_minor_pieces_num = 0

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.white_pawns_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.black_pawns_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 9):

                if self.white_queens_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 9):

                if self.black_queens_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 10):

                if self.white_rooks_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 10):

                if self.black_rooks_inf[i][2] == True:

                    keep_checking_for_draw = False

                    break

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.white_bishops_inf[i][2] == True:

                    white_minor_pieces_num += 1

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.black_bishops_inf[i][2] == True:

                    black_minor_pieces_num += 1

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.white_knights_inf[i][2] == True:

                    white_minor_pieces_num += 1

        if keep_checking_for_draw == True:

            for i in range(0, 8):

                if self.black_knights_inf[i][2] == True:

                    black_minor_pieces_num += 1

        if keep_checking_for_draw == True:

            if white_minor_pieces_num >= 2:

                keep_checking_for_draw = False

            if black_minor_pieces_num >= 2:

                keep_checking_for_draw = False

        if keep_checking_for_draw == True:

            if startup.save_game_data == True:

                startup.game_save_winner = 0

            startup.game_over = True

            return True

        else:

            return False

class Notation():

    def __init__(self):

        pass

    def get_notation(self, piece, from_x, from_y, to_x, to_y):

        notation_val = "error"

        capture = False

        if piece == "P":

            if to_y == 7 or to_y == 0:

                if to_x == from_x and (to_y == from_y + 1 or to_y == from_y - 1 or to_y == from_y + 2 or to_y == from_y - 2):

                    notation_val = self.get_column(to_x) + self.get_row(to_y) + "="

                elif (to_x == from_x + 1 or to_x == from_x - 1) and (to_y == from_y + 1 or to_y == from_y - 1):

                    notation_val = self.get_column(from_x) + "x" + self.get_column(to_x) + self.get_row(to_y) + "="

            else:

                if to_x == from_x and (to_y == from_y + 1 or to_y == from_y - 1 or to_y == from_y + 2 or to_y == from_y - 2):

                    notation_val = self.get_column(to_x) + self.get_row(to_y)

                elif (to_x == from_x + 1 or to_x == from_x - 1) and (to_y == from_y + 1 or to_y == from_y - 1):

                    notation_val = self.get_column(from_x) + "x" + self.get_column(to_x) + self.get_row(to_y)

        else:

            if startup.white_turn == True:

                for i in range(0, len(pieces.black_occupation_x)):

                    if to_x == pieces.black_occupation_x[i] and to_y == pieces.black_occupation_y[i]:

                        capture = True

            else:

                for i in range(0, len(pieces.white_occupation_x)):

                    if to_x == pieces.white_occupation_x[i] and to_y == pieces.white_occupation_y[i]:

                        capture = True

            if capture == True:

                notation_val = piece + self.get_column(from_x) + self.get_row(from_y) + "x" + self.get_column(to_x) + self.get_row(to_y)

            else:

                notation_val = piece + self.get_column(from_x) + self.get_row(from_y) + self.get_column(to_x) + self.get_row(to_y)

        return notation_val

    def get_column(self, x):

        if x == 0:

            return "a"

        elif x == 1:

            return "b"

        elif x == 2:

            return "c"

        elif x == 3:

            return "d"

        elif x == 4:

            return "e"

        elif x == 5:

            return "f"

        elif x == 6:

            return "g"

        elif x == 7:

            return "h"

    def get_column_char(self, x):

        if x == "a":

            return 0

        elif x == "b":

            return 1

        elif x == "c":

            return 2

        elif x == "d":

            return 3

        elif x == "e":

            return 4

        elif x == "f":

            return 5

        elif x == "g":

            return 6

        elif x == "h":

            return 7

    def get_row(self, y):

        for i in range(0, 8):

            if y == i:

                return str(i + 1)

        if y != 0 and y != 1 and y != 2 and y != 3 and y != 4 and y != 5 and y != 6 and y != 7:

            return "9"

    def create_fen_position(self):

        fen = "11111111/11111111/11111111/11111111/11111111/11111111/11111111/11111111 w KQkq - - -"

        pos = 83

        fen = fen[:pos] + str(pieces.turn_num) + fen[pos + 1:]

        pos = 81

        fen = fen[:pos] + str(pieces.half_moves) + fen[pos + 1:]

        if pieces.en_passant_x_y[0] != 8 and pieces.en_passant_x_y[1] != 8:

            pos = 79

            if startup.white_turn == True:

                fen = fen[:pos] + self.get_column(pieces.en_passant_x_y[0]) + self.get_row(pieces.en_passant_x_y[1] + 1) + fen[pos + 1:]

            else:

                fen = fen[:pos] + self.get_column(pieces.en_passant_x_y[0]) + self.get_row(pieces.en_passant_x_y[1] - 1) + fen[pos + 1:]

        if pieces.black_king_inf[0][5] == True:

            black_queenside_castling = False
            black_kingside_castling = False

            for i in range(0, 10):

                if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][5] == True and pieces.black_rooks_inf[i][0] == 0 and pieces.black_rooks_inf[i][1] == 7:

                    black_queenside_castling = True

                if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][5] == True and pieces.black_rooks_inf[i][0] == 7 and pieces.black_rooks_inf[i][1] == 7:

                    black_kingside_castling = True

            if black_queenside_castling == False:

                pos = 77

                fen = fen[:pos] + fen[pos + 1:]

            if black_kingside_castling == False:

                pos = 76

                fen = fen[:pos] + fen[pos + 1:]

        else:

            pos = 76

            fen = fen[:pos] + fen[pos + 2:]

        if pieces.white_king_inf[0][5] == True:

            white_queenside_castling = False
            white_kingside_castling = False

            for i in range(0, 10):

                if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][5] == True and pieces.white_rooks_inf[i][0] == 0 and pieces.white_rooks_inf[i][1] == 0:

                    white_queenside_castling = True

                if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][5] == True and pieces.white_rooks_inf[i][0] == 7 and pieces.white_rooks_inf[i][1] == 0:

                    white_kingside_castling = True

            if white_queenside_castling == False:

                pos = 75

                fen = fen[:pos] + fen[pos + 1:]

            if white_kingside_castling == False:

                pos = 74

                fen = fen[:pos] + fen[pos + 1:]

        else:

            pos = 74

            if fen[76] == " ":

                fen = fen[:pos] + "-" + fen[pos + 2:]

            else:

                fen = fen[:pos] + fen[pos + 2:]

        pos = 72

        if startup.white_turn == True:

            fen = fen[:pos] + "w" + fen[pos + 1:]

        else:

            fen = fen[:pos] + "b" + fen[pos + 1:]

        for i in range(0, 8):

            if pieces.white_pawns_inf[i][2] == True:

                pos = pieces.white_pawns_inf[i][0] + ((7 - pieces.white_pawns_inf[i][1]) * 9)

                fen = fen[:pos] + "P" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.white_bishops_inf[i][2] == True:

                pos = pieces.white_bishops_inf[i][0] + ((7 - pieces.white_bishops_inf[i][1]) * 9)

                fen = fen[:pos] + "B" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.white_knights_inf[i][2] == True:

                pos = pieces.white_knights_inf[i][0] + ((7 - pieces.white_knights_inf[i][1]) * 9)

                fen = fen[:pos] + "N" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.white_rooks_inf[i][2] == True:

                pos = pieces.white_rooks_inf[i][0] + ((7 - pieces.white_rooks_inf[i][1]) * 9)

                fen = fen[:pos] + "R" + fen[pos + 1:]

        for i in range(0, 9):

            if pieces.white_queens_inf[i][2] == True:

                pos = pieces.white_queens_inf[i][0] + ((7 - pieces.white_queens_inf[i][1]) * 9)

                fen = fen[:pos] + "Q" + fen[pos + 1:]

        if pieces.white_king_inf[0][2] == True:

            pos = pieces.white_king_inf[0][0] + ((7 - pieces.white_king_inf[0][1]) * 9)

            fen = fen[:pos] + "K" + fen[pos + 1:]

        for i in range(0, 8):

            if pieces.black_pawns_inf[i][2] == True:

                pos = pieces.black_pawns_inf[i][0] + ((7 - pieces.black_pawns_inf[i][1]) * 9)

                fen = fen[:pos] + "p" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.black_bishops_inf[i][2] == True:

                pos = pieces.black_bishops_inf[i][0] + ((7 - pieces.black_bishops_inf[i][1]) * 9)

                fen = fen[:pos] + "b" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.black_knights_inf[i][2] == True:

                pos = pieces.black_knights_inf[i][0] + ((7 - pieces.black_knights_inf[i][1]) * 9)

                fen = fen[:pos] + "n" + fen[pos + 1:]

        for i in range(0, 10):

            if pieces.black_rooks_inf[i][2] == True:

                pos = pieces.black_rooks_inf[i][0] + ((7 - pieces.black_rooks_inf[i][1]) * 9)

                fen = fen[:pos] + "r" + fen[pos + 1:]

        for i in range(0, 9):

            if pieces.black_queens_inf[i][2] == True:

                pos = pieces.black_queens_inf[i][0] + ((7 - pieces.black_queens_inf[i][1]) * 9)

                fen = fen[:pos] + "q" + fen[pos + 1:]

        if pieces.black_king_inf[0][2] == True:

            pos = pieces.black_king_inf[0][0] + ((7 - pieces.black_king_inf[0][1]) * 9)

            fen = fen[:pos] + "k" + fen[pos + 1:]

        pos = 0

        while fen[pos] != " ":

            if (fen[pos] == "1" or fen[pos] == "2" or fen[pos] == "3" or fen[pos] == "4" or fen[pos] == "5" or fen[pos] == "6" or fen[pos] == "7") and fen[pos + 1] == "1":

                fen = fen[:pos] + str(int(fen[pos]) + int(fen[pos + 1])) + fen[pos + 2:]

            else:

                pos += 1

        return fen

    def load_fen_position(self, fen):

        pieces.white_pawns_inf = [[0, 1, False, False], [1, 1, False, False], [2, 1, False, False], [3, 1, False, False], [4, 1, False, False], [5, 1, False, False], [6, 1, False, False], [7, 1, False, False]]
        pieces.white_bishops_inf = [[2, 0, False], [5, 0, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False]]
        pieces.white_knights_inf = [[1, 0, False], [6, 0, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False]]
        pieces.white_rooks_inf = [[0, 0, False, False], [7, 0, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False]]
        pieces.white_queens_inf = [[3, 0, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False]]
        pieces.white_king_inf = [[4, 0, False, False]]

        pieces.black_pawns_inf = [[0, 6, False, False], [1, 6, False, False], [2, 6, False, False], [3, 6, False, False], [4, 6, False, False], [5, 6, False, False], [6, 6, False, False], [7, 6, False, False]]
        pieces.black_bishops_inf = [[2, 7, False], [5, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False]]
        pieces.black_knights_inf = [[6, 7, False], [1, 7, False], [6, 3, False], [0, 3, False], [2, 0, False], [2, 6, False], [6, 2, False], [0, 2, False], [0, 7, False], [0, 7, False]]
        pieces.black_rooks_inf = [[0, 7, False, False], [7, 7, False, False], [2, 0, False, False], [4, 6, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False], [0, 7, False, False]]
        pieces.black_queens_inf = [[3, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False], [0, 7, False]]
        pieces.black_king_inf = [[4, 7, False, False]]

        fen_stage = 0
        x = 0
        y = 7

        half_move_chars = ""
        turn_num_chars = ""

        for char in fen:

            if char == " ":

                fen_stage += 1

            elif fen_stage == 0:

                if char == "/":

                    x = -1
                    y -= 1

                elif char.isnumeric():

                    x += int(char) - 1

                elif char == "P":

                    count = 0

                    while count <= 7:

                        if pieces.white_pawns_inf[count][2] == False:

                            pieces.white_pawns_inf[count][0] = x
                            pieces.white_pawns_inf[count][1] = y
                            pieces.white_pawns_inf[count][2] = True

                            if y == 1:

                                pieces.white_pawns_inf[count][5] = True

                            break

                        else:

                            count += 1

                elif char == "B":

                    count = 0

                    while count <= 9:

                        if pieces.white_bishops_inf[count][2] == False:

                            pieces.white_bishops_inf[count][0] = x
                            pieces.white_bishops_inf[count][1] = y
                            pieces.white_bishops_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "N":

                    count = 0

                    while count <= 9:

                        if pieces.white_knights_inf[count][2] == False:

                            pieces.white_knights_inf[count][0] = x
                            pieces.white_knights_inf[count][1] = y
                            pieces.white_knights_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "R":

                    count = 0

                    while count <= 9:

                        if pieces.white_rooks_inf[count][2] == False:

                            pieces.white_rooks_inf[count][0] = x
                            pieces.white_rooks_inf[count][1] = y
                            pieces.white_rooks_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "Q":

                    count = 0

                    while count <= 8:

                        if pieces.white_queens_inf[count][2] == False:

                            pieces.white_queens_inf[count][0] = x
                            pieces.white_queens_inf[count][1] = y
                            pieces.white_queens_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "K":

                    if pieces.white_king_inf[0][2] == False:

                        pieces.white_king_inf[0][0] = x
                        pieces.white_king_inf[0][1] = y
                        pieces.white_king_inf[0][2] = True

                elif char == "p":

                    count = 0

                    while count <= 7:

                        if pieces.black_pawns_inf[count][2] == False:

                            pieces.black_pawns_inf[count][0] = x
                            pieces.black_pawns_inf[count][1] = y
                            pieces.black_pawns_inf[count][2] = True

                            if y == 6:

                                pieces.black_pawns_inf[count][5] = True

                            break

                        else:

                            count += 1

                elif char == "b":

                    count = 0

                    while count <= 9:

                        if pieces.black_bishops_inf[count][2] == False:

                            pieces.black_bishops_inf[count][0] = x
                            pieces.black_bishops_inf[count][1] = y
                            pieces.black_bishops_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "n":

                    count = 0

                    while count <= 9:

                        if pieces.black_knights_inf[count][2] == False:

                            pieces.black_knights_inf[count][0] = x
                            pieces.black_knights_inf[count][1] = y
                            pieces.black_knights_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "r":

                    count = 0

                    while count <= 9:

                        if pieces.black_rooks_inf[count][2] == False:

                            pieces.black_rooks_inf[count][0] = x
                            pieces.black_rooks_inf[count][1] = y
                            pieces.black_rooks_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "q":

                    count = 0

                    while count <= 8:

                        if pieces.black_queens_inf[count][2] == False:

                            pieces.black_queens_inf[count][0] = x
                            pieces.black_queens_inf[count][1] = y
                            pieces.black_queens_inf[count][2] = True

                            break

                        else:

                            count += 1

                elif char == "k":

                    if pieces.black_king_inf[0][2] == False:

                        pieces.black_king_inf[0][0] = x
                        pieces.black_king_inf[0][1] = y
                        pieces.black_king_inf[0][2] = True

                x += 1

            elif fen_stage == 1:

                if char == "w":

                    startup.white_turn = True

                elif char == "b":

                    startup.white_turn = False

            elif fen_stage == 2:

                if char == "K":

                    pieces.white_king_inf[0][5] = True

                    for i in range(0, 10):

                        if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][0] == 7 and pieces.white_rooks_inf[i][1] == 0:

                            pieces.white_rooks_inf[i][5] = True

                elif char == "Q":

                    pieces.white_king_inf[0][5] = True

                    for i in range(0, 10):

                        if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][0] == 0 and pieces.white_rooks_inf[i][1] == 0:

                            pieces.white_rooks_inf[i][5] = True

                elif char == "k":

                    pieces.black_king_inf[0][5] = True

                    for i in range(0, 10):

                        if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][0] == 7 and pieces.black_rooks_inf[i][1] == 7:

                            pieces.black_rooks_inf[i][5] = True

                elif char == "q":

                    pieces.black_king_inf[0][5] = True

                    for i in range(0, 10):

                        if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][0] == 0 and pieces.black_rooks_inf[i][1] == 7:

                            pieces.black_rooks_inf[i][5] = True

            elif fen_stage == 3:

                if char.isnumeric():

                    if startup.white_turn == True:

                        pieces.en_passant_x_y[1] = int(char) - 2

                    else:

                        pieces.en_passant_x_y[1] = int(char)

                else:

                    pieces.en_passant_x_y[0] = self.get_column_char(char)

            elif fen_stage == 4:

                if char.isnumeric():

                    half_move_chars = half_move_chars + char

                    pieces.half_moves = int(half_move_chars)

            elif fen_stage == 5:

                if char.isnumeric():

                    turn_num_chars = turn_num_chars + char

                    pieces.turn_num = int(turn_num_chars)

    def save_notation_for_repetition(self):

        draw_by_repetition = False

        fen = self.create_fen_position()

        #print(fen)

        fen = fen[:fen.find(" ")]

        repetition_draw_file_append = open("repetition_draw_file.txt", "a")
        repetition_draw_file_append.write(fen + "\n")
        repetition_draw_file_append.close()

        repeat_num = 0

        repetition_draw_file_read = open("repetition_draw_file.txt", "r")

        for line in repetition_draw_file_read:

            if line == fen + "\n":

                repeat_num += 1

        repetition_draw_file_read.close()

        if repeat_num >= 3:

            draw_by_repetition = True

            if startup.save_game_data == True:

                startup.game_save_winner = 0

            startup.game_over = True

        return draw_by_repetition

class Start():

    def __init__(self):

        root = Tk()

        #width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight() * 0.9
        self.screen_height = math.trunc(self.screen_height) - (math.trunc(self.screen_height) % 8)

        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_height, self.screen_height))
        pygame.display.set_caption("Chess")

        self.tile_size = self.screen_height // 8

        self.run = True
        self.update = False
        self.update_display = True
        self.white_turn = True
        self.playing_as_white = True
        self.auto_rotate = False
        self.your_turn = True

        self.save_game_data = False

        self.auto_move = False
        self.one_player = False
        self.two_player = False

        self.move_choice = ""

        if not os.path.exists("repetition_draw_file.txt"):

            open("repetition_draw_file.txt", "a").close()

        else:

            repetition_draw_file_write = open("repetition_draw_file.txt", "w")
            repetition_draw_file_write.write("")
            repetition_draw_file_write.close()

        #self.event_handler_thread = threading.Thread(target = self.event_handler_func)
        self.player_customisations_thread = threading.Thread(target = self.player_customisations_func)
        self.outline_selected_piece_thread = threading.Thread(target = self.outline_selected_piece)
        self.piece_follow_mouse_thread = threading.Thread(target = self.piece_follow_mouse)
        self.auto_move_thread = threading.Thread(target = self.auto_move_func)
        self.one_player_thread = threading.Thread(target = self.one_player_func)
        self.two_player_thread = threading.Thread(target = self.two_player_func)
        self.play_again_thread = threading.Thread(target = self.play_again_func)

        #self.event_handler_thread_started = False
        self.player_customisations_thread_started = False
        self.outline_selected_piece_thread_started = False
        self.piece_follow_mouse_thread_started = False
        self.auto_move_thread_started = False
        self.one_player_thread_started = False
        self.two_player_thread_started = False
        self.play_again_thread_started = False

    def start(self):

        #self.event_handler_thread = threading.Thread(target = self.event_handler_func)
        #self.event_handler_thread.start()
        #self.event_handler_thread_started = True

        self.player_customisations_thread = threading.Thread(target = self.player_customisations_func)
        self.player_customisations_thread.start()
        self.player_customisations_thread_started = True

        self.outline_selected_piece_thread = threading.Thread(target = self.outline_selected_piece)
        self.outline_selected_piece_thread.start()
        self.outline_selected_piece_thread_started = True

        self.piece_follow_mouse_thread = threading.Thread(target = self.piece_follow_mouse)
        self.piece_follow_mouse_thread.start()
        self.piece_follow_mouse_thread_started = True

        while self.run:

            #if self.update_display:

            board.draw_board()

            if self.playing_as_white:

                pieces.draw_pieces_white()

            else:

                pieces.draw_pieces_black()

            pygame.display.update()

                #self.update_display = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    self.mouse_sprite_collisions_mouse_down(mouse_pos)

                if event.type == pygame.MOUSEBUTTONUP:

                    mouse_pos = pygame.mouse.get_pos()

                    self.sprite_released_mouse_up(mouse_pos)

            if self.update == True:

                self.update = False

                if self.save_game_data == True:

                    self.game_save_list = os.listdir(f"Data/Game{self.game_save_number+1}")
                    self.game_save_amount = len(self.game_save_list)

                if self.auto_move == True:

                    self.auto_move_thread = threading.Thread(target = self.auto_move_func)
                    self.auto_move_thread.start()
                    self.auto_move_thread_started = True

                elif self.one_player == True:

                    self.one_player_thread = threading.Thread(target = self.one_player_func)
                    self.one_player_thread.start()
                    self.one_player_thread_started = True

                elif self.two_player == True:

                    self.two_player_thread = threading.Thread(target = self.two_player_func)
                    self.two_player_thread.start()
                    self.two_player_thread_started = True

                else:

                    self.play_again_thread = threading.Thread(target = self.play_again_func)
                    self.play_again_thread.start()
                    self.play_again_thread_started = True

        #if self.event_handler_thread_started == True:

            #self.event_handler_thread.join()

        if self.player_customisations_thread_started == True:

            self.player_customisations_thread.join()

        if self.outline_selected_piece_thread_started == True:

            self.outline_selected_piece_thread.join()

        if self.piece_follow_mouse_thread_started == True:

            self.piece_follow_mouse_thread.join()

        if self.auto_move_thread_started == True:

            self.auto_move_thread.join()

        if self.one_player_thread_started == True:

            self.one_player_thread.join()

        if self.two_player_thread_started == True:

            self.two_player_thread.join()

        if self.play_again_thread_started == True:

            self.play_again_thread.join()

        pygame.quit()

    def event_handler_func(self):

        while self.run:

            #for event in pygame.event.get():

                #if event.type == pygame.QUIT:

                    #self.run = False

            pass

                #if event.type ==

    def mouse_sprite_collisions_mouse_down(self, mouse_pos):

        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]

        if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

            if pieces.promotion_strip_inf[2] == True:

                pieces.promotion_strip_inf[2] = False

                if pieces.promotion_strip_inf[1] == 7:

                    if self.playing_as_white:

                        if mouse_pos_x >= pieces.promotion_strip_inf[0] * self.tile_size and mouse_pos_x <= (pieces.promotion_strip_inf[0] + 1) * self.tile_size and mouse_pos_y >= 0 * self.tile_size and mouse_pos_y <= 1 * self.tile_size:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=Q"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=Q"

                        elif mouse_pos_x >= pieces.promotion_strip_inf[0] * self.tile_size and mouse_pos_x <= ((pieces.promotion_strip_inf[0] + 0.5) * self.tile_size) // 1 and mouse_pos_y >= 1 * self.tile_size and mouse_pos_y <= (1.5 * self.tile_size) // 1:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=R"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=R"

                        elif mouse_pos_x >= ((pieces.promotion_strip_inf[0] + 0.5) * self.tile_size) // 1 and mouse_pos_x <= (pieces.promotion_strip_inf[0] + 1) * self.tile_size and mouse_pos_y >= 1 * self.tile_size and mouse_pos_y <= (1.5 * self.tile_size) // 1:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=B"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=B"

                        elif mouse_pos_x >= ((pieces.promotion_strip_inf[0] + 0.25) * self.tile_size) // 1 and mouse_pos_x <= ((pieces.promotion_strip_inf[0] + 0.75) * self.tile_size) // 1 and mouse_pos_y >= (1.5 * self.tile_size) // 1 and mouse_pos_y <= 2 * self.tile_size:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=N"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=N"

                    else:

                        if mouse_pos_x >= (7 - pieces.promotion_strip_inf[0]) * self.tile_size and mouse_pos_x <= ((7 - pieces.promotion_strip_inf[0]) + 1) * self.tile_size and mouse_pos_y >= 7 * self.tile_size and mouse_pos_y <= 8 * self.tile_size:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=Q"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=Q"

                        elif mouse_pos_x >= (7 - pieces.promotion_strip_inf[0]) * self.tile_size and mouse_pos_x <= (((7 - pieces.promotion_strip_inf[0]) + 0.5) * self.tile_size) // 1 and mouse_pos_y >= (6.5 * self.tile_size) // 1 and mouse_pos_y <= 7 * self.tile_size:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=R"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=R"

                        elif mouse_pos_x >= (((7 - pieces.promotion_strip_inf[0]) + 0.5) * self.tile_size) // 1 and mouse_pos_x <= ((7 - pieces.promotion_strip_inf[0]) + 1) * self.tile_size and mouse_pos_y >= (6.5 * self.tile_size) // 1 and mouse_pos_y <= 7 * self.tile_size:

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=B"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=B"

                        elif mouse_pos_x >= (((7 - pieces.promotion_strip_inf[0]) + 0.25) * self.tile_size) // 1 and mouse_pos_x <= (((7 - pieces.promotion_strip_inf[0]) + 0.75) * self.tile_size) // 1 and mouse_pos_y >= 6 * self.tile_size and mouse_pos_y <= (6.5 * self.tile_size) // 1 :

                            pawn_x_pos = pieces.white_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=N"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(7) + "=N"

                elif pieces.promotion_strip_inf[1] == 0:

                    if self.playing_as_white:

                        if mouse_pos_x >= pieces.promotion_strip_inf[0] * self.tile_size and mouse_pos_x <= (pieces.promotion_strip_inf[0] + 1) * self.tile_size and mouse_pos_y >= 7 * self.tile_size and mouse_pos_y <= 8 * self.tile_size:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=Q"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=Q"

                        elif mouse_pos_x >= pieces.promotion_strip_inf[0] * self.tile_size and mouse_pos_x <= ((pieces.promotion_strip_inf[0] + 0.5) * self.tile_size) // 1 and mouse_pos_y >= (6.5 * self.tile_size) // 1 and mouse_pos_y <= 7 * self.tile_size:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=R"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=R"

                        elif mouse_pos_x >= ((pieces.promotion_strip_inf[0] + 0.5) * self.tile_size) // 1 and mouse_pos_x <= (pieces.promotion_strip_inf[0] + 1) * self.tile_size and mouse_pos_y >= (6.5 * self.tile_size) // 1 and mouse_pos_y <= 7 * self.tile_size:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=B"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=B"

                        elif mouse_pos_x >= ((pieces.promotion_strip_inf[0] + 0.25) * self.tile_size) // 1 and mouse_pos_x <= ((pieces.promotion_strip_inf[0] + 0.75) * self.tile_size) // 1 and mouse_pos_y >= 6 * self.tile_size and mouse_pos_y <= (6.5 * self.tile_size) // 1 :

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=N"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=N"

                    else:

                        if mouse_pos_x >= (7 - pieces.promotion_strip_inf[0]) * self.tile_size and mouse_pos_x <= ((7 - pieces.promotion_strip_inf[0]) + 1) * self.tile_size and mouse_pos_y >= 0 * self.tile_size and mouse_pos_y <= 1 * self.tile_size:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=Q"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=Q"

                        elif mouse_pos_x >= (7 - pieces.promotion_strip_inf[0]) * self.tile_size and mouse_pos_x <= (((7 - pieces.promotion_strip_inf[0]) + 0.5) * self.tile_size) // 1 and mouse_pos_y >= 1 * self.tile_size and mouse_pos_y <= (1.5 * self.tile_size) // 1:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=R"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=R"

                        elif mouse_pos_x >= (((7 - pieces.promotion_strip_inf[0]) + 0.5) * self.tile_size) // 1 and mouse_pos_x <= ((7 - pieces.promotion_strip_inf[0]) + 1) * self.tile_size and mouse_pos_y >= 1 * self.tile_size and mouse_pos_y <= (1.5 * self.tile_size) // 1:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=B"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=B"

                        elif mouse_pos_x >= (((7 - pieces.promotion_strip_inf[0]) + 0.25) * self.tile_size) // 1 and mouse_pos_x <= (((7 - pieces.promotion_strip_inf[0]) + 0.75) * self.tile_size) // 1 and mouse_pos_y >= (1.5 * self.tile_size) // 1 and mouse_pos_y <= 2 * self.tile_size:

                            pawn_x_pos = pieces.black_pawns_inf[pieces.promotion_strip_inf[3]][0]

                            if pawn_x_pos == pieces.promotion_strip_inf[0]:

                                self.move_choice = notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=N"

                            else:

                                self.move_choice = notation.get_column(pawn_x_pos) + "x" + notation.get_column(pieces.promotion_strip_inf[0]) + notation.get_row(0) + "=N"

            if self.playing_as_white:

                tile_x = mouse_pos_x // self.tile_size
                tile_y = 7 - (mouse_pos_y // self.tile_size)

            else:

                tile_x = 7 - (mouse_pos_x // self.tile_size)
                tile_y = mouse_pos_y // self.tile_size

            for i in range(0, 8):

                if pieces.white_pawns_inf[i][2] == True and pieces.white_pawns_inf[i][0] == tile_x and pieces.white_pawns_inf[i][1] == tile_y:

                    pieces.white_pawns_inf[i][3] = True
                    pieces.white_pawns_inf[i][4] = True

                else:

                    pieces.white_pawns_inf[i][3] = False

            for i in range(0, 10):

                if pieces.white_bishops_inf[i][2] == True and pieces.white_bishops_inf[i][0] == tile_x and pieces.white_bishops_inf[i][1] == tile_y:

                    pieces.white_bishops_inf[i][3] = True
                    pieces.white_bishops_inf[i][4] = True

                else:

                    pieces.white_bishops_inf[i][3] = False

            for i in range(0, 10):

                if pieces.white_knights_inf[i][2] == True and pieces.white_knights_inf[i][0] == tile_x and pieces.white_knights_inf[i][1] == tile_y:

                    pieces.white_knights_inf[i][3] = True
                    pieces.white_knights_inf[i][4] = True

                else:

                    pieces.white_knights_inf[i][3] = False

            for i in range(0, 10):

                if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][0] == tile_x and pieces.white_rooks_inf[i][1] == tile_y:

                    pieces.white_rooks_inf[i][3] = True
                    pieces.white_rooks_inf[i][4] = True

                else:

                    pieces.white_rooks_inf[i][3] = False

            for i in range(0, 9):

                if pieces.white_queens_inf[i][2] == True and pieces.white_queens_inf[i][0] == tile_x and pieces.white_queens_inf[i][1] == tile_y:

                    pieces.white_queens_inf[i][3] = True
                    pieces.white_queens_inf[i][4] = True

                else:

                    pieces.white_queens_inf[i][3] = False

            if pieces.white_king_inf[0][2] == True and pieces.white_king_inf[0][0] == tile_x and pieces.white_king_inf[0][1] == tile_y:

                pieces.white_king_inf[0][3] = True
                pieces.white_king_inf[0][4] = True

            else:

                pieces.white_king_inf[0][3] = False

            for i in range(0, 8):

                if pieces.black_pawns_inf[i][2] == True and pieces.black_pawns_inf[i][0] == tile_x and pieces.black_pawns_inf[i][1] == tile_y:

                    pieces.black_pawns_inf[i][3] = True
                    pieces.black_pawns_inf[i][4] = True

                else:

                    pieces.black_pawns_inf[i][3] = False

            for i in range(0, 10):

                if pieces.black_bishops_inf[i][2] == True and pieces.black_bishops_inf[i][0] == tile_x and pieces.black_bishops_inf[i][1] == tile_y:

                    pieces.black_bishops_inf[i][3] = True
                    pieces.black_bishops_inf[i][4] = True

                else:

                    pieces.black_bishops_inf[i][3] = False

            for i in range(0, 10):

                if pieces.black_knights_inf[i][2] == True and pieces.black_knights_inf[i][0] == tile_x and pieces.black_knights_inf[i][1] == tile_y:

                    pieces.black_knights_inf[i][3] = True
                    pieces.black_knights_inf[i][4] = True

                else:

                    pieces.black_knights_inf[i][3] = False

            for i in range(0, 10):

                if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][0] == tile_x and pieces.black_rooks_inf[i][1] == tile_y:

                    pieces.black_rooks_inf[i][3] = True
                    pieces.black_rooks_inf[i][4] = True

                else:

                    pieces.black_rooks_inf[i][3] = False

            for i in range(0, 9):

                if pieces.black_queens_inf[i][2] == True and pieces.black_queens_inf[i][0] == tile_x and pieces.black_queens_inf[i][1] == tile_y:

                    pieces.black_queens_inf[i][3] = True
                    pieces.black_queens_inf[i][4] = True

                else:

                    pieces.black_queens_inf[i][3] = False

            if pieces.black_king_inf[0][2] == True and pieces.black_king_inf[0][0] == tile_x and pieces.black_king_inf[0][1] == tile_y:

                pieces.black_king_inf[0][3] = True
                pieces.black_king_inf[0][4] = True

            else:

                pieces.black_king_inf[0][3] = False

    def sprite_released_mouse_up(self, mouse_pos):

        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]

        if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

            if self.playing_as_white:

                tile_x = mouse_pos_x // self.tile_size
                tile_y = 7 - (mouse_pos_y // self.tile_size)

            else:

                tile_x = 7 - (mouse_pos_x // self.tile_size)
                tile_y = mouse_pos_y // self.tile_size

            for i in range(0, 8):

                if pieces.white_pawns_inf[i][4] == True:

                    pieces.white_pawns_inf[i][4] = False

            for i in range(0, 10):

                if pieces.white_bishops_inf[i][4] == True:

                    pieces.white_bishops_inf[i][4] = False

            for i in range(0, 10):

                if pieces.white_knights_inf[i][4] == True:

                    pieces.white_knights_inf[i][4] = False

            for i in range(0, 10):

                if pieces.white_rooks_inf[i][4] == True:

                    pieces.white_rooks_inf[i][4] = False

            for i in range(0, 9):

                if pieces.white_queens_inf[i][4] == True:

                    pieces.white_queens_inf[i][4] = False

            if pieces.white_king_inf[0][4] == True:

                pieces.white_king_inf[0][4] = False

            for i in range(0, 8):

                if pieces.black_pawns_inf[i][4] == True:

                    pieces.black_pawns_inf[i][4] = False

            for i in range(0, 10):

                if pieces.black_bishops_inf[i][4] == True:

                    pieces.black_bishops_inf[i][4] = False

            for i in range(0, 10):

                if pieces.black_knights_inf[i][4] == True:

                    pieces.black_knights_inf[i][4] = False

            for i in range(0, 10):

                if pieces.black_rooks_inf[i][4] == True:

                    pieces.black_rooks_inf[i][4] = False

            for i in range(0, 9):

                if pieces.black_queens_inf[i][4] == True:

                    pieces.black_queens_inf[i][4] = False

            if pieces.black_king_inf[0][4] == True:

                pieces.black_king_inf[0][4] = False

            if pieces.tile_outline_inf[2] == True and pieces.tile_outline_inf[3] == True and tile_x == pieces.tile_outline_inf[0] and tile_y == pieces.tile_outline_inf[1]:

                pieces.tile_outline_inf[2] = False
                pieces.tile_outline_inf[3] = False

        if pieces.tile_outline_inf[2] == True and pieces.tile_outline_inf[3] == False:

            pieces.tile_outline_inf[3] = True

    def outline_selected_piece(self):

        while self.run:

            for i in range(0, 8):

                if pieces.white_pawns_inf[i][2] == True and pieces.white_pawns_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.white_pawns_inf[i][0], pieces.white_pawns_inf[i][1])

                    while self.run and pieces.white_pawns_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.white_pawns_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.white_bishops_inf[i][2] == True and pieces.white_bishops_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.white_bishops_inf[i][0], pieces.white_bishops_inf[i][1])

                    while self.run and pieces.white_bishops_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.white_bishops_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.white_knights_inf[i][2] == True and pieces.white_knights_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.white_knights_inf[i][0], pieces.white_knights_inf[i][1])

                    while self.run and pieces.white_knights_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.white_knights_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.white_rooks_inf[i][0], pieces.white_rooks_inf[i][1])

                    while self.run and pieces.white_rooks_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.white_rooks_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 9):

                if pieces.white_queens_inf[i][2] == True and pieces.white_queens_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.white_queens_inf[i][0], pieces.white_queens_inf[i][1])

                    while self.run and pieces.white_queens_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.white_queens_inf[i][3] = False

                    self.redraw_board_without_outline()

            if pieces.white_king_inf[0][2] == True and pieces.white_king_inf[0][3] == True:

                self.redraw_board_for_outline(pieces.white_king_inf[0][0], pieces.white_king_inf[0][1])

                while self.run and pieces.white_king_inf[0][3] == True and pieces.tile_outline_inf[2] == True:

                    pass

                pieces.white_king_inf[0][3] = False

                self.redraw_board_without_outline()

            for i in range(0, 8):

                if pieces.black_pawns_inf[i][2] == True and pieces.black_pawns_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.black_pawns_inf[i][0], pieces.black_pawns_inf[i][1])

                    while self.run and pieces.black_pawns_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.black_pawns_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.black_bishops_inf[i][2] == True and pieces.black_bishops_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.black_bishops_inf[i][0], pieces.black_bishops_inf[i][1])

                    while self.run and pieces.black_bishops_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.black_bishops_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.black_knights_inf[i][2] == True and pieces.black_knights_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.black_knights_inf[i][0], pieces.black_knights_inf[i][1])

                    while self.run and pieces.black_knights_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.black_knights_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 10):

                if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.black_rooks_inf[i][0], pieces.black_rooks_inf[i][1])

                    while self.run and pieces.black_rooks_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.black_rooks_inf[i][3] = False

                    self.redraw_board_without_outline()

            for i in range(0, 9):

                if pieces.black_queens_inf[i][2] == True and pieces.black_queens_inf[i][3] == True:

                    self.redraw_board_for_outline(pieces.black_queens_inf[i][0], pieces.black_queens_inf[i][1])

                    while self.run and pieces.black_queens_inf[i][3] == True and pieces.tile_outline_inf[2] == True:

                        pass

                    pieces.black_queens_inf[i][3] = False

                    self.redraw_board_without_outline()

            if pieces.black_king_inf[0][2] == True and pieces.black_king_inf[0][3] == True:

                self.redraw_board_for_outline(pieces.black_king_inf[0][0], pieces.black_king_inf[0][1])

                while self.run and pieces.black_king_inf[0][3] == True and pieces.tile_outline_inf[2] == True:

                    pass

                pieces.black_king_inf[0][3] = False

                self.redraw_board_without_outline()

    def piece_follow_mouse(self):

        while self.run:

            pawn_placement = 0

            for i in range(0, 8):

                if pieces.white_pawns_inf[i][2] == True and pieces.white_pawns_inf[i][4] == True:

                    while self.run and pieces.white_pawns_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("P", pieces.white_pawns_inf[i][0], pieces.white_pawns_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

                        else:

                            if tile_y == 7:

                                for legal_move in pieces.final_legal_moves:

                                    if legal_move[:-1] == move:

                                        pieces.promotion_strip_inf = [tile_x, tile_y, True, pawn_placement]

                                        break

                pawn_placement += 1

            for i in range(0, 10):

                if pieces.white_bishops_inf[i][2] == True and pieces.white_bishops_inf[i][4] == True:

                    while self.run and pieces.white_bishops_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("B", pieces.white_bishops_inf[i][0], pieces.white_bishops_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 10):

                if pieces.white_knights_inf[i][2] == True and pieces.white_knights_inf[i][4] == True:

                    while self.run and pieces.white_knights_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("N", pieces.white_knights_inf[i][0], pieces.white_knights_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 10):

                if pieces.white_rooks_inf[i][2] == True and pieces.white_rooks_inf[i][4] == True:

                    while self.run and pieces.white_rooks_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("R", pieces.white_rooks_inf[i][0], pieces.white_rooks_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 9):

                if pieces.white_queens_inf[i][2] == True and pieces.white_queens_inf[i][4] == True:

                    while self.run and pieces.white_queens_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("Q", pieces.white_queens_inf[i][0], pieces.white_queens_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            if pieces.white_king_inf[0][2] == True and pieces.white_king_inf[0][4] == True:

                while self.run and pieces.white_king_inf[0][4] == True:

                    pass

                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_x = mouse_pos[0]
                mouse_pos_y = mouse_pos[1]

                if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                    if self.playing_as_white:

                        tile_x = mouse_pos_x // self.tile_size
                        tile_y = 7 - (mouse_pos_y // self.tile_size)

                    else:

                        tile_x = 7 - (mouse_pos_x // self.tile_size)
                        tile_y = mouse_pos_y // self.tile_size

                    move = notation.get_notation("K", pieces.white_king_inf[0][0], pieces.white_king_inf[0][1], tile_x, tile_y)

                    if move in pieces.final_legal_moves:

                        self.move_choice = move

                    else:

                        for move in pieces.final_legal_moves:

                            if move == "O-O" and (tile_x == 6 or tile_x == 7) and tile_y == 0:

                                self.move_choice = move

                            if move == "O-O-O" and (tile_x == 0 or tile_x == 2) and tile_y == 0:

                                self.move_choice = move

            pawn_placement = 0

            for i in range(0, 8):

                if pieces.black_pawns_inf[i][2] == True and pieces.black_pawns_inf[i][4] == True:

                    while self.run and pieces.black_pawns_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("P", pieces.black_pawns_inf[i][0], pieces.black_pawns_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

                        else:

                            if tile_y == 0:

                                for legal_move in pieces.final_legal_moves:

                                    if legal_move[:-1] == move:

                                        pieces.promotion_strip_inf = [tile_x, tile_y, True, pawn_placement]

                                        break

                pawn_placement += 1

            for i in range(0, 10):

                if pieces.black_bishops_inf[i][2] == True and pieces.black_bishops_inf[i][4] == True:

                    while self.run and pieces.black_bishops_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("B", pieces.black_bishops_inf[i][0], pieces.black_bishops_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 10):

                if pieces.black_knights_inf[i][2] == True and pieces.black_knights_inf[i][4] == True:

                    while self.run and pieces.black_knights_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("N", pieces.black_knights_inf[i][0], pieces.black_knights_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 10):

                if pieces.black_rooks_inf[i][2] == True and pieces.black_rooks_inf[i][4] == True:

                    while self.run and pieces.black_rooks_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("R", pieces.black_rooks_inf[i][0], pieces.black_rooks_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            for i in range(0, 9):

                if pieces.black_queens_inf[i][2] == True and pieces.black_queens_inf[i][4] == True:

                    while self.run and pieces.black_queens_inf[i][4] == True:

                        pass

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0]
                    mouse_pos_y = mouse_pos[1]

                    if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                        if self.playing_as_white:

                            tile_x = mouse_pos_x // self.tile_size
                            tile_y = 7 - (mouse_pos_y // self.tile_size)

                        else:

                            tile_x = 7 - (mouse_pos_x // self.tile_size)
                            tile_y = mouse_pos_y // self.tile_size

                        move = notation.get_notation("Q", pieces.black_queens_inf[i][0], pieces.black_queens_inf[i][1], tile_x, tile_y)

                        if move in pieces.final_legal_moves:

                            self.move_choice = move

            if pieces.black_king_inf[0][2] == True and pieces.black_king_inf[0][4] == True:

                while self.run and pieces.black_king_inf[0][4] == True:

                    pass

                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_x = mouse_pos[0]
                mouse_pos_y = mouse_pos[1]

                if mouse_pos_x >= self.tile_size * 0 and mouse_pos_x < self.tile_size * 8 and mouse_pos_y >= self.tile_size * 0 and mouse_pos_y < self.tile_size * 8:

                    if self.playing_as_white:

                        tile_x = mouse_pos_x // self.tile_size
                        tile_y = 7 - (mouse_pos_y // self.tile_size)

                    else:

                        tile_x = 7 - (mouse_pos_x // self.tile_size)
                        tile_y = mouse_pos_y // self.tile_size

                    move = notation.get_notation("K", pieces.black_king_inf[0][0], pieces.black_king_inf[0][1], tile_x, tile_y)

                    if move in pieces.final_legal_moves:

                        self.move_choice = move

                    else:

                        for move in pieces.final_legal_moves:

                            if move == "O-O" and (tile_x == 6 or tile_x == 7) and tile_y == 7:

                                self.move_choice = move

                            if move == "O-O-O" and (tile_x == 0 or tile_x == 2) and tile_y == 7:

                                self.move_choice = move

    def redraw_board_for_outline(self, x, y):

        pieces.tile_outline_inf[0] = x
        pieces.tile_outline_inf[1] = y

        pieces.tile_outline_inf[2] = True

    def redraw_board_without_outline(self):

        pieces.tile_outline_inf[2] = False
        pieces.tile_outline_inf[3] = False

    def player_customisations_func(self):

        #self.update_display = False

        #board.draw_board()
        #pieces.draw_pieces_white()

        #self.update_display = True

        while self.run:

            print("How many players? (0-2)")
            player_amount = input()

            try:

                player_amount = int(player_amount)

                if player_amount >= 0 and player_amount <= 2:

                    break

                else:

                    print("That is not a valid number.")

            except:

                print("That is not a valid number.")

        if player_amount == 0:

            self.auto_move = True

        elif player_amount == 1:

            self.one_player = True

            while self.run:

                print("Do you want to play as white, black or a random colour? (w/b/r)")
                playing_as_input = input()

                if playing_as_input == "w":

                    self.playing_as_white = True
                    break

                elif playing_as_input == "b":

                    self.playing_as_white = False
                    break

                elif playing_as_input == "r":

                    self.playing_as_white = random.choice([True, False])
                    break

                else:

                    print("That is not a valid answer.")

            self.your_turn = self.playing_as_white

        elif player_amount == 2:

            self.two_player = True

            while self.run:

                print("Do you want to rotate the board automatically? (y/n)")
                board_rotate_input = input()

                if board_rotate_input == "y":

                    self.auto_rotate = True
                    break

                elif board_rotate_input == "n":

                    self.auto_rotate = False
                    break

                else:

                    print("That is not a valid answer.")

        while self.run:

            print("Do you want to play from a pre-determined position? (y/n)")
            predetermined_position_input = input()

            if predetermined_position_input == "y":

                while self.run:

                    print("Paste the fen position.")
                    fen_position = input()

                    try:

                        notation.load_fen_position(fen_position)
                        break

                    except:

                        print("That is not a valid position.")

                self.update_display = False

                board.draw_board()

                if self.playing_as_white == True:

                    pieces.draw_pieces_white()

                else:

                    pieces.draw_pieces_black()

                self.update_display = True

                break

            elif predetermined_position_input == "n":

                break

            else:

                print("That is not a valid answer.")

        while self.run:

            print("Would you like to save this game's data? (y/n)")
            save_game_data_input = input()

            if save_game_data_input == "y":

                self.save_game_data = True

                if not os.path.exists(f"Data"):

                    os.mkdir(f"Data")

                self.game_save_list = os.listdir(f"Data")
                self.game_save_number = len(self.game_save_list)
                self.game_save_winner = None

                os.mkdir(f"Data/Game{self.game_save_number+1}")

                break

            elif save_game_data_input == "n":

                break

            else:

                print("That is not a valid answer.")

        if self.playing_as_white == True:

            pieces.draw_pieces_white()

        else:

            pieces.draw_pieces_black()

        draw_by_insufficient_material = pieces.check_draw_by_insufficient_material()

        if draw_by_insufficient_material == True:

            print("It's a draw by insufficient material!")

            self.auto_move = False
            self.one_player = False
            self.two_player = False

        self.update = True

    def auto_move_func(self):

        pieces.white_black_occupation()
        pieces.calc_legal_moves()
        pieces.check_checks()

        pieces.final_legal_moves = deepcopy(pieces.legal_moves)

        if len(pieces.final_legal_moves) > 0:

            if pieces.half_move_limit == True:

                print("It's a draw by too many moves!")

                if self.save_game_data == True:

                    self.game_save_amount -= 1
                    self.game_save_winner = 0

                self.auto_move = False

            else:

                time.sleep(0)

                self.move_choice = engine.engine()

                pieces.final_legal_moves = []

                notation_val, take = pieces.convert_to_easy_notation(self.move_choice)
                pieces.move_piece(notation_val, take)

                if pieces.half_moves >= 100:

                    pieces.half_move_limit = True

                self.white_turn = not self.white_turn

                self.update_display = False

                board.draw_board()

                if self.playing_as_white == True:

                    pieces.draw_pieces_white()

                else:

                    pieces.draw_pieces_black()

                self.update_display = True

                draw_by_insufficient_material = pieces.check_draw_by_insufficient_material()

                if draw_by_insufficient_material == True:

                    print("It's a draw by insufficient material!")

                    self.auto_move = False

                draw_by_repetition = notation.save_notation_for_repetition()

                if draw_by_repetition == True:

                    print("It's a draw by repetition!")

                    self.auto_move = False

            if self.save_game_data == True:

                self.save_game_data_func()

        else:

            pieces.no_moves()

            if self.save_game_data == True:

                self.save_game_data_func()

            self.auto_move = False

        self.update = True

    def one_player_func(self):

        pieces.white_black_occupation()
        pieces.calc_legal_moves()
        pieces.check_checks()

        pieces.final_legal_moves = deepcopy(pieces.legal_moves)

        if len(pieces.final_legal_moves) > 0:

            if pieces.half_move_limit == True:

                print("It's a draw by too many moves!")

                if self.save_game_data == True:

                    self.game_save_amount -= 1
                    self.game_save_winner = 0

                self.one_player = False

            else:

                if self.your_turn == True:

                    print(pieces.final_legal_moves)

                    while self.run:

                        print("Choose a move! (Copy the move exactly)")

                        while self.run and self.move_choice == "":

                            pass

                        if self.move_choice in pieces.final_legal_moves:

                            pieces.final_legal_moves = []

                            break

                        else:

                            print("That is not a valid move.")

                else:

                    time.sleep(0)

                    self.move_choice = engine.engine()

                    pieces.final_legal_moves = []

                self.your_turn = not self.your_turn

                notation_val, take = pieces.convert_to_easy_notation(self.move_choice)
                self.move_choice = ""

                pieces.move_piece(notation_val, take)

                if pieces.half_moves >= 100:

                    pieces.half_move_limit = True

                self.white_turn = not self.white_turn

                self.update_display = False

                board.draw_board()

                if self.playing_as_white == True:

                    pieces.draw_pieces_white()

                else:

                    pieces.draw_pieces_black()

                self.update_display = True

                draw_by_insufficient_material = pieces.check_draw_by_insufficient_material()

                if draw_by_insufficient_material == True:

                    print("It's a draw by insufficient material!")

                    self.one_player = False

                draw_by_repetition = notation.save_notation_for_repetition()

                if draw_by_repetition == True:

                    print("It's a draw by repetition!")

                    self.one_player = False

            if self.save_game_data == True:

                self.save_game_data_func()

        else:

            pieces.no_moves()

            if self.save_game_data == True:

                self.save_game_data_func()

            self.one_player = False

        self.update = True

    def two_player_func(self):

        pieces.white_black_occupation()
        pieces.calc_legal_moves()
        pieces.check_checks()

        pieces.final_legal_moves = deepcopy(pieces.legal_moves)

        if len(pieces.final_legal_moves) > 0:

            if pieces.half_move_limit == True:

                print("It's a draw by too many moves!")

                if self.save_game_data == True:

                    self.game_save_amount -= 1
                    self.game_save_winner = 0

                self.two_player = False

            else:

                print(pieces.final_legal_moves)

                while self.run:

                    print("Choose a move! (Copy the move exactly)")

                    while self.run and self.move_choice == "":

                        pass

                    #self.move_choice = input()

                    #if self.move_choice in pieces.final_legal_moves:

                    if self.move_choice in pieces.final_legal_moves:

                        pieces.final_legal_moves = []

                        break

                    else:

                        print("That is not a valid move.")

                notation_val, take = pieces.convert_to_easy_notation(self.move_choice)
                self.move_choice = ""

                #notation_val, take = pieces.convert_to_easy_notation(self.move_choice)
                pieces.move_piece(notation_val, take)

                if pieces.half_moves >= 100:

                    pieces.half_move_limit = True

                self.white_turn = not self.white_turn

                if self.auto_rotate == True:

                    self.playing_as_white = self.white_turn

                self.update_display = False

                board.draw_board()

                if self.playing_as_white == True:

                    pieces.draw_pieces_white()

                else:

                    pieces.draw_pieces_black()

                self.update_display = True

                draw_by_insufficient_material = pieces.check_draw_by_insufficient_material()

                if draw_by_insufficient_material == True:

                    print("It's a draw by insufficient material!")

                    self.two_player = False

                draw_by_repetition = notation.save_notation_for_repetition()

                if draw_by_repetition == True:

                    print("It's a draw by repetition!")

                    self.two_player = False

            if self.save_game_data == True:

                self.save_game_data_func()

        else:

            pieces.no_moves()

            if self.save_game_data == True:

                self.save_game_data_func()

            self.two_player = False

        self.update = True

    def play_again_func(self):

        while self.run:

            print("Do you want to play again? (y/n)")

            play_again_input = input()

            if play_again_input == "y":

                self.white_turn = True
                self.playing_as_white = True
                self.auto_rotate = False
                self.your_turn = True

                self.save_game_data = False

                self.auto_move = False
                self.one_player = False
                self.two_player = False

                self.move_choice = ""

                repetition_draw_file_write = open("repetition_draw_file.txt", "w")
                repetition_draw_file_write.write("")
                repetition_draw_file_write.close()

                pieces.white_pawns_inf = [[0, 1, True, False, False, True], [1, 1, True, False, False, True], [2, 1, True, False, False, True], [3, 1, True, False, False, True], [4, 1, True, False, False, True], [5, 1, True, False, False, True], [6, 1, True, False, False, True], [7, 1, True, False, False, True]]
                pieces.white_bishops_inf = [[2, 0, True, False, False], [5, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.white_knights_inf = [[1, 0, True, False, False], [6, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.white_rooks_inf = [[0, 0, True, False, False, True], [7, 0, True, False, False, True], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False]]
                pieces.white_queens_inf = [[3, 0, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.white_king_inf = [[4, 0, True, False, False, True]]

                pieces.black_pawns_inf = [[0, 6, True, False, False, True], [1, 6, True, False, False, True], [2, 6, True, False, False, True], [3, 6, True, False, False, True], [4, 6, True, False, False, True], [5, 6, True, False, False, True], [6, 6, True, False, False, True], [7, 6, True, False, False, True]]
                pieces.black_bishops_inf = [[2, 7, True, False, False], [5, 7, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.black_knights_inf = [[6, 7, True, False, False], [1, 7, True, False, False], [6, 3, False, False, False], [0, 3, False, False, False], [2, 0, False, False, False], [2, 6, False, False, False], [6, 2, False, False, False], [0, 2, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.black_rooks_inf = [[0, 7, True, False, False, True], [7, 7, True, False, False, True], [2, 0, False, False, False, False], [4, 6, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False], [0, 7, False, False, False, False]]
                pieces.black_queens_inf = [[3, 7, True, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False], [0, 7, False, False, False]]
                pieces.black_king_inf = [[4, 7, True, False, False, True]]

                pieces.tile_outline_inf = [0, 0, False, False]
                pieces.promotion_strip_inf = [0, 0, False, 0]

                pieces.piece_value_matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0]]

                pieces.white_occupation_x = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
                pieces.white_occupation_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

                pieces.black_occupation_x = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
                pieces.black_occupation_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

                pieces.en_passant_x_y = [8, 8]

                pieces.half_moves = 0
                pieces.half_move_limit = False
                pieces.turn_num = 1

                self.player_customisations_func()

                self.update = True

                break

            elif play_again_input == "n":

                break

            else:

                print("That is not a valid answer.")

    def save_game_data_func(self):

        os.mkdir(f"Data/Game{self.game_save_number+1}/Position{self.game_save_amount+1}")
        numpy.save(f"Data/Game{self.game_save_number+1}/Position{self.game_save_amount+1}/Board.npy", numpy.asarray(pieces.convert_pieces_to_matrix()))
        numpy.save(f"Data/Game{self.game_save_number+1}/Position{self.game_save_amount+1}/Move.npy", numpy.asarray(self.move_choice))
        numpy.save(f"Data/Game{self.game_save_number+1}/Position{self.game_save_amount+1}/Turn.npy", numpy.asarray([self.white_turn]))

        if self.game_save_winner != None:

            # calculates the winner based on the amount of material left
            if self.game_save_winner == 0:

                white_points = 0

                num_of_white_pawns = len(pieces.white_pawns_inf)
                for i in range(0, num_of_white_pawns):

                    if pieces.white_pawns_inf[i][2] == True:
                        white_points += 1

                num_of_white_knights = len(pieces.white_knights_inf)
                for i in range(0, num_of_white_knights):

                    if pieces.white_knights_inf[i][2] == True:
                        white_points += 3

                num_of_white_bishops = len(pieces.white_bishops_inf)
                for i in range(0, num_of_white_bishops):

                    if pieces.white_bishops_inf[i][2] == True:
                        white_points += 3.5

                num_of_white_rooks = len(pieces.white_rooks_inf)
                for i in range(0, num_of_white_rooks):

                    if pieces.white_rooks_inf[i][2] == True:
                        white_points += 5

                num_of_white_queens = len(pieces.white_queens_inf)
                for i in range(0, num_of_white_queens):

                    if pieces.white_queens_inf[i][2] == True:
                        white_points += 8

                black_points = 0

                num_of_black_pawns = len(pieces.black_pawns_inf)
                for i in range(0, num_of_black_pawns):

                    if pieces.black_pawns_inf[i][2] == True:
                        black_points += 1

                num_of_black_knights = len(pieces.black_knights_inf)
                for i in range(0, num_of_black_knights):

                    if pieces.black_knights_inf[i][2] == True:
                        black_points += 3

                num_of_black_bishops = len(pieces.black_bishops_inf)
                for i in range(0, num_of_black_bishops):

                    if pieces.black_bishops_inf[i][2] == True:
                        black_points += 3.5

                num_of_black_rooks = len(pieces.black_rooks_inf)
                for i in range(0, num_of_black_rooks):

                    if pieces.black_rooks_inf[i][2] == True:
                        black_points += 5

                num_of_black_queens = len(pieces.black_queens_inf)
                for i in range(0, num_of_black_queens):

                    if pieces.black_queens_inf[i][2] == True:
                        black_points += 8

                if white_points > black_points:

                    self.game_save_winner = 1

                elif black_points > white_points:

                    self.game_save_winner = -1

                else:

                    self.game_save_winner = 0

            print(self.game_save_winner)
            numpy.save(f"Data/Game{self.game_save_number+1}/Winner.npy", numpy.asarray([self.game_save_winner]))

startup = Start()
board = Board()
pieces = Pieces()
notation = Notation()
engine = NeuralNet.NeuralNetwork()
