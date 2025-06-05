use gl33::{global_loader::{glEnableVertexAttribArray, glVertexAttribPointer}, GL_FALSE, GL_FLOAT};

use crate::opengl::{buffer::{Buffer, BufferType}, types::Vertex, vertex_array::VertexArray};

const TRIANGLE: [Vertex; 3] = [
  [-0.5, -0.5, 1.0],
  [ 0.5, -0.5, 1.0],
  [ 0.0,  0.5, 0.0],
];

pub const VERTEX_SHADER: &str = r#"#version 330 core
  layout (location = 0) in vec3 pos;

  out vec4 vertexColor;

  void main() {
    gl_Position = vec4(pos, 1.0);
    vertexColor = vec4((pos.x * -2.0) + pos.z, (pos.y * 2.0) + pos.z, (pos.x * 2.0) + pos.z, 1.0);
  }
"#;

pub const FRAGMENT_SHADER: &str = r#"#version 330 core
  in vec4 vertexColor;
  out vec4 outColor;

  void main() {
    outColor = vertexColor;
  }
"#;

pub fn load_triangle() {
  let _vao = VertexArray::new().expect("Failed to create vertex array").bind();
  let vbo = Buffer::new(BufferType::ARRAY).expect("Failed to create vertex buffer").bind();

  unsafe {
    glVertexAttribPointer(
      0,
      3,
      GL_FLOAT,
      GL_FALSE.0 as u8,
      size_of::<Vertex>().try_into().unwrap(),
      0 as *const _,
    );
    glEnableVertexAttribArray(0);
  }

  vbo.buffer_data(bytemuck::cast_slice(&TRIANGLE));
}
