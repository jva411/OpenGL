use gl33::{global_loader::glPolygonMode, PolygonMode, GL_FILL, GL_FRONT_AND_BACK, GL_LINE};

pub enum RenderMode {
  COMMON,
  WIRE_FRAME,
}

pub fn set_render_mode(mode: RenderMode) {
  match mode {
    RenderMode::COMMON => set_polygon_mode(GL_FILL),
    RenderMode::WIRE_FRAME => set_polygon_mode(GL_LINE),
  }
}


fn set_polygon_mode(mode: PolygonMode) {
  unsafe {
    glPolygonMode(GL_FRONT_AND_BACK, mode);
  }
}
