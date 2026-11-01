import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ProductCard } from "@/components/product/ProductCard";
import { copy } from "@/content/copy";
import { BESTSELLERS, CATEGORIES, NEW_ARRIVALS, REVIEWS } from "@/content/products";

export const metadata: Metadata = {
  title: "ساعات ونظارات",
  description: "نوا هاوس. ساعات ونظارات في المغرب، والأسعار بالدرهم، والدفع عند الاستلام.",
};

export default function HomePage() {
  return (
    <>
      <section className="max-w-[1180px] mx-auto px-5 pt-8 pb-16 lg:pt-14">
        <div className="grid lg:grid-cols-[1.05fr_0.95fr] gap-6 lg:gap-10 items-stretch min-h-[70vh]">
          <div className="flex flex-col justify-end lg:justify-center gap-6 order-2 lg:order-1 py-6">
            <p className="text-brass text-xs tracking-[0.22em] uppercase">{copy.hero.eyebrow}</p>
            <h1 className="text-ink max-w-[12ch]">{copy.hero.headline}</h1>
            <p className="text-muted text-lg max-w-[440px] leading-relaxed">{copy.hero.sub}</p>
            <div className="flex flex-wrap gap-3">
              <Link href="/shop" className="inline-flex items-center bg-ink text-paper px-7 py-3 text-sm tracking-wide min-h-[48px]">
                {copy.hero.cta}
              </Link>
              <Link href="#categories" className="inline-flex items-center border border-ink px-7 py-3 text-sm min-h-[48px]">
                {copy.hero.secondary}
              </Link>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3 order-1 lg:order-2 min-h-[320px]">
            <div className="relative overflow-hidden bg-sand">
              <Image src="/images/hero-watch.jpg" alt="ساعة من مجموعة نوا هاوس" fill priority className="object-cover" sizes="40vw" />
            </div>
            <div className="relative overflow-hidden bg-sand mt-8">
              <Image src="/images/hero-sun.jpg" alt="نظارة شمسية من مجموعة نوا هاوس" fill className="object-cover" sizes="40vw" />
            </div>
          </div>
        </div>
      </section>

      <section id="categories" className="max-w-[1180px] mx-auto px-5 py-16">
        <h2 className="text-center mb-10">تسوّق حسب الفئة</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {CATEGORIES.map((category) => (
            <Link key={category.slug} href={category.href} className="lift group">
              <div className="relative bg-sand overflow-hidden" style={{ aspectRatio: "3/4" }}>
                <Image src={category.image} alt={category.nameAr} fill className="object-cover transition-transform duration-500 group-hover:scale-[1.03]" sizes="280px" />
              </div>
              <p className="mt-3 text-center text-sm tracking-wide">{category.nameAr}</p>
            </Link>
          ))}
        </div>
      </section>

      <section className="max-w-[1180px] mx-auto px-5 py-8">
        <div className="flex items-end justify-between mb-8">
          <h2>الأكثر طلباً</h2>
          <Link href="/shop" className="text-sm text-muted hover:text-ink">المتجر</Link>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-10">
          {BESTSELLERS.map((slug) => (
            <ProductCard key={slug} slug={slug} />
          ))}
        </div>
      </section>

      <section className="max-w-[1180px] mx-auto px-5 py-16">
        <h2 className="mb-8">وصل حديثاً</h2>
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-10">
          {NEW_ARRIVALS.map((slug) => (
            <ProductCard key={slug} slug={slug} />
          ))}
        </div>
      </section>

      <section className="max-w-[1180px] mx-auto px-5 py-8">
        <h2 className="mb-8">{copy.collections.title}</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <CollectionCard
            href={copy.collections.watches.href}
            title={copy.collections.watches.title}
            image="/images/collections/watches.jpg"
            alt="مجموعة الساعات"
          />
          <CollectionCard
            href={copy.collections.eyewear.href}
            title={copy.collections.eyewear.title}
            image="/images/collections/eyewear.jpg"
            alt="مجموعة النظارات"
          />
        </div>
      </section>

      <section className="bg-ivory border-y border-line">
        <div className="max-w-[1180px] mx-auto px-5 py-16">
          <h2 className="text-center mb-10">{copy.why.title}</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {copy.why.items.map((item) => (
              <div key={item.title}>
                <h3 className="text-base mb-2">{item.title}</h3>
                <p className="text-muted text-sm leading-relaxed">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-[1180px] mx-auto px-5 py-16">
        <h2 className="text-center mb-10">{copy.reviewsTitle}</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {REVIEWS.map((review) => (
            <figure key={review.author} className="border border-line p-6">
              <blockquote className="text-ink leading-relaxed">«{review.text}»</blockquote>
              <figcaption className="text-muted text-sm mt-4">
                {review.author} · {review.city}
              </figcaption>
            </figure>
          ))}
        </div>
      </section>
    </>
  );
}

function CollectionCard({ href, title, image, alt }: { href: string; title: string; image: string; alt: string }) {
  return (
    <Link href={href} className="relative block min-h-[280px] overflow-hidden bg-sand group">
      <Image src={image} alt={alt} fill className="object-cover transition-transform duration-700 group-hover:scale-[1.03]" sizes="(max-width: 768px) 100vw, 560px" />
      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
      <span className="absolute bottom-6 start-6 text-paper text-2xl font-serif">{title}</span>
    </Link>
  );
}
