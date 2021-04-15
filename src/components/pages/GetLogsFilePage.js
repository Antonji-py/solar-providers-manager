import React, { useState, useEffect } from "react";
import { Button, ToggleButtonGroup, ToggleButton } from "react-bootstrap";
import { Multiselect } from "multiselect-react-dropdown";

import "./GetLogsFilePage.css";

function GetLogsFilePage() {
  const [providerPlants, setProviderPlants] = useState(undefined);
  const [selectedPlants, setSelectedPlants] = useState([]);
  const [availableDevices, setAvailableDevice] = useState([]);
  const [selectedDevices, setSelectedDevices] = useState(undefined);
  const [startDate, setStartDate] = useState(undefined);
  const [endDate, setEndDate] = useState(undefined);

  const [selectAllButtonDisabled, setSelectAllButtonDisabled] = useState(true);

  useEffect(() => {
    updateAvailableDevices();
  }, [selectedPlants]);

  const getPlants = async (provider) => {
    const response = await fetch("/get-plants");
    const data = await response.json();

    setProviderPlants(data.plants[provider]);
  };

  const handleProviderChange = (e) => {
    if (e.target.value != undefined) {
      getPlants(e.target.value);
      setSelectAllButtonDisabled(false);
    }
  };

  const PlantsSelect = () => {
    const style = {
      multiselectContainer: {
        width: "100%",
        display: "inline-block",
      },
    };

    return (
      <>
        <Multiselect
          onSelect={onSelectPlantChange}
          onRemove={onRemovePlantChange}
          selectedValues={selectedPlants}
          options={providerPlants}
          displayValue="plant_name"
          placeholder="Select plant"
          closeOnSelect={false}
          style={style}
        />
      </>
    );
  };

  const onSelectPlantChange = (selectedList, selectedItem) => {
    setSelectedPlants(selectedList);
  };

  const onRemovePlantChange = (selectedList, removedItem) => {
    setSelectedPlants(selectedList);
  };

  const updateAvailableDevices = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        plants: selectedPlants,
      }),
    };

    fetch("/get-devices-by-ids", requestOptions)
      .then((response) => response.json())
      .then((data) => setAvailableDevice(data.devices));
  };

  const DeviceSelect = () => {
    const style = {
      multiselectContainer: {
        width: "100%",
        display: "inline-block",
      },
    };

    return (
      <>
        <Multiselect
          onSelect={onSelectDeviceChange}
          onRemove={onRemoveDeviceChange}
          selectedValues={selectedDevices}
          options={availableDevices}
          displayValue="serial_number"
          placeholder="Select device"
          closeOnSelect={false}
          style={style}
        />
      </>
    );
  };

  const onSelectDeviceChange = (selectedList, selectedItem) => {
    setSelectedDevices(selectedList);
  };

  const onRemoveDeviceChange = (selectedList, removedItem) => {
    setSelectedDevices(selectedList);
  };

  const handleSubmitButton = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        devices: selectedDevices,
        startDate: startDate,
        endDate: endDate,
      }),
    };

    fetch("/get-logs-file", requestOptions)
      .then((response) => response.json())
      .then((data) => alert(data.result));
  };

  return (
    <>
      <div className="form-container">
        <div className="form-row">
          <div className="radio-group">
            <ToggleButtonGroup
              onClick={handleProviderChange}
              type="radio"
              name="providerCheckbox"
            >
              <ToggleButton value="growatt">Growatt</ToggleButton>
              <ToggleButton value="solaredge">SolarEdge</ToggleButton>
            </ToggleButtonGroup>
          </div>
        </div>
        <div className="form-row">
          <div className="multiselect-container" style={{ margin: "0 auto" }}>
            <div className="multiselect-form">
              <PlantsSelect />
              <Button
                variant="secondary"
                onClick={() => {
                  setSelectedPlants(providerPlants);
                }}
                disabled={selectAllButtonDisabled}
                style={{ width: "100%" }}
              >
                Select All
              </Button>
            </div>
            <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
            <div className="multiselect-form">
              <DeviceSelect />
              <Button
                variant="secondary"
                onClick={() => {
                  setSelectedDevices(availableDevices);
                }}
                disabled={selectAllButtonDisabled}
                style={{ width: "100%" }}
              >
                Select All
              </Button>
            </div>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group row" style={{ margin: "0 auto" }}>
            <label class="col-sm-2 col-form-label">Start Date:</label>
            <div class="col-sm-10">
              <input
                type="date"
                className="form-control"
                onChange={(e) => {
                  setStartDate(e.target.value);
                }}
              ></input>
            </div>
            <label class="col-sm-2 col-form-label">End Date:</label>
            <div class="col-sm-10">
              <input
                type="date"
                className="form-control"
                onChange={(e) => {
                  setEndDate(e.target.value);
                }}
              ></input>
            </div>
          </div>
        </div>
        <div className="form-row">
          <Button onClick={handleSubmitButton} style={{ margin: "0 auto" }}>
            Submit
          </Button>
        </div>
      </div>
    </>
  );
}

export default GetLogsFilePage;
