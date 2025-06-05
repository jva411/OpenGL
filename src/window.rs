use beryllium::{events::{Event, SDLK_ESCAPE}, init::InitFlags, video::{CreateWinArgs, GlContextFlags, GlProfile, GlWindow}, Sdl};
use gl33::{global_loader::{glClear, glDrawArrays, glDrawElements}, GL_COLOR_BUFFER_BIT, GL_TRIANGLES, GL_UNSIGNED_INT};

use crate::opengl::load_gl;

pub struct Window {
  width: i32,
  height: i32,
  title: &'static str,
  sdl: Sdl,
  window: GlWindow,
}

impl Window {
  pub fn new(width: i32, height: i32, title: &'static str) -> Window {
    let sdl = init_sdl();
    let window = init_window(&sdl, width, height, title);
    load_gl(&window);

    return Window {
      width,
      height,
      title,
      sdl,
      window,
    };
  }

  pub fn loop_step(&self) -> Result<(), ()> {
    if let Err(_) = self.handle_events() {
      return Err(());
    }

    unsafe {
      glClear(GL_COLOR_BUFFER_BIT);
      glDrawArrays(GL_TRIANGLES, 0, 3);
      // glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0 as *const _);
    }
    self.window.swap_window();

    return Ok(());
  }

  fn handle_events(&self) -> Result<(), ()> {
    while let Some(event) = self.sdl.poll_events() {
      match event {
        (Event::Quit, _) => return Err(()),
        (Event::Key { keycode: SDLK_ESCAPE, pressed: false, .. }, _) => return Err(()),
        _ => ()
      }
    }

    return Ok(());
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
