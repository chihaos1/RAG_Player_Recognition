type QueryProps = {
    image: File | null;
    update_query_status: (query_status: boolean) => void;
    append_query_result: (query_result: string[]) => void;
    update_click_status: (clickStatus: boolean) => void;
}

export default async function query_images({image, update_query_status, append_query_result, update_click_status}: QueryProps) {
    update_click_status(true)
    if (!image) {
        throw new Error("Upload file was invalid")
        return
    }
    
    const formData = new FormData()
    formData.append('file', image);

    const response: Response = (
        await fetch("http://54.159.206.126:8000/query/image", {
            method: "POST",
            body: formData
        }))
    
    if (response.ok) {
        const data = await response.json()
        update_query_status(true)
        append_query_result(data)
        console.log(data)
        return data
    } else {
        throw new Error(`Upload failed: ${response.statusText}`)
    }
}
