"""
变分形式，
所有的变分形式都可以写成两种形式
form_3:int {c(x)* D_ij phi * D_kl psi }dx
form_2:int {b(x)* D_ij phi  }dx

在Fem 类中组装变分形式

"""


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


class Form2:
    ORDER = 2

    def __init__(self, load_function):
        """
        标识形式（f,v）
        :param load_function:  加载函数
        """
        self.load_fun = load_function
        if callable(load_function):
            def func(x):
                return load_function(x)
        else:
            def func(x):
                return load_function
        self.load_fun = func


class Form3:
    ORDER = 3

    def __init__(self, coefficient_function, trial_der=1, test_der=1):
        """
        标识形式 (c(x)du/dx,dv/dx)
        记录两个导数阶
        :param coefficient_function:
        :param trial_der:
        :param test_der:
        """
        self.trial_der = trial_der
        self.test_der = test_der
        self.coefficient_function = coefficient_function
        if callable(coefficient_function):
            self.coefficient_function = coefficient_function

            def func(x):
                return coefficient_function(x)

        else:
            def func(**kwargs):
                return coefficient_function
        self.coefficient_function = func


