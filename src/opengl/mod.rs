use beryllium::video::GlWindow;
use gl33::{global_loader::{glBufferData, glClearColor, glEnableVertexAttribArray, glVertexAttribPointer, load_global_gl}, GL_ARRAY_BUFFER, GL_FALSE, GL_FLOAT, GL_STATIC_DRAW};

use crate::opengl::{buffer::{Buffer, BufferType}, program::Program, shader::{Shader, ShaderType}, types::Vertex, vertex_array::VertexArray};

mod buffer;
mod program;
mod types;
mod vertex_array;
mod shader;

const TRIANGLE: [Vertex; 3] = [
  [-0.5, -0.5, 0.0],
  [0.5, -0.5, 0.0],
  [0.0, 0.5, 0.0],
];

const VERTEX_SHADER: &str = r#"#version 330 core
  layout (location = 0) in vec3 pos;

  void main() {
    gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
  }
"#;

const FRAGMENT_SHADER: &str = r#"#version 330 core
  out vec4 color;

  void main() {
    color = vec4(1.0, 0.0, 0.0, 1.0);
  }
"#;

#[macro_export]
macro_rules! gl_check {
  ($var: ident, $function1: ident, $function2: ident, $status: ident, $message: expr) => {
    let mut success = 0;
    $function1($var, $status, &mut success);
    if success == 0 {
      let mut log: Vec<u8> = Vec::with_capacity(1024);
      let mut log_length = 0;

      $function2($var, 1024, &mut log_length, log.as_mut_ptr());

      println!("{}: {}", $message, String::from_utf8_lossy(&log));
    }
  };
}


fn load_triangle() {
  unsafe {
    let _vao = VertexArray::new().expect("Failed to create vertex array").bind();
    let _vbo = Buffer::new(BufferType::ARRAY).expect("Failed to create vertex buffer").bind();

    glVertexAttribPointer(
      0,
      3,
      GL_FLOAT,
      GL_FALSE.0 as u8,
      size_of::<Vertex>().try_into().unwrap(),
      0 as *const _,
    );
    glEnableVertexAttribArray(0);

    glBufferData(
      GL_ARRAY_BUFFER,
      size_of_val(&TRIANGLE).try_into().unwrap(),
      TRIANGLE.as_ptr().cast(),
      GL_STATIC_DRAW,
    );
  }
}


pub fn load_gl(window: &GlWindow) {
  unsafe {
    load_global_gl(&|name| window.get_proc_address(name));
    glClearColor(0.2, 0.3, 0.3, 1.0);

    load_triangle();

    let shaders = vec![
      Shader::new(ShaderType::VERTEX, VERTEX_SHADER.to_string()).expect("Failed to create vertex shader"),
      Shader::new(ShaderType::FRAGMENT, FRAGMENT_SHADER.to_string()).expect("Failed to create fragment shader"),
    ];
    let program = Program::new(shaders).expect("Failed to create program!").bind();

    program.shaders.iter().for_each(|shader| shader.delete());
  }
}
