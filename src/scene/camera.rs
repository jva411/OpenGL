use glam::{Mat4, Vec3};

pub struct Camera {
  pub position: Vec3,
  pub rotation: Vec3,
  pub up: Vec3,
  pub fov: f32,
  pub aspect_ratio: f32,
  pub near: f32,
  pub far: f32,
}

impl Camera {
  pub fn new(position: Vec3, rotation: Vec3, up: Vec3, fov: f32, aspect_ratio: f32, near: f32, far: f32) -> Self {
    return Self {
      position,
      rotation,
      up,
      fov,
      aspect_ratio,
      near,
      far,
    };
  }

  pub fn get_view_mat4(&self) -> Mat4 {
    return Mat4::look_to_rh(self.position, self.rotation, self.up);
  }

  pub fn get_projection_mat4(&self) -> Mat4 {
    return Mat4::perspective_rh(self.fov, self.aspect_ratio, self.near, self.far);
    // return Mat4::orthographic_rh(-1.0, 1.0, -1.0, 1.0, self.near, self.far);
  }
}
