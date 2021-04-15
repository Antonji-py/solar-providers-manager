import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import HomePage from "./components/pages/HomePage";
import GetLogsFilePage from "./components/pages/GetLogsFilePage";
import GetFaultLogsFilePage from "./components/pages/GetFaultLogsFilePage";
import GetMonthlyReportPage from "./components/pages/GetMonthlyReportPage";

import "rsuite/dist/styles/rsuite-default.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/" exact component={HomePage} />
        <Route path="/get-logs-file" exact component={GetLogsFilePage} />
        <Route
          path="/get-fault-logs-file"
          exact
          component={GetFaultLogsFilePage}
        />
        <Route
          path="/get-monthly-report-file"
          exact
          component={GetMonthlyReportPage}
        />
      </Switch>
    </Router>
  );
}

export default App;
