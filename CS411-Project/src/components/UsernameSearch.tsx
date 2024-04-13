import { useContext, useRef } from 'react';
import { Row } from 'react-bootstrap'

import * as CONTEXTS from "../global/contexts";

const UsernameSearch = () => {
  const tokenCon = useContext(CONTEXTS.TokenContext);
  const id = useRef("")

  const search = () => {

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
          id.current = e.target.value;
        }}
      />
      </Row>
      <Row>
        <a className="searchBtn" onClick={search} href="">Search</a>
      </Row>
    </div>
  )
}

export default UsernameSearch