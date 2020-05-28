
const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}
export default function post_api<T>(url: string, payload: any): Promise<T> {
  return fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(payload)}).then(resp => {
    if (!resp.ok) {
      throw new Error(resp.statusText)
    }
    return resp.json() as Promise<T>
  })
}