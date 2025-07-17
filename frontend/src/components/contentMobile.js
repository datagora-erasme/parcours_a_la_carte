import { useContext, useRef, useState } from 'react';
import { FaLayerGroup, FaWalking, FaSnowflake, FaMapMarkedAlt, FaInfoCircle, FaArrowRight, FaChevronUp, FaChevronDown } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';
import ContentBody from './contentBody';
import useOpenMenu from '../hooks/useOpenMenu';

const ContentMobile = ({
  activeMenu, setActiveMenu,
  showLayers, setShowLayers,
  setShowReadMore, showReadMore,
  showItineraryCalculation, setShowItineraryCalculation,
  showBasemap, setShowBasemap,
  basemap, setBasemap,
  isBarOpen, setIsBarOpen,
}) => {
  const {
    showCurrentItineraryDetails,
    setShowCircle,
    setShowCurrentItineraryDetails,
    showFindFreshness,
    setShowFindFreshness,
    leafletMap,
    showPoiDetails,
    setShowPoiDetails,
  } = useContext(MainContext);

  const { openMenu } = useOpenMenu({
    activeMenu,
    setActiveMenu,
    setShowItineraryCalculation,
    setShowFindFreshness,
    setShowLayers,
    setShowReadMore,
    setShowBasemap,
    isBarOpen,
    setIsBarOpen,
  })

  const contentRef = useRef(null)
  const [panelHeight, setPanelHeight] = useState(300)

  const handleClose = () => {
    setIsBarOpen(false)
    if (contentRef.current) {
      const height = contentRef.current.offsetHeight
      setPanelHeight(height)
      if (leafletMap) {
        leafletMap.panBy([0, -height], { animate: true })
      }
    }
  }

  const handleOpen = () => {
    setIsBarOpen(true)
    if (leafletMap) {
      leafletMap.panBy([0, panelHeight], { animated: true })
    }
  }

  return (
    <>
      {/* MOBILE CONTAINER */}
      {isBarOpen && (
        <>
          {/* Wrapper bloc */}
          <div ref={contentRef} className="fixed bottom-[60px] left-0 w-full z-[9995] bg-bgWhite flex flex-col rounded-tl-[20px] rounded-tr-[20px]">
            {/* Handle */}
            <div className="w-full flex justify-center rounded-tl-[20px] rounded-tr-[20px]">
              <button
                onClick={handleClose}
                className="bg-white w-full flex justify-center py-2 rounded-tl-[20px] rounded-tr-[20px]"
              >
                <FaChevronDown className="text-black" />
              </button>
            </div>
  
            {/* scroll content */}
            <div className={`overflow-auto max-h-[350px] w-full py-2 ${activeMenu ? 'px-4' : 'px-1'}`}>
              {!activeMenu ? (
                <>
                  <div className="pr-[10px] pl-[4px] py-[11px] border-b-2 border-grey-500">
                    <button
                      onClick={() => openMenu('itinerary')}
                      className="flex justify-between w-full px-4"
                    >
                      <div className="flex gap-2 items-center">
                        <FaWalking className="text-xl text-primary" />
                        <div>Calculer un itinéraire piéton</div>
                      </div>
                      <FaArrowRight className="text-primary mt-1" />
                    </button>
                  </div>
  
                  <div className="pr-[10px] pl-[4px] py-[11px] border-b-2 border-grey-500">
                    <button
                      onClick={() => openMenu('findFreshness')}
                      className="flex justify-between w-full px-4"
                    >
                      <div className="flex gap-2 items-center">
                        <FaSnowflake className="text-xl text-primary" />
                        <span>Trouver un lieu frais</span>
                      </div>
                      <FaArrowRight className="text-primary mt-1" />
                    </button>
                  </div>
  
                  <div className="pr-[10px] pl-[4px] py-[11px] border-b-2 border-grey-500">
                    <button
                      onClick={() => openMenu('layers')}
                      className="flex justify-between w-full px-4"
                    >
                      <div className="flex gap-2 items-center">
                        <FaMapMarkedAlt className="text-xl text-primary" />
                        <span>Consulter les cartes</span>
                      </div>
                      <FaArrowRight className="text-primary mt-1" />
                    </button>
                  </div>
  
                  <div className="pr-[10px] pl-[4px] py-[11px] border-b-2 border-grey-500">
                    <button
                      onClick={() => openMenu('more')}
                      className="flex justify-between w-full px-4"
                    >
                      <div className="flex gap-2 items-center">
                        <FaInfoCircle className="text-xl text-primary" />
                        <span>En savoir plus</span>
                      </div>
                      <FaArrowRight className="text-primary mt-1" />
                    </button>
                  </div>
                </>
              ) : (
                <ContentBody
                  activeMenu={activeMenu}
                  setActiveMenu={setActiveMenu}
                  showCurrentItineraryDetails={showCurrentItineraryDetails}
                  setShowCurrentItineraryDetails={setShowCurrentItineraryDetails}
                  setShowCircle={setShowCircle}
                  showItineraryCalculation={showItineraryCalculation}
                  setShowItineraryCalculation={setShowItineraryCalculation}
                  showFindFreshness={showFindFreshness}
                  setShowFindFreshness={setShowFindFreshness}
                  showLayers={showLayers}
                  showReadMore={showReadMore}
                  showBasemap={showBasemap}
                  setShowBasemap={setShowBasemap}
                  basemap={basemap}
                  setBasemap={setBasemap}
                  showPoiDetails={showPoiDetails}
                  setShowPoiDetails={setShowPoiDetails}
                />
              )}
            </div>
          </div>
        </>
      )}
  
      {/* when close */}
      {!isBarOpen && (
        <div className="fixed bottom-[60px] w-full z-[9995] flex justify-center rounded-tl-[20px] rounded-tr-[20px]">
          <button
            onClick={handleOpen}
            className="bg-white w-full py-2 flex justify-center rounded-tl-[20px] rounded-tr-[20px]"
          >
            <FaChevronUp className="text-black" />
          </button>
        </div>
      )}
  
      {/* NAV BAR fixe en bas */}
      <div className="fixed bottom-0 left-0 w-screen bg-white h-[60px] z-[9995]">
        <div className="h-full flex gap-2 justify-center items-center">
          <button
            onClick={() => openMenu('itinerary')}
            className={`p-1 h-full flex justify-center items-center flex-col`}
          >
            <FaWalking
              className={`text-xl ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'itinerary'
                  ? 'text-primary'
                  : 'text-grayBtn'
              }`}
            />
            <span
              className={`text-xs mt-1 ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'itinerary'
                  ? 'text-primary font-bold'
                  : 'text-grayBtn'
              }`}
            >
              Itinéraire
            </span>
          </button>
  
          <button
            onClick={() => openMenu('findFreshness')}
            className={`p-1 h-full flex justify-center items-center flex-col`}
          >
            <FaSnowflake
              className={`text-xl ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'findFreshness'
                  ? 'text-primary'
                  : 'text-grayBtn'
              }`}
            />
            <span
              className={`text-xs mt-2 ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'findFreshness'
                  ? 'text-primary font-bold'
                  : 'text-grayBtn'
              }`}
            >
              Lieux frais
            </span>
          </button>
  
          <button
            onClick={() => openMenu('layers')}
            className={`p-1 flex justify-center items-center flex-col`}
          >
            <FaMapMarkedAlt
              className={`text-xl ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'layers'
                  ? 'text-primary'
                  : 'text-grayBtn'
              }`}
            />
            <span
              className={`text-xs mt-2 ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'layers'
                  ? 'text-primary font-bold'
                  : 'text-grayBtn'
              }`}
            >
              Cartes
            </span>
          </button>
  
          <button
            onClick={() => openMenu('more')}
            className={`p-1 flex justify-center items-center flex-col`}
          >
            <FaInfoCircle
              className={`text-xl ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'more'
                  ? 'text-primary'
                  : 'text-grayBtn'
              }`}
            />
            <span
              className={`text-xs mt-2 ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'more'
                  ? 'text-primary font-bold'
                  : 'text-grayBtn'
              }`}
            >
              Informations
            </span>
          </button>
  
          <button
            onClick={() => openMenu('basemap')}
            className={`p-1 flex justify-center items-center flex-col`}
          >
            <FaLayerGroup
              className={`text-xl ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'basemap'
                  ? 'text-primary'
                  : 'text-grayBtn'
              }`}
            />
            <span
              className={`text-xs mt-2 ${
                activeMenu === null
                  ? 'text-primary'
                  : activeMenu === 'basemap'
                  ? 'text-primary font-bold'
                  : 'text-grayBtn'
              }`}
            >
              Plans
            </span>
          </button>
        </div>
      </div>
    </>
  );
  
  
}

export default ContentMobile;