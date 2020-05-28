import React, { Component, ChangeEvent } from 'react'
import SpotOrderUpdate from './SpotOrderUpdate'
import { Order } from '../common/data_types'
import get_api from '../common/get_api_typed'

const initialState: SpotOrderUpdateWrapperState = { orders: [], activeOrderNumber: "" }
type SpotOrderUpdateWrapperState = {
  orders: Order[]
  activeOrderNumber: string
}
type State = Readonly<typeof initialState>

interface SpotOrderUpdateWrapperProps {
  spotNumber: number
  activeOrderNumber?: string
  spotUpdater: (orderNumber: string) => void
}

class SpotOrderUpdateWrapper extends Component<SpotOrderUpdateWrapperProps, State> {

  constructor(props: SpotOrderUpdateWrapperProps) {
    super(props)
    this.state = {orders: [], activeOrderNumber: (props.activeOrderNumber || "")}
    // console.log(props.activeOrderNumber)
  }

  render() {
    const { spotNumber } = this.props
    const { orders, activeOrderNumber } = this.state
    return(
      <SpotOrderUpdate
        spotNumber={spotNumber}
        activeOrderNumber={activeOrderNumber}
        onChangeHandler={this.spotOrderChangeHandler}
        orders={orders} />
    )
  }

  private spotOrderChangeHandler = (event: ChangeEvent<HTMLSelectElement>): void => {
    this.setState({activeOrderNumber: event.target.value})
    this.props.spotUpdater(event.target.value);
  }

  componentWillReceiveProps(nextProps: SpotOrderUpdateWrapperProps) {
    this.setState({activeOrderNumber: (nextProps.activeOrderNumber || "")})
  }

  componentDidMount() {
    get_api<Order[]>("http://localhost:5000/api/read/orders")
      .then(
        (newOrders) => {
          this.setState({ orders: newOrders })
        }
        )
      .catch(err => {console.log(err)});
    setTimeout(()=>{this.forceRecheck()}, 1000)
  }

  forceRecheck = () => {
    this.updateAppStatus()
  }

  private handleClick = () => {
    // this.props.determineState().then(newStatus => {
    //   this.setState({appStatus: newStatus})
    // })
  }

  private updateAppStatus() {
    
  }
}

export default SpotOrderUpdateWrapper