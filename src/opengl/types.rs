// Core types
pub type Vec3 = [f32; 3];
pub type RGB = Vec3;
pub type Vertex2 = [Vec3; 2];
pub type Vertex3 = [Vec3; 3];
pub type TriIndex = [u32; 3];

pub const VEC3_SIZE: usize = size_of::<Vec3>();
pub const VERTEX2_SIZE: usize = size_of::<Vertex2>();
pub const VERTEX3_SIZE: usize = size_of::<Vertex3>();

// OpenGL types
pub type GLuint = u32;
