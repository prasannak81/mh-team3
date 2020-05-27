import React from 'react';
import Card from 'react-bootstrap/Card';

interface ParkingSpotProps {
  spotNumber: number
  spotName?: string
}

const ParkingSpot: React.FC<ParkingSpotProps> = ({ spotNumber, spotName }:ParkingSpotProps) => (
  <Card className="text-center">
    <Card.Header>Parking Spot {spotNumber || "?"}</Card.Header>
    <Card.Body>
      <Card.Title>{spotName || "DEFAULT VALUE"}</Card.Title>
      <Card.Text>
        With supporting text below as a natural lead-in to additional content.
      </Card.Text>
    </Card.Body>
    <Card.Footer className="text-muted"><b>Updated:</b> 2 minutes ago</Card.Footer>
  </Card>
);

export default ParkingSpot;
