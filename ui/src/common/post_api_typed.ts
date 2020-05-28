
const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}
type postApiMethodType = 'POST' | 'PUT'
export default function post_api<T>(url: string, payload: any, methodType: postApiMethodType = 'POST'): Promise<T> {
  return fetch(url, {method: methodType, headers: headers, body: JSON.stringify(payload)}).then(resp => {
    if (!resp.ok) {
      throw new Error(resp.statusText)
    }
    return resp.json() as Promise<T>
  })
}