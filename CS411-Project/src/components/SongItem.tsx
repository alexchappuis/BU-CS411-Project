import { Row, Col } from 'react-bootstrap';

import "../styles/home.css"

interface Props {
    name: string;
    id: string;
    duration: number;
    coverUrl: string;
    previewUrl: string;
}

const SongItem = ( {name, id, duration, coverUrl, previewUrl }: Props) => {
  let durationMinutes = Math.floor(duration / 1000 / 60);
  let durationSeconds = Math.floor(duration / 1000) % 60;
  return (
    <Row className="songDesc">
      <Col sm={{span: 2, offset: 0}} className="albumCover">
        <img src={coverUrl} alt={name + " Cover"} />
      </Col>
      <Col sm={{span: 5, offset: 0}} className="verticalCenterContainer">
        <div className="verticalCenter">
          <h1>{name}</h1>
          <small>{id}</small>
          <h4>{durationMinutes}m{durationSeconds}s</h4>
        </div>
      </Col>
      <Col sm={{span: 5, offset: 0}} className="verticalCenterContainer">
        <div className="verticalCenter">
          <audio controls>
            <source src={previewUrl} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      </Col>
    </Row>
  )
}

export default SongItem