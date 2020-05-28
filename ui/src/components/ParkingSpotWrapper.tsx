import React, { Component } from 'react'
import ParkingSpot from './ParkingSpot'
import { Order, ParkingSpotInfo, ParkingSpotStatus } from '../common/data_types'
import get_api from '../common/get_api_typed'
import post_api from '../common/post_api_typed'

const initialState: ParkingSpotWrapperState = { orders: [], info: { status: ParkingSpotStatus.Open, orderNumber: "", lastUpdated: ""} }
type ParkingSpotWrapperState = {
  orders: Order[]
  info: ParkingSpotInfo
}
type State = Readonly<typeof initialState>

interface ParkingSpotWrapperProps {
  spotNumber: number
}

class ParkingSpotWrapper extends Component<ParkingSpotWrapperProps, State> {
  readonly state: State = initialState
  render() {
    const { spotNumber } = this.props
    const { info } = this.state
    return(
      <ParkingSpot
        spotNumber={spotNumber} spotStatus={info.status} lastUpdated={info.lastUpdated} activeOrderNumber={info.orderNumber} spotUpdater={this.updateSpotStatus.bind(this)} />
    )
  }

  componentDidMount() {
    this.refreshSpotStatus()
  }

  private handleClick = () => {
    // this.props.determineState().then(newStatus => {
    //   this.setState({appStatus: newStatus})
    // })
  }

  private refreshSpotStatus() {
    this.getSpotStatus()
    setTimeout(()=>{this.refreshSpotStatus()}, 5000)
  }

  private getSpotStatus() {
    get_api<ParkingSpotInfo>("http://localhost:5000/api/read/spots/"+this.props.spotNumber)
      .then(
        (spotInfo) => {
          this.setState({ info: spotInfo })
          if(spotInfo.status === ParkingSpotStatus.Departed) {
            this.resetSpotStatus()
          }
        }
        )
      .catch(err => {console.log(err)});
  }

  private updateSpotStatus(orderNumber: string):void {
    post_api<ParkingSpotInfo>("http://localhost:5000/api/update/spots/"+this.props.spotNumber, {status: ParkingSpotStatus.Waiting, orderNumber: orderNumber, lastUpdated: "TODO"}) //TODO: Set as current ISO
      .then(
        (resp) => {
          console.log(resp);
        })
      .catch(err => {console.log(err)});
  }

  private resetSpotStatus() {
    post_api<ParkingSpotInfo>("http://localhost:5000/api/update/spots/"+this.props.spotNumber, {status: ParkingSpotStatus.Open, orderNumber: "", lastUpdated: "TODO"}) //TODO: Set as current ISO
      .then(
        (resp) => {
          console.log(resp);
        })
      .catch(err => {console.log(err)});
  }
}

export default ParkingSpotWrapper