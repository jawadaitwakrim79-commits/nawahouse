import Link from "next/link";
import { Logo } from "@/components/Logo";
import { copy } from "@/content/copy";

export function Footer() {
  const phone = process.env.NEXT_PUBLIC_CONTACT_PHONE;
  const email = process.env.NEXT_PUBLIC_CONTACT_EMAIL;
  const instagram = process.env.NEXT_PUBLIC_INSTAGRAM_URL || "https://instagram.com/nawahouse";
  const facebook = process.env.NEXT_PUBLIC_FACEBOOK_URL || "https://facebook.com/nawahouse";

  return (
    <footer className="bg-ink text-paper mt-24">
      <div className="max-w-[1180px] mx-auto px-5 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          <div className="flex flex-col gap-4">
            <Logo size="sm" variant="light" />
            <p className="text-paper/70 text-sm leading-relaxed max-w-[260px]">{copy.brand.shortDescAr}</p>
            <p className="text-brass text-xs tracking-[0.14em] uppercase">{copy.brand.taglineEn}</p>
          </div>
          <FooterCol title={copy.footer.shopColumn.title} links={copy.footer.shopColumn.links} />
          <FooterCol title={copy.footer.helpColumn.title} links={copy.footer.helpColumn.links} />
          <div>
            <h4 className="text-sm tracking-wide mb-4">{copy.footer.contactColumn.title}</h4>
            <div className="flex flex-col gap-2 text-paper/70 text-sm">
              {phone && (
                <a href={`tel:${phone}`} className="hover:text-paper" dir="ltr">
                  {phone}
                </a>
              )}
              {email && (
                <a href={`mailto:${email}`} className="hover:text-paper">
                  {email}
                </a>
              )}
              <span>{copy.contact.city}</span>
              <span>{copy.contact.hours}</span>
              <div className="flex gap-4 pt-3">
                <a href={instagram} className="hover:text-brass" target="_blank" rel="noreferrer">
                  Instagram
                </a>
                <a href={facebook} className="hover:text-brass" target="_blank" rel="noreferrer">
                  Facebook
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="border-t border-white/10 pt-6 flex flex-col sm:flex-row justify-between gap-3 text-paper/60 text-sm">
          <span>{copy.brand.copyright}</span>
          <span className="text-brass">{copy.footer.cod}</span>
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
      <h4 className="text-sm tracking-wide mb-4">{title}</h4>
      <ul className="flex flex-col gap-2">
        {links.map((link) => (
          <li key={link.href}>
            <Link href={link.href} className="text-paper/70 text-sm hover:text-paper">
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
