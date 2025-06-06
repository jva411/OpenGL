use gl33::{global_loader::{glEnableVertexAttribArray, glVertexAttribPointer}, GL_FALSE, GL_FLOAT};

use crate::opengl::types::{GLuint, VEC3_SIZE, VERTEX3_SIZE};

pub fn set_vertex_attribute(index: GLuint) {
  let skip = VEC3_SIZE * (index as usize);

  unsafe {
    glVertexAttribPointer(
      index,
      3,
      GL_FLOAT,
      GL_FALSE.0 as u8,
      VERTEX3_SIZE.try_into().unwrap(),
      skip as *const _,
    );
    glEnableVertexAttribArray(index);
  }
}
