use gl33::{global_loader::{glCompileShader, glCreateShader, glDeleteShader, glGetShaderInfoLog, glGetShaderiv, glShaderSource}, GL_COMPILE_STATUS};

use crate::{gl_check, opengl::types::GLuint};

pub mod ShaderType {
    use gl33::{GLenum, GL_FRAGMENT_SHADER, GL_VERTEX_SHADER};

    #[derive(Debug, Clone, Copy)]
    pub struct Type {
        pub gl_type: GLenum,
    }

    pub const VERTEX: Type = Type { gl_type: GL_VERTEX_SHADER };
    pub const FRAGMENT: Type = Type { gl_type: GL_FRAGMENT_SHADER };
}

pub struct Shader {
    pub name: GLuint,
    pub _type: ShaderType::Type,
    pub source: String,
}

impl Shader {
    pub fn new(_type: ShaderType::Type, source: String) -> Option<Self> {
        let name = glCreateShader(_type.gl_type);

        if name == 0 {
            return None;
        }

        unsafe {
            glShaderSource(
                name,
                1,
                &(source.as_bytes().as_ptr().cast()),
                &(source.len().try_into().unwrap()),
            );
            glCompileShader(name);

            gl_check!(name, glGetShaderiv, glGetShaderInfoLog, GL_COMPILE_STATUS, "Failed to compile shader");
        }

        return Some(Shader { name, _type, source });
    }

    pub fn delete(&self) {
        unsafe {
            glDeleteShader(self.name);
        }
    }
}
