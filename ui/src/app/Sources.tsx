'use client';

import { useState, useEffect } from "react";
import { ProductService } from "./mock_product_data";
import { Button } from "primereact/button";
import { DataView, DataViewLayoutOptions } from "primereact/dataview";
import { Rating } from 'primereact/rating';
import { Tag } from 'primereact/tag';
import { Dropdown } from 'primereact/dropdown';
import { classNames } from 'primereact/utils';

import { ScrollTop } from 'primereact/scrolltop';
import { Carousel } from 'primereact/carousel';

import s from './sources.module.scss';
import { Panel } from 'primereact/panel';

function lower(s: string) {
  return s ? s.toLowerCase() : null;
}

interface CategoryModel {
  id: string,
  name: string,
  code: string,
  image: string,
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
        {['home_page'].map((uriName) => urlObj[0] && (
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
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedSource, setSelectedSource] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearchStarted, setIsSearchStarted] = useState(false);
  
  const [panelWidth, setPanelWidth] = useState("20%");
  const [showGrids, setShowGrids] = useState(true);

  const [jobId, setJobId] = useState(null);
  const [logs, setLogs] = useState([]);

  const onSourceClick = (source) => {
    setSelectedSource(source);
    setIsDrawerOpen(true);
  };
  const [layout, setLayout] = useState('grid');

  const [sortKey, setSortKey] = useState('');
  const [sortOrder, setSortOrder] = useState(0);
  const [sortField, setSortField] = useState('');
  const sortOptions = [
    { label: 'Desc', value: '!name' },
    { label: 'Asc', value: 'name' }
  ];

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

  const runJvoyJob = async (event) => {
    if (event.type === 'submit') {
      event.preventDefault();
    }

    const firstUrlKey = Object.keys(selectedSource.urls)[0];
    const firstUrl = selectedSource.urls[firstUrlKey];

    const response = await fetch('http://localhost:8001/api/jvoy/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_task: searchTerm,
        url: firstUrl
      })
    });
  
    if (!response.ok) {
      console.error('Failed to run jvoy job');
      return;
    }
  
    setPanelWidth("100%");
    setShowGrids(false);

    const data = await response.json();
    console.log('Job ID:', data.job_id);

    setJobId(data.job_id);    
  };

  useEffect(() => {
    if (!jobId) {
      return;
    }
  
    const timeoutId = setTimeout(() => {
      const intervalId = setInterval(async () => {
        const statusResponse = await fetch(`http://localhost:8001/api/lib/status?job_id=${jobId}`);
  
        if (!statusResponse.ok) {
          console.error('Failed to fetch job status');
          return;
        }
  
        const statusData = await statusResponse.json();
  
        // If the job is not running/started, stop polling
        if (statusData.job.status !== 'running' && statusData.job.status !== 'started') {
          clearInterval(intervalId);
          return;
        }
  
        const logsResponse = await fetch(`http://localhost:8001/api/jvoy/logs/${jobId}`);
  
        if (!logsResponse.ok) {
          console.error('Failed to fetch logs');
          return;
        }
  
        const newLogs = await logsResponse.json();
        setLogs(newLogs);
      }, 5000);  // Poll every 5 seconds
  
      return () => clearInterval(intervalId);
    }, 1000);  // Start polling after 10 seconds
  
    return () => clearTimeout(timeoutId);
  }, [jobId]);


  const listItem = (source, index) => {
    return (

      <div className="col-12" key={source.id} onClick={() => onSourceClick(source)}>
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

  const gridItem = (source, index) => {
    const colors = ["#ff1744", "#2979ff", "#f50057", "#d500f9", "#651fff", "#1de9b6", "#ffea00", "#76ff03"];

    const randomColor = "#000000".replace(/0/g, function() { return (~~(Math.random() * 16)).toString(16); });

    const logoUrl = Boolean(source.logo_url) && source.logo_url.includes('http') && source.logo_url;

    const descriptions = source.content["Web Page Descriptions"];

    const sourceUrls = Object.keys(source.content["Information on Links on Web Page"]);

    return (
        <div 
          className={classNames("col-12 sm:col-12 lg:col-6 xl:col-3 p-2", s.squareCard, 
            { [s.highlight]: source.id === selectedSource?.id })} 
          onClick={() => onSourceClick(source)}
        >
        <div
          className={classNames("p-3 border-1 surface-border surface-card border-round", s.cardContents)}
        >

          <div className={classNames("font-bold text-xl line-height-2", s.sourceName)}>
            {logoUrl ? (
              <img src={logoUrl}
                // height={45}
                className={s.sourceImage}
                title={`Logo for ${descriptions.name}`}
                alt={`Logo for ${descriptions.name}`}
              />
            ) : (
              <div>
                {descriptions.name} {descriptions.initials && `(${descriptions.initials})`}
              </div>
            )}
          </div>

          <div className="flex flex-column align-items-center py-1">

            <span className={s.description}>
              {descriptions.purpose}
            </span>

            {Boolean(sourceUrls.length) && (
              <AvailableUrls urlObj={sourceUrls} />
            )}

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
      <div className="flex">
        <Dropdown
          options={sortOptions}
          value={sortKey}
          optionLabel="label"
          placeholder="Sort By Name"
          onChange={onSortChange}
          className="w-full sm:w-14rem mr-4"
        />
        <DataViewLayoutOptions
          layout={layout}
          onChange={(e) => setLayout(e.value)}
        />
      </div>
    );
  };

  const logsCarouselTemplate = (log) => {
    const logLines = log.split('\n');
    return (
      <div className="carousel-item-content">
        {logLines.map((line, i) => {
          const lineHtml = line.trim();
          if (lineHtml.startsWith('<img')) {
            return <div className="carousel-item-image" key={i} dangerouslySetInnerHTML={{ __html: lineHtml }} />;
          } else {
            return <p key={i} dangerouslySetInnerHTML={{ __html: lineHtml }} />;
          }
        })}
      </div>
    );
  }

  return (
    <div className={s.root}>
      <h4>Sources</h4>
  
      <div className={`${s.content} ${isDrawerOpen ? s.withDrawer : ''}`}>
    {showGrids && (
          <DataView
            className={s.dataview}
            value={sources}
            listTemplate={listTemplate}
            layout={'grid'}
            header={header()}
            sortField={sortField}
            sortOrder={sortOrder}
          />
      )}
  
        {isDrawerOpen && (
          <aside className={`${s.drawer} ${isDrawerOpen ? s.open : ''}`} style={{ width: panelWidth }}>
            <Panel header="Source Details">
                  <button className={s.closeButton} onClick={() => {setIsDrawerOpen(false); setShowGrids(true);}}>
                    ×
                  </button>
                  {selectedSource && (
                    <div>
                      <h3>{selectedSource.name}</h3>
                      <p className={s.drawerDescription}>{selectedSource.description}</p>
                    </div>
                  )}
                  <div className={s.searchBar}>
                  <form onSubmit={(e) => { runJvoyJob(e); setIsSearchStarted(true); }} className={s.searchBar}>
                      <textarea 
                          className={s.searchInput} 
                          placeholder="Search datasource..." 
                          value={searchTerm}
                          onChange={e => setSearchTerm(e.target.value)}
                      />
                      <button type="submit" className={s.enterButton}>⏎</button>
                    </form>
                  </div>
                  {isSearchStarted && (
                    <div className={s.logContainer}>
                      {logs.map((log, index) => (
                        <div key={index} className={s.logChunk} dangerouslySetInnerHTML={{ __html: log }}>
                        </div>
                      ))}
                    </div>
                  )}
            </Panel>
          </aside>
        )}
      </div>
  
      <ScrollTop />
    </div>
  )
}

export default Sources;
