import { Row, Col } from 'react-bootstrap';

interface Props {
    name: string;
    id: number;
    hoursPlayed: number;
    usersPlayed?: number;
    rank: number;
    coverUrl: string;
}

const GameRecord = ( {name, id, hoursPlayed, usersPlayed, rank, coverUrl }: Props) => {
  let rankDisplay;
  switch(rank) {
    case 1:
      rankDisplay = <h1 className="first">{rank}</h1>;
      break;
    case 2:
      rankDisplay = <h1 className="second">{rank}</h1>;
      break;
    case 3:
      rankDisplay = <h1 className="third">{rank}</h1>;
      break;
    default:
      rankDisplay = <h1 className="fourthFifth">{rank}</h1>;
      break;
  }
  return (
    <Row>
      <Col sm={{span: 1, offset: 0}} className="doubleCenterContainer">
        {rankDisplay}
      </Col>
      <Col sm={{span: 4, offset: 0}} className="gameCover">
        <img src={coverUrl} alt={name + " Cover"} />
      </Col>
      <Col sm={{span: 7, offset: 0}} className="verticalCenterContainer">
        <div className="verticalCenter">
          <h1>{name}</h1>
          <h6>ID: {id}</h6>
          <h3>{hoursPlayed} hours played</h3>
          {usersPlayed && usersPlayed > 1 && <h3>{usersPlayed} unique users have played this game</h3>}
          {usersPlayed && usersPlayed === 1 && <h3>{usersPlayed} unique user has played this game</h3>}
        </div>
      </Col>
    </Row>
  )
}

export default GameRecord