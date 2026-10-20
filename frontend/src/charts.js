import Chart from 'chart.js/auto';

// Discharge green, charge indigo, hold gray
export const TEAL = '#09825D', AMBER = '#E5A10B', RED = '#DF1B41', BLUE = '#5469D4', HOLD = '#C1C9D2';
export const TEAL_T = 'rgba(84,105,212,0.08)';

Chart.defaults.color = '#697386';
Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
Chart.defaults.font.size = 12;
Chart.defaults.elements.line.tension = 0.25;
Chart.defaults.elements.point.radius = 0;
Chart.defaults.elements.point.hoverRadius = 4;
Chart.defaults.elements.bar.borderRadius = 2;
Chart.defaults.interaction = { mode: 'index', intersect: false };

export function baseOptions(yLabel, legend = false) {
  return {
    responsive: true, maintainAspectRatio: false, animation: { duration: 300 },
    plugins: {
      legend: { display: legend, align: 'end', labels: { color: '#697386', boxWidth: 8, boxHeight: 8, usePointStyle: true, pointStyle: 'circle', font: { size: 12 } } },
      tooltip: { backgroundColor: '#fff', borderColor: '#e3e8ee', borderWidth: 1, padding: 10, cornerRadius: 6, titleColor: '#1a1f36', bodyColor: '#3c4257', boxPadding: 4, usePointStyle: true },
    },
    scales: {
      x: { grid: { display: false }, border: { color: '#e3e8ee' }, ticks: { color: '#697386', maxRotation: 0, autoSkipPadding: 8 } },
      y: { grid: { color: '#f0f2f5' }, border: { display: false }, ticks: { color: '#697386', maxTicksLimit: 6 }, title: { display: !!yLabel, text: yLabel, color: '#697386', font: { size: 12 } } },
    },
  };
}

export const hourLabels = rows => rows.map(r => `${r.hour}h`);
export const revColors = rows => rows.map(r => r.revenue > 0 ? TEAL : r.revenue < 0 ? RED : HOLD);

export { Chart };
