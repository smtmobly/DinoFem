import meshio
import numpy as np


class DinoMesh:
    """
    这是有限元网格处理的基类。必须包含如下
    数据信息：
        points  存储点的坐标信息
        points_size 点的数量信息
        cells  存储 单元信息，对应一个点编号列表
        cells_size 单元数量信息
        boundary_mat 信息，改信息包含3个部分
            - 边界单元所在cell的编号
            - 边界单元的点的编号的列表
        boundary_size 边界上单元的数量
    函数重定义：
        update_boundary_info(self) 设定边界信息矩阵
        set_boundary_ibc(self,bc,btype)  设定不同边界上的边界类型的信息



    1、初始化时只处理网格信息，只设定边界,默认边界值为dirichlet边界条件
    2、边界设定在单独的函数set_boundary中进行
    3、边界条件设定的值，由类变量__boundary_type字典来设定。
        d 代表dirichlet边界
        n 代表neumann边界
        r 代表robin边界

    """
    __boundary_type_keys = ['d', 'n', 'r']
    __boundary_type_values = [-1, -2, -3]
    __boundary_type = dict(zip(__boundary_type_keys, __boundary_type_values))

    def __init__(self):
        self.data = None
        self.faces = []
        self.faces_size=len(self.faces)
        self.volumes = []
        self.volumes_size = len(self.volumes)
        self.boundary_nodes = None
        self.update_boundary_info()

    def update_boundary_info(self):
        pass

    @property
    def boundary_type(self):
        return self.__boundary_type
    @property
    def points(self):
        return

    @property
    def points_size(self):
        return

    @property
    def cells(self):
        return self.volumes

    @property
    def cells_size(self):
        return self.volumes_size

    @property
    def boundary_mat(self):
        return self.boundary_nodes

    @property
    def boundary_size(self):
        return self.faces_size

    def face_list(self, bc):
        return

    def set_boundary_ibc(self, bc, btype):
        pass



