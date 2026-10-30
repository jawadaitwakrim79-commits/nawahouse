import type { Metadata } from "next";
import Image from "next/image";
import { copy } from "@/content/copy";

export const metadata: Metadata = {
  title: "عن نوا هاوس",
  description: "نوا هاوس، ساعات ونظارات في المغرب.",
};

export default function AboutPage() {
  return (
    <section className="max-w-[1180px] mx-auto px-5 py-16">
      <div className="grid lg:grid-cols-2 gap-10 items-center">
        <div className="flex flex-col gap-5">
          <p className="text-brass text-xs tracking-[0.18em] uppercase">{copy.brand.nameEn}</p>
          <h1>{copy.about.title}</h1>
          <p className="text-lg leading-relaxed">{copy.about.intro}</p>
          {copy.about.paragraphs.map((paragraph) => (
            <p key={paragraph} className="text-muted leading-relaxed">
              {paragraph}
            </p>
          ))}
        </div>
        <div className="relative min-h-[420px] bg-sand">
          <Image
            src="/images/about-atelier.jpg"
            alt="ساعة من نوا هاوس"
            fill
            className="object-cover"
            sizes="(max-width: 1024px) 100vw, 560px"
          />
        </div>
      </div>
    </section>
  );
}
