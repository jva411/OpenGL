use gl33::{global_loader::{glBindTexture, glGenTextures, glGenerateMipmap, glTexImage2D}, GL_RGB, GL_TEXTURE_2D, GL_UNSIGNED_BYTE};
use image::{RgbImage};

use crate::opengl::types::GLuint;

pub struct Texture {
  pub name: GLuint,
}

impl Texture {
  pub fn new() -> Option<Self> {
    let mut name = 0;
    unsafe { glGenTextures(1, &mut name) }

    if name == 0 {
      return None;
    }

    return Some(Self { name });
  }

  pub fn bind(&self) {
    unsafe { glBindTexture(GL_TEXTURE_2D, self.name) }
  }

  pub fn load_RGB(&self, image: RgbImage) {
    unsafe {
      glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB.0 as i32,
        image.width() as i32,
        image.height() as i32,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        image.as_ptr() as *const _,
      );
      glGenerateMipmap(GL_TEXTURE_2D);
    };
  }
}
