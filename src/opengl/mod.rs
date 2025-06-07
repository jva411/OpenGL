use beryllium::video::GlWindow;
use gl33::{global_loader::{glClearColor, glEnable, glGetProgramiv,  load_global_gl}, GL_CULL_FACE, GL_DEPTH_TEST, GL_MULTISAMPLE};
use glam::{vec3, vec4, Mat4};

use crate::{objects::{quad::load_quad, triangle::{load_triangle, FRAGMENT_SHADER, VERTEX_SHADER}}, opengl::{program::Program, render_mode::{set_render_mode, RenderMode}, shader::{Shader, ShaderType}, uniform::set_matrix4fv}, scene::camera::Camera};

pub mod buffer;
pub mod program;
pub mod render_mode;
pub mod shader;
pub mod texture;
pub mod types;
pub mod uniform;
pub mod vertex_array;
pub mod vertex;

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


pub fn load_gl(window: &GlWindow) -> (Program, Camera) {
  unsafe {
    load_global_gl(&|name| window.get_proc_address(name));
    glClearColor(0.2, 0.3, 0.3, 1.0);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_MULTISAMPLE);
    glEnable(GL_CULL_FACE);

    load_triangle();
    // load_quad();

    let shaders = vec![
      Shader::new(ShaderType::VERTEX, VERTEX_SHADER.to_string()).expect("Failed to create vertex shader"),
      Shader::new(ShaderType::FRAGMENT, FRAGMENT_SHADER.to_string()).expect("Failed to create fragment shader"),
    ];
    let program = Program::new(shaders).expect("Failed to create program!").bind();
    let camera = load_camera(&program);

    program.shaders.iter().for_each(|shader| shader.delete());

    // set_render_mode(RenderMode::WIRE_FRAME);
    return (program, camera);
  }
}

pub fn set_view(program: &Program, camera: &Camera) {
  set_matrix4fv(program.name, "view\0", &camera.get_view_mat4()).expect("Failed to set view matrix");
}

fn load_camera(program: &Program) -> Camera {
  let camera = Camera::new(
    vec3(0.0, 0.0, 3.0),
    vec3(0.0, 0.0, -1.0),
    vec3(0.0, 1.0, 0.0),
    45.0,
    16.0 / 9.0,
    0.1,
    100.0
  );

  set_matrix4fv(program.name, "projection\0", &camera.get_projection_mat4()).expect("Failed to set projection matrix");
  set_matrix4fv(program.name, "view\0", &camera.get_view_mat4()).expect("Failed to set view matrix");
  let model = Mat4::from_translation(vec3(0.5, 0.5, 0.5));
  set_matrix4fv(program.name, "model\0", &model).expect("Failed to set model matrix");

  return camera;
}
