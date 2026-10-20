import { PAGE_LABELS, NBSP } from '../format.js';
import { NavIcons, PanelIcon } from './Icons.jsx';

function NavItem({ id, page, onNav, children }) {
  return (
    <button className={`nav-item${page === id ? ' active' : ''}`} title={PAGE_LABELS[id]} onClick={() => onNav(id)}>
      {NavIcons[id]}
      <span className="nav-label">{PAGE_LABELS[id]}</span>
      {children}
    </button>
  );
}

const API_STATUS = { ok: 'API connected', err: 'API unreachable' };

export function Sidebar({ page, onNav, batteryCount, api }) {
  return (
    <aside className="sidebar">
      <nav className="sidebar-section">
        <div className="sidebar-label">Overview</div>
        <NavItem id="dashboard" page={page} onNav={onNav} />
        <NavItem id="fleet" page={page} onNav={onNav}><span className="nav-badge">{batteryCount}</span></NavItem>
      </nav>
      <nav className="sidebar-section">
        <div className="sidebar-label">Operations</div>
        <NavItem id="optimization" page={page} onNav={onNav} />
        <NavItem id="schedule" page={page} onNav={onNav} />
      </nav>
      <nav className="sidebar-section">
        <div className="sidebar-label">Analytics</div>
        <NavItem id="history" page={page} onNav={onNav} />
      </nav>
      <div className="sidebar-footer">
        <span className={`status-dot${API_STATUS[api] ? ' ' + api : ''}`} title={API_STATUS[api]} />
        <span className="nav-label">{API_STATUS[api] ?? 'Connecting…'}</span>
      </div>
    </aside>
  );
}

export function Header({ page, collapsed, onToggle, batteries, batteryId, onSelectBattery }) {
  const label = collapsed ? 'Expand sidebar' : 'Collapse sidebar';
  return (
    <header className="header">
      <button className="sidebar-toggle" aria-label={label} aria-expanded={!collapsed} title={label} onClick={onToggle}>
        <PanelIcon />
      </button>
      <div className="header-breadcrumb">{PAGE_LABELS[page]}</div>
      <div className="header-right">
        <label className="select-wrap">Battery
          <select className="select" value={batteryId ?? ''} onChange={e => onSelectBattery(Number(e.target.value))}>
            {batteries.map(b => <option key={b.battery_id} value={b.battery_id}>{b.name}</option>)}
          </select>
        </label>
      </div>
    </header>
  );
}

export function PageHeader({ title, sub, children }) {
  return (
    <div className="page-hdr">
      <div><div className="page-title">{title}</div><div className="page-sub">{sub || NBSP}</div></div>
      {children}
    </div>
  );
}

export function CardHeader({ title, sub, children }) {
  return (
    <div className="chart-hdr">
      <div><div className="chart-title">{title}</div><div className="chart-sub">{sub || NBSP}</div></div>
      {children}
    </div>
  );
}

export function Kpi({ tone, label, value, sub, valueClass }) {
  return (
    <div className={`kpi-card ${tone}`}>
      <div className="kpi-label">{label}</div>
      <div className={`kpi-value ${valueClass ?? tone}`}>{value}</div>
      <div className="kpi-delta">{sub || NBSP}</div>
    </div>
  );
}
