// src/api/cash_flow.js
// High-level API helpers for the cash-flow module, using the shared axios instance
// Endpoints assume a REST API under /api (see backend app/urls.py). Adjust paths if needed.

import api from "./axios";

// Transactions
export async function listTransactions({ from, to, page = 1, page_size = 20 } = {}) {
	const params = {};
	if (from) params.from = from; // YYYY-MM-DD
	if (to) params.to = to;       // YYYY-MM-DD
	params.page = page;
	params.page_size = page_size;
	const { data } = await api.get("/transactions/", { params });
	return data; // expect { results: [...], count, next, previous }
}

export async function createTransaction(payload) {
	// payload example:
	// { bank_account, credit_card, category, description, type, amount, date, status }
	const { data } = await api.post("/transactions/", payload);
	return data;
}

export async function deleteTransaction(id) {
	await api.delete(`/transactions/${id}/`);
}

// Credit Card specific
export async function listCreditCardTransactions({ date, credit_card} = {}) {
	const params = {};
	if (date) params.date = date; // YYYY-MM-DD (billing period reference)
	if (credit_card) params.credit_card = credit_card;  
	const { data } = await api.get("/credit-cards/transactions/", { params });
	return data;
}

export async function importCreditCardFile(file) {
	const form = new FormData();
	form.append("file", file);
	const { data } = await api.post("/credit-cards/import/", form, {
		headers: { "Content-Type": "multipart/form-data" },
	});
	return data; // expect summary of imported rows
}

// Accounts / dashboard
export async function getAccountsSummary() {
	const { data } = await api.get("/accounts/summary/");
	return data; // expect { total_balance, accounts: [...] }
}

export async function listCreditCards() {
	const { data } = await api.get("/credit-cards/");
	return data; // expect { credit_cards: [...] }
}

// Categories
export async function listCategories() {
	const { data } = await api.get("/categories/");
	return data; // expect list
}

// Convenience default export
export default {
	listTransactions,
	createTransaction,
	deleteTransaction,
	listCreditCardTransactions,
	importCreditCardFile,
	getAccountsSummary,
	listCategories,
};

