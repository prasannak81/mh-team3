import React from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Surround from './components/Surround';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ParkingSpot from './components/ParkingSpot';

const App: React.FC = () => {
  return (
    <Surround>
      <Container className="p-3">
        <Jumbotron>
          <h1 className="header">
            ResturantX Contactless Pickup Dashboard
          </h1>
        </Jumbotron>
        <Row xs={1} md={2}>
          <Col><ParkingSpot spotNumber={1} /></Col>
          <Col><ParkingSpot spotNumber={2} /></Col>
          <Col><ParkingSpot spotNumber={3} /></Col>
          <Col><ParkingSpot spotNumber={4} /></Col>
        </Row>
      </Container>
    </Surround>
  );
};

export default App;
