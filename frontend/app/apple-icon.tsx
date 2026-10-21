import { ImageResponse } from "next/og";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

/**
 * Apple touch icon — Nawa House "N" monogram.
 * Larger size, square with slight rounded corners (iOS handles the mask).
 */
export default function AppleIcon() {
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
          fontSize: 118,
          fontWeight: 600,
          fontFamily: "Outfit, sans-serif",
        }}
      >
        N
      </div>
    ),
    { ...size }
  );
}
