'use client';

import { useState } from "react";
import { ProductService } from "./mock_product_data";
import { Button } from "primereact/button";
// import { Avatar } from "primereact/avatar";
import { DataView, DataViewLayoutOptions } from "primereact/dataview";
import { Rating } from 'primereact/rating';
import { Tag } from 'primereact/tag';
import { Dropdown } from 'primereact/dropdown';
import { classNames } from 'primereact/utils';

import { ScrollTop } from 'primereact/scrolltop';
// import Image from 'next/image';

import s from './sources.module.scss';

function lower(s: string) {
  return s ? s.toLowerCase() : null;
}

interface CategoryModel {
  id: string,
  name: string,
  code: string,
  image: string,
  // category: string,
  categories: [string]
}

const uriLabelMappings = {
  "home_page": "Website",
  "data_landing": "Data",
  "site_map": "Site Map"
};

const AvailableUrls = ({ urlObj }) => {
  return (
    <div className={s.availableUrls}>
      <div>
        {['home_page', 'data_landing'].map((uriName) => urlObj[uriName] && (
          <a
            key={uriName}
            target="_blank"
            rel="noopener noreferrer"
            href={urlObj[uriName]}
          >
            <Button
              icon="pi pi-external-link"
              severity="info"
              text
              size="small"
              label={uriLabelMappings[uriName]}
            />
          </a>
        ))}
      </div>
    </div>
  );
}

const Sources = ({ category = { name: 'all' }, sources }) => {

  // const [sources, setFilteredSources] = useState([]);
  const [layout, setLayout] = useState('grid');

  const [sortKey, setSortKey] = useState('');
  const [sortOrder, setSortOrder] = useState(0);
  const [sortField, setSortField] = useState('');
  const sortOptions = [
    { label: 'Desc', value: '!name' },
    { label: 'Asc', value: 'name' }
  ];

  // TODO filter items on category changes with
  //  useState and such
    // ProductService
    //   .getProducts()
    //   .then((data) => {
    //     let filtered = data.slice(0, 13);
    //     if (!['all', undefined, null].includes(category.name)) {
    //       filtered = data.filter((item: CategoryModel) => {
    //         const selectedCategoryName = lower(category?.name);
    //         return (item?.categories || []).map(i => i.toLowerCase()).includes(selectedCategoryName);
    //       });
    //     }
    //     setFilteredSources(filtered);
    //   });

  const getSeverity = (source) => {
    switch (source.inventoryStatus) {
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

  const listItem = (source, index) => {
    return (

      <div className="col-12" key={source.id}>
        <div className={classNames('flex flex-column xl:flex-row xl:align-items-start p-3 gap-4', { 'border-top-1 surface-border': index !== 0 })}>
          <img className="w-9 sm:w-16rem xl:w-10rem shadow-2 block xl:block mx-auto border-round" src={`https://primefaces.org/cdn/primereact/images/products/${source.image}`} alt={source.name} />
          <div className="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
            <div className="flex flex-column align-items-center sm:align-items-start gap-3">
              <div className="text-2xl font-bold text-900">{source.name}</div>
              <Rating value={source.rating} readOnly cancel={false}></Rating>
              <div className="flex align-items-center gap-3">
                <span className="flex align-items-center gap-2">
                  <i className="pi pi-tag"></i>
                  <span className="font-semibold">{source.category}</span>
                </span>
                <Tag value={source.inventoryStatus} severity={getSeverity(source)}></Tag>
              </div>
            </div>
            <div className="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
              <span className="text-2xl font-semibold">${source.price}</span>
              <Button icon="pi pi-shopping-cart" className="p-button-rounded" disabled={source.inventoryStatus === 'OUTOFSTOCK'}></Button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // <Avatar 
  //   icon={`pi pi-${source.icon}`} 
  //   size="normal"
  //    shape="circle"
  //    style={{ backgroundColor: colors[index] || randomColor }}
  //   />

  const gridItem = (source, index) => {
    const colors = ["#ff1744", "#2979ff", "#f50057", "#d500f9", "#651fff", "#1de9b6", "#ffea00", "#76ff03"];

    const randomColor = "#000000".replace(/0/g, function() { return (~~(Math.random() * 16)).toString(16); });

    const logoUrl = Boolean(source.logo_url) && source.logo_url.includes('http') && source.logo_url;

    // <>
    // className={s.actionIcons}
    //   <Button rounded icon={`pi pi-${source.icon}`} style={{ backgroundColor: colors[index] || randomColor, border: 'none' }} />
    //   <Button text size="large" icon="pi pi-bookmark" style={{ fontSize: '1.5rem', padding: 0 }} />
    // </>

    // {!logoUrl && (
    //   <div className={classNames("font-bold text-xl line-height-2", s.sourceName)}>
    //     {source.name}
    //   </div>
    // )}

    return (
      <div className={classNames("col-12 sm:col-12 lg:col-6 xl:col-3 p-2", s.squareCard)}>
        <div
          className={classNames("p-3 border-1 surface-border surface-card border-round", s.cardContents)}
        >

          <div className={classNames("font-bold text-xl line-height-2", s.sourceName)}>
            {logoUrl ? (
              <img src={logoUrl}
                // height={45}
                className={s.sourceImage}
                title={`Logo for ${source.name}`}
                alt={`Logo for ${source.name}`}
              />
            ) : (
              <div>
                {source.name} {source.initials && `(${source.initials})`}
              </div>
            )}
          </div>

          <div className="flex flex-column align-items-center py-1">

            <span className={s.description}>
              {source.description}
            </span>

            <div className={classNames(s.categories, 'w-full p-1')}>
              {Boolean(source?.categories?.length) && (
                source.categories.map((cat: string) => (
                  <Tag
                    key={cat}
                    className={s.category}
                    rounded
                    value={cat}
                  />
                ))
              )}
              {Boolean(source?.tags?.length) && (
                source.tags.map((tag: string) => (
                  <Tag
                    key={tag}
                    className={s.tag}
                    rounded
                    value={tag}
                  />
                ))
              )}
            </div>

            {Boolean(Object.keys(source?.urls || {}).length) && (
              <AvailableUrls urlObj={source.urls} />
            )}

            <div className={s.accessType}>
              <h4>Data Access:</h4>
              &nbsp;
              <span>
                {source.access_type}
              </span>
            </div>

          </div>

        </div>
      </div>
    );
  };

  const itemTemplate = (source, layout, index) => {
    if (!source) {
      return;
    }

    if (layout === 'list') return listItem(source, index);
    else if (layout === 'grid') return gridItem(source, index);
  };

  const listTemplate = (sources, layout) => {
    return <div className="grid grid-nogutter">{sources.map((source, index) => itemTemplate(source, layout, index))}</div>;
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
        value={sources}
        listTemplate={listTemplate}
        layout={'grid'}
        header={header()}
        sortField={sortField}
        sortOrder={sortOrder}
      />
      <ScrollTop />
    </div>
  )

  // paginator
  // rows={5}

}

export default Sources;
