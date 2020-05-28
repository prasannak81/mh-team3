import React from 'react';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import {Col} from 'react-bootstrap';
import SpotOrderUpdateWrapper from './SpotOrderUpdateWrapper';

interface ParkingSpotProps {
  spotNumber: number,
  spotStatus: string,
  lastUpdated: string,
  activeOrderNumber: string
}

const ParkingSpot: React.FC<ParkingSpotProps> = ({ spotNumber, spotStatus, lastUpdated, activeOrderNumber }:ParkingSpotProps) => (
  <Card className="text-center" style={{ marginTop: '15px', marginBottom: '15px' }}>
    <Card.Header>Parking Spot <b>{spotNumber || "?"}</b></Card.Header>
    <Card.Body>
      <Container>
        <Row>
          <Col>
            Status: <b>{spotStatus}</b>
          </Col>
          <Col>
          <SpotOrderUpdateWrapper spotNumber={spotNumber} activeOrderNumber={activeOrderNumber}/>
          </Col>
        </Row>
      </Container>
    </Card.Body>
    <Card.Footer className="text-muted"><b>Updated:</b> {lastUpdated}</Card.Footer>
  </Card>
);

export default ParkingSpot;
