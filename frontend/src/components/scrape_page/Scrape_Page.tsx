import "./Scrape_Page.css";
import Button from "../UI/Button/Button.tsx";
import Card from "../UI/Card/Card.tsx"
import { Spinner } from "../UI/Spinner/Spinner.tsx";
import scrape_images from "../utils/api/scrape.tsx"
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import  pl_logo from "../../assets/team_logos/PremierLeague.png"
import  newcastle_logo from "../../assets/team_logos/Newcastle.png"
import  west_ham_logo from "../../assets/team_logos/WestHam.png"
import  brighton_logo from "../../assets/team_logos/Brighton.png"

type TeamLogoMap = {
    default: string,
    Newcastle_United: string,
    West_Ham_United: string,
    "Brighton_%2526_Hove_Albion": string
}
type ValidTeamOptions = "default" | "Newcastle_United" | "West_Ham_United" | "Brighton_%2526_Hove_Albion"

export type ScrapedData = {
    [key: string]: number;
    
}

export default function Scrape_Page() {
    const [selectedTeam, setTeamSelection] = useState<ValidTeamOptions>("default")
    const [imageCount, setImageCount] = useState<number>(5)
    const [scrapedData, setScrapedData] = useState<ScrapedData | unknown>({});
    const [isScraped, setScrapeStatus] = useState<boolean>(false)
    const [isClicked, setClickStatus] = useState<boolean>(false)
    const navigate = useNavigate();

    const handleTeamSelection = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTeamSelection(e.target.value as ValidTeamOptions)
    }

    const handleImageSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
        const imageCount = e.target.value as string
        const parsedImageCount = parseInt(imageCount)
        setImageCount(parsedImageCount)
    }

    const handleScraping = (scrapeResult: unknown, scrapeStatus: boolean) => {
        setScrapedData(scrapeResult)
        setScrapeStatus(scrapeStatus)
    }

    const handleClick = (clickStatus: boolean) => {
        setClickStatus(clickStatus)
    }

    const logoMap: TeamLogoMap = {
        default: pl_logo,
        Newcastle_United: newcastle_logo,
        West_Ham_United: west_ham_logo,
        "Brighton_%2526_Hove_Albion": brighton_logo,
    }

    useEffect(() => {
        if (isScraped) {
            navigate("/embed", { state: { scrapedData: scrapedData } })
        }
    }, [isScraped])

    return (
        <Card background="first">
            <div id="scrape_page_title">
                <h2>Player Image Scraping</h2>
            </div>
            <div id="selection-container">
                <div id="scrape-container"> 
                    <div className="selection">
                        <label htmlFor="team-selection">Select a Team</label>
                        <select className="choices" name="team-selection" value={selectedTeam} onChange={handleTeamSelection}>
                            <option value="default" disabled>-</option>
                            <option value="Newcastle_United">Newcastle United</option>
                            <option value="West_Ham_United">West Ham United</option>
                            <option value="Brighton_%2526_Hove_Albion">Brighton & Hove Albion</option>
                        </select>
                    </div>
                    <div className="selection">
                        <label htmlFor="image-count">Image per Player</label>
                        <input type="number"
                               className="choices" name="image-count"
                               placeholder="Enter a number (1-10)"
                               value={imageCount} onChange={handleImageSelection} />
                    </div>
                </div>
                <div id="image-container">
                        <img id="team-logo"
                            src={logoMap[selectedTeam]}
                        />
                </div>
            </div>
            <div id="scrape-button-container">
                <Button text="Scrape" 
                        customFunction={() => scrape_images({
                                team: selectedTeam, 
                                image_count: `${imageCount}`,
                                update_scrape_status: handleScraping,
                                update_click_status: handleClick})}/>
                {isClicked && <Spinner />}
            </div>  
            
        </Card>
    )

  }
  
