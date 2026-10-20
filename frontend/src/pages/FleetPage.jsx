import { plural } from '../format.js';
import FleetList from '../components/FleetList.jsx';
import { PageHeader, CardHeader } from '../components/Layout.jsx';

export default function FleetPage({ batteries, batteryId, latest, runs, onOpenBattery }) {
  const isos = [...new Set(batteries.map(b => b.iso))].join(', ');
  return (
    <section className="page active">
      <PageHeader title="Battery Fleet" sub={`${plural(batteries.length, 'asset')}${isos ? ' · ' + isos : ''}`} />
      <div className="chart-card">
        <CardHeader title="Fleet Assets" sub="Select a battery to view full optimization detail" />
        <FleetList batteries={batteries} batteryId={batteryId} latest={latest} runCount={runs.length} onOpen={onOpenBattery} />
      </div>
    </section>
  );
}
