import Link from "next/link";

type LogoVariant = "dark" | "light";

/**
 * Nawa House wordmark + "N" circle monogram.
 *
 * - `dark` variant (default): deep olive circle with ivory N — for light headers / footers.
 * - `light` variant: ivory circle with olive N — for the transparent header over the hero.
 */
export function Logo({
  size = "md",
  variant = "light",
}: {
  size?: "sm" | "md";
  variant?: LogoVariant;
}) {
  const circleSize = size === "sm" ? 36 : 44;
  const fontSize = size === "sm" ? 18 : 22;

  const isLight = variant === "light";
  const circleFill = isLight ? "#F3EDE4" : "#2C3A2E";
  const circleStroke = isLight ? "#2C3A2E" : "none";
  const letterFill = isLight ? "#2C3A2E" : "#F3EDE4";

  return (
    <Link href="/" className="flex items-center gap-3 no-underline">
      {/* N monogram */}
      <svg
        width={circleSize}
        height={circleSize}
        viewBox="0 0 44 44"
        fill="none"
        aria-hidden="true"
      >
        <circle
          cx="22"
          cy="22"
          r={isLight ? 21 : 22}
          fill={circleFill}
          stroke={circleStroke}
          strokeWidth={isLight ? 1.5 : 0}
        />
        <text
          x="22"
          y="30"
          textAnchor="middle"
          fontFamily="Outfit, sans-serif"
          fontWeight="600"
          fontSize="24"
          fill={letterFill}
        >
          N
        </text>
      </svg>

      {/* Wordmark */}
      <span className="flex flex-col leading-tight">
        <span
          className="text-ink"
          style={{ fontSize: `${fontSize}px`, fontFamily: "var(--font-serif)" }}
        >
          نوا للبيت
        </span>
        <span
          className="text-muted tracking-widest uppercase"
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "11px",
            letterSpacing: "0.12em",
          }}
        >
          Nawa House
        </span>
      </span>
    </Link>
  );
}
