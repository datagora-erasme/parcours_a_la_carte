import React, { useState, useContext, useCallback, useEffect } from 'react';
import { BiCurrentLocation } from 'react-icons/bi';
import MainContext from '../contexts/mainContext';
import axios from 'axios';
import _debounce from 'lodash/debounce';
import PoiDetails from './poiDetails';


const FreshnessAroundUser = () => {
    const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
    const [showStartSuggestions, setShowStartSuggestions] = useState(false);

    const {
        setZoomToUserPosition,
        setUserPosition,
        startAddress,
        setStartAddress,
        selectedStartAddress,
        setSelectedStartAddress,
        userAddress,
        radius,
        setRadius,
        setShowCircle,
        isMobile,
        poiDetails
    } = useContext(MainContext);

    const handleStartAddressAPI = query => {
        axios
            .get(`https://download.data.grandlyon.com/geocoding/photon-bal/api?q=${query}`)
            .then(response => {
                setStartAddressSuggestions(response.data.features);
                // setZoomToUserPosition(true);
                // setShowCircle(true);
            })
            .catch(error => {
                console.log(error);
            });
    };
    /*eslint-disable*/
    const debounceStartAddress = useCallback(_debounce(handleStartAddressAPI, 300), []);

    const addressName = ({ city, street, postcode, housenumber }) => {
        return `${housenumber ? housenumber : ''} ${street}, ${postcode} ${city.toUpperCase()}`;
    };

    const handleStartAddressChange = event => {
        const value = event.target.value;
        //replace double white space and then replace by +
        let query = value.replace(/\s{2,}/g, ' ');
        query = query.replace(/ /g, '+');
        setStartAddress(value);
        setSelectedStartAddress(null);
        if (query.length > 3) {
            debounceStartAddress(query);
        } else {
            setStartAddressSuggestions([]);
        }
    };

    // const findFreshnessAroundMe = () => {
    //     if (selectedStartAddress) {
    //         setZoomToUserPosition(true);
    //         setShowCircle(true);
    //     } else {
    //         alert('Veuillez activez votre géolocalisation pour utiliser cette fonctionnalité');
    //     }
    // };

        const findFreshnessAroundMe = () => {
            let url;
        if (selectedStartAddress) {
            // coordinates = [longitude, latitude]
            const lng = selectedStartAddress.geometry.coordinates[0];
            const lat = selectedStartAddress.geometry.coordinates[1];
            const zoom = 16;
            const url = `https://lesrefugesclimatiques.gogocarto.fr/map#/carte/@${lat},${lng},${zoom}z?cat=all`;
            window.open(url, '_blank');

        } else {
            url =`https://lesrefugesclimatiques.gogocarto.fr/map#/carte/@45.744,4.876,11z?cat=all`;
            window.open(url, '_blank');
        }
    };

    const handleSelectStartAddress = id => {
        for (let address of startAddressSuggestions) {
            if (address.properties.osm_id === id) {
                // setStartAddress(`${addressName(address.properties).slice(0, 30)}...`);
                setStartAddress(addressName(address.properties));
                setSelectedStartAddress(address);
                setStartAddressSuggestions([]);
            }
        }
    };

    const handleChangeRadius = e => {
        setRadius(e.target.value);
    };

    const handleSelectUserAddress = () => {
        if (userAddress) {
            // setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
            setStartAddress(userAddress.properties.label);
            setSelectedStartAddress(userAddress);
        } else {
            navigator?.geolocation?.getCurrentPosition(
                pos => {
                    const { latitude, longitude } = pos.coords;
                    setUserPosition([latitude, longitude]);
                },
                err => {
                    console.log(err);
                }
            );
        }
    };

    useEffect(() => {
        if (userAddress && startAddress === '') {
            // setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
            setStartAddress(userAddress.properties.label);
            setSelectedStartAddress(userAddress);
        }
    }, [userAddress]);

    const AdressSuggestionDisplay = ({ address }) => {

    const parts = address.split(',');
    const name = parts[0].trim();
    const restOfTheAddress = parts.slice(1).join(',').trim(); 

    return (
        <span className="whitespace-nowrap cursor-pointer">
        <span className="text-primary font-bold cursor-pointer">{name}</span>
        {restOfTheAddress && (
            <span className="italic">, {restOfTheAddress}</span>
        )}
        </span>
    );
    };


    return (
        <div className="w-full">

            <div className="font-bold pt-1 text-start">Trouver un lieu frais</div>
            <p className="text-sm mt-2">
                Cet outil vous renvoie vers la carte{' '}
                <a
                    href="https://lesrefugesclimatiques.gogocarto.fr/map#/carte/@45.744,4.876,11z?cat=all"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary font-bold underline"

                >
                    GoGoCarto
                </a>
                {' '}des Refuges climatiques de la Métropole.
            </p>
            <div className="flex flex-col">
                <label htmlFor="startAddress" className="block mb-1 mt-4 flex justify-between">
                    <p>Adresse</p>
                </label>
                <div className="relative flex gap-2">
                    <input
                        type="text"
                        id="startAddress"
                        name="startAddress"
                        value={startAddress}
                        onChange={handleStartAddressChange}
                        onFocus={() => setShowStartSuggestions(true)}
                        onBlur={() => setTimeout(() => setShowStartSuggestions(false), 200)}
                        className="main-input mb-2"
                        placeholder="Adresse"
                    />
                    {showStartSuggestions && (
                        <ul
                            id="startAddressSuggestions"
                            className="absolute z-10 w-full max-h-[200px] bg-white border-gray-300 rounded-md shadow-lg mt-12 md:mt-10 overflow-y-auto"
                            value={startAddress}
                        >
                        <div className="italic flex items-center cursor-pointer py-2" onClick={() => {
                            handleSelectUserAddress();
                            window.trackButtonClick(`FindFreshness_UseUserPosition`);
                        }}>
                            <BiCurrentLocation
                                size={30}
                                className="mt-2 cursor-pointer"
                            />
                            <span className="ml-1">Utiliser ma position</span> 
                            </div>
                            <hr></hr>
                            {startAddressSuggestions.map(suggestion => {
                                const name = addressName(suggestion.properties);
                                return (
                                    <li
                                        className="overflow-hidden pl-2 py-1 text-start cursor-pointer"
                                        key={suggestion.properties.osm_id}
                                        value={suggestion.properties.osm_id}
                                        onClick={() => handleSelectStartAddress(suggestion.properties.osm_id)}
                                    >
                                        {/* {name > 40 ? `${name.slice(0, 40)}...` : name} */}
                                        <AdressSuggestionDisplay address={name} />
                                    </li>
                                );
                            })}
                        </ul>
                    )}

                </div>
                {/*
                <div className="w-full mx-auto mb-2 flex flex-col gap-2 mt-2">
                    <div className="w-full flex justify-between">
                        <p>Distance</p>
                        <p className="font-bold">{radius} km</p>
                    </div>
                    <input
                        type="range"
                        min="0.2"
                        max="10"
                        step="0.2"
                        value={radius}
                        onChange={handleChangeRadius}
                        className="w-full h-1 bg-gray-300 rounded-full appearance-none custom-slider-freshness"
                    />
                    <div className="flex justify-between">
                        <span className="italic text-[#767676]">0.2 km</span>
                        <span className="italic text-[#767676]">10 km</span>
                    </div>
                </div>
                */}


                {/* <div className="w-full flex justify-center" onClick={() => window.trackButtonClick('FindFreshness')}>
                    {!selectedStartAddress ? (
                    <button
                        onClick={(e) => { e.stopPropagation(); findFreshnessAroundMe(); }}
                        className="text-white p-4 rounded-full shadow-md mt-2 font-bold bg-primary"
                        // le bouton doit être cliquable quand il est affiché
                        disabled={false}
                        >
                        Trouver les lieux frais
                        </button>
                    ) : (
                        !poiDetails && (
                        <div style={{ fontStyle: 'italic' }} className="text-center mt-2 text-primary">
                            Cliquez sur les différents points de la carte pour en savoir plus.
                        </div>
                        )
                    )}
                    
                </div> */}

                
                <div className="w-full flex justify-center mt-2">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            window.trackButtonClick('FindFreshness');
                            findFreshnessAroundMe();
                        }}
                        className="text-white p-4 rounded-full shadow-md font-bold bg-primary"
                    >
                            Voir la carte GoGoCarto
                    </button>                                      
                </div> 


                {/* {!isMobile && 
                <div className="mt-4">
                    <PoiDetails />
                </div>
                } */}
            </div>
        </div>
    );
};

export default FreshnessAroundUser;
