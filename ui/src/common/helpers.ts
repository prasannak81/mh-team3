export const lazyPlural = (count:number, noun:string, suffix:string = 's'):string =>
  `${noun}${count !== 1 ? suffix : ''}`;