const svgProps = { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round' };

export const NavIcons = {
  dashboard: <svg {...svgProps}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>,
  fleet: <svg {...svgProps}><rect x="2" y="7" width="18" height="11" rx="2"/><path d="M22 11v3"/><line x1="6" y1="11" x2="6" y2="14"/><line x1="10" y1="11" x2="10" y2="14"/></svg>,
  optimization: <svg {...svgProps}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>,
  schedule: <svg {...svgProps}><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>,
  history: <svg {...svgProps}><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>,
};

export function BatteryIcon({ size }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="#00D4AA" strokeWidth="1.8" strokeLinecap="round"><rect x="2" y="7" width="18" height="11" rx="2"/><path d="M22 11v3"/><line x1="6" y1="11" x2="6" y2="14"/><line x1="10" y1="11" x2="10" y2="14"/></svg>
  );
}

export function PulseIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>;
}

export function PanelIcon() {
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="9" y1="4" x2="9" y2="20"/></svg>;
}
