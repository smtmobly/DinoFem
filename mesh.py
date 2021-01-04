"""
Mesh类需要从meshfile文件中读取，后续有限元计算所需要的点，单元和边界信息。
"""
from DinoFem import *
# from DinoFem.basis_function_set import BasisFun


class Mesh:
    """
    从MeshFromVtk的实例中获取网格信息，并根据设定的不同基函数类型，生成有限元计算的点和单元信息
    """
    def __init__(self,mesh_from_vtk,basis_type_trial=None,basis_type_test=None,basis_type=None):
        """
        :param mesh_from_vtk: 输入MeshFromVTK的实例
        :param basis_type_trial: 设定trial的基函数类
        :param basis_type_test:  设定test的基函数类
        :param basis_type:        该参数设定之后，basis_type_trial和basis_type_test认为是一样的，全部设定为basis_type
        """
        self.__mesh_from_vtk = mesh_from_vtk
        # -------------------------------------------------------------
        # 网格和边界信息
        # -------------------------------------------------------------
        self.__points = None
        self.__grid_cells = None
        self.__boundary_info = None
        # 单元个数
        self._num_of_cells = None
        # 边界点个数
        self._num_of_bdn = None
        self.get_geo_mesh()
        # --------------------------------------------------------------
        # 有限元所使用的基函数信息
        # -------------------------------------------------------------
        if basis_type is not None:
            self._basis_type_trial = basis_type
            self._basis_type_test = basis_type
        else:
            self._basis_type_trial = basis_type_trial
            self._basis_type_test = basis_type_test

        self._basis_trial = None
        self._basis_test = None
        self._num_of_basis = None
        self.get_basis_function_info()

        # --------------------------------------------------------------
        # 有限元使用的节点和单元信息
        # -------------------------------------------------------------
        self.__fem_points_trial = None
        self.__fem_points_test = None
        self.__fem_cells_trial = None
        self.__fem_cells_test = None
        self.get_fem_mesh()

    # 设定网格点矩阵points
    # 设定网格cell 矩阵 grid_cells，网格cell的个数 num_of_cells
    # 设定边界信息boundary_info, 边界点个数，
    def get_geo_mesh(self):
        self.__points = self.__mesh_from_vtk.points()
        self.__grid_cells, self._num_of_cells = self.__mesh_from_vtk.mesh_grid_cells()
        self.__boundary_info, self._num_of_bdn = self.__mesh_from_vtk.boundary_info()
        return

    def get_basis_function_info(self):
        self._basis_trial = BasisFun(self._basis_type_trial)
        self._basis_test = BasisFun(self._basis_type_test)
        self._num_of_basis = self._num_of_cells+1
        return

    def get_fem_mesh(self):
        self.__fem_points_trial = self.points
        self.__fem_points_test = self.points
        self.__fem_cells_trial = self.grid_cells
        self.__fem_cells_test = self.grid_cells
        return

    @property
    def points(self):
        return self.__points

    @property
    def grid_cells(self):
        return self.__grid_cells

    @property
    def boundary_info(self):
        return self.__boundary_info

    @property
    def num_of_basis(self):
        return self._num_of_basis

    @property
    def num_of_cells(self):
        return self._num_of_cells

    @property
    def num_of_bdn(self):
        return self._num_of_bdn

    @property
    def basis_trial(self):
        return self._basis_trial

    @property
    def basis_test(self):
        return self._basis_test

    @property
    def fem_points_trial(self):
        return self.__fem_points_trial

    @property
    def fem_points_test(self):
        return self.__fem_points_test

    @property
    def fem_cells_trial(self):
        return self.__fem_cells_trial

    @property
    def fem_cells_test(self):
        return self.__fem_cells_test




