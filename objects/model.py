import os
import numpy as np
from objects.mesh import Mesh
from objects.object import Object
from utils.textures import Textures
from utils.transform import Transform
from utils.material import Material, BLANK

class Model(Object):
    def __init__(self, path: str, transform: Transform = None):
        super().__init__(transform)
        self.is_compound = True
        self.meshes: list[Mesh] = []
        self.load_model(path)

    def load_model(self, path: str):
        directory = os.path.dirname(path)
        vertices, normals, texcoords = [], [], []
        faces = []
        materials: dict[str, Material] = {}
        current_material = None

        with open(path, 'r') as f:
            for line in f:
                if line.startswith('mtllib'):
                    mtl_path = os.path.join(directory, line.split()[1])
                    materials = self.load_mtl(mtl_path)
                elif line.startswith('v '):
                    vertices.append(list(map(float, line.split()[1:])))
                elif line.startswith('vn '):
                    normals.append(list(map(float, line.split()[1:])))
                elif line.startswith('vt '):
                    texcoords.append(list(map(float, line.split()[1:3])))
                elif line.startswith('usemtl'):
                    current_material = line.split()[1]
                elif line.startswith('f '):
                    face_data = line.split()[1:]
                    for i in range(len(face_data) - 2):
                        face = [face_data[0], face_data[i+1], face_data[i+2]]
                        faces.append((face, current_material))

        # Dicionário para agrupar vértices e índices por material
        mesh_data = {}

        # Dicionário para cachear vértices únicos e evitar duplicação
        vertex_cache = {}

        for face, material_name in faces:
            if material_name not in mesh_data:
                mesh_data[material_name] = {'vertices': [], 'indices': []}

            current_mesh = mesh_data[material_name]

            for vertex_str in face:
                # Se o vértice já foi processado, reutilize seu índice
                if vertex_str in vertex_cache and vertex_cache[vertex_str]['material'] == material_name:
                    current_mesh['indices'].append(vertex_cache[vertex_str]['index'])
                    continue

                # --- INÍCIO DA CORREÇÃO ---
                # Analisa os componentes da face (v, vt, vn) de forma robusta
                parts = vertex_str.split('/')
                v_idx = int(parts[0]) - 1
                vt_idx = int(parts[1]) - 1 if len(parts) > 1 and parts[1] else -1
                vn_idx = int(parts[2]) - 1 if len(parts) > 2 and parts[2] else -1
                # --- FIM DA CORREÇÃO ---

                # Constrói o vértice com os dados disponíveis
                vertex_data = []
                vertex_data.extend(vertices[v_idx])
                vertex_data.extend(normals[vn_idx] if vn_idx != -1 and normals else [0, 0, 0])
                vertex_data.extend(texcoords[vt_idx] if vt_idx != -1 and texcoords else [0, 0])

                # Adiciona o novo vértice à lista e ao cache
                new_index = len(current_mesh['vertices'])
                current_mesh['vertices'].append(vertex_data)
                current_mesh['indices'].append(new_index)
                vertex_cache[vertex_str] = {'index': new_index, 'material': material_name}

        # Cria os objetos Mesh para cada material
        for material_name, data in mesh_data.items():
            # Achata a lista de vértices para o buffer
            flat_vertices = [item for sublist in data['vertices'] for item in sublist]
            final_vertices = np.array(flat_vertices, dtype=np.float32)
            final_indices = np.array(data['indices'], dtype=np.uint32)

            material = materials.get(material_name, BLANK.copy())

            self.meshes.append(Mesh(final_vertices, final_indices, transform=self.transform, material=material))

    def load_mtl(self, path: str):
        materials: dict[str, Material] = {}
        current_material = None
        directory = os.path.dirname(path)

        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('newmtl'):
                    current_material = line.split()[1]
                    materials[current_material] = BLANK.copy()
                elif line.startswith('map_Kd') and current_material:
                    # Extrai o caminho da textura do arquivo .mtl
                    path_in_mtl = line.split(maxsplit=1)[1].strip()

                    # Pega apenas o nome do arquivo, ignorando o caminho absoluto
                    texture_filename = os.path.basename(path_in_mtl)

                    # Monta o caminho local, assumindo que a textura está na mesma pasta do .mtl
                    local_texture_path = os.path.join(directory, texture_filename)

                    # Se o arquivo não for encontrado, tenta trocar a extensão para .png
                    if not os.path.exists(local_texture_path):
                        base_name, _ = os.path.splitext(local_texture_path)
                        png_path = base_name + '.png'
                        if os.path.exists(png_path):
                            local_texture_path = png_path

                    # Tenta carregar a textura. Se o arquivo ainda não existir, o material ficará sem textura.
                    try:
                        specular_path = local_texture_path # Simplificação, usando a mesma textura para especular
                        materials[current_material].textures = Textures(local_texture_path, specular_path)
                    except Exception as e:
                        print(f"Aviso: Não foi possível carregar a textura '{local_texture_path}'. Erro: {e}")

                elif line.startswith('Ns') and current_material:
                    materials[current_material].shininess = float(line.split()[1])
                elif line.startswith('Kd') and current_material:
                    materials[current_material].diffuse = np.array(list(map(float, line.split()[1:])), dtype=np.float32)
                elif line.startswith('Ks') and current_material:
                    materials[current_material].specular = np.array(list(map(float, line.split()[1:])), dtype=np.float32)

        return materials

    def tick(self):
        super().tick()
        for mesh in self.meshes:
            mesh.tick()

    def __iter__(self):
        return iter(self.meshes)
