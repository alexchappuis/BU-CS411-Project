import { useContext, useRef, useState } from 'react';
import { Row } from 'react-bootstrap'

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

const UsernameSearch = () => {
  const tokenCon = useContext(CONTEXTS.TokenContext);
  const [id, setId] = useState("");

  const search = () => {
    console.log("Searching");
    fetch(ROUTES.SERVER_GET_STEAM_USER, {
      method: "POST",
      body: JSON.stringify({
        id: id,
      }),
    })
    .then(resp => resp.json())
    .then(data => console.log(data));
  }

  return (
    <div id="steamSearch">
      <Row id="searchLabel">
        <p>Steam User ID Search</p>
      </Row>
      <Row id="idSearch">
      <input
        type="text"
        id="idSearchEntry"
        onChange={(e) => {
          setId(e.target.value);
        }}
      />
      </Row>
      <Row>
        <button className="searchBtn" onClick={search} disabled={id === ""}>Search</button>
      </Row>
    </div>
  )
}

export default UsernameSearch