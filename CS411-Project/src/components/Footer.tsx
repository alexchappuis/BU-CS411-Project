import { Container, Row, Col } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faGithub,
} from "@fortawesome/free-brands-svg-icons";

import * as ROUTES from "../global/routes";

import "../styles/footer.css";

function Footer() {
  return (
    <div id="footer">
      <Container>
        <Row className="justify-content-center">
            <Col sm={{span: 12, offset: 0}} className="footerCopyright">
                <small>Copyright &copy; 2024 Alex Chappuis, Noah Barnes, Richard Lin</small>
            </Col>
        </Row>
        <Row className="justify-content-center">
            <Col sm={{span: 12, offset: 0}}>
                <a target="_blank" href={ROUTES.GITHUB} className="footerIcon">
                    <FontAwesomeIcon icon={faGithub} />
                </a>
            </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Footer;
