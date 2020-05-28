import React from 'react';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import {Col} from 'react-bootstrap';
import SpotOrderUpdateWrapper from './SpotOrderUpdateWrapper';
import { ParkingSpotStatus } from '../common/data_types';
import moment from 'moment'

interface ParkingSpotProps {
  spotNumber: number,
  spotStatus: string,
  lastUpdated: number,
  activeOrderNumber: string,
  spotUpdater: (orderNumber: string) => void
}

type ParkingSpotStatusColor = "info" | "warning" | "success" | "danger" | undefined;

const ParkingSpot: React.FC<ParkingSpotProps> = ({ spotNumber, spotStatus, lastUpdated, activeOrderNumber, spotUpdater }:ParkingSpotProps) => {
  let borderColor:ParkingSpotStatusColor = undefined;
  const waitingFor:number = Math.round((moment().unix() - lastUpdated) / 60);

  switch(spotStatus) {
    case ParkingSpotStatus.Arrived:
      borderColor = "info"
      break;
    case ParkingSpotStatus.Waiting:
      borderColor = (waitingFor >= 5 ? "danger" : "warning");
      break;
    case ParkingSpotStatus.Departed:
      borderColor = "success"
      break;
  }

  const lastUpdateDesc:string = lastUpdated ? moment(lastUpdated*1000).fromNow() : "...";

  return <Card className="text-center" style={{ marginTop: '15px', marginBottom: '15px' }} border={borderColor}>
    <Card.Header>Parking Spot <b>{spotNumber || "?"}</b><br /><b>{spotStatus} {(spotStatus === ParkingSpotStatus.Waiting) && <>({waitingFor} minutes)</>} </b></Card.Header>
    <Card.Body>
      <Container>
        <Row>
          <Col>
            <SpotOrderUpdateWrapper spotNumber={spotNumber} activeOrderNumber={activeOrderNumber} spotUpdater={spotUpdater}/>
          </Col>
        </Row>
      </Container>
    </Card.Body>
    <Card.Footer className="text-muted"><b>Updated:</b> {lastUpdateDesc || "Some Time Ago"}</Card.Footer>
  </Card>
};

export default ParkingSpot;
