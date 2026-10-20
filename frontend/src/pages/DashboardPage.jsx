import { useMemo, useState } from 'react';
import { money, mwh, runLabel } from '../format.js';
import { BLUE, TEAL, HOLD, TEAL_T, baseOptions, hourLabels, revColors } from '../charts.js';
import ChartCanvas from '../components/ChartCanvas.jsx';
import FleetList from '../components/FleetList.jsx';
import { PulseIcon } from '../components/Icons.jsx';
import { PageHeader, CardHeader, Kpi } from '../components/Layout.jsx';

const TABS = [['soc', 'State of Charge'], ['revenue', 'Revenue'], ['power', 'Charge / Discharge']];

// Plain-language takeaways from the latest run
function buildInsights(latest) {
  const rows = latest.rows;
  const items = [['success', <><strong>Net {latest.revenue >= 0 ? 'profit' : 'loss'} of {money(Math.abs(latest.revenue))}</strong> on {runLabel(latest)}</>]];
  const peak = rows.reduce((m, r) => r.price_mwh > m.price_mwh ? r : m, rows[0]);
  const low = rows.reduce((m, r) => r.price_mwh < m.price_mwh ? r : m, rows[0]);
  if (peak) items.push(['warn', <><strong>Peak price {money(peak.price_mwh)}/MWh</strong> at hour {peak.hour} — battery set to {peak.action}</>]);
  if (low) items.push(['info', <><strong>Lowest price {money(low.price_mwh)}/MWh</strong> at hour {low.hour} — battery set to {low.action}</>]);
  const best = rows.reduce((m, r) => r.revenue > m.revenue ? r : m, rows[0]);
  if (best && best.revenue > 0) items.push(['success', <><strong>Best hour: {best.hour}</strong> earned {money(best.revenue)}</>]);
  return items;
}

export default function DashboardPage({ battery, batteries, batteryId, runs, latest, onNav, onOpenBattery }) {
  const [tab, setTab] = useState('soc');
  const rows = latest ? latest.rows : [];

  const mainChart = useMemo(() => {
    if (!rows.length) return null;
    const labels = hourLabels(rows);
    if (tab === 'soc') return { type: 'line', data: { labels, datasets: [{ label: 'SoC (MWh)', data: rows.map(r => r.soc_kw / 1000), borderColor: BLUE, backgroundColor: TEAL_T, fill: true, borderWidth: 2 }] }, options: baseOptions('MWh') };
    if (tab === 'revenue') return { type: 'bar', data: { labels, datasets: [{ label: 'Revenue ($)', data: rows.map(r => r.revenue), backgroundColor: revColors(rows), borderRadius: 3 }] }, options: baseOptions('$') };
    const opts = baseOptions('MW', true);
    return { type: 'bar', data: { labels, datasets: [
      { label: 'Charge (MW)', data: rows.map(r => -r.charge_kw / 1000), backgroundColor: BLUE },
      { label: 'Discharge (MW)', data: rows.map(r => r.discharge_kw / 1000), backgroundColor: TEAL },
    ] }, options: { ...opts, scales: { ...opts.scales, x: { ...opts.scales.x, stacked: true }, y: { ...opts.scales.y, stacked: true } } } };
  }, [rows, tab]);

  const counts = useMemo(() => ['charge', 'discharge', 'hold'].map(a => rows.filter(r => r.action === a).length), [rows]);
  const mixChart = useMemo(() => rows.length ? {
    type: 'doughnut',
    data: { labels: ['Charge', 'Discharge', 'Hold'], datasets: [{ data: counts, backgroundColor: [BLUE, TEAL, HOLD], borderColor: '#fff', borderWidth: 2 }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: '72%', plugins: { legend: { display: false }, tooltip: baseOptions().plugins.tooltip } },
  } : null, [rows, counts]);

  const sub = battery ? `${battery.iso} · ${battery.owner} · ${battery.name}` : (batteries.length ? 'No battery selected' : 'Loading…');

  return (
    <section className="page active">
      <PageHeader title="Portfolio Overview" sub={sub}>
        <button className="btn btn-secondary" onClick={() => onNav('optimization')}>
          <PulseIcon />
          View Optimization
        </button>
      </PageHeader>

      <div className="kpi-grid">
        <Kpi tone="teal" label="Net Revenue — Latest Run" value={latest ? money(latest.revenue) : '—'} valueClass={latest && latest.revenue < 0 ? 'red' : 'teal'} sub={latest && `${runLabel(latest)} · ${latest.date}`} />
        <Kpi tone="blue" label="Energy Charged" value={latest ? mwh(latest.charged) : '—'} sub={latest && `${counts[0]} charging hours`} />
        <Kpi tone="amber" label="Energy Discharged" value={latest ? mwh(latest.discharged) : '—'} sub={latest && `${counts[1]} discharging hours`} />
        <Kpi tone="red" label="Optimization Runs" value={latest ? runs.length : '—'} valueClass="" sub={latest && `Latest version: v${latest.version}`} />
      </div>

      <div className="grid-3-1">
        <div className="chart-card">
          <CardHeader title="Latest Run — 24h Profile" sub={latest && `${runLabel(latest)} · ${latest.date}`}>
            <div className="chart-tabs" role="tablist">
              {TABS.map(([id, label]) => (
                <button key={id} className={`chart-tab${tab === id ? ' active' : ''}`} onClick={() => setTab(id)}>{label}</button>
              ))}
            </div>
          </CardHeader>
          <ChartCanvas config={mainChart} />
        </div>

        <div className="chart-card">
          <CardHeader title="Dispatch Mix" sub="Hours by action — latest run" />
          <ChartCanvas config={mixChart} height="160px" />
          <div className="mini-stats">
            <div className="mini-stat"><div className="mini-stat-val" style={{ color: 'var(--charge)' }}>{latest ? counts[0] + 'h' : '—'}</div><div className="mini-stat-lbl">Charge</div></div>
            <div className="mini-stat"><div className="mini-stat-val" style={{ color: 'var(--discharge)' }}>{latest ? counts[1] + 'h' : '—'}</div><div className="mini-stat-lbl">Discharge</div></div>
            <div className="mini-stat"><div className="mini-stat-val" style={{ color: 'var(--hold)' }}>{latest ? counts[2] + 'h' : '—'}</div><div className="mini-stat-lbl">Hold</div></div>
          </div>
        </div>
      </div>

      <div className="grid-3-1">
        <div className="chart-card">
          <CardHeader title="Battery Fleet" sub="Click a battery to view its optimization">
            <button className="btn btn-secondary" onClick={() => onNav('fleet')}>View all</button>
          </CardHeader>
          <FleetList batteries={batteries} batteryId={batteryId} latest={latest} runCount={runs.length} onOpen={onOpenBattery} />
        </div>

        <div className="chart-card">
          <CardHeader title="Insights" sub="From the latest run" />
          <div className="alert-list">
            {latest
              ? buildInsights(latest).map(([cls, content], i) => <div key={i} className={`alert-item ${cls}`}><div className="alert-dot"></div><div className="alert-text">{content}</div></div>)
              : <div className="empty">No optimization runs yet.</div>}
          </div>
        </div>
      </div>
    </section>
  );
}
