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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

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

        self.origin = Vec3(
            (corner1.x + corner2.x) / 2,
            (corner1.y + corner2.y) / 2,
            (corner1.z + corner2.z) / 2,
        )

        self.points = list()
        self.create_points(corner1, corner2)

    @classmethod
    def new(cls):
        return Cube(Vec3(0, 0, 0), Vec3(1, 1, 1))

    def create_points(self, corner1, corner2):
        x_distance = abs(corner1.x) + abs(corner2.x)
        y_distance = abs(corner1.y) + abs(corner2.y)
        # ignoring z as it is the min/max for the bottom/top
        # z_distance = abs(corner1.z) + abs(corner2.z)
        self.points.append(corner1)
        self.points.append(Vec3(corner1.x, corner1.y + y_distance, corner1.z))
        self.points.append(Vec3(corner1.x + x_distance, corner1.y, corner1.z))
        self.points.append(
            Vec3(corner1.x + x_distance, corner1.y + y_distance, corner1.z)
        )

        self.points.append(
            Vec3(corner2.x - x_distance, corner2.y - y_distance, corner2.z)
        )
        self.points.append(Vec3(corner2.x - x_distance, corner2.y, corner2.z))
        self.points.append(corner2)
        self.points.append(Vec3(corner2.x, corner2.y - y_distance, corner2.z))

    def translate(self, x, y, z):
        for point in self.points:
            point.x += x
            point.y += y
            point.z += z

    def rotate(self, degrees, direction):
        """

        :param degrees: in radians
        :param direction: x, y, z value
        :return:
        """
        pass

    def get_cube_origin(self):

        x, y, z = 0, 0, 0

        for point in self.points:
            x += point.x
            y += point.y
            z += point.z

        return Vec3(x / 8, y / 8, z / 8)


def dot(a, b):
    """Calculate the magnitude of one vector multiplied by another."""
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
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
        product = dot(point, direction)
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
        b, a = simplex

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
        if dot(ab, ao) >= 0:
            d = cross(cross(ab, ao), ab)
        else:
            simplex.pop(0)
            d = ao

    # __ Three point simplex: Triangle
    elif len(simplex) == 3:
        c, b, a = simplex
        ao = -a
        ab = b - a  # from point A to B
        ac = c - a  # from point A to C

        abc = cross(ab, ac)  # Compute the triangle's normal

        # Test in one direction of the face
        if dot(cross(abc, ac), ao) >= 0:

            if dot(ac, ao) >= 0:
                simplex = [a, c]
                d = cross(cross(ac, ao), ac)
            else:
                if dot(ab, ao) >= 0:
                    simplex = [a, b]
                    d = cross(cross(ab, ao), ab)
                else:
                    simplex = [a]
                    d = ao

        # Test in the other direction ...
        else:
            if dot(cross(ab, abc), ao) >= 0:
                if dot(ab, ao) >= 0:
                    simplex = [a, b]
                    d = cross(cross(ab, ao), ab)
                else:
                    simplex = [a]
                    d = ao
            else:
                if dot(abc, ao) > 0:
                    simplex = [a, b, c]
                    d = abc
                else:
                    simplex = [a, c, b]
                    d = -abc

    # __ Four point simplex: Tetrahedron
    elif len(simplex) == 4:
        d, c, b, a = simplex

        ao = -a

        ab = b - a
        ac = c - a
        ad = d - a

        abc = cross(ab, ac)
        acd = cross(ac, ad)
        adb = cross(ad, ab)

        if dot(abc, ao) >= 0 and dot(acd, ao) >= 0 and dot(adb, ao) >= 0:
            # must be behind all three faces so we have surrounded the origin!
            return simplex, d, True

        # This has never been hit yet in my tests -- I need a test case.
        # print(simplex)

    # print("Direction:", d)
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

    for _ in range(10000):  # cube only has 8 verts - should pass/fail before ten
        a = support(p, direction) - support(q, -direction)

        if dot(a, direction) < 0:
            # print("Collision NOT detected.")
            return False
        #
        # if a == direction:
        #     # print("Direction and vert in the same location -- we must have origin?")
        #     return True

        simplex.append(a)

        simplex, direction, contains_origin = nearest_simplex(simplex, direction)
        if contains_origin:
            # print("Collision detected using the following simplex: {}".format(simplex))
            return True

    # print("Failed to find an answer.")

    return False


def test_01_no_collision():
    # Create Test cubes
    cube_01 = Cube(Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5))
    cube_02 = Cube(Vec3(0.8, 0.8, 0.8), Vec3(1, 1, 1))

    direction = Vec3(0.1, 0.2, 1.0)

    result = gjk_intersection(cube_01, cube_02, direction)

    print("[{}] test_01_no_collision".format("passed" if result is False else "FAILED"))


def test_02_collision():
    # Create Test cubes
    cube_01 = Cube(Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5))
    cube_02 = Cube(Vec3(0.1, 0.1, 0.1), Vec3(1, 1, 1))

    direction = Vec3(1.0, 0.0, 0.0)

    result = gjk_intersection(cube_01, cube_02, direction)

    print("[{}] test_02_collision".format("passed" if result is True else "FAILED"))


def test_03_collision_with_cubes_in_negative_space():
    """Note that the starting point edge is touching and at 0,0,0."""
    # Create Test cubes
    cube_01 = Cube(Vec3(-0.5, -0.5, -0.5), Vec3(0.5, 0.5, 0.5))
    cube_02 = Cube(Vec3(-0.2, -0.2, -0.2), Vec3(0.2, 0.2, 0.2))

    # A random starting direction
    direction = Vec3(0.0, 0.2, 0.0)

    result = gjk_intersection(cube_01, cube_02, direction)

    print(
        "[{}] test_03_collision_lower_corner_verts_in_same_position".format(
            "passed" if result is True else "FAILED"
        )
    )


def test_04_collision_with_with_x_positive_direction():
    # Create Test cubes
    cube_01 = Cube(Vec3(0, 0, 0), Vec3(1, 1, 1))
    cube_02 = Cube(Vec3(0.2, 0.2, 0.2), Vec3(1, 1, 1))

    direction = Vec3(1.0, 0.0, 0.0)

    result = gjk_intersection(cube_01, cube_02, direction)

    print(
        "[{}] test_04_collision_with_with_x_positive_direction".format(
            "passed" if result is True else "FAILED"
        )
    )


def test_05_collision_edges_touching():
    # Create Test cubes
    cube_01 = Cube(Vec3(1, 1, 1), Vec3(1.1, 1.1, 1.1))
    cube_02 = Cube(Vec3(1, 1, 1), Vec3(1.2, 1.2, 1.2))

    direction = Vec3(0.0, 0.1, 1.0)

    result = gjk_intersection(cube_01, cube_02, direction)

    print(
        "[{}] test_05_collision_edges_touching".format(
            "passed" if result is True else "FAILED"
        )
    )


def test_06_move_cube():
    cube_01 = Cube(Vec3(0, 0, 5), Vec3(1, 1, 6))
    cube_02 = Cube(Vec3(0, 0, 1), Vec3(1, 1, 4))

    direction = Vec3(0.0, 0.1, 2.0)
    index, result = -1, False
    for index in range(1_000_000_000):
        cube_02.translate(0, 0, 0.001)
        result = gjk_intersection(cube_01, cube_02, direction)
        if result:
            break

    print(
        "[{}] test_06_move_cube() in {} iterations".format(
            "passed" if result is True else "FAILED", index + 1
        )
    )


if __name__ == "__main__":
    test_01_no_collision()
    test_02_collision()
    test_03_collision_with_cubes_in_negative_space()
    test_04_collision_with_with_x_positive_direction()
    test_05_collision_edges_touching()
    test_06_move_cube()

    # cube = Cube.new()
    # for p in cube.points:
    #     print(p)
    # print(cube.origin)
