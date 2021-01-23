import meshio
import numpy as np
from DinoFem.fem3d.meshbase import DinoMesh


class Inp2mesh(DinoMesh):
    """
    1、初始化时只处理网格信息，只设定边界,默认边界值为dirichlet边界条件
    2、边界设定在单独的函数set_boundary中进行
    3、边界条件设定的值，由类变量__boundary_type字典来设定。
        d 代表dirichlet边界
        n 代表neumann边界
        r 代表robin边界
    """

    def __init__(self, inp_file):
        super().__init__()
        self.data = meshio.read(inp_file)
        self.faces = self.data.get_cells_type("triangle")
        self.faces_size=len(self.faces)
        self.volumes = self.data.get_cells_type('tetra')
        self.volumes_size = len(self.volumes)
        self.boundary_nodes = np.zeros((self.faces_size, 5))
        self.update_boundary_info()

    def update_boundary_info(self):
        for i in range(self.faces_size):
            for j in range(self.volumes_size):
                if all([e in self.volumes[j] for e in self.faces[i]]):
                    self.boundary_nodes[i, 0] = -1
                    self.boundary_nodes[i, 1] = j
                    self.boundary_nodes[i, 2:] = self.faces[i]

    @property
    def points(self):
        return self.data.points

    @property
    def points_size(self):
        return len(self.data.points)

    @property
    def cells(self):
        return self.volumes

    @property
    def cells_size(self):
        return self.volumes_size

    @property
    def boundary(self):
        return  self.boundary_nodes

    @property
    def boundary_element_size(self):
        return self.faces_size

    def face_list(self, bc):
        return self.data.cell_sets_dict[bc]['triangle']

    def set_boundary_ibc(self,bc,btype):
        value = self.boundary_type[btype]
        for i in self.face_list(bc):
            self.boundary_nodes[i,0]=value


if __name__ == '__main__':
    a=Inp2mesh("../resources/fem_test003.inp")
    a.set_boundary_ibc('face1','n')
    a.set_boundary_ibc('face2', 'r')
    print(a.boundary_nodes)
    print(a.boundary_nodes[a.boundary_nodes[:, 0] == -1, :])
