import "./Embed_Page.css"
import Button from "../ui/Button/Button.tsx";
import Card from "../ui/Card/Card.tsx"
import { Spinner } from "../ui/Spinner/Spinner.tsx";
import embed_images from "../utils/api/embed.tsx";
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import playerImg from '../../assets/images/Player.png'

type PlayerImages = { 
	[key: string]: number }

export default function Embed_Page() {
	const [isEmbed, setEmbedStatus] = useState<boolean>(false)
	const [isClicked, setClickStatus] = useState<boolean>(false)
	const location = useLocation() //Can access the state passed during navigation
	const playerImages: PlayerImages = location.state.scrapedData
	const navigate = useNavigate();

	const handleEmbedding = (embed_status: boolean) => {
        setEmbedStatus(embed_status)
    }

	const handleClick = (clickStatus: boolean) => {
        setClickStatus(clickStatus)
    }


	useEffect(() => {
		if (isEmbed) {
			navigate("/query")
		}
    }, [isEmbed])

	return (
	  <Card>
		<div id="embed_page_title">
                <h2>Player Image Embedding</h2>
        </div>
		<div id="scrape_results">
			{Object.entries(playerImages).map(([player, images]) => (
				<div className="player-container" key={player}>
					<img className="player-image" src={playerImg}/>
					<p>{player}</p>
					<p>{images} Images</p>
				</div>
			))}
		</div>
		<div id="scrape-button-container">
			<Button text="Embed" 
					customFunction={() => embed_images({
						update_embed_status: handleEmbedding,
						update_click_status: handleClick})}/>
			{isClicked && <Spinner />}
		</div>  
	  </Card>

	);
  }