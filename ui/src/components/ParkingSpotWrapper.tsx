import React, { Component } from 'react'
import ParkingSpot from './ParkingSpot'
import { Order, ParkingSpotInfo, ParkingSpotStatus } from '../common/data_types'
import get_api from '../common/get_api_typed'

const initialState: ParkingSpotWrapperState = { orders: [], info: { status: ParkingSpotStatus.Open, orderNumber: "", lastUpdated: ""} }
type ParkingSpotWrapperState = {
  orders: Order[]
  info: ParkingSpotInfo
}
type State = Readonly<typeof initialState>

interface ParkingSpotWrapperProps {
  spotNumber: number
}

type determineStateFunction = () => Promise<string>;
type btnClickHandlerFunction = () => void;


class ParkingSpotWrapper extends Component<ParkingSpotWrapperProps, State> {
  readonly state: State = initialState
  render() {
    const { spotNumber } = this.props
    const { info } = this.state
    return(
      <ParkingSpot
        spotNumber={spotNumber} spotStatus={info.status} lastUpdated={info.lastUpdated} activeOrderNumber={info.orderNumber} />
    )
  }

  componentDidMount() {
    this.updateSpotStatus()
    setTimeout(()=>{this.updateSpotStatus()}, 1000)
  }

  private handleClick = () => {
    // this.props.determineState().then(newStatus => {
    //   this.setState({appStatus: newStatus})
    // })
  }

  private updateSpotStatus() {
    get_api<ParkingSpotInfo>("http://localhost:5000/api/read/spots/"+this.props.spotNumber)
      .then(
        (spotInfo) => {
          this.setState({ info: spotInfo })
        }
        )
      .catch(err => {console.log(err)});
  }
}

export default ParkingSpotWrapper