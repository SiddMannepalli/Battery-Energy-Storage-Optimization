import { useEffect, useRef } from 'react';
import { Chart } from '../charts.js';

// A Chart.js canvas that is rebuilt whenever its config changes
export default function ChartCanvas({ config, height }) {
  const canvasRef = useRef(null);
  useEffect(() => {
    if (!config) return;
    const chart = new Chart(canvasRef.current, config);
    return () => chart.destroy();
  }, [config]);
  return <div className="chart-wrap" style={height ? { height } : undefined}><canvas ref={canvasRef} /></div>;
}
