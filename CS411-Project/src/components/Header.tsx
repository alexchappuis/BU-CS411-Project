import { useState, useEffect, useContext } from "react";
import { Container, Navbar, Nav } from "react-bootstrap";

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import "../styles/header.css";

function Header() {
  const tokenCon = useContext(CONTEXTS.TokenContext);

  useEffect(() => {
    const hash = window.location.hash;
    let localToken = window.localStorage.getItem("token");
    if(localToken) tokenCon.setToken(localToken);
    else if(hash) {
        let atString = hash.substring(1).split("&").find(elem => elem.startsWith("access_token"));
        if(atString) {
            let tokenString = atString.split("=")[1];
            window.location.hash = "";
            window.localStorage.setItem("token", tokenString)
            tokenCon.setToken(tokenString);
        } else {
            console.error("Could not get Spotify OAuth access token.");
        }
    }
  }, [])

  const logout = () => {
    tokenCon.setToken("");
    window.localStorage.removeItem("token");
  }

  return (
    <div id="header">
      <Navbar expand="sm" id="headerBar">
        <Container>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse className="justify-content-end" id="basic-navbar-nav">
            <Nav>
              <Nav.Link href={ROUTES.HOME}>Home</Nav.Link>
              {tokenCon.token && <Nav.Link onClick={logout}>Logout</Nav.Link>}
              {!tokenCon.token && <Nav.Link href={ROUTES.LOGIN}>Spotify Login</Nav.Link>}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}

export default Header;

/*
Spotify OAuth React Tutorial
https://www.youtube.com/watch?v=wBq3HCvYfUg
*/