type ButtonProps = {
    text: string;
    customFunction: () => unknown
}

export default function Button({text, customFunction}: ButtonProps) {

    return <button className="button" onClick={customFunction}>{text}</button>
}