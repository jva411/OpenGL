use gl33::{global_loader::{glBindBuffer, glGenBuffers}};

use crate::opengl::types::GLuint;

pub mod BufferType {
    use gl33::{GLenum, GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER};

    #[derive(Debug, Clone, Copy)]
    pub struct Type {
        pub gl_type: GLenum
    }

    pub const ARRAY: Type = Type { gl_type: GL_ARRAY_BUFFER };
    pub const ELEMENT_ARRAY: Type = Type { gl_type: GL_ELEMENT_ARRAY_BUFFER };
}

pub struct Buffer {
    pub name: GLuint,
    pub _type: BufferType::Type,
}

impl Buffer {
    pub fn new(buffer_type: BufferType::Type) -> Option<Self> {
        let mut vbo = 0;
        unsafe { glGenBuffers(1, &mut vbo); };

        if vbo == 0 {
            return None;
        }

        return Some(Self { name: vbo, _type: buffer_type });
    }

    pub fn bind(self) -> Self {
        unsafe {
            glBindBuffer(self._type.gl_type, self.name);
        }
        return self;
    }

    pub fn unbind(&self) -> &Self {
        unsafe {
            glBindBuffer(self._type.gl_type, 0);
        }
        return self;
    }
}
