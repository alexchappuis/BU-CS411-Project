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
  const [login, setLogin] = useState<CONTEXTS.SpotifyLogin>(
    {token: "", refreshToken: "", expiration: 0}
  );
  return (
    <div id="app">
      <CONTEXTS.SpotifyContext.Provider value={{login, setLogin}}>
        <Header />
        <BrowserRouter>
          <div>
              <Routes>
                <Route path={ROUTES.HOME} element={<Home />} />
              </Routes>
          </div>
        </BrowserRouter>
        <Footer />
      </CONTEXTS.SpotifyContext.Provider>
    </div>
  );
}

export default App;
