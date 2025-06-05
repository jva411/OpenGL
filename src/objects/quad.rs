use gl33::{global_loader::{glEnableVertexAttribArray, glVertexAttribPointer}, GL_FALSE, GL_FLOAT};

use crate::opengl::{buffer::{Buffer, BufferType}, types::{TriIndex, Vertex}, vertex_array::VertexArray};

pub struct Quad {
  pub vertices: [Vertex; 4],
  pub indices: [TriIndex; 2],
}

pub const QUAD: Quad = Quad {
  vertices: [
    [ 0.5,  0.5, 1.0],
    [ 0.5, -0.5, 1.0],
    [-0.5, -0.5, 1.0],
    [-0.5,  0.5, 1.0],
  ],
  indices: [[0, 1, 3], [1, 2, 3]],
};

pub fn load_quad() {
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

  vbo.buffer_data(bytemuck::cast_slice(&QUAD.vertices));

  let ebo = Buffer::new(BufferType::ELEMENT_ARRAY).expect("Failed to create index buffer").bind();
  ebo.buffer_data(bytemuck::cast_slice(&QUAD.indices));
}
