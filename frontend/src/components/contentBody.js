import BackButton from "./backButton";
import CalculateItinerary from "./calculateItinerary";
import FreshnessAroundUser from "./freshnessAroundUser";
import ListLayers from "./listLayers";
import ReadMore from "./readMore";
import CurrentItineraryDetails from "./currentItineraryDetails";

const ContentBody = ({
  activeMenu,
  setActiveMenu,
  showCurrentItineraryDetails,
  setShowCurrentItineraryDetails,
  setShowCircle,
  showItineraryCalculation,
  setShowItineraryCalculation,
  showFindFreshness,
  showLayers,
  showReadMore
}) => (
  <div className="w-full">
    {/* Retour */}
    {activeMenu && !showCurrentItineraryDetails && (
      <BackButton setActiveMenu={setActiveMenu} setShowCircle={setShowCircle} />
    )}

    <div className="max-h-[500px] overflow-auto w-full">
      {activeMenu === 'itinerary' && showItineraryCalculation && (
        <CalculateItinerary
          showItineraryCalculation={showItineraryCalculation}
          setShowItineraryCalculation={setShowItineraryCalculation}
        />
      )}

      {activeMenu === 'findFreshness' && showFindFreshness && <FreshnessAroundUser />}

      {activeMenu === 'layers' && showLayers && <ListLayers />}

      {activeMenu === 'more' && showReadMore && <ReadMore />}

      {activeMenu === 'itinerary' && showCurrentItineraryDetails && (
        <CurrentItineraryDetails
          setShowItineraryCalculation={setShowItineraryCalculation}
          setShowCurrentItineraryDetails={setShowCurrentItineraryDetails}
        />
      )}
    </div>
  </div>
)

export default ContentBody;