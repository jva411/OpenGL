use glam::{Mat4, Vec3};

pub struct Camera {
  pub position: Vec3,
  pub rotation: Vec3,
  pub up: Vec3,
  pub right: Vec3,
  pub fov: f32,
  pub aspect_ratio: f32,
  pub near: f32,
  pub far: f32,
}

impl Camera {
  pub fn new(position: Vec3, rotation: Vec3, up: Vec3, fov: f32, aspect_ratio: f32, near: f32, far: f32) -> Self {
    let right = rotation.cross(up).normalize();

    return Self {
      position,
      rotation,
      up,
      right,
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

  pub fn translate(&mut self, right: f32, forward: f32, up: f32) {
    self.position += self.right * right + self.rotation * forward + self.up * up;
  }

  pub fn rotate_x(&mut self, degrees: f32) {
    let new_rotation = self.rotation.rotate_towards(self.up, degrees.to_radians()).normalize();
    let new_right = new_rotation.cross(self.up).normalize();

    self.rotation = new_rotation;
    self.right = new_right;
  }

  pub fn rotate_y(&mut self, degrees: f32) {
    let new_rotation = self.rotation.rotate_towards(self.right, degrees.to_radians()).normalize();
    let new_up = self.right.cross(new_rotation).normalize();

    self.rotation = new_rotation;
    self.up = new_up;
  }
}
