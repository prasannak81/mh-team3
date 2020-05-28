export const lazyPlural = (count:number, noun:string, suffix:string = 's'):string =>
  `${noun}${count !== 1 ? suffix : ''}`;

export const APIBASE = process.env.NODE_ENV == "production" ? "/api" : "http://localhost:5000/api";
