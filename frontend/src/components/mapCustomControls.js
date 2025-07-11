import { useMap } from 'react-leaflet';
import { useContext } from 'react'
import { FaCrosshairs, FaLayerGroup, FaPlus, FaMinus } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';

export default function MapCustomControls({ setShowFloatingTools }) {
  const map = useMap();
  const { isMobile } = useContext(MainContext);

  return (
    <div className={`absolute right-4 flex flex-col gap-2 z-[9994] ${isMobile ? 'bottom-28' : 'bottom-8'}`}>
      {/* Btn center */}
      <button
        onClick={() => map.locate({ setView: true })}
        className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
      >
        <FaCrosshairs className="text-primary text-lg" />
      </button>

      {/* Btn layers */}
      {!isMobile && 
        <button
          onClick={() => {
            console.log('click');
            setShowFloatingTools(true)
          }}
          className="bg-white w-8 h-8 rounded-full shadow-md flex items-center justify-center"
        >
          <FaLayerGroup className="text-primary text-lg" />
        </button>
      }

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
