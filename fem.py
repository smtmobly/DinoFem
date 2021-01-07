"""
FemSolver 类，
输入：
    dim                     维数
    mesh_vtk_file           纯几何信息
    bc_vtk_file             边界信息
    basis_type_trial        trial基函数类型
    basis_type_test         test 基函数类型
    variation_form          变分形式
    boundary_form           边界形式
"""
from DinoFem import FemMesh,FemKernel,StiffMatrix
from DinoFem import direct_inverse,logger


class FemSolver:
    def __init__(self,input_param):
        self.__input_param = input_param
        self.mesh = FemMesh(self.__input_param)
        # 变分形式
        self.variation_form = None
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

    # variation_form 变分形式设定
    def set_variation_form(self, vf):
        self.variation_form = vf
        logger.info("STEP3:variation_form are prepared and be checked.------------------------------------OK")

    # ----------------------------------------------------------------------
    # 有限元计算单元生成
    #
    # 1、生成几何网格，有限元网格，边界信息
    # 2、生成刚度矩阵信息 Ax=b 中的A和b，并进行边界处理
    # -----------------------------------------------------------------------
    def assemble_mat_b_bc(self):
        """
        生成StiffMatrix实例
        """
        kernel = FemKernel(self.mesh, self.variation_form)
        self.stiff = StiffMatrix(kernel)

    # ----------------------------------------------------------------------
    # 求解
    # -----------------------------------------------------------------------
    def solve(self):
        self.__u = direct_inverse(self.stiff.mat, self.stiff.b)
        logger.info("STEP6:The FEM is solved.------------------------------------------------------------------------OK")
        logger.info(">>--------END FEM PROCEDURE----------<<")
    # ----------------------------------------------------------------------
    # 误差估计
    # -----------------------------------------------------------------------
    def estimate_err(self, exact_solution):
        if self.__input_param.dim == 1:
            value = 0
            for i in range(len(self.mesh.points)):
                value = max(value, abs(self.u[i]-exact_solution(self.mesh.x(i))))
            return value
        else:
            logger.error(__file__ + "--" + "this form will update later, now  only have the 1 dimension ")
            # TODO
            exit(0)
        logger.info(
            "<estimating error>Error Estimated.--------------------------------------------------"
            "----------------------OK")

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
        self.assemble_mat_b_bc()
        self.solve()



