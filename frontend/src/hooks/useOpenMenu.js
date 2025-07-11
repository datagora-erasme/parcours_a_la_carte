import { useContext } from 'react'
import MainContext from '../contexts/mainContext'

export default function useOpenMenu({
  activeMenu,
  setActiveMenu,
  setShowItineraryCalculation,
  setShowFindFreshness,
  setShowLayers,
  setShowReadMore,
  setShowBasemap,
  isBarOpen,
  setIsBarOpen
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

  function handleClickMenu(menuName) {
    if (typeof setIsBarOpen === 'function' && !isBarOpen) {
      setIsBarOpen(true);
    }

    if (activeMenu === menuName) {
      setActiveMenu(null)
    } else {
      setActiveMenu(menuName)
    }
  }

  function openMenu(menuName) {
    // console.log(menuName);
    handleClickMenu(menuName);
  
    setShowItineraryCalculation(menuName === 'itinerary');
    setShowFindFreshness(menuName === 'findFreshness');
    setShowLayers(menuName === 'layers');
    setShowReadMore(menuName === 'more');
  
    if (typeof setShowBasemap === 'function') {
      setShowBasemap(menuName === 'basemap');
    }
  
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
      if (menuName === 'basemap' && typeof setShowBasemap === 'function') {
        setShowBasemap(false);
      }
    };
    setHistory([...history, { fn: historyFn }]);
  
    if (menuName === 'itinerary') window.trackButtonClick('OpenCalculateItinerary');
    if (menuName === 'findFreshness') window.trackButtonClick('OpenFindFreshness');
    if (menuName === 'layers') window.trackButtonClick('OpenLayers');
    if (menuName === 'more') window.trackButtonClick('OpenMore');
    if (menuName === 'basemap') window.trackButtonClick('OpenBasemap');
  }
  

  return { openMenu }
}