"use client";
import { useEffect } from "react";
import { PRODUCTS, type Slug } from "@/content/products";
import { trackViewContent } from "@/lib/tracking";
import { sendEvent } from "@/lib/api";

export function ViewContentTracker({ slug }: { slug: Slug }) {
  useEffect(() => {
    const eid = crypto.randomUUID();
    const value = PRODUCTS[slug].price;
    trackViewContent(eid, { value, currency: "MAD", contentIds: [slug], numItems: 1 });
    void sendEvent({ event_name: "ViewContent", event_id: eid, value, currency: "MAD", content_ids: [slug] });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return null;
}
