use gl33::{global_loader::{glAttachShader, glCreateProgram, glGetProgramInfoLog, glGetProgramiv, glLinkProgram, glUseProgram}, GL_LINK_STATUS};

use crate::{gl_check, opengl::{shader::Shader, types::GLuint}};

pub struct Program {
    pub name: GLuint,
    pub shaders: Vec<Shader>,
}

impl Program {
    pub fn new(shaders: Vec<Shader>) -> Option<Self> {
        let name = glCreateProgram();

        if name == 0 {
            return None;
        }

        for shader in &shaders {
            glAttachShader(name, shader.name);
        }

        glLinkProgram(name);

        unsafe {
            gl_check!(name, glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS, "Failed to link program");
        }

        return Some(Program { name, shaders });
    }

    pub fn bind(self) -> Self {
        glUseProgram(self.name);
        return self;
    }

    pub fn unbind(&self) {
        glUseProgram(0);
    }
}
