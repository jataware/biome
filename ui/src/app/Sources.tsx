'use client';

import { useState, useEffect } from "react";
import { ProductService } from "./mock_product_data";
import { Button } from "primereact/button";
// import { Avatar } from "primereact/avatar";
import { DataView, DataViewLayoutOptions } from "primereact/dataview";
import { Rating } from 'primereact/rating';
import { Tag } from 'primereact/tag';
import { Dropdown } from 'primereact/dropdown';
import { classNames } from 'primereact/utils';

import s from './sources.module.scss';

function lower(s: string) {
  return s ? s.toLowerCase() : null;
}

interface CategoryModel {
  id: string,
  name: string,
  code: string,
  image: string,
  category: string
}

const Sources = ({ category = { name: 'all' } }) => {

  const [products, setProducts] = useState([]);
  const [layout, setLayout] = useState('grid');

  const [sortKey, setSortKey] = useState('');
  const [sortOrder, setSortOrder] = useState(0);
  const [sortField, setSortField] = useState('');
  const sortOptions = [
    { label: 'Desc', value: '!name' },
    { label: 'Asc', value: 'name' }
  ];

  useEffect(() => {
    ProductService
      .getProducts()
      .then((data) => {
        let filtered = data.slice(0, 13);
        if (!['all', undefined, null].includes(category.name)) {
          filtered = data.filter((item: CategoryModel) => {
            const dog = lower(category?.name);
            const cat = lower(item?.category);
            return cat === dog;
          });
        }
        setProducts(filtered);
      });
  }, [category]);

  const getSeverity = (product) => {
    switch (product.inventoryStatus) {
      case 'INSTOCK':
      case 'Verified':
        return 'success';

      case 'LOWSTOCK':
        return 'warning';

      case 'OUTOFSTOCK':
        return 'danger';

      default:
        return null;
    }
  };

  const onSortChange = (event) => {
    const value = event.value;

    if (value.indexOf('!') === 0) {
      setSortOrder(-1);
      setSortField(value.substring(1, value.length));
      setSortKey(value);
    } else {
      setSortOrder(1);
      setSortField(value);
      setSortKey(value);
    }
  };

  const listItem = (product, index) => {
    return (

      <div className="col-12" key={product.id}>
        <div className={classNames('flex flex-column xl:flex-row xl:align-items-start p-4 gap-4', { 'border-top-1 surface-border': index !== 0 })}>
          <img className="w-9 sm:w-16rem xl:w-10rem shadow-2 block xl:block mx-auto border-round" src={`https://primefaces.org/cdn/primereact/images/product/${product.image}`} alt={product.name} />
          <div className="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
            <div className="flex flex-column align-items-center sm:align-items-start gap-3">
              <div className="text-2xl font-bold text-900">{product.name}</div>
              <Rating value={product.rating} readOnly cancel={false}></Rating>
              <div className="flex align-items-center gap-3">
                <span className="flex align-items-center gap-2">
                  <i className="pi pi-tag"></i>
                  <span className="font-semibold">{product.category}</span>
                </span>
                <Tag value={product.inventoryStatus} severity={getSeverity(product)}></Tag>
              </div>
            </div>
            <div className="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
              <span className="text-2xl font-semibold">${product.price}</span>
              <Button icon="pi pi-shopping-cart" className="p-button-rounded" disabled={product.inventoryStatus === 'OUTOFSTOCK'}></Button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // <Avatar 
  //   icon={`pi pi-${product.icon}`} 
  //   size="normal"
  //    shape="circle"
  //    style={{ backgroundColor: colors[index] || randomColor }}
  //   />

  const gridItem = (product, index) => {
    const colors = ["#ff1744", "#2979ff", "#f50057", "#d500f9", "#651fff", "#1de9b6", "#ffea00", "#76ff03"];

    const randomColor = "#000000".replace(/0/g, function() { return (~~(Math.random() * 16)).toString(16); });

    return (
      <div className={classNames("col-12 sm:col-12 lg:col-6 xl:col-3 p-2", s.squareCard)}
        key={product.id}
      >
        <div className={classNames("p-4 border-1 surface-border surface-card border-round", s.cardContents)}>

          <div className={s.actionIcons}>
            <Button rounded icon={`pi pi-${product.icon}`} style={{ backgroundColor: colors[index] || randomColor, border: 'none' }} />
            <Button text size="large" icon="pi pi-bookmark" style={{ fontSize: '1.5rem', padding: 0 }} />
          </div>

          <div className={classNames("font-bold text-xl line-height-2", s.sourceName)}>
            {product.name}
          </div>

          <div className="flex flex-column align-items-center py-1">

            <span className={s.description}>{product.description}</span>

            <div className={classNames(s.categories, 'w-full py-3')}>
              <Tag className={s.categoryWeather} rounded value={product.category} />
              &nbsp;
              <Tag className={s.categoryAll} rounded value={product.category} />
            </div>

            <div className="flex justify-content-between w-full">
              <Rating stars={3} value={product.rating} readOnly cancel={false}></Rating>

              {['INSTOCK', 'Verified'].includes(product.inventoryStatus) && (
                <Tag
                  icon="pi pi-check-circle"
                  value={product.inventoryStatus}
                  severity={getSeverity(product)}
                />
              )}
            </div>
          </div>

          <div className="flex align-items-center pt-2">
            <Tag
              rounded
              icon="pi pi-clock"
              value={`${product.price}ms`}
              className={s.grayTag}
            />
            &nbsp;
            &nbsp;
            <Tag
              rounded
              icon="pi pi-check"
              value="90%"
              className={s.grayTag}
            />
          </div>
        </div>
      </div>
    );
  };

  const itemTemplate = (product, layout, index) => {
    if (!product) {
      return;
    }

    if (layout === 'list') return listItem(product, index);
    else if (layout === 'grid') return gridItem(product, index);
  };

  const listTemplate = (products, layout) => {
    return <div className="grid grid-nogutter">{products.map((product, index) => itemTemplate(product, layout, index))}</div>;
  };

  const header = () => {
    return (
      <div className="flex justify-content-between">
        <Dropdown
          options={sortOptions}
          value={sortKey}
          optionLabel="label"
          placeholder="Sort By Name"
          onChange={onSortChange}
          className="w-full sm:w-14rem"
        />
        <DataViewLayoutOptions
          layout={layout}
          onChange={(e) => setLayout(e.value)}
        />
      </div>
    );
  };

  return (
    <div className={s.root}>
      <h4>Sources</h4>

      <DataView
        className={s.dataview}
        value={products}
        listTemplate={listTemplate}
        layout={layout}
        header={header()}
        sortField={sortField}
        sortOrder={sortOrder}
      />
    </div>
  )

  // paginator
  // rows={5}

}

export default Sources;
