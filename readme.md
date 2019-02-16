# GJK: Gilbert Johnson Keerthi Distance Algorithm

Experimenting with shapes and if they intersect with each other.

1. Wikipedia article: https://en.wikipedia.org/wiki/Gilbert%E2%80%93Johnson%E2%80%93Keerthi_distance_algorithm
2. Casey Muratori Presents GJKL: https://youtu.be/Qupqu1xe7Io
3. Siggraph 2017 Related: https://www.youtube.com/watch?v=NcivnQ02rGw

# The Algorithm:
  -- Where:
      -> Q - Simplex Set - list of points - in this case 1 to 4
      -> d - direction
      -> C - shape (1, 2, or 3 dimensions)
      -> P - point
      -> CH() - Convex Hull()
      -> Sc() - Subset of Shape
      -> V = Most extreme point of C in a particular direction
      
1. Initialize the simplex set Q with up to d+1 points from C (in d dimensions)
2. Compute point P of minimum norm in CH(Q)
3. If P is the origin, exit; return 0
4. Reduce Q to the smallest subset Q’ of Q, such that P in CH(Q’)
5. Let V=Sc(–P) be a supporting point in direction –P
6. If V no more extreme in direction –P than P itself, exit; return ||P||
7. Add V to Q. Go to step 2

# Examples from the webs: 
- C implimentation of GJK: https://github.com/ElsevierSoftwareX/SOFTX_2018_38/blob/master/lib/src/openGJK.c
- Python implimentation of GJK: https://github.com/Wopple/GJK/blob/master/python/gjk.py
- Another c: https://github.com/kroitor/gjk.c/blob/master/gjk.c
- example: https://pastebin.com/FXbS9GGS
- Tutorial: http://vec3.ca/gjk/implementation/

# Basic Things I think I"m learning :)
Q. What is a simplex?  
A. A simplex is a vert set that can form simple shapes, such as a line, a triangle, or tetrahedron.

Q. What is going on with this algorithm?  
A. The structure comes down to three main parts. 
- The main loop which searches simplex shapes in search of encompassing the origin
- The Support - calculating new distance to origin.
- NearestSimplex - decides if problem is solved, updates simplex, and calcs new direction to origin

Q. What does the dot product do here?  
A. The dot product is used to discover if the origin is getting closer or further away from the simplex.    
For example, if |A||B| . |origin| is negative - then the origin is getting further away from our search.  This  
information can be used to throw away the first point (which should be the furthest from origin), use the opposite direction to get another point that
should be now closer to the origin. Looping again would grab a new point and |B||C| . |origin| should now be positive.

Q. What does the cross product do here?  
A. The cross product calculates the direction from the simplex to origin.

Q. Do we need to calculate for a simplex of zero or 1?  
A. The algorithm will always calculate on a minimum of two points since its primed with the first item before entering
the algorithm's loop.  And upon entering the loop a second item is added.  

Q. Do we need to calculate for a simplex of greater than 4 (tetrahedron?)  
A. ??