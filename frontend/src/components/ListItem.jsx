import React from 'react';
import './ListItem.css';

/**
 * Generic styled list item component.
 * Props:
 * - imageUrl: string
 * - title: string
 * - rating: number | string
 * - meta: string (secondary line)
 * - address?: string
 * - description?: string
 * - onClick?: () => void
 */
function ListItem({ imageUrl, title, rating, meta, address, description, actions, onClick }) {
  return (
    <div className="list-item" onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }}>
      {imageUrl && <img src={imageUrl} alt={title} className="list-item-avatar" />}
      <div className="list-item-info">
        <div className="list-item-top">
          <div className="list-item-name">{title}</div>
          {rating !== undefined && rating !== null && (
            <div className="list-item-rating">{rating} ★</div>
          )}
        </div>
        {meta && <div className="list-item-meta">{meta}</div>}
        {address && <div className="list-item-address">{address}</div>}
        {description && <div className="list-item-desc">{description}</div>}
        {actions && <div className="list-item-actions">{actions}</div>}
      </div>
    </div>
  );
}

export default ListItem;
