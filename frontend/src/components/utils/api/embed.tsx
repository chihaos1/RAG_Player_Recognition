type EmbedImageProps = {
    update_embed_status: (embed_status: boolean) => void;
    update_click_status: (clickStatus: boolean) => void
}

export default async function embed_images({update_embed_status, update_click_status}: EmbedImageProps) {
    update_click_status(true)
    console.log("Started Embedding")
    const response: Response = (
        await fetch('http://54.159.206.126:8000/embed/images'))
    update_embed_status(true) 
    console.log(await response.json())

    return 
}
