from DinoFem import *
"""
FemSolver 类，
输入：
    dim                     维数
    mesh_vtk_file           纯几何信息
    bc_vtk_file             边界信息
    basis_type_trial        trial基函数类型
    basis_type_test         test 基函数类型
    variation_form          变分形式
"""


class FemSolver:
    def __init__(self):
        # 网格和边界信息
        # 几何信息
        self.mesh_vtk_file = None
        self.bc_vtk_file = None
        self.dim = None
        # 有限元网格信息
        self.basis_type_trial = None
        self.basis_type_test = None
        # 有限元网格信息
        self.mesh = None
        # 变分形式
        self.variation_form = None
        # 边界形式
        self.boundary_form = None
        # Ax=b， 边界处理之后的刚度信息
        self.stiff = None
        # 解
        self.__u = None

    # ----------------------------------------------------------------------
    #  基本输入设置
    #    dim                     维数
    #    mesh_vtk_file           纯几何信息
    #   bc_vtk_file             边界信息
    #   basis_type_trial        trial基函数类型
    #   basis_type_test         test 基函数类型
    #   variation_form          变分形式
    # -----------------------------------------------------------------------

    # dim  维数设定
    def set_dim(self, dim):
        self.dim = dim

    # mesh_vtk_file 几何网格输入
    def set_mesh_vtk_file(self, filename):
        self.mesh_vtk_file=filename

    # bc_vtk_file 边界信息输入
    def set_bc_vtk_file(self, filename):
        self.bc_vtk_file=filename

    # basis_type_trial trial基函数类型设定
    def set_basis_type_trial(self, basis_type):
        self.basis_type_trial = basis_type

    # basis_type_trial test基函数类型设定
    def set_basis_type_test(self, basis_type):
        self.basis_type_test = basis_type

    # variation_form 变分形式设定
    def set_variation_form(self, vf):
        self.variation_form = vf

    # boundary_form 边界形式和信息设定
    def set_boundary_form(self, bf):
        self.boundary_form = bf

    # ----------------------------------------------------------------------
    # 有限元计算单元生成
    #
    # 1、生成几何网格，有限元网格，边界信息
    # 2、生成刚度矩阵信息 Ax=b 中的A和b，并进行边界处理
    # -----------------------------------------------------------------------
    def generate_mesh(self):
        geo_mesh = MeshFromVTK(self.mesh_vtk_file,self.bc_vtk_file,self.dim)
        self.mesh = Mesh(mesh_from_vtk=geo_mesh,
                         basis_type_trial=self.basis_type_trial,
                         basis_type_test=self.basis_type_test)

    def assemble_mat_b_bc(self):
        """
        生成StiffMatrix实例
        """
        self.stiff = StiffMatrix(self.mesh, self.variation_form,self.boundary_form)

    # ----------------------------------------------------------------------
    # 求解
    # -----------------------------------------------------------------------
    def solve(self):
        self.__u=direct_inverse(self.stiff.mat,self.stiff.b)

    # ----------------------------------------------------------------------
    # 误差估计
    # -----------------------------------------------------------------------
    def estimate_err(self, exact_solution):
        if self.dim == 1:
            value = 0
            for i in range(len(self.mesh.points)):
                value = max(value, abs(self.u[i]-exact_solution(self.mesh.points[i])))
            return value
        else:
            logger.error(__file__ + "--" + "this form will update later, now  only have the 1 dimension ")
            # TODO
            exit(0)

    # ----------------------------------------------------------------------
    # 属性
    # -----------------------------------------------------------------------
    @property
    def u(self):
        return self.__u
    # ----------------------------------------------------------------------
    #  运行过程
    # -----------------------------------------------------------------------

    def run(self):
        self.generate_mesh()
        self.assemble_mat_b_bc()
        self.solve()



