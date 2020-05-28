export default function get_api<T>(url: string): Promise<T> {
  return fetch(url).then(resp => {
    if (!resp.ok) {
      throw new Error(resp.statusText)
    }
    return resp.json() as Promise<T>
  })
}