import type { Metadata } from "next";
import { ContactForm } from "./ContactForm";
import { copy } from "@/content/copy";

export const metadata: Metadata = {
  title: "تواصل",
  description: "تواصل مع نوا هاوس.",
};

export default function ContactPage() {
  return (
    <div className="max-w-[640px] mx-auto px-5 py-16">
      <h1 className="mb-3">{copy.contact.title}</h1>
      <p className="text-muted mb-2">{copy.contact.body}</p>
      <p className="text-muted mb-8">{copy.contact.hours} · {copy.contact.city}</p>
      <ContactForm />
    </div>
  );
}
