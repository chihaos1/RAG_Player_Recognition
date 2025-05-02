type EmbedImageProps = {
    update_embed_status: (embed_status: boolean) => void;
    update_click_status: (clickStatus: boolean) => void
}

export default async function embed_images({update_embed_status, update_click_status}: EmbedImageProps) {
    update_click_status(true)
    const response: Response = (
        await fetch('http://127.0.0.1:8082/embed/images'))
    if (response.ok) {
        update_embed_status(true) 
        console.log(await response.json())
    } else {
        throw new Error(`Request failed with status ${response.status}: ${response.statusText}`)
    }

    return 
}