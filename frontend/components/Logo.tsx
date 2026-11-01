import Link from "next/link";
import { copy } from "@/content/copy";

type LogoVariant = "dark" | "light";

export function Logo({
  size = "md",
  variant = "dark",
}: {
  size?: "sm" | "md";
  variant?: LogoVariant;
}) {
  const circleSize = size === "sm" ? 36 : 44;
  const isLight = variant === "light";
  const circleFill = isLight ? "#F7F5F0" : "#171717";
  const letterFill = isLight ? "#171717" : "#F7F5F0";

  return (
    <Link href="/" className="flex items-center gap-3 no-underline">
      <svg width={circleSize} height={circleSize} viewBox="0 0 44 44" fill="none" aria-hidden="true">
        <circle cx="22" cy="22" r="21" fill={circleFill} stroke="#C5A46D" strokeWidth="1" />
        <text
          x="22"
          y="29"
          textAnchor="middle"
          fontFamily="Outfit, sans-serif"
          fontWeight="600"
          fontSize="20"
          fill={letterFill}
        >
          N
        </text>
      </svg>
      <span className="flex flex-col leading-tight">
        <span className={isLight ? "text-paper" : "text-ink"} style={{ fontSize: size === "sm" ? 16 : 18, fontFamily: "var(--font-serif)" }}>
          {copy.brand.nameAr}
        </span>
        <span
          className={`uppercase ${isLight ? "text-paper/70" : "text-muted"}`}
          style={{ fontFamily: "var(--font-display)", fontSize: "10px", letterSpacing: "0.16em" }}
        >
          {copy.brand.nameEn}
        </span>
      </span>
    </Link>
  );
}
