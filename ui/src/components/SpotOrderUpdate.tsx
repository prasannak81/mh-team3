import React, { ChangeEvent } from 'react';
import { Form } from 'react-bootstrap';
import { Order } from '../common/data_types';

interface SpotOrderUpdateProps {
  spotNumber: number,
  orders: Order[],
  activeOrderNumber?: string,
  onChangeHandler: (event: ChangeEvent<HTMLSelectElement>) => void
}

const SpotOrderUpdate: React.FC<SpotOrderUpdateProps> = ({ orders, spotNumber, activeOrderNumber = "", onChangeHandler }:SpotOrderUpdateProps) => (
  <Form>
    <Form.Group controlId={"updateOrderSpot-"+spotNumber}>
      <Form.Label>Select Order</Form.Label>
      <Form.Control as="select" value={activeOrderNumber} onChange={onChangeHandler}>
        <option>-</option>
        {orders.map((order, idx) => {
          return <option key={idx} value={order.orderNumber}>(#{order.orderNumber}) {order.orderName}</option>
        })}
        <option>INVALID</option>
      </Form.Control>
    </Form.Group>
  </Form>
);

export default SpotOrderUpdate;
