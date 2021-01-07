"""
组装刚度矩阵
"""
from DinoFem import np, IntegrateSet,logger


class StiffMatrix:
    def __init__(self, kernel):
        self.mesh = kernel.mesh
        self.input = kernel.mesh.input_param
        self.kernel = kernel
        self.num_of_basis = self.mesh.num_of_basis
        self.__mat = np.zeros((self.mesh.num_of_basis, self.mesh.num_of_basis), dtype=float)
        self.__b = np.zeros((self.mesh.num_of_basis, ), dtype=float)
        self.integrator = None
        self.choose_integrator()
        self.assemble_mat()
        self.assemble_b()
        self.treat_boundary_condition()
        logger.info("STEP5:StiffMatrix are prepared and be checked.------------------------------------OK")

    @property
    def dim(self):
        return self.mesh.dim

    def choose_integrator(self):
        def func(i,f):
            p1 = self.mesh.x(self.mesh.cells[i][0])
            p2 = self.mesh.x(self.mesh.cells[i][1])
            return IntegrateSet.integrator("Gauss1D")(f,p1,p2)

        self.integrator = func

    def assemble_mat(self):
        for i in range(self.mesh.num_cells):
            for alpha in range(self.input.basis_trial.phi_num):
                for beta in range(self.input.basis_test.phi_num):
                    f = lambda x: self.kernel.u_kernel(i, alpha, beta, x)
                    r = self.integrator(i, f)
                    k1 = self.mesh.fem_cells_test[i][beta]
                    k2 = self.mesh.fem_cells_trial[i][alpha]
                    self.__mat[k1][k2] += r

    def assemble_b(self):
        for i in range(self.mesh.num_cells):
            for beta in range(self.input.basis_test.phi_num):
                f = lambda x: self.kernel.b_kernel(i, beta, x)
                r = self.integrator(i, f)
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
                self.__b[i] = self.mesh.boundary_value[k]  # (self.mesh.fem_points_trial[i])

    @property
    def mat(self):
        return self.__mat

    @property
    def b(self):
        return self.__b


