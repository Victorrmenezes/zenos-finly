import React, { useState, useEffect } from 'react';
import BasePage from './BasePage';
import './CregitCardPage.css';
import { listCreditCardTransactions, importCreditCardFile } from '../api/cash_flow';
import Table from '../components/MyTable.jsx';

function CreditCardPage() {
	const [transactions, setTransactions] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [importPreview, setImportPreview] = useState(null);
	const [importing, setImporting] = useState(false);
	const [importResult, setImportResult] = useState(null);
	const [creditCardId, setCreditCardId] = useState(''); // future filter/select
	const [referenceDate, setReferenceDate] = useState(() => new Date().toISOString().slice(0,10));

	async function fetchTransactions() {
		setLoading(true); setError(null);
		try {
			const data = await listCreditCardTransactions({ date: referenceDate, credit_card: creditCardId || undefined });
			// If backend later paginates: handle data.results else assume data is list
			const items = Array.isArray(data) ? data : data.results || [];
			setTransactions(items);
		} catch (e) {
			setError(e?.response?.data?.detail || e.message);
		} finally {
			setLoading(false);
		}
	}

	useEffect(() => { fetchTransactions(); }, [referenceDate, creditCardId]);

	function handleAddClick() {
		// Placeholder for future modal/creation form
	}

	function handleFileChange(e) {
		const file = e.target.files?.[0];
		if (!file) return;
		// Show first lines preview (text formats). For xlsx we skip preview and upload directly.
		const ext = file.name.split('.').pop().toLowerCase();
		if (['csv','txt'].includes(ext)) {
			const reader = new FileReader();
			reader.onload = evt => {
				const text = evt.target.result;
				const lines = text.split(/\r?\n/).slice(0,5);
				setImportPreview(lines.filter(l => l.trim() !== ''));
			};
			reader.readAsText(file);
		} else {
			setImportPreview([`Arquivo ${file.name}`]);
		}
		uploadFile(file);
	}

	async function uploadFile(file) {
		setImporting(true); setImportResult(null); setError(null);
		try {
			const result = await importCreditCardFile(file);
			setImportResult(result);
			// refresh list after import
			await fetchTransactions();
		} catch (e) {
			setError(e?.response?.data?.detail || e.message);
		} finally {
			setImporting(false);
		}
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
							<input type="file" accept=".csv,.txt,.xlsx" onChange={handleFileChange} hidden />
						</label>
					</div>
				</header>

				<div className="filters-row">
					<div className="filter-item">
						<label>Data referência</label>
						<input type="date" value={referenceDate} onChange={e => setReferenceDate(e.target.value)} />
					</div>
					<div className="filter-item">
						<label>Cartão (ID)</label>
						<input type="text" placeholder="Opcional" value={creditCardId} onChange={e => setCreditCardId(e.target.value)} />
					</div>
				</div>

				{importPreview && (
					<div className="import-preview">
						<div className="import-preview-head">Pré-visualização (primeiras linhas)</div>
						<pre>{importPreview.join('\n')}</pre>
						<button type="button" className="link-btn" onClick={() => setImportPreview(null)}>Limpar pré-visualização</button>
					</div>
				)}

				{importing && <div className="status-msg">Importando arquivo...</div>}
				{importResult && <div className="status-msg success">Importado: {importResult.imported} linhas.</div>}
				{error && <div className="status-msg error">Erro: {error}</div>}

				<Table
					data={transactions}
					excludeKeys={["id", "credit_card", "bank_account", "category"]}
					headers={{ date: 'Data', description: 'Descrição', status: 'Status', amount: 'Valor' }}
					formatters={{
						date: (v) => v ? new Date(v).toLocaleDateString('pt-BR') : '',
						amount: (v) => Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
					}}
					loading={loading}
					emptyText={error ? '' : 'Nenhuma transação.'}
					rowClassName={(row) => row.status === 'PLANNED' ? 'row-planned' : 'row-confirmed'}
				/>
			</div>
		</BasePage>
	);
}

export default CreditCardPage;
