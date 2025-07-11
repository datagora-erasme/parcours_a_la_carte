const BaseMapContent = ({ basemap, setBasemap, showBasemap, setShowBasemap }) => {
  const basemaps = [
    { key: 'grandlyon', label: 'Open Street Map', img: '/basemap_osm.png' },
    { key: 'positron', label: 'Positron Light', img: '/basemap_positron.png' },
    { key: 'satellite', label: 'Satellite', img: '/basemap_satellite.png' },
  ]
  return (
    <>
      <div className="flex flex-col gap-2 w-full pb-2">
        {basemaps.map((b) => (
          <button
          key={b.key}
          onClick={() => setBasemap(b.key)}
          className={`w-full text-left px-4 py-2 rounded-md ${
            basemap === b.key ? 'bg-primary text-white' : 'bg-white'
          }`}
        >
          <div className="flex items-center gap-2">
            <img src={b.img} className="w-12 h-auto rounded-sm" alt={b.label} />
            {b.label}
          </div>
        </button>
        ))}
        <div className="text-black flex justify-start w-full text-left">
          {basemap === "grandlyon"
            ? (<span>© OpenStreetMap contributors / <a className="!text-primary italic underline underline decoration-1" href="https://www.openstreetmap.org/copyright" target="blank">www.openstreetmap.org</a></span>)
            : basemap === "positron"
            ? (<span>© CARTO / <a className="!text-primary italic underline decoration-1" href="https://github.com/CartoDB/basemap-styles" target="blank">github.com/CartoDB</a></span>)
            : basemap === "satellite"
            ? (<span>© IGN – Geoportail / <a className="!text-primary italic underline decoration-1" href="hhttps://geoservices.ign.fr/" target="blank">www.geoservices.ign.fr</a></span>)
            : ""}
      </div>
      </div>
    </>
  )
}

export default BaseMapContent;