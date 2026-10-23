import type { Metadata, Viewport } from "next";
import { Amiri, IBM_Plex_Sans_Arabic, Outfit } from "next/font/google";
import "./globals.css";
import { SiteShell } from "@/components/SiteShell";

const amiri = Amiri({
  weight: ["400", "700"],
  subsets: ["arabic"],
  variable: "--font-amiri",
  display: "swap",
});

const ibmPlex = IBM_Plex_Sans_Arabic({
  weight: ["400", "500", "700"],
  subsets: ["arabic"],
  variable: "--font-ibm-plex",
  display: "swap",
});

const outfit = Outfit({
  weight: ["400", "600"],
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "نوا للبيت · بيت العناية",
    template: "%s · نوا للبيت",
  },
  description:
    "نوا للبيت · بيت العناية. ثلاث قطع مختارة بعناية للبيت السعودي: مبخرة عود كهربائية، إضاءة شفق، ومنقّي هواء HEPA-13. سعر ثابت، الدفع عند الاستلام.",
  metadataBase: new URL("https://nawahouse.shop"),
  alternates: { canonical: "/" },
  openGraph: {
    siteName: "نوا للبيت · Nawa House",
    locale: "ar_SA",
    type: "website",
  },
};

export const viewport: Viewport = {
  themeColor: "#2C3A2E",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="ar"
      dir="rtl"
      className={`${amiri.variable} ${ibmPlex.variable} ${outfit.variable}`}
    >
      <body className="bg-paper text-ink">
        <SiteShell>{children}</SiteShell>
      </body>
    </html>
  );
}
