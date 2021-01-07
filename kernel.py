from DinoFem import KernelObject,logger


class FemKernel(KernelObject):
    def __init__(self, mesh, variation_form):
        super().__init__(mesh, variation_form)
        logger.info("STEP4:Kernels are prepared and be checked.------------------------------------OK")

    def u_kernel(self, i, alpha, beta, x):
        """
        i 对应cells的指标
        :param i:
        :param alpha:

        :param beta:
        :param x:
        :return: 第i个单元中的双线性积分核函数
        """
        result = 0.0
        if self.input_param.dim == 1:
            p1 = self.mesh.x(self.mesh.cells[i][0])
            p2 = self.mesh.x(self.mesh.cells[i][1])
            for form in self.variation_form.u_form:
                trial = self.input_param.basis_trial.phi
                trial_der = form.trial_der
                test = self.input_param.basis_test.phi
                test_der = form.test_der
                result += trial(p1,p2,alpha,trial_der,x)* test(p1,p2,beta,test_der,x)*form.coefficient_function(x)
        return result

    def b_kernel(self, i, beta, x):
        """
        i 对应cells的指标
        :param i:
        :param beta
        :param x:
        :return: 第i个单元中的荷载积分核函数
        """
        result = 0.0
        if self.input_param.dim == 1:
            p1 = self.mesh.x(self.mesh.cells[i][0])
            p2 = self.mesh.x(self.mesh.cells[i][1])
            for form in self.variation_form.b_form:
                test = self.input_param.basis_test.phi
                result += test(p1,p2,beta,0,x)*form.load_fun(x)
        return result
