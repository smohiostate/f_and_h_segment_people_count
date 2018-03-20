import math



class IncompatibleDimensionsError(Exception):
    pass


class Coordinate(object):

    def __init__(self, *dimensional_components):
        self._dimensional_components = dimensional_components

    def __repr__(self):
        return 'Coordinate({})'.format(', '.join([str(dimension) for dimension in self._dimensional_components]))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            dimensional_components_extended = [dimensional_component + other for dimensional_component in self.dimensional_components()]
            return Coordinate(*dimensional_components_extended)

        if not isinstance(other, Coordinate):
            raise ValueError('Addition of non-coordinates is invalid.')

        if self.number_of_dimensions() != other.number_of_dimensions():
            raise IncompatibleDimensionsError('Coordinates do not match dimensions.')

        dimensional_components_added = map(lambda components: sum(components), zip(self.dimensional_components(), other.dimensional_components()))
        return Coordinate(*dimensional_components_added)


    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            dimensional_components_extended = [dimensional_component - other for dimensional_component in self.dimensional_components()]
            return Coordinate(*dimensional_components_extended)

        if not isinstance(other, Coordinate):
            raise ValueError('Subtraction of non-coordinates is invalid.')

        if self.number_of_dimensions() != other.number_of_dimensions():
            raise IncompatibleDimensionsError('Coordinates do not match dimensions.')

        dimensional_components_subtracted = map(lambda components: sum(components), zip(self.dimensional_components(), other.dimensional_components()))
        return Coordinate(*dimensional_components_subtracted)

    def __len__(self):
        return self.magnitude()

    def __mul__(self, other):
        raise ArithmeticError('Using the generic multiplication operator between coordinates is vague. Please use scale(), cross_product(), or dot_product().')

    def scale(self, muliplier):
        raise NotImplementedError

    def cross_product(self, other):
        raise NotImplementedError

    def dot_product(self, other):
        raise NotImplementedError

    def dimensional_components(self):
        return self._dimensional_components

    def number_of_dimensions(self):
        return len(self.dimensional_components())

    def magnitude(self):
        square_sum_of_dimensional_components = sum([component ** 2 for component in self.dimensional_components()])
        return math.sqrt(square_sum_of_dimensional_components)
