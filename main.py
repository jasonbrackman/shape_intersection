# Experimenting with shapes and if they intersect with each other.
# 1. https://en.wikipedia.org/wiki/Gilbert%E2%80%93Johnson%E2%80%93Keerthi_distance_algorithm
#    - https://youtu.be/Qupqu1xe7Io
#
#  The GJK Algorithm:
#   -- Where:
#       -> Q - Simplex Set - list of points - in this case 1 to 4
#       -> d - direction
#       -> C - shape (1, 2, or 3 dimensions)
#       -> P - point
#       -> CH() - Convex Hull()
#       -> Sc() - Subset of Shape
#       -> V = Most extreme point of C in a particular direction
# 1. Initialize the simplex set Q with up to d+1 points from C (in d dimensions)
# 2. Compute point P of minimum norm in CH(Q)
# 3. If P is the origin, exit; return 0
# 4. Reduce Q to the smallest subset Q’ of Q, such that P in CH(Q’)
# 5. Let V=Sc(–P) be a supporting point in direction –P
# 6. If V no more extreme in direction –P than P itself, exit; return ||P||
# 7. Add V to Q. Go to step 2
#
# C implimentation of GJK: https://github.com/ElsevierSoftwareX/SOFTX_2018_38/blob/master/lib/src/openGJK.c
# Python implimentation of GJK: https://github.com/Wopple/GJK/blob/master/python/gjk.py
#


class Vec3:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __iter__(self):
        for item in (self._x, self._y, self._z):
            yield item

    def __neg__(self):
        return Vec3(-self._x, -self._y, -self._z)

    def __repr__(self):
        return "Vec3({}, {}, {})".format(self._x, self._y, self._z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, rhs):
        self._x = rhs

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, rhs):
        self._y = rhs

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, rhs):
        self._z = rhs


class Cube:
    """
    Cube is defined as two points that exist in opposite diagonal corners.
    - So a Vec3(0,0,0) and a Vec3(2, 2, 2) is living in xyz space for each point:
        .
          . # note that this point is 2 units away in z
    - producing a 2 x 2 x 2 cube
    """

    def __init__(self, corner1, corner2):
        self.points = list()
        self.create_points(corner1, corner2)

    def create_points(self, corner1, corner2):
        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        # create first set of points (a side)
        self.points.append(Vec3(x1, y1, z1))
        self.points.append(Vec3(x1 + x2, y1, z1))
        self.points.append(Vec3(x1 + x2, y1 + y2, z1))
        self.points.append(Vec3(x1, y1 + y2, z1))

        # create second set of points
        self.points.append(Vec3(x2, y2, z2))
        self.points.append(Vec3(x2 + x1, y2, z2))
        self.points.append(Vec3(x2 + x1, y2 + y1, z2))
        self.points.append(Vec3(x2, y2 + y1, z2))


def dot_product(a, b):
    """Calculate the magnitude of one vector multiplied by another."""
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross_product(a, b):
    """Calculate a vector that is at right angles to two points passed in."""
    return Vec3(
        a.y * b.z - a.z * b.y,  # i
        a.z * b.x - a.x * b.z,  # j
        a.x * b.y - a.y * b.x,  # k
    )


def support(shape, direction):
    """
    Support(shape, d), which returns the point on shape which has the highest dot product with d.
    - This would be teh most 'extreme' or furthest point going in the direction passed in.
    :param shape:
    :param direction:
    :return:
    """
    furthest_in_direction = None
    result = -1_000_000_000
    for point in shape.points:
        product = dot_product(point, direction)
        if product > result:
            result = product
            furthest_in_direction = point

    return furthest_in_direction


def nearest_simplex(simplex, direction):
    """
    A simplex is an array of points that may be represented as a:
    - 1 point = vert
    - 2 points = line
    - 3 points = triangle
    - 4 points = tetrahedron

    :param simplex: May contain 2, 3, or 4 points.
    :param direction:
    :return: updated points, updated direction and a bool of True if  shape contains origin.
    """

    # __ Two Point Simplex
    if len(simplex) == 2:
        b = simplex[0]
        a = simplex[1]
        ao = -a
        ab = b - a

        if dot_product(ab, ao) >= 0:
            direction = cross_product(ab, ao)

        else:
            simplex.pop(0)
            direction = ao

    # __ Three point simplex
    else:
        # need to impliment
        pass

    return simplex, direction, False


def gjk_intersection(p, q, initial_axis):
    """
    Collision detection alogrithm named after Gilbert Johnson Keerthi.
    :param p: Shape
    :param q: Shape
    :param initial_axis: Vec3
    :return:
    """
    # a -> Vec3
    # s -> list(): Simplex result
    # d -> Vec3 - Direction

    a = support(p, initial_axis) - support(q, -initial_axis)
    points = [a]
    direction = -a

    while True:
        a = support(p, direction) - support(q, -direction)

        if dot_product(a, direction) < 0:
            # reject - we tried to get the furthest point -- and the furthest point is not past origin -- so we
            # failed to even reach a place that could encompass origin.
            # no intersection / exit early
            return False

        points.append(a)
        print(points)

        points, direction, contains_origin = nearest_simplex(points, direction)
        if contains_origin:
            print("Collision detected.")
            return True


if __name__ == "__main__":
    corner1 = Vec3(0.0, 0.0, 0.0)
    corner2 = Vec3(1.0, 1.0, 1.0)

    direction = Vec3(0.0, 0.0, 1.0)
    print("[Direction]: {} and its negative: {}".format(direction, -direction))

    cube_01 = Cube(corner1, corner2)
    cube_02 = Cube(corner1, Vec3(2.0, 2.0, 2.0))

    i = support(cube_01, direction)
    print("[Cube_01] Highest Dot Product Point (+ direction): {}".format(i))

    j = support(cube_02, -direction)
    print("[Cube_02] Highest Dot Product Point (- direction): {}".format(j))

    gjk_intersection(cube_01, cube_02, direction)
