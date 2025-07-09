import { useContext, useState } from 'react';
import { FaLayerGroup, FaWalking, FaSnowflake, FaMapMarkedAlt, FaInfoCircle, FaArrowRight, FaChevronUp, FaChevronDown } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';
import ContentBody from './contentBody';
import useOpenMenu from '../hooks/useOpenMenu';

const ContentMobile = ({
  activeMenu, setActiveMenu,
  showLayers, setShowLayers,
  setShowReadMore, showReadMore,
  showItineraryCalculation, setShowItineraryCalculation
}) => {
  const {
    showCurrentItineraryDetails,
    setShowCircle,
    setShowCurrentItineraryDetails,
    showFindFreshness,
    setShowFindFreshness,
  } = useContext(MainContext);

  const [isBarOpen, setIsBarOpen] = useState(true)

  const { openMenu } = useOpenMenu({
    activeMenu,
    setActiveMenu,
    setShowItineraryCalculation,
    setShowFindFreshness,
    setShowLayers,
    setShowReadMore,
  })

  return (
    <>
      {/* Content mobile */}
      {isBarOpen ? (
        <div style={{ zIndex: 9995 }} className="h-full w-screen">
          {!activeMenu ? (
            <div className="fixed bg-bgWhite bottom-[60px] z-[9995] w-full">
            {/* handle head */}
            <div className="w-full flex justify-center pb-2 bg-white">
              <button onClick={() => setIsBarOpen(false)}>
                <FaChevronDown className="text-black" />
              </button>
            </div>
            <div className="pr-[10px] pl-[4px] py-[11px] border-b-2 border-grey-500">
              <button
                onClick={() => openMenu('itinerary')}
                className="flex justify-between w-full px-4"
                >
                  <div className="flex gap-2 items-center">
                <FaWalking className={`text-xl text-primary`} />
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
                <FaSnowflake className={`text-xl text-primary`} />
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
                  <FaMapMarkedAlt className={`text-xl text-primary`} />
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
                  <FaInfoCircle className={`text-xl text-primary`} />
                  <span>En savoir plus</span>
                  </div>
                    <FaArrowRight className="text-primary mt-1" />
              </button>
            </div>
            </div>
          ) :
            (
            <div className="fixed bg-bgWhite bottom-[60px] left-0 z-[9995] w-full px-6 py-2 max-h-[350px] overflow-auto">
              {/* handle head */}
              <div className="w-full flex justify-center pb-2 bg-white">
                <button onClick={() => setIsBarOpen(false)}>
                  <FaChevronDown className="text-black" />
                </button>
              </div>
              {/* Contents */}
              <ContentBody
                activeMenu={activeMenu}
                setActiveMenu={setActiveMenu}
                showCurrentItineraryDetails={showCurrentItineraryDetails}
                setShowCurrentItineraryDetails={setShowCurrentItineraryDetails}
                setShowCircle={setShowCircle}
                showItineraryCalculation={showItineraryCalculation}
                setShowItineraryCalculation={setShowItineraryCalculation}
                showFindFreshness={showFindFreshness}
                showLayers={showLayers}
                showReadMore={showReadMore}
              />
            </div>
          )}
        </div>
      ) : (
        <div className="fixed bottom-[60px] w-full z-[9995] bg-white ">
        <button onClick={() => setIsBarOpen(true)} className="px-4 py-2">
          <FaChevronUp className="text-black" />
        </button>
      </div>
      )}
      {/* Nav */}
      <div className="fixed bottom-0 left-0 w-screen bg-white h-[60px] z-[9995]">
        <div className="h-full flex gap-2 justify-center items-center">
          <button
            onClick={() => openMenu('itinerary')}
            className={`p-1 h-full flex justify-center items-center flex-col`}
          >
            <FaWalking className={`text-xl ${activeMenu === 'itinerary' ? 'text-primary' : 'text-grayBtn'}`} />
            <span className={`text-xs mt-1 ${activeMenu === 'itinerary' ? 'text-primary font-bold' : 'text-grayBtn'}`}>Itinéraire</span>
          </button>
          <button
            onClick={() => openMenu('findFreshness')}
            className={`p-1 h-full flex justify-center items-center flex-col`}
            >
            <FaSnowflake className={`text-xl ${activeMenu === 'findFreshness' ? 'text-primary' : 'text-grayBtn'}`} />
            <span className={`text-xs mt-2 ${activeMenu === 'findFreshness' ? 'text-primary font-bold' : 'text-grayBtn'}`}>Lieux frais</span>
          </button>
          <button
            onClick={() => openMenu('layers')}
            className={`p-1 flex justify-center items-center flex-col`}
            >
            <FaMapMarkedAlt className={`text-xl ${activeMenu === 'layers' ? 'text-primary' : 'text-grayBtn'}`} />
            <span className={`text-xs mt-2 ${activeMenu === 'layers' ? 'text-primary font-bold' : 'text-grayBtn'}`}>Cartes</span>
          </button>
          <button
            onClick={() => openMenu('more')}
            className={`p-1 rounded-bl-lg flex justify-center items-center flex-col`}
            >
            <FaInfoCircle className={`text-xl ${activeMenu === 'more' ? 'text-primary' : 'text-grayBtn'}`} />
            <span className={`text-xs mt-2 ${activeMenu === 'more' ? 'text-primary font-bold' : 'text-grayBtn'}`}>Informations</span>
          </button>
          <button
            onClick={() => openMenu('baseMap')}
            className={`p-1 rounded-bl-lg flex justify-center items-center flex-col`}
            >
            <FaLayerGroup className={`text-xl ${activeMenu === 'basemap' ? 'text-primary' : 'text-grayBtn'}`} />
            <span className={`text-xs mt-2 ${activeMenu === 'basemap' ? 'text-primary font-bold' : 'text-grayBtn'}`}>Plans</span>
          </button>
        </div>
      </div>
    </>
  )
}

export default ContentMobile;