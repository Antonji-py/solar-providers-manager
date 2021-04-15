import React from "react";
import { Link } from "react-router-dom";
import { Button } from "rsuite";

import "./Navbar.css";

function Navbar() {
  const handleRefreshPlantsButton = () => {
    fetch("/refresh-plants")
      .then((response) => response.json())
      .then((data) => alert(data.result));
  };

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <img
            src="http://fastenergy.pl/wp-content/uploads/2020/01/Fast-Energy-logo-16.png"
            width="117"
            height="45"
          ></img>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link to="/" className="nav-link active">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/get-logs-file" className="nav-link">
                  Get Logs File
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/get-fault-logs-file" className="nav-link">
                  Get Fault Logs File
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/get-monthly-report-file" className="nav-link">
                  Get Monthly Report File
                </Link>
              </li>
            </ul>
          </div>
          <div className="refresh-btn">
            <Button size="lg" onClick={handleRefreshPlantsButton}>
              Refresh Plants
            </Button>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
