import { ImageResponse } from "next/og";

export const size = { width: 64, height: 64 };
export const contentType = "image/png";

/**
 * Dynamic favicon — Nawa House "N" monogram on olive apothecary green.
 * Served at /icon and used by browsers as favicon.ico fallback.
 */
export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          background: "#2C3A2E",
          color: "#F3EDE4",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 42,
          fontWeight: 600,
          fontFamily: "Outfit, sans-serif",
          borderRadius: "50%",
        }}
      >
        N
      </div>
    ),
    { ...size }
  );
}
