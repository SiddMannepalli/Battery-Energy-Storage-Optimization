import { useState } from 'react';
import { money, signedMoney, num, cap, plural } from '../format.js';
import { PageHeader, CardHeader } from '../components/Layout.jsx';

export default function SchedulePage({ battery, runs, latest }) {
  const [mode, setMode] = useState('latest');
  const shown = mode === 'latest' ? (latest ? [latest] : []) : [...runs].reverse();
  const rows = shown.flatMap(run => run.rows);

  return (
    <section className="page active">
      <PageHeader title="Dispatch Schedule" sub={battery ? battery.name : ''}>
        <label className="select-wrap">View
          <select className="select" value={mode} onChange={e => setMode(e.target.value)}>
            <option value="latest">Latest run only</option>
            <option value="all">All historical runs</option>
          </select>
        </label>
      </PageHeader>
      <div className="chart-card">
        <CardHeader title="Hourly Charge / Discharge Plan" sub={`${plural(shown.length, 'run')} · ${rows.length} hours`} />
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Run</th><th>Version</th><th>Date</th><th>Hour</th><th>Action</th>
                <th className="num">Charge kW</th><th className="num">Discharge kW</th><th className="num">SoC kWh</th>
                <th className="num">Price $/MWh</th><th className="num">Revenue $</th>
              </tr>
            </thead>
            <tbody>
              {rows.length ? rows.map(r => (
                <tr key={`${r.output_id}-${r.hour}`}>
                  <td>#{r.output_id}</td><td>v{r.version}</td><td>{r.date}</td><td>{r.hour}:00</td>
                  <td className={`action-${r.action}`}>{cap(r.action)}</td>
                  <td className="num">{r.charge_kw > 0 ? num(r.charge_kw) : '—'}</td>
                  <td className="num">{r.discharge_kw > 0 ? num(r.discharge_kw) : '—'}</td>
                  <td className="num">{num(r.soc_kw)}</td>
                  <td className="num">{money(r.price_mwh)}</td>
                  <td className={`num ${r.revenue > 0 ? 'rev-pos' : r.revenue < 0 ? 'rev-neg' : ''}`}>{signedMoney(r.revenue)}</td>
                </tr>
              )) : <tr><td colSpan="10" className="empty">No schedule data.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
