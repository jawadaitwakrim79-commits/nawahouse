import { goodsTotal, orderTotal, productPrice } from "../lib/pricing";

describe("catalog prices", () => {
  test("atlas is 1490", () => expect(productPrice("atlas")).toBe(1490));
  test("two pieces add", () => {
    expect(goodsTotal([
      { slug: "lune", quantity: 1 },
      { slug: "dune", quantity: 1 },
    ])).toBe(1980);
  });
  test("quantity multiplies", () => {
    expect(goodsTotal([{ slug: "cadre", quantity: 2 }])).toBe(1180);
  });
  test("shipping is added, not invented inside the goods total", () => {
    expect(orderTotal(1490, 0)).toBe(1490);
    expect(orderTotal(1490, 40)).toBe(1530);
  });
});
