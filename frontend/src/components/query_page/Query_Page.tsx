import "./Query_Page.css"
import Button from "../UI/Button/Button.tsx";
import Card from "../UI/Card/Card.tsx"
import { Spinner } from "../UI/Spinner/Spinner.tsx";
import query_images from "../utils/api/query.tsx";
import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Query_Page() {
	const [image, setImage] = useState<File | null>(null)
	const [previewURL, setPreviewURL] = useState<string | null>(null)
	const [isQueried, setQueryStatus] = useState<boolean>(false)
	const [queryResult, setQueryResult] = useState<string[] | null>(null)
	const [isClicked, setClickStatus] = useState<boolean>(false)
	const fileInputRef = useRef<HTMLInputElement | null>(null)
	const navigate = useNavigate();

	const handleDropImage = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
		if (event.dataTransfer.files && event.dataTransfer.files[0]) {
			const uploadedImage = event.dataTransfer.files[0]
			setImage(uploadedImage);
			setPreviewURL(URL.createObjectURL(uploadedImage))
		}
    };

	const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => { //Prevents the image from being opened by default by the browser
		event.preventDefault(); 
	}

	const handleUploadClick = () => {
		fileInputRef.current?.click()
	}

	const handleClickStatus = (clickStatus: boolean) => {
        setClickStatus(clickStatus)
    }

	const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => { 
		if (event.target.files && event.target.files[0]) {
			const uploadedImage = event.target.files[0]
			setImage(uploadedImage);
			setPreviewURL(URL.createObjectURL(uploadedImage))
		}
	}

	const handleQueryStatus = (query_status: boolean) => {
		setQueryStatus(query_status)
	}

	const handleQueryResult = (query_result: string[]) => {
		setQueryResult(query_result)
	}

	const handleReturnClick = () => {
		navigate("/")
	}

	return (
	  <Card background="third">
		{!isQueried && (
			<>
				<div className="query_page_title">
					<h2>Player Image Querying</h2>
				</div>
				<div id="query-container">
					<div id="image-dropbox" onClick={handleUploadClick} onDrop={handleDropImage} onDragOver={handleDragOver}>
					<input id="image-input" type="file" accept="image/*" ref={fileInputRef} onChange={handleFileChange}/>
					{previewURL ? (<img id="preview" src={previewURL}/>) : (<p>Drop an Image Here</p>)}
				</div>
					{image ? (<p id="image-name">Selected Image: {image.name}</p>): (<p></p>)}
				</div>
				<div id="query-button">
					<Button text="Query" customFunction={() => query_images({
															image, 
															update_query_status: handleQueryStatus,
															append_query_result: handleQueryResult,
															update_click_status: handleClickStatus})}/>
					{isClicked && <Spinner />}
				</div>
			</>
		)}
		{isQueried && (
			<>
				<div className="query_page_title">
					<h2>{queryResult![0]}</h2>
				</div>
				<div id="query-result-container">
					<div id="query-result">
						{(() => { 
							const bulletPoints = JSON.parse(queryResult![1]);
							return Object.entries(bulletPoints).map((bulletPoint) => {
								const sectionHeader = bulletPoint[0]
								const sectionContent: string[] = bulletPoint[1]
								return (
									<div id="summaries">
									<h3>{sectionHeader}</h3>
										{sectionContent.map((point, index) => (
										<p key={index}>{point}</p>
										))}
									</div>);
							})
						})()}
					</div>
					<div id="restart-button">
						<Button text="Restart" 
							customFunction={() => handleReturnClick()}/>
					</div>  	
				</div>
			</>
		)}
	  </Card>
	);
  }
