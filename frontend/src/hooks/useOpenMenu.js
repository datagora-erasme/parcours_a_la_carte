import { useContext } from 'react'
import MainContext from '../contexts/mainContext'

export default function useOpenMenu({
  activeMenu,
  setActiveMenu,
  setShowItineraryCalculation,
  setShowFindFreshness,
  setShowLayers,
  setShowReadMore,
}) {
  const {
    history,
    setHistory,
    setShowPoiDetails,
    setShowCircle,
    setZoomToUserPosition,
    setCurrentItinerary,
    setSelectedEndAddress,
    setEndAddress,
    setShowCurrentItineraryDetails,
    setSelectedLayers,
  } = useContext(MainContext)

  function handleClcikMenu(menuName) {
    if (activeMenu === menuName) {
      setActiveMenu(null)
    } else {
      setActiveMenu(menuName)
    }
  }

  function openMenu(menuName) {
    handleClcikMenu(menuName)

    setShowItineraryCalculation(menuName === 'itinerary');
    setShowFindFreshness(menuName === 'findFreshness');
    setShowLayers(menuName === 'layers');
    setShowReadMore(menuName === 'more');

    setShowPoiDetails(false);
    setShowCircle(menuName === 'findFreshness');
    setZoomToUserPosition(menuName === 'findFreshness');
    setCurrentItinerary(null);
    setSelectedEndAddress(null);
    setEndAddress('');
    setShowCurrentItineraryDetails(false);
    setSelectedLayers([]);

    const historyFn = () => {
      if (menuName === 'itinerary') setShowItineraryCalculation(false);
      if (menuName === 'findFreshness') setShowFindFreshness(false);
      if (menuName === 'layers') setShowLayers(false);
      if (menuName === 'more') setShowReadMore(false);
    };
    setHistory([...history, { fn: historyFn }]);

    if (menuName === 'itinerary') window.trackButtonClick('OpenCalculateItinerary');
    if (menuName === 'findFreshness') window.trackButtonClick('OpenFindFreshness');
    if (menuName === 'layers') window.trackButtonClick('OpenLayers');

  }

  return { openMenu }
}