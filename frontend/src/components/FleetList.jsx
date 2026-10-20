import { money } from '../format.js';
import { BatteryIcon } from './Icons.jsx';

export default function FleetList({ batteries, batteryId, latest, runCount, onOpen }) {
  if (!batteries.length) return <div className="battery-list"><div className="empty">No batteries found.</div></div>;
  return (
    <div className="battery-list">
      {batteries.map(b => {
        const selected = b.battery_id === batteryId;
        const run = selected ? latest : null;
        return (
          <button key={b.battery_id} className={`battery-row ${selected ? 'selected' : ''}`} onClick={() => onOpen(b.battery_id)}>
            <div className="battery-icon"><BatteryIcon /></div>
            <div className="battery-info">
              <div className="battery-name">{b.name}</div>
              <div className="battery-meta">{b.location} · {b.owner} · {b.iso}</div>
            </div>
            {run && (
              <div className="battery-stats">
                <div className="bstat"><div className={`bstat-val ${run.revenue >= 0 ? 'rev-pos' : 'rev-neg'}`}>{money(run.revenue, 0)}</div><div className="bstat-lbl">Latest run</div></div>
                <div className="bstat"><div className="bstat-val">{runCount}</div><div className="bstat-lbl">Runs</div></div>
              </div>
            )}
          </button>
        );
      })}
    </div>
  );
}
