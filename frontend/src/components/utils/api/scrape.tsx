import { type ScrapedData } from "../../scrape_page/Scrape_Page"

type ScrapeProps = {
    team: string;
    image_count: string;
    update_scrape_status: (scrapeResult: ScrapedData | unknown, scrapeStatus: boolean) => void;
    update_click_status: (clickStatus: boolean) => void
}

export default async function scrape_images({team, image_count, update_scrape_status, update_click_status}:ScrapeProps) {
    update_click_status(true)
    const response: Response = (
        await fetch(`http://54.159.206.126:8000/scrape/images?team_name=${team}&image_per_player=${image_count}`))
    const data = await response.json()
    update_scrape_status(data, true)
    return data
}
