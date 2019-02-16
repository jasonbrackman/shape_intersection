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
    - This would be the most 'extreme' or furthest point going in the direction passed in.
    :param shape:
    :param direction:
    :return: furthest point in the direction passed in.
    """
    furthest_in_direction = None
    result = float("-inf")
    for point in shape.points:
        product = dot_product(point, direction)
        if product > result:
            result = product
            furthest_in_direction = point

    return furthest_in_direction


def nearest_simplex(simplex, d):
    """
    A simplex is an array of points that may be represented as a:
    - 2 points = line
    - 3 points = triangle
    - 4 points = tetrahedron

    :param simplex: collection of points that can create simple shapes
    :param d:
    :return: updated points, updated direction and a bool of True if  shape contains origin.
    """

    # __ Two Point Simplex: Line
    if len(simplex) == 2:
        a, b = simplex

        # a was found in a direction away from origin - its opposite is towards Origin.
        ao = -a

        # Will result in a new vector going in the direction of the newly added point
        ab = b - a

        # if AB is perpendicular (or at a > angle) to Origin (AO):
        #   - calculate the new vector to origin from the simplex
        # else if its a negative number:
        #   - we must be going in the wrong direction
        #   - make the direction the opposite of what we started with
        #   - drop the first entry since the origin is not in that direction and we don't want to recalc later.
        if dot_product(ab, ao) >= 0:
            d = cross_product(cross_product(ab, ao), ab)
        else:
            simplex.pop(0)
            d = ao

    # __ Three point simplex: Triangle
    elif len(simplex) == 3:
        a, b, c = simplex
        ao = -a
        ab = b - a  # from point A to B
        ac = c - a  # from point A to C

        ac_perp = cross_product(cross_product(ab, ac), ac)

        if dot_product(ac_perp, ao) >= 0:
            d = ac_perp

        else:
            ab_perp = cross_product(cross_product(ac, ab), ab)
            if dot_product(ab_perp, ao) < 0:
                return simplex, d, True
            # simplex update?
            d = ab_perp

        print("in a simplex3")

    # __ Four point simplex: Tetrahedron
    elif len(simplex) == 4:
        print("What do I do here?")
        print(simplex)

    print("Direction:", d)
    return simplex, d, False


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
    simplex = [a]
    direction = -a

    for _ in range(10):  # cube only has 8 verts - should pass/fail before ten
        a = support(p, direction) - support(q, -direction)

        if dot_product(a, direction) < 0:
            print("Collision NOT detected.")
            return False

        simplex.append(a)

        simplex, direction, contains_origin = nearest_simplex(simplex, direction)
        if contains_origin:
            print("Collision detected.")
            return True

    print("Failed to find an answer.")


if __name__ == "__main__":

    direction = Vec3(34.1, 0.2, 1.0)
    print("[Direction]: {} and its negative: {}".format(direction, -direction))

    cube_01 = Cube(Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5))
    cube_02 = Cube(Vec3(0.2, 0.2, 0.2), Vec3(1, 1, 1))

    i = support(cube_01, direction)
    print("[Cube_01] Highest Dot Product Point (+ direction): {}".format(i))

    j = support(cube_02, -direction)
    print("[Cube_02] Highest Dot Product Point (- direction): {}".format(j))

    gjk_intersection(cube_01, cube_02, direction)
