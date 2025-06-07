use std::thread::sleep;

use beryllium::{events::{Event, SDLK_a as SDLK_A, SDLK_d as SDLK_D, SDLK_s as SDLK_S, SDLK_w as SDLK_W, KMOD_LSHIFT, SDLK_ESCAPE, SDLK_LSHIFT, SDLK_SPACE}, init::InitFlags, video::{CreateWinArgs, GlContextFlags, GlProfile, GlWindow}, Sdl};
use gl33::{global_loader::{glClear, glDrawArrays, glDrawElements}, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRIANGLES, GL_UNSIGNED_INT};

use crate::{opengl::{load_gl, program::Program, set_view}, scene::camera::Camera};

struct Tick {
  tick: u32,
  fps: u64,
  last_frame_time: std::time::Instant,
  elapsed_time: std::time::Duration,
}

impl Tick {
  fn new(fps: u64) -> Tick {
    return Tick {
      tick: 0,
      fps,
      last_frame_time: std::time::Instant::now(),
      elapsed_time: std::time::Duration::from_millis(0),
    }
  }
}

pub struct Window {
  width: i32,
  height: i32,
  title: &'static str,
  sdl: Sdl,
  window: GlWindow,
  tick: Tick,
  program: Program,
  camera: Camera,
}

impl Window {
  pub fn new(width: i32, height: i32, title: &'static str) -> Window {
    let sdl = init_sdl();
    let window = init_window(&sdl, width, height, title);
    let (program, camera) = load_gl(&window);

    return Window {
      width,
      height,
      title,
      sdl,
      window,
      tick: Tick::new(60),
      program,
      camera,
    };
  }

  pub fn loop_step(&mut self) -> Result<(), ()> {
    let render_start = std::time::Instant::now();
    if let Err(_) = self.handle_events() {
      return Err(());
    }

    unsafe {
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glDrawArrays(GL_TRIANGLES, 0, 3);
      // glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0 as *const _);
    }
    self.window.swap_window();

    let render_end = std::time::Instant::now();
    self.tick.tick += 1;
    self.tick.elapsed_time = render_end.duration_since(self.tick.last_frame_time);
    self.tick.last_frame_time = render_end;

    let render_duration = render_end.duration_since(render_start);
    sleep(std::time::Duration::from_millis((1000 / self.tick.fps) - render_duration.as_millis() as u64));

    return Ok(());
  }

  fn handle_events(&mut self) -> Result<(), ()> {
    while let Some(event) = self.sdl.poll_events() {
      match event {
        (Event::Quit, _) => return Err(()),
        (Event::Key { keycode: SDLK_ESCAPE, pressed: false, .. }, _) => return Err(()),
        (Event::Key { .. }, _) => self.kb_event_handle(event.0),
        (Event::MouseMotion { .. }, _) => self.mouse_event_handle(event.0),
        _ => ()
      }
    }

    return Ok(());
  }

  fn mouse_event_handle(&mut self, event: Event) {
    if let Event::MouseMotion { button_state: 4, x_delta, y_delta, .. } = event {
      self.rotate(-y_delta as f32, x_delta as f32);
    }
  }

  fn kb_event_handle(&mut self, event: Event) {
    if let Event::Key { keycode, pressed: true, modifiers, .. } = event {
      println!("{:#?}", keycode);
      let mut right = 0.0;
      let mut forward = 0.0;
      let mut up = 0.0;

      if keycode == SDLK_W { forward += 1.0 };
      if keycode == SDLK_S { forward -= 1.0 };

      if keycode == SDLK_A { right -= 1.0 };
      if keycode == SDLK_D { right += 1.0 };

      if keycode == SDLK_SPACE {
        up += if (modifiers.0 & KMOD_LSHIFT.0) != 0 { -1.0 } else { 1.0 };
      };

      self.translate(right, forward, up);
    }
  }

  fn translate(&mut self, right: f32, forward: f32, up: f32) {
    let speed = 1.5;
    let movement_right = self.tick.elapsed_time.as_secs_f32() * speed * right;
    let movement_forward = self.tick.elapsed_time.as_secs_f32() * speed * forward;
    let movement_up = self.tick.elapsed_time.as_secs_f32() * speed * up;

    self.camera.translate(movement_right, movement_forward, movement_up);

    set_view(&self.program, &self.camera);
  }

  fn rotate(&mut self, x_delta: f32, y_delta: f32) {
    let speed = 3.0;
    let rotation_x = self.tick.elapsed_time.as_secs_f32() * speed * x_delta;
    let rotation_y = self.tick.elapsed_time.as_secs_f32() * speed * y_delta;

    self.camera.rotate_x(rotation_x);
    self.camera.rotate_y(rotation_y);

    set_view(&self.program, &self.camera);
  }
}

fn init_window(sdl: &Sdl, width: i32, height: i32, title: &'static str) -> GlWindow {
  let window_args = CreateWinArgs {
    title,
    width,
    height,
    allow_high_dpi: true,
    borderless: false,
    resizable: false,
  };

  let window = sdl
    .create_gl_window(window_args)
    .unwrap();

  return window;
}

fn init_sdl() -> Sdl {
  let sdl = Sdl::init(InitFlags::EVERYTHING);

  sdl.set_gl_context_major_version(3).unwrap();
  sdl.set_gl_context_minor_version(3).unwrap();
  sdl.set_gl_profile(GlProfile::Core).unwrap();

  let mut flags = GlContextFlags::default();
  if cfg!(target_os = "macos") {
    flags |= GlContextFlags::FORWARD_COMPATIBLE;
  }
  if cfg!(debug_assertions) {
    flags |= GlContextFlags::DEBUG;
  }
  sdl.set_gl_context_flags(flags).unwrap();

  return sdl;
}
