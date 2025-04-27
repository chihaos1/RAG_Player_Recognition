import "./Scrape_Page.css";
import Button from "../UI/Button/Button.tsx";
import { useState } from 'react';

import  pl_logo from "../../assets/team_logos/PremierLeague.png"
import  newcastle_logo from "../../assets/team_logos/Newcastle.png"
import  west_ham_logo from "../../assets/team_logos/WestHam.png"
import  brighton_logo from "../../assets/team_logos/Brighton.png"

type TeamLogoMap = {
    default: string,
    newcastle: string,
    west_ham: string
    brighton: string
}
type ValidTeamOptions = "default" | "newcastle" | "west_ham" | "brighton"

export default function Scrape_Page() {
    const [selectedLogo, setLogoSelection] = useState<ValidTeamOptions>("default")
    const [imageCount, setImageCount] = useState<number>(5)

    const handleLogoSelection = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setLogoSelection(e.target.value as ValidTeamOptions)
    }

    const handleImageSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
        const imageCount = e.target.value as string
        const parsedImageCount = parseInt(imageCount)
        setImageCount(parsedImageCount)
    }

    const logoMap: TeamLogoMap = {
        default: pl_logo,
        newcastle: newcastle_logo,
        west_ham: west_ham_logo,
        brighton: brighton_logo,
    }

    return (
        <>
            <div id="scrape_page_title">
                <h2>Player Image Scraping</h2>
            </div>
            <div id="selection-container">
                <div id="scrape-container"> 
                    <div className="selection">
                        <label htmlFor="team-selection">Select a Team</label>
                        <select className="choices" name="team-selection" value={selectedLogo} onChange={handleLogoSelection}>
                            <option value="default" disabled>-</option>
                            <option value="newcastle">Newcastle United</option>
                            <option value="west_ham">West Ham United</option>
                            <option value="brighton">Brighton & Hove Albion</option>
                        </select>
                    </div>
                    <div className="selection">
                        <label htmlFor="image-count">Image per Player</label>
                        <input type="number"
                               className="choices" name="image-count"
                               placeholder="Enter a number (1-10)"
                               value={imageCount} onChange={handleImageSelection} />
                    </div>
                    {/* {error && <p>{error}</p>} */}
                </div>
                <div id="image-container">
                        <img id="team-logo"
                            src={logoMap[selectedLogo]}
                        />
                </div>
            </div>
            <div id="scrape-button-container">
                <Button text="Scrape"/>
            </div>
            
            
        </>

    )

  }
  