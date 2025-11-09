import React, { useState } from 'react';
import BasePage from './BasePage';
import './CregitCardPage.css';

// Mock credit card transactions (replace with API later)
const MOCK_CC_TX = [
	{ id: 101, date: '2025-11-01', description: 'Compra supermercado', amount: -245.90, status: 'CONFIRMED' },
	{ id: 102, date: '2025-11-03', description: 'Posto de gasolina', amount: -180.00, status: 'CONFIRMED' },
	{ id: 103, date: '2025-11-05', description: 'Assinatura software', amount: -49.99, status: 'PLANNED' },
	{ id: 104, date: '2025-11-08', description: 'Restaurante', amount: -130.50, status: 'CONFIRMED' },
];

function CreditCardPage() {
	const [transactions, setTransactions] = useState(MOCK_CC_TX);
	const [importPreview, setImportPreview] = useState(null);

	function handleAddClick() {
		// Placeholder: normally open a modal or navigate to form
		const fake = { id: Date.now(), date: new Date().toISOString().slice(0,10), description: 'Nova compra', amount: -10, status: 'PLANNED' };
		setTransactions(prev => [fake, ...prev]);
	}

	function handleFileChange(e) {
		const file = e.target.files?.[0];
		if (!file) return;
		// Simple client-side preview of first lines (no upload yet)
		const reader = new FileReader();
		reader.onload = evt => {
			const text = evt.target.result;
			const lines = text.split(/\r?\n/).slice(0,5);
			setImportPreview(lines.filter(l => l.trim() !== ''));
		};
		reader.readAsText(file);
	}

	return (
		<BasePage>
			<div className="cc-wrapper">
				<header className="cc-header">
					<h1 className="cc-title">Cartão de Crédito</h1>
					<div className="cc-actions">
						<button type="button" className="btn cc-btn" onClick={handleAddClick}>Adicionar Transação</button>
						<label className="btn cc-btn secondary">
							Importar Arquivo
							<input type="file" accept=".csv,.txt" onChange={handleFileChange} hidden />
						</label>
					</div>
				</header>

				{importPreview && (
					<div className="import-preview">
						<div className="import-preview-head">Pré-visualização (primeiras linhas)</div>
						<pre>{importPreview.join('\n')}</pre>
						<button type="button" className="link-btn" onClick={() => setImportPreview(null)}>Limpar pré-visualização</button>
					</div>
				)}

				<table className="cc-table">
					<thead>
						<tr>
							<th>Data</th>
							<th>Descrição</th>
							<th>Status</th>
							<th>Valor</th>
						</tr>
					</thead>
					<tbody>
						{transactions.map(tx => (
							<tr key={tx.id} className={tx.status === 'PLANNED' ? 'row-planned' : 'row-confirmed'}>
								<td>{new Date(tx.date).toLocaleDateString('pt-BR')}</td>
								<td>{tx.description}</td>
								<td>{tx.status}</td>
								<td className="amount">{tx.amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
							</tr>
						))}
						{transactions.length === 0 && (
							<tr><td colSpan={4} className="empty">Nenhuma transação.</td></tr>
						)}
					</tbody>
				</table>
			</div>
		</BasePage>
	);
}

export default CreditCardPage;
