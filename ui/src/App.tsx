import React from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';
import Surround from './components/Surround';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ParkingSpotWrapper from './components/ParkingSpotWrapper';

const App: React.FC = () => {
  return (
    <Surround>
      <Container className="p-3" fluid={true}>
        <Jumbotron>
          <h1 className="header">
            ResturantX Contactless Pickup Dashboard
          </h1>
        </Jumbotron>
        <Row xs={1} md={2} lg={4}>
          <Col><ParkingSpotWrapper spotNumber={1} /></Col>
          <Col><ParkingSpotWrapper spotNumber={2} /></Col>
          <Col><ParkingSpotWrapper spotNumber={3} /></Col>
          <Col><ParkingSpotWrapper spotNumber={4} /></Col>
          <Col><ParkingSpotWrapper spotNumber={5} /></Col>
          <Col><ParkingSpotWrapper spotNumber={6} /></Col>
          <Col><ParkingSpotWrapper spotNumber={7} /></Col>
          <Col><ParkingSpotWrapper spotNumber={8} /></Col>
        </Row>
      </Container>
    </Surround>
  );
};

export default App;
