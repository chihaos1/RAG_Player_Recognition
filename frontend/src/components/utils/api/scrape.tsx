import { get } from '../http.ts'



export default function scrape_images() {
    const data = (fetch('http://127.0.0.1:8082/scrape/images')) as unknown;
}