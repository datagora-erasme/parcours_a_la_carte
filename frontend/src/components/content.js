import { useContext, useState } from 'react';
import { FaArrowRight, FaWalking, FaMapMarkedAlt, FaInfoCircle, FaSnowflake } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';
import ContentBody from './contentBody';
import useOpenMenu from '../hooks/useOpenMenu';

function Content({
  setActiveMenu, activeMenu,
  showLayers, setShowLayers,
  showReadMore, setShowReadMore
}) {
  const [showItineraryCalculation, setShowItineraryCalculation] = useState(false);

  const {
    setShowCircle,
    setShowCurrentItineraryDetails,
    showPoiDetails,
    setShowPoiDetails,
    showFindFreshness,
    setShowFindFreshness,
    showCurrentItineraryDetails
  } = useContext(MainContext);
  
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
        {/* Container */}
        <div style={{ zIndex: 1000 }} className="fixed top-0 left-0 h-screen bg-transparent px-8 flex flex-col items-center">
          <div className="flex flex-row items-start">
            {/* vertical menu */}
            <div className="flex flex-col gap-2 mt-[40%]">
              <button
                onClick={() => openMenu('itinerary')}
                className={`p-1 w-[40px] h-[40px] rounded-tl-lg flex justify-center items-center ${activeMenu === 'itinerary' ? 'bg-primary' : 'bg-bgWhite'}`}
              >
                <FaWalking className={`text-xl ${
                  activeMenu === null
                    ? 'text-primary'
                    : activeMenu === 'itinerary'
                    ? 'text-white'
                    : 'text-grayBtn'
                }`} />
              </button>
              <button
                onClick={() => openMenu('findFreshness')}
                className={`p-1 w-[40px] h-[40px] flex justify-center items-center ${activeMenu === 'findFreshness' ? 'bg-primary' : 'bg-bgWhite'}`}
              >
                <FaSnowflake className={`text-xl ${
                  activeMenu === null
                    ? 'text-primary'
                    : activeMenu === 'findFreshness'
                    ? 'text-white'
                    : 'text-grayBtn'
                }`} />
              </button>
              <button
                onClick={() => openMenu('layers')}
                className={`p-1 w-[40px] h-[40px] flex justify-center items-center ${activeMenu === 'layers' ? 'bg-primary' : 'bg-bgWhite'}`}
              >
                <FaMapMarkedAlt className={`text-xl ${
                  activeMenu === null
                    ? 'text-primary'
                    : activeMenu === 'layers'
                    ? 'text-white'
                    : 'text-grayBtn'
                }`} />
              </button>
              <button
                onClick={() => openMenu('more')}
                className={`p-1 w-[40px] h-[40px] rounded-bl-lg flex justify-center items-center ${activeMenu === 'more' ? 'bg-primary' : 'bg-bgWhite'}`}
              >
                <FaInfoCircle className={`text-xl ${
                  activeMenu === null
                    ? 'text-primary'
                    : activeMenu === 'more'
                    ? 'text-white'
                    : 'text-grayBtn'
                }`} />
              </button>
            </div>
            {/*  */}
            <div className="flex flex-col items-center">
              {/* card title */}
              <div className="relative bg-bgWhite top-10 text-primary max-w-xs rounded-3xl h-[100px] p-[10px] max-w-xs min-w-[310px] z-50 shadow-md">
                <h1 className="text-2xl font-semibold">
                  Parcours à la carte
                </h1>
                <h3 className="text-base font-normal italic">
                  Une expérimentation ERASME pour la Métropole de Lyon
                </h3>
              </div>
              <div className="relative bg-bgWhite pt-10 pb-5 max-w-sm w-[355px] rounded-[20px] shadow-md min-h-[280px] max-h-[580px]">
                <div className="pt-4">
                  {/* menu */}
                  {!activeMenu && (
                    <>
                    <div className="px-[10px] py-[11px] border-b-2 border-grey-500">
                      <button
                        onClick={() => openMenu('itinerary')}
                        className="flex justify-between w-full px-4"
                      >
                        <div>Calculer un itinéraire piéton</div>
                          <FaArrowRight className="hidden md:block text-primary mt-1" />
                      </button>
                    </div>
                    <div className="px-[10px] py-[11px] border-b-2 border-grey-500">
                      <button
                        onClick={() => openMenu('findFreshness')}
                        className="flex justify-between w-full px-4"
                      >
                        <span>Trouver un lieu frais</span>
                          <FaArrowRight className="hidden md:block text-primary mt-1" />
                      </button>
                    </div>
                    <div className="px-[10px] py-[11px] border-b-2 border-grey-500">
                      <button
                          onClick={() => openMenu('layers')}
                          className="flex justify-between w-full px-4"
                      >
                        <span>Consulter les cartes</span>
                          <FaArrowRight className="hidden md:block text-primary mt-1" />
                      </button>
                    </div>
                    <div className="px-[10px] py-[11px] border-b-2 border-grey-500">
                        <button
                          onClick={() => openMenu('more')}
                          className="flex justify-between w-full px-4"
                        >
                          <span>En savoir plus</span>
                              <FaArrowRight className="hidden md:block text-primary mt-1" />
                      </button>
                    </div>
                    </>
                  )}
                  {/* Contents */}
                  <div className="flex flex-col items-start px-4">
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
                      showPoiDetails={showPoiDetails}
                      setShowPoiDetails={setShowPoiDetails}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    );
}

export default Content;
