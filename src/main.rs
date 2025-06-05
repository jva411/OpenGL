use window::Window;

mod window;
mod opengl;
mod objects;

fn main() {
  let window = Window::new(1280, 720, "Hello, world!");

  main_loop(&window);
}

fn main_loop(window: &Window) {
  'main_loop: loop {
    match window.loop_step() {
      Ok(_) => (),
      Err(_) => break 'main_loop,
    }
  }
}
