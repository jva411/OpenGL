use window::Window;

mod objects;
mod opengl;
mod scene;
mod window;

fn main() {
  let mut window = Window::new(800, 450, "Hello, world!");

  main_loop(&mut window);
}

fn main_loop(window: &mut Window) {
  'main_loop: loop {
    match window.loop_step() {
      Ok(_) => (),
      Err(_) => break 'main_loop,
    }
  }
}
