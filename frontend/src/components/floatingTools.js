import BaseMapContent from "./baseMapContent";
import { FaTimes } from "react-icons/fa";

const FloatingTools = ({ showFloatingTools, setShowFloatingTools, basemap, setBasemap }) => {
  return (
    <>
      {showFloatingTools && 
        <div className="fixed bottom-28 right-14 bg-bgWhite min-h-200px z-[9995] w-[280px] flex flex-col items-start rounded-2xl shadow-md p-4">
          <div className="flex justify-between items-center w-full mb-2">
            <h1 className="text-2xl font-bold text-primary">
              Plans
            </h1>
            <FaTimes className="text-lg" onClick={() => setShowFloatingTools(false)} />
          </div>
          <BaseMapContent basemap={basemap} setBasemap={setBasemap} />
        </div>
      }
    </>
  )
}

export default FloatingTools;