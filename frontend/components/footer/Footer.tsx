import Link from "next/link";
import { Logo } from "@/components/Logo";
import { copy } from "@/content/copy";

export function Footer() {
  const phone = process.env.NEXT_PUBLIC_CONTACT_PHONE;
  const email = process.env.NEXT_PUBLIC_CONTACT_EMAIL;

  return (
    <footer className="bg-ivory border-t border-line mt-24">
      <div className="max-w-[1120px] mx-auto px-5 py-16">
        {/* Top: brand block + columns */}
        <div className="grid grid-cols-1 md:grid-cols-[1.3fr_1fr_1fr_1fr] gap-10 mb-12">
          {/* Brand block */}
          <div className="flex flex-col gap-4">
            <Logo size="sm" variant="dark" />
            <p className="text-muted text-sm leading-relaxed max-w-[260px]">
              {copy.brand.shortDescAr}
            </p>
            <div className="flex items-center gap-2 pt-1">
              <span className="inline-block w-2 h-2 rounded-full bg-brass" aria-hidden />
              <span className="text-xs text-ink tracking-wide">
                {copy.brand.tagline} · {copy.brand.taglineEn}
              </span>
            </div>
          </div>

          <FooterCol title={copy.footer.shopColumn.title} links={copy.footer.shopColumn.links} />
          <FooterCol title={copy.footer.helpColumn.title} links={copy.footer.helpColumn.links} />

          <div>
            <h4 className="font-bold text-ink mb-4">{copy.footer.contactColumn.title}</h4>
            <div className="flex flex-col gap-2 text-muted text-sm">
              {phone && (
                <a href={`tel:${phone}`} className="hover:text-brand transition-colors">
                  {phone}
                </a>
              )}
              {email && (
                <a href={`mailto:${email}`} className="hover:text-brand transition-colors">
                  {email}
                </a>
              )}
              <span>@nawahouse.sa</span>
              <span className="pt-1">ساعات العمل: ٤ عصرًا – ١١ مساءً</span>
              <span>الرياض</span>
            </div>
          </div>
        </div>

        {/* Bottom row */}
        <div className="border-t border-line pt-6 flex flex-col sm:flex-row justify-between items-center gap-4 text-muted text-sm">
          <span>{copy.brand.copyright}</span>
          <span className="border border-brass text-brass px-4 py-1.5 rounded-full text-xs font-bold tracking-wide">
            {copy.footer.cod}
          </span>
        </div>
      </div>
    </footer>
  );
}

function FooterCol({
  title,
  links,
}: {
  title: string;
  links: readonly { label: string; href: string }[];
}) {
  return (
    <div>
      <h4 className="font-bold text-ink mb-4">{title}</h4>
      <ul className="flex flex-col gap-2">
        {links.map((l) => (
          <li key={l.href}>
            <Link
              href={l.href}
              className="text-muted text-sm hover:text-brand transition-colors"
            >
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
