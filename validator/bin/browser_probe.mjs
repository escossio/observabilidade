#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright-core";

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Parametro sem valor: --${key}`);
    }
    result[key] = value;
    i += 1;
  }
  return result;
}

function nowIso() {
  return new Date().toISOString();
}

const args = parseArgs(process.argv.slice(2));
const targetUrl = args.url;
const outDir = args["out-dir"];
const chromiumPath = args.chromium || "/usr/bin/chromium";

if (!targetUrl || !outDir) {
  console.error("Uso: browser_probe.mjs --url <url> --out-dir <dir> [--chromium <path>]");
  process.exit(2);
}

const consoleEvents = [];
const networkEvents = [];
let finalStatus = null;
let finalUrl = targetUrl;
let pageTitle = "";

const browser = await chromium.launch({
  executablePath: chromiumPath,
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--ignore-certificate-errors"
  ]
});

try {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    ignoreHTTPSErrors: true
  });
  const page = await context.newPage();

  page.on("console", (msg) => {
    consoleEvents.push({
      ts: nowIso(),
      type: msg.type(),
      text: msg.text(),
      location: msg.location()
    });
  });

  page.on("pageerror", (error) => {
    consoleEvents.push({
      ts: nowIso(),
      type: "pageerror",
      text: error.message
    });
  });

  page.on("response", async (response) => {
    const request = response.request();
    networkEvents.push({
      ts: nowIso(),
      event: "response",
      url: response.url(),
      method: request.method(),
      resourceType: request.resourceType(),
      status: response.status(),
      ok: response.ok(),
      failure: null
    });
  });

  page.on("requestfailed", (request) => {
    networkEvents.push({
      ts: nowIso(),
      event: "requestfailed",
      url: request.url(),
      method: request.method(),
      resourceType: request.resourceType(),
      status: null,
      ok: false,
      failure: request.failure()?.errorText || "unknown"
    });
  });

  const response = await page.goto(targetUrl, {
    waitUntil: "domcontentloaded",
    timeout: 30000
  });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(3000);
  await page.screenshot({
    path: path.join(outDir, "page.png"),
    fullPage: true
  });

  finalStatus = response ? response.status() : null;
  finalUrl = page.url();
  pageTitle = await page.title().catch(() => "");

  await fs.writeFile(
    path.join(outDir, "browser-console.json"),
    JSON.stringify(consoleEvents, null, 2) + "\n",
    "utf8"
  );
  await fs.writeFile(
    path.join(outDir, "browser-network.json"),
    JSON.stringify(networkEvents, null, 2) + "\n",
    "utf8"
  );

  const summary = {
    target: targetUrl,
    finalUrl,
    title: pageTitle,
    status: finalStatus,
    requestCount: networkEvents.length,
    consoleEntries: consoleEvents.length,
    consoleErrors: consoleEvents.filter((entry) => entry.type === "error" || entry.type === "pageerror").length,
    networkFailures: networkEvents.filter(
      (entry) => entry.event === "requestfailed" || (entry.event === "response" && entry.ok === false)
    ).length
  };

  await fs.writeFile(
    path.join(outDir, "browser-summary.json"),
    JSON.stringify(summary, null, 2) + "\n",
    "utf8"
  );

  process.stdout.write(JSON.stringify(summary) + "\n");
} finally {
  await browser.close();
}
