"""
-d/dx( exp(x)*du/dx )
=
-exp(x)*(cos(x)-2*sin(x)-x*cos(x)-x*sin(x))

变分形式
exp(x)*du/dx*dv/dx = -exp(x)*(cos(x)-2*sin(x)-x*cos(x)-x*sin(x))*v

在有限元中u是trial， v 是test
边界条件
u(0)=0
u(1)=cos(1)

精确解
u=x*cos(x)
"""
from DinoFem.fem1d import *
import math
# -------------------------------------------------
#  准备mesh_vtk_file,bc_vtk_file
# --------------------------------------------------


class Solver:
    def __init__(self, a, b, N, dim, trial_type, test_type):
        # self.fem_solver = FemSolver()
        # self.fem_solver.set_dim(dim)

        mesh_vtk_file, bc_vtk_file = generate_vtk_file(a, b, N)
        self.input = InputParam(1,
                                101,
                                101,
                                mesh_vtk_file,
                                bc_vtk_file)
        # 生成求解器，并生成网格信息
        self.fem_solver = FemSolver(self.input)

        self.vf = None
        self.set_vp()
        self.fem_solver.set_variation_form(self.vf)
        self.fem_solver.assemble_mat_b_bc()
        self.fem_solver.solve()
        self.err = self.fem_solver.estimate_err(self.exact_solution)

    def check_geo_mesh(self):
        print("check mesh")
        print(self.fem_solver.mesh.points)
        print(self.fem_solver.mesh.cells)
        print(self.fem_solver.mesh.fem_points_trial)
        print(self.fem_solver.mesh.fem_cells_trial)

    def check_variation_form(self):
        print("check variation form")
        basis = BasisFun(101)
        print(basis.dim)
        kernal_u,kernal_b = self.vf.analysis_variation_form(basis, basis)
        print(kernal_u(0,1,0,0,0))
        print(kernal_b(0,1,0,0))

    def check_stiff(self):
        print(self.fem_solver.stiff.mat)
        print(self.fem_solver.stiff.b)

    @staticmethod
    def b_fun(x):
        return x*math.cos(1)

    @staticmethod
    def coeff(x):
        return math.exp(x)

    @staticmethod
    def load_function(x):
        return -math.exp(x)*(math.cos(x)-2*math.sin(x)-x*math.cos(x)-x*math.sin(x))

    @staticmethod
    def exact_solution(x):
        return x*math.cos(x)

    def set_vp(self):
        """
        exp(x)*du/dx*dv/dx = -exp(x)*(cos(x)-2*sin(x)-x*cos(x)-x*sin(x))*v
        """
        vp = VariationForm()
        vp.add_u_form(Form3(self.coeff))
        vp.add_b_form(Form2(self.load_function))
        self.vf = vp


def generate_vtk_file(a, b, N):
    L=b-a
    h=L/N
    n_points = N+1
    n_cells = N
    # ---------------------
    #  生成mesh_vtk
    # ---------------------
    # mesh points
    vertices = np.zeros((n_points,3),dtype=float)
    for i in range(n_points):
        xi = a + i*h
        vertices[i, :] = [xi, 0, 0]

    # mesh faces
    faces = np.zeros((n_cells, 3), dtype=int)
    for i in range(n_cells):
        faces[i, :] = [2, i, i+1]

    surf = pv.PolyData(vertices, faces)
    # -------------------------
    # 生成 bc_vtk
    # -------------------------
    # 定义点
    boundary_nodes = surf.points[[0, -1]]
    # 定义 边界类型
    f = np.zeros((2, 1))
    f[0] = -1
    f[-1] = -1
    # 定义边界点在全局的点指标映射
    boundary_point_index = np.zeros((2, 1))
    boundary_point_index[0] = 0
    boundary_point_index[1] = N
    # 定义边界点的取值
    g = np.zeros((2, 1))
    g[0] = 0
    g[1] = math.cos(1)
    # 生成基础网格
    b = pv.PolyData(pv.PolyData(boundary_nodes))
    # 生成 boundary_type属性值
    b.point_arrays['boundary_type'] = f
    # 生成 boundary_point_index 属性值
    b.point_arrays['boundary_point_index'] = boundary_point_index
    # 生成 boundary_value 属性值
    b.point_arrays['boundary_value'] = g
    # -------------------------
    # 生成 mesh_vtk_file,bc_vtk_file
    # -------------------------

    b.save("boundary.vtk")
    surf.save("mesh.vtk")
    return "mesh.vtk","boundary.vtk"


def show():
    surf = pv.read("mesh.vtk")
    b = pv.read("boundary.vtk")
    p = pv.Plotter(shape=(2, 2))
    p.subplot(0, 0)
    p.add_mesh(surf, show_edges=True)
    p.add_mesh(pv.PolyData(surf.points), color='red', point_size=10, show_edges=True)
    p.subplot(0, 1)
    p.add_mesh(b, point_size=10, show_edges=True, scalars="boundary_point_index")
    p.subplot(1, 0)
    p.add_mesh(b, point_size=10, show_edges=True, scalars="boundary_type")
    p.subplot(1, 1)
    p.add_mesh(b, point_size=10, show_edges=True, scalars="boundary_value")
    p.show()


if __name__ == '__main__':
    nerr=[]
    for i in range(6):
        n=2**(i+2)
        s=Solver(0,1,n,1,101,101)
        nerr.append(s.err)
    norder =[]
    for i in range(5):
        norder.append(math.log2(nerr[i]/nerr[i+1]))
    print('%-10.10s' % "err", '      ', '%-10.10s' % "order")
    print('%-10.10f' % nerr[0])
    for i in range(5):
        print('%-10.10f' % nerr[i+1], '    ', '%-10.10f' % norder[i])
