import type { Metadata } from "next";
import Image from "next/image";
import { copy } from "@/content/copy";

export const metadata: Metadata = {
  title: "بيت العناية",
  description:
    "نوا للبيت علامة سعودية متخصصة في تحسين أجواء البيت والراحة اليومية — تصميم مدروس، جودة، واهتمام بالتفاصيل.",
};

export default function AboutPage() {
  return (
    <>
      {/* Hero — intro + image */}
      <section className="max-w-[1120px] mx-auto px-5 py-16">
        <div className="band">
          <div className="copy flex flex-col justify-center gap-6">
            <p className="text-brass font-semibold text-xs tracking-[0.18em] uppercase">
              {copy.brand.taglineEn}
            </p>
            <h1 className="text-ink">{copy.about.title}</h1>
            <p className="text-ink text-lg leading-relaxed">
              {copy.about.intro}
            </p>
          </div>
          <div
            className="media relative rounded-[20px] overflow-hidden bg-sand"
            style={{ minHeight: "400px" }}
          >
            <Image
              src="/images/about-room.webp"
              alt="غرفة نوا للبيت"
              fill
              className="object-cover"
              sizes="(max-width: 1023px) 100vw, 560px"
            />
          </div>
        </div>
      </section>

      {/* Narrative paragraphs */}
      <section className="max-w-[720px] mx-auto px-5 py-12">
        <div className="flex flex-col gap-5">
          {copy.about.paragraphs.map((para, i) => (
            <p key={i} className="text-muted text-base leading-[1.9]">
              {para}
            </p>
          ))}
        </div>
      </section>

      {/* Pillars grid — the four principles */}
      <section className="bg-ivory border-y border-line">
        <div className="max-w-[1120px] mx-auto px-5 py-16">
          <h2 className="text-center text-ink mb-12">كيف نشتغل</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {copy.about.pillars.map((p) => (
              <div
                key={p.title}
                className="bg-paper rounded-[16px] p-6 border border-line flex flex-col gap-3"
              >
                <div className="flex items-center gap-3">
                  <span
                    className="inline-block w-2 h-2 rounded-full bg-brass"
                    aria-hidden
                  />
                  <h3 className="text-ink font-bold text-lg">{p.title}</h3>
                </div>
                <p className="text-muted text-sm leading-relaxed">{p.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Closing promise band */}
      <section className="max-w-[720px] mx-auto px-5 py-16 text-center">
        <p className="text-brass font-semibold text-xs tracking-[0.18em] uppercase mb-4">
          وعدنا
        </p>
        <p className="text-ink text-xl leading-relaxed font-serif">
          «نختار لكِ ثلاث قطع فقط للبيت، بعد ما نقرأ ورقة كل جهاز. ما نقول إلا اللي
          نضمنه، ونتصل قبل ما يطلع المندوب.»
        </p>
      </section>
    </>
  );
}
