"""
组装刚度矩阵
"""
from DinoFem import *


class StiffMatrix:
    def __init__(self, mesh,variation_form,boundary_form):
        self.mesh = mesh
        self.num_of_basis = mesh.num_of_basis
        self.__mat = np.zeros((mesh.num_of_basis, mesh.num_of_basis), dtype=float)
        self.__b = np.zeros((mesh.num_of_basis, ), dtype=float)
        self.variation_form = variation_form
        self.boundary_form = boundary_form
        self.kernal_u = None
        self.kernal_b = None
        self.integrator = None

        self.choose_integrator()
        self.analysis_variation_form()
        self.assemble_mat()
        self.assemble_b()
        self.treat_boundary_condition()

    def analysis_variation_form(self):
        self.kernal_u, self.kernal_b = \
            self.variation_form.analysis_variation_form(self.mesh.basis_trial, self.mesh.basis_test)

    def choose_integrator(self):
        self.integrator = IntegrateSet.choice_integrator("Gauss")

    def assemble_mat(self):
        for i in range(self.mesh.num_of_cells):
            for alpha in range(self.mesh.basis_trial.num_of_local_basis_fun):
                for beta in range(self.mesh.basis_test.num_of_local_basis_fun):
                    p1 = self.mesh.points[self.mesh.grid_cells[i][0]]
                    p2 = self.mesh.points[self.mesh.grid_cells[i][1]]
                    f = lambda x: self.kernal_u(p1, p2, alpha, beta, x)
                    r = self.integrator(f, p1, p2)
                    k1 = self.mesh.fem_cells_test[i][beta]
                    k2 = self.mesh.fem_cells_trial[i][alpha]
                    self.__mat[k1][k2] += r

    def assemble_b(self):
        for i in range(self.mesh.num_of_cells):
            for beta in range(self.mesh.basis_test.num_of_local_basis_fun):
                p1 = self.mesh.points[self.mesh.grid_cells[i][0]]
                p2 = self.mesh.points[self.mesh.grid_cells[i][1]]
                f = lambda x: self.kernal_b(p1, p2, beta, x)
                r = self.integrator(f, p1, p2)
                k = self.mesh.fem_cells_test[i][beta]
                self.__b[k] += r

    # 处理边界条件
    def treat_boundary_condition(self):
        for k in range(self.mesh.num_of_bdn):
            if self.mesh.boundary_info[k][0] == -1:
                i = self.mesh.boundary_info[k][1]
                i=int(i)
                self.__mat[i][:] = 0
                self.__mat[i][i] = 1
                # g是边界的值
                self.__b[i] = self.boundary_form[-1](self.mesh.fem_points_trial[i])

    @property
    def mat(self):
        return self.__mat

    @property
    def b(self):
        return self.__b


