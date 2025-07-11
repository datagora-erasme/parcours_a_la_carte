import React, { useContext } from 'react';
import MainContext from '../contexts/mainContext';
import { FaArrowLeft, FaMapMarkerAlt, FaRegClock, FaQuestionCircle  } from 'react-icons/fa'

const PoiDetails = ({ showMenu, setShowFindFreshness, setShowPoiDetails }) => {
  const { poiDetails, isMobile } = useContext(MainContext)

    const transformOpeningHours = openinghours => {
        const new_s = openinghours.split(';');
        return (
            <span>
                {new_s.map((s, i) => {
                    return (
                        <span key={i}>
                            {s} <br />
                        </span>
                    );
                })}
            </span>
        );
    };

    return (
      <>
        {isMobile && 
            <button className="flex mb-2" onClick={() => {
                setShowPoiDetails(false);
                setShowFindFreshness(true)
            }}>
                <FaArrowLeft className="mt-1 mr-2 text-primary" />
                <div className="text-primary font-bold">Nouveau lieu</div>
            </button>
        }
                {poiDetails && (
          <div className="flex flex-col gap-2">
            <div className="font-bold pt-1 text-start">Votre sélection</div>
                        <h3 className="mb-2 text-start font-bold text-primary">{poiDetails.properties.nom}</h3>
                        {poiDetails.properties.adresse !== null &&
                            poiDetails.properties.adresse !== '' &&
                            poiDetails.properties.commune !== null &&
                            poiDetails.properties.commune !== '' && (
                                <div className="w-full flex gap-2">
                                    <FaMapMarkerAlt className="text-primary text-2xl" />
                                    <span className="flex text-left text-md italic">
                                        {poiDetails.properties.adresse},{'  ' + poiDetails.properties.commune}
                                    </span>
                                </div>
                            )}
                        {poiDetails.properties.openinghours !== null && poiDetails.properties.openinghours !== '' && (
                            <div className="w-full flex gap-2 my-1">
                                <FaRegClock className="text-primary text-2xl" />
                                <span className="flex text-left italic text-md">
                                    {transformOpeningHours(poiDetails.properties.openinghours)}
                                </span>
                            </div>
                        )}
                        {poiDetails.properties.commentaire !== null && poiDetails.properties.commentaire !== '' && (
                          <div className="w-full flex gap-2 items-start">
                            <FaQuestionCircle className="text-primary text-2xl flex-shrink-0" />
                            <span className="text-left italic text-md">{poiDetails.properties.commentaire}</span>
                          </div>
                        )}
                    </div>
                )}
        </>
    );
};

export default PoiDetails;
