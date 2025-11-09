import React from 'react';

/**
 * Generic List component: renders a titled, scrollable list using a renderItem callback.
 * Props:
 * - title: string header
 * - items: array of data items
 * - renderItem: function (item, index) => ReactNode
 * - loading: boolean
 * - error: string | null
 * - emptyText: string (optional)
 */
function List({ title = '', items = [], renderItem, loading = false, error = null, emptyText = 'Nenhum item encontrado.' }) {
  return (
    <div className="list-container">
      {loading && <div className="list-loading">Carregando...</div>}
      {error && <div className="list-error">{error}</div>}
      <div className="list-items">
        {Array.isArray(items) && items.length > 0 ? (
          items.map((item, idx) => (renderItem ? renderItem(item, idx) : null))
        ) : (
          !loading && <div className="list-empty">{emptyText}</div>
        )}
      </div>
    </div>
  );
}

export default List;
