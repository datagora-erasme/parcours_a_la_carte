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
                    />
                )
            }
            <ButtonShareFeedback />
            <Map />
        </div>
    );
}

export default Home;
