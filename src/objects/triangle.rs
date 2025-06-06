use std::{env::current_dir, fs::File};

use crate::opengl::{buffer::{Buffer, BufferType}, texture::Texture, types::Vertex3, vertex::set_vertex_attribute, vertex_array::VertexArray};

const TRIANGLE: [Vertex3; 3] = [
  // [[x, y, z], [r, g, b], [s, t, r]]
  [[-0.5, -0.5, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
  [[ 0.5, -0.5, 0.0], [0.0, 1.0, 0.0], [5.0, 0.0, 0.0]],
  [[ 0.0,  0.5, 0.0], [0.0, 0.0, 1.0], [2.5, 5.0, 0.0]],
];

pub const VERTEX_SHADER: &str = r#"#version 330 core
  layout (location = 0) in vec3 pos;
  layout (location = 1) in vec3 color;
  layout (location = 2) in vec3 aTextCoord;

  out vec3 vertexColor;
  out vec2 textCoord;

  uniform mat4 model;
  uniform mat4 view;
  uniform mat4 projection;

  void main() {
    gl_Position = projection * view * model * vec4(pos, 1.0);
    vertexColor = color;
    textCoord = aTextCoord.st;
  }
"#;

pub const FRAGMENT_SHADER: &str = r#"#version 330 core
  in vec3 vertexColor;
  in vec2 textCoord;

  out vec4 outColor;

  uniform sampler2D texture1;

  void main() {
    outColor = texture(texture1, textCoord);
  }
"#;

pub fn load_triangle() {
  let _vao = VertexArray::new().expect("Failed to create vertex array").bind();
  let vbo = Buffer::new(BufferType::ARRAY).expect("Failed to create vertex buffer").bind();

  set_vertex_attribute(0);
  set_vertex_attribute(1);
  set_vertex_attribute(2);

  vbo.buffer_data(bytemuck::cast_slice(&TRIANGLE));

  let texture = Texture::new().expect("Failed to create texture");
  texture.bind();
  texture.load_RGB(image::open("assets/textures/wall_bricks.jpg").unwrap().to_rgb8());
}
