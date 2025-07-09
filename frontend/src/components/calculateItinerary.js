import React, { useCallback, useContext, useEffect, useState } from 'react';
import axios from 'axios';
// import _debounce from 'lodash/debounce';
import { FaSnowflake } from 'react-icons/fa';
import { HiSpeakerXMark } from 'react-icons/hi2';
import { TbFlowerOff } from 'react-icons/tb';
import { MdPhotoCamera } from 'react-icons/md';

import { BiCurrentLocation } from 'react-icons/bi';
import MainContext from '../contexts/mainContext';

const CalculateItinerary = ({ showItineraryCalculation, setShowItineraryCalculation, showCurrentItineraryDetails }) => {
    const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
    const [endAddressSuggestions, setEndAddressSuggestions] = useState([]);
    const [showStartSuggestions, setShowStartSuggestions] = useState(false);
    const [showEndSuggestions, setShowEndSuggestions] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const {
        setCurrentItinerary,
        userAddress,
        history,
        setHistory,
        setShowCurrentItineraryDetails,
        selectedStartAddress,
        setSelectedStartAddress,
        selectedEndAddress,
        setSelectedEndAddress,
        startAddress,
        setStartAddress,
        endAddress,
        setEndAddress,
        setUserPosition,
        roundGeographicalCoordinatesOnItineraries,
        criteria,
        setCriteria,
        setCurrentItineraryStartPointUsedForCalculation,
        setCurrentItineraryEndPointUsedForCalculation,
    } = useContext(MainContext);

    /**
     * Check if 2 addresses are the same
     */
    const isSameAddress = (baseAddress, candidateAddress) => {
        if (baseAddress?.properties?.osm_id) {
            return baseAddress.properties.osm_id === candidateAddress.properties.osm_id;
        }
        if (baseAddress?.properties?.banId) {
            //Case where the address comes from user position instead of the user input.
            const baseAddressFormatted = `${baseAddress.properties.name} ${baseAddress.properties.citycode}`.toUpperCase();
            const cadidateAddressFormatted =
                `${candidateAddress.properties.housenumber} ${candidateAddress.properties.name} ${candidateAddress.properties.extra.insee}`.toUpperCase();

            return baseAddressFormatted === cadidateAddressFormatted;
        } else return false;
    };

    const handleStartAddressAPI = query => {
        axios
            .get(`https://download.data.grandlyon.com/geocoding/photon-bal/api?q=${query}`)
            .then(response => {
                //If an end address is already select, we filter it from the start addresses suggestions. User can't be able to choose the same address
                setStartAddressSuggestions(response.data.features.filter(address => !isSameAddress(selectedEndAddress, address)));
            })
            .catch(error => {
                console.log(error);
            });
    };

    const handleEndAddressAPI = query => {
        axios
            .get(`https://download.data.grandlyon.com/geocoding/photon-bal/api?q=${query}`)
            .then(response => {
                //If a start address is already select, we filter it from the end addresses suggestions. User can't be able to choose the same address
                setEndAddressSuggestions(response.data.features.filter(address => !isSameAddress(selectedStartAddress, address)));
            })
            .catch(error => {
                console.log(error);
            });
    };

    const debounceStartAddress = useCallback(handleStartAddressAPI, [selectedEndAddress]);
    const debounceEndAddress = useCallback(handleEndAddressAPI, [selectedStartAddress]);

    const handleStartAddressChange = event => {
        const value = event.target.value;
        let query = value.replace(/\s{2,}/g, ' ').replace(/ /g, '+');
        setStartAddress(value);
        setSelectedStartAddress(null);
        if (query.length > 3) {
            debounceStartAddress(query);
        } else {
            setStartAddressSuggestions([]);
        }
    };

    const handleEndAddressChange = event => {
        const value = event.target.value;
        let query = value.replace(/\s{2,}/g, ' ').replace(/ /g, '+');
        setEndAddress(value);
        setSelectedEndAddress(null);
        if (query.length > 3) {
            debounceEndAddress(query);
        } else {
            setEndAddressSuggestions([]);
        }
    };

    const addressName = ({ city, street, postcode, housenumber, name, osm_value }) => {
        const displayName = () => {
            return osm_value !== 'street' && osm_value !== 'house';
        };

        return `${displayName() ? `${name}: ` : ''}${housenumber ? housenumber : ''} ${street}, ${postcode} ${city.toUpperCase()}`;
    };

    const handleSelectStartAddress = id => {
        for (let address of startAddressSuggestions) {
            if (address.properties.osm_id === id) {
                setStartAddress(`${addressName(address.properties).slice(0, 30)}...`);
                setSelectedStartAddress(address);
                setStartAddressSuggestions([]);
            }
        }
    };

    const handleSelectEndAddress = id => {
        for (let address of endAddressSuggestions) {
            if (address.properties.osm_id === id) {
                setEndAddress(addressName(address.properties));
                setSelectedEndAddress(address);
                setEndAddressSuggestions([]);
                sessionStorage.setItem('previousEndAddress', JSON.stringify(address));
            }
        }
    };

    const handlePreviousEndAddress = () => {
        const previousEndAddress = JSON.parse(sessionStorage.getItem('previousEndAddress'));
        if (!previousEndAddress) return;
        setEndAddress(addressName(previousEndAddress.properties));
        setSelectedEndAddress(previousEndAddress);
        setEndAddressSuggestions([]);
    };

    const handleSelectUserAddress = () => {
        if (userAddress) {
            setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
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

    const calculateItinerary = () => {
        setIsLoading(true);
        setShowCurrentItineraryDetails(false);
        axios
            .get(`${process.env.REACT_APP_URL_SERVER}/itinerary/`, {
                params: {
                    start: {
                        lat: selectedStartAddress.geometry.coordinates[1],
                        lon: selectedStartAddress.geometry.coordinates[0],
                    },
                    end: {
                        lat: selectedEndAddress.geometry.coordinates[1],
                        lon: selectedEndAddress.geometry.coordinates[0],
                    },
                    //criteria : criteria ? criteria.join(',') : {}
                    //criteria : criteria.map((n) => `${n}`).join('&')
                    criteria,
                },
            })
            .then(response => {
                const roundIt = roundGeographicalCoordinatesOnItineraries(response.data["itinerary"]);
                setCurrentItinerary(roundIt);
                setCurrentItineraryStartPointUsedForCalculation(response.data["nearest_node_start"])
                setCurrentItineraryEndPointUsedForCalculation(response.data["nearest_node_end"])
                setIsLoading(false);
                setShowItineraryCalculation(false);
                setShowCurrentItineraryDetails(true);
                setHistory([
                    ...history,
                    {
                        fn: () => {
                            setShowCurrentItineraryDetails(false);
                            setShowItineraryCalculation(true);
                        },
                    },
                ]);
            })
            .catch(error => {
                console.error(error);
            });
    };

    const handleEndFocus = () => {
        setShowEndSuggestions(true);
    };

    useEffect(() => {
        if (userAddress && startAddress === '') {
            setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
            setSelectedStartAddress(userAddress);
        }

        if (sessionStorage?.getItem('previousEndAddress')) {
            handlePreviousEndAddress();
        }
    }, [userAddress]);

    const toggleCriteria = criterion => {
        if (criteria.includes(criterion)) {
            setCriteria(criteria.filter(c => c !== criterion));
        } else {
            setCriteria([...criteria, criterion]);
        }
    };

    /**
     * Address style display on the UI.
     * Note that other styles should be applied to the parent html tag
     */
    const AdressSuggestionDisplay = ({ address }) => {
        /**
         * Extracts the 'name' part of the address if it exists.
         * This regex is based on the current configuration on the `addressName` function.
         * If the `addressName` function changes, change this accordingly
         */
        const hasName = address.match(/^([^:]+: )\s*(.*)$/);
        const name = hasName ? hasName[1] : '';
        const restOfTheAddress = hasName ? hasName[2].trim() : address;

        return (
            <span className="whitespace-nowrap">
                <i>{name}</i>
                {restOfTheAddress}
            </span>
        );
    };

    return (
        <>
        <div className="w-full">
        
        <div className="font-bold pt-1 text-start">Calculer un itinéraire piéton</div>
          <label htmlFor="startAddress" className="block mb-1 mt-4 flex">
              Départ
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
                    className="main-input"
                    placeholder="Adresse de départ"
                />
                {showStartSuggestions && (
                    <ul
                        id="startAddressSuggestions"
                        className="absolute z-10 w-full max-h-[200px] bg-white border-gray-300 rounded-md shadow-lg mt-12 md:mt-10 overflow-y-scroll"
                        value={startAddress}
                    >
                        {startAddressSuggestions.map(suggestion => {
                            const name = addressName(suggestion.properties);
                            return (
                                <li
                                    className="overflow-hidden text-ellipsis pl-2"
                                    key={suggestion.properties.osm_id}
                                    value={suggestion.properties.osm_id}
                                    onClick={() => handleSelectStartAddress(suggestion.properties.osm_id)}
                                >
                                    <AdressSuggestionDisplay address={name} />
                                </li>
                            );
                        })}
                    </ul>
                )}
                <BiCurrentLocation
                    size={30}
                    className="mt-1 cursor-pointer"
                    onClick={() => {
                        handleSelectUserAddress();
                        window.trackButtonClick(`CalculateItinerary_UseUserPosition`);
                    }}
                />
            </div>
            <label htmlFor="endAddress" className="block my-2 flex ">
                Arrivée
            </label>
            <div className="relative">
                <input
                    type="text"
                    id="endAddress"
                    name="endAddress"
                    value={endAddress}
                    onChange={handleEndAddressChange}
                    onFocus={() => handleEndFocus(true)}
                    onBlur={() => setTimeout(() => handleEndFocus(false), 200)}
                    className="main-input mb-4"
                    placeholder="Adresse d'arrivée"
                />
                {showEndSuggestions && (
                    <ul
                        id="endAddressSuggestions"
                        className="absolute z-10 w-full max-h-[200px] bg-white border-gray-300 rounded-md shadow-lg mt-0 overflow-y-scroll"
                        value={endAddress}
                    >
                        {endAddressSuggestions.map(suggestion => {
                            const name = addressName(suggestion.properties);
                            return (
                                <li
                                    className="overflow-hidden text-ellipsis pl-2"
                                    key={suggestion.properties.osm_id}
                                    value={suggestion.properties.osm_id}
                                    onClick={() => handleSelectEndAddress(suggestion.properties.osm_id)}
                                >
                                    <AdressSuggestionDisplay address={name} />
                                </li>
                            );
                        })}
                    </ul>
                )}
            </div>

            <div>
                <span className="block mb-1 mt-4 flex">Critères</span>
                <div className="flex justify-center items-center mb-4 ">
                    <button
                        onClick={() => {
                            toggleCriteria('frais');
                            window.trackButtonClick(`CalculateItinerary_PlusAuFrais`);
                        }}
                        className={`px-4 py-3 inline-flex items-center mx-1 text-sm rounded-full transition duration-300 ${criteria.includes('frais') ? 'bg-black text-white' : 'bg-white text-black shadow-md'}`}
                    >
                        <FaSnowflake className="mr-2 text-lg" /> Plus au frais
                    </button>

                    <button
                        onClick={() => {
                            toggleCriteria('pollen');
                            window.trackButtonClick(`CalculateItinerary_MoinsDePollen`);
                        }}
                        className={`px-4 py-3 inline-flex items-center mx-1 text-sm rounded-full transition duration-300 ${criteria.includes('pollen') ? 'bg-black text-white' : 'bg-white text-black shadow-md'}`}
                    >
                        <TbFlowerOff className="mr-2 text-lg" /> Moins de pollen
                    </button>
                </div>
                <div className="flex justify-center items-center mb-4 ">
                    <button
                        onClick={() => {
                            toggleCriteria('bruit');
                            window.trackButtonClick(`CalculateItinerary_MoinsDeBruit`);
                        }}
                        className={`px-3 py-3 inline-flex items-center mx-1 text-sm rounded-full transition duration-300 ${criteria.includes('bruit') ? 'bg-black text-white' : 'bg-white text-black shadow-md'}`}
                    >
                        <HiSpeakerXMark className="mr-2 text-lg" /> Moins de bruit
                    </button>
                    <button
                        onClick={() => {
                            toggleCriteria('tourisme');
                            window.trackButtonClick(`CalculateItinerary_LieuxTouristiques`);
                        }}
                        className={`px-3 py-3 inline-flex items-center mx-1 text-sm rounded-full transition duration-300 ${criteria.includes('tourisme') ? 'bg-black text-white' : 'bg-white text-black shadow-md'}`}
                    >
                        <MdPhotoCamera className="mr-2 text-lg" /> Lieux touristiques
                    </button>
                </div>

                <div className="flex justify-center items-center">
                    <button
                        onClick={calculateItinerary}
                        className={`text-white p-4 rounded-full shadow-md mt-2 ${!selectedStartAddress || !selectedEndAddress ? 'bg-gray-500 ' : 'bg-primary'}`}
                        disabled={!selectedStartAddress || !selectedEndAddress}
                    >
                        {isLoading ? (
                            <div className="flex items-center gap-2">
                                <span>En cours de chargement</span>
                                <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-primary animate-spin mr-3"></div>
                            </div>
                        ) : (
                            <div
                                className="flex items-center gap-2"
                                onClick={() => {
                                    window.trackButtonClick('ValidateCalculateItinerary');
                                    window.trackItineraryOptions(
                                        JSON.stringify({
                                            startAddress: selectedStartAddress,
                                            endAddress: selectedEndAddress,
                                            criteria: criteria,
                                        })
                                    );
                                }}
                            >
                                <span className="font-bold">Valider ma recherche</span>
                                {/* <FaCheck /> */}
                            </div>
                        )}
                    </button>
                </div>
            </div>
        </div>
            </>
        
    );
};

export default CalculateItinerary;
