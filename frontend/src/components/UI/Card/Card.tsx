import './Card.css'
import { type ReactNode } from "react";

type CardProps = {
    background: string;
    children: ReactNode
}

export default function Card({ background, children }: CardProps) {
    return (
        <div className={`card ${background}`}>
            {children}
        </div>
    )

}