import { Col, Row } from "react-bootstrap";
import SpotifyLogin from "../components/SpotifyLogin";
import "../styles/home.css";
import UsernameSearch from "../components/UsernameSearch";

function Home() {
  return (
    <div className="page">
      <Row>
        <Col sm={{span: 4, offset: 1}}>
          <SpotifyLogin />
        </Col>
        <Col sm={{span: 5, offset: 1}}>
          <UsernameSearch />
        </Col>
      </Row>
    </div>
  );
}

export default Home;
