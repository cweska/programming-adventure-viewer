"use client";

import { useEffect, useState, type ReactNode } from "react";
import type { Scene } from "../lib/lesson/schema";
import { publicPath } from "../lib/site";
import { Torch } from "./Torch";

export function Theater({
  scene,
  caption,
  flareToken,
  focusedImageId,
  stage,
}: {
  scene: Scene;
  caption: string;
  flareToken: number;
  focusedImageId: string | null;
  stage?: ReactNode;
}) {
  const [flaring, setFlaring] = useState(false);

  useEffect(() => {
    if (flareToken === 0) return;
    setFlaring(true);
    const timer = window.setTimeout(() => setFlaring(false), 1400);
    return () => window.clearTimeout(timer);
  }, [flareToken]);

  return (
    <section className="theater" aria-label="Theater">
      <Torch side="left" />
      <div className="frame" data-testid="theater-frame">
        <div className={["stage", flaring ? "is-flaring" : "", stage ? "has-board" : ""].filter(Boolean).join(" ")}>
          {stage ? (
            <div className="board-stage">{stage}</div>
          ) : (
            <div className="collage">
              {scene.images.map((image) => {
                const id = image.id ?? image.src;
                const className = focusedImageId
                  ? id === focusedImageId
                    ? "is-focused"
                    : "is-dimmed"
                  : "";
                return (
                  <figure key={id} className={className} data-image-id={id}>
                    <img src={publicPath(image.src)} alt={image.alt} />
                  </figure>
                );
              })}
            </div>
          )}
          {scene.video ? <video className="scene-video" src={publicPath(scene.video)} controls /> : null}
          {scene.narration || scene.music ? (
            <div className="audio-row">
              {scene.narration ? <audio src={publicPath(scene.narration)} controls aria-label="Narration" /> : null}
              {scene.music ? <audio src={publicPath(scene.music)} controls aria-label="Music" /> : null}
            </div>
          ) : null}
          <div className="caption" data-testid="caption">
            <p>{caption}</p>
          </div>
        </div>
      </div>
      <Torch side="right" />
    </section>
  );
}
