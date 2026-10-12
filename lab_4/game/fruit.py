import math

class Fruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind  # "fruit" or "bomb"
        self.sliced = False

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def contains_point(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.radius

    def intersects_segment(self, x1, y1, x2, y2):
        """True if the blade segment (x1,y1)->(x2,y2) touches this fruit.

        A single-point check misses fast swipes because the mouse can jump
        from one side of the fruit to the other between two events. Instead
        we find the point on the segment closest to the fruit's centre and
        compare that distance to the radius.
        """
        dx, dy = x2 - x1, y2 - y1
        length_sq = dx * dx + dy * dy
        if length_sq == 0:
            return self.contains_point(x1, y1)
        # Projection of the centre onto the segment, clamped to [0, 1]
        t = ((self.x - x1) * dx + (self.y - y1) * dy) / length_sq
        t = max(0.0, min(1.0, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        return self.contains_point(closest_x, closest_y)

    def off_screen(self, height):
        return self.y - self.radius > height
