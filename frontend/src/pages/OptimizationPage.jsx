import { useMemo } from 'react';
import { money, mwh, runLabel, NBSP } from '../format.js';
import { BLUE, TEAL, HOLD, TEAL_T, baseOptions, hourLabels, revColors } from '../charts.js';
import ChartCanvas from '../components/ChartCanvas.jsx';
import { BatteryIcon } from '../components/Icons.jsx';
import { PageHeader, CardHeader } from '../components/Layout.jsx';

function downloadCSV(battery, latest) {
  const cols = ['output_id', 'version', 'date', 'hour', 'action', 'charge_kw', 'discharge_kw', 'soc_kw', 'price_mwh', 'revenue'];
  const csv = [cols.join(','), ...latest.rows.map(r => cols.map(c => JSON.stringify(r[c] ?? '')).join(','))].join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  a.download = `${(battery?.name || 'battery')}_run_${latest.output_id}.csv`;
  a.click();
  URL.revokeObjectURL(a.href);
}

function Heatmap({ rows }) {
  const maxPrice = Math.max(...rows.map(r => r.price_mwh), 1);
  return (
    <>
      <div className="heatmap-grid">
        {rows.map(r => {
          const k = 0.4 + Math.min(r.price_mwh / maxPrice, 1) * 0.6;
          const bg = r.action === 'charge' ? `rgba(84,105,212,${k})` : r.action === 'discharge' ? `rgba(9,130,93,${k})` : '#eef0f3';
          const label = r.action === 'charge' ? 'C' : r.action === 'discharge' ? 'D' : '—';
          return <div key={r.hour} className={`hm-cell ${r.action === 'hold' ? 'hold' : ''}`} style={{ background: bg }} title={`Hour ${r.hour} · ${money(r.price_mwh)}/MWh · ${r.action}`}>{label}</div>;
        })}
      </div>
      <div className="hm-labels">{rows.map(r => <div key={r.hour} className="hm-label">{r.hour}</div>)}</div>
    </>
  );
}

export default function OptimizationPage({ battery, latest }) {
  const rows = latest ? latest.rows : [];

  const charts = useMemo(() => {
    if (!rows.length) return {};
    const labels = hourLabels(rows);
    const maxSoc = Math.max(...rows.map(r => r.soc_kw)) / 1000;
    return {
      soc: { type: 'line', data: { labels, datasets: [
        { label: 'SoC', data: rows.map(r => r.soc_kw / 1000), borderColor: BLUE, backgroundColor: TEAL_T, fill: true, borderWidth: 2 },
        { label: 'Peak SoC', data: rows.map(() => maxSoc), borderColor: '#a3acb9', borderDash: [4, 4], borderWidth: 1 },
      ] }, options: baseOptions('MWh', true) },
      revenue: { type: 'bar', data: { labels, datasets: [{ label: 'Revenue', data: rows.map(r => r.revenue), backgroundColor: revColors(rows), borderRadius: 3 }] }, options: baseOptions('$') },
      price: { type: 'line', data: { labels, datasets: [{ label: 'Price', data: rows.map(r => r.price_mwh), borderColor: '#3c4257', backgroundColor: 'transparent', borderWidth: 2, pointRadius: 3, pointBorderWidth: 0, pointBackgroundColor: rows.map(r => r.action === 'charge' ? BLUE : r.action === 'discharge' ? TEAL : HOLD) }] }, options: baseOptions('$/MWh') },
    };
  }, [rows]);

  const sub = latest ? `${battery ? battery.name + ' · ' : ''}${runLabel(latest)} · ${latest.date} · ${latest.type}` : 'No runs yet';

  return (
    <section className="page active">
      <PageHeader title="Optimization Engine" sub={sub}>
        <button className="btn btn-secondary" onClick={() => latest && downloadCSV(battery, latest)}>↓ Export CSV</button>
      </PageHeader>

      <div className="battery-detail-hdr">
        <div className="detail-icon"><BatteryIcon size={26} /></div>
        <div>
          <div className="detail-name">{battery ? battery.name : '—'}</div>
          <div className="detail-sub">{battery ? `${battery.location} · ${battery.iso} · Owner: ${battery.owner}` : NBSP}</div>
        </div>
        <div className="detail-kpis">
          <div><div className="dkpi-val">{latest ? money(latest.revenue) : '—'}</div><div className="dkpi-lbl">Net Revenue</div></div>
          <div><div className="dkpi-val">{latest ? mwh(latest.charged) : '—'}</div><div className="dkpi-lbl">Total Charged</div></div>
          <div><div className="dkpi-val">{latest ? mwh(latest.discharged) : '—'}</div><div className="dkpi-lbl">Total Discharged</div></div>
          <div><div className="dkpi-val">{rows.length ? mwh(rows.at(-1).soc_kw) : '—'}</div><div className="dkpi-lbl">End SoC</div></div>
        </div>
      </div>

      <div className="chart-card mb">
        <CardHeader title="Hourly Price Signal & Dispatch Action" sub="Cell brightness follows the hour's price" />
        <Heatmap rows={rows} />
        <div className="legend">
          <span><i style={{ background: '#5469D4' }}></i>Charge</span>
          <span><i style={{ background: '#09825D' }}></i>Discharge</span>
          <span><i style={{ background: '#eef0f3', border: '1px solid #d0d7de' }}></i>Hold</span>
        </div>
      </div>

      <div className="grid-2">
        <div className="chart-card">
          <CardHeader title="State of Charge" sub="Trajectory across the 24h horizon (MWh)" />
          <ChartCanvas config={charts.soc} />
        </div>
        <div className="chart-card">
          <CardHeader title="Hourly Revenue" sub="Charge cost (−) and discharge revenue (+)" />
          <ChartCanvas config={charts.revenue} />
        </div>
      </div>

      <div className="chart-card">
        <CardHeader title="Price Curve" sub="Settlement price by hour ($/MWh)" />
        <ChartCanvas config={charts.price} height="200px" />
      </div>
    </section>
  );
}
