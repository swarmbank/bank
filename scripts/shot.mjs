// Full-page screenshot via Chrome DevTools Protocol. Usage: node scripts/shot.mjs <url> <out.png> <width> [mobile]
import { spawn } from "node:child_process";
import fs from "node:fs";
const [url, out, widthArg, mobile, clipArg] = process.argv.slice(2);
const width = Number(widthArg || 1440);
const port = 9222 + Math.floor(Math.random() * 500);
const prof = fs.mkdtempSync("/tmp/shot-prof-");
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, "--no-first-run", "--disable-gpu", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let targets;
for (let i = 0; i < 40; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (targets?.length) break; } catch {} await sleep(250); }
const ws = new WebSocket(targets.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } };
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width, height: 900, deviceScaleFactor: 1, mobile: mobile === "mobile" });
await send("Page.navigate", { url });
await sleep(1500);
const { result: { result: { value: height } } } = await send("Runtime.evaluate", { expression: "Math.ceil(Math.max(document.documentElement.scrollHeight, document.body.scrollHeight))", returnByValue: true });
await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: mobile === "mobile" });
await sleep(400);
const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: 0, y: 0, width, height: clipArg ? Math.min(height, Number(clipArg)) : height, scale: 1 } });
fs.writeFileSync(out, Buffer.from(shot.result.data, "base64"));
console.log(`${out} ${width}x${clipArg ? Math.min(height, Number(clipArg)) : height}`);
ws.close(); chrome.kill(); await new Promise((r) => chrome.on("exit", r)); await sleep(300); try { fs.rmSync(prof, { recursive: true, force: true }); } catch {}
