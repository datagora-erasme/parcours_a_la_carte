import { useMap } from 'react-leaflet';
import { FaCrosshairs, FaLayerGroup, FaPlus, FaMinus } from 'react-icons/fa';

export default function MapCustomControls() {
  const map = useMap();

  return (
    <div className="absolute bottom-8 right-4 flex flex-col gap-2 z-[9994]">
      {/* Btn center */}
      <button
        onClick={() => map.locate({ setView: true })}
        className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
      >
        <FaCrosshairs className="text-primary text-lg" />
      </button>

      {/* Btn layers */}
      <button
        onClick={() => console.log('Toggle layers')}
        className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
      >
        <FaLayerGroup className="text-primary text-lg" />
      </button>

      {/* Btn zoom in */}
      <button
        onClick={() => map.zoomIn()}
        className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
      >
        <FaPlus className="text-primary text-lg" />
      </button>

      {/* Btn zoom out */}
      <button
        onClick={() => map.zoomOut()}
        className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
      >
        <FaMinus className="text-primary text-lg" />
      </button>
    </div>
  );
}
