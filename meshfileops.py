"""
本库的网格文件使用vtk数据格式的vtkPolyData类
输入是两个vtk文件，一个vtk给了网格信息，一个vtk给了边界信息
mesh_vtk_file 给了全局的网格信息
bc_vtk_file 给了边界点的信息，同时里面有一个属性“boundary_type”指定了边界的类型。
    /*
    边界条件的bc_type
    Dirichlet   -1
    Neumann     -2
    Robin       -3
    */
同时，有一个boundary_point_index 指出边界点坐标在全局里的位置

vtk都是三维数据。
dim =1 时，只取点的x坐标，y=z=0
dim=2时，只取点的x,y坐标，z=0
dim=3 时，取x,y,z坐标

"""
from DinoFem import *


class MeshFromVTK:
    def __init__(self,mesh_vtk_file=None,bc_vtk_file=None,dim=1):
        """
        生成points矩阵和cells矩阵，生成边界信息矩阵和参数
        :param mesh_vtk_file: 几何信息和剖分之后的网格
        :param bc_vtk_file: 边界信息形成边界网格和属性值
        :param dim:  维数
        """
        self.__dim = None
        if dim in [1, 2, 3]:
            self.__dim = dim
        else:
            logger.error(__file__ + "--" + "dimension should be 1,2,3. wrong dimension input!")
            exit()
        self.__mesh = pv.read(mesh_vtk_file)
        self.__boundary = pv.read(bc_vtk_file)

    # 维数属性值，只读
    @property
    def dim(self):
        return self.__dim

    # 读取points矩阵
    def points(self):
        if self.dim == 1:
            return self.__mesh.points[:, 0]
        elif self.dim == 2:
            return self.__mesh.points[:, 0:2]
        else:
            return self.__mesh.points

    # 读取cells 信息和cell的数量
    def mesh_grid_cells(self):
        faces = self.__mesh.faces
        index = 0
        step = faces[0]
        face_list = []
        for i in range(len(faces)):

            if i == index:
                begin_index = index
                end_index = index + step + 1
                face_list.append(faces[begin_index+1:end_index])
                index = end_index
                if index < len(faces):
                    step = faces[index]
            else:
                pass
        n_faces = len(face_list)
        return face_list, n_faces

    # 读取边界点指标，边界类型，不同类型对应的值
    def boundary_info(self):
        boundary_point_index = self.__boundary.point_arrays['boundary_point_index']
        boundary_type = self.__boundary.point_arrays['boundary_type']
        boundary_info = []
        for i in range(len(boundary_point_index)):
            boundary_info.append([boundary_type[i], boundary_point_index[i]])
        bdn = len(boundary_info)
        return boundary_info, bdn


if __name__ == '__main__':
    mesh_file = "./resources/mesh.vtk"
    boundary_file = "./resources/boundary.vtk"
    msh=MeshFromVTK(mesh_file,boundary_file,1)
    print(msh.points())
    print(msh.mesh_grid_cells())
    print(msh.boundary_info())



