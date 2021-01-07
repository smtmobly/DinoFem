from DinoFem import MeshObject,logger


class FemMesh(MeshObject):
    def __init__(self,input_param):
        super().__init__(input_param)
        self.__cells = None
        # 设置几何边界信息
        self.__boundary_info = None
        self.__boundary_value = None
        self.__num_of_boundary_points = None
        # 设置有限元网格信息
        self.__fem_points_trial = None
        self.__fem_points_test = None
        self.__fem_cells_trial = None
        self.__fem_cells_test = None
        self.set_mesh_grid_cells()
        self.set_boundary_info()
        self.get_fem_mesh()
        logger.info("STEP2:FemMesh are prepared and be checked.------------------------------------OK")


    @property
    def cells(self):
        return self.__cells


    @property
    def fem_points_trial(self):
        return self.__fem_points_trial

    @property
    def fem_points_test(self):
        return self.__fem_points_test

    @property
    def fem_cells_trial(self):
        return self.__fem_cells_trial

    @property
    def fem_cells_test(self):
        return self.__fem_cells_test

    @property
    def num_of_basis(self):
        return self.num_of_points

    @property
    def num_of_bdn(self):
        return self.__num_of_boundary_points

    # 读取cells 信息和cell的数量
    def set_mesh_grid_cells(self):
        faces = self.faces_list
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
        self.__cells = face_list

    # 读取边界点指标，边界类型，不同类型对应的值
    def set_boundary_info(self):
        boundary_point_index = self.boundary.point_arrays['boundary_point_index']
        boundary_type = self.boundary.point_arrays['boundary_type']
        boundary_value = self.boundary.point_arrays['boundary_value']
        boundary_info = []
        for i in range(len(boundary_point_index)):
            boundary_info.append([boundary_type[i], boundary_point_index[i]])

        self.__boundary_info = boundary_info
        self.__boundary_value = boundary_value
        self.__num_of_boundary_points = len(boundary_info)

    def get_fem_mesh(self):
        self.__fem_points_trial = self.points
        self.__fem_points_test = self.points
        self.__fem_cells_trial = self.cells
        self.__fem_cells_test = self.cells
        return

    @property
    def boundary_info(self):
        return self.__boundary_info

    @property
    def boundary_value(self):
        return self.__boundary_value

    @property
    def num_of_boundary_points(self):
        return self.__num_of_boundary_points

    @property
    def basis_points_trial(self):
        return self.__fem_points_trial

    @property
    def basis_points_test(self):
        return self.__fem_points_test

    @property
    def basis_cells_trial(self):
        return self.__fem_cells_trial

    @property
    def basis_cells_test(self):
        return self.__fem_cells_test

