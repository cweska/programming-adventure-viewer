import { memo } from "react";
import type { Tile } from "../../lib/game/schema";

export const TILE = 48;

type Palette = Record<"grass" | "path" | "sand" | "floor" | "canopy" | "rock" | "wood" | "water" | "roof", string>;

const PALETTES: Record<"night" | "day", Palette> = {
  night: {
    grass: "#1f3a2a",
    path: "#4a4636",
    sand: "#5a5040",
    floor: "#5b4632",
    canopy: "#143022",
    rock: "#59606b",
    wood: "#5a3a22",
    water: "#1d3557",
    roof: "#3a2438",
  },
  day: {
    grass: "#5f9e4a",
    path: "#c8b27a",
    sand: "#e0c98f",
    floor: "#a07850",
    canopy: "#2f6b34",
    rock: "#8a8f96",
    wood: "#8b5a2b",
    water: "#3d7cc9",
    roof: "#7a3b2e",
  },
};

function ground(tile: Tile, palette: Palette): string {
  switch (tile) {
    case "path":
    case "door":
      return palette.path;
    case "sand":
      return palette.sand;
    case "floor":
      return palette.floor;
    case "water":
      return palette.water;
    case "wall":
    case "window":
      return palette.wood;
    case "roof":
      return palette.roof;
    default:
      return palette.grass;
  }
}

function Decoration({ tile, palette, sky }: { tile: Tile; palette: Palette; sky: "night" | "day" }) {
  const half = TILE / 2;
  switch (tile) {
    case "flowers":
      return (
        <g>
          <circle cx={12} cy={14} r={3} fill="#e7a6ff" />
          <circle cx={32} cy={22} r={3} fill="#ffe08a" />
          <circle cx={18} cy={34} r={3} fill="#ffe08a" />
          <circle cx={36} cy={38} r={3} fill="#e7a6ff" />
        </g>
      );
    case "tree":
      return (
        <g>
          <rect x={half - 4} y={28} width={8} height={16} fill="#4a2f1a" />
          <circle cx={half} cy={20} r={17} fill={palette.canopy} stroke="#0b1a10" strokeWidth={2} />
          <circle cx={half - 6} cy={15} r={6} fill="#ffffff" opacity={0.08} />
        </g>
      );
    case "rock":
      return <ellipse cx={half} cy={30} rx={16} ry={12} fill={palette.rock} stroke="#2b3138" strokeWidth={2} />;
    case "fence":
      return (
        <g stroke={palette.wood} strokeWidth={5}>
          <path d={`M4 ${half - 8} H${TILE - 4} M4 ${half + 8} H${TILE - 4}`} />
          <path d={`M10 6 V${TILE - 4} M${TILE - 10} 6 V${TILE - 4}`} />
        </g>
      );
    case "water":
      return (
        <path
          d="M6 18 q 6 -5 12 0 t 12 0 t 12 0 M6 34 q 6 -5 12 0 t 12 0 t 12 0"
          stroke="#7fb2e5"
          strokeOpacity={0.6}
          strokeWidth={2}
          fill="none"
        />
      );
    case "wall":
      return <path d="M0 12 H48 M0 24 H48 M0 36 H48" stroke="#2a190d" strokeWidth={2} opacity={0.7} />;
    case "roof":
      return (
        <path d="M0 16 H48 M0 32 H48 M12 0 V16 M36 16 V32 M12 32 V48" stroke="#1d121d" strokeWidth={2} opacity={0.6} />
      );
    case "window":
      return (
        <g>
          <rect
            x={10}
            y={10}
            width={28}
            height={26}
            fill={sky === "night" ? "#ffcf6b" : "#bfe3ff"}
            stroke="#2a190d"
            strokeWidth={4}
          />
          <path d="M24 10 V36 M10 23 H38" stroke="#2a190d" strokeWidth={3} />
        </g>
      );
    case "door":
      return (
        <g>
          <rect
            x={8}
            y={0}
            width={32}
            height={48}
            fill={sky === "night" ? "#ffcf6b" : "#6b4528"}
            stroke="#2a190d"
            strokeWidth={4}
          />
          {sky === "night" ? <rect x={8} y={0} width={32} height={48} fill="#ffcf6b" opacity={0.35} /> : null}
        </g>
      );
    default:
      return null;
  }
}

export const MapTiles = memo(function MapTiles({ tiles, sky }: { tiles: Tile[][]; sky: "night" | "day" }) {
  const palette = PALETTES[sky];
  return (
    <g aria-hidden="true">
      {tiles.map((row, y) =>
        row.map((tile, x) => (
          <g key={`${x},${y}`} transform={`translate(${x * TILE} ${y * TILE})`} data-tile={tile}>
            <rect width={TILE} height={TILE} fill={ground(tile, palette)} />
            <Decoration tile={tile} palette={palette} sky={sky} />
            <rect width={TILE} height={TILE} fill="none" stroke="#000000" strokeOpacity={0.12} />
          </g>
        )),
      )}
    </g>
  );
});
