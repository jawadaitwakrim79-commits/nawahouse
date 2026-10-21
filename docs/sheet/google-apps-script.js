/**
 * Paste this file into the Google Sheet bound script.
 * Deploy as a Web App, execute as Me, access Anyone.
 * Script property WEBHOOK_SECRET must match the backend SHEET_WEBHOOK_SECRET.
 *
 * Apps Script drops most custom headers, so the secret travels in the JSON body.
 */
var COLUMNS = [
  "order_id",
  "created_at_riyadh",
  "status",
  "customer_name",
  "phone_e164",
  "phone_local",
  "items",
  "main_units",
  "upsell_accepted",
  "upsell_slug",
  "total_sar",
  "currency",
  "payment_method",
  "page_url",
  "event_id",
  "fbp",
  "fbc",
  "ttclid",
  "ttp",
  "sc_click_id",
  "client_ip",
  "user_agent",
  "city",
  "district",
  "address",
  "landmark",
  "call_attempts",
  "call_notes",
  "confirmed_at",
  "shipped_at",
  "delivered_at",
  "cancel_reason",
];

function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);
    var expected = PropertiesService.getScriptProperties().getProperty("WEBHOOK_SECRET");
    if (!expected || body.secret !== expected) {
      return json({ ok: false, error: "unauthorized" });
    }
    if (!body.order_id) {
      return json({ ok: false, error: "missing order_id" });
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    var header = sheet.getRange(1, 1, 1, COLUMNS.length).getValues()[0];
    if (String(header[0]) !== "order_id") {
      sheet.getRange(1, 1, 1, COLUMNS.length).setValues([COLUMNS]);
    }

    var last = sheet.getLastRow();
    if (last >= 2) {
      var existing = sheet.getRange(2, 1, last - 1, 1).getValues();
      for (var i = 0; i < existing.length; i++) {
        if (String(existing[i][0]) === String(body.order_id)) {
          return json({ ok: true, duplicate: true });
        }
      }
    }

    var row = COLUMNS.map(function (key) {
      if (key === "call_attempts") return body[key] || 0;
      var value = body[key];
      return value === undefined || value === null ? "" : value;
    });
    sheet.appendRow(row);
    return json({ ok: true, duplicate: false });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
