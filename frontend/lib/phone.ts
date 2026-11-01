/**
 * Moroccan phone normalisation — browser side.
 * Matches the backend: +212 and a 9-digit national number starting with 5, 6, or 7.
 */

export interface PhoneResult {
  e164: string;
  metaDigits: string;
  tiktokE164: string;
}

const NATIONAL_RE = /^[5-7]\d{8}$/;
const ARABIC_DIGITS: Record<string, string> = {
  "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
  "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9",
  "۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4",
  "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",
};

function toWestern(raw: string): string {
  return raw.replace(/[٠-٩۰-۹]/g, (digit) => ARABIC_DIGITS[digit] ?? digit);
}

export function normalizePhone(raw: string): PhoneResult | null {
  if (!raw) return null;
  let cleaned = toWestern(raw).replace(/[\s\-().]/g, "");
  if (cleaned.startsWith("+")) cleaned = cleaned.slice(1);
  if (cleaned.startsWith("00")) cleaned = cleaned.slice(2);

  let national: string;
  if (cleaned.startsWith("212")) national = cleaned.slice(3);
  else if (cleaned.startsWith("0")) national = cleaned.slice(1);
  else national = cleaned;

  if (!NATIONAL_RE.test(national)) return null;

  const metaDigits = "212" + national;
  const e164 = "+" + metaDigits;
  return { e164, metaDigits, tiktokE164: e164 };
}

export function isValidPhone(raw: string): boolean {
  return normalizePhone(raw) !== null;
}
