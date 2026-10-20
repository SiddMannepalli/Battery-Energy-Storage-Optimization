import { sum } from './format.js';

// Same origin in both setups: Vercel routes these paths to FastAPI, and `npm run dev` proxies them to uvicorn
const API = '';

export async function getJSON(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(`${path} returned ${res.status}`);
  return res.json();
}

// Group the flat API rows into one object per optimization run
export function groupRuns(rows) {
  const byId = new Map();
  rows.forEach(r => {
    if (!byId.has(r.output_id)) byId.set(r.output_id, { output_id: r.output_id, version: r.version, date: r.date, type: r.optimization_type, rows: [] });
    byId.get(r.output_id).rows.push(r);
  });
  const runs = [...byId.values()];
  runs.forEach(run => {
    run.rows.sort((a, b) => a.hour - b.hour);
    run.revenue = sum(run.rows, 'revenue');
    run.charged = sum(run.rows, 'charge_kw');
    run.discharged = sum(run.rows, 'discharge_kw');
  });
  return runs.sort((a, b) => a.output_id - b.output_id);
}

// Same rule as the API's /latest endpoint: highest version wins; newest run within it
export function latestRun(runs) {
  if (!runs.length) return null;
  const maxV = Math.max(...runs.map(r => r.version));
  return runs.filter(r => r.version === maxV).at(-1);
}
