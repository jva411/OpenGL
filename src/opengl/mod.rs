use beryllium::video::GlWindow;
use gl33::global_loader::{glClearColor, load_global_gl};

use crate::{objects::{quad::load_quad, triangle::{load_triangle, FRAGMENT_SHADER, VERTEX_SHADER}}, opengl::{program::Program, render_mode::{set_render_mode, RenderMode}, shader::{Shader, ShaderType}}};

pub mod buffer;
pub mod render_mode;
pub mod program;
pub mod types;
pub mod vertex_array;
pub mod shader;

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


pub fn load_gl(window: &GlWindow) {
  unsafe {
    load_global_gl(&|name| window.get_proc_address(name));
    glClearColor(0.2, 0.3, 0.3, 1.0);

    load_triangle();
    // load_quad();

    let shaders = vec![
      Shader::new(ShaderType::VERTEX, VERTEX_SHADER.to_string()).expect("Failed to create vertex shader"),
      Shader::new(ShaderType::FRAGMENT, FRAGMENT_SHADER.to_string()).expect("Failed to create fragment shader"),
    ];
    let program = Program::new(shaders).expect("Failed to create program!").bind();

    program.shaders.iter().for_each(|shader| shader.delete());

    // set_render_mode(RenderMode::WIRE_FRAME);
  }
}
