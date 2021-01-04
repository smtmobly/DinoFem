"""
变分形式，
所有的变分形式都可以写成两种形式
form_3:int {c(x)* D_ij phi * D_kl psi }dx
form_2:int {b(x)* D_ij phi  }dx

在Fem 类中组装变分形式

"""
from DinoFem import *


class VariationForm:
    """
    A u = b
    u_form 列表存储的是装配到A矩阵的项
    b_form列表存储的是装配到b的项
    """
    def __init__(self):
        self.u_form = []
        self.b_form = []

    def add_u_form(self, form):
        # form3 type
        self.u_form.append(form)

    def add_b_form(self, form):
        # form2 type
        self.b_form.append(form)

    def analysis_variation_form(self, basis_trial, basis_test):
        if basis_trial.dim == 1:

            def kernal_u(p1, p2, alpha, beta,x):
                result=0.0
                for form in self.u_form:
                    diff_x_trial = form.trial_der_order
                    diff_x_test = form.test_der_order
                    result += form.coefficient_function(x)*basis_trial.phi(p1,p2,alpha,diff_x_trial, x)\
                        * basis_test.phi(p1,p2,beta, diff_x_test, x)
                return result

            def kernal_b(p1, p2,  beta,x):
                result=0.0
                for form in self.b_form:
                    diff_x = form.der_order
                    result += form.load_fun(x)*basis_test.phi(p1,p2,beta,diff_x, x)
                return result
            return kernal_u,kernal_b
        else:
            # TODO
            logger.error(__file__ + "--" + "this form will update later, now  only have the 101 basis type")
            exit(0)


class Form2:
    def __init__(self, load_function, der_order=0):
        self.form_order = 2
        self.load_fun = load_function
        if callable(load_function):
            self.load_fun = load_function
        else:
            def func(**kwargs):
                return load_function
            self.load_fun = func
        self.der_order = der_order


class Form3:
    def __init__(self, coefficient_function, trial_der_order, test_der_order):
        self.form_order = 3
        self.coefficient_function = coefficient_function
        if callable(coefficient_function):
            self.coefficient_function = coefficient_function
        else:
            def func(**kwargs):
                return coefficient_function
            self.coefficient_function = func
        self.trial_der_order = trial_der_order
        self.test_der_order = test_der_order


