
import math 

class Vector2(object):
    """A class representing a 2D vector."""

    def __init__(self, x=0, y=0):
        """Initialize the Vector2 object.

        Args:
            x (float): The x-coordinate of the vector. Default is 0.
            y (float): The y-coordinate of the vector. Default is 0.
        """
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):
        """Add two vectors.

        Args:
            other (Vector2): The vector to be added.

        Returns:
            Vector2: The sum of the two vectors.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract two vectors.

        Args:
            other (Vector2): The vector to be subtracted.

        Returns:
            Vector2: The difference between the two vectors.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """Negate the vector.

        Returns:
            Vector2: The negated vector.
        """
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        """Multiply the vector by a scalar.

        Args:
            scalar (float): The scalar value to multiply the vector by.

        Returns:
            Vector2: The scaled vector.
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        """Divide the vector by a scalar (Python 2.x).

        Args:
            scalar (float): The scalar value to divide the vector by.

        Returns:
            Vector2: The divided vector.
        """
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        """Divide the vector by a scalar (Python 3.x).

        Args:
            scalar (float): The scalar value to divide the vector by.

        Returns:
            Vector2: The divided vector.
        """
        return self.__div__(scalar)

    def __eq__(self, other):
        """Check if two vectors are approximately equal.

        Args:
            other (Vector2): The vector to compare with.

        Returns:
            bool: True if the vectors are approximately equal, False otherwise.
        """
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitudeSquared(self):
        """Calculate the squared magnitude of the vector.

        Returns:
            float: The squared magnitude of the vector.
        """
        return self.x**2 + self.y**2

    def magnitude(self):
        """Calculate the magnitude of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return math.sqrt(self.magnitudeSquared())

    def copy(self):
        """Create a copy of the vector.

        Returns:
            Vector2: A copy of the vector.
        """
        return Vector2(self.x, self.y)

    def asTuple(self):
        """Convert the vector to a tuple.

        Returns:
            tuple: The vector as a tuple.
        """
        return self.x, self.y

    def asInt(self):
        """Convert the vector to a tuple with integer values.

        Returns:
            tuple: The vector as a tuple with integer values.
        """
        return int(self.x), int(self.y)

    def __str__(self):
        """Convert the vector to a string representation.

        Returns:
            str: The vector as a string.
        """
        return "<"+str(self.x)+", "+str(self.y)+">"