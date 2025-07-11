import React, { useContext } from 'react';
import { FaArrowLeft } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';

const BackButton = ({ setActiveMenu, setShowCircle }) => {
    const { history, setHistory, setPoiDetails } = useContext(MainContext);
    return (
        <button
            style={{ zIndex: 1000 }}
            onClick={() => {
                history[history.length - 1].fn();
                setHistory(history.slice(0, -1));
                setActiveMenu(null)
                setShowCircle(false)
                setPoiDetails(null)
            }}
            className="flex"
        >
            <FaArrowLeft className="mt-1 mr-2 text-primary" />
            <div className="text-primary font-bold">Retour</div>
        </button>
    );
};

export default BackButton;
