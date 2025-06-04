use gl33::global_loader::{glBindVertexArray, glGenVertexArrays};

use crate::opengl::types::GLuint;

pub struct VertexArray {
    pub name: GLuint
}

impl VertexArray {
    pub fn new() -> Option<Self> {
        let mut vao = 0;
        unsafe { glGenVertexArrays(1, &mut vao); };

        if vao == 0 {
            return None;
        }

        return Some(Self { name: vao });
    }

    pub fn bind(self) -> Self {
        glBindVertexArray(self.name);
        return self;
    }

    pub fn unbind(&self) {
        glBindVertexArray(0);
    }
}
