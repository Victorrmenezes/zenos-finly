import React from 'react';
import './Table.css';

/**
 * Generic table for arrays of plain JS objects.
 * - Derives columns from object keys when not provided
 * - Responsive (labels on mobile via data-label)
 * - Pretty defaults: zebra rows, hover, sticky header
 *
 * Props:
 * - data: Array<object>
 * - columns?: Array<string> (keys to show, in order). If omitted, uses keys of the first row.
 * - excludeKeys?: Array<string>
 * - headers?: Record<string,string>  (map key -> header title)
 * - formatters?: Record<string,(value:any,row:object)=>React.ReactNode>
 * - loading?: boolean
 * - emptyText?: string
 * - dense?: boolean
 * - zebra?: boolean
 * - hover?: boolean
 * - stickyHeader?: boolean
 * - rowKey?: (row, index) => string|number
 * - onRowClick?: (row) => void
 * - rowClassName?: (row) => string
 */
export default function Table({
	data = [],
	columns,
	excludeKeys = [],
	headers = {},
	formatters = {},
	loading = false,
	emptyText = 'Nenhum registro encontrado.',
	dense = false,
	zebra = true,
	hover = true,
	stickyHeader = true,
	rowKey,
	onRowClick,
	rowClassName,
}) {
	// Derive columns from first row if not provided
	const resolvedColumns = React.useMemo(() => {
		if (columns && columns.length) return columns.filter(k => !excludeKeys.includes(k));
		const first = data && data.length ? data[0] : null;
		if (!first) return [];
		return Object.keys(first).filter(k => !excludeKeys.includes(k));
	}, [columns, data, excludeKeys]);

	const headerFor = (key) => headers[key] || humanize(key);

	const classNames = [
		'tbl',
		zebra ? 'zebra' : '',
		hover ? 'hover' : '',
		stickyHeader ? 'sticky-hdr' : '',
		dense ? 'dense' : '',
	].filter(Boolean).join(' ');

	return (
		<div className="tbl-wrapper">
			<table className={classNames}>
				<thead>
					<tr>
						{resolvedColumns.map((col) => (
							<th key={col}>{headerFor(col)}</th>
						))}
					</tr>
				</thead>
				<tbody>
					{loading ? (
						<tr className="loading-row"><td colSpan={resolvedColumns.length}><div className="loading-bar" /></td></tr>
					) : data && data.length ? (
						data.map((row, idx) => {
							const key = rowKey ? rowKey(row, idx) : (row.id ?? idx);
							const clickable = !!onRowClick;
							const extraClass = rowClassName ? rowClassName(row) : '';
							return (
								<tr key={key} className={[clickable ? 'clickable' : '', extraClass].filter(Boolean).join(' ')} onClick={clickable ? () => onRowClick(row) : undefined}>
									{resolvedColumns.map((col) => {
										const raw = row[col];
										const val = formatters[col] ? formatters[col](raw, row) : defaultRender(raw);
										return (
											<td key={col} data-label={headerFor(col)}>{val}</td>
										);
									})}
								</tr>
							);
						})
					) : (
						<tr className="empty-row"><td colSpan={resolvedColumns.length}>{emptyText}</td></tr>
					)}
				</tbody>
			</table>
		</div>
	);
}

function humanize(key) {
	return String(key)
		.replace(/_/g, ' ')
		.replace(/\b\w/g, (m) => m.toUpperCase());
}

function defaultRender(value) {
	if (value == null) return '';
	if (typeof value === 'boolean') return value ? 'Sim' : 'Não';
	return String(value);
}

