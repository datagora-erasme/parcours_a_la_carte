import React, { useContext, useState, useMemo, useEffect } from 'react';
import MainContext from '../contexts/mainContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPersonHiking, faRoute, faSpinner } from '@fortawesome/free-solid-svg-icons';


function ListLayers() {
    const { listLayers, setSelectedLayers, loadingLayers, loadingExtraLayers } = useContext(MainContext);
    
    // const handleCheckbox = id => {
    //     const updatedCheckboxes = checkboxes.map(layer => (layer.id === id ? { ...layer, checked: !layer.checked } : layer));
        
    //     setCheckboxes(updatedCheckboxes);
    //     setSelectedLayers(updatedCheckboxes.filter(layer => layer.checked).map(layer => layer.id));
    // };

    const extraLayers = useMemo(() => ([
        {
            id: 'boucle_rando',
            name: 'Boucles de randonnée',
            type: 'wfs',
            wfs: {
                url: 'https://data.grandlyon.com/geoserver/metropole-de-lyon/ows',
                typeName: 'metropole-de-lyon:boucle-de-randonnee',
                srsName: 'EPSG:4326',
            },
            marker_option: { iconUrl: undefined},
            faIcon: faPersonHiking,
        },
        {
            id: 'tour_of_lyon',
            name: 'Parcours ville de Lyon',
            type: 'geojson',
            marker_option: { iconUrl: undefined },
            faIcon: faRoute,
        }
    ]), [])

    const allLayers = useMemo(() => [...listLayers, ...extraLayers], [listLayers, extraLayers])
    const [checkboxes, setCheckboxes] = useState(allLayers.map(layer => ({ ...layer, checked: false })))

    useEffect(() => {
        setCheckboxes(prev => {
            const chechedId = new Set(prev.filter(layer => layer.checked).map(layer => String(layer.id)))
            return allLayers.map(layer => ({ ...layer, checked: chechedId.has(String(layer.id)) }))
        })
    }, [allLayers])

    const handleCheckbox = (id) => {
        setCheckboxes(prev =>
            prev.map(layer => layer.id === id ? { ...layer, checked: !layer.checked } : layer)
            )
    }

    useEffect(() => {
        const selected = checkboxes.filter(layer => layer.checked).map(layer => layer.id)
        setSelectedLayers(selected);
    }, [checkboxes, setSelectedLayers]);

    const renderIcon = (layer) => {
        const cls = (layer.checked
        ? 'w-16 h-16 bg-gray-300 border-2 rounded-full'
        : 'w-16 h-16 border-2 rounded-full hover:bg-gray-100'
        ) + ' flex items-center justify-center'

        return (
            <span className={cls} aria-hidden>
                {layer?.marker_option?.iconUrl ? (
                <img src={layer.marker_option.iconUrl} alt="" className="rounded-full p-2" />
                ) : layer?.faIcon ? (
                <FontAwesomeIcon icon={layer.faIcon }  color="white" className="bg-black p-2 w-7 h-7 rounded-full"  />
                ) : (
                <span></span>
                )}
            </span>
        )
    }

    return (
        <div className="w-full">
            {allLayers.length !== 0 ? (
                <ul className="mt-2 grid grid-cols-3">
                    {checkboxes.map(layer => {
                        const isLoading = loadingLayers[layer.id] || loadingExtraLayers[layer.id]
                        return (
                            <li key={layer.id} onClick={() => window.trackButtonClick?.(`ShowLayer_${layer.id}`)}>
                                <input
                                    type="checkbox"
                                    id={layer.id}
                                    checked={layer.checked}
                                    onChange={() => handleCheckbox(layer.id)}
                                    className="hidden"
                                />
                                <label htmlFor={layer.id} className="flex flex-col items-center text-[12px] mb-2 cursor-pointer">
                                    {isLoading ? (
                                        <FontAwesomeIcon
                                            icon={faSpinner}
                                            spin
                                            className="p-2 w-10 h-10 rounded-full p-2"
                                        />
                                    
                                    ) : (
                                        <>
                                        {renderIcon(layer)}
                                        </>
                                    )}
                                    
                                    {layer.name}
                                </label>
                            </li>
                        );
                    })}
                </ul>
            ) : (
                'Loading...'
            )}
        </div>
    );
}

export default ListLayers;
