const SHEET_NAME = "Commands";
const SECRET_PROPERTY = "TELEBRIDGE_SECRET";


function doGet(e) {
  try {
    const action = String(e.parameter.action || "");
    const secret = String(e.parameter.secret || "");

    if (action === "ping") {
      checkSecret(secret);

      return jsonResponse({
        ok: true,
        message: "TeleBridge AI connected"
      });
    }

    if (action === "pending") {
      checkSecret(secret);
      return getPendingCommand();
    }

    return jsonResponse({
      ok: false,
      error: "Unknown action"
    });

  } catch (error) {
    return jsonResponse({
      ok: false,
      error: String(error.message || error)
    });
  }
}


function doPost(e) {
  try {
    let body = {};

    try {
      body = JSON.parse(e.postData.contents || "{}");
    } catch (error) {
      return jsonResponse({
        ok: false,
        error: "Invalid JSON"
      });
    }

    const action = String(body.action || "");

    if (action === "setup") {
      return setupBridge(body);
    }

    if (action === "result") {
      checkSecret(String(body.secret || ""));
      return saveResult(body);
    }

    return jsonResponse({
      ok: false,
      error: "Unknown action"
    });

  } catch (error) {
    return jsonResponse({
      ok: false,
      error: String(error.message || error)
    });
  }
}


function setupBridge(body) {
  const newSecret = String(body.secret || "");

  if (!newSecret) {
    return jsonResponse({
      ok: false,
      error: "Secret is empty"
    });
  }

  if (newSecret.length < 32) {
    return jsonResponse({
      ok: false,
      error: "Secret is too short"
    });
  }

  const properties = PropertiesService.getScriptProperties();

  const existingSecret = properties.getProperty(
    SECRET_PROPERTY
  );

  if (existingSecret) {
    return jsonResponse({
      ok: false,
      error: "Bridge already configured"
    });
  }

  properties.setProperty(
    SECRET_PROPERTY,
    newSecret
  );

  return jsonResponse({
    ok: true,
    message: "Bridge configured"
  });
}


function checkSecret(secret) {
  const savedSecret = PropertiesService
    .getScriptProperties()
    .getProperty(SECRET_PROPERTY);

  if (!savedSecret) {
    throw new Error(
      "Bridge is not configured"
    );
  }

  if (!secret || secret !== savedSecret) {
    throw new Error(
      "Unauthorized"
    );
  }

  return true;
}


function getSheet() {
  const spreadsheet =
    SpreadsheetApp.getActiveSpreadsheet();

  if (!spreadsheet) {
    throw new Error(
      "Spreadsheet not found"
    );
  }

  let sheet = spreadsheet.getSheetByName(
    SHEET_NAME
  );

  if (!sheet) {
    sheet = spreadsheet.insertSheet(
      SHEET_NAME
    );
  }

  const expectedHeaders = [
    "id",
    "command",
    "target",
    "text",
    "status",
    "result"
  ];

  const currentHeaders = sheet
    .getRange(1, 1, 1, 6)
    .getValues()[0];

  let headersCorrect = true;

  for (let i = 0; i < expectedHeaders.length; i++) {
    if (
      String(currentHeaders[i]).trim() !==
      expectedHeaders[i]
    ) {
      headersCorrect = false;
      break;
    }
  }

  if (!headersCorrect) {
    sheet
      .getRange(1, 1, 1, 6)
      .setValues([expectedHeaders]);
  }

  return sheet;
}


function getPendingCommand() {
  const lock =
    LockService.getScriptLock();

  lock.waitLock(10000);

  try {
    const sheet = getSheet();

    const lastRow = sheet.getLastRow();

    if (lastRow < 2) {
      return jsonResponse({
        ok: true,
        found: false
      });
    }

    const values = sheet
      .getRange(
        2,
        1,
        lastRow - 1,
        6
      )
      .getValues();

    for (let i = 0; i < values.length; i++) {
      const row = values[i];

      const id = String(row[0] || "");
      const command = String(row[1] || "");
      const target = String(row[2] || "");
      const text = String(row[3] || "");
      const status = String(row[4] || "")
        .trim()
        .toLowerCase();

      if (status === "pending") {
        const sheetRow = i + 2;

        sheet
          .getRange(sheetRow, 5)
          .setValue("processing");

        SpreadsheetApp.flush();

        return jsonResponse({
          ok: true,
          found: true,
          id: id,
          command: command,
          target: target,
          text: text
        });
      }
    }

    return jsonResponse({
      ok: true,
      found: false
    });

  } finally {
    lock.releaseLock();
  }
}


function saveResult(body) {
  const id = String(body.id || "");

  if (!id) {
    return jsonResponse({
      ok: false,
      error: "Command ID is empty"
    });
  }

  const success = body.ok === true;

  const result = String(
    body.result === undefined
      ? ""
      : body.result
  );

  const sheet = getSheet();

  const lastRow = sheet.getLastRow();

  if (lastRow < 2) {
    return jsonResponse({
      ok: false,
      error: "Command not found"
    });
  }

  const ids = sheet
    .getRange(
      2,
      1,
      lastRow - 1,
      1
    )
    .getValues();

  for (let i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === id) {
      const row = i + 2;

      sheet
        .getRange(row, 5)
        .setValue(
          success ? "done" : "error"
        );

      sheet
        .getRange(row, 6)
        .setValue(result);

      SpreadsheetApp.flush();

      return jsonResponse({
        ok: true
      });
    }
  }

  return jsonResponse({
    ok: false,
    error: "Command not found"
  });
}


function resetTeleBridgeSecret() {
  PropertiesService
    .getScriptProperties()
    .deleteProperty(SECRET_PROPERTY);

  Logger.log(
    "TeleBridge secret has been reset."
  );
}


function setupCommandsSheet() {
  const sheet = getSheet();

  sheet.setFrozenRows(1);

  sheet.autoResizeColumns(
    1,
    6
  );

  return true;
}


function jsonResponse(data) {
  return ContentService
    .createTextOutput(
      JSON.stringify(data)
    )
    .setMimeType(
      ContentService.MimeType.JSON
    );
}