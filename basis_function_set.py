from DinoFem import *

# --------------------------------------------------------
# 基函数说明
#
# 1D 基函数
# 线性基函数   编号 101  对应函数 phi_1d_linear
# 二次基函数   编号 102  对应函数 phi_1d_quadratic


class BasisFun:
    def __init__(self, basis_type):
        self.basis_type = basis_type
        self.phi = None
        self.num_of_local_basis_fun = None
        self.dim = None
        self.set_basis_fun()

    def set_basis_fun(self):
        if self.basis_type == 101:
            self.dim = 1
            self.phi = phi_1d_linear
            self.num_of_local_basis_fun = 2
        else:
            # TODO
            logger.error(__file__ + "--" + "this form will update later, now  only have the 101 basis type")
            exit(0)


def phi_1d_linear(p1, p2, alpha, diff_x, x):
    if alpha not in [0, 1] or diff_x not in [0, 1, 2, 3]:
        logger(__file__ + "--" + "alpha or diff_x index wrong ,should be 0 or 1!")
        exit(0)
    h = p2-p1
    if diff_x == 0:
        if alpha == 0:
            return (p2-x)/h
        else:
            return (x-p1)/h
    elif diff_x == 1:
        if alpha == 0:
            return -1/h
        else:
            return 1/h
    else:
        return 0


if __name__ == '__main__':
    b=BasisFun(101)
    print(b.dim)