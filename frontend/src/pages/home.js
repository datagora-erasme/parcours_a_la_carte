import { useState, useContext } from 'react';
import Map from '../components/map';
import MainContext from '../contexts/mainContext';

import Content from '../components/content';
import ContentMobile from '../components/contentMobile';
import ButtonShareFeedback from '../components/buttonShareFeedback';

function Home() {
    const [showMenu, setShowMenu] = useState(true);
    const [activeMenu, setActiveMenu] = useState(null)
    const [showLayers, setShowLayers] = useState(false);
    const [showReadMore, setShowReadMore] = useState(false)
    const [showItineraryCalculation, setShowItineraryCalculation] = useState(false);
    const [showBasemap, setShowBasemap] = useState(false)
    const [basemap, setBasemap] = useState('grandlyon')
    const [isBarOpen, setIsBarOpen] = useState(true)
    const { isMobile } = useContext(MainContext);
    sessionStorage.clear(); //Clear session storage after refreshing the page

    return (
        <div style={{ position: 'relative' }} className="min-h-screen max-h-screen">
            {!isMobile ? 
                (
                    <Content
                        showMenu={showMenu}
                        setShowMenu={setShowMenu}
                        activeMenu={activeMenu}
                        setActiveMenu={setActiveMenu}
                        showLayers={showLayers}
                        setShowLayers={setShowLayers}
                        showReadMore={showReadMore}
                        setShowReadMore={setShowReadMore}
                        showItineraryCalculation={showItineraryCalculation}
                        setShowItineraryCalculation={setShowItineraryCalculation}
                    />
                )
                :
                (
                    <ContentMobile
                        activeMenu={activeMenu}
                        setActiveMenu={setActiveMenu}
                        showLayers={showLayers}
                        setShowLayers={setShowLayers}
                        showReadMore={showReadMore}
                        setShowReadMore={setShowReadMore}
                        showItineraryCalculation={showItineraryCalculation}
                        setShowItineraryCalculation={setShowItineraryCalculation}
                        showBasemap={showBasemap}
                        setShowBasemap={setShowBasemap}
                        setBasemap={setBasemap}
                        basemap={basemap}
                        isBarOpen={isBarOpen}
                        setIsBarOpen={setIsBarOpen}
                    />
                )
            }
            {isMobile &&
            <div className="absolute left-1/2 top-0 -translate-x-1/2 z-[9995] my-4 py-2 px-4 rounded-full shadow-md bg-bgWhite text-primary font-bold xs:text-base">
                Parcours à la carte
            </div>
            }
            <ButtonShareFeedback />
            <Map basemap={basemap} setBasemap={setBasemap} isBarOpen={isBarOpen} />
        </div>
    );
}

export default Home;
