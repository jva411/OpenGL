use gl33::{global_loader::{glGetUniformLocation, glUniformMatrix4fv}, GL_FALSE};
use glam::Mat4;

use crate::opengl::types::GLuint;

pub fn set_matrix4fv(program_name: GLuint, uniform_name: &str, mat4: &Mat4) -> Result<(), String> {
  let uniform_location = unsafe {
    glGetUniformLocation(program_name, uniform_name.as_ptr())
  };

  if uniform_location == -1 {
    return Err(format!("Uniform {} not found", uniform_name));
  }

  unsafe {
    glUniformMatrix4fv(
      uniform_location,
      1,
      GL_FALSE.0 as u8,
      mat4.to_cols_array().as_ptr()
    );
  }

  return Ok(());
}
