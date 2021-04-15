import React, { useState, useEffect } from "react";
import { Multiselect } from "multiselect-react-dropdown";
import { Button, ToggleButtonGroup, ToggleButton } from "react-bootstrap";

function GetMonthlyReportPage() {
  const [providerPlants, setProviderPlants] = useState(undefined);
  const [selectedPlants, setSelectedPlants] = useState([]);
  const [date, setDate] = useState(undefined);

  const [selectAllButtonDisabled, setSelectAllButtonDisabled] = useState(true);

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

  const handleSubmitButton = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        plants: selectedPlants,
        date: date,
      }),
    };
    console.log(requestOptions);

    fetch("/get-monthly-report-file", requestOptions)
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
          </div>
        </div>
        <div className="form-row">
          <div className="form-group row" style={{ margin: "0 auto" }}>
            <div className="form-group row" style={{ margin: "0 auto" }}>
              <label className="col-sm-2 col-form-label">Month:&nbsp;</label>
              <div className="col-sm-10">
                <input
                  type="month"
                  className="form-control"
                  onChange={(e) => {
                    setDate(e.target.value);
                  }}
                ></input>
              </div>
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

export default GetMonthlyReportPage;
