import React, { useState, useMemo } from 'react';
import BasePage from './BasePage';
import './HomePage.css';

// Simple mock transactions; later replace with API fetch
const MOCK_TRANSACTIONS = [
  { id: 1, date: '2025-11-01', description: 'Compra mercado', type: 'EXPENSE', amount: -120.55 },
  { id: 2, date: '2025-11-02', description: 'Salário', type: 'INCOME', amount: 4500.00 },
  { id: 3, date: '2025-11-05', description: 'Assinatura streaming', type: 'EXPENSE', amount: -29.90 },
  { id: 4, date: '2025-11-08', description: 'Transferência poupança', type: 'TRANSFER', amount: -300.00 },
];

function HomePage() {
  const today = new Date().toISOString().slice(0,10);
  const monthStart = today.slice(0,8) + '01';
  const [from, setFrom] = useState(monthStart);
  const [to, setTo] = useState(today);

  const filtered = useMemo(() => {
    return MOCK_TRANSACTIONS.filter(t => t.date >= from && t.date <= to);
  }, [from, to]);

  const total = useMemo(() => filtered.reduce((sum, t) => sum + t.amount, 0), [filtered]);

  return (
    <BasePage>
      <div className="home-container">
        <h1 className="home-title">Dashboard Financeiro</h1>
        {/* Date range filter */}
        <form className="date-filter" onSubmit={e => e.preventDefault()}>
          <label>
            De
            <input type="date" value={from} onChange={e => setFrom(e.target.value)} />
          </label>
          <label>
            Até
            <input type="date" value={to} onChange={e => setTo(e.target.value)} />
          </label>
        </form>

        {/* Chart placeholder */}
        <div className="chart-placeholder">
          <div className="chart-box">Gráfico</div>
        </div>

        {/* Summary */}
        <div className="summary">
          <span>Total no período:</span>
          <strong className={total >= 0 ? 'pos' : 'neg'}>{total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</strong>
          <span className="count">{filtered.length} transações</span>
        </div>

        {/* Transactions list */}
        <table className="tx-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Descrição</th>
              <th>Tipo</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(t => (
              <tr key={t.id} className={
                t.type === 'INCOME' ? 'tx-income' : t.type === 'EXPENSE' ? 'tx-expense' : 'tx-transfer'
              }>
                <td>{new Date(t.date).toLocaleDateString('pt-BR')}</td>
                <td>{t.description}</td>
                <td>{t.type}</td>
                <td>{t.amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr><td colSpan={4} className="empty">Nenhuma transação no intervalo.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </BasePage>
  );
}

export default HomePage;
