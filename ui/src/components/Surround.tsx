import React, { ReactNode } from 'react';
import Navbar from 'react-bootstrap/Navbar';

interface SurroundProps {
  children: ReactNode[] | ReactNode;
}

const Surround: React.FC<SurroundProps> = ({ children }:SurroundProps) => (
  <>
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand>RestaurantX</Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse className="justify-content-end">
        <Navbar.Text>
          Signed in as: <a href="#login">Neil Armstrong</a>
        </Navbar.Text>
      </Navbar.Collapse>
    </Navbar>
    {children}
  </>
);

export default Surround;
