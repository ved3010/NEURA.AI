"use client";

import { useEffect, useRef } from "react";
import { createOrbScene, type OrbSceneApi } from "@/lib/orbScene";

export default function PureSiriOrbPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<OrbSceneApi | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const scene = createOrbScene(container, { pureTransparent: true });
    sceneRef.current = scene;

    return () => {
      scene.dispose();
      sceneRef.current = null;
    };
  }, []);

  return (
    <div className="pure-orb-wrapper">
      <div ref={containerRef} className="pure-orb-canvas" />
    </div>
  );
}
