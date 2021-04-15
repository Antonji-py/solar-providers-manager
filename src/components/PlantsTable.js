import React, { useState, useEffect } from "react";

import "./PlantsTable.css";

function PlantsTable() {
  const [plants, setPlants] = useState(undefined);
  const [devices, setDevices] = useState(undefined);

  useEffect(() => {
    getPlants();
    getDevices();
  }, []);

  const getPlants = async () => {
    const response = await fetch("/get-plants");
    const data = await response.json();

    setPlants(data.plants);
  };

  const getDevices = async () => {
    const response = await fetch("/get-devices");
    const data = await response.json();

    setDevices(data.devices);
  };

  return (
    <>
      <div className="row">
        <div class="col-sm-6">
          <img
            src="https://growatt.pl/wp-content/uploads/2020/07/logo.png"
            class="rounded mx-auto d-block"
            height="150"
            width="414"
          />
        </div>
        <div class="col-sm-6">
          <img
            src="https://www.selfa-pv.com/ckfinder/userfiles/images/Inwertery/SolarEdge_logo(1).jpg"
            class="rounded mx-auto d-block"
            height="150"
            width="394"
          />
        </div>
        {plants &&
          Object.values(plants)?.map((provider, indexProvider) => {
            return (
              <div className="table-responsive col-md-6">
                <table className="table table-hover">
                  <thead className="table-dark">
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Plant Name</th>
                      <th scope="col">Plant ID</th>
                      <th scope="col">Inverter ID</th>
                    </tr>
                  </thead>
                  <tbody>
                    {provider.map((plant, indexPlants) => (
                      <>
                        <tr>
                          <th scope="row">{indexPlants + 1}</th>
                          <td>{plant.plant_name}</td>
                          <td>{plant.id}</td>
                          <td>
                            {devices &&
                              devices[Object.keys(devices)[indexProvider]][
                                indexPlants
                              ]?.map((device) => <p>{device.serial_number}</p>)}
                          </td>
                        </tr>
                      </>
                    ))}
                  </tbody>
                </table>
              </div>
            );
          })}
      </div>
    </>
  );
}

export default PlantsTable;
