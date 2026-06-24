import BackButton from "./backButton";
import CalculateItinerary from "./calculateItinerary";
import FreshnessAroundUser from "./freshnessAroundUser";
import ListLayers from "./listLayers";
import ReadMore from "./readMore";
import CurrentItineraryDetails from "./currentItineraryDetails";
import BaseMapContent from "./baseMapContent";
import PoiDetails from "./poiDetails";

import { useContext } from 'react'
import MainContext from '../contexts/mainContext';

const ContentBody = ({
  activeMenu,
  setActiveMenu,
  showCurrentItineraryDetails,
  setShowCurrentItineraryDetails,
  setShowCircle,
  showItineraryCalculation,
  setShowItineraryCalculation,
  showFindFreshness,
  setShowFindFreshness,
  showLayers,
  showReadMore,
  showBasemap,
  basemap,
  setBasemap,
  showPoiDetails,
  setShowPoiDetails
}) => {
  
  const { isMobile } = useContext(MainContext);

    if (showPoiDetails && !isMobile) {
    return null;
  }

  return (
    <div className="w-full">
      {/* Retour */}
      {activeMenu && !showCurrentItineraryDetails && !showPoiDetails && (
        <BackButton setActiveMenu={setActiveMenu} setShowCircle={setShowCircle} />
      )}
  
      <div className={`w-full ${activeMenu=== 'findFreshness' ? '' : 'max-h-[450px] overflow-auto'}`}>
        {activeMenu === 'itinerary' && showItineraryCalculation && (
          <CalculateItinerary
            showItineraryCalculation={showItineraryCalculation}
            setShowItineraryCalculation={setShowItineraryCalculation}
          />
        )}
        {activeMenu === 'itinerary' && showCurrentItineraryDetails && (
          <CurrentItineraryDetails
            setShowItineraryCalculation={setShowItineraryCalculation}
            setShowCurrentItineraryDetails={setShowCurrentItineraryDetails}
          />
        )}
  
        {activeMenu === 'findFreshness' && showFindFreshness && <FreshnessAroundUser />}
        {activeMenu === 'findFreshness' && showPoiDetails && isMobile && <PoiDetails setShowFindFreshness={setShowFindFreshness} setShowPoiDetails={setShowPoiDetails} />}
  
        {activeMenu === 'layers' && showLayers && <ListLayers />}
  
        {activeMenu === 'more' && showReadMore && <ReadMore />}
  
        {activeMenu === "basemap" && showBasemap &&
          <>
          <div className="font-bold pt-1 mb-2 flex justify-start">Plans</div>
          <BaseMapContent basemap={basemap} setBasemap={setBasemap} />
          </>
        }
  
      </div>
    </div>
  )
}

export default ContentBody;