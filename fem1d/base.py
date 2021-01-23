"""
InputParam 将所有的基本输入，放置到其中。
"""
from DinoFem.fem1d import logger, BasisFun, pv


class InputParam:
    def __init__(self,
                 dim,
                 trial_basis_type,
                 test_basis_type,
                 mesh_vtk_file,
                 bc_vtk_file):
        self.__dim = dim
        # 检查维数信息
        if self.__dim in [1, 2, 3]:
            pass
        else:
            logger.error(__file__ + '---' +
                         "dimension should be 1,2,3, "+ str(dim) + "is not allowed!" )
            exit(0)

        self.__trial_basis_fun = BasisFun(trial_basis_type)
        self.__test_basis_fun = BasisFun(test_basis_type)

        # 检查 基函数是否符合维数要求
        if self.__trial_basis_fun.is_ok(dim):
            pass
        else:
            logger.error(__file__ + '---' +
                         "the basis function type" + str(trial_basis_type) + " is not allowed for dim " + str(dim))
            exit(0)

        if self.__test_basis_fun.is_ok(dim):
            pass
        else:
            logger.error(__file__ + '---' +
                         "the basis function type" + str(test_basis_type) + " is not allowed for dim " + str(dim))
            exit(0)

        self.__mesh_vtk_file = mesh_vtk_file
        self.__bc_vtk_file = bc_vtk_file
        # 检查输入文件后缀名为vtk
        if self.__mesh_vtk_file.endswith(".vtk"):
            pass
        else:
            logger.error(__file__ + '---' +
                         "input mesh file is only supported vtk")
            exit(0)

        self.__bc_vtk_file = bc_vtk_file
        if self.__bc_vtk_file.endswith(".vtk"):
            pass
        else:
            logger.error(__file__ + '---' +
                         "input boundary mesh file is only supported vtk")
            exit(0)
        logger.info("<<--------BEGIN FEM PROCEDURE---------->>")
        logger.info("STEP 1:input param are prepared and be checked.------------------------------------OK")

    @property
    def dim(self):
        return self.__dim

    @property
    def basis_trial(self):
        return self.__trial_basis_fun

    @property
    def basis_test(self):
        return self.__test_basis_fun

    @property
    def mesh_vtk_file(self):
        return self.__mesh_vtk_file

    @property
    def bc_vtk_file(self):
        return self.__bc_vtk_file


class MeshObject:
    def __init__(self,input_param):
        self.__input_param = input_param
        self.__mesh = pv.read(input_param.mesh_vtk_file)
        self.__boundary = pv.read(input_param.bc_vtk_file)
        # 设置几何单元信息

        self.__num_cells = self.__mesh.n_faces


    @property
    def boundary(self):
        return self.__boundary

    @property
    def input_param(self):
        return self.__input_param

    # 读取points矩阵
    @property
    def points(self):
        return self.__mesh.points

    @property
    def num_of_points(self):
        return self.__mesh.n_points

    def point(self, i):
        return self.__mesh.points[i, :]

    def x(self, i):
        return self.__mesh.points[i, 0]

    def y(self, i):
        return self.__mesh.points[i, 1]

    def z(self, i):
        return self.__mesh.points[i, 2]

    @property
    def faces_list(self):
        return self.__mesh.faces

    @property
    def num_cells(self):
        return self.__num_cells

    # 读取cells 信息和cell的数量
    def set_mesh_grid_cells(self):
        pass

    # 读取边界点指标，边界类型，不同类型对应的值
    def set_boundary_info(self):
        pass

    # 生成fem 的网格矩阵
    def get_fem_mesh(self):
        pass


class KernelObject:
    def __init__(self, mesh, variation_form):
        self.__input_param = mesh.input_param
        self.__mesh = mesh
        self.__variation_form = variation_form
        self.__u_integrator = None
        self.__b_integrator = None

    @property
    def input_param(self):
        return self.__input_param

    @property
    def mesh(self):
        return self.__mesh

    @property
    def variation_form(self):
        return self.__variation_form

    @property
    def u_integrator(self):
        return self.__u_integrator

    @property
    def b_integrator(self):
        return self.__b_integrator

    # 参考基函数到局部时的jacobi函数——trial
    def jacob_trial(self,i,alpha,der_x):
        pass

    # 参考基函数到局部时的jacobi函数——trial
    def jacob_test(self, i, beta,der_x):
        pass

    # 参考基函数的求导后的链式结果 -- trial
    def chain_trial(self,i,alpha,der_x):
        pass

    # 参考基函数的求导后的链式结果 -- test
    def chain_test(self, i, beta,der_x):
        pass

    def u_kernel(self, i, alpha, beta, x):
        pass

    def b_kernel(self, i, beta, x):
        pass

    def set_u_integrator(self):
        pass

    def set_b_integrator(self):
        pass





