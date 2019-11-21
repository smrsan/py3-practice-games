class Shape:
    def __init__(self):
        self.__matrix = [[1]]
        self.color = ''
        self.xy = [0, 0]

    def set_matrix(self, new_matrix):
        self.__matrix = new_matrix[:]

    def is_colored_block(self, x, y):
        return self.__matrix[y][x] == 1

    def is_shape(self, x, y):
        x -= self.xy[0]
        y -= self.xy[1]
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        return self.__matrix[y][x] == 1

    @property
    def width(self):
        return len(self.__matrix[0])

    @property
    def height(self):
        return len(self.__matrix)

    def go_left(self):
        self.xy[0] -= 1

    def go_right(self):
        self.xy[0] += 1

    def go_down(self):
        self.xy[1] += 1

    def go_up(self):
        self.xy[1] -= 1

    #   Rotate Matrix to Left
    #   [x0:y0] [x1:y0] [x2:y0]
    #   [x0:y1] [x1:y1] [x2:y1]
    #   [x0:y2] [x1:y2] [x2:y2]
    #   [x0:y3] [x1:y3] [x2:y3]

    #   [x0:y0]=[x2:y0] [x1:y0]=[x2:y1] [x2:y0]=[x2:y2] [x3:y0]=[x2:y3]
    #   [x0:y1]=[x1:y0] [x1:y1]=[x1:y1] [x2:y1]=[x1:y2] [x3:y1]=[x1:y3]
    #   [x0:y2]=[x0:y0] [x1:y2]=[x0:y1] [x2:y2]=[x0:y2] [x3:y2]=[x0:y3]
    def rotate_left(self):
        new_matrix = self.__get_empty_rotated_matrix()
        for y in range(self.height):
            for x in range(self.width):
                nx = y
                ny = (self.width - 1) - x
                new_matrix[ny][nx] = self.__matrix[y][x]
        self.set_matrix(new_matrix)

    #   Rotate Matrix to Right
    #   [x0:y0] [x1:y0] [x2:y0]
    #   [x0:y1] [x1:y1] [x2:y1]
    #   [x0:y2] [x1:y2] [x2:y2]
    #   [x0:y3] [x1:y3] [x2:y3]

    #   [x0,y0]=[x0:y3] [x1,y0]=[x0:y2] [x2,y0]=[x0:y1] [x3,y0]=[x0:y0]
    #   [x0,y1]=[x1:y3] [x1,y1]=[x1:y2] [x2,y1]=[x1:y1] [x3,y1]=[x1:y0]
    #   [x0,y2]=[x2:y3] [x1,y2]=[x2:y2] [x2,y2]=[x2:y1] [x3,y2]=[x2:y0]
    def rotate_right(self):
        new_matrix = self.__get_empty_rotated_matrix()
        for y in range(self.height):
            for x in range(self.width):
                nx = (self.height - 1) - y
                ny = x
                new_matrix[ny][nx] = self.__matrix[y][x]
        self.set_matrix(new_matrix)

    def get_block(self, x, y):
        try:
            return self.__matrix[y][x]
        except IndexError:
            return None

    def __get_empty_rotated_matrix(self):
        matrix = []
        for y in range(self.width):
            matrix.append([])
            for x in range(self.height):
                matrix[y].append(0)
        return matrix
