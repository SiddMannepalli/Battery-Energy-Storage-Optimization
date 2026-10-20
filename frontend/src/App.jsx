import { useCallback, useEffect, useMemo, useState } from 'react';
import { getJSON, groupRuns, latestRun } from './api.js';
import { Sidebar, Header } from './components/Layout.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import FleetPage from './pages/FleetPage.jsx';
import OptimizationPage from './pages/OptimizationPage.jsx';
import SchedulePage from './pages/SchedulePage.jsx';
import HistoryPage from './pages/HistoryPage.jsx';

export default function App() {
  const [page, setPage] = useState('dashboard');
  const [collapsed, setCollapsed] = useState(() => document.body.classList.contains('sidebar-collapsed'));
  const [api, setApi] = useState('pending');
  const [error, setError] = useState(null);
  const [batteries, setBatteries] = useState([]);
  const [batteryId, setBatteryId] = useState(null);
  const [rows, setRows] = useState([]);

  // Sidebar state lives on <body> so the CSS and the pre-paint script in index.html agree
  useEffect(() => {
    document.body.classList.toggle('sidebar-collapsed', collapsed);
    try { localStorage.setItem('sidebarCollapsed', collapsed ? '1' : '0'); } catch (e) {}
  }, [collapsed]);

  useEffect(() => {
    getJSON('/batteries')
      .then(list => {
        setApi('ok');
        setBatteries(list);
        if (list.length) setBatteryId(list[0].battery_id);
      })
      .catch(() => {
        setApi('err');
        setError('Could not reach the API. Check the Vercel function logs, or that uvicorn is running on port 8000 when using npm run dev.');
      });
  }, []);

  useEffect(() => {
    if (batteryId == null) return;
    let cancelled = false;
    getJSON(`/optimization/battery/${batteryId}`)
      .then(data => { if (!cancelled) { setRows(data); setError(null); } })
      .catch(() => {
        if (cancelled) return;
        setRows([]);
        setApi('err');
        setError('Failed to load optimization data for this battery.');
      });
    return () => { cancelled = true; };
  }, [batteryId]);

  const runs = useMemo(() => groupRuns(rows), [rows]);
  const latest = useMemo(() => latestRun(runs), [runs]);
  const battery = batteries.find(b => b.battery_id === batteryId);

  const openBattery = useCallback(id => { setBatteryId(id); setPage('optimization'); }, []);
  const shared = { battery, batteries, batteryId, runs, latest };

  return (
    <>
      <Sidebar page={page} onNav={setPage} batteryCount={batteries.length} api={api} />
      <div className="main">
        <Header page={page} collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} batteries={batteries} batteryId={batteryId} onSelectBattery={setBatteryId} />
        <div className="content">
          <div className={`banner${error ? ' show' : ''}`} role="alert"><span className="alert-dot"></span><span>{error}</span></div>
          {page === 'dashboard' && <DashboardPage {...shared} onNav={setPage} onOpenBattery={openBattery} />}
          {page === 'fleet' && <FleetPage {...shared} onOpenBattery={openBattery} />}
          {page === 'optimization' && <OptimizationPage {...shared} />}
          {page === 'schedule' && <SchedulePage {...shared} />}
          {page === 'history' && <HistoryPage {...shared} />}
        </div>
      </div>
    </>
  );
}
