import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";

import * as ROUTES from "./global/routes";
import * as CONTEXTS from "./global/contexts";

import "./App.css";

function App() {
  const [token, setToken] = useState("");
  return (
    <div id="app">
      <CONTEXTS.TokenContext.Provider value={{token, setToken}}>
        <Header />
        <BrowserRouter>
          <div>
              <Routes>
                <Route path={ROUTES.HOME} element={<Home />} />
              </Routes>
          </div>
        </BrowserRouter>
        <Footer />
      </CONTEXTS.TokenContext.Provider>
    </div>
  );
}

export default App;
