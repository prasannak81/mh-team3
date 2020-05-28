export type Order = {
  orderNumber: string
  orderName: string
}

export enum ParkingSpotStatus {
  Open = "OPEN",
  Arrived = "ARRIVED",
  Waiting = "WAITING",
  Departed = "DEPARTED"
}

export type ParkingSpotInfo = {
  status: ParkingSpotStatus
  orderNumber: string
  lastUpdated: string
}