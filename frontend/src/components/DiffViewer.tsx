import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

export function DiffViewer() {
  return (
    <div className="viewer panel">
      <h3>3D Diff Viewer</h3>
      <Canvas camera={{ position: [40, 40, 40], fov: 45 }}>
        <ambientLight intensity={0.8} />
        <directionalLight position={[20, 20, 10]} intensity={1.2} />
        <mesh position={[-8, 0, 0]}>
          <boxGeometry args={[10, 10, 10]} />
          <meshStandardMaterial color="#4e79a7" transparent opacity={0.35} />
        </mesh>
        <mesh position={[8, 0, 0]}>
          <boxGeometry args={[10, 8, 10]} />
          <meshStandardMaterial color="#e15759" transparent opacity={0.35} />
        </mesh>
        <OrbitControls />
      </Canvas>
      <p className="muted">
        Viewer scaffold is wired for added/removed region overlays; STEP tessellation payload integration is the
        next backend/frontend handshake.
      </p>
    </div>
  );
}
