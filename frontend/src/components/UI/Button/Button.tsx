type ButtonProps = {
    text: string;
    fn: () => void
}

export default function Button({text, fn}: ButtonProps) {

    return <button className="button">{text}</button>
}