

class IntegrateSet:
    def __init__(self):
        self.integrate_type=None

    @staticmethod
    def gauss_1d(f,a,b):
        # Gauss_Legand integrate
        gauss_points = [0, 0.9061798, 0.5384693, -0.9061798, -0.5384693]
        gauss_weights = [0.5688889, 0.2369269, 0.4786287, 0.2369269, 0.4786287]
        int_value=0.0
        l1 = (b - a) / 2
        l2 = (b + a) / 2

        for i in range(len(gauss_points)):
            x_star = l2+gauss_points[i]*l1
            int_value += l1*gauss_weights[i]*f(x_star)
        return int_value

    @classmethod
    def integrator(cls,integrator_name):
        if integrator_name == "Gauss1D":
            return cls.gauss_1d


if __name__ == '__main__':
    def f(x):
        import math
        return math.exp(x)
    print(IntegrateSet.gauss(f,0,1))