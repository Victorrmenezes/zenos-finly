import React from 'react';
import './MonthPicker.css';

// MonthPicker: nice month/year selector with dropdown grid
// Props:
// - value: string (YYYY-MM or YYYY-MM-DD) or Date
// - onChange: (newValue: string) => void  // emits YYYY-MM-01
// - locale?: string (default 'pt-BR')
// - placeholder?: string
export default function MonthPicker({ value, onChange, locale = 'pt-BR', placeholder = 'Selecione o mês' }) {
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef(null);

  const selected = toDate(value);
  const [panelYear, setPanelYear] = React.useState(selected.getFullYear());

  React.useEffect(() => {
    // sync panel year when external value changes
    const d = toDate(value);
    setPanelYear(d.getFullYear());
  }, [value]);

  React.useEffect(() => {
    const onDocClick = (e) => {
      if (!ref.current) return;
      if (!ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', onDocClick);
    return () => document.removeEventListener('mousedown', onDocClick);
  }, []);

  const label = selected
    ? selected.toLocaleDateString(locale, { month: 'short', year: 'numeric' })
    : '';

  const months = Array.from({ length: 12 }, (_, i) => i);

  function handleSelect(monthIndex) {
    const d = new Date(panelYear, monthIndex, 1);
    const iso = formatYYYYMM01(d);
    onChange?.(iso);
    setOpen(false);
  }

  return (
    <div className="mpicker" ref={ref}>
      <button type="button" className={`mpicker-input ${open ? 'open' : ''}`} onClick={() => setOpen((o) => !o)}>
        {label || <span className="placeholder">{placeholder}</span>}
        <span className="chev">▾</span>
      </button>

      {open && (
        <div className="mpicker-panel">
          <div className="mpicker-head">
            <button className="nav" onClick={() => setPanelYear((y) => y - 1)} aria-label="Ano anterior">‹</button>
            <div className="year-label">{panelYear}</div>
            <button className="nav" onClick={() => setPanelYear((y) => y + 1)} aria-label="Próximo ano">›</button>
          </div>
          <div className="mpicker-grid">
            {months.map((m) => {
              const d = new Date(panelYear, m, 1);
              const isSelected = selected.getFullYear() === panelYear && selected.getMonth() === m;
              const name = d.toLocaleDateString(locale, { month: 'short' });
              return (
                <button
                  key={m}
                  className={`cell ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleSelect(m)}
                  type="button"
                >
                  {capitalize(name)}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

function toDate(val) {
  if (val instanceof Date) return val;
  if (typeof val === 'string' && val) {
    // Accept YYYY-MM or YYYY-MM-DD
    const parts = val.split('-');
    const y = Number(parts[0]);
    const m = Number(parts[1] || 1) - 1;
    const d = Number(parts[2] || 1);
    const dt = new Date(y, isNaN(m) ? 0 : m, isNaN(d) ? 1 : d);
    return isNaN(dt.getTime()) ? new Date() : dt;
  }
  return new Date();
}

function formatYYYYMM01(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  return `${y}-${m}-01`;
}

function capitalize(s) {
  if (!s) return s;
  return s.charAt(0).toUpperCase() + s.slice(1);
}
