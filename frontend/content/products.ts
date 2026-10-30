export type CategorySlug =
  | "mens-watches"
  | "womens-watches"
  | "sunglasses"
  | "optical";

export type Slug =
  | "atlas"
  | "noir"
  | "lune"
  | "perle"
  | "dune"
  | "soleil"
  | "cadre"
  | "ligne";

export interface ProductColor {
  id: string;
  label: string;
  swatch: string;
}

export interface WatchSpecs {
  kind: "watch";
  caseMaterial: string;
  strapMaterial: string;
  movement: string;
  color: string;
  style: string;
}

export interface EyewearSpecs {
  kind: "eyewear";
  frameShape: string;
  frameMaterial: string;
  frameColor: string;
  lens: string;
  sizes: string;
}

export interface ProductData {
  slug: Slug;
  nameAr: string;
  fullNameAr: string;
  category: CategorySlug;
  audience: "men" | "women" | "unisex";
  oneLine: string;
  description: string;
  price: number;
  badge: "bestseller" | "new" | null;
  colors: ProductColor[];
  specs: WatchSpecs | EyewearSpecs;
  imageSrcs: string[];
  related: Slug[];
}

export const CATEGORIES: { slug: CategorySlug; nameAr: string; image: string; href: string }[] = [
  {
    slug: "mens-watches",
    nameAr: "ساعات رجالية",
    image: "/images/products/noir.jpg",
    href: "/shop?category=mens-watches",
  },
  {
    slug: "womens-watches",
    nameAr: "ساعات نسائية",
    image: "/images/products/lune.jpg",
    href: "/shop?category=womens-watches",
  },
  {
    slug: "sunglasses",
    nameAr: "نظارات شمسية",
    image: "/images/products/dune.jpg",
    href: "/shop?category=sunglasses",
  },
  {
    slug: "optical",
    nameAr: "إطارات طبية",
    image: "/images/products/cadre.jpg",
    href: "/shop?category=optical",
  },
];

export const PRODUCTS: Record<Slug, ProductData> = {
  atlas: {
    slug: "atlas",
    nameAr: "أطلس",
    fullNameAr: "ساعة أطلس الرجالية",
    category: "mens-watches",
    audience: "men",
    oneLine: "علبة فولاذية، سوار جلد، وحركة كوارتز هادئة.",
    description:
      "أطلس ساعة يومية بخطوط نظيفة. العلبة من الفولاذ المقاوم للصدأ، والسوار من الجلد، والميناء أسود بقراءة واضحة.",
    price: 1490,
    badge: "bestseller",
    colors: [
      { id: "black", label: "أسود", swatch: "#171717" },
      { id: "brown", label: "بني", swatch: "#6B4A32" },
    ],
    specs: {
      kind: "watch",
      caseMaterial: "فولاذ مقاوم للصدأ",
      strapMaterial: "جلد",
      movement: "كوارتز",
      color: "أسود",
      style: "كلاسيكي",
    },
    imageSrcs: ["/images/products/atlas.jpg"],
    related: ["noir", "dune", "lune"],
  },
  noir: {
    slug: "noir",
    nameAr: "نوار",
    fullNameAr: "ساعة نوار الرجالية",
    category: "mens-watches",
    audience: "men",
    oneLine: "حركة أوتوماتيك وسوار فولاذي وميناء أسود.",
    description:
      "نوار للذين يفضّلون حضوراً أهدأ من الشعارات. علبة وسوار من الفولاذ، حركة أوتوماتيك، وميناء أسود.",
    price: 1890,
    badge: "bestseller",
    colors: [
      { id: "black", label: "أسود", swatch: "#171717" },
      { id: "silver", label: "فضي", swatch: "#C8C6C2" },
    ],
    specs: {
      kind: "watch",
      caseMaterial: "فولاذ مقاوم للصدأ",
      strapMaterial: "سوار فولاذي",
      movement: "أوتوماتيك",
      color: "أسود",
      style: "رياضي أنيق",
    },
    imageSrcs: ["/images/products/noir.jpg"],
    related: ["atlas", "dune", "perle"],
  },
  lune: {
    slug: "lune",
    nameAr: "لون",
    fullNameAr: "ساعة لون النسائية",
    category: "womens-watches",
    audience: "women",
    oneLine: "ميناء شامبانيا وسوار جلد لساعة سهرة رفيعة.",
    description:
      "لون ساعة صغيرة القياس بميناء بلون الشامبانيا وسوار جلد. مناسبة للسهرة كما لليوم الهادئ.",
    price: 1290,
    badge: "bestseller",
    colors: [
      { id: "champagne", label: "شامبانيا", swatch: "#C5A46D" },
      { id: "white", label: "أبيض", swatch: "#F7F5F0" },
    ],
    specs: {
      kind: "watch",
      caseMaterial: "فولاذ مقاوم للصدأ",
      strapMaterial: "جلد",
      movement: "كوارتز",
      color: "شامبانيا",
      style: "سهرة",
    },
    imageSrcs: ["/images/products/lune.jpg"],
    related: ["perle", "soleil", "cadre"],
  },
  perle: {
    slug: "perle",
    nameAr: "بيرل",
    fullNameAr: "ساعة بيرل النسائية",
    category: "womens-watches",
    audience: "women",
    oneLine: "سوار شبكي معدني وميناء فضي بسيط.",
    description:
      "بيرل ساعة رفيعة بسوار شبكي. الخطوط قليلة، والقراءة مباشرة، واللون فضي أو ذهبي وردي.",
    price: 990,
    badge: "new",
    colors: [
      { id: "silver", label: "فضي", swatch: "#C8C6C2" },
      { id: "rose", label: "ذهبي وردي", swatch: "#C4A484" },
    ],
    specs: {
      kind: "watch",
      caseMaterial: "فولاذ مقاوم للصدأ",
      strapMaterial: "شبك معدني",
      movement: "كوارتز",
      color: "فضي",
      style: "بسيط",
    },
    imageSrcs: ["/images/products/perle.jpg"],
    related: ["lune", "soleil", "ligne"],
  },
  dune: {
    slug: "dune",
    nameAr: "دون",
    fullNameAr: "نظارة دون الشمسية",
    category: "sunglasses",
    audience: "men",
    oneLine: "إطار أسيتات مستطيل وعدسات داكنة بحماية UV400.",
    description:
      "دون نظارة شمسية رجالية بشكل مستطيل. الإطار من الأسيتات، والعدسات داكنة بحماية UV400.",
    price: 690,
    badge: "bestseller",
    colors: [
      { id: "black", label: "أسود", swatch: "#171717" },
      { id: "havana", label: "هافانا", swatch: "#8A5A32" },
    ],
    specs: {
      kind: "eyewear",
      frameShape: "مستطيل",
      frameMaterial: "أسيتات",
      frameColor: "أسود",
      lens: "عدسات داكنة، حماية UV400",
      sizes: "مقاس موحّد",
    },
    imageSrcs: ["/images/products/dune.jpg"],
    related: ["soleil", "noir", "cadre"],
  },
  soleil: {
    slug: "soleil",
    nameAr: "سولاي",
    fullNameAr: "نظارة سولاي الشمسية",
    category: "sunglasses",
    audience: "women",
    oneLine: "شكل عين القطة وإطار أسيتات بعدسات UV400.",
    description:
      "سولاي نظارة شمسية نسائية بشكل عين القطة. الإطار من الأسيتات، والعدسات بحماية UV400.",
    price: 720,
    badge: "new",
    colors: [
      { id: "havana", label: "هافانا", swatch: "#8A5A32" },
      { id: "black", label: "أسود", swatch: "#171717" },
    ],
    specs: {
      kind: "eyewear",
      frameShape: "عين القطة",
      frameMaterial: "أسيتات",
      frameColor: "هافانا",
      lens: "حماية UV400",
      sizes: "مقاس موحّد",
    },
    imageSrcs: ["/images/products/soleil.jpg"],
    related: ["dune", "lune", "cadre"],
  },
  cadre: {
    slug: "cadre",
    nameAr: "كادر",
    fullNameAr: "إطار كادر الطبي",
    category: "optical",
    audience: "unisex",
    oneLine: "إطار أسيتات مستطيل يُركَّب عليه قياس النظر.",
    description:
      "كادر إطار طبي مستطيل من الأسيتات. يصل بعدسات تجريبية تُستبدل بعدسة طبية عند البصريات.",
    price: 590,
    badge: null,
    colors: [
      { id: "black", label: "أسود", swatch: "#171717" },
      { id: "havana", label: "هافانا", swatch: "#8A5A32" },
    ],
    specs: {
      kind: "eyewear",
      frameShape: "مستطيل",
      frameMaterial: "أسيتات",
      frameColor: "أسود",
      lens: "عدسات تجريبية، تُستبدل بعدسة طبية",
      sizes: "52-18-145",
    },
    imageSrcs: ["/images/products/cadre.jpg"],
    related: ["ligne", "dune", "atlas"],
  },
  ligne: {
    slug: "ligne",
    nameAr: "لين",
    fullNameAr: "إطار لين الطبي",
    category: "optical",
    audience: "unisex",
    oneLine: "إطار معدني دائري خفيف لعدسة طبية.",
    description:
      "لين إطار دائري من المعدن. خفيف على الوجه، ويصل بعدسات تجريبية جاهزة للاستبدال بعدسة النظر.",
    price: 540,
    badge: "new",
    colors: [
      { id: "gold", label: "ذهبي", swatch: "#C5A46D" },
      { id: "silver", label: "فضي", swatch: "#C8C6C2" },
    ],
    specs: {
      kind: "eyewear",
      frameShape: "دائري",
      frameMaterial: "معدن",
      frameColor: "ذهبي",
      lens: "عدسات تجريبية، تُستبدل بعدسة طبية",
      sizes: "48-20-140",
    },
    imageSrcs: ["/images/products/ligne.jpg"],
    related: ["cadre", "perle", "soleil"],
  },
};

export const PRODUCTS_ARRAY = Object.values(PRODUCTS);

export const BESTSELLERS: Slug[] = ["noir", "lune", "dune", "atlas"];
export const NEW_ARRIVALS: Slug[] = ["perle", "soleil", "ligne"];

export const REVIEWS = [
  {
    text: "الساعة وصلت كما في الصورة، والدفع كان عند الاستلام في الدار البيضاء.",
    author: "يوسف",
    city: "الدار البيضاء",
  },
  {
    text: "إطار كادر خفيف. ركّبت عليه عدستي الطبية عند البصريات بدون مشكلة.",
    author: "سلمى",
    city: "الرباط",
  },
  {
    text: "نظارة دون واضحة في شمس مراكش، والتغليف كان مرتباً.",
    author: "أمين",
    city: "مراكش",
  },
];

export function categoryName(slug: CategorySlug): string {
  return CATEGORIES.find((category) => category.slug === slug)?.nameAr ?? slug;
}

export function isSlug(value: string): value is Slug {
  return value in PRODUCTS;
}
