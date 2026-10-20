export const money = (v, d = 2) => (v < 0 ? '−$' : '$') + Math.abs(v).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d });
export const signedMoney = v => v === 0 ? '—' : (v > 0 ? '+' : '') + money(v);
export const mwh = kwh => (kwh / 1000).toLocaleString(undefined, { maximumFractionDigits: 1 }) + ' MWh';
export const num = (v, d = 1) => v.toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d });
export const sum = (rows, k) => rows.reduce((s, r) => s + r[k], 0);
export const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
export const runLabel = run => `v${run.version} · #${run.output_id}`;
export const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;
export const NBSP = ' ';

export const PAGE_LABELS = { dashboard: 'Dashboard', fleet: 'Fleet', optimization: 'Optimization', schedule: 'Schedule', history: 'Run History' };
