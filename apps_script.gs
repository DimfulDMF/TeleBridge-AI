const SHEET_NAME = "Commands";

// Поставь сюда свой секрет.
// НЕ публикуй настоящий секрет на GitHub.
const BRIDGE_SECRET = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET";

function doGet(e) {
  try {
    const action = e.parameter.action || "";
    const secret = e.parameter.secret || "";

    if (secret !== BRIDGE_SECRET) {
      return json({
        ok: false,
        error: "Unauthorized"
      });
    }

    if (action === "ping") {
      return json({
        ok: true,
        message: "TeleBridge AI online"
      });
    }

    if (action === "pending") {
      const sheet = getSheet();
      const data = sheet.getDataRange().getValues();

      for (let i = 1; i < data.length; i++) {
        const row = data[i];

        const id = row[0];
        const command = row[1];
        const target = row[2];
        const text = row[3];
        const status = row[4];

        if (String(status).toLowerCase() === "pending") {
          // Сразу помечаем команду как взятую.
          sheet.getRange(i + 1, 5).setValue("processing");

          return json({
            ok: true,
            found: true,
            id: String(id),
            command: String(command || ""),
            target: String(target || ""),
            text: String(text || "")
          });
        }
      }

      return json({
        ok: true,
        found: false
      });
    }

    return json({
      ok: false,
      error: "Unknown action"
    });

  } catch (err) {
    return json({
      ok: false,
      error: String(err)
    });
  }
}


function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents || "{}");

    if (body.secret !== BRIDGE_SECRET) {
      return json({
        ok: false,
        error: "Unauthorized"
      });
    }

    const action = body.action || "";

    if (action === "result") {
      const id = String(body.id || "");
      const status = String(body.status || "done");
      const result = String(body.result || "");

      const sheet = getSheet();
      const data = sheet.getDataRange().getValues();

      for (let i = 1; i < data.length; i++) {
        if (String(data[i][0]) === id) {
          sheet.getRange(i + 1, 5).setValue(status);
          sheet.getRange(i + 1, 6).setValue(result);

          return json({
            ok: true
          });
        }
      }

      return json({
        ok: false,
        error: "Command not found"
      });
    }

    return json({
      ok: false,
      error: "Unknown action"
    });

  } catch (err) {
    return json({
      ok: false,
      error: String(err)
    });
  }
}


function getSheet() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  let sheet = spreadsheet.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);

    sheet.appendRow([
      "id",
      "command",
      "target",
      "text",
      "status",
      "result"
    ]);
  }

  return sheet;
}


function json(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}