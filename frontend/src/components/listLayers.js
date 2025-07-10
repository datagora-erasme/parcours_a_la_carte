import React, { useContext, useState } from 'react';
import MainContext from '../contexts/mainContext';

function ListLayers() {
    const { listLayers, setSelectedLayers, isLayerLoading } = useContext(MainContext);
    const [checkboxes, setCheckboxes] = useState(listLayers.map(layer => ({ ...layer, checked: false })));

    const handleCheckbox = id => {
        const updatedCheckboxes = checkboxes.map(layer => (layer.id === id ? { ...layer, checked: !layer.checked } : layer));

        setCheckboxes(updatedCheckboxes);
        setSelectedLayers(updatedCheckboxes.filter(layer => layer.checked).map(layer => layer.id));
    };

    return (
        <div className="w-full">
            {listLayers.length !== 0 ? (
                <ul className="mt-2 grid grid-cols-3">
                    {checkboxes.map(layer => {
                        return (
                            <li key={layer.id} onClick={() => window.trackButtonClick(`ShowLayer_${layer.id}`)}>
                                <input
                                    type="checkbox"
                                    id={layer.id}
                                    checked={layer.checked}
                                    onChange={() => handleCheckbox(layer.id)}
                                    className="hidden"
                                />
                                <label htmlFor={layer.id} className="flex flex-col justify-center items-center text-[12px] mb-2">
                                    <img
                                        src={layer.marker_option.iconUrl}
                                        alt="icon"
                                        className={
                                            layer.checked
                                                ? 'w-16 p-2 bg-gray-300 border-solid border-2 rounded-full cursor-pointer'
                                                : 'w-16 p-2 border-solid border-2 rounded-full hover:bg-gray-100 cursor-pointer'
                                        }
                                    />
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
